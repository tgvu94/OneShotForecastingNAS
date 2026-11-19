"""spatialgate, a learned gate over (window, sensor) cells, read as a composite (no forecast model is trained here).

    python -m pilot.spatialgate_gate --set sd      # reads <root>/train_dump/{stid,full}/seed{0,1,2}/forecast_{val,test}.npy

One gate per seed: a gradient-boosted regression of the gain of a cell (error of the base model minus error of the full model,
per target step, raw unit) on features that are known at the forecast origin without a call of the spatial module.  The first
half of the validation windows gives the two lookup features, the second half fits the gate, the test split reads it.  The
composite takes the full model in the cells with the highest predicted gain and the base model elsewhere (pilot.spatialgate_time).
  gate      : cells by the predicted gain
  gate_time : whole windows by the mean predicted gain over the sensors
  rnd       : random cells
Output: <root>/tables/gate_cells.md and gate_cells.csv.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from pilot.datasets import npz_path
from pilot.spatialgate_time import BASE, HORIZON, SEEDS, SHARES, SLOTS, top_cells

FEATURES = ["slot", "dow", "weekend", "last", "d1", "d3", "d11", "std12", "nb_minus_own", "nb_d3", "base_change", "base_slope",
            "resid", "mu", "sd", "lookup_sensor", "lookup_slot"]


def run_cells(root: Path, arch: str, seed: int, split: str, raw: np.ndarray):
    """(sum of the absolute error [W, N], valid targets [W, N], first target rows [W], forecast mean [W, N], forecast last-first [W, N])."""
    d = root / "train_dump" / arch / f"seed{seed}"
    rec = json.load(open(d / "metrics.json"))["forecast_dump"][split]
    pred = np.load(d / f"forecast_{split}.npy", mmap_mode="r")
    rows = rec["first_target_row"] + np.arange(pred.shape[0])
    S, C, pm, ps = (np.zeros((pred.shape[0], pred.shape[2])) for _ in range(4))
    for a in range(0, len(rows), 512):
        r = rows[a:a + 512]
        p = np.asarray(pred[a:a + 512], dtype=np.float64)
        tgt = raw[r[:, None] + np.arange(HORIZON)[None]].astype(np.float64)
        m = tgt != 0
        S[a:a + 512], C[a:a + 512] = (np.abs(p - tgt) * m).sum(1), m.sum(1)
        pm[a:a + 512], ps[a:a + 512] = p.mean(1), p[:, -1] - p[:, 0]
    assert abs(S.sum() / C.sum() - rec["mae_raw"]) < 1e-3 * rec["mae_raw"]
    return S, C, rows, pm, ps


def main(argv=None) -> int:
    from sklearn.ensemble import HistGradientBoostingRegressor

    ap = argparse.ArgumentParser(description="spatialgate: a learned gate over cells")
    ap.add_argument("--set", required=True, choices=["sd", "gla"])
    args = ap.parse_args(argv)
    ds = f"largest{args.set}"
    root = BASE / f"{ds}_h12"
    raw = np.load(npz_path(ds))["data"][:, :, 0].astype(np.float64)
    n_train = int(len(raw) * 0.6)
    mu, sd = raw[:n_train].mean(0), np.where(raw[:n_train].std(0) == 0, 1.0, raw[:n_train].std(0))
    z = np.where(raw == 0, np.nan, (raw - mu) / sd)                       # a missing reading is NaN in the features
    senders = np.load(root / "data" / f"{ds}_senders.npy")
    num, den = np.zeros_like(z), np.zeros_like(z)
    for k in range(senders.shape[1]):
        col = z[:, np.maximum(senders[:, k], 0)]
        ok = np.isfinite(col) & (senders[:, k] >= 0)[None]
        num += np.where(ok, col, 0)
        den += ok
    zn = np.where(den > 0, num / np.maximum(den, 1), np.nan)
    N = raw.shape[1]

    def features(rows, base_mean, base_slope, base_err, lookup_sensor, lookup_slot):
        W = len(rows)
        h = z[rows[:, None] - 1 - np.arange(HORIZON)[None]]              # [W, 12, N], newest first
        last = h[:, 0]
        slot = rows % SLOTS
        dow = ((rows // SLOTS) + 1) % 7                                   # row 0 is a Tuesday
        resid = np.full((W, N), np.nan)
        resid[HORIZON:] = base_err[:-HORIZON]
        cols = [np.broadcast_to(slot[:, None], (W, N)), np.broadcast_to(dow[:, None], (W, N)), np.broadcast_to((dow >= 5)[:, None], (W, N)),
                last, last - h[:, 1], last - h[:, 3], last - h[:, 11], np.nanstd(h, axis=1),
                zn[rows - 1] - last, zn[rows - 1] - zn[rows - 4],
                (base_mean - raw[rows - 1]) / sd, base_slope / sd, resid / sd,
                np.broadcast_to(mu, (W, N)), np.broadcast_to(sd, (W, N)), np.broadcast_to(lookup_sensor, (W, N)),
                lookup_slot[slot + SLOTS * (dow >= 5)]]
        return np.stack([np.asarray(c, dtype=np.float32).ravel() for c in cols], axis=1)

    rows_out = []
    rng = np.random.default_rng(0)
    for s in SEEDS:
        Sb_v, C_v, rows_v, pm_v, ps_v = run_cells(root, "stid", s, "val", raw)
        Sf_v = run_cells(root, "full", s, "val", raw)[0]
        Sb_t, C_t, rows_t, pm_t, ps_t = run_cells(root, "stid", s, "test", raw)
        Sf_t = run_cells(root, "full", s, "test", raw)[0]
        g_v = (Sb_v - Sf_v) / np.maximum(C_v, 1)
        half = len(rows_v) // 2
        a, cv = g_v[:half], C_v[:half] > 0
        lookup_sensor = (a * cv).sum(0) / np.maximum(cv.sum(0), 1)
        key = (rows_v[:half] % SLOTS) + SLOTS * ((((rows_v[:half] // SLOTS) + 1) % 7) >= 5)
        lookup_slot = np.zeros((2 * SLOTS, N))
        for k in range(2 * SLOTS):
            pick = key == k
            if pick.any():
                lookup_slot[k] = (a[pick] * cv[pick]).sum(0) / np.maximum(cv[pick].sum(0), 1)
        err_v, err_t = Sb_v / np.maximum(C_v, 1), Sb_t / np.maximum(C_t, 1)
        Xv = features(rows_v, pm_v, ps_v, err_v, lookup_sensor, lookup_slot).reshape(len(rows_v), N, -1)[half:]
        fit = (C_v[half:] > 0).ravel()
        gate = HistGradientBoostingRegressor(max_iter=200, random_state=s)
        gate.fit(Xv.reshape(-1, Xv.shape[-1])[fit], g_v[half:].ravel()[fit])
        Xt = features(rows_t, pm_t, ps_t, err_t, lookup_sensor, lookup_slot)
        W = len(rows_t)
        pred = gate.predict(Xt).reshape(W, N)
        valid = C_t > 0
        total = C_t.sum()
        base, full = Sb_t.sum() / total, Sf_t.sum() / total
        g_t = (Sb_t - Sf_t) / np.maximum(C_t, 1)
        corr = float(np.corrcoef(pred[valid], g_t[valid])[0, 1])
        rows_out.append({"score": "base", "share": 0.0, "seed": s, "mae": base, "gain_kept": 0.0, "corr": np.nan})
        rows_out.append({"score": "full", "share": 1.0, "seed": s, "mae": full, "gain_kept": 1.0, "corr": np.nan})
        scores = {"gate": pred, "gate_time": np.broadcast_to(((pred * valid).sum(1) / np.maximum(valid.sum(1), 1))[:, None], (W, N)),
                  "rnd": rng.random((W, N))}
        for name, sc in scores.items():
            for share in SHARES:
                zc = top_cells(sc, valid, share)
                mae = (Sf_t[zc].sum() + Sb_t[~zc].sum()) / total
                rows_out.append({"score": name, "share": share, "seed": s, "mae": mae, "gain_kept": (base - mae) / (base - full),
                                 "corr": corr if name == "gate" else np.nan})
        # the gate decides alone: every cell with a positive predicted gain
        zc = (pred > 0) & valid
        mae = (Sf_t[zc].sum() + Sb_t[~zc].sum()) / total
        rows_out.append({"score": "gate_positive", "share": float(zc.sum() / valid.sum()), "seed": s, "mae": mae,
                         "gain_kept": (base - mae) / (base - full), "corr": np.nan})
        print(f"seed {s}: correlation of the predicted gain with the test gain {corr:.3f}; positive share {zc.sum() / valid.sum():.3f}, mae {mae:.4f}", flush=True)
    df = pd.DataFrame(rows_out)
    df.loc[df.score == "gate_positive", "share_measured"] = df.loc[df.score == "gate_positive", "share"]
    df.loc[df.score == "gate_positive", "share"] = -1.0
    (root / "tables").mkdir(exist_ok=True)
    df.to_csv(root / "tables" / "gate_cells.csv", index=False, float_format="%.6g")
    g = df.groupby(["score", "share"], sort=False).agg(mae=("mae", "mean"), sd=("mae", "std"), gain_kept=("gain_kept", "mean"),
                                                       share_measured=("share_measured", "mean")).reset_index()
    g.loc[g.score == "gate_positive", "share"] = g.loc[g.score == "gate_positive", "share_measured"]
    full_mae, sigma = float(g.loc[g.score == "full", "mae"].iloc[0]), float(g.loc[g.score == "full", "sd"].iloc[0])
    g["above_full_in_sigma"] = (g["mae"] - full_mae) / sigma
    lines = ["| score | share of cells | test MAE | sd of 3 seeds | gain kept | above the full model, in sigma_seed |", "|---|---|---|---|---|---|"]
    lines += [f"| {r.score} | {r.share:.2f} | {r.mae:.3f} | {r.sd:.3f} | {r.gain_kept:.3f} | {r.above_full_in_sigma:.1f} |" for r in g.itertuples()]
    (root / "tables" / "gate_cells.md").write_text(
        f"# {ds}: composite with a learned gate over (window, sensor) cells\n\nTest split; the gate is fit on the second half of the "
        f"validation windows, one gate per seed; sigma_seed of the full model {sigma:.3f}.  gate_positive: every cell with a positive "
        f"predicted gain, its share is measured.\n\n" + "\n".join(lines) + "\n")
    print(g.drop(columns="share_measured").to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
