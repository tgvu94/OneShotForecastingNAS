"""Per-city task statistics: the spatial-coupling measures r1 and r2 of BasicTS+ (Shao et al. 2024, Sec. V-B) and a short
FACTS-style list of series statistics, both on the training split (first 60 % of the rows, as the repo's loaders use).

    python -m pilot.task_stats --datasets pems04,pems08,metrla --out results/stzero/compare/tables

r1 and r2: for every time step t, the cosine-similarity matrices A^P over the N history windows X[t-W:t, :] and A^F over the
N future windows X[t:t+H, :].  A node pair is *indistinguishable* when A^P > e_u = 0.9 and A^F < e_l = 0.5.
r1 = indistinguishable pairs / (T x N x N); r2 = indistinguishable pairs / pairs with A^P > e_u.  All N x N pairs count,
including i = j (never indistinguishable, always similar), as the paper's T.N.N denominator implies.  Windows with zero norm
get similarity 0.  The paper uses W = H = 12 (its STF setting) and does not say whether the data are normalised; both the
z-scored (per node, training statistics) and the raw rows are written, plus our own W = 96 / H = 12 window.

Writes <out>/spatial_coupling.csv + .md (one row per dataset and setting) and <out>/task_stats.csv (one row per dataset).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from pilot import datasets
from pilot.paths import COMPARE_DIR, Root

E_U, E_L = 0.9, 0.5
TRAIN_SHARE = 0.6  # experiments/datasets/get_PEMS_dataset.py: num_train = int(len(data_raw) * 0.6)


def load_train(dataset: str) -> tuple[np.ndarray, np.ndarray]:
    """(raw, zscored) training rows of channel 0, shape (T_train, N)."""
    d = np.load(datasets.npz_path(dataset))
    a = d[d.files[0]]
    x = a[..., 0].astype(np.float64) if a.ndim == 3 else a.astype(np.float64)
    n_train = int(len(x) * TRAIN_SHARE)
    raw = x[:n_train]
    mu, sd = raw.mean(0), raw.std(0)
    sd[sd == 0] = 1.0
    return raw, (raw - mu) / sd


def _unit(w: torch.Tensor) -> torch.Tensor:
    """(T, W, N) -> columns normalised to unit L2 norm over W; zero-norm columns stay zero."""
    n = w.norm(dim=1, keepdim=True)
    return torch.where(n > 0, w / n.clamp_min(1e-12), torch.zeros_like(w))


@torch.no_grad()
def r1_r2(x: np.ndarray, W: int, H: int, chunk: int = 128, e_u: float = E_U, e_l: float = E_L) -> dict:
    X = torch.from_numpy(np.ascontiguousarray(x)).float()
    T, N = X.shape
    ts = torch.arange(W, T - H + 1)
    n_indist = n_similar = 0
    for s in range(0, len(ts), chunk):
        tt = ts[s:s + chunk]
        P = torch.stack([X[t - W:t] for t in tt])          # (c, W, N)
        F = torch.stack([X[t:t + H] for t in tt])          # (c, H, N)
        P, F = _unit(P), _unit(F)
        AP = torch.bmm(P.transpose(1, 2), P)               # (c, N, N) cosine over history windows
        AF = torch.bmm(F.transpose(1, 2), F)
        sim = AP > e_u
        n_similar += int(sim.sum())
        n_indist += int((sim & (AF < e_l)).sum())
    n_steps = int(len(ts))
    return {"W": W, "H": H, "T_steps": n_steps, "N": int(N), "n_pairs": n_steps * N * N, "n_similar_history": n_similar,
            "n_indistinguishable": n_indist, "r1": n_indist / (n_steps * N * N), "r2": n_indist / max(n_similar, 1),
            "r1_permille": 1000.0 * n_indist / (n_steps * N * N), "r2_permille": 1000.0 * n_indist / max(n_similar, 1)}


def acf(x: np.ndarray, lag: int) -> float:
    """Median over nodes of the lag-``lag`` autocorrelation of the z-scored training rows."""
    if lag >= len(x) - 2:
        return float("nan")
    a, b = x[:-lag], x[lag:]
    a = a - a.mean(0)
    b = b - b.mean(0)
    den = np.sqrt((a ** 2).sum(0) * (b ** 2).sum(0))
    den[den == 0] = np.nan
    return float(np.nanmedian((a * b).sum(0) / den))


def series_stats(dataset: str, raw: np.ndarray, z: np.ndarray, root: Root) -> dict:
    from scipy.stats import kurtosis, skew

    T, N = raw.shape
    A = np.load(root.adj) if root.adj.exists() else None
    naive = json.load(open(root.naive_baselines)) if root.naive_baselines.exists() else {}
    diff = np.diff(z, axis=0)
    return {"dataset": dataset, "n_nodes": int(N), "T_train": int(T), "mean": float(raw.mean()), "std": float(raw.std()),
            "cv_median_node": float(np.median(raw.std(0) / np.where(raw.mean(0) == 0, np.nan, raw.mean(0)))),
            "skew_median_node": float(np.median(skew(raw, axis=0))), "kurtosis_median_node": float(np.median(kurtosis(raw, axis=0))),
            "frac_zero": float((raw == 0).mean()), "acf_lag1": acf(z, 1), "acf_lag12": acf(z, 12), "acf_lag288": acf(z, 288),
            "diff_std_over_std": float(diff.std() / z.std()),
            "n_edges": int(A.sum() // 2) if A is not None else np.nan, "density": float(A.sum() / (N * (N - 1))) if A is not None else np.nan,
            "mean_degree": float(A.sum(1).mean()) if A is not None else np.nan,
            "naive_last_value_val_mae": naive.get("val", {}).get("last_value", {}).get("mae", np.nan),
            "naive_train_mean_val_mae": naive.get("val", {}).get("train_mean", {}).get("mae", np.nan)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", default="pems04,pems08,metrla")
    ap.add_argument("--horizon", type=int, default=12, help="root used for the adjacency and naive baselines: results/stzero/<ds>_h<horizon>")
    ap.add_argument("--out", default=f"{COMPARE_DIR}/tables")
    ap.add_argument("--windows", default="12/12,96/12", help="W/H pairs for r1, r2")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows, stats = [], []
    for ds in [d.strip() for d in args.datasets.split(",") if d.strip()]:
        raw, z = load_train(ds)
        root = Root.for_setting(ds, args.horizon)
        for wh in args.windows.split(","):
            W, H = (int(v) for v in wh.split("/"))
            for label, x in (("zscore", z), ("raw", raw)):
                r = r1_r2(x, W, H)
                rows.append({"dataset": ds, "scaling": label, **r})
                print(f"{ds} {label} W={W} H={H}: r1 = {r['r1_permille']:.3f} permille, r2 = {r['r2_permille']:.2f} permille ({r['n_indistinguishable']} of {r['n_similar_history']} similar-history pairs)")
        st = series_stats(ds, raw, z, root)
        prim = next(r for r in rows if r["dataset"] == ds and r["scaling"] == "zscore" and r["W"] == 12 and r["H"] == 12)
        st.update({"r1_permille_w12": prim["r1_permille"], "r2_permille_w12": prim["r2_permille"]})
        stats.append(st)
    df = pd.DataFrame(rows)
    df.to_csv(out / "spatial_coupling.csv", index=False)
    ts = pd.DataFrame(stats)
    ts.to_csv(out / "task_stats.csv", index=False)
    L = ["# Spatial coupling of each city (BasicTS+ r1, r2) and series statistics, training split", "",
         f"Indistinguishable pair: cosine(history) > {E_U} and cosine(future) < {E_L}. r1 = indistinguishable / (T N N); "
         "r2 = indistinguishable / similar-history pairs. Per-mille scale as in the paper's Fig. 4. The paper reports W = H = 12 on "
         "11 datasets without a value table; the raw and z-scored rows bracket its unstated normalisation.", "",
         "| dataset | scaling | W | H | steps | r1 (permille) | r2 (permille) | indistinguishable | similar history |", "|---|---|---|---|---|---|---|---|---|"]
    for _, r in df.iterrows():
        L.append(f"| {r.dataset} | {r.scaling} | {r.W} | {r.H} | {r.T_steps} | {r.r1_permille:.3f} | {r.r2_permille:.2f} | {r.n_indistinguishable} | {r.n_similar_history} |")
    L += ["", "## Series statistics (training split, channel 0, raw unless stated)", "",
          "| dataset | N | T | mean | std | CV (median node) | skew | kurtosis | zeros | ACF lag 1 / 12 / 288 (z-scored) | diff std / std | edges | density | naive last-value val MAE |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, s in ts.iterrows():
        L.append(f"| {s.dataset} | {s.n_nodes} | {s.T_train} | {s['mean']:.1f} | {s['std']:.1f} | {s.cv_median_node:.2f} | {s.skew_median_node:.2f} | {s.kurtosis_median_node:.2f} | "
                 f"{s.frac_zero:.3f} | {s.acf_lag1:.3f} / {s.acf_lag12:.3f} / {s.acf_lag288:.3f} | {s.diff_std_over_std:.3f} | {s.n_edges} | {s.density:.4f} | {s.naive_last_value_val_mae:.4f} |")
    (out / "spatial_coupling.md").write_text("\n".join(L) + "\n")
    print(f"-> {out / 'spatial_coupling.csv'}, {out / 'spatial_coupling.md'}, {out / 'task_stats.csv'}")


if __name__ == "__main__":
    main()
