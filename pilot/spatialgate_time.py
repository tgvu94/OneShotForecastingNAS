"""spatialgate, the choice per time window: does a set of (window, sensor) cells hold the gain of the full model over the base model?

    python -m pilot.spatialgate_time --set sd      # reads <root>/train_dump/{stid,full}/seed{0,1,2}/forecast_{val,test}.npy

A cell is one forecast window of one sensor (12 target steps).  A composite forecast takes the full model in the chosen cells and
the base model in all other cells, both of the same seed; its masked MAE in the raw unit is compared with the MAE of the full
model.  No model is trained here: the composite is what a gate at inference gives when it runs the spatial module for the chosen
cells only.  The cells are chosen at the shares 0.10, 0.25 and 0.50 of the cells with a valid target, by one of these scores:
  ora_same : the test gain of the cell, same seed (the ceiling; it reads the test error and its seed noise)
  ora_seed : the test gain of the cell, mean of the other two seeds (it reads the test error, without the noise of the seed)
  ora_time : whole windows, by the test gain of the window over all sensors, mean of the other two seeds
  sensor   : whole sensors, by the gain of the sensor on the validation split
  slot     : the gain on the validation split at the same sensor, slot of the day (96) and day type (work day, weekend)
  level    : the gain on the validation split at the same sensor and the same decile of its last input value
  resid    : the absolute error of the base model of the same seed in the last window with known targets (12 steps before)
  rnd      : random cells
Output: <root>/tables/time_cells.md and time_cells.csv.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from pilot.datasets import npz_path

BASE = Path("results/spatialgate")
SEEDS = (0, 1, 2)
SHARES = (0.10, 0.25, 0.50)
HORIZON = 12
SLOTS = 96


def cell_sums(root: Path, arch: str, seed: int, split: str, raw: np.ndarray):
    """(sum of the absolute error [W, N], valid targets [W, N], first target rows [W]) of one run."""
    d = root / "train_dump" / arch / f"seed{seed}"
    rec = json.load(open(d / "metrics.json"))["forecast_dump"][split]
    pred = np.load(d / f"forecast_{split}.npy", mmap_mode="r")
    rows = rec["first_target_row"] + np.arange(pred.shape[0])
    S = np.zeros((pred.shape[0], pred.shape[2]))
    C = np.zeros_like(S)
    for a in range(0, len(rows), 512):
        r = rows[a:a + 512]
        tgt = raw[r[:, None] + np.arange(HORIZON)[None]].astype(np.float64)      # [w, H, N]
        m = tgt != 0
        S[a:a + 512] = (np.abs(np.asarray(pred[a:a + 512], dtype=np.float64) - tgt) * m).sum(1)
        C[a:a + 512] = m.sum(1)
    mae = S.sum() / C.sum()
    assert abs(mae - rec["mae_raw"]) < 1e-3 * rec["mae_raw"], (arch, seed, split, mae, rec["mae_raw"])
    return S, C, rows


def top_cells(score: np.ndarray, valid: np.ndarray, share: float) -> np.ndarray:
    flat = np.where(valid, score, -np.inf).ravel()
    k = int(round(share * valid.sum()))
    z = np.zeros(flat.shape, dtype=bool)
    z[np.argsort(-flat, kind="stable")[:k]] = True
    return z.reshape(score.shape) & valid


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="spatialgate: the gain per (window, sensor) cell")
    ap.add_argument("--set", required=True, choices=["sd", "gla"])
    args = ap.parse_args(argv)
    ds = f"largest{args.set}"
    root = BASE / f"{ds}_h12"
    raw = np.load(npz_path(ds))["data"][:, :, 0]
    n_train = int(len(raw) * 0.6)
    mu, sd = raw[:n_train].mean(0), np.where(raw[:n_train].std(0) == 0, 1.0, raw[:n_train].std(0))

    S = {(a, s, sp): None for a in ("stid", "full") for s in SEEDS for sp in ("val", "test")}
    C, rows = {}, {}
    for a, s, sp in S:
        S[a, s, sp], C[sp], rows[sp] = cell_sums(root, a, s, sp, raw)
    gain = {(s, sp): S["stid", s, sp] - S["full", s, sp] for s in SEEDS for sp in ("val", "test")}     # summed error saved per cell
    valid = C["test"] > 0
    W, N = valid.shape
    per_step = lambda g, sp: g / np.maximum(C[sp], 1)                                                    # noqa: E731

    # scores fit on the validation split (mean of the seeds)
    gv = per_step(sum(gain[s, "val"] for s in SEEDS) / len(SEEDS), "val")
    cv = C["val"] > 0
    sensor_score = np.broadcast_to((gv * cv).sum(0) / np.maximum(cv.sum(0), 1), (W, N))
    slot_of = lambda r: (r % SLOTS) + SLOTS * ((((r // SLOTS) + 1) % 7) >= 5)                            # noqa: E731  (row 0 is a Tuesday)
    sv, st = slot_of(rows["val"]), slot_of(rows["test"])
    table = np.zeros((2 * SLOTS, N))
    for k in range(2 * SLOTS):
        pick = sv == k
        if pick.any():
            table[k] = (gv[pick] * cv[pick]).sum(0) / np.maximum(cv[pick].sum(0), 1)
    slot_score = table[st]
    zv, zt = (raw[rows["val"] - 1] - mu) / sd, (raw[rows["test"] - 1] - mu) / sd
    level_score = np.zeros((W, N))
    for i in range(N):
        edges = np.quantile(zv[:, i], np.linspace(0.1, 0.9, 9))
        bv, bt = np.searchsorted(edges, zv[:, i]), np.searchsorted(edges, zt[:, i])
        num = np.bincount(bv, weights=gv[:, i] * cv[:, i], minlength=10)
        den = np.bincount(bv, weights=cv[:, i].astype(float), minlength=10)
        level_score[:, i] = (num / np.maximum(den, 1))[bt]
    rng = np.random.default_rng(0)
    rnd_score = rng.random((W, N))

    rows_out = []
    total = C["test"].sum()
    for s in SEEDS:
        others = [t for t in SEEDS if t != s]
        g_same = per_step(gain[s, "test"], "test")
        g_seed = per_step(sum(gain[t, "test"] for t in others) / len(others), "test")
        g_time = np.broadcast_to((sum(gain[t, "test"] for t in others).sum(1) / np.maximum(C["test"].sum(1), 1))[:, None], (W, N))
        eb = per_step(S["stid", s, "test"], "test")
        resid = np.zeros((W, N))
        resid[HORIZON:] = eb[:-HORIZON]
        base, full = S["stid", s, "test"].sum() / total, S["full", s, "test"].sum() / total
        rows_out.append({"score": "base", "share": 0.0, "seed": s, "mae": base, "gain_kept": 0.0})
        rows_out.append({"score": "full", "share": 1.0, "seed": s, "mae": full, "gain_kept": 1.0})
        scores = {"ora_same": g_same, "ora_seed": g_seed, "ora_time": g_time, "sensor": sensor_score, "slot": slot_score,
                  "level": level_score, "resid": resid, "rnd": rnd_score}
        for name, sc in scores.items():
            for share in SHARES:
                z = top_cells(sc, valid, share)
                mae = (S["full", s, "test"][z].sum() + S["stid", s, "test"][~z].sum()) / total
                rows_out.append({"score": name, "share": share, "seed": s, "mae": mae, "gain_kept": (base - mae) / (base - full)})
    df = pd.DataFrame(rows_out)
    (root / "tables").mkdir(exist_ok=True)
    df.to_csv(root / "tables" / "time_cells.csv", index=False, float_format="%.6g")
    g = df.groupby(["score", "share"], sort=False).agg(mae=("mae", "mean"), sd=("mae", "std"), gain_kept=("gain_kept", "mean")).reset_index()
    full_mae, sigma = float(g.loc[g.score == "full", "mae"].iloc[0]), float(g.loc[g.score == "full", "sd"].iloc[0])
    g["above_full_in_sigma"] = (g["mae"] - full_mae) / sigma
    lines = ["| score | share of cells | test MAE | sd of 3 seeds | gain kept | above the full model, in sigma_seed |", "|---|---|---|---|---|---|"]
    lines += [f"| {r.score} | {r.share:.2f} | {r.mae:.3f} | {r.sd:.3f} | {r.gain_kept:.3f} | {r.above_full_in_sigma:.1f} |" for r in g.itertuples()]
    (root / "tables" / "time_cells.md").write_text(
        f"# {ds}: composite of the full model in the chosen (window, sensor) cells and the base model elsewhere\n\n"
        f"Test split, {W} windows, {N} sensors, {int(valid.sum())} cells with a valid target; sigma_seed of the full model {sigma:.3f}.\n\n"
        + "\n".join(lines) + "\n")
    print(g.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
