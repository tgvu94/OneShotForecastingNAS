"""spatialgate, linear stage: is the gain of a neighbour term concentrated in a minority of the sensors?  No GPU, no training run.

    python -m pilot.spatialgate linear --datasets pems08,metrla --out results/spatialgate/compare/tables
    python -m pilot.spatialgate summary --out results/spatialgate/compare/tables      # the summary table again, from the stored files

Per sensor i, with a per-sensor linear model fit by weighted ridge on z-scored values (training statistics):
    base : value at t+h from the 12 values up to t and time-of-day terms (bias, 3 harmonics of the target time)
    plus : base and the mean of the graph neighbours' 12 values up to t (one added linear term on the neighbours' past)
    e_i, e_plus_i = MAE in the raw unit on the evaluation rows, mean over the horizons 3, 6 and 12;  d_i = e_i - e_plus_i
    c1_i = spatial residual score of Zambon and Alippi (weighted mean, over the edges of i and the evaluation rows, of the sign
           of the product of the two median-removed base residuals), mean over the horizons
Three fits per dataset: train -> validation (the main reading), first half of train -> second half, second half -> first half.
A value of 0 or NaN is missing: it is no target, and as an input it is set to the training mean of the sensor (0 after z-scoring).
A sensor with fewer than half of its training rows valid is excluded: every value of it is missing (without this rule a sensor with
no training value keeps mean 0 and deviation 1, and its later raw values enter the neighbour mean of other sensors unscaled).
Splits: first 60 % of the rows = train, next 20 % = validation, as the loaders of the repo.  The test rows are never read.

Datasets: the registry names of pilot.datasets (channel 0 of the .npz, the adjacency of its distance list or pickle), and
largestsd / largestgba / largestgla / largestca: $NAS_DATA_ROOT/LargeST/2019.h5 at 15-minute steps (mean of the valid 5-minute
values), sensors by district (11; 4; 7, 8, 12; all), adjacency.npy > 0, symmetric, zero diagonal.

Writes <out>/linear_sensors_<dataset>.csv (one row per sensor), <out>/linear_summary.csv and .md (one row per dataset).
"""
from __future__ import annotations

import argparse
import os
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from scipy import sparse
from scipy.stats import spearmanr

from pilot import datasets
from pilot.adjacency import load_adj_from_distance_csv, load_adj_from_pickle

LAGS = 12
HORIZONS = (3, 6, 12)
HARMONICS = 3
TRAIN_SHARE, VAL_SHARE = 0.6, 0.2
TOP = 0.25
MIN_TRAIN_VALID = 0.5     # a sensor with a lower share of valid training rows has no usable statistics: every value of it is missing
RIDGE = 1e-3
STEPS_PER_DAY = {"metrla": 288, "pems03": 288, "pems04": 288, "pems07": 288, "pems08": 288, "pemsbay": 288,
                 "chengdu": 144, "shenzhen": 144, "expytky": 144}
LARGEST = {"largestsd": [11], "largestgba": [4], "largestgla": [7, 8, 12], "largestca": None}
PASS_SHARE, PASS_STAB, FAIL_SHARE, FAIL_STAB = 0.50, 0.5, 0.35, 0.3     # the lines of the plan, per dataset


def _largest_dir() -> Path:
    return Path(os.environ.get("NAS_DATA_ROOT", "~/scratch/all_datasets")).expanduser() / "LargeST"


def load_largest(name: str) -> tuple[np.ndarray, np.ndarray, int]:
    import h5py

    d = _largest_dir()
    meta = pd.read_csv(d / "ca_meta.csv")
    keep = np.arange(len(meta)) if LARGEST[name] is None else np.flatnonzero(meta["District"].isin(LARGEST[name]).to_numpy())
    with h5py.File(d / "2019.h5", "r") as f:
        g = f[list(f.keys())[0]]
        ids = [s.decode() for s in g["axis0"][:]]
        assert ids == [str(i) for i in meta["ID"]], "sensor order of 2019.h5 differs from ca_meta.csv"
        v = g["block0_values"]
        T5 = v.shape[0] - v.shape[0] % 3
        out = np.zeros((T5 // 3, len(keep)), dtype=np.float32)
        step = 3 * 2880                                              # 30 days of 5-minute rows per read
        for s in range(0, T5, step):
            blk = v[s:min(s + step, T5)][:, keep].astype(np.float32)
            blk[blk == 0] = np.nan
            blk = blk.reshape(-1, 3, len(keep))
            ok = np.isfinite(blk)
            cnt = ok.sum(1)
            out[s // 3:s // 3 + len(blk)] = np.where(cnt > 0, np.where(ok, blk, 0).sum(1) / np.maximum(cnt, 1), 0)
    A = np.load(d / "adjacency.npy", mmap_mode="r")
    A = np.asarray(A[np.ix_(keep, keep)] > 0)
    A = (A | A.T).astype(np.float32)
    np.fill_diagonal(A, 0)
    return out, A, 96


def load_city(name: str) -> tuple[np.ndarray, np.ndarray, int]:
    d = np.load(datasets.npz_path(name))
    a = d[d.files[0]]
    x = (a[..., 0] if a.ndim == 3 else a).astype(np.float32)
    n = datasets.n_nodes(name)
    csv = datasets.distance_csv_path(name)
    if csv is not None and csv.exists():
        A = load_adj_from_distance_csv(csv, n)
    else:
        A, _ = load_adj_from_pickle(datasets.adj_pickle_path(name), n)
    return x, np.asarray(A, dtype=np.float32), STEPS_PER_DAY[name]


def load(name: str):
    return load_largest(name) if name in LARGEST else load_city(name)


def _spearman(a, b) -> float:
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 5 or np.ptp(a[ok]) == 0 or np.ptp(b[ok]) == 0:
        return float("nan")
    return float(spearmanr(a[ok], b[ok]).statistic)


def _top_mask(v: np.ndarray, share: float = TOP) -> np.ndarray:
    k = max(1, int(np.ceil(share * len(v))))
    m = np.zeros(len(v), dtype=bool)
    m[np.argsort(-np.nan_to_num(v, nan=-np.inf), kind="stable")[:k]] = True
    return m


class Task:
    """z-scored values, validity, neighbour means and time-of-day terms of one dataset."""

    def __init__(self, x: np.ndarray, A: np.ndarray, steps_per_day: int):
        self.T, self.N = x.shape
        self.n_train = int(self.T * TRAIN_SHARE)
        self.n_val_end = int(self.T * (TRAIN_SHARE + VAL_SHARE))
        valid = np.isfinite(x) & (x != 0)
        self.excluded = valid[:self.n_train].mean(0) < MIN_TRAIN_VALID
        valid[:, self.excluded] = False
        tr, vtr = x[:self.n_train], valid[:self.n_train]
        cnt = np.maximum(vtr.sum(0), 1)
        mu = np.where(vtr, tr, 0).sum(0) / cnt
        sd = np.sqrt(np.where(vtr, (tr - mu) ** 2, 0).sum(0) / cnt)
        sd[sd == 0] = 1.0
        z = np.where(valid, (x - mu) / sd, 0).astype(np.float32)
        self.sd = sd.astype(np.float32)
        self.var_raw = (sd ** 2).astype(np.float64)
        self.deg = A.sum(1)
        As = sparse.csr_matrix(A)
        num = (As @ z.T).T                                            # (T, N): sum of the valid neighbours' z values
        den = (As @ valid.T.astype(np.float32)).T
        zn = np.where(den > 0, num / np.maximum(den, 1), 0).astype(np.float32)
        self.A = As
        self.z, self.zn, self.valid = torch.from_numpy(z), torch.from_numpy(zn), torch.from_numpy(valid)
        t = np.arange(self.T, dtype=np.float64) / steps_per_day * 2 * np.pi
        tod = [np.ones(self.T)] + [f(k * t) for k in range(1, HARMONICS + 1) for f in (np.sin, np.cos)]
        self.tod = torch.from_numpy(np.stack(tod, 1).astype(np.float32))     # (T, 1 + 2 * HARMONICS), by row index
        self.zl = self.z.unfold(0, LAGS, 1)                                  # (T - 11, N, 12): row s = values s .. s + 11
        self.znl = self.zn.unfold(0, LAGS, 1)

    def _origins(self, lo: int, hi: int, h: int) -> torch.Tensor:
        """Forecast origins t with every input row in [lo, hi) and the target row t + h in [lo, hi)."""
        return torch.arange(lo + LAGS - 1, hi - h)

    def _features(self, t: torch.Tensor, cols: slice, h: int):
        s = t - (LAGS - 1)
        own = self.zl[s][:, cols]                                             # (R, B, 12)
        nb = self.znl[s][:, cols]
        tod = self.tod[t + h][:, None, :].expand(-1, own.shape[1], -1)
        F = torch.cat([own, tod, nb], 2).permute(1, 0, 2).contiguous()        # (B, R, 12 + 7 + 12): base = the first 19 columns
        y = self.z[t + h][:, cols].T.contiguous()                             # (B, R)
        w = self.valid[t + h][:, cols].T.float().contiguous()
        return F, y, w

    def fit_eval(self, fit: tuple[int, int], ev: tuple[int, int], chunk: int = 256) -> dict:
        """Per-sensor MAE (raw unit) of both models on the rows `ev`, and the residual score c1 of the base model there."""
        nb_ = LAGS + 1 + 2 * HARMONICS
        e = np.zeros((2, len(HORIZONS), self.N))
        c1 = np.zeros((len(HORIZONS), self.N))
        for hi_, h in enumerate(HORIZONS):
            tf, te = self._origins(*fit, h), self._origins(*ev, h)
            res = torch.zeros(len(te), self.N)
            val = torch.zeros(len(te), self.N, dtype=torch.bool)
            for c in range(0, self.N, chunk):
                cols = slice(c, min(c + chunk, self.N))
                F, y, w = self._features(tf, cols, h)
                Fw = F * w[..., None]
                G = Fw.transpose(1, 2).double() @ F.double()                  # (B, 31, 31)
                b = (Fw.transpose(1, 2).double() @ y.double()[..., None])     # (B, 31, 1)
                lam = RIDGE * w.sum(1).clamp_min(1.0).double()[:, None, None]
                eye = torch.eye(G.shape[1], dtype=torch.float64)
                beta_plus = torch.linalg.solve(G + lam * eye, b)
                beta_base = torch.linalg.solve(G[:, :nb_, :nb_] + lam * eye[:nb_, :nb_], b[:, :nb_])
                del F, Fw, G
                F, y, w = self._features(te, cols, h)
                sd = torch.from_numpy(self.sd[cols])[:, None]
                r_base = y - (F[..., :nb_].double() @ beta_base).squeeze(-1).float()
                r_plus = y - (F.double() @ beta_plus).squeeze(-1).float()
                n_ok = w.sum(1).clamp_min(1.0)
                e[0, hi_, cols] = ((r_base.abs() * sd * w).sum(1) / n_ok).numpy()
                e[1, hi_, cols] = ((r_plus.abs() * sd * w).sum(1) / n_ok).numpy()
                e[:, hi_, cols][:, (w.sum(1) == 0).numpy()] = np.nan
                res[:, cols] = r_base.T
                val[:, cols] = w.T.bool()
                del F
            c1[hi_] = self._c1(res, val)
        with np.errstate(all="ignore"), warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            return self._mean(e, c1)

    @staticmethod
    def _mean(e, c1) -> dict:
        return {"e": np.nanmean(e[0], 0), "e_plus": np.nanmean(e[1], 0), "c1": np.nanmean(c1, 0)}

    def _c1(self, res: torch.Tensor, val: torch.Tensor) -> np.ndarray:
        """Node score with lambda = 1: sum over the edges (i, j) and rows of sgn(r_i r_j), over the count of valid pairs."""
        r = res.clone()
        r[~val] = float("nan")
        med = torch.nanmedian(r, 0).values
        S = torch.sign(torch.nan_to_num(r - med, nan=0.0))
        S[~val] = 0
        V = val.float()
        rows, cols = self.A.nonzero()
        num, den = np.zeros(self.N), np.zeros(self.N)
        for s in range(0, len(rows), 4096):
            i, j = torch.from_numpy(rows[s:s + 4096]).long(), torch.from_numpy(cols[s:s + 4096]).long()
            np.add.at(num, rows[s:s + 4096], (S[:, i] * S[:, j]).sum(0).numpy())
            np.add.at(den, rows[s:s + 4096], (V[:, i] * V[:, j]).sum(0).numpy())
        return np.where(den > 0, num / np.maximum(den, 1), np.nan)


def run_dataset(name: str, out: Path, chunk: int) -> None:
    t0 = time.time()
    x, A, spd = load(name)
    task = Task(x, A, spd)
    half = task.n_train // 2
    main = task.fit_eval((0, task.n_train), (task.n_train, task.n_val_end), chunk)
    a = task.fit_eval((0, half), (half, task.n_train), chunk)                 # fit on the first half, read on the second
    b = task.fit_eval((half, task.n_train), (0, half), chunk)
    df = pd.DataFrame({
        "sensor": np.arange(task.N), "excluded": task.excluded.astype(int), "degree": task.deg.astype(int), "sd_raw": task.sd, "var_raw": task.var_raw,
        "e": main["e"], "e_plus": main["e_plus"], "d": main["e"] - main["e_plus"], "c1": main["c1"],
        "d_half_a": a["e"] - a["e_plus"], "d_half_b": b["e"] - b["e_plus"], "c1_half_a": a["c1"],
    })
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / f"linear_sensors_{name}.csv", index=False, float_format="%.6g")
    print(f"{name}: T={task.T} N={task.N} edges={int(A.sum() // 2)} isolated={int((task.deg == 0).sum())} "
          f"{time.time() - t0:.0f} s", flush=True)


def summarise(out: Path) -> pd.DataFrame:
    rows = []
    for f in sorted(out.glob("linear_sensors_*.csv")):
        name = f.stem[len("linear_sensors_"):]
        df = pd.read_csv(f)
        d, tot = df["d"].to_numpy(), float(np.nansum(df["d"]))
        top = _top_mask(d)
        top_a = _top_mask(df["d_half_a"].to_numpy())
        r = {"dataset": name, "n": len(df), "excluded": int(df["excluded"].sum()), "isolated": int((df["degree"] == 0).sum()),
             "mae_base": float(np.nanmean(df["e"])), "mae_plus": float(np.nanmean(df["e_plus"])),
             "g_s": float(np.nansum(df["e"]) / np.nansum(df["e_plus"])),
             "share_positive": float(np.nanmean(d > 0)), "c1_mean": float(np.nanmean(df["c1"])),
             "top25_share": float(np.nansum(d[top]) / tot) if tot > 0 else float("nan"),
             "top25_share_from_half_a": float(np.nansum(d[top_a]) / tot) if tot > 0 else float("nan"),
             "stability": _spearman(df["d_half_a"].to_numpy(), df["d_half_b"].to_numpy())}
        for key, col in (("c1", "c1"), ("c1_half_a", "c1_half_a"), ("degree", "degree"), ("variance", "var_raw")):
            v = df[col].to_numpy()
            r[f"rho_{key}"] = _spearman(v, d)
            r[f"overlap_{key}"] = float((_top_mask(v) & top).sum() / top.sum())
        r["line"] = ("no gain" if not tot > 0 else
                     "pass" if r["top25_share"] >= PASS_SHARE and r["stability"] >= PASS_STAB else
                     "fail" if r["top25_share"] < FAIL_SHARE or r["stability"] < FAIL_STAB else "between")
        rows.append(r)
    s = pd.DataFrame(rows)
    s.to_csv(out / "linear_summary.csv", index=False, float_format="%.4g")
    with open(out / "linear_summary.md", "w") as fh:
        fh.write("Linear stage of spatialgate: per-sensor gain d of a neighbour term over a per-sensor model (train -> validation, "
                 "horizons 3, 6, 12, raw unit).  top25_share = share of the summed d in the top 25 % of the sensors by d; "
                 "top25_share_from_half_a = the same sum for the top 25 % by the d of another period (first half of train -> "
                 "second half); stability = Spearman of d between the two half fits; rho and overlap = Spearman with d and the "
                 "share of the top 25 % by d that the top 25 % by the signal holds (uniform = 0.25).\n\n")
        fh.write(s.to_markdown(index=False, floatfmt=".3f") + "\n")
    return s


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="spatialgate: the linear stage")
    ap.add_argument("mode", choices=["linear", "summary"])
    ap.add_argument("--datasets", default="pems08")
    ap.add_argument("--out", default="results/spatialgate/compare/tables")
    ap.add_argument("--chunk", type=int, default=256, help="sensors per solve")
    ap.add_argument("--force", action="store_true", help="compute a dataset again when its file exists")
    args = ap.parse_args(argv)
    out = Path(args.out)
    if args.mode == "linear":
        for name in [d for d in args.datasets.split(",") if d]:
            if (out / f"linear_sensors_{name}.csv").exists() and not args.force:
                print(f"{name}: stored, skipped", flush=True)
                continue
            run_dataset(name, out, args.chunk)
    print(summarise(out).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
