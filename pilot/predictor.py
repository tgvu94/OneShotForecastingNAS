"""Option 3 of Branch 3b: a small predictor on our own labels, with task statistics as input, tested leave-one-city-out.

    python -m pilot.predictor --roots results/stzero/pems04_h12 results/stzero/pems08_h12 results/stzero/metrla_h12 \
        --task-stats results/stzero/compare/tables/task_stats.csv --out results/stzero/compare/tables

Architecture encoding (the simplest operator-description form of F2): counts of every operator name in the seq encoder, the
seq decoder, the flat cell and the graph cell, the edge count of each cell, the head and decoder type (one-hot), log parameter
count and log FLOPs.  Task encoding: the row of task_stats.csv for the city (node count, r1, r2, autocorrelations, spread,
graph density, naive-baseline MAE), standardised over the training cities.  Target: the within-city rank of -val MAE scaled to
[0, 1], so cities with different error scales can be pooled.

Rotations: for each held-out city, fit on the other two and score the held-out architectures.  Reported per rotation:
Spearman rho with -val MAE on the held-out city, its 95 % bootstrap CI, and the partial rho after the rank regression on
log parameter count.  Three predictors: ridge on the architecture features alone; gradient boosting on the architecture
features alone; gradient boosting on architecture + task features (the only one that can use the city).  A within-city 5-fold
CV row per city gives the upper reference.  With two training cities, a task feature is a two-level constant inside the training
set, so option 3 can only learn an interaction between city and operator; this is stated in the output.

Direction 4 of the evalcost plan adds, on the same features:
(a) leave one operator family out, within a city: fit on the other families, score the held-out family; Spearman and Kendall
    tau (pass line F2: Kendall >= 0.5 on the held-out family on two of three cities); families with fewer than 8 architectures skip;
(b) the stored zero-cost proxies as features (PROXY_FEATS), each rank-normalised inside its city to [0, 1] so that cities with
    different scales pool; LOCO rows "gbr proxies only" and "gbr arch + proxies";
(c) a learning curve within a city: fit on n random labels, score the rest, n in --curve-n, --curve-draws draws; the cost of the
    n labels in GPU-hours of that root (logged seconds) and the smallest n whose mean Spearman reaches 0.6.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, rankdata, spearmanr

from pilot.analyze import partial_spearman
from pilot.genotype import load_archs
from pilot.paths import COMPARE_DIR, Root

HEADS = ["mse", "mae", "quantile"]
DECODERS = ["linear", "seq"]
PROXY_FEATS = ["zico", "zico_t", "zico_s", "glass", "glass_t", "glass_s", "zico_sizectrl", "nwot", "nwot_per_layer", "swap", "synflow_all",
               "snip_all", "grad_norm_all", "grasp_all", "fisher", "jacov", "zen", "l2_norm_all", "plain_all", "params", "flops"]
META_COLS = {"arch_id", "val_mae", "params", "city", "target", "seq_family", "graph_family", "hours"}


def arch_features(g: dict) -> dict:
    f = {}
    for cell, edges in (("enc", g["seq"]["encoder"]), ("dec", g["seq"]["decoder"]), ("flat", g["flat"]["cell"]),
                        ("graph", g["graph"]["cell"] if g.get("graph") else [])):
        ops = [op for _, _, op in edges if op is not None]
        f[f"{cell}_n_edges"] = len(ops)
        for op, c in Counter(ops).items():
            f[f"{cell}_{op}"] = c
    f["has_graph"] = int(bool(g.get("graph")))
    for h in HEADS:
        f[f"head_{h}"] = int(g["head"] == h)
    for d in DECODERS:
        f[f"dec_{d}"] = int(g["seq"]["decoder_type"] == d)
    return f


def load_city(root: Root) -> pd.DataFrame:
    j = pd.read_csv(root.tables / "joined.csv")
    feats = {r["arch_id"]: arch_features(r["genotype"]) for r in load_archs(root.archs_jsonl)}
    F = pd.DataFrame([feats[a] for a in j.arch_id]).fillna(0)
    F["log_params"], F["log_flops"] = np.log(j.params.values), np.log(j.flops.values)
    F.index = j.index
    df = pd.concat([j[["arch_id", "val_mae", "params"]], F], axis=1)
    df["city"] = root.dataset
    df["target"] = (rankdata(-df.val_mae) - 1) / max(len(df) - 1, 1)   # within-city rank of -val MAE in [0, 1]
    for c in ("seq_family", "graph_family"):
        df[c] = j[c].values if c in j else "none"
    df["hours"] = j["train_seconds"].values / 3600 if "train_seconds" in j else np.nan
    for p in PROXY_FEATS:                                                # rank inside the city, NaN -> the middle
        if p in j:
            v = j[p].values.astype(float); r = np.full(len(v), 0.5)
            ok = np.isfinite(v); r[ok] = (rankdata(v[ok]) - 1) / max(ok.sum() - 1, 1)
            df[f"px_{p}"] = r
    return df


def evaluate_tau(pred: np.ndarray, d: pd.DataFrame) -> dict:
    y = -d.val_mae.values
    return {"n": int(len(d)), "spearman": float(spearmanr(pred, y).correlation), "kendall": float(kendalltau(pred, y).correlation)}


def family_holdout(cities: dict, arch_cols: list, seeds: list, min_n: int = 8) -> pd.DataFrame:
    """(a) inside each city, hold out every seq family and every graph family in turn."""
    rows = []
    for city, d in cities.items():
        X = d[arch_cols].values.astype(float); y = d.target.values
        for col in ("seq_family", "graph_family"):
            for fam, g in d.groupby(col):
                te = (d[col] == fam).values
                if te.sum() < min_n or (~te).sum() < min_n:
                    continue
                p = np.mean([fit_predict("gbr", X[~te], y[~te], X[te], s) for s in seeds], axis=0)
                rows.append({"city": city, "family_kind": col, "held_out_family": fam, "n_train": int((~te).sum()), **evaluate_tau(p, d[te])})
    return pd.DataFrame(rows)


def learning_curve(cities: dict, arch_cols: list, px_cols: list, seeds: list, ns: list, draws: int) -> pd.DataFrame:
    """(c) inside each city, fit on n random labels and score the rest; mean and 5-95 % range over draws; cost of the n labels."""
    rows = []
    for city, d in cities.items():
        Xa = d[arch_cols].values.astype(float); Xp = d[arch_cols + px_cols].values.astype(float); y = d.target.values
        hours = d.hours.values.astype(float)
        for n in ns:
            if n >= len(d) - 10:
                continue
            for name, X in (("gbr arch-only", Xa), ("gbr arch + proxies", Xp)):
                rs, cost = [], []
                for k in range(draws):
                    rng = np.random.default_rng(k)
                    tr = rng.choice(len(d), n, replace=False); te = np.setdiff1d(np.arange(len(d)), tr)
                    p = fit_predict("gbr", X[tr], y[tr], X[te], seeds[0])
                    rs.append(spearmanr(p, -d.val_mae.values[te]).correlation); cost.append(np.nansum(hours[tr]))
                rows.append({"city": city, "predictor": name, "n_labels": n, "draws": draws, "spearman_mean": float(np.mean(rs)),
                             "spearman_p5": float(np.percentile(rs, 5)), "spearman_p95": float(np.percentile(rs, 95)),
                             "gpu_hours_labels": float(np.mean(cost))})
    return pd.DataFrame(rows)


def evaluate(pred: np.ndarray, d: pd.DataFrame, n_boot: int = 2000, seed: int = 0) -> dict:
    y = -d.val_mae.values
    rho = spearmanr(pred, y).correlation
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        i = rng.integers(0, len(y), len(y))
        if np.std(pred[i]) > 0 and np.std(y[i]) > 0:
            boots.append(spearmanr(pred[i], y[i]).correlation)
    lo, hi = np.nanpercentile(boots, [2.5, 97.5]) if boots else (np.nan, np.nan)
    tmp = pd.DataFrame({"pred": pred, "params": d.params.values, "val_mae": d.val_mae.values})
    return {"n": int(len(d)), "spearman": float(rho), "ci_lo": float(lo), "ci_hi": float(hi), "partial_params": partial_spearman(tmp, "pred")}


def fit_predict(kind: str, Xtr: np.ndarray, ytr: np.ndarray, Xte: np.ndarray, seed: int = 0) -> np.ndarray:
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.linear_model import RidgeCV
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    if kind == "ridge":
        m = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-2, 3, 12)))
    elif kind == "gbr":
        m = GradientBoostingRegressor(n_estimators=300, max_depth=3, learning_rate=0.03, subsample=0.8, random_state=seed)
    else:
        raise KeyError(kind)
    m.fit(Xtr, ytr)
    return m.predict(Xte)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", nargs="+", default=["results/stzero/pems04_h12", "results/stzero/pems08_h12", "results/stzero/metrla_h12"])
    ap.add_argument("--task-stats", nargs="+", default=[f"{COMPARE_DIR}/tables/task_stats.csv"], help="one or more task_stats csv files (rows = cities)")
    ap.add_argument("--curve-n", default="10,25,50,75,100,125")
    ap.add_argument("--curve-draws", type=int, default=20)
    ap.add_argument("--task-cols", default="n_nodes,r1_permille_w12,r2_permille_w12,acf_lag1,acf_lag12,acf_lag288,cv_median_node,frac_zero,density,naive_last_value_val_mae,diff_std_over_std")
    ap.add_argument("--out", default=f"{COMPARE_DIR}/tables")
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--seeds", default="0,1,2", help="fit seeds for the boosting models; the table reports the mean prediction")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    roots = [Root(r) for r in args.roots]
    cities = {r.dataset: load_city(r) for r in roots}
    task = pd.concat([pd.read_csv(f) for f in args.task_stats]).drop_duplicates("dataset").set_index("dataset")
    task_cols = [c for c in args.task_cols.split(",") if c in task.columns]
    all_cols = set().union(*[set(c.columns) - META_COLS for c in cities.values()])
    px_cols = sorted(c for c in all_cols if c.startswith("px_"))
    arch_cols = sorted(all_cols - set(px_cols))
    for c in cities.values():
        for col in arch_cols:
            if col not in c:
                c[col] = 0
        for col in px_cols:
            if col not in c:
                c[col] = 0.5
    seeds = [int(s) for s in args.seeds.split(",")]
    rows = []
    for held in cities:
        train = pd.concat([c for k, c in cities.items() if k != held], ignore_index=True)
        test = cities[held]
        Xa_tr, Xa_te = train[arch_cols].values.astype(float), test[arch_cols].values.astype(float)
        T_tr = task.loc[train.city, task_cols].values.astype(float)
        T_te = task.loc[[held] * len(test), task_cols].values.astype(float)
        mu, sd = np.nanmean(T_tr, 0), np.nanstd(T_tr, 0)
        sd[~np.isfinite(sd) | (sd == 0)] = 1.0
        T_tr, T_te = np.nan_to_num((T_tr - mu) / sd), np.nan_to_num((T_te - mu) / sd)
        ytr = train.target.values
        Xp_tr, Xp_te = train[px_cols].values.astype(float), test[px_cols].values.astype(float)
        preds = {"ridge arch-only": fit_predict("ridge", Xa_tr, ytr, Xa_te),
                 "gbr arch-only": np.mean([fit_predict("gbr", Xa_tr, ytr, Xa_te, s) for s in seeds], axis=0),
                 "gbr arch + task stats": np.mean([fit_predict("gbr", np.c_[Xa_tr, T_tr], ytr, np.c_[Xa_te, T_te], s) for s in seeds], axis=0),
                 "gbr proxies only": np.mean([fit_predict("gbr", Xp_tr, ytr, Xp_te, s) for s in seeds], axis=0),
                 "gbr arch + proxies": np.mean([fit_predict("gbr", np.c_[Xa_tr, Xp_tr], ytr, np.c_[Xa_te, Xp_te], s) for s in seeds], axis=0)}
        for name, p in preds.items():
            rows.append({"held_out": held, "n_train": int(len(train)), "train_cities": "+".join(k for k in cities if k != held),
                         "predictor": name, **evaluate(p, test, args.n_boot)})
        # within-city 5-fold reference (upper bound: sees the city's own labels)
        from sklearn.model_selection import KFold
        p = np.zeros(len(test))
        for tr, te in KFold(5, shuffle=True, random_state=0).split(Xa_te):
            p[te] = np.mean([fit_predict("gbr", Xa_te[tr], test.target.values[tr], Xa_te[te], s) for s in seeds], axis=0)
        rows.append({"held_out": held, "n_train": int(len(test)), "train_cities": f"{held} (5-fold CV, reference)", "predictor": "gbr arch-only, within city",
                     **evaluate(p, test, args.n_boot)})
    df = pd.DataFrame(rows)
    df.to_csv(out / "predictor_loco.csv", index=False)
    n_cities = len(cities)
    L = ["# Predictor on our labels, leave-one-city-out", "",
         "Target: within-city rank of -val MAE (seed 0) in [0, 1]. Features: operator counts per cell, edge counts, head, decoder, log params, log FLOPs; "
         f"task statistics {task_cols} (z-scored over the training cities); the stored proxies {[c[3:] for c in px_cols]} rank-normalised inside each city. "
         f"Spearman with -val MAE on the held-out city, 95 % bootstrap CI ({args.n_boot} samples), partial rho after the rank regression on log params. "
         f"Boosting predictions are the mean over fit seeds {seeds}.", "",
         f"With {n_cities - 1} training cities every task statistic takes {n_cities - 1} values in the training set, so the task-aware model can learn only a "
         "city x operator interaction, and the held-out city's statistics are an extrapolation. This is a property of a benchmark with few cities, not of the predictor.", "",
         "| held-out city | N | trained on | predictor | rho (95 % CI) | partial rho (log params) |", "|---|---|---|---|---|---|"]
    for _, r in df.iterrows():
        L.append(f"| {r.held_out} | {r.n} | {r.train_cities} ({r.n_train}) | {r.predictor} | {r.spearman:+.2f} ({r.ci_lo:+.2f}, {r.ci_hi:+.2f}) | {r.partial_params:+.2f} |")
    fam = family_holdout(cities, arch_cols, seeds)
    fam.to_csv(out / "predictor_family.csv", index=False)
    L += ["", "## Leave one operator family out, within a city (gbr arch-only)", "",
          "Fit on the other families of the same city, score the held-out family. Pass line F2: Kendall >= 0.5 on the held-out family on two of three cities.", "",
          "| city | family kind | held-out family | n held out | n train | Spearman | Kendall |", "|---|---|---|---|---|---|---|"]
    for _, r in fam.iterrows():
        L.append(f"| {r.city} | {r.family_kind} | {r.held_out_family} | {r.n} | {r.n_train} | {r.spearman:+.2f} | {r.kendall:+.2f} |")
    if len(fam):
        agg = fam.groupby(["city", "family_kind"]).apply(lambda g: pd.Series({"n_families": len(g), "kendall_weighted": np.average(g.kendall, weights=g.n),
                                                                             "families_ge_0.5": int((g.kendall >= 0.5).sum())})).reset_index()
        L += ["", "| city | family kind | families | n-weighted Kendall | families with Kendall >= 0.5 |", "|---|---|---|---|---|"]
        for _, r in agg.iterrows():
            L.append(f"| {r.city} | {r.family_kind} | {int(r.n_families)} | {r.kendall_weighted:+.2f} | {int(r['families_ge_0.5'])} |")
    ns = [int(x) for x in args.curve_n.split(",")]
    curve = learning_curve(cities, arch_cols, px_cols, seeds, ns, args.curve_draws)
    curve.to_csv(out / "predictor_curve.csv", index=False)
    L += ["", "## Learning curve within a city", "",
          f"Fit on n random labels of the city, score the rest; mean and 5-95 % range of Spearman over {args.curve_draws} draws; cost = the logged GPU-hours of the n labels.", "",
          "| city | predictor | n labels | GPU-hours of the labels | Spearman mean (5 %, 95 %) |", "|---|---|---|---|---|"]
    for _, r in curve.iterrows():
        L.append(f"| {r.city} | {r.predictor} | {r.n_labels} | {r.gpu_hours_labels:.2f} | {r.spearman_mean:+.2f} ({r.spearman_p5:+.2f}, {r.spearman_p95:+.2f}) |")
    if len(curve):
        L += ["", "| city | predictor | smallest n with mean Spearman >= 0.6 | its GPU-hours |", "|---|---|---|---|"]
        for (c, pn), g in curve.groupby(["city", "predictor"], sort=False):
            hit = g[g.spearman_mean >= 0.6].sort_values("n_labels")
            L.append(f"| {c} | {pn} | {int(hit.n_labels.iloc[0]) if len(hit) else '> ' + str(int(g.n_labels.max()))} | {hit.gpu_hours_labels.iloc[0]:.2f} |" if len(hit) else f"| {c} | {pn} | > {int(g.n_labels.max())} | |")
    (out / "predictor_loco.md").write_text("\n".join(L) + "\n")
    print(df.to_string(index=False, float_format=lambda v: f"{v:+.2f}"))
    print(fam.to_string(index=False, float_format=lambda v: f"{v:+.2f}"))
    print(curve.to_string(index=False, float_format=lambda v: f"{v:+.2f}"))
    json.dump({"roots": [str(r.dir) for r in roots], "n_per_city": {k: int(len(v)) for k, v in cities.items()}, "arch_cols": arch_cols,
               "px_cols": px_cols, "task_cols": task_cols, "seeds": seeds, "curve_n": ns, "curve_draws": args.curve_draws}, open(out / "predictor_loco.json", "w"), indent=2)


if __name__ == "__main__":
    main()
