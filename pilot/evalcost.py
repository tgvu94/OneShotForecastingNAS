"""evalcost: every cheap evaluator of the benchmark on two axes, quality (regret of its pick) and cost (GPU-hours).

    python -m pilot.evalcost                                   # the three h12 roots, out = results/stzero/compare/tables
    python -m pilot.evalcost --roots results/stzero/pems04_h12 --target val_mae

Inputs, all stored: <root>/tables/joined.csv (labels, proxies, params, head, family) and <root>/train/<id>/seed0/metrics.json
(the per-epoch history: val_mae, test_mae, seconds).  No training, no forward pass.

Evaluators
* floors: random pick (expected regret over draws), params, flops, transfer (the top-k of another city)
* stored zero-cost proxies (PROXIES), plus the size-controlled ZiCo and regularised SWAP of pilot.analyze
* early-val k: rank by the validation MAE after k epochs; cost = the logged seconds of those k epochs over all N
* successive halving on the logged curves: r0 epochs per round, keep the top 1/eta by val MAE, until one survives
* proxy filter: top half by proxy, then early-val k on the survivors; and the count of true top-10 % architectures the filter drops

Quality = regret of the evaluator's pick: test MAE of its top-1 minus the best test MAE in the set; and the best-of-top-5
(the search trains the five it ranks first and keeps the best).  Regret is in MAE units and, where a seed subset exists, in
units of sigma_seed (std of the test MAE over seeds 0 to 2 of the same architecture, mean over the subset; provisional
until the 50-architecture subset is trained).  Cost = GPU-hours on the hardware of the logs, from the logged seconds.
Secondary: Spearman rho with -target, partial rho after log params, rho inside each head (n-weighted mean).

Sign convention as in pilot.analyze: a score is correlated with -MAE; a good evaluator has positive rho and its pick is argmax.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

from pilot.analyze import derived_scores, partial_spearman
from pilot.paths import COMPARE_DIR, Root

PROXIES = ["zico", "zico_sizectrl", "swap", "swap_reg", "nwot", "synflow_all", "snip_all", "grasp_all", "grad_norm_all",
           "fisher", "jacov", "zen", "l2_norm_all", "plain_all",
           "zico_t", "zico_s", "glass", "glass_t", "glass_s", "nwot_per_layer"]
FLOORS = ["params", "flops"]
PROXY_COST_H = 0.0   # a zero-cost proxy costs seconds per architecture; recorded as 0 on the GPU-hour axis, stated in the md


# ---------------------------------------------------------------- loading
def load_root(root: Root, target: str) -> tuple[pd.DataFrame, dict]:
    """joined.csv plus the per-epoch curves.  Returns (df, curves) with curves[arch_id] = DataFrame(epoch rows)."""
    df = pd.read_csv(root.tables / "joined.csv")
    derived_scores(df)
    curves, seed_rows = {}, []
    for aid in df.arch_id:
        for s in (0, 1, 2):
            p = root.dir / "train" / aid / f"seed{s}" / "metrics.json"
            if not p.exists():
                continue
            m = json.load(open(p))
            if m.get("status") != "done":
                continue
            if s == 0:
                curves[aid] = pd.DataFrame(m["history"])
            seed_rows.append({"arch_id": aid, "seed": s, "test_mae": m["test_mae"], "val_mae": m["val_mae"]})
    seeds = pd.DataFrame(seed_rows)
    sig = seeds.groupby("arch_id")[target].agg(["std", "count"])
    sig = sig[sig["count"] >= 3]
    meta = {"sigma_seed": float(sig["std"].mean()) if len(sig) else float("nan"), "sigma_seed_n_arch": int(len(sig)),
            "n": int(len(df)), "target": target, "max_epochs": int(max(len(c) for c in curves.values()))}
    df = df[df.arch_id.isin(curves)].reset_index(drop=True)
    return df, {"curves": curves, "meta": meta}


# ---------------------------------------------------------------- measures
def regret(df: pd.DataFrame, score: np.ndarray, target: str, k: int = 5) -> dict:
    """Regret of argmax(score) and of the best among the top-k by score, in target units."""
    y = df[target].values.astype(float)
    best = float(np.nanmin(y))
    ok = np.isfinite(score)
    if ok.sum() < 2:
        return {"regret_top1": np.nan, "regret_best_of_5": np.nan, "pick_rank_pct": np.nan}
    order = np.argsort(-np.where(ok, score, -np.inf))
    top1, topk = order[0], order[:k]
    pct = float((rankdata(y)[top1] - 1) / max(len(y) - 1, 1) * 100)   # 0 % = the best architecture
    return {"regret_top1": float(y[top1] - best), "regret_best_of_5": float(np.nanmin(y[topk]) - best), "pick_rank_pct": pct}


def rho_block(df: pd.DataFrame, score: np.ndarray, target: str) -> dict:
    d = df.assign(_s=score)
    out = {"rho": np.nan, "rho_partial": np.nan, "rho_within_head": np.nan}
    m = d["_s"].notna() & d[target].notna()
    if m.sum() >= 4 and np.std(d.loc[m, "_s"]) > 0:
        out["rho"] = float(spearmanr(d.loc[m, "_s"], -d.loc[m, target]).correlation)
        out["rho_partial"] = partial_spearman(d.loc[m], "_s", "params", target)
        ws, rs = [], []
        for h, g in d.loc[m].groupby("head"):
            if len(g) >= 8 and np.std(g["_s"]) > 0:
                rs.append(spearmanr(g["_s"], -g[target]).correlation); ws.append(len(g))
        if ws:
            out["rho_within_head"] = float(np.average(rs, weights=ws))
    return out


def random_regret(df: pd.DataFrame, target: str, n_draw: int = 5000, seed: int = 0) -> dict:
    y = df[target].values.astype(float); best = np.nanmin(y)
    rng = np.random.default_rng(seed)
    r1 = y[rng.integers(0, len(y), n_draw)] - best
    r5 = np.array([np.min(y[rng.choice(len(y), 5, replace=False)]) for _ in range(n_draw)]) - best
    return {"regret_top1": float(r1.mean()), "regret_best_of_5": float(r5.mean()), "pick_rank_pct": 50.0}


# ---------------------------------------------------------------- evaluators on the curves
def early_val(curves: dict, ids, k: int) -> tuple[np.ndarray, float]:
    """Score = -val MAE after k epochs (the last logged epoch if the run stopped before k); cost = seconds of those epochs."""
    s, secs = [], 0.0
    for aid in ids:
        c = curves[aid]; kk = min(k, len(c))
        s.append(-float(c.val_mae.iloc[kk - 1])); secs += float(c.seconds.iloc[:kk].sum())
    return np.array(s), secs / 3600


def full_cost(curves: dict, ids) -> float:
    return sum(float(curves[a].seconds.sum()) for a in ids) / 3600


def successive_halving(df: pd.DataFrame, curves: dict, target: str, r0: int, eta: int, max_epochs: int) -> dict:
    """Round j trains the survivors to r0 * eta**j epochs (capped), keeps the top 1/eta by val MAE at that epoch.
    Stops when one survives or the cap is reached (then the best val MAE at the cap wins).  Cost = seconds consumed."""
    ids = list(df.arch_id); alive = list(range(len(ids))); secs = 0.0; done = np.zeros(len(ids), dtype=int)
    y = df[target].values.astype(float); best = np.nanmin(y)
    top10 = set(np.argsort(y)[: max(1, len(y) // 10)])
    dropped_top10_round1 = None
    budget, rnd = r0, 0
    while True:
        budget = min(budget, max_epochs)
        val = []
        for i in alive:
            c = curves[ids[i]]; kk = min(budget, len(c))
            secs += float(c.seconds.iloc[done[i]:kk].sum()); done[i] = max(done[i], kk)
            val.append(float(c.val_mae.iloc[kk - 1]))
        order = [alive[j] for j in np.argsort(val)]
        if len(alive) == 1 or budget >= max_epochs:
            winner = order[0]; break
        keep = max(1, len(alive) // eta)
        survivors, cut = order[:keep], order[keep:]
        if rnd == 0:
            dropped_top10_round1 = int(len(top10 & set(cut)))
        alive = survivors; budget *= eta; rnd += 1
    top5 = order[:5]
    return {"regret_top1": float(y[winner] - best), "regret_best_of_5": float(np.min(y[top5]) - best),
            "pick_rank_pct": float((rankdata(y)[winner] - 1) / max(len(y) - 1, 1) * 100),
            "gpu_hours": secs / 3600, "rounds": rnd + 1, "dropped_top10_round1": dropped_top10_round1}


def proxy_filter(df: pd.DataFrame, curves: dict, target: str, proxy: str, k: int) -> dict:
    """Top half by proxy, then early-val k on them.  Also the count of true top-10 % architectures in the proxy's bottom half."""
    s = df[proxy].values.astype(float); y = df[target].values.astype(float)
    ok = np.isfinite(s)
    if ok.sum() < 8:
        return {}
    order = np.argsort(-np.where(ok, s, -np.inf)); half = len(order) // 2
    top, bottom = order[:half], order[half:]
    top10 = set(np.argsort(y)[: max(1, len(y) // 10)])
    sub = df.iloc[top].reset_index(drop=True)
    sc, hrs = early_val(curves, sub.arch_id, k)
    r = regret(sub, sc, target)
    best_all = np.nanmin(y)
    pick = int(top[int(np.argmax(sc))])
    return {"top10_in_bottom_half": int(len(top10 & set(bottom))), "top10_total": len(top10),
            "regret_top1": float(y[pick] - best_all), "regret_best_of_5": float(np.min(y[top[np.argsort(-sc)[:5]]]) - best_all),
            "gpu_hours": hrs}


def transfer(dfs: dict, target: str, k: int = 5) -> pd.DataFrame:
    """Top-k of a source city by target, scored at every other city on the shared architectures."""
    rows = []
    for src, ds in dfs.items():
        for dst, dd in dfs.items():
            if src == dst:
                continue
            shared = sorted(set(ds.arch_id) & set(dd.arch_id))
            if len(shared) < 10:
                continue
            s = ds[ds.arch_id.isin(shared)].set_index("arch_id"); d = dd[dd.arch_id.isin(shared)].set_index("arch_id")
            top = s[target].nsmallest(k).index
            y = d[target]; best = y.min()
            pct = (rankdata(y.values)[[list(y.index).index(a) for a in top]] - 1) / max(len(y) - 1, 1) * 100
            rows.append({"source": src, "target_city": dst, "n_shared": len(shared), "regret_top1": float(y[top[0]] - best),
                         "regret_best_of_5": float(y[top].min() - best), "top1_rank_pct": float(pct[0]), "top5_mean_rank_pct": float(pct.mean()),
                         "rho_cities": float(spearmanr(s.loc[shared, target], d.loc[shared, target]).correlation)})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- driver
def run_city(root: Root, target: str, ks: list[int], sh_r0: list[int], etas: list[int]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    df, aux = load_root(root, target)
    curves, meta = aux["curves"], aux["meta"]
    ids = list(df.arch_id)
    rows = []

    def add(name, kind, score, hours, extra=None):
        r = {"city": root.dataset, "evaluator": name, "kind": kind, "gpu_hours": hours, **regret(df, score, target), **rho_block(df, score, target)}
        if extra:
            r.update(extra)
        rows.append(r)

    rows.append({"city": root.dataset, "evaluator": "random", "kind": "floor", "gpu_hours": 0.0, **random_regret(df, target),
                 "rho": 0.0, "rho_partial": 0.0, "rho_within_head": 0.0})
    for p in FLOORS:
        add(p, "floor", df[p].values.astype(float), 0.0)
    for p in PROXIES:
        if p in df and df[p].notna().sum() >= 8:
            add(p, "zero-cost proxy", df[p].values.astype(float), PROXY_COST_H)
    for k in ks:
        sc, hrs = early_val(curves, ids, k)
        add(f"early_val_k{k}", "brief training", sc, hrs, {"k": k})
    add("full_training", "ceiling", -df[target].values.astype(float), full_cost(curves, ids))

    sh_rows = []
    for r0 in sh_r0:
        for eta in etas:
            res = successive_halving(df, curves, target, r0, eta, meta["max_epochs"])
            sh_rows.append({"city": root.dataset, "evaluator": f"sh_r{r0}_eta{eta}", "kind": "successive halving", "r0": r0, "eta": eta, **res})
    filt_rows = []
    for p in ["zico", "swap", "zico_sizectrl", "params"]:
        if p in df:
            for k in [1, 3, 5]:
                res = proxy_filter(df, curves, target, p, k)
                if res:
                    filt_rows.append({"city": root.dataset, "evaluator": f"{p}_half_then_k{k}", "kind": "proxy filter", "proxy": p, "k": k, **res})
    return pd.DataFrame(rows), pd.DataFrame(sh_rows), pd.DataFrame(filt_rows), {"df": df, "meta": meta}


def to_sigma(t: pd.DataFrame, sigma: float) -> pd.DataFrame:
    t = t.copy()
    for c in ("regret_top1", "regret_best_of_5"):
        t[c + "_sigma"] = t[c] / sigma if sigma and np.isfinite(sigma) else np.nan
    return t


def md(t: pd.DataFrame, cols: list[str], title: str, note: str = "") -> str:
    lines = [f"### {title}", ""]
    if note:
        lines += [note, ""]
    lines.append("| " + " | ".join(cols) + " |"); lines.append("|" + "---|" * len(cols))
    for _, r in t.iterrows():
        cells = []
        for c in cols:
            v = r.get(c, "")
            cells.append(f"{v:.3f}" if isinstance(v, float) and np.isfinite(v) else ("" if isinstance(v, float) else str(v)))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", nargs="+", default=["results/stzero/pems04_h12", "results/stzero/pems08_h12", "results/stzero/metrla_h12"])
    ap.add_argument("--target", default="test_mae", choices=["test_mae", "val_mae"])
    ap.add_argument("--ks", default="1,2,3,4,5,6,8,10,15")
    ap.add_argument("--sh-r0", default="1,2,3")
    ap.add_argument("--etas", default="2,3")
    ap.add_argument("--out", default=f"{COMPARE_DIR}/tables")
    a = ap.parse_args()
    ks = [int(x) for x in a.ks.split(",")]; r0s = [int(x) for x in a.sh_r0.split(",")]; etas = [int(x) for x in a.etas.split(",")]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    main_t, sh_t, filt_t, dfs, metas = [], [], [], {}, {}
    for r in a.roots:
        root = Root.from_tables_dir(r)
        m, s, f, aux = run_city(root, a.target, ks, r0s, etas)
        sig = aux["meta"]["sigma_seed"]
        main_t.append(to_sigma(m, sig)); sh_t.append(to_sigma(s, sig)); filt_t.append(to_sigma(f, sig))
        dfs[root.dataset] = aux["df"]; metas[root.dataset] = aux["meta"]
    main_t, sh_t, filt_t = pd.concat(main_t), pd.concat(sh_t), pd.concat(filt_t)
    tr = transfer(dfs, a.target)
    main_t.to_csv(out / "evalcost_points.csv", index=False); sh_t.to_csv(out / "evalcost_halving.csv", index=False)
    filt_t.to_csv(out / "evalcost_filter.csv", index=False); tr.to_csv(out / "evalcost_transfer.csv", index=False)
    json.dump(metas, open(out / "evalcost_meta.json", "w"), indent=1)

    doc = [f"# evalcost: cost against quality of every cheap evaluator, target = {a.target} (seed 0)", "",
           "Regret = the evaluator's pick minus the best architecture of the set, in MAE units of the normalised target and in "
           "units of sigma_seed. sigma_seed is provisional: the std over seeds 0 to 2 of the few architectures that have three seeds "
           "(count per city below). GPU-hours are the logged seconds on one H100 3g.40gb slice. A zero-cost proxy is recorded at 0 h "
           "(seconds per architecture). rho is Spearman with -MAE; partial = after rank regression on log params; within head = "
           "n-weighted mean of rho inside each loss head.", ""]
    for c, m in metas.items():
        doc.append(f"- {c}: N = {m['n']}, max epochs {m['max_epochs']}, sigma_seed = {m['sigma_seed']:.4f} over {m['sigma_seed_n_arch']} architectures")
    doc.append("")
    cols = ["evaluator", "kind", "gpu_hours", "regret_top1", "regret_top1_sigma", "regret_best_of_5", "regret_best_of_5_sigma", "pick_rank_pct", "rho", "rho_partial", "rho_within_head"]
    for c in metas:
        doc.append(md(main_t[main_t.city == c], cols, f"{c}: floors, proxies, brief training, ceiling"))
        doc.append(md(sh_t[sh_t.city == c], ["evaluator", "gpu_hours", "rounds", "dropped_top10_round1", "regret_top1", "regret_top1_sigma", "regret_best_of_5", "pick_rank_pct"],
                      f"{c}: successive halving on the logged curves"))
        doc.append(md(filt_t[filt_t.city == c], ["evaluator", "gpu_hours", "top10_in_bottom_half", "top10_total", "regret_top1", "regret_top1_sigma", "regret_best_of_5"],
                      f"{c}: proxy as a filter, then brief training on the top half"))
    doc.append(md(tr, ["source", "target_city", "n_shared", "regret_top1", "regret_best_of_5", "top1_rank_pct", "top5_mean_rank_pct", "rho_cities"],
                  "Transfer: the top-5 of a source city, scored at the target city", "rho_cities = Spearman of the labels of the shared architectures between the two cities."))
    (out / "evalcost.md").write_text("\n".join(doc))
    print("\n".join(doc))


if __name__ == "__main__":
    main()
