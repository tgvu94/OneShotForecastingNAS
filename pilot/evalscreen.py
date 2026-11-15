"""evalscreen: screening of candidate evaluators on the stored labels, per-epoch logs and proxy scores of the benchst roots.

    python -m pilot.evalscreen base                 # the stored evaluators on the common measure
    python -m pilot.evalscreen proxy_combination    # a model on the proxy scores, fit on the other cities
    python -m pilot.evalscreen curve_rank           # a model on the first k epochs, fit on the other cities
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


def load_cities(roots: list[Root]) -> dict:
    out = {}
    for r in roots:
        df, aux = ec.load_root(r, TARGET); cost = ec.load_cost(r); curves = aux["curves"]
        val = [curves[a].val_mae.values.astype(float) for a in df.arch_id]
        trn = [curves[a].train_loss.values.astype(float) for a in df.arch_id]
        cumh = [np.concatenate([[0.0], np.cumsum(curves[a].seconds.values.astype(float))]) / 3600 for a in df.arch_id]
        out[r.dataset] = City(r.dataset, df, val, trn, cumh, {**aux["meta"], **cost})
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
    raw = {r.dataset: pr.load_city(r) for r in roots}
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["base", "proxy_combination", "curve_rank"])
    ap.add_argument("--roots", nargs="+", default=ROOTS)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    roots = [Root(r) for r in a.roots]; out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cities = load_cities(roots)
    {"base": run_base, "proxy_combination": run_proxy_combination, "curve_rank": run_curve_rank}[a.what](roots, cities, out)


if __name__ == "__main__":
    main()
