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
    python -m pilot.fmroute cells    --root results/fmroute/pems08_h12 --dataset pems08
    python -m pilot.fmroute measures --roots results/fmroute/*_h12 --out results/fmroute/compare

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


# The rule that a line of the plan reads at each city (rule 1 of the plan); every city is scored under both.
LINE_RULE = {"metrla": "absolute", "pemsbay": "absolute", "pems08": "absolute", "pems04": "absolute",
             "chengdu": "relative", "expytky": "relative"}
SCOPES = REGIMES + ("labelled",)        # labelled: the three regimes together, every target whose window has a regime label
MIN_TARGETS = 120                       # a sensor-regime cell enters the spread of the ratio with 10 windows or more


def cmd_cells(args) -> int:
    """Scores every forecast file of a root with the one scorer: ``frozen/<setting>/forecast_<split>.npy`` and
    ``train/<model>/seed<k>/forecast_<split>.npy``, and on the test split the simple mean of each frozen and each trained
    forecast.  One file ``cells/<split>/<name>.npz`` per forecast; a file that exists is kept."""
    root = Path(args.root)
    raw = load_raw(args.dataset)
    frozen = sorted(d for d in (root / "frozen").glob("*") if d.is_dir())
    trained = sorted(d for d in (root / "train").glob("*/seed*") if d.is_dir())
    if not frozen or not trained:
        raise SystemExit(f"{root}: {len(frozen)} frozen and {len(trained)} trained folders; both sides are needed")
    for split in ("val", "test"):
        y, valid, rows = targets(args.dataset, split, raw)
        labs = {rule: regime_labels(args.dataset, split, raw, rule) for rule in RULES}

        def write(name, f):
            out = root / "cells" / split / f"{name}.npz"
            if out.exists():
                return
            save = {"regimes": np.array(REGIMES), "first_target_row": rows[0]}
            for rule in RULES:
                save[f"sums_{rule}"], save[f"counts_{rule}"] = cell_sums(f, y, valid, labs[rule])
            err = np.where(valid, np.abs(f.astype(np.float64) - y), 0.0)
            save["sums_all"], save["counts_all"] = err.sum(0).T, valid.sum(0).T
            out.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(out, **save)
            print(json.dumps({"split": split, "name": name, "mae": float(err.sum() / max(valid.sum(), 1))}), flush=True)

        fz = {d.name: np.load(d / f"forecast_{split}.npy") for d in frozen}
        for name, f in fz.items():
            write(name, f)
        for d in trained:
            name = f"{d.parent.name}_{d.name}"
            f = np.load(d / f"forecast_{split}.npy")
            write(name, f)
            if split == "test":
                for k, g in fz.items():
                    write(f"mean_{k}_{name}", (f + g) / 2)
    return 0


def _cells(root: Path, split: str, name: str, rule: str):
    """(sums, counts) [sensors, 4]: the three regimes and their total, summed over the steps."""
    z = np.load(root / "cells" / split / f"{name}.npz")
    s, c = z[f"sums_{rule}"].sum(-1), z[f"counts_{rule}"].sum(-1)
    return np.concatenate([s, s.sum(1, keepdims=True)], 1), np.concatenate([c, c.sum(1, keepdims=True)], 1)


def _mae(s, c):
    """MAE per scope over the sensors; NaN for a scope with no target."""
    c = c.sum(0)
    return np.where(c > 0, s.sum(0) / np.maximum(c, 1), np.nan)


def city_measures(root: Path, dataset: str, rule: str) -> dict:
    """The measures of the plan at one city under one regime rule.  The frozen side has one forecast per setting; the trained
    side has one per seed, and a quantity of the trained side, of the selector and of the mean is the mean over the seeds.
    sigma_seed of a scope is the standard deviation (ddof = 1) of the test MAE of the trained model of the pair in that scope.

    Choices that no test label enters: the frozen setting and the trained model of the main pair have the lowest MAE on the
    validation split.  The lookup selector uses, in a sensor-regime cell, the model with the lower validation MAE of the cell;
    a cell with no validation target takes the model with the lower validation MAE of the city.
    The better single model of the city has the lower test MAE over the labelled targets (this choice reads test labels and is
    in favour of the single model)."""
    settings = sorted(d.name for d in (root / "frozen").glob("*") if d.is_dir())
    models = sorted(d.name for d in (root / "train").glob("*") if d.is_dir())
    seeds = {m: sorted(d.name for d in (root / "train" / m).glob("seed*")) for m in models}
    F = {k: {sp: _cells(root, sp, k, rule) for sp in ("val", "test")} for k in settings}
    T = {m: {sd: {sp: _cells(root, sp, f"{m}_{sd}", rule) for sp in ("val", "test")} for sd in seeds[m]} for m in models}
    counts = F[settings[0]]["test"][1]
    out = {"dataset": dataset, "rule": rule, "sensors": int(counts.shape[0]),
           "share_of_targets": dict(zip(REGIMES, (counts[:, :3].sum(0) / max(counts[:, 3].sum(), 1)).tolist())),
           "models": {}, "pairs": {}}
    for k in settings:
        out["models"][k] = {"side": "frozen", "val_mae": dict(zip(SCOPES, _mae(*F[k]["val"]).tolist())),
                            "test_mae": dict(zip(SCOPES, _mae(*F[k]["test"]).tolist()))}
    for m in models:
        te = np.array([_mae(*T[m][sd]["test"]) for sd in seeds[m]])
        va = np.array([_mae(*T[m][sd]["val"]) for sd in seeds[m]])
        out["models"][m] = {"side": "trained", "seeds": len(seeds[m]), "val_mae": dict(zip(SCOPES, va.mean(0).tolist())),
                            "test_mae": dict(zip(SCOPES, te.mean(0).tolist())),
                            "sigma_seed": dict(zip(SCOPES, te.std(0, ddof=1).tolist()))}
    lab = SCOPES.index("labelled")
    main = (min(settings, key=lambda k: out["models"][k]["val_mae"]["labelled"]),
            min(models, key=lambda m: out["models"][m]["val_mae"]["labelled"]))
    out["main_pair"] = list(main)
    for k in settings:
        for m in models:
            fs, c = F[k]["test"]
            fvs, cv = F[k]["val"]
            f_city = out["models"][k]["val_mae"]["labelled"]
            per = {q: [] for q in ("selector", "oracle", "mean", "agree_cells", "agree_targets", "frozen_cells", "frozen_targets")}
            ts_mean = np.zeros_like(fs)
            for sd in seeds[m]:
                ts, _ = T[m][sd]["test"]
                tvs, _ = T[m][sd]["val"]
                ts_mean += ts / len(seeds[m])
                has_val, has_test = cv[:, :3] > 0, c[:, :3] > 0
                with np.errstate(invalid="ignore", divide="ignore"):
                    pick_f = np.where(has_val, fvs[:, :3] / cv[:, :3] < tvs[:, :3] / cv[:, :3],
                                      f_city < float(_mae(tvs, cv)[lab]))
                sel = np.where(pick_f, fs[:, :3], ts[:, :3])
                orc = np.minimum(fs[:, :3], ts[:, :3])
                tot = lambda a: np.concatenate([a, a.sum(1, keepdims=True)], 1)
                per["selector"].append(_mae(tot(sel), c))
                per["oracle"].append(_mae(tot(orc), c))
                per["mean"].append(_mae(*_cells(root, "test", f"mean_{k}_{m}_{sd}", rule)))
                both = has_val & has_test
                same = pick_f == (fs[:, :3] < ts[:, :3])
                per["agree_cells"].append(float(same[both].mean()))
                per["agree_targets"].append(float((same * c[:, :3])[both].sum() / c[:, :3][both].sum()))
                per["frozen_cells"].append(float(pick_f[has_test].mean()))
                per["frozen_targets"].append(float((pick_f * c[:, :3]).sum() / c[:, :3].sum()))
            mf, mt = np.array(_mae(fs, c)), np.array([out["models"][m]["test_mae"][sc] for sc in SCOPES])
            sig = np.array([out["models"][m]["sigma_seed"][sc] for sc in SCOPES])
            single_is_frozen = bool(mf[lab] < mt[lab])
            single = mf if single_is_frozen else mt
            selm, mixm = np.mean(per["selector"], 0), np.mean(per["mean"], 0)
            gain = single - selm                                    # above 0: the selector is below the better single model
            with np.errstate(invalid="ignore", divide="ignore"):
                ratio = np.where((c >= MIN_TARGETS) & (ts_mean > 0), fs / ts_mean, np.nan)   # the counts cancel
            spread = {}
            for i, sc in enumerate(SCOPES):
                r = ratio[np.isfinite(ratio[:, i]), i]
                spread[sc] = ({"sensors": int(len(r)), "share_below_1": float((r < 1).mean()),
                               **{f"p{q}": float(np.percentile(r, q)) for q in (10, 25, 50, 75, 90)}} if len(r) else {"sensors": 0})
            live = [i for i in range(3) if np.isfinite(mf[i])]
            passes = [bool(gain[i] > 2 * sig[i] and selm[i] < mixm[i]) for i in (lab, SCOPES.index("transition"))]
            rec = {"better_single": k if single_is_frozen else m,
                   "frozen_wins_regime": {SCOPES[i]: bool(mf[i] < mt[i]) for i in live},
                   "one_model_wins_every_regime": len({bool(mf[i] < mt[i]) for i in live}) == 1,
                   "selector_within_2_sigma_every_regime": all(bool(gain[i] <= 2 * sig[i]) for i in live),
                   "selector_passes": {"labelled": passes[0], "transition": passes[1]}, "city_pass": any(passes),
                   "agreement_of_val_and_test_winner": {"cells": float(np.mean(per["agree_cells"])),
                                                        "targets": float(np.mean(per["agree_targets"]))},
                   "share_given_to_frozen": {"cells": float(np.mean(per["frozen_cells"])),
                                             "targets": float(np.mean(per["frozen_targets"]))},
                   "ratio_frozen_over_trained_per_sensor": spread, "scopes": {}}
            rec["city_fail"] = bool(rec["one_model_wins_every_regime"] or rec["selector_within_2_sigma_every_regime"])
            for i, sc in enumerate(SCOPES):
                rec["scopes"][sc] = {"frozen": float(mf[i]), "trained": float(mt[i]), "sigma_seed": float(sig[i]),
                                     "better_single": float(single[i]), "lower_of_the_two": float(min(mf[i], mt[i])),
                                     "selector": float(selm[i]), "selector_std_over_seeds": float(np.std(per["selector"], 0, ddof=1)[i]),
                                     "mean_of_forecasts": float(mixm[i]), "oracle": float(np.mean(per["oracle"], 0)[i]),
                                     "gain_over_better_single": float(gain[i]),
                                     "gain_in_sigma_seed": float(gain[i] / sig[i]) if sig[i] > 0 else None}
            out["pairs"][f"{k}|{m}"] = rec
    return out


def cmd_measures(args) -> int:
    """The measures and the lines of the plan from the cell files of the roots: ``measures.json`` and ``MEASURES.md`` in --out.
    A line reads the main pair of each city under the rule of LINE_RULE."""
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    res = {}
    for root in map(Path, args.roots):
        dataset = root.name.split("_h")[0]
        res[dataset] = {rule: city_measures(root, dataset, rule) for rule in RULES}
    cities = list(res)
    line = {d: res[d][LINE_RULE[d]] for d in cities}
    main = {d: line[d]["pairs"]["|".join(line[d]["main_pair"])] for d in cities}
    n_pass = sum(main[d]["city_pass"] for d in cities)
    n_within = sum(main[d]["selector_within_2_sigma_every_regime"] for d in cities)
    n_one = sum(main[d]["one_model_wins_every_regime"] for d in cities)
    need = 4 if len(cities) == 5 else None
    verdict = {"cities": cities, "city_pass": n_pass, "selector_within_2_sigma_every_regime": n_within,
               "one_model_wins_every_regime": n_one,
               "line": ("not read: the line needs five cities" if need is None else "pass" if n_pass >= need else "fail" if max(n_within, n_one) >= need
                        else "between the lines")}
    (out / "measures.json").write_text(json.dumps({"verdict": verdict, "cities": res}, indent=1))
    f = lambda x: "n/a" if x is None or not np.isfinite(x) else f"{x:.4f}"
    md = ["# fmroute: the measures of the frozen and the trained side, per regime", "",
          "Test split, h = 12, MAE in the raw unit of the city, zero mask, targets whose window has a regime label. "
          "A value of the trained side, of the selector and of the mean is the mean over 3 seeds. "
          "The main pair of a city is the frozen setting and the trained model with the lowest validation MAE.", "",
          f"**Line of the plan (main pair, rule of the city):** {verdict['line']}. Cities that pass: {n_pass}. "
          f"Cities where the selector is within 2 sigma_seed in every regime: {n_within}. "
          f"Cities where one model wins every regime: {n_one}.", ""]
    for rule_of in ("line", "other"):
        md += [f"## {'The rule that the line reads' if rule_of == 'line' else 'The other rule'}", ""]
        for d in cities:
            rule = LINE_RULE[d] if rule_of == "line" else [r for r in RULES if r != LINE_RULE[d]][0]
            cm = res[d][rule]
            sh = cm["share_of_targets"]
            md += [f"### {d}, {rule} rule", "",
                   "Share of the targets: " + ", ".join(f"{r} {sh[r]:.3f}" for r in REGIMES) + ".", "",
                   "| Model | Side | " + " | ".join(SCOPES) + " |", "|---|---|" + "---|" * len(SCOPES)]
            for name, m in cm["models"].items():
                cell = lambda sc: f(m["test_mae"][sc]) + (f" ± {m['sigma_seed'][sc]:.4f}" if m["side"] == "trained" else "")
                md.append(f"| `{name}` | {m['side']} | " + " | ".join(cell(sc) for sc in SCOPES) + " |")
            md.append("")
            for key, rec in cm["pairs"].items():
                tag = " (main pair)" if key == "|".join(cm["main_pair"]) else ""
                md += [f"**Pair `{key.replace('|', '` and `')}`{tag}.** Better single model: `{rec['better_single']}`. "
                       f"Validation and test winner agree in {rec['agreement_of_val_and_test_winner']['cells']:.3f} of the cells "
                       f"({rec['agreement_of_val_and_test_winner']['targets']:.3f} of the targets). "
                       f"The selector gives {rec['share_given_to_frozen']['targets']:.3f} of the targets to the frozen model. "
                       f"City pass: {rec['city_pass']}; within 2 sigma_seed in every regime: "
                       f"{rec['selector_within_2_sigma_every_regime']}; one model wins every regime: "
                       f"{rec['one_model_wins_every_regime']}.", "",
                       "| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | "
                       "Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |", "|---|---|---|---|---|---|---|---|---|---|"]
                for sc in SCOPES:
                    q, sp = rec["scopes"][sc], rec["ratio_frozen_over_trained_per_sensor"][sc]
                    rs = f"{sp['p10']:.2f} / {sp['p50']:.2f} / {sp['p90']:.2f}" if sp["sensors"] else "n/a"
                    md.append(f"| {sc} | {f(q['better_single'])} | {f(q['lower_of_the_two'])} | {f(q['selector'])} | "
                              f"{f(q['mean_of_forecasts'])} | {f(q['oracle'])} | {f(q['gain_over_better_single'])} | "
                              f"{'n/a' if q['gain_in_sigma_seed'] is None or not np.isfinite(q['gain_in_sigma_seed']) else format(q['gain_in_sigma_seed'], '.1f')} | "
                              f"{rs} | {format(sp['share_below_1'], '.3f') + ' of ' + str(sp['sensors']) if sp['sensors'] else 'n/a'} |")
                md.append("")
    (out / "MEASURES.md").write_text("\n".join(md))
    print(json.dumps(verdict))
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
    p = sub.add_parser("cells"); p.add_argument("--root", required=True); p.add_argument("--dataset", required=True)
    p = sub.add_parser("measures"); p.add_argument("--roots", nargs="+", required=True); p.add_argument("--out", required=True)
    p = sub.add_parser("regimecheck")
    p.add_argument("--dataset", required=True); p.add_argument("--model", default="amazon/chronos-bolt-small")
    p.add_argument("--device", default="cuda"); p.add_argument("--context-steps", type=int, default=None, help="default: 14 hours")
    args = ap.parse_args(argv)
    return {"regimes": cmd_regimes, "score": cmd_score, "chronos": cmd_chronos, "regimecheck": cmd_regimecheck, "cells": cmd_cells,
            "measures": cmd_measures}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
