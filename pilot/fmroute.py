"""fmroute: a frozen foundation model against models trained at the city, per sensor and per regime.

The windows are those of the benchst protocol (h = 12, split 60/20/20 by rows, 96 rows of history before the first target of the
val and of the test split).  Every forecast file is float32 [windows, horizon, sensors] in the raw unit of channel 0 of the city
file, window i = entry i of ``split_rows``.  ``pilot.train_arch --dump-forecasts`` writes the files of the trained side;
``python -m pilot.fmroute chronos`` writes those of the frozen side (it runs in the second venv, which holds no pipeline package,
so this module imports numpy, torch and ``pilot.datasets`` only).

    python -m pilot.fmroute regimes --dataset pemsbay
    python -m pilot.fmroute chronos --dataset pems08 --split test --setting joint --out <dir> [--limit-windows 50]
    python -m pilot.fmroute score   --dataset pems08 --split test --forecast <file.npy> --out <cells.npz>
    python -m pilot.fmroute regimecheck --dataset pemsbay

A regime is a property of one sensor and one target window (the protocol of wang2026regime): free flow when every step of the
window is above the upper speed threshold, congested when every step is below the lower one, transition otherwise.  The label
comes from the speed channel of the city file, which is channel 0 but at the flow cities.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

from pilot.datasets import npz_path

HORIZON, WINDOW = 12, 96
MPH = 1.609344
# speed channel of the file, its unit, minutes per step.  The unit of chengdu and expytky is read from the value range; the
# files carry no unit.
CITY = {
    "metrla":  {"speed_channel": 0, "unit": "mph", "step_min": 5},
    "pemsbay": {"speed_channel": 0, "unit": "mph", "step_min": 5},
    "pems04":  {"speed_channel": 2, "unit": "mph", "step_min": 5},
    "pems08":  {"speed_channel": 2, "unit": "mph", "step_min": 5},
    "chengdu": {"speed_channel": 0, "unit": "km/h", "step_min": 10},
    "expytky": {"speed_channel": 0, "unit": "km/h", "step_min": 10},
}
REGIMES = ("free", "transition", "congested")
FREE_MPH, CONGESTED_MPH = 55.0, 25.0
# The relative rule, for a city where the thresholds of US freeways leave a regime empty: the free-flow speed of a sensor is the
# 85th percentile of its valid speeds on the training split; free flow is every step above FREE_REL of it, congested is every
# step below CONGESTED_REL of it (55 and 25 mph over a free-flow speed of 68 mph are 0.81 and 0.37).
RULES = ("absolute", "relative")
FREE_REL, CONGESTED_REL, FREE_FLOW_PERCENTILE = 0.8, 0.4, 85


def split_rows(n_rows: int, window: int, horizon: int, split: str) -> np.ndarray:
    """Row of the first target step of every window of a split, in the order of the split (pilot.data.get_dataset_and_loaders:
    entry m of the split has its last history row at m and its targets at m+1 .. m+horizon)."""
    n_train = int(n_rows * 0.6)
    n_val = int(n_rows * 0.8) - n_train
    n_test = n_rows - n_train - n_val
    if split == "val":
        m = np.arange(n_train + window - 1, n_train + n_val - horizon)
    elif split == "test":
        m = np.arange(n_rows - n_test + window - 1, n_rows - horizon)
    else:
        raise ValueError(f"split {split!r}: val or test")
    return m + 1


def load_raw(dataset: str) -> np.ndarray:
    """[rows, sensors, channels] of the city file."""
    return np.load(npz_path(dataset), allow_pickle=True)["data"]


def window_view(series: np.ndarray, rows: np.ndarray, horizon: int = HORIZON) -> np.ndarray:
    """series [rows, sensors] -> [windows, horizon, sensors] at the given first target rows."""
    return series[rows[:, None] + np.arange(horizon)[None, :]]


def targets(dataset: str, split: str, raw: np.ndarray | None = None):
    """(y [windows, horizon, sensors] of channel 0, valid mask of the same shape, first target rows).  A raw 0 or NaN is a
    missing value (the zero mask of the benchst protocol)."""
    raw = load_raw(dataset) if raw is None else raw
    rows = split_rows(len(raw), WINDOW, HORIZON, split)
    y = window_view(raw[:, :, 0], rows).astype(np.float32)
    return y, np.isfinite(y) & (y != 0), rows


def free_flow_speed(dataset: str, raw: np.ndarray | None = None) -> np.ndarray:
    """[sensors]: the 85th percentile of the valid speeds of the training split (the first 60 % of the rows)."""
    raw = load_raw(dataset) if raw is None else raw
    v = raw[:int(len(raw) * 0.6), :, CITY[dataset]["speed_channel"]].astype(np.float64)
    v[~np.isfinite(v) | (v == 0)] = np.nan
    return np.nanpercentile(v, FREE_FLOW_PERCENTILE, axis=0)


def regime_labels(dataset: str, split: str, raw: np.ndarray | None = None, rule: str = "absolute") -> np.ndarray:
    """int8 [windows, sensors]: 0 free flow, 1 transition, 2 congested, -1 when a speed of the target window is missing.
    ``rule``: absolute (55 and 25 mph) or relative (shares of the free-flow speed of the sensor)."""
    raw = load_raw(dataset) if raw is None else raw
    spec = CITY[dataset]
    rows = split_rows(len(raw), WINDOW, HORIZON, split)
    v = window_view(raw[:, :, spec["speed_channel"]], rows)
    ok = (np.isfinite(v) & (v != 0)).all(1)
    if rule == "absolute":
        k = MPH if spec["unit"] == "km/h" else 1.0
        hi, lo = FREE_MPH * k, CONGESTED_MPH * k
    elif rule == "relative":
        vf = free_flow_speed(dataset, raw)[None, None, :]
        hi, lo = FREE_REL * vf, CONGESTED_REL * vf
    else:
        raise ValueError(f"rule {rule!r}: one of {RULES}")
    with np.errstate(invalid="ignore"):
        free, cong = (v > hi).all(1), (v < lo).all(1)
    lab = np.full(ok.shape, 1, dtype=np.int8)
    lab[free], lab[cong] = 0, 2
    lab[~ok] = -1
    return lab


def cell_sums(forecast: np.ndarray, y: np.ndarray, valid: np.ndarray, lab: np.ndarray):
    """Sum of the absolute error and count of valid targets per sensor, regime and step: two arrays [sensors, 3, horizon].
    The one scorer of both sides."""
    if forecast.shape != y.shape:
        raise ValueError(f"forecast {forecast.shape} and targets {y.shape} differ")
    err = np.where(valid, np.abs(forecast.astype(np.float64) - y), 0.0)
    n_sensors, h = y.shape[2], y.shape[1]
    sums, counts = np.zeros((n_sensors, 3, h)), np.zeros((n_sensors, 3, h))
    for r in range(3):
        sel = (lab == r)[:, None, :]                      # [windows, 1, sensors]
        sums[:, r] = (err * sel).sum(0).T
        counts[:, r] = (valid & sel).sum(0).T
    return sums, counts


def cmd_regimes(args) -> int:
    raw = load_raw(args.dataset)
    for split in ("val", "test"):
        for rule in RULES:
            lab = regime_labels(args.dataset, split, raw, rule)
            n = (lab >= 0).sum()
            share = {REGIMES[r]: round(float((lab == r).sum() / max(n, 1)), 4) for r in range(3)}
            print(json.dumps({"dataset": args.dataset, "split": split, "rule": rule, "windows": int(lab.shape[0]),
                              "sensors": int(lab.shape[1]), "labelled_share": round(float(n / lab.size), 4), **share}))
    return 0


def cmd_score(args) -> int:
    raw = load_raw(args.dataset)
    y, valid, rows = targets(args.dataset, args.split, raw)
    f = np.asarray(np.load(args.forecast, mmap_mode="r"))
    save = {"regimes": np.array(REGIMES), "first_target_row": rows[0]}
    for rule in RULES:                                    # one file holds the cells of both regime rules
        sums, counts = cell_sums(f, y, valid, regime_labels(args.dataset, args.split, raw, rule))
        save[f"sums_{rule}"], save[f"counts_{rule}"] = sums, counts
        tot = sums.sum((0, 2)) / np.maximum(counts.sum((0, 2)), 1)
        print(json.dumps({"dataset": args.dataset, "split": args.split, "rule": rule, "forecast": str(args.forecast),
                          "mae_labelled": float(sums.sum() / max(counts.sum(), 1)),
                          **{f"mae_{REGIMES[r]}": float(tot[r]) for r in range(3)},
                          **{f"share_{REGIMES[r]}": float(counts[:, r].sum() / max(counts.sum(), 1)) for r in range(3)}}))
    err = np.where(valid, np.abs(f.astype(np.float64) - y), 0.0)   # every valid target, also where the speed gives no label
    save["sums_all"], save["counts_all"] = err.sum(0).T, valid.sum(0).T
    print(json.dumps({"dataset": args.dataset, "split": args.split, "mae": float(err.sum() / max(valid.sum(), 1))}))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out, **save)
    return 0


def cmd_chronos(args) -> int:
    """The frozen side: Chronos-2, zero-shot.  The context of a window is the week before its first target row (rule 4 of the
    plan), a missing value (raw 0) is NaN in the context.  ``joint``: one item per window with every sensor of the city as a
    variate, so the model attends across the sensors.  ``alone``: one item per sensor and window.  The point forecast is the
    median.  Resumable: one part file per chunk of windows; the parts are joined when all exist."""
    import torch
    from chronos import Chronos2Pipeline

    raw = load_raw(args.dataset)
    series = raw[:, :, 0].astype(np.float32)
    series[~np.isfinite(series) | (series == 0)] = np.nan
    rows = split_rows(len(raw), WINDOW, HORIZON, args.split)
    if args.limit_windows:
        rows = rows[np.unique(np.linspace(0, len(rows) - 1, args.limit_windows).astype(int))]
    ctx = args.context_steps or 7 * 24 * 60 // CITY[args.dataset]["step_min"]
    n_sensors = series.shape[1]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    pipe = Chronos2Pipeline.from_pretrained(args.model, device_map=args.device)
    levels = [0.05, 0.1, 0.5, 0.9, 0.95]
    chunk = args.chunk or (max(1, 2048 // n_sensors) if args.setting == "joint" else max(1, 4096 // n_sensors))
    t0, done, parts = time.time(), 0, []
    if args.device.startswith("cuda"):
        torch.cuda.reset_peak_memory_stats()
    for a in range(0, len(rows), chunk):
        b = min(a + chunk, len(rows))
        part = out / f"part_{args.split}_{a:06d}_{b:06d}.npy"
        parts.append(part)
        if part.exists():
            continue
        x = np.stack([series[max(r - ctx, 0):r].T for r in rows[a:b]])              # [windows, sensors, context]
        if args.setting == "joint":
            inputs, bs = x, args.batch_size or n_sensors * 1
        else:
            inputs, bs = x.reshape(-1, 1, x.shape[-1]), args.batch_size or 256
        q, _ = pipe.predict_quantiles(inputs, prediction_length=HORIZON, quantile_levels=levels, batch_size=bs)
        q = torch.stack([t.float().cpu() for t in q]).numpy()                        # [items, variates, horizon, levels]
        q = q.reshape(b - a, n_sensors, HORIZON, len(levels)).transpose(0, 2, 1, 3)  # [windows, horizon, sensors, levels]
        tmp = part.with_suffix(".tmp.npy")
        np.save(tmp, q.astype(np.float32))
        tmp.replace(part)
        done += b - a
        print(f"{args.split} windows {a}:{b} of {len(rows)}; {(time.time() - t0) / done:.3f} s per window", flush=True)
    q = np.concatenate([np.load(p) for p in parts])
    info = {"dataset": args.dataset, "split": args.split, "setting": args.setting, "model": args.model, "context_steps": int(ctx),
            "windows": int(len(rows)), "sensors": int(n_sensors), "quantile_levels": levels, "chunk": int(chunk),
            "seconds_this_call": round(time.time() - t0, 1), "windows_this_call": int(done),
            "peak_mem_gb": round(torch.cuda.max_memory_allocated() / 1e9, 3) if args.device.startswith("cuda") else None,
            "limit_windows": args.limit_windows, "first_target_rows": [int(rows[0]), int(rows[-1])], "torch": torch.__version__}
    if not args.limit_windows:
        np.save(out / f"forecast_{args.split}.npy", q[..., levels.index(0.5)])
        np.save(out / f"quantiles_{args.split}.npy", q[..., [0, 1, 3, 4]].astype(np.float16))
        for p in parts:
            p.unlink()
    else:   # a timing run: the error of the sample, for a first look only
        y = window_view(raw[:, :, 0], rows).astype(np.float32)
        valid = np.isfinite(y) & (y != 0)
        info["mae_sample"] = float(np.abs(q[..., 2] - y)[valid].mean())
    (out / f"chronos_{args.split}.json").write_text(json.dumps(info, indent=2))
    print(json.dumps(info))
    return 0


def cmd_regimecheck(args) -> int:
    """The published regime table again, as a check of the regime code: Chronos-Bolt-Small under the protocol of wang2026regime
    (split 70/10/20; the 50 sensors with the highest share of training readings below 25 mph; per seed 42, 43, 44 a draw of 30 of
    them and of 50 test windows; 14 hours of context; h = 12; MAE and coverage of the 90 % interval per regime).  The paper does
    not state how it draws the windows: here they are 50 rows of the test split, uniform without replacement, the same for the
    30 sensors.  A missing value (raw 0) is NaN in the context and no target."""
    import torch
    from chronos import ChronosBoltPipeline

    spec = CITY[args.dataset]
    k = MPH if spec["unit"] == "km/h" else 1.0
    v = load_raw(args.dataset)[:, :, spec["speed_channel"]].astype(np.float32)
    v[~np.isfinite(v) | (v == 0)] = np.nan
    n_train, n_test0 = int(len(v) * 0.7), int(len(v) * 0.8)
    with np.errstate(invalid="ignore"):
        freq = np.nanmean(np.where(np.isfinite(v[:n_train]), v[:n_train] < CONGESTED_MPH * k, np.nan), axis=0)
    pool = np.argsort(-freq)[:50]
    ctx = args.context_steps or 14 * 60 // spec["step_min"]
    pipe = ChronosBoltPipeline.from_pretrained(args.model, device_map=args.device)
    per_seed = []
    for seed in (42, 43, 44):
        rng = np.random.default_rng(seed)
        sensors = np.sort(rng.choice(pool, 30, replace=False))
        rows = np.sort(rng.choice(np.arange(n_test0 + ctx, len(v) - HORIZON), 50, replace=False))
        x = np.stack([v[r - ctx:r, i] for r in rows for i in sensors])
        y = np.stack([v[r:r + HORIZON, i] for r in rows for i in sensors])
        q, _ = pipe.predict_quantiles(torch.from_numpy(x), prediction_length=HORIZON, quantile_levels=[0.05, 0.5, 0.95])
        q = q.float().cpu().numpy() / 1.0
        ok = np.isfinite(y).all(1)
        free, cong = (y > FREE_MPH * k).all(1), (y < CONGESTED_MPH * k).all(1)
        lab = np.where(free, 0, np.where(cong, 2, 1))
        rec = {"seed": seed, "pairs": int(ok.sum())}
        for r, name in list(enumerate(REGIMES)) + [(None, "overall")]:
            sel = ok & ((lab == r) if r is not None else True)
            rec[f"n_{name}"] = int(sel.sum())
            # the unit of the paper is mph
            rec[f"mae_{name}"] = float(np.abs(q[sel, :, 1] - y[sel]).mean() / k) if sel.any() else None
            rec[f"cov90_{name}"] = float(((y[sel] >= q[sel, :, 0]) & (y[sel] <= q[sel, :, 2])).mean()) if sel.any() else None
            # the last step only (h = 12), the form of a per-horizon table
            rec[f"mae_h12_{name}"] = float(np.abs(q[sel, -1, 1] - y[sel, -1]).mean() / k) if sel.any() else None
            rec[f"cov90_h12_{name}"] = float(((y[sel, -1] >= q[sel, -1, 0]) & (y[sel, -1] <= q[sel, -1, 2])).mean()) if sel.any() else None
        per_seed.append(rec)
        print(json.dumps(rec))
    keys = [key for key in per_seed[0] if key != "seed"]
    summ = {key: [round(float(np.mean([r[key] for r in per_seed if r[key] is not None])), 4),
                  round(float(np.std([r[key] for r in per_seed if r[key] is not None])), 4)] for key in keys}
    print(json.dumps({"dataset": args.dataset, "model": args.model, "context_steps": int(ctx), "mean_and_std_over_seeds": summ}))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("regimes"); p.add_argument("--dataset", required=True)
    p = sub.add_parser("score")
    p.add_argument("--dataset", required=True); p.add_argument("--split", default="test"); p.add_argument("--forecast", required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("chronos")
    p.add_argument("--dataset", required=True); p.add_argument("--split", default="test")
    p.add_argument("--setting", choices=("joint", "alone"), required=True); p.add_argument("--out", required=True)
    p.add_argument("--model", default="amazon/chronos-2"); p.add_argument("--device", default="cuda")
    p.add_argument("--context-steps", type=int, default=None, help="default: one week of the city clock")
    p.add_argument("--chunk", type=int, default=None, help="windows per part file"); p.add_argument("--batch-size", type=int, default=None)
    p.add_argument("--limit-windows", type=int, default=None, help="a timing run on this many windows, spread over the split")
    p = sub.add_parser("regimecheck")
    p.add_argument("--dataset", required=True); p.add_argument("--model", default="amazon/chronos-bolt-small")
    p.add_argument("--device", default="cuda"); p.add_argument("--context-steps", type=int, default=None, help="default: 14 hours")
    args = ap.parse_args(argv)
    return {"regimes": cmd_regimes, "score": cmd_score, "chronos": cmd_chronos, "regimecheck": cmd_regimecheck}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
