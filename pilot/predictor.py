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
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

from pilot.analyze import partial_spearman
from pilot.genotype import load_archs
from pilot.paths import COMPARE_DIR, Root

HEADS = ["mse", "mae", "quantile"]
DECODERS = ["linear", "seq"]


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
    return df


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
    ap.add_argument("--task-stats", default=f"{COMPARE_DIR}/tables/task_stats.csv")
    ap.add_argument("--task-cols", default="n_nodes,r1_permille_w12,r2_permille_w12,acf_lag1,acf_lag12,acf_lag288,cv_median_node,frac_zero,density,naive_last_value_val_mae,diff_std_over_std")
    ap.add_argument("--out", default=f"{COMPARE_DIR}/tables")
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--seeds", default="0,1,2", help="fit seeds for the boosting models; the table reports the mean prediction")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    roots = [Root(r) for r in args.roots]
    cities = {r.dataset: load_city(r) for r in roots}
    task = pd.read_csv(args.task_stats).set_index("dataset")
    task_cols = [c for c in args.task_cols.split(",") if c in task.columns]
    arch_cols = sorted(set().union(*[set(c.columns) - {"arch_id", "val_mae", "params", "city", "target"} for c in cities.values()]))
    for c in cities.values():
        for col in arch_cols:
            if col not in c:
                c[col] = 0
    seeds = [int(s) for s in args.seeds.split(",")]
    rows = []
    for held in cities:
        train = pd.concat([c for k, c in cities.items() if k != held], ignore_index=True)
        test = cities[held]
        Xa_tr, Xa_te = train[arch_cols].values.astype(float), test[arch_cols].values.astype(float)
        T_tr = task.loc[train.city, task_cols].values.astype(float)
        T_te = task.loc[[held] * len(test), task_cols].values.astype(float)
        mu, sd = T_tr.mean(0), T_tr.std(0)
        sd[sd == 0] = 1.0
        T_tr, T_te = (T_tr - mu) / sd, (T_te - mu) / sd
        ytr = train.target.values
        preds = {"ridge arch-only": fit_predict("ridge", Xa_tr, ytr, Xa_te),
                 "gbr arch-only": np.mean([fit_predict("gbr", Xa_tr, ytr, Xa_te, s) for s in seeds], axis=0),
                 "gbr arch + task stats": np.mean([fit_predict("gbr", np.c_[Xa_tr, T_tr], ytr, np.c_[Xa_te, T_te], s) for s in seeds], axis=0)}
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
    L = ["# Option 3 of Branch 3b: predictor on our labels, leave-one-city-out", "",
         "Target: within-city rank of -val MAE (seed 0) in [0, 1]. Features: operator counts per cell, edge counts, head, decoder, log params, log FLOPs; "
         f"task statistics {task_cols} (z-scored over the training cities). Spearman with -val MAE on the held-out city, 95 % bootstrap CI "
         f"({args.n_boot} samples), partial rho after the rank regression on log params. Boosting predictions are the mean over fit seeds {seeds}.", "",
         "With two training cities every task statistic takes two values in the training set, so the task-aware model can learn only a city x operator "
         "interaction, and the held-out city's statistics are an extrapolation. This is a property of a three-city benchmark, not of the predictor.", "",
         "| held-out city | N | trained on | predictor | rho (95 % CI) | partial rho (log params) |", "|---|---|---|---|---|---|"]
    for _, r in df.iterrows():
        L.append(f"| {r.held_out} | {r.n} | {r.train_cities} ({r.n_train}) | {r.predictor} | {r.spearman:+.2f} ({r.ci_lo:+.2f}, {r.ci_hi:+.2f}) | {r.partial_params:+.2f} |")
    (out / "predictor_loco.md").write_text("\n".join(L) + "\n")
    print(df.to_string(index=False, float_format=lambda v: f"{v:+.2f}"))
    json.dump({"roots": [str(r.dir) for r in roots], "n_per_city": {k: int(len(v)) for k, v in cities.items()}, "arch_cols": arch_cols,
               "task_cols": task_cols, "seeds": seeds}, open(out / "predictor_loco.json", "w"), indent=2)


if __name__ == "__main__":
    main()
