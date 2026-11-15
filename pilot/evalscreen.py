"""evalscreen: screening of candidate evaluators on the stored labels, per-epoch logs and proxy scores of the benchst roots.

    python -m pilot.evalscreen base                 # the stored evaluators on the common measure
    python -m pilot.evalscreen proxy_combination    # a model on the proxy scores, fit on the other cities
    python -m pilot.evalscreen curve_rank           # a model on the first k epochs, fit on the other cities
    python -m pilot.evalscreen transfer             # cheap sources, the choice of the source, the headroom of transfer
    python -m pilot.evalscreen halving_prior        # successive halving with a prior
    python -m pilot.evalscreen active_labels        # an active choice of the labels at the target city
    python -m pilot.evalscreen space_cut            # a reduced search space learned from the other cities
    python -m pilot.evalscreen route                # probe trainings choose the recipe (reads the base and halving_prior tables)
    python -m pilot.evalscreen operator_traits      # a predictor on operator traits, city and operator family held out together
    python -m pilot.evalscreen label_share          # a sparse (architecture, city) label matrix shared by the cities
    python -m pilot.evalscreen variance             # the share of the label variance of each design axis, against the seed variance
    python -m pilot.evalscreen fresh_list --fresh results/freshlist/pemsbay_h12 --roots <source roots>   # a second list at a city: predictor,
                                                    # search-space rules, design axes and the top of the list; nothing is fit on it
    out = results/evalscreen/compare/tables

No training, no forward pass, no GPU.  Reads <root>/tables/joined.csv, <root>/train/<id>/seed*/metrics.json and
<root>/COST.json through pilot.evalcost and pilot.predictor; writes nothing into a root.

Common measure, "cost to one sigma": an evaluator ranks the list; the search trains its first b picks to the end (b in
BUDGETS) and keeps the best.  Cost = the epochs the evaluator trained plus the remaining epochs of the b picks, on the
reference unit (logged hours / cost_ratio).  The cost to one sigma is the cost at the smallest b whose best pick lies within
one sigma_seed of the best test MAE of the list; pct = that cost as a share of training the whole list.  sigma_seed = std of
the test MAE over seeds 0 to 2, mean over the architectures that have three seeds (count in the meta file).

Robust form: the same measure on N_SUB random subsets of SUB_SIZE architectures (the same subsets for every evaluator; the
evaluator runs again inside each subset).  sub_share = the share of subsets where some b meets the line; sub_pct_median = the
median cost share over the subsets, empty when fewer than half of them meet the line.  A cell that rests on one lucky pick
has a low sub_share.

Every learned score is fit on the other cities (target = within-city rank of -test MAE) and scored on the held-out city.
Every Spearman is reported over all heads and inside each head (n-weighted mean, stratified bootstrap CI).
Sign convention as in pilot.evalcost: a score is correlated with -MAE; the pick is argmax.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, rankdata, spearmanr

from pilot import evalcost as ec
from pilot import predictor as pr
from pilot.paths import Root

ROOTS = ["results/benchst/metrla_h12", "results/benchst/pems04_h12", "results/benchst/chengdu_h12", "results/benchst/shenzhen_h12"]
OUT = "results/evalscreen/compare/tables"
BUDGETS = [1, 2, 3, 5, 8, 10]
KS = [1, 2, 3, 4, 5, 6, 8, 10]
SH_SETTINGS = [(1, 3), (1, 2), (2, 3), (2, 2), (3, 3), (3, 2)]          # (r0, eta); (1, 3) is the reference recipe
FILTER_PROXIES = ["zico", "zico_sizectrl"]
FILTER_KS = [1, 3, 5]
HEADS = ["mae", "mse", "quantile"]
LATE_K = 3                                                             # a city is "late" when early validation needs k > LATE_K
TARGET = "test_mae"
N_SUB, SUB_SIZE, SUB_SEED = 200, 100, 0
PROXY_NAMES = ["params", "flops", "l2_norm", "l2_norm_all", "grad_norm", "grad_norm_all", "snip", "snip_all", "plain", "plain_all", "fisher",
               "synflow", "synflow_all", "jacov", "nwot", "nwot_per_layer", "swap", "swap_b8", "zen", "grasp", "grasp_all",
               "zico", "zico_t", "zico_s", "glass", "glass_t", "glass_s"]
ZICO_FAMILY = ["zico", "zico_t", "zico_s", "glass", "glass_t", "glass_s", "params"]
CURVE_KS = [1, 2, 3, 5]
FIT_SEEDS = (0, 1, 2)


# ---------------------------------------------------------------- small helpers
def zscore(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float); ok = np.isfinite(v)
    out = np.zeros(len(v)); sd = np.std(v[ok]) if ok.any() else 0.0
    if sd > 0:
        out[ok] = (v[ok] - np.mean(v[ok])) / sd
    return out


def order_of(score: np.ndarray) -> np.ndarray:
    """Indices by descending score; a missing score goes last."""
    s = np.asarray(score, dtype=float)
    return np.argsort(-np.where(np.isfinite(s), s, -np.inf), kind="stable")


def rho(a: np.ndarray, b: np.ndarray) -> float:
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 4 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return float("nan")
    return float(spearmanr(a[m], b[m]).correlation)


def unit_rank(v: np.ndarray) -> np.ndarray:
    """Rank in [0, 1] inside the given set; a missing value goes to the middle."""
    v = np.asarray(v, dtype=float); r = np.full(len(v), 0.5); ok = np.isfinite(v)
    if ok.sum() > 1:
        r[ok] = (rankdata(v[ok]) - 1) / (ok.sum() - 1)
    return r


# ---------------------------------------------------------------- one city as arrays
@dataclass
class City:
    name: str
    df: pd.DataFrame
    val: list            # per architecture: val MAE per epoch
    trn: list            # per architecture: train loss per epoch
    cumh: list           # per architecture: cumulative hours, cumh[i][e] = hours of the first e epochs
    meta: dict
    subs: list = field(default_factory=list)

    def __post_init__(self):
        self.ids = list(self.df.arch_id); self.n = len(self.ids)
        self.y = self.df[TARGET].values.astype(float); self.head = self.df["head"].values
        self.full_h = np.array([c[-1] for c in self.cumh]); self.sigma = self.meta["sigma_seed"]; self.ratio = self.meta["cost_ratio"]
        self.max_ep = self.meta["max_epochs"]; self.length = np.array([len(v) for v in self.val])
        rng = np.random.default_rng(SUB_SEED)
        self.subs = [np.sort(rng.choice(self.n, min(SUB_SIZE, self.n), replace=False)) for _ in range(N_SUB)]
        self.index = {a: i for i, a in enumerate(self.ids)}

    def hours(self, done: np.ndarray, idx: np.ndarray) -> np.ndarray:
        return np.array([self.cumh[i][min(int(done[i]), self.length[i])] for i in idx])

    def val_at(self, k: int) -> np.ndarray:
        return np.array([v[min(k, len(v)) - 1] for v in self.val])

    def align(self, ser: pd.Series) -> np.ndarray:
        return np.array([float(ser[a]) if a in ser.index else np.nan for a in self.ids])


def city_key(r: Root) -> str:
    """The key of a root in every table: the dataset for a benchst root (so the stored tables keep their names), else
    <experiment>/<dataset>, so that two roots of one city (a second list) do not collide."""
    exp = r.dir.parent.name
    return r.dataset if exp == "benchst" else f"{exp}/{r.dataset}"


def load_cities(roots: list[Root]) -> dict:
    out = {}
    for r in roots:
        df, aux = ec.load_root(r, TARGET); cost = ec.load_cost(r); curves = aux["curves"]
        val = [curves[a].val_mae.values.astype(float) for a in df.arch_id]
        trn = [curves[a].train_loss.values.astype(float) for a in df.arch_id]
        cumh = [np.concatenate([[0.0], np.cumsum(curves[a].seconds.values.astype(float))]) / 3600 for a in df.arch_id]
        k = city_key(r)
        out[k] = City(k, df, val, trn, cumh, {**aux["meta"], **cost, "dataset": r.dataset, "experiment": r.dir.parent.name})
    return out


# ---------------------------------------------------------------- evaluators: f(city, subset) -> (order, epochs trained)
def score_eval(score: np.ndarray, k: int = 0):
    def run(c: City, sub: np.ndarray):
        done = np.zeros(c.n, dtype=int); done[sub] = np.minimum(k, c.length[sub])
        return sub[order_of(score[sub])], done
    return run


def random_eval(seed: int = 0):
    def run(c: City, sub: np.ndarray):
        rng = np.random.default_rng([seed, int(sub.sum())])
        return rng.permutation(sub), np.zeros(c.n, dtype=int)
    return run


def halving_eval(r0: int, eta: int, prior: np.ndarray | None = None, weights: list | None = None, info: dict | None = None):
    """Successive halving on the logged curves.  Rung j trains the survivors to r0 * eta**j epochs (capped) and keeps the
    top 1/eta.  The rung score is -val MAE, or (1 - w) z(-val MAE) + w z(prior) with w = weights[j] when a prior is given.
    The order lists the survivors first, then the cut lists from the last rung back."""
    def run(c: City, sub: np.ndarray):
        alive = list(sub); done = np.zeros(c.n, dtype=int); budget, rnd, tail, first_cut = r0, 0, [], []
        while True:
            budget = min(budget, c.max_ep); a = np.array(alive)
            done[a] = np.maximum(done[a], np.minimum(budget, c.length[a]))
            score = -np.array([c.val[i][done[i] - 1] for i in a])
            w = weights[rnd] if (prior is not None and weights is not None and rnd < len(weights)) else 0.0
            if w > 0:
                score = (1 - w) * zscore(score) + w * zscore(prior[a])
            ordered = list(a[order_of(score)])
            if len(alive) == 1 or budget >= c.max_ep:
                break
            keep = max(1, len(alive) // eta)
            if rnd == 0:
                first_cut = ordered[keep:]
            tail = ordered[keep:] + tail; alive = ordered[:keep]; budget *= eta; rnd += 1
        if info is not None:
            info.update(first_cut=first_cut, rounds=rnd + 1)
        return np.array(ordered + tail), done
    return run


def filter_eval(proxy: np.ndarray, k: int, info: dict | None = None):
    """Top half by proxy, then early validation at k epochs on that half.  The bottom half follows in proxy order."""
    def run(c: City, sub: np.ndarray):
        o = sub[order_of(proxy[sub])]; half = len(o) // 2; top, bottom = o[:half], o[half:]
        done = np.zeros(c.n, dtype=int); done[top] = np.minimum(k, c.length[top])
        val = -np.array([c.val[i][done[i] - 1] for i in top])
        if info is not None:
            info.update(bottom=list(bottom))
        return np.concatenate([top[order_of(val)], bottom]), done
    return run


# ---------------------------------------------------------------- the common measure
def budget_rows(c: City, sub: np.ndarray, order: np.ndarray, done: np.ndarray) -> list[dict]:
    y = c.y; best = float(y[sub].min()); spent = float(c.hours(done, sub).sum())
    rk = {i: r for i, r in zip(sub, (rankdata(y[sub]) - 1) / max(len(sub) - 1, 1) * 100)}
    rows = []
    for b in BUDGETS:
        pick = order[:min(b, len(order))]
        rows.append({"budget": b, "gpu_hours": spent + float(np.clip(c.full_h[pick] - c.hours(done, pick), 0, None).sum()),
                     "regret": float(y[pick].min() - best), "best_rank_pct": float(min(rk[i] for i in pick))})
    return rows


def first_hit(rows: list[dict], tol: float) -> tuple[float, float]:
    for r in rows:
        if r["regret"] <= tol + 1e-12:
            return r["budget"], r["gpu_hours"]
    return np.nan, np.nan


def measure(c: City, ev, expected_random: bool = False) -> tuple[list[dict], dict]:
    """Full-list budget rows and the summary with the robust columns."""
    full = np.arange(c.n); total = float(c.full_h.sum()); tol = c.sigma if c.sigma and np.isfinite(c.sigma) else 0.0
    if expected_random:
        rng = np.random.default_rng(0); best = float(c.y.min())
        rows = [{"budget": b, "gpu_hours": b * float(c.full_h.mean()), "best_rank_pct": np.nan,
                 "regret": float(np.mean([c.y[rng.choice(c.n, b, replace=False)].min() for _ in range(5000)]) - best)} for b in BUDGETS]
    else:
        rows = budget_rows(c, full, *ev(c, full))
    s = {"regret_b1": rows[0]["regret"], "regret_b1_sigma": rows[0]["regret"] / tol if tol else np.nan, "rank_pct_b1": rows[0]["best_rank_pct"],
         "regret_b5": [r for r in rows if r["budget"] == 5][0]["regret"]}
    for tag, t in (("sigma", tol), ("zero", 0.0)):
        b, h = first_hit(rows, t)
        s[f"b_{tag}"] = b; s[f"hours_{tag}_ref"] = h / c.ratio if np.isfinite(h) else np.nan; s[f"pct_{tag}"] = h / total * 100 if np.isfinite(h) else np.nan
    pcts, bs = [], []
    for sub in c.subs:
        b, h = first_hit(budget_rows(c, sub, *ev(c, sub)), tol)
        pcts.append(h / float(c.full_h[sub].sum()) * 100 if np.isfinite(h) else np.inf); bs.append(b if np.isfinite(b) else np.inf)
    pcts, bs = np.array(pcts), np.array(bs)
    s["sub_share"] = float(np.mean(np.isfinite(pcts)))
    s["sub_pct_median"] = float(np.median(pcts)) if np.isfinite(np.median(pcts)) else np.nan
    s["sub_b_median"] = float(np.median(bs)) if np.isfinite(np.median(bs)) else np.nan
    return rows, s


# ---------------------------------------------------------------- head control
def within_head(c: City, score: np.ndarray, idx: dict | None = None) -> float:
    y = -c.y; rs, ws = [], []
    for h in HEADS:
        i = np.where(c.head == h)[0] if idx is None else idx[h]
        r = rho(score[i], y[i])
        if np.isfinite(r):
            rs.append(r); ws.append(len(i))
    return float(np.average(rs, weights=ws)) if ws else float("nan")


def head_block(c: City, score: np.ndarray, n_boot: int = 300, seed: int = 0) -> dict:
    y = -c.y; idx = {h: np.where(c.head == h)[0] for h in HEADS}
    out = {"rho_all": rho(score, y), **{f"rho_{h}": rho(score[idx[h]], y[idx[h]]) for h in HEADS}, "rho_within_head": within_head(c, score)}
    rng = np.random.default_rng(seed)
    boots = [within_head(c, score, {h: rng.choice(idx[h], len(idx[h])) for h in HEADS}) for _ in range(n_boot)]
    out["within_ci_lo"], out["within_ci_hi"] = float(np.nanpercentile(boots, 2.5)), float(np.nanpercentile(boots, 97.5))
    m = idx["mae"]                                                     # the pick inside the MAE-head architectures alone
    if len(m) >= 8 and np.isfinite(score[m]).sum() >= 4:
        ym = c.y[m]; pick = order_of(score[m])[0]
        out["mae_head_regret_sigma"] = float(ym[pick] - ym.min()) / c.sigma if c.sigma else np.nan
        out["mae_head_rank_pct"] = float((rankdata(ym)[pick] - 1) / max(len(ym) - 1, 1) * 100)
    return out


def paired_within_diff(c: City, s1: np.ndarray, s2: np.ndarray, n_boot: int = 1000, seed: int = 0) -> dict:
    """Within-head rho of s1 minus that of s2, on the same stratified resamples."""
    idx = {h: np.where(c.head == h)[0] for h in HEADS}; rng = np.random.default_rng(seed); d = []
    for _ in range(n_boot):
        b = {h: rng.choice(idx[h], len(idx[h])) for h in HEADS}
        d.append(within_head(c, s1, b) - within_head(c, s2, b))
    return {"diff": within_head(c, s1) - within_head(c, s2), "diff_ci_lo": float(np.nanpercentile(d, 2.5)), "diff_ci_hi": float(np.nanpercentile(d, 97.5))}


# ---------------------------------------------------------------- models fit on the other cities
def rank_target(c: City) -> np.ndarray:
    return unit_rank(-c.y)


def fit_loco(cities: dict, feats: dict, kind: str, drop: dict | None = None) -> dict:
    """feats[city] = feature matrix (rows in the order of the city's list).  For each held-out city, fit on the other cities
    (minus the rows flagged in drop[city]) and predict every architecture of the held-out city."""
    out = {}
    for held in cities:
        Xtr, ytr = [], []
        for k, c in cities.items():
            if k == held:
                continue
            keep = np.ones(c.n, bool) if drop is None else ~drop[k]
            Xtr.append(feats[k][keep]); ytr.append(rank_target(c)[keep])
        Xtr, ytr = np.vstack(Xtr), np.concatenate(ytr)
        out[held] = pr.fit_predict("ridge", Xtr, ytr, feats[held]) if kind == "ridge" else np.mean([pr.fit_predict("gbr", Xtr, ytr, feats[held], s) for s in FIT_SEEDS], axis=0)
    return out


def head_onehot(c: City) -> np.ndarray:
    return np.column_stack([(c.head == h).astype(float) for h in HEADS])


def proxy_matrix(c: City, names: list) -> np.ndarray:
    return np.column_stack([unit_rank(c.df[p].values.astype(float)) if p in c.df else np.full(c.n, 0.5) for p in names])


def arch_matrices(roots: list[Root], cities: dict) -> dict:
    """The operator-count encoding of pilot.predictor, aligned to the city lists."""
    raw = {city_key(r): pr.load_city(r) for r in roots}
    cols = sorted(set().union(*[set(d.columns) - pr.META_COLS for d in raw.values()]) - {c for d in raw.values() for c in d.columns if c.startswith("px_")})
    out = {}
    for k, d in raw.items():
        for col in cols:
            if col not in d:
                d[col] = 0
        out[k] = d.set_index("arch_id").loc[cities[k].ids, cols].values.astype(float)
    return out


class Sink:
    """Collects the measure and the head control of every evaluator of one run."""
    def __init__(self):
        self.cost, self.budget, self.head = [], [], []

    def add(self, c: City, name: str, kind: str, ev, score: np.ndarray | None = None, extra: dict | None = None, expected_random: bool = False):
        rows, s = measure(c, ev, expected_random)
        for r in rows:
            self.budget.append({"city": c.name, "evaluator": name, "kind": kind, **r, "gpu_hours_ref": r["gpu_hours"] / c.ratio})
        self.cost.append({"city": c.name, "evaluator": name, "kind": kind, **s, **(extra or {})})
        if score is not None:
            self.head.append({"city": c.name, "evaluator": name, "kind": kind, **head_block(c, np.asarray(score, dtype=float))})

    def frames(self):
        return pd.DataFrame(self.cost), pd.DataFrame(self.budget), pd.DataFrame(self.head)


COST_COLS = ["evaluator", "kind", "regret_b1_sigma", "rank_pct_b1", "b_sigma", "hours_sigma_ref", "pct_sigma", "sub_share", "sub_pct_median", "sub_b_median"]
HEAD_COLS = ["evaluator", "kind", "rho_all", "rho_within_head", "within_ci_lo", "within_ci_hi", "rho_mae", "rho_mse", "rho_quantile", "mae_head_regret_sigma", "mae_head_rank_pct"]
MEASURE_NOTE = ("b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining "
                "epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. "
                f"sub_share = the share of {N_SUB} random subsets of {SUB_SIZE} architectures where some b meets the line; sub_pct_median = the median cost share over the "
                "subsets, empty when fewer than half meet the line.")


def pooled_transfer(cities: dict, held: str) -> np.ndarray:
    c = cities[held]; ranks = []
    for k, s in cities.items():
        if k != held:
            ranks.append(unit_rank(c.align(pd.Series(-s.y, index=s.ids))))
    return np.mean(ranks, axis=0)


# ---------------------------------------------------------------- base: the stored evaluators
def convergence(c: City) -> tuple[list[dict], dict]:
    y = -c.y; best_ep = np.array([int(np.argmin(v)) + 1 for v in c.val]); rows = []
    for h in ["all"] + HEADS:
        m = np.ones(c.n, bool) if h == "all" else c.head == h
        rows.append({"city": c.name, "head": h, "n": int(m.sum()), "median_best_epoch": float(np.median(best_ep[m])), "share_stopped_early": float(np.mean(c.length[m] < c.max_ep))})
    k_all = k_in = np.nan; per_k = {}
    for k in range(1, c.max_ep + 1):
        s = -c.val_at(k); per_k[k] = (rho(s, y), within_head(c, s))
        if np.isnan(k_all) and per_k[k][0] >= 0.6:
            k_all = k
        if np.isnan(k_in) and per_k[k][1] >= 0.6:
            k_in = k
    return rows, {"city": c.name, "k_rho06_all_heads": k_all, "k_rho06_within_head": k_in, "late": bool(np.isnan(k_in) or k_in > LATE_K),
                  **{f"rho_within_k{k}": per_k[k][1] for k in (1, 2, 3, 5)}}


def run_base(roots: list[Root], cities: dict, out: Path) -> None:
    arch = arch_matrices(roots, cities)
    px = {k: proxy_matrix(c, pr.PROXY_FEATS) for k, c in cities.items()}
    loco = {"loco_ridge_arch": fit_loco(cities, arch, "ridge"), "loco_gbr_arch": fit_loco(cities, arch, "gbr"),
            "loco_gbr_proxies": fit_loco(cities, px, "gbr"), "loco_gbr_arch_proxies": fit_loco(cities, {k: np.c_[arch[k], px[k]] for k in cities}, "gbr")}
    sink = Sink(); conv_rows, flags = [], []
    for name, c in cities.items():
        top15 = set(np.argsort(c.y)[:max(1, c.n // 10)]); full = np.arange(c.n)
        sink.add(c, "random", "floor", random_eval(), expected_random=True)
        for p in dict.fromkeys(ec.FLOORS + ec.PROXIES + ["grasp_all"]):
            if p in c.df and c.df[p].notna().sum() >= 8:
                s = c.df[p].values.astype(float)
                sink.add(c, p, "floor" if p in ec.FLOORS else "zero-cost proxy", score_eval(s), s)
        for k in KS:
            s = -c.val_at(k); sink.add(c, f"early_val_k{k}", "brief training", score_eval(s, k), s, {"k": k})
        for r0, eta in SH_SETTINGS:
            info = {}; halving_eval(r0, eta, info=info)(c, full)
            sink.add(c, f"sh_r{r0}_eta{eta}", "successive halving", halving_eval(r0, eta), extra={"top10pct_dropped_first_rung": int(len(top15 & set(info["first_cut"]))), "rounds": info["rounds"]})
        for p in FILTER_PROXIES:
            if p in c.df:
                s = c.df[p].values.astype(float)
                for k in FILTER_KS:
                    info = {}; filter_eval(s, k, info)(c, full)
                    sink.add(c, f"{p}_half_then_k{k}", "proxy filter", filter_eval(s, k), extra={"top10pct_in_bottom_half": int(len(top15 & set(info["bottom"]))), "k": k})
        for src, S in cities.items():
            if src != name:
                s = c.align(pd.Series(-S.y, index=S.ids)); sink.add(c, f"transfer_from_{src}", "transfer", score_eval(s), s)
        s = pooled_transfer(cities, name); sink.add(c, "transfer_pooled", "transfer", score_eval(s), s)
        for ln, pred in loco.items():
            sink.add(c, ln, "predictor, other cities", score_eval(pred[name]), pred[name])
        sink.add(c, "full_training", "ceiling", score_eval(-c.y, c.max_ep), -c.y)
        rows, flag = convergence(c); conv_rows += rows; flags.append(flag)
        c.meta["full_hours_ref"] = float(c.full_h.sum()) / c.ratio
    ct, bt, ht = sink.frames(); cv = pd.DataFrame(conv_rows).merge(pd.DataFrame(flags), on="city")
    ct.to_csv(out / "base_cost_to_sigma.csv", index=False); bt.to_csv(out / "base_budget.csv", index=False)
    ht.to_csv(out / "base_head_control.csv", index=False); cv.to_csv(out / "base_convergence.csv", index=False)
    metas = {k: dict(c.meta) for k, c in cities.items()}
    json.dump({"target": TARGET, "budgets": BUDGETS, "late_k": LATE_K, "n_sub": N_SUB, "sub_size": SUB_SIZE, "cities": metas}, open(out / "evalscreen_meta.json", "w"), indent=1)
    doc = ["# evalscreen base: the stored evaluators on the common measure", "",
           f"Target = {TARGET}, seed 0, zero-masked pipeline, shared list. b in {BUDGETS}. " + MEASURE_NOTE + " random is an expectation over draws on the full list.", ""]
    for k, m in metas.items():
        doc.append(f"- {k}: N = {m['n']}, sigma_seed = {m['sigma_seed']:.4f} over {m['sigma_seed_n_arch']} architectures, whole list {m['full_hours_ref']:.1f} GPU-hours "
                   f"(reference unit; cost_ratio {m['cost_ratio']:.2f}, {m['cluster']})")
    doc.append("")
    for k in metas:
        doc.append(ec.md(ct[ct.city == k].sort_values(["sub_pct_median", "pct_sigma"], na_position="last"), COST_COLS, f"{k}: cost to one sigma, cheapest robust form first"))
        doc.append(ec.md(ht[ht.city == k].sort_values("rho_within_head", ascending=False), HEAD_COLS, f"{k}: head control, Spearman with -{TARGET}",
                         "rho_within_head = n-weighted mean of the three heads, with a stratified bootstrap CI; mae_head_* = the pick among the MAE-head architectures alone."))
    doc.append(ec.md(cv, ["city", "head", "n", "median_best_epoch", "share_stopped_early", "k_rho06_all_heads", "k_rho06_within_head", "late", "rho_within_k1", "rho_within_k2", "rho_within_k3", "rho_within_k5"],
                     "Convergence", f"k_rho06_* = the smallest k at which early validation reaches rho >= 0.6; late = the within-head k is above {LATE_K}."))
    (out / "evalscreen_base.md").write_text("\n".join(doc))


# ---------------------------------------------------------------- proxy_combination: a model on the proxy scores
def best_single_proxy(c: City) -> tuple[str, np.ndarray, float]:
    best = (None, None, -np.inf)
    for p in PROXY_NAMES:
        if p in c.df:
            s = c.df[p].values.astype(float); r = within_head(c, s)
            if np.isfinite(r) and r > best[2]:
                best = (p, s, r)
    return best


def family_rows(cities: dict, feats: dict, kind: str, label: str, min_n: int = 8) -> list[dict]:
    """Leave one city and one operator family out together: the family is removed from the training cities and scored at the
    held-out city.  Kendall tau with -test MAE on the held-out family."""
    rows = []
    for col in ("seq_family", "graph_family"):
        fams = sorted(set().union(*[set(c.df[col]) for c in cities.values()]))
        for fam in fams:
            drop = {k: (c.df[col] == fam).values for k, c in cities.items()}
            if all(d.sum() < min_n for d in drop.values()):
                continue
            pred = fit_loco(cities, feats, kind, drop)
            for held, c in cities.items():
                te = drop[held]
                if te.sum() >= min_n:
                    rows.append({"city": held, "model": label, "family_kind": col, "held_out_family": fam, "n": int(te.sum()),
                                 "kendall": float(kendalltau(pred[held][te], -c.y[te]).correlation), "spearman": rho(pred[held][te], -c.y[te])})
    return rows


def run_proxy_combination(roots: list[Root], cities: dict, out: Path) -> None:
    sets = {"proxies_head": lambda c: np.c_[proxy_matrix(c, PROXY_NAMES), head_onehot(c)], "proxies": lambda c: proxy_matrix(c, PROXY_NAMES),
            "zico_family_params": lambda c: proxy_matrix(c, ZICO_FAMILY)}
    arch = arch_matrices(roots, cities)
    sink = Sink(); cmp_rows, fam_rows = [], []
    for sname, f in sets.items():
        feats = {k: f(c) for k, c in cities.items()}
        for kind in ("ridge", "gbr"):
            label = f"{kind}_{sname}"; pred = fit_loco(cities, feats, kind)
            for name, c in cities.items():
                sink.add(c, label, "proxy combination, other cities", score_eval(pred[name]), pred[name])
                bp, bs, br = best_single_proxy(c)
                cmp_rows.append({"city": name, "model": label, "rho_within_head": within_head(c, pred[name]), "best_single_proxy": bp, "best_single_within": br,
                                 **paired_within_diff(c, pred[name], bs)})
            fam_rows += family_rows(cities, feats, kind, label)
    for kind in ("ridge", "gbr"):                                      # the reference: the operator-count encoding under the same family test
        fam_rows += family_rows(cities, arch, kind, f"{kind}_operator_counts")
    for name, c in cities.items():                                     # references on the same measure
        s = pooled_transfer(cities, name); sink.add(c, "transfer_pooled", "transfer", score_eval(s), s)
        bp, bs, _ = best_single_proxy(c); sink.add(c, f"best_single_proxy ({bp})", "zero-cost proxy", score_eval(bs), bs)
    ct, _, ht = sink.frames(); cm, fm = pd.DataFrame(cmp_rows), pd.DataFrame(fam_rows)
    agg = fm.groupby(["city", "model"]).apply(lambda g: pd.Series({"families": len(g), "kendall_weighted": np.average(g.kendall, weights=g.n),
                                                                  "families_ge_0.5": int((g.kendall >= 0.5).sum())})).reset_index()
    gru = fm[fm.held_out_family == "gru"].pivot(index="model", columns="city", values="kendall").reset_index()
    cm["clause_rho"] = (cm.rho_within_head >= 0.5) & (cm["diff"] > 0); cm["ci_excludes_0"] = cm.diff_ci_lo > 0
    verdict = cm.groupby("model").agg(cities_rho_ge_05_and_above=("clause_rho", "sum"), cities_ci_excludes_0=("ci_excludes_0", "sum")).reset_index()
    verdict = verdict.merge(agg.assign(ok=agg.kendall_weighted >= 0.5).groupby("model").ok.sum().rename("cities_family_kendall_ge_05").reset_index(), on="model", how="left")
    verdict["pass"] = (verdict.cities_rho_ge_05_and_above >= 3) & (verdict.cities_ci_excludes_0 >= 2) & (verdict.cities_family_kendall_ge_05 >= 3)
    for n_, t in (("cost", ct), ("head", ht), ("compare", cm), ("family", fm), ("family_summary", agg), ("verdict", verdict)):
        t.to_csv(out / f"proxy_combination_{n_}.csv", index=False)
    doc = ["# evalscreen proxy_combination: a model on the proxy scores, fit on the other cities", "",
           f"Inputs: the {len(PROXY_NAMES)} stored scores as ranks inside the city (set `proxies`), with the head one-hot (`proxies_head`), or the ZiCo family and the parameter "
           "count alone (`zico_family_params`). Models: ridge, gradient boosting (300 trees, depth 3, mean of 3 fit seeds). Target of the fit: within-city rank of -test MAE of the "
           "three training cities. Pass: inside the heads rho >= 0.5 and above the best single proxy at three of four cities, the paired CI of the difference excludes 0 at two "
           "cities or more, and the n-weighted Kendall on a held-out family at the held-out city is >= 0.5 at three of four cities. The best single proxy is chosen with the labels "
           "of the held-out city, which favours the baseline.", ""]
    doc.append(ec.md(verdict, list(verdict.columns), "Verdict per model"))
    doc.append(ec.md(cm, ["city", "model", "rho_within_head", "best_single_proxy", "best_single_within", "diff", "diff_ci_lo", "diff_ci_hi"], "Inside the heads: the model against the best single proxy",
                     "diff = within-head rho of the model minus that of the best single proxy; CI from 1000 paired stratified resamples."))
    doc.append(ec.md(agg, ["city", "model", "families", "kendall_weighted", "families_ge_0.5"], "City and operator family held out together", "Kendall with -test MAE on the held-out family at the held-out city; n-weighted over the families with 8 architectures or more."))
    doc.append(ec.md(gru, list(gru.columns), "Kendall on the held-out gru family"))
    for k in cities:
        doc.append(ec.md(ct[ct.city == k].sort_values(["sub_pct_median", "pct_sigma"], na_position="last"), COST_COLS, f"{k}: cost to one sigma", MEASURE_NOTE))
        doc.append(ec.md(ht[ht.city == k].sort_values("rho_within_head", ascending=False), HEAD_COLS, f"{k}: head control"))
    (out / "evalscreen_proxy_combination.md").write_text("\n".join(doc))
    print(verdict.to_string(index=False)); print(cm.to_string(index=False, float_format=lambda v: f"{v:.2f}"))


# ---------------------------------------------------------------- curve_rank: a model on the first k epochs
def curve_features(c: City, k: int) -> np.ndarray:
    """Ranks inside the city of the val MAE and the train loss at each of the first k epochs, of their change from epoch 1 to
    k, the rank of the last two inside the head, and the head one-hot."""
    V = np.column_stack([c.val_at(e) for e in range(1, k + 1)]); T = np.column_stack([np.array([t[min(e, len(t)) - 1] for t in c.trn]) for e in range(1, k + 1)])
    cols = [unit_rank(V[:, e]) for e in range(k)] + [unit_rank(T[:, e]) for e in range(k)]
    if k > 1:
        cols += [unit_rank(V[:, -1] / V[:, 0]), unit_rank(T[:, -1] / T[:, 0])]
    for M in (V, T):
        r = np.full(c.n, 0.5)
        for h in HEADS:
            m = c.head == h; r[m] = unit_rank(M[m, -1])
        cols.append(r)
    return np.c_[np.column_stack(cols), head_onehot(c)]


def inverse_epoch_extrapolation(c: City, k: int, to: int = 20) -> np.ndarray:
    """Least-squares fit of val(e) = a + b / e on the first k epochs, read at epoch `to`.  No fit across cities."""
    e = np.arange(1, k + 1); A = np.c_[np.ones(k), 1 / e]; out = []
    for v in c.val:
        a, b = np.linalg.lstsq(A, v[:k] if len(v) >= k else np.r_[v, np.full(k - len(v), v[-1])], rcond=None)[0]
        out.append(-(a + b / to))
    return np.array(out)


def loss_sum_within_head(c: City, k: int) -> np.ndarray:
    """Sum of the train loss over the first k epochs, z-scored inside each head (the losses of the heads have different scales)."""
    s = np.array([-float(np.sum(t[:k])) for t in c.trn]); out = np.zeros(c.n)
    for h in HEADS:
        m = c.head == h; out[m] = zscore(s[m])
    return out


def run_curve_rank(roots: list[Root], cities: dict, out: Path) -> None:
    sink = Sink(); cmp_rows = []
    for k in CURVE_KS:
        feats = {n_: curve_features(c, k) for n_, c in cities.items()}
        preds = {f"ridge_curve_k{k}": fit_loco(cities, feats, "ridge"), f"gbr_curve_k{k}": fit_loco(cities, feats, "gbr")}
        for name, c in cities.items():
            base = -c.val_at(k)
            cand = {**{m: p[name] for m, p in preds.items()}, f"loss_sum_k{k}": loss_sum_within_head(c, k)}
            if k >= 2:
                cand[f"inverse_epoch_k{k}"] = inverse_epoch_extrapolation(c, k)
            sink.add(c, f"early_val_k{k}", "brief training", score_eval(base, k), base, {"k": k})
            for m, s in cand.items():
                kind = "curve model, other cities" if "curve" in m else ("extrapolation, no fit" if "inverse" in m else "train-loss sum")
                sink.add(c, m, kind, score_eval(s, k), s, {"k": k})
                cmp_rows.append({"city": name, "k": k, "model": m.rsplit("_k", 1)[0], "rho_within_head": within_head(c, s), "early_val_within": within_head(c, base),
                                 **paired_within_diff(c, s, base)})
    for name, c in cities.items():
        s = pooled_transfer(cities, name); sink.add(c, "transfer_pooled", "transfer", score_eval(s), s)
    ct, _, ht = sink.frames(); cm = pd.DataFrame(cmp_rows)
    v = []
    for m, g in cm.groupby("model"):
        g3 = g[g.k <= 3]; best = g3.groupby("city").rho_within_head.max()
        above = g3.groupby("city").apply(lambda t: bool(((t.rho_within_head >= 0.6) & (t["diff"] > 0)).any()))
        v.append({"model": m, "cities_rho_ge_06_at_k_le_3": int((best >= 0.6).sum()), "cities_ge_06_and_above_early_val": int(above.sum()),
                  "cities_above_early_val_at_k3": int((g[g.k == 3]["diff"] > 0).sum()), "cities_ci_excludes_0_at_k3": int((g[g.k == 3].diff_ci_lo > 0).sum())})
    verdict = pd.DataFrame(v); verdict["pass"] = (verdict.cities_rho_ge_06_at_k_le_3 >= 3) & (verdict.cities_above_early_val_at_k3 >= len(cities))
    for n_, t in (("cost", ct), ("head", ht), ("compare", cm), ("verdict", verdict)):
        t.to_csv(out / f"curve_rank_{n_}.csv", index=False)
    doc = ["# evalscreen curve_rank: a model on the first k epochs, fit on the other cities", "",
           "Inputs: ranks inside the city of the val MAE and the train loss at each of the first k epochs, their change from epoch 1 to k, the rank of the last two inside the head, "
           "and the head one-hot. Models: ridge, gradient boosting, fit on three cities, scored on the fourth. inverse_epoch = a least-squares fit of val(e) = a + b / e per run, read "
           "at epoch 20, with no fit across cities. loss_sum = the sum of the train loss over the first k epochs, z-scored inside each head. Every score costs k epochs of the whole "
           "list. Pass: inside the heads rho >= 0.6 at k <= 3 at three of four cities, and above early validation at the same k at every late city (all four, see base).", ""]
    doc.append(ec.md(verdict, list(verdict.columns), "Verdict per model"))
    piv = cm.pivot_table(index=["model", "k"], columns="city", values="rho_within_head").reset_index()
    doc.append(ec.md(piv, list(piv.columns), "Spearman inside the heads, by k"))
    ev = cm[cm.model == cm.model.iloc[0]].pivot_table(index="k", columns="city", values="early_val_within").reset_index()
    doc.append(ec.md(ev, list(ev.columns), "Early validation inside the heads, by k (the baseline)"))
    doc.append(ec.md(cm, ["city", "k", "model", "rho_within_head", "early_val_within", "diff", "diff_ci_lo", "diff_ci_hi"], "Against early validation at the same k", "CI from 1000 paired stratified resamples."))
    for name in cities:
        doc.append(ec.md(ct[ct.city == name].sort_values(["sub_pct_median", "pct_sigma"], na_position="last"), COST_COLS, f"{name}: cost to one sigma", MEASURE_NOTE))
    (out / "evalscreen_curve_rank.md").write_text("\n".join(doc))
    print(verdict.to_string(index=False)); print(piv.to_string(index=False, float_format=lambda x: f"{x:.2f}")); print(ev.to_string(index=False, float_format=lambda x: f"{x:.2f}"))


# ---------------------------------------------------------------- transfer: cheap sources, source choice, headroom
SOURCE_KS = [1, 3, 5, 10]
TASK_STATS = "results/benchst/compare/tables/candidates_task_stats.csv"
TASK_COLS = ["r1_permille_w12", "r2_permille_w12", "acf_lag1"]
N_PROBE, PROBE_K = 5, 3


def source_rank(cities: dict, held: str, k: int | None, sources: list | None = None) -> np.ndarray:
    """Pooled rank at the held-out city from the other cities: their final labels (k None) or their val MAE after k epochs."""
    c = cities[held]; ranks = []
    for name, s in cities.items():
        if name != held and (sources is None or name in sources):
            v = -s.y if k is None else -s.val_at(k)
            ranks.append(unit_rank(c.align(pd.Series(v, index=s.ids))))
    return np.mean(ranks, axis=0)


def run_transfer(roots: list[Root], cities: dict, out: Path) -> None:
    sink = Sink(); krows, hrows, prows = [], [], []
    names = list(cities)
    for held, c in cities.items():
        full = source_rank(cities, held, None); sink.add(c, "pooled_final_labels", "transfer", score_eval(full), full)
        w_full = within_head(c, full)
        for k in SOURCE_KS:                                             # K: sources trained k epochs only
            s = source_rank(cities, held, k); sink.add(c, f"pooled_source_k{k}", "transfer, cheap sources", score_eval(s), s, {"k": k})
            src_cost = np.mean([float(sum(S.cumh[i][min(k, S.length[i])] for i in range(S.n)) / S.full_h.sum()) for n_, S in cities.items() if n_ != held])
            krows.append({"city": held, "k": k, "rho_within_head": within_head(c, s), "full_label_within": w_full, "loss": w_full - within_head(c, s), "source_cost_share": src_cost})
        for src in names:                                               # single sources, final labels and five epochs
            if src != held:
                s = source_rank(cities, held, None, [src]); sink.add(c, f"from_{src}", "transfer, one source", score_eval(s), s)
                s5 = source_rank(cities, held, 5, [src]); sink.add(c, f"from_{src}_k5", "transfer, one cheap source", score_eval(s5), s5)
        # I: headroom of transfer, and the probe statistic
        y = c.y; best = y.min(); o = order_of(full)
        rng = np.random.default_rng(0); sets = [np.arange(N_PROBE)] + [rng.choice(c.n, N_PROBE, replace=False) for _ in range(20)]
        spreads = [float(np.std(y[p], ddof=1) / c.sigma) for p in sets]
        hrows.append({"city": held, "sigma_seed": c.sigma, "list_std_over_sigma": float(np.std(y, ddof=1) / c.sigma), "list_range_over_sigma": float((y.max() - best) / c.sigma),
                      "share_of_list_within_1_sigma": float(np.mean(y - best <= c.sigma)), "headroom_pooled_top1_sigma": float((y[o[0]] - best) / c.sigma),
                      "headroom_pooled_best_of_5_sigma": float((y[o[:5]].min() - best) / c.sigma), "probe_spread_first5": spreads[0],
                      "probe_spread_mean_random5": float(np.mean(spreads[1:])), "probe_spread_p5": float(np.percentile(spreads[1:], 5)), "probe_spread_p95": float(np.percentile(spreads[1:], 95))})
    ct, _, ht = sink.frames()
    # H: a label-free similarity picks the source
    try:
        ts = pd.read_csv(TASK_STATS).set_index("dataset"); tcols = [x for x in TASK_COLS if x in ts.columns]
        Z = (ts[tcols] - ts.loc[[x for x in ts.index if x in names], tcols].mean()) / ts.loc[[x for x in ts.index if x in names], tcols].std()
    except Exception:
        Z, tcols = None, []
    for tgt in names:
        c = cities[tgt]
        for src in names:
            if src == tgt:
                continue
            S = cities[src]
            px = [rho(c.df[p].values.astype(float), c.align(pd.Series(S.df[p].values.astype(float), index=S.ids))) for p in PROXY_NAMES if p in c.df and p in S.df and p not in ("params", "flops")]
            probes = np.arange(N_PROBE); pr_s = c.align(pd.Series(-S.val_at(PROBE_K), index=S.ids))[probes]
            row = ct[(ct.city == tgt) & (ct.evaluator == f"from_{src}")].iloc[0]
            prows.append({"target": tgt, "source": src, "sim_proxy_profile": float(np.nanmean(px)), "sim_probe_agreement": rho(-c.val_at(PROBE_K)[probes], pr_s) if N_PROBE >= 4 else np.nan,
                          "sim_task_stats": -float(np.linalg.norm(Z.loc[tgt] - Z.loc[src])) if Z is not None and tgt in Z.index and src in Z.index else np.nan,
                          "label_rho_within_head": within_head(c, source_rank(cities, tgt, None, [src])), "sub_share": row.sub_share, "sub_pct_median": row.sub_pct_median, "pct_sigma": row.pct_sigma})
    pt = pd.DataFrame(prows); kt = pd.DataFrame(krows); hd = pd.DataFrame(hrows)
    choice = []
    for sim in ("sim_proxy_profile", "sim_probe_agreement", "sim_task_stats"):
        for tgt, g in pt.groupby("target"):
            if g[sim].notna().sum() < 2:
                continue
            g = g.assign(true_rank=g.label_rho_within_head.rank(ascending=False)); pick = g.loc[g[sim].idxmax()]
            pooled = ct[(ct.city == tgt) & (ct.evaluator == "pooled_final_labels")].iloc[0]
            choice.append({"similarity": sim, "target": tgt, "chosen_source": pick.source, "true_rank_of_choice": int(pick.true_rank), "chosen_sub_pct_median": pick.sub_pct_median,
                           "pooled_sub_pct_median": pooled.sub_pct_median, "chosen_below_pooled": bool(pick.sub_pct_median < pooled.sub_pct_median),
                           "rho_sim_vs_label_rho": rho(g[sim].values, g.label_rho_within_head.values) if len(g) >= 4 else np.nan})
    ch = pd.DataFrame(choice)
    kv = kt[kt.k == 5].merge(ct[ct.evaluator == "pooled_source_k5"][["city", "sub_share", "sub_pct_median"]], on="city").merge(
        ct[ct.evaluator == "pooled_final_labels"][["city", "sub_pct_median"]].rename(columns={"sub_pct_median": "full_sub_pct_median"}), on="city")
    kv["ok"] = (kv.loss <= 0.1) & (kv.sub_pct_median <= 1.5 * kv.full_sub_pct_median) & (kv.sub_share >= 0.9)
    for n_, t in (("cost", ct), ("head", ht), ("cheap_sources", kt), ("cheap_sources_k5", kv), ("headroom", hd), ("source_pairs", pt), ("source_choice", ch)):
        t.to_csv(out / f"transfer_{n_}.csv", index=False)
    doc = ["# evalscreen transfer: cheap sources, the choice of the source, and the headroom of transfer", "",
           "pooled_final_labels = mean label rank over the other three cities. pooled_source_k = the same rank from the validation MAE of the sources after k epochs; "
           "source_cost_share = the share of a source list's full cost that k epochs take. " + MEASURE_NOTE, ""]
    doc.append(ec.md(kt, list(kt.columns), "Cheap sources: Spearman inside the heads at the target against the epochs trained at the sources"))
    doc.append(ec.md(kv, list(kv.columns), "Cheap sources at k = 5 against the pass line", "ok = loss <= 0.1 and robust cost at most 1.5 times the full-label pooled rank with a subset share >= 0.9."))
    doc.append(ec.md(hd, list(hd.columns), "Headroom of transfer in sigma_seed, and the probe statistic", f"probe_spread = std of the test MAE of {N_PROBE} architectures over sigma_seed (the first {N_PROBE} of the list; 20 random sets)."))
    doc.append(ec.md(pt, list(pt.columns), "Source pairs: label-free similarities against the transfer quality"))
    doc.append(ec.md(ch, list(ch.columns), "The source that each similarity picks"))
    for k in cities:
        doc.append(ec.md(ct[ct.city == k].sort_values(["sub_pct_median", "pct_sigma"], na_position="last"), COST_COLS, f"{k}: cost to one sigma"))
    (out / "evalscreen_transfer.md").write_text("\n".join(doc))
    pd.set_option("display.width", 250)
    for t in (kt, kv, hd, pt, ch):
        print(t.to_string(index=False, float_format=lambda x: f"{x:.2f}")); print()


# ---------------------------------------------------------------- shared by the four tests below
def eff_cost(t: pd.DataFrame) -> pd.Series:
    """The robust cost share of a row, or 100 (train the whole list) when fewer than 90 % of the subsets meet the line."""
    return t.sub_pct_median.where((t.sub_share >= 0.9) & t.sub_pct_median.notna(), 100.0)


def warm_priors(roots: list[Root], cities: dict) -> dict:
    arch = arch_matrices(roots, cities)
    a = fit_loco(cities, {k: np.c_[proxy_matrix(c, PROXY_NAMES), head_onehot(c)] for k, c in cities.items()}, "gbr")
    o = fit_loco(cities, arch, "gbr")
    return {"pooled": {k: source_rank(cities, k, None) for k in cities}, "opcount": o, "proxymix": a}, arch


# ---------------------------------------------------------------- halving_prior: successive halving with a prior
def prior_filter_halving(prior: np.ndarray, r0: int, eta: int, info: dict | None = None):
    """The prior keeps the top 1/eta with no training; plain halving runs on that part; the rest follows in prior order."""
    def run(c: City, sub: np.ndarray):
        o = sub[order_of(prior[sub])]; keep = max(1, len(o) // eta); top, rest = o[:keep], o[keep:]
        order, done = halving_eval(r0, eta)(c, top)
        if info is not None:
            info.update(first_cut=list(rest))
        return np.concatenate([order, rest]), done
    return run


def run_halving_prior(roots: list[Root], cities: dict, out: Path) -> None:
    warm, _ = warm_priors(roots, cities); r0, eta = 1, 3; sink = Sink()
    for name, c in cities.items():
        top15 = set(np.argsort(c.y)[:max(1, c.n // 10)]); full = np.arange(c.n)
        priors = {**{f"warm_{k}": v[name] for k, v in warm.items()}, "cold_zico_sizectrl": c.df["zico_sizectrl"].values.astype(float)}
        for pn, p in priors.items():
            for sched, mk in (("filter", lambda i: prior_filter_halving(p, r0, eta, i)), ("blend", lambda i: halving_eval(r0, eta, p, [0.5, 0.25, 0.125, 0.0625], i))):
                info = {}; mk(info)(c, full)
                sink.add(c, f"sh_{pn}_{sched}", "halving with a prior", mk(None), extra={"setting": pn.split("_")[0], "top10pct_dropped_first_rung": int(len(top15 & set(info["first_cut"])))})
        info = {}; halving_eval(r0, eta, info=info)(c, full)
        sink.add(c, "sh_plain", "reference", halving_eval(r0, eta), extra={"setting": "cold", "top10pct_dropped_first_rung": int(len(top15 & set(info["first_cut"])))})
        zs = c.df["zico_sizectrl"].values.astype(float)
        sink.add(c, "zico_sizectrl_half_then_k5", "reference", filter_eval(zs, 5), extra={"setting": "cold"})
        sink.add(c, "early_val_k5", "reference", score_eval(-c.val_at(5), 5), extra={"setting": "cold"})
        sink.add(c, "transfer_pooled", "reference", score_eval(warm["pooled"][name]), extra={"setting": "warm"})
    ct, _, _ = sink.frames(); ct["eff"] = eff_cost(ct)
    refs = ["sh_plain", "zico_sizectrl_half_then_k5", "early_val_k5"]; rows = []
    for setting in ("warm", "cold"):
        cand = sorted(set(ct[(ct.kind == "halving with a prior") & (ct.setting == setting)].evaluator))
        for held in cities:
            tr = ct[(ct.city != held) & ct.evaluator.isin(cand)].groupby("evaluator").eff.mean(); pick = tr.idxmin()
            h = ct[ct.city == held].set_index("evaluator")
            rows.append({"setting": setting, "held_out": held, "chosen_on_other_cities": pick, "eff_cost": h.eff[pick], "sub_share": h.sub_share[pick],
                         "dropped_first_rung": h.top10pct_dropped_first_rung[pick], "plain_dropped_first_rung": h.top10pct_dropped_first_rung["sh_plain"],
                         **{f"ref_{r}": h.eff[r] for r in refs}, "ref_transfer_pooled": h.eff["transfer_pooled"],
                         "le_10pct": bool(h.eff[pick] <= 10), "below_all_refs": bool(h.eff[pick] < min(h.eff[r] for r in refs))})
    ch = pd.DataFrame(rows)
    verdict = ch.groupby("setting").agg(cities_le_10pct=("le_10pct", "sum"), cities_below_all_refs=("below_all_refs", "sum"),
                                        cities_fewer_drops=("dropped_first_rung", lambda x: int((x.values < ch.loc[x.index, "plain_dropped_first_rung"].values).sum()))).reset_index()
    verdict["pass"] = (verdict.cities_le_10pct >= 3) & (verdict.cities_below_all_refs >= 3) & (verdict.cities_fewer_drops >= len(cities))
    for n_, t in (("cost", ct), ("choice", ch), ("verdict", verdict)):
        t.to_csv(out / f"halving_prior_{n_}.csv", index=False)
    piv = ct.pivot(index="evaluator", columns="city", values="eff").reset_index(); drop = ct.pivot(index="evaluator", columns="city", values="top10pct_dropped_first_rung").reset_index()
    doc = ["# evalscreen halving_prior: successive halving with a prior (r0 = 1, eta = 3)", "",
           "filter = the prior keeps the top third with no training, then plain halving; blend = rung score 0.5 z(prior) + 0.5 z(-val MAE) at the first rung, the prior weight halved at each "
           "later rung. Warm priors are fit on the other cities: pooled = mean label rank, opcount = boosting on operator counts, proxymix = boosting on the proxies and the head. The cold "
           "prior is the size-controlled ZiCo of the city. eff = the median cost share over the subsets, or 100 when fewer than 90 % of the subsets meet the line. The setting of each "
           "held-out city is the one with the lowest mean eff on the other three cities.", ""]
    doc += [ec.md(verdict, list(verdict.columns), "Verdict"), ec.md(ch, list(ch.columns), "The setting chosen on the other cities, read at the held-out city"),
            ec.md(piv, list(piv.columns), "eff, every setting"), ec.md(drop, list(drop.columns), "Top-15 architectures dropped at the first rung")]
    (out / "evalscreen_halving_prior.md").write_text("\n".join(doc))
    pd.set_option("display.width", 250)
    for t in (verdict, ch, piv, drop):
        print(t.to_string(index=False, float_format=lambda x: f"{x:.1f}")); print()


# ---------------------------------------------------------------- active_labels: which few architectures to train at the target
LABEL_NS, LABEL_ROUND = [5, 10, 15], 5


def label_sequence(c: City, sub: np.ndarray, prior: np.ndarray, arch: np.ndarray, rule: str, seed: int) -> np.ndarray:
    rng = np.random.default_rng([seed, int(sub.sum())]); n_max = LABEL_NS[-1]
    lab = list(rng.choice(sub, LABEL_ROUND, replace=False)) if rule == "random" else list(sub[order_of(prior[sub])][:LABEL_ROUND])
    while len(lab) < n_max:
        rest = np.setdiff1d(sub, lab)
        if rule == "random":
            nxt = rng.choice(rest, LABEL_ROUND, replace=False)
        elif rule == "prior":
            nxt = rest[order_of(prior[rest])][:LABEL_ROUND]
        else:                                                            # refit on the labels so far; four picks and one exploration pick
            L = np.array(lab); pred = pr.fit_predict("ridge", np.c_[arch[L], prior[L]], zscore(-c.y[L]), np.c_[arch[rest], prior[rest]])
            top = rest[order_of(pred)][:LABEL_ROUND - 1]; nxt = np.r_[top, rng.choice(np.setdiff1d(rest, top), 1)]
        lab += list(nxt)
    return np.array(lab)


def label_outcome(c: City, sub: np.ndarray, seq: np.ndarray) -> dict:
    best = c.y[sub].min(); tot = float(c.full_h[sub].sum()); out = {"n_sigma": np.inf, "pct": np.inf}
    for n in LABEL_NS:
        r = float(c.y[seq[:n]].min() - best); out[f"regret_n{n}_sigma"] = r / c.sigma
        if r <= c.sigma + 1e-12 and not np.isfinite(out["n_sigma"]):
            out["n_sigma"] = n; out["pct"] = float(c.full_h[seq[:n]].sum()) / tot * 100
    return out


def run_active_labels(roots: list[Root], cities: dict, out: Path) -> None:
    warm, arch = warm_priors(roots, cities); rows = []
    for name, c in cities.items():
        full = np.arange(c.n)
        for setting, prior in (("warm", warm["pooled"][name]), ("cold", c.df["zico_sizectrl"].values.astype(float))):
            for rule in ("random", "prior", "refit"):
                fl = [label_outcome(c, full, label_sequence(c, full, prior, arch[name], rule, s)) for s in range(20 if rule != "prior" else 1)]
                sb = [label_outcome(c, sub, label_sequence(c, sub, prior, arch[name], rule, 0)) for sub in c.subs]
                pct = np.array([o["pct"] for o in sb]); ns = np.array([o["n_sigma"] for o in sb])
                rows.append({"city": name, "setting": setting, "rule": rule, **{f"regret_n{n}_sigma": float(np.mean([o[f"regret_n{n}_sigma"] for o in fl])) for n in LABEL_NS},
                             "sub_share": float(np.mean(np.isfinite(pct))), "sub_pct_median": float(np.median(pct)) if np.isfinite(np.median(pct)) else np.nan,
                             "sub_n_median": float(np.median(ns)) if np.isfinite(np.median(ns)) else np.nan,
                             **{f"sub_regret_n{n}_sigma": float(np.mean([o[f"regret_n{n}_sigma"] for o in sb])) for n in LABEL_NS}})
    t = pd.DataFrame(rows); t["eff"] = eff_cost(t); v = []
    for setting, g in t.groupby("setting"):
        p = g.pivot(index="city", columns="rule", values="eff")
        v.append({"setting": setting, "cities_refit_meets_line": int((p.refit < 100).sum()), "cities_refit_below_random_and_prior": int(((p.refit < p.random) & (p.refit < p.prior)).sum())})
    verdict = pd.DataFrame(v); verdict["pass"] = (verdict.cities_refit_meets_line >= 3) & (verdict.cities_refit_below_random_and_prior >= 3)
    t.to_csv(out / "active_labels.csv", index=False); verdict.to_csv(out / "active_labels_verdict.csv", index=False)
    doc = ["# evalscreen active_labels: an active choice of the labels at the target city", "",
           f"Rounds of {LABEL_ROUND} labels up to 15. random = random labels; prior = the next five of the prior, no refit; refit = a ridge on the operator counts and the prior, fit on the "
           "labels so far, picks four and one random architecture. Warm prior = the pooled transfer rank; cold prior = the size-controlled ZiCo of the city. The pick is the best labelled "
           "architecture. regret_n = regret after n labels on the full list (mean of 20 draws where the rule draws); sub_* = the 200 subsets; eff as in halving_prior.", ""]
    doc += [ec.md(verdict, list(verdict.columns), "Verdict"), ec.md(t, list(t.columns), "Every rule")]
    (out / "evalscreen_active_labels.md").write_text("\n".join(doc))
    pd.set_option("display.width", 250); print(verdict.to_string(index=False)); print(t.drop(columns=[c_ for c_ in t.columns if c_.startswith("sub_regret")]).to_string(index=False, float_format=lambda x: f"{x:.2f}"))


# ---------------------------------------------------------------- space_cut: a reduced search space learned from the other cities
CUT_COLS = ["seq_family", "graph_family", "flat_family", "decoder"]


def choice_masks(c: City, pairs: bool) -> dict:
    m = {f"{col}={v}": (c.df[col] == v).values for col in CUT_COLS for v in sorted(set(c.df[col]))}
    if pairs:
        for i, a in enumerate(CUT_COLS):
            for b in CUT_COLS[i + 1:]:
                for va in sorted(set(c.df[a])):
                    for vb in sorted(set(c.df[b])):
                        m[f"{a}={va}&{b}={vb}"] = ((c.df[a] == va) & (c.df[b] == vb)).values
    return m


def head_rank(c: City) -> np.ndarray:
    r = np.zeros(c.n)
    for h in HEADS:
        m = c.head == h; r[m] = unit_rank(-c.y[m])
    return r


def learn_cut(train: dict, keep_frac: float, pairs: bool) -> list:
    """Greedy: remove the choice whose architectures rank lowest inside their heads, when it is below the mean of the remaining
    list at every training city that holds 3 or more of them (2 cities or more); stop at the keep fraction."""
    masks = {k: choice_masks(c, pairs) for k, c in train.items()}; tgt = {k: head_rank(c) for k, c in train.items()}
    alive = {k: np.ones(c.n, bool) for k, c in train.items()}; total = sum(c.n for c in train.values()); removed = []
    keys = sorted(set().union(*[set(m) for m in masks.values()]))
    while sum(a.sum() for a in alive.values()) / total > keep_frac:
        best = (None, 0.0)
        for key in keys:
            if key in removed:
                continue
            diffs, n_mem = [], 0
            for k in train:
                mem = masks[k].get(key, np.zeros(train[k].n, bool)) & alive[k]
                if mem.sum() >= 3:
                    diffs.append(tgt[k][mem].mean() - tgt[k][alive[k]].mean()); n_mem += mem.sum()
            if len(diffs) >= 2 and max(diffs) < 0 and n_mem >= 0.03 * total and np.mean(diffs) < best[1]:
                best = (key, float(np.mean(diffs)))
        if best[0] is None:
            break
        removed.append(best[0])
        for k in train:
            alive[k] &= ~masks[k].get(best[0], np.zeros(train[k].n, bool))
    return removed


def restricted_random(kept: np.ndarray, seed: int = 0):
    def run(c: City, sub: np.ndarray):
        rng = np.random.default_rng([seed, int(sub.sum())]); inside = sub[kept[sub]]; rest = sub[~kept[sub]]
        return np.concatenate([rng.permutation(inside), rng.permutation(rest)]), np.zeros(c.n, dtype=int)
    return run


def run_space_cut(roots: list[Root], cities: dict, out: Path) -> None:
    sink = Sink(); rows = []; rng = np.random.default_rng(0)
    for held, c in cities.items():
        train = {k: v for k, v in cities.items() if k != held}; top15 = np.argsort(c.y)[:15]; best = c.y.min()
        mae = np.where(c.head == "mae")[0]; mae_top = mae[np.argsort(c.y[mae])[:4]]
        r10 = float(np.mean([c.y[rng.choice(c.n, 10, replace=False)].min() for _ in range(5000)]) - best) / c.sigma
        cuts = {}
        for pairs in (False, True):
            for frac in (0.5, 0.25):
                rem = learn_cut(train, frac, pairs); masks = choice_masks(c, pairs); kept = np.ones(c.n, bool)
                for key in rem:
                    kept &= ~masks.get(key, np.zeros(c.n, bool))
                cuts[f"learned_{'pairs' if pairs else 'single'}_keep{int(frac * 100)}"] = (kept, rem)
        for ref, s in (("ref_zico_sizectrl_top_half", c.df["zico_sizectrl"].values.astype(float)), ("ref_pooled_transfer_top_half", source_rank(cities, held, None))):
            kept = np.zeros(c.n, bool); kept[order_of(s)[:c.n // 2]] = True; cuts[ref] = (kept, [])
        for cn, (kept, rem) in cuts.items():
            idx = np.where(kept)[0]
            r5 = float(np.mean([c.y[rng.choice(idx, min(5, len(idx)), replace=False)].min() for _ in range(5000)]) - best) / c.sigma if len(idx) else np.nan
            rows.append({"city": held, "cut": cn, "kept_share": float(kept.mean()), "top15_kept": int(kept[top15].sum()), "best_kept": bool(kept[top15[0]]),
                         "mae_head_top4_kept": int(kept[mae_top].sum()), "random5_inside_sigma": r5, "random10_full_sigma": r10, "rules_removed": "; ".join(rem)})
            sink.add(c, f"random_inside_{cn}", "random in a reduced list", restricted_random(kept))
        sink.add(c, "random_full_list", "floor", random_eval())
    t = pd.DataFrame(rows); ct, _, _ = sink.frames()
    t["ok"] = (t.kept_share <= 0.5) & (t.top15_kept >= 13) & (t.random5_inside_sigma < t.random10_full_sigma)
    verdict = t.groupby("cut").agg(cities_ok=("ok", "sum"), kept_share_mean=("kept_share", "mean"), top15_kept_min=("top15_kept", "min")).reset_index(); verdict["pass"] = verdict.cities_ok >= 3
    for n_, x in (("cuts", t), ("cost", ct), ("verdict", verdict)):
        x.to_csv(out / f"space_cut_{n_}.csv", index=False)
    doc = ["# evalscreen space_cut: a reduced search space learned from the labels of the other cities", "",
           f"Choices: {CUT_COLS} (single) and their pairs. Greedy rule on three cities: remove the choice whose architectures rank lowest inside their heads, when it is below the mean of "
           "the remaining list at every training city that holds three or more of them; stop at the keep fraction. The rule never sees the head, and the rank is taken inside the head. "
           "Line: the reduced list of the held-out city holds at most half of the list and 13 or more of the top 15, and five random picks inside it have a lower expected regret than "
           "ten random picks in the full list, at three of four cities. ref_* = a list filter, not a rule on the space.", ""]
    doc += [ec.md(verdict, list(verdict.columns), "Verdict"), ec.md(t, list(t.columns), "Every cut at every held-out city")]
    for k in cities:
        doc.append(ec.md(ct[ct.city == k].sort_values(["sub_pct_median", "pct_sigma"], na_position="last"), COST_COLS, f"{k}: cost to one sigma of random picks inside each reduced list"))
    (out / "evalscreen_space_cut.md").write_text("\n".join(doc))
    pd.set_option("display.width", 280); pd.set_option("display.max_colwidth", 150); print(verdict.to_string(index=False, float_format=lambda x: f"{x:.2f}")); print(t.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    print(ct[["city", "evaluator", "sub_share", "sub_pct_median"]].pivot(index="evaluator", columns="city", values="sub_share").to_string(float_format=lambda x: f"{x:.2f}"))


# ---------------------------------------------------------------- route: a few probe trainings choose the recipe
def run_route(roots: list[Root], cities: dict, out: Path) -> None:
    base = pd.read_csv(out / "base_cost_to_sigma.csv"); hp = pd.read_csv(out / "halving_prior_cost.csv")
    base["eff"] = eff_cost(base); allc = pd.concat([base[["city", "evaluator", "eff"]], hp[hp.kind == "halving with a prior"][["city", "evaluator", "eff"]]])
    cold = ["zico_sizectrl", "zico", "sh_r1_eta3", "early_val_k2", "early_val_k3", "early_val_k5", "zico_sizectrl_half_then_k1", "zico_sizectrl_half_then_k3", "zico_sizectrl_half_then_k5",
            "sh_cold_zico_sizectrl_filter", "sh_cold_zico_sizectrl_blend"]
    warm = cold + ["transfer_pooled", "loco_gbr_arch", "sh_warm_pooled_filter", "sh_warm_pooled_blend"]
    pooled = {k: source_rank(cities, k, None) for k in cities}; probes = np.arange(N_PROBE); feats = {}
    for k, c in cities.items():
        v1, v3 = c.val_at(1)[probes], c.val_at(PROBE_K)[probes]
        feats[k] = {"improve_1_to_3": float(np.median(v3 / v1)), "probe_cv_k3": float(np.std(v3) / np.mean(v3)),
                    "agree_cold_prior": rho(c.df["zico_sizectrl"].values.astype(float)[probes], -v3), "agree_warm_prior": rho(pooled[k][probes], -v3)}
    ft = pd.DataFrame(feats).T; probe_pct = {k: float(sum(c.cumh[i][PROBE_K] for i in probes) / c.full_h.sum() * 100) for k, c in cities.items()}
    rows = []
    for setting, recipes in (("cold", cold), ("warm", warm)):
        P = allc[allc.evaluator.isin(recipes)].pivot(index="evaluator", columns="city", values="eff")
        cols = ["improve_1_to_3", "probe_cv_k3", "agree_cold_prior"] + (["agree_warm_prior"] if setting == "warm" else [])
        for held in cities:
            tr = [k for k in cities if k != held]; Z = (ft[cols] - ft.loc[tr, cols].mean()) / ft.loc[tr, cols].std().replace(0, 1)
            near = min(tr, key=lambda k: float(np.linalg.norm((Z.loc[held] - Z.loc[k]).fillna(0)))); rule = P[near].idxmin(); fixed = P[tr].mean(axis=1).idxmin(); oracle = P[held].idxmin()
            rows.append({"setting": setting, "held_out": held, "oracle_recipe": oracle, "oracle_eff": P.loc[oracle, held], "nearest_city": near, "rule_recipe": rule,
                         "rule_eff_with_probes": P.loc[rule, held] + probe_pct[held], "fixed_recipe": fixed, "fixed_eff": P.loc[fixed, held],
                         "rule_within_1.25_oracle": bool(P.loc[rule, held] + probe_pct[held] <= 1.25 * P.loc[oracle, held])})
    t = pd.DataFrame(rows)
    verdict = t.groupby("setting").agg(cities_within_1_25=("rule_within_1.25_oracle", "sum"), rule_mean=("rule_eff_with_probes", "mean"), fixed_mean=("fixed_eff", "mean"), oracle_mean=("oracle_eff", "mean")).reset_index()
    verdict["pass"] = (verdict.cities_within_1_25 >= len(cities)) & (verdict.rule_mean < verdict.fixed_mean)
    t.to_csv(out / "route.csv", index=False); ft.to_csv(out / "route_probe_features.csv"); verdict.to_csv(out / "route_verdict.csv", index=False)
    doc = ["# evalscreen route: a few probe trainings choose the recipe", "",
           f"Probes: the first {N_PROBE} architectures of the list, trained {PROBE_K} epochs. Features: the median ratio of the val MAE at epoch 3 to epoch 1, the spread of the probes at "
           "epoch 3, and the agreement of the prior with the probes. Rule: take the cheapest recipe of the training city whose probe features are nearest. fixed = the recipe with the "
           "lowest mean eff on the three training cities. oracle = the cheapest recipe of the held-out city. eff as in halving_prior; the rule pays the probes.", ""]
    doc += [ec.md(verdict, list(verdict.columns), "Verdict"), ec.md(t, list(t.columns), "Held-out decisions"), ec.md(ft.reset_index().rename(columns={"index": "city"}), ["city"] + list(ft.columns), "Probe features")]
    (out / "evalscreen_route.md").write_text("\n".join(doc))
    pd.set_option("display.width", 280); print(verdict.to_string(index=False, float_format=lambda x: f"{x:.1f}")); print(t.to_string(index=False, float_format=lambda x: f"{x:.1f}")); print(ft.to_string(float_format=lambda x: f"{x:.2f}"))


# ---------------------------------------------------------------- operator_traits: a predictor that reads what an operator is
SEQ_TRAITS = {"gru": ["recurrent", "gated", "global", "weights"], "lstm": ["recurrent", "gated", "memory", "global", "weights"],
              "tcn": ["conv", "local", "weights"], "sep_tcn": ["conv", "separable", "local", "weights"], "transformer": ["attention", "global", "weights"],
              "mlp_mix": ["dense", "global", "weights"], "skip_connection": ["identity"]}
FLAT_TRAITS = {"mlp": ["dense", "weights"], "nbeats_g": ["dense", "basis", "weights"], "nbeats_s": ["basis", "fixed_basis", "periodic", "weights"],
               "nbeats_t": ["basis", "fixed_basis", "polynomial", "weights"], "skip_connection": ["identity"]}
GRAPH_TRAITS = {"gcn": ["message", "given_adj", "weights"], "diffusion": ["message", "given_adj", "multi_hop", "weights"],
                "adaptive": ["message", "learned_adj", "weights"], "graph_identity": ["identity"]}
SHARED_COLS = ["enc_n_edges", "dec_n_edges", "flat_n_edges", "graph_n_edges", "has_graph", "head_mae", "head_mse", "head_quantile", "dec_linear", "dec_seq", "log_params", "log_flops"]


def trait_matrices(roots: list[Root], cities: dict) -> tuple[dict, dict]:
    """Per city: the trait counts per cell with the shared columns, and the same next to the operator counts."""
    from pilot.genotype import load_archs
    raw = {city_key(r): pr.load_city(r).set_index("arch_id") for r in roots}; arch = arch_matrices(roots, cities)
    keys = sorted({f"{cell}_{t}" for cell, tab in (("enc", SEQ_TRAITS), ("dec", SEQ_TRAITS), ("flat", FLAT_TRAITS), ("graph", GRAPH_TRAITS)) for ts in tab.values() for t in ts})
    traits, both = {}, {}
    for r in roots:
        key = city_key(r); c = cities[key]; geno = {a["arch_id"]: a["genotype"] for a in load_archs(r.archs_jsonl)}; rows = []
        for aid in c.ids:
            g = geno[aid]; f = dict.fromkeys(keys, 0)
            for cell, edges, tab in (("enc", g["seq"]["encoder"], SEQ_TRAITS), ("dec", g["seq"]["decoder"], SEQ_TRAITS), ("flat", g["flat"]["cell"], FLAT_TRAITS),
                                     ("graph", g["graph"]["cell"] if g.get("graph") else [], GRAPH_TRAITS)):
                for _, _, op in edges:
                    if op is not None:
                        for t in tab[op]:
                            f[f"{cell}_{t}"] += 1
            rows.append([f[k] for k in keys])
        d = raw[key]
        shared = np.column_stack([d.loc[c.ids, col].values.astype(float) if col in d else np.zeros(c.n) for col in SHARED_COLS])
        traits[key] = np.c_[np.array(rows, dtype=float), shared]; both[key] = np.c_[np.array(rows, dtype=float), arch[key]]
    return traits, both


def run_operator_traits(roots: list[Root], cities: dict, out: Path) -> None:
    traits, both = trait_matrices(roots, cities); arch = arch_matrices(roots, cities); rows = []
    for label, feats in (("traits", traits), ("traits_and_counts", both), ("operator_counts", arch)):
        for kind in ("ridge", "gbr"):
            rows += family_rows(cities, feats, kind, f"{kind}_{label}")
            pred = fit_loco(cities, feats, kind)                          # no family held out: the plain leave-one-city-out value
            for name, c in cities.items():
                rows.append({"city": name, "model": f"{kind}_{label}", "family_kind": "none", "held_out_family": "(none)", "n": c.n,
                             "kendall": float(kendalltau(pred[name], -c.y).correlation), "spearman": within_head(c, pred[name])})
    fm = pd.DataFrame(rows); fam = fm[fm.family_kind != "none"]
    agg = fam.groupby(["city", "model"]).apply(lambda g: pd.Series({"families": len(g), "kendall_weighted": np.average(g.kendall, weights=g.n), "families_ge_0.5": int((g.kendall >= 0.5).sum())})).reset_index()
    piv = agg.pivot(index="model", columns="city", values="kendall_weighted"); v = []
    for m in piv.index:
        if "operator_counts" in m:
            continue
        ref = piv.loc[m.split("_")[0] + "_operator_counts"]
        v.append({"model": m, "cities_kendall_ge_05": int((piv.loc[m] >= 0.5).sum()), "cities_above_operator_counts": int((piv.loc[m] > ref).sum()), "mean_gain": float((piv.loc[m] - ref).mean())})
    verdict = pd.DataFrame(v); verdict["pass"] = (verdict.cities_kendall_ge_05 >= 3) & (verdict.cities_above_operator_counts >= 3)
    per_fam = fam.pivot_table(index=["held_out_family", "model"], columns="city", values="kendall").reset_index()
    plain = fm[fm.family_kind == "none"].pivot(index="model", columns="city", values="spearman").reset_index()
    for n_, t in (("family", fm), ("summary", agg), ("verdict", verdict)):
        t.to_csv(out / f"operator_traits_{n_}.csv", index=False)
    doc = ["# evalscreen operator_traits: a predictor that reads what an operator is", "",
           "Each operator has a fixed list of traits (SEQ_TRAITS, FLAT_TRAITS, GRAPH_TRAITS in pilot/evalscreen.py). An architecture is encoded by the count of each trait in each cell. "
           "Test: one city and one operator family are held out together; Kendall with -test MAE on the held-out family at the held-out city, n-weighted over the families with 8 "
           "architectures or more. Pass: 0.5 or more at three of four cities and above the operator-count predictor at three of four cities.", ""]
    doc += [ec.md(verdict, list(verdict.columns), "Verdict"), ec.md(piv.reset_index(), ["model"] + list(piv.columns), "n-weighted Kendall on the held-out family at the held-out city"),
            ec.md(per_fam, list(per_fam.columns), "Kendall per held-out family"), ec.md(plain, list(plain.columns), "No family held out: Spearman inside the heads at the held-out city")]
    (out / "evalscreen_operator_traits.md").write_text("\n".join(doc))
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
    for t in (verdict, piv.reset_index(), plain, per_fam[per_fam.model.isin(["gbr_traits", "gbr_operator_counts", "ridge_traits", "ridge_operator_counts"])]):
        print(t.to_string(index=False, float_format=lambda x: f"{x:.2f}")); print()


# ---------------------------------------------------------------- label_share: a sparse label matrix shared by the cities
SHARE_NS, SHARE_BS, SHARE_DRAWS = [5, 10, 15, 30], [1, 3, 5], 50


def share_design(design: str, n: int, n_arch: int, names: list, rng) -> dict:
    if design == "independent":
        return {k: rng.choice(n_arch, n, replace=False) for k in names}
    perm = rng.permutation(n_arch)
    if design == "disjoint":
        return {k: perm[i * n:(i + 1) * n] for i, k in enumerate(names)}
    a = n // 2; anchor = perm[:a]; rest = perm[a:]; m = n - a                # anchor: half common, half disjoint
    return {k: np.r_[anchor, rest[i * m:(i + 1) * m]] for i, k in enumerate(names)}


def run_label_share(roots: list[Root], cities: dict, out: Path) -> None:
    arch = arch_matrices(roots, cities); names = list(cities); n_arch = cities[names[0]].n
    pos = {k: {a: i for i, a in enumerate(c.ids)} for k, c in cities.items()}; ref_ids = cities[names[0]].ids
    idx = {k: np.array([pos[k][a] for a in ref_ids]) for k in names}       # row r of the matrix = the same architecture at every city
    Y = {k: cities[k].y[idx[k]] for k in names}; X = {k: arch[k][idx[k]] for k in names}; H = {k: cities[k].full_h[idx[k]] / cities[k].ratio for k in names}
    fleet = sum(h.sum() for h in H.values()); rows = []
    for design in ("independent", "disjoint", "anchor"):
        for n in SHARE_NS:
            if design != "independent" and n * len(names) > n_arch and design == "disjoint":
                continue
            hit = {(m, b, k): [] for m in ("own", "pooled", "pooled_own", "observed_mean", "random") for b in SHARE_BS for k in names}
            cost = {b: [] for b in SHARE_BS}
            for d in range(SHARE_DRAWS):
                rng = np.random.default_rng([d, n, len(design)]); obs = share_design(design, n, n_arch, names, rng)
                tgt = {k: zscore(-Y[k][obs[k]]) for k in names}
                Xp = np.vstack([X[k][obs[k]] for k in names]); yp = np.concatenate([tgt[k] for k in names])
                pooled = {k: pr.fit_predict("ridge", Xp, yp, X[k]) for k in names}
                seen = np.full((n_arch, len(names)), np.nan)
                for j, k in enumerate(names):
                    seen[obs[k], j] = tgt[k]
                for j, k in enumerate(names):
                    own = pr.fit_predict("ridge", X[k][obs[k]], tgt[k], X[k])
                    po = pr.fit_predict("ridge", np.c_[X[k][obs[k]], pooled[k][obs[k]]], tgt[k], np.c_[X[k], pooled[k]])
                    others = np.delete(seen, j, axis=1); cnt = np.sum(np.isfinite(others), axis=1)
                    om = np.where(cnt > 0, np.nansum(others, axis=1) / np.maximum(cnt, 1), zscore(pooled[k]) * 0.5)
                    best = Y[k].min(); un = np.setdiff1d(np.arange(n_arch), obs[k]); base = Y[k][obs[k]].min()
                    for m, sc in (("own", own), ("pooled", pooled[k]), ("pooled_own", po), ("observed_mean", om), ("random", rng.random(n_arch))):
                        o = un[order_of(sc[un])]
                        for b in SHARE_BS:
                            hit[(m, b, k)].append(min(base, Y[k][o[:b]].min()) - best <= cities[k].sigma + 1e-12)
                for b in SHARE_BS:                                       # cost of the pairs and of b picks at the mean training cost
                    cost[b].append((sum(H[k][obs[k]].sum() for k in names) + b * sum(H[k].mean() for k in names)) / fleet * 100)
            for (m, b, k), v in hit.items():
                rows.append({"design": design, "n": n, "b": b, "model": m, "city": k, "share": float(np.mean(v)), "fleet_cost_pct": float(np.mean(cost[b]))})
    t = pd.DataFrame(rows)
    g = t.groupby(["design", "n", "b", "model"]).agg(fleet_cost_pct=("fleet_cost_pct", "mean"), mean_share=("share", "mean"), min_share=("share", "min"),
                                                   cities_ge_09=("share", lambda x: int((x >= 0.9).sum()))).reset_index()
    own = g[g.model == "own"].set_index(["design", "n", "b"]).mean_share
    g["above_own"] = [r.mean_share > own[(r.design, r.n, r.b)] for r in g.itertuples()]
    v = []
    for m in ("pooled", "pooled_own", "observed_mean"):
        x = g[g.model == m]; ok = x[(x.fleet_cost_pct <= 10) & (x.cities_ge_09 >= 3)]
        v.append({"model": m, "settings_at_10pct_with_3_cities": len(ok), "share_of_settings_above_own": float(x.above_own.mean()),
                  "cheapest_setting_with_3_cities_pct": float(x[x.cities_ge_09 >= 3].fleet_cost_pct.min()) if (x.cities_ge_09 >= 3).any() else np.nan})
    verdict = pd.DataFrame(v); verdict["pass"] = (verdict.settings_at_10pct_with_3_cities > 0) & (verdict.share_of_settings_above_own >= 1.0)
    ref = []                                                              # one city in full, the others by transfer of its best five
    for src in names:
        o = np.argsort(Y[src])[:5]; ok = [bool(Y[k][o].min() - Y[k].min() <= cities[k].sigma + 1e-12) for k in names if k != src]
        ref.append({"reference": f"{src} in full, transfer of its best 5", "fleet_cost_pct": (H[src].sum() + sum(H[k][o].sum() for k in names if k != src)) / fleet * 100, "other_cities_within_sigma": int(sum(ok))})
    ref = pd.DataFrame(ref)
    for n_, x in (("cells", t), ("summary", g), ("verdict", verdict), ("reference", ref)):
        x.to_csv(out / f"label_share_{n_}.csv", index=False)
    doc = ["# evalscreen label_share: a sparse label matrix shared by the cities", "",
           f"n architectures are trained at each city (design: independent, disjoint, or anchor = half common and half disjoint); a model predicts every missing entry; each city trains its b "
           f"best predictions and keeps the best architecture it trained. share = the share of {SHARE_DRAWS} random designs where that architecture lies within one sigma_seed of the best of "
           "the list. fleet_cost_pct = the GPU-hours of all pairs and picks over the GPU-hours of the whole matrix. own = a ridge on the labels of the city alone; pooled = one ridge on all "
           "trained pairs; pooled_own = own with the pooled prediction as an input; observed_mean = the mean rank at the cities that trained the architecture. Pass: a sharing model with a "
           "share of 0.9 or more at three of four cities at a fleet cost of 10 % or less, and a mean share above own at every setting.", ""]
    doc += [ec.md(verdict, list(verdict.columns), "Verdict"), ec.md(ref, list(ref.columns), "Reference: one city trained in full"),
            ec.md(g, list(g.columns), "Every setting"), ec.md(t, list(t.columns), "Every city")]
    (out / "evalscreen_label_share.md").write_text("\n".join(doc))
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 400)
    print(verdict.to_string(index=False, float_format=lambda x: f"{x:.2f}")); print(ref.to_string(index=False, float_format=lambda x: f"{x:.1f}"))
    print(g[g.b == 5].pivot_table(index=["design", "n"], columns="model", values="mean_share").to_string(float_format=lambda x: f"{x:.2f}"))
    print(g[g.b == 5].pivot_table(index=["design", "n"], columns="model", values="cities_ge_09").to_string()); print(g[g.b == 5].groupby("n").fleet_cost_pct.mean().to_string())
    print(t[(t.b == 5) & (t.design == "independent") & t.model.isin(["own", "pooled_own", "observed_mean", "random"])].pivot_table(index=["n", "model"], columns="city", values="share").to_string(float_format=lambda x: f"{x:.2f}"))


# ---------------------------------------------------------------- variance: which design axis moves the label
AXES = ["head", "decoder", "seq_family", "graph_family", "flat_family", "log_params"]


def _design(c: City, axes: list, rows: np.ndarray) -> np.ndarray:
    cols = [np.ones(len(rows))]
    for a in axes:
        if a == "log_params":
            cols.append(zscore(np.log(c.df["params"].values.astype(float)))[rows])
        else:
            v = c.df[a].values[rows]
            for lev in sorted(set(c.df[a].values))[1:]:
                cols.append((v == lev).astype(float))
    return np.column_stack(cols)


def _adj_r2(c: City, axes: list, rows: np.ndarray) -> float:
    y = c.y[rows]; X = _design(c, axes, rows); beta = np.linalg.lstsq(X, y, rcond=None)[0]
    ss_res = float(np.sum((y - X @ beta) ** 2)); ss_tot = float(np.sum((y - y.mean()) ** 2)); n, p = len(y), np.linalg.matrix_rank(X) - 1
    return 1 - (ss_res / max(n - p - 1, 1)) / (ss_tot / (n - 1)) if ss_tot > 0 else np.nan


def variance_rows(name: str, c: City, seed: int = 0) -> list[dict]:
    """The share of the label variance of each design axis at one city, over all heads and with the head fixed to MAE."""
    rows = []; rng = np.random.default_rng(seed)
    for scope, idx in (("all heads", np.arange(c.n)), ("MAE head only", np.where(c.head == "mae")[0])):
        axes = [a for a in AXES if not (scope != "all heads" and a == "head")]
        var = float(np.var(c.y[idx], ddof=1)); full = _adj_r2(c, axes, idx); seed_share = c.sigma ** 2 / var
        rows.append({"city": name, "scope": scope, "axis": "(all axes, additive)", "n": len(idx), "marginal_r2": full, "unique_r2": np.nan, "ci_lo": np.nan, "ci_hi": np.nan,
                     "axis_var_over_seed_var": full / seed_share, "best_level": "", "best_level_gain_sigma": np.nan, "level_range_sigma": np.nan})
        rows.append({"city": name, "scope": scope, "axis": "(seed)", "n": len(idx), "marginal_r2": seed_share, "unique_r2": np.nan, "ci_lo": np.nan, "ci_hi": np.nan,
                     "axis_var_over_seed_var": 1.0, "best_level": "", "best_level_gain_sigma": np.nan, "level_range_sigma": np.nan})
        for a in axes:
            m = _adj_r2(c, [a], idx); u = full - _adj_r2(c, [x for x in axes if x != a], idx)
            boots = [_adj_r2(c, [a], rng.choice(idx, len(idx))) for _ in range(300)]
            if a == "log_params":
                best, gain, rge = "", np.nan, np.nan
            else:
                g = pd.Series(c.y[idx]).groupby(c.df[a].values[idx]).agg(["mean", "count"]); g = g[g["count"] >= 5]
                best = str(g["mean"].idxmin()); gain = float((c.y[idx].mean() - g["mean"].min()) / c.sigma); rge = float((g["mean"].max() - g["mean"].min()) / c.sigma)
            rows.append({"city": name, "scope": scope, "axis": a, "n": len(idx), "marginal_r2": m, "unique_r2": u, "ci_lo": float(np.nanpercentile(boots, 2.5)), "ci_hi": float(np.nanpercentile(boots, 97.5)),
                         "axis_var_over_seed_var": m / seed_share, "best_level": best, "best_level_gain_sigma": gain, "level_range_sigma": rge})
    return rows


def run_variance(roots: list[Root], cities: dict, out: Path) -> None:
    rows = [r for name, c in cities.items() for r in variance_rows(name, c)]
    t = pd.DataFrame(rows); t.to_csv(out / "variance_axes.csv", index=False)
    doc = ["# evalscreen variance: which design axis moves the label", "",
           "Label = test MAE, seed 0. marginal_r2 = adjusted R2 of a one-axis model (the share of the label variance that the axis explains alone), with a bootstrap CI; unique_r2 = the "
           "adjusted R2 of the additive model of all axes minus that of the model without the axis. (seed) = sigma_seed squared over the label variance. axis_var_over_seed_var = "
           "marginal_r2 over the seed share; the rule of the map gives an axis a search budget only above 1. best_level_gain_sigma = the mean of the list minus the mean of the best level of "
           "the axis, in sigma_seed; level_range_sigma = worst level mean minus best level mean (levels with 5 architectures or more). 'MAE head only' repeats the analysis with the head fixed.", ""]
    for name in cities:
        for scope in ("all heads", "MAE head only"):
            doc.append(ec.md(t[(t.city == name) & (t.scope == scope)], ["axis", "n", "marginal_r2", "ci_lo", "ci_hi", "unique_r2", "axis_var_over_seed_var", "best_level", "best_level_gain_sigma", "level_range_sigma"], f"{name}, {scope}"))
    (out / "evalscreen_variance.md").write_text("\n".join(doc))
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
    for col in ("marginal_r2", "unique_r2", "axis_var_over_seed_var", "best_level_gain_sigma"):
        print("==", col); print(t.pivot_table(index=["scope", "axis"], columns="city", values=col, sort=False).to_string(float_format=lambda x: f"{x:.2f}"))
    print(t[t.best_level != ""].pivot(index=["scope", "axis"], columns="city", values="best_level").to_string())


# ---------------------------------------------------------------- fresh_list: a second list at a city of the benchmark
FROZEN_SINGLE_RULE = ["decoder=linear", "seq_family=gru", "seq_family=tcn"]      # candidate E, the same in every rotation at commit 2403fc6
FRESH_ROOT = "results/freshlist/pemsbay_h12"


def fit_on(train: list, cities: dict, feats: dict, kind: str, Xte: np.ndarray) -> np.ndarray:
    Xtr = np.vstack([feats[k] for k in train]); ytr = np.concatenate([rank_target(cities[k]) for k in train])
    return pr.fit_predict("ridge", Xtr, ytr, Xte) if kind == "ridge" else np.mean([pr.fit_predict("gbr", Xtr, ytr, Xte, s) for s in FIT_SEEDS], axis=0)


def run_fresh_list(roots: list[Root], cities: dict, out: Path, fresh_root: Root) -> None:
    """The four questions of the fresh list.  Nothing is fit on the fresh labels.  F1: a predictor fit on the sources ranks the
    fresh list (fit 'other cities' = no source of the same city; fit 'all sources' = with the shared list of the same city).
    F2: the frozen search-space rules.  F3: the variance by design axis against the shared list of the same city.
    F4: the best of the fresh list against the best of the shared list."""
    fk = city_key(fresh_root); assert fk not in cities, f"{fk} is among the source roots"
    f = load_cities([fresh_root])[fk]; allc = {**cities, fk: f}; all_roots = roots + [fresh_root]
    same = [k for k, c in cities.items() if c.meta["dataset"] == f.meta["dataset"]]; other = [k for k in cities if k not in same]
    if same:                                                              # sigma_seed is a property of the city and the pipeline, not of the list
        f.meta["sigma_seed_own"] = f.sigma; f.sigma = cities[same[0]].sigma; f.meta["sigma_seed"] = f.sigma
    overlap = len(set(f.ids) & set().union(*[set(c.ids) for c in cities.values()]))
    arch = arch_matrices(all_roots, allc); px = {k: np.c_[proxy_matrix(c, PROXY_NAMES), head_onehot(c)] for k, c in allc.items()}
    sink = Sink(); f1 = []
    fits = [("other cities", other)] + ([("all sources", other + same)] if same else [])
    for fit_name, train in fits:
        for label, feats, kind in (("gbr_operator_counts", arch, "gbr"), ("ridge_operator_counts", arch, "ridge"), ("gbr_proxies_head", px, "gbr")):
            p = fit_on(train, allc, feats, kind, feats[fk]); name = f"{label}, fit on {fit_name}"
            sink.add(f, name, "predictor on the sources", score_eval(p), p)
            hb = head_block(f, p); o = order_of(p)
            f1.append({"model": label, "fit": fit_name, "n_train": int(sum(allc[k].n for k in train)), "rho_all": hb["rho_all"], "rho_within_head": hb["rho_within_head"],
                       "ci_lo": hb["within_ci_lo"], "ci_hi": hb["within_ci_hi"], "regret_top1_sigma": float((f.y[o[0]] - f.y.min()) / f.sigma),
                       "regret_best_of_5_sigma": float((f.y[o[:5]].min() - f.y.min()) / f.sigma)})
    f1 = pd.DataFrame(f1)
    full = np.arange(f.n)                                                 # same-city evaluators on the fresh list, for reference
    for p in ("zico", "zico_t", "glass", "zico_sizectrl", "params"):
        if p in f.df:
            sc = f.df[p].values.astype(float); sink.add(f, p, "floor" if p == "params" else "zero-cost proxy", score_eval(sc), sc)
    for k in (1, 2, 3, 5):
        sc = -f.val_at(k); sink.add(f, f"early_val_k{k}", "brief training", score_eval(sc, k), sc)
    sink.add(f, "sh_r1_eta3", "successive halving", halving_eval(1, 3))
    if "zico_sizectrl" in f.df:
        sink.add(f, "zico_sizectrl_half_then_k5", "proxy filter", filter_eval(f.df["zico_sizectrl"].values.astype(float), 5))
    sink.add(f, "random", "floor", random_eval(), expected_random=True)
    ct, _, ht = sink.frames()
    # F2: the search-space rules
    rng = np.random.default_rng(0); best = f.y.min(); top15 = np.argsort(f.y)[:15]; f2 = []
    r10 = float(np.mean([f.y[rng.choice(f.n, 10, replace=False)].min() for _ in range(5000)]) - best) / f.sigma
    rules = {"single rule, frozen": (FROZEN_SINGLE_RULE, False)}
    if other:
        tr = {k: cities[k] for k in other}
        rules["single rule, learned on the other cities, keep half"] = (learn_cut(tr, 0.5, False), False)
        rules["pair rule, learned on the other cities, keep half"] = (learn_cut(tr, 0.5, True), True)
    for rn, (rem, pairs) in rules.items():
        masks = choice_masks(f, pairs); kept = np.ones(f.n, bool)
        for key in rem:
            kept &= ~masks.get(key, np.zeros(f.n, bool))
        idx = np.where(kept)[0]
        r5 = float(np.mean([f.y[rng.choice(idx, min(5, len(idx)), replace=False)].min() for _ in range(5000)]) - best) / f.sigma if len(idx) else np.nan
        f2.append({"rule": rn, "kept_share": float(kept.mean()), "top15_kept": int(kept[top15].sum()), "best_kept": bool(kept[top15[0]]), "random5_inside_sigma": r5,
                   "random10_full_sigma": r10, "choices_removed": "; ".join(rem)})
    f2 = pd.DataFrame(f2)
    # F3: the design axes on both lists
    f3 = pd.DataFrame(variance_rows(fk, f) + ([r for k in same for r in variance_rows(k, cities[k])]))
    ax = f3[(f3.scope == "all heads") & f3.unique_r2.notna()]
    def first_two(k):
        return list(ax[ax.city == k].sort_values("unique_r2", ascending=False).axis[:2])
    lev = f3[(f3.scope == "all heads") & (f3.best_level != "")].pivot(index="axis", columns="city", values="best_level")
    # F4: the top of the two lists
    f4 = []
    if same:
        sh = cities[same[0]]; ys, yf = np.sort(sh.y), np.sort(f.y)
        for label, a, b in (("best", ys[0], yf[0]), ("mean of the best 5", ys[:5].mean(), yf[:5].mean()), ("mean of the best 15", ys[:15].mean(), yf[:15].mean()), ("median", np.median(ys), np.median(yf))):
            f4.append({"quantity": label, "shared_list": float(a), "fresh_list": float(b), "fresh_minus_shared_sigma": float((b - a) / f.sigma)})
        f4.append({"quantity": "list spread, std over sigma_seed", "shared_list": float(np.std(sh.y, ddof=1) / f.sigma), "fresh_list": float(np.std(f.y, ddof=1) / f.sigma), "fresh_minus_shared_sigma": np.nan})
    f4 = pd.DataFrame(f4)
    # verdict
    v = []
    a = f1[(f1.model == "gbr_operator_counts") & (f1.fit == "other cities")]
    if len(a):
        a = a.iloc[0]; v.append({"question": "F1 predictor on new architectures", "value": f"rho inside the heads {a.rho_within_head:.2f}; best of 5 picks {a.regret_best_of_5_sigma:.2f} sigma",
                                 "verdict": "pass" if (a.rho_within_head >= 0.5 and a.regret_best_of_5_sigma <= 1) else ("fail" if a.rho_within_head < 0.3 else "between the lines")})
    s = f2[f2.rule == "single rule, frozen"].iloc[0]
    v.append({"question": "F2 search-space rule on new architectures", "value": f"keeps {s.kept_share:.2f} of the list and {s.top15_kept} of the top 15",
              "verdict": "pass" if (s.kept_share <= 0.5 and s.top15_kept >= 13) else ("fail" if s.top15_kept <= 11 else "between the lines")})
    if same:
        t2f, t2s = first_two(fk), first_two(same[0]); agree = int((lev[fk] == lev[same[0]]).sum()); n_ax = int(len(lev))
        ok = set(t2f) == {"head", "decoder"} and set(t2s) == {"head", "decoder"} and agree >= 4
        bad = t2f[0] != t2s[0] or (n_ax - agree) >= 2
        v.append({"question": "F3 the same design axes", "value": f"first two axes fresh {t2f}, shared {t2s}; best level equal on {agree} of {n_ax} axes", "verdict": "pass" if ok else ("fail" if bad else "between the lines")})
    verdict = pd.DataFrame(v)
    tag = fk.replace("/", "_")
    for n_, x in (("predictor", f1), ("rules", f2), ("axes", f3), ("top", f4), ("cost", ct), ("head", ht), ("verdict", verdict)):
        x.to_csv(out / f"fresh_list_{tag}_{n_}.csv", index=False)
    doc = [f"# evalscreen fresh_list: {fk}, a second list at a city of the benchmark", "",
           f"Fresh list: N = {f.n}, {overlap} architectures in common with the source lists. Sources: {list(cities)}; the same city among them: {same or 'none'}. "
           f"sigma_seed = {f.sigma:.4f}" + (f" (of the shared list of the city; the fresh list's own value from its seed runs is {f.meta['sigma_seed_own']:.4f})" if same else "") + ". "
           "Nothing is fit on the fresh labels. F1: pass = rho inside the heads >= 0.5 for boosting on operator counts fit on the other cities and its best of five picks within one "
           "sigma_seed; fail = rho below 0.3. F2: pass = the frozen single rule keeps at most half of the list and 13 or more of the top 15; fail = it removes 4 or more of the top 15. "
           "F3: pass = head and decoder are the two axes with the highest unique share on both lists and the best level is equal on four axes or more. F4 is a measurement.", ""]
    doc += [ec.md(verdict, list(verdict.columns), "Verdict"), ec.md(f1, list(f1.columns), "F1: predictors fit on the sources, read on the fresh list"),
            ec.md(f2, list(f2.columns), "F2: the search-space rules on the fresh list"), ec.md(f4, list(f4.columns), "F4: the top of the two lists") if len(f4) else ""]
    for k in [fk] + same:
        doc.append(ec.md(f3[(f3.city == k) & (f3.scope == "all heads")], ["axis", "n", "marginal_r2", "ci_lo", "ci_hi", "unique_r2", "axis_var_over_seed_var", "best_level", "best_level_gain_sigma"], f"F3: design axes, {k}, all heads"))
    doc += [ec.md(ct.sort_values(["sub_pct_median", "pct_sigma"], na_position="last"), COST_COLS, "Cost to one sigma on the fresh list", MEASURE_NOTE),
            ec.md(ht.sort_values("rho_within_head", ascending=False), HEAD_COLS, "Head control on the fresh list")]
    (out / f"evalscreen_fresh_list_{tag}.md").write_text("\n".join(doc))
    pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 120)
    for x in (verdict, f1, f2.drop(columns=["choices_removed"]), f4):
        print(x.to_string(index=False, float_format=lambda z: f"{z:.3f}")); print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["base", "proxy_combination", "curve_rank", "transfer", "halving_prior", "active_labels", "space_cut", "route", "operator_traits", "label_share", "variance", "fresh_list"])
    ap.add_argument("--roots", nargs="+", default=ROOTS)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--fresh", default=FRESH_ROOT, help="fresh_list: the root of the second list; --roots are then the source roots")
    a = ap.parse_args()
    roots = [Root(r) for r in a.roots]; out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cities = load_cities(roots)
    if a.what == "fresh_list":
        return run_fresh_list(roots, cities, out, Root(a.fresh))
    {"base": run_base, "proxy_combination": run_proxy_combination, "curve_rank": run_curve_rank, "transfer": run_transfer, "halving_prior": run_halving_prior, "active_labels": run_active_labels,
     "space_cut": run_space_cut, "route": run_route, "operator_traits": run_operator_traits, "label_share": run_label_share, "variance": run_variance}[a.what](roots, cities, out)


if __name__ == "__main__":
    main()
