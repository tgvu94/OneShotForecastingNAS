"""calibration: a hand design under the published protocol against the published error and against the frozen model
(Survey/experiments/calibration-plan.md).

    python -m pilot.calibration --datasets metrla pemsbay --out results/calibration/compare/MEASURES.md
    python -m pilot.calibration --datasets metrla pemsbay --parts --out results/calibration/compare/PARTS.md

Reads, per city:
  $NAS_ROOT/BasicTS/checkpoints/<run>/<NAME>/full_s<seed>/*/test_results/predictions.npy   BasicTS run of a model, stock config,
        test part of the split 0.7 / 0.1 / 0.2, history of 12 steps (raw float32 memmap [windows, 12, sensors, 1], raw unit)
  results/calibration/<city>/frozen/chronos2_joint_test.npy      the stored forecast of pilot.fmroute chronos (benchst test windows)
  results/calibration/<city>/benchst/<model>_seed<s>.npy         the forecast dump of a model of results/fmroute/<city>_h12
The common windows are the test windows of the published split that are also test windows of the benchst split.  One scorer:
the masked MAE in the raw unit (a target of 0 is missing), at step 3, 6 and 12, as the mean of the 12 steps, and per regime
(pilot.fmroute, absolute rule) for the mean of the 12 steps.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np

from pilot.fmroute import HORIZON, REGIMES, WINDOW, load_raw, regime_labels, split_rows

BASE = Path("results/calibration")
NAME = {"metrla": "METR-LA", "pemsbay": "PEMS-BAY"}
PUBLISHED = {"STID": {"metrla": 3.12, "pemsbay": 1.56}, "GWNet": {"metrla": 3.03, "pemsbay": 1.59}}   # [shao2024basicts], Table V
RUNS = {"STID": "STID_ablation", "GWNet": "GWNet_calibration"}        # folder under BasicTS/checkpoints
SEEDS = (0, 1, 2)
COLS = ("step 3", "step 6", "step 12", "mean of 12") + REGIMES


def scores(pred: np.ndarray, y: np.ndarray, valid: np.ndarray, lab: np.ndarray) -> list[float]:
    err = np.where(valid, np.abs(pred.astype(np.float64) - y), 0.0)
    out = [err[:, h].sum() / valid[:, h].sum() for h in (2, 5, 11)] + [err.sum() / valid.sum()]
    for r in range(len(REGIMES)):
        sel = (lab == r)[:, None, :]
        out.append((err * sel).sum() / max((valid & sel).sum(), 1))
    return [float(v) for v in out]


def city(ds: str, basicts: Path) -> dict:
    raw = load_raw(ds)[:, :, 0].astype(np.float32)
    n, N = raw.shape
    valid_len, test_len = int(n * 0.1), int(n * 0.2)
    pub_rows = (n - test_len) + 12 + np.arange(test_len - 23)                  # first target row of every published test window
    our_rows = split_rows(n, WINDOW, HORIZON, "test")
    assert our_rows[0] >= pub_rows[0] and our_rows[-1] == pub_rows[-1], (our_rows[0], pub_rows[0], our_rows[-1], pub_rows[-1])
    skip = int(our_rows[0] - pub_rows[0])                                      # published windows before the first common one
    target = lambda rows: raw[rows[:, None] + np.arange(HORIZON)[None]]        # noqa: E731
    y_pub, y = target(pub_rows), target(our_rows)
    v_pub, v = y_pub != 0, y != 0
    lab = regime_labels(ds, "test", load_raw(ds), "absolute")
    out = {"dataset": ds, "published_windows": int(len(pub_rows)), "common_windows": int(len(our_rows)),
           "train_rows_published": int(n - valid_len - test_len), "train_rows_benchst": int(n * 0.6), "rows": {}, "whole": {}}

    def add(name, preds):                                                      # preds: list over seeds of [common windows, 12, sensors]
        s = np.array([scores(p, y, v, lab) for p in preds])
        out["rows"][name] = {"mean": s.mean(0).tolist(), "sd": (s.std(0, ddof=1).tolist() if len(s) > 1 else None), "seeds": len(s)}

    for model, run in RUNS.items():
        files = [sorted((basicts / "checkpoints" / run / NAME[ds] / f"full_s{k}").glob("*/test_results/predictions.npy")) for k in SEEDS]
        if not all(files):
            continue
        preds, whole = [], []
        for f in files:
            p = np.memmap(f[-1], dtype=np.float32, mode="r", shape=(len(pub_rows), HORIZON, N, 1))[..., 0]
            t = np.memmap(f[-1].with_name("targets.npy"), dtype=np.float32, mode="r", shape=(len(pub_rows), HORIZON, N, 1))[..., 0]
            gap = float(np.abs(np.asarray(t) - y_pub).max())
            assert gap < 1e-2, f"{f[-1]}: the targets of the run differ from the raw file at the rows of the split (max gap {gap})"
            whole.append(float((np.abs(np.asarray(p, dtype=np.float64) - y_pub) * v_pub).sum() / v_pub.sum()))
            preds.append(np.asarray(p[skip:]))
        out["whole"][model] = {"mean": float(np.mean(whole)), "sd": float(np.std(whole, ddof=1)), "published": PUBLISHED[model][ds]}
        add(f"{model}, published protocol", preds)
    add("chronos2_joint, zero-shot", [np.load(BASE / ds / "frozen" / "chronos2_joint_test.npy")])
    bench = sorted((BASE / ds / "benchst").glob("*_seed0.npy"))
    for f in bench:
        model = f.name[: -len("_seed0.npy")]
        add(f"{model}, benchst protocol", [np.load(f.with_name(f"{model}_seed{k}.npy")) for k in SEEDS])
    return out


PARTS = ("stock", "split", "nodescale", "nodeloss", "instnorm", "clip", "sched", "all")
LONG_HISTORY = ("instnorm", "all")                                   # variants whose dataset gives 96 history steps


def parts(ds: str, basicts: Path) -> dict:
    """STID under BasicTS with one part of our pipeline at a time (checkpoints/STID_parts), on the windows that every variant
    and the benchst split hold."""
    raw = load_raw(ds)[:, :, 0].astype(np.float32)
    n, N = raw.shape
    test_len = int(n * 0.2)
    first = lambda hist: (n - test_len) + hist                         # noqa: E731  first target row of the first test window
    our_rows = split_rows(n, WINDOW, HORIZON, "test")
    start = max(first(96), int(our_rows[0]))
    rows = np.arange(start, n - HORIZON + 1)
    y = raw[rows[:, None] + np.arange(HORIZON)[None]]
    v = y != 0
    lab = regime_labels(ds, "test", load_raw(ds), "absolute")[start - int(our_rows[0]):]
    out = {"dataset": ds, "windows": int(len(rows)), "rows": {}}
    for run in sorted((basicts / "checkpoints" / "STID_parts" / NAME[ds]).glob("*_s*")):
        variant, seed = run.name.rsplit("_s", 1)
        f = sorted(run.glob("*/test_results/predictions.npy"))
        if not f:
            continue
        hist = 96 if variant in LONG_HISTORY else 12
        w = test_len - hist - HORIZON + 1
        p = np.memmap(f[-1], dtype=np.float32, mode="r", shape=(w, HORIZON, N, 1))[..., 0]
        t = np.memmap(f[-1].with_name("targets.npy"), dtype=np.float32, mode="r", shape=(w, HORIZON, N, 1))[..., 0]
        skip = start - first(hist)
        gap = float(np.abs(np.asarray(t[skip:]) - y).max())
        assert gap < 1e-2, f"{f[-1]}: the targets of the run differ from the raw file (max gap {gap})"
        out["rows"].setdefault(variant, []).append(scores(np.asarray(p[skip:]), y, v, lab))
    bench = [np.load(f)[start - int(our_rows[0]):] for f in sorted((BASE / ds / "benchst").glob("stid_trueclock_seed*.npy"))]
    if bench:
        out["rows"]["benchst, stid_trueclock"] = [scores(p, y, v, lab) for p in bench]
    fz = BASE / ds / "frozen" / "chronos2_joint_test.npy"
    if fz.exists():
        out["rows"]["chronos2_joint"] = [scores(np.load(fz)[start - int(our_rows[0]):], y, v, lab)]
    return out


def parts_table(cities: list[dict]) -> list[str]:
    L = ["# calibration: STID under the BasicTS pipeline with one part of our pipeline at a time", "",
         "Masked MAE in the raw unit (mph) on the test windows that every variant and the benchst split hold.  A value is the mean of",
         "the seeds of the row; the column 'against stock' is the mean of the 12 steps against the row 'stock'.", ""]
    for c in cities:
        L += [f"## {c['dataset']} ({c['windows']} windows)", "", "| Variant | seeds | " + " | ".join(COLS) + " | against stock |", "|---|---|" + "---|" * (len(COLS) + 1)]
        ref = np.mean(c["rows"]["stock"], 0)[3] if "stock" in c["rows"] else None
        order = [p for p in PARTS if p in c["rows"]] + [k for k in c["rows"] if k not in PARTS]
        for k in order:
            m = np.mean(c["rows"][k], 0)
            L.append(f"| {k} | {len(c['rows'][k])} | " + " | ".join(f"{x:.4f}" for x in m) + f" | {100 * (m[3] / ref - 1):+.2f} % |" if ref else "")
        L.append("")
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="calibration: published protocol against the published error and the frozen model")
    ap.add_argument("--datasets", nargs="+", required=True, choices=sorted(NAME))
    ap.add_argument("--basicts", default=None, help="default: $NAS_ROOT/BasicTS, or ../BasicTS")
    ap.add_argument("--out", required=True)
    ap.add_argument("--parts", action="store_true", help="the table of the runs of pilot/calibration_parts.sbatch")
    args = ap.parse_args(argv)
    basicts = Path(args.basicts or Path(os.environ.get("NAS_ROOT", "..")) / "BasicTS")
    if args.parts:
        cities = [parts(ds, basicts) for ds in args.datasets]
        L = parts_table(cities)
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(L) + "\n")
        out.with_suffix(".json").write_text(json.dumps(cities, indent=1))
        print("\n".join(L))
        return 0
    cities = [city(ds, basicts) for ds in args.datasets]
    L = ["# calibration: hand designs under the published protocol, the frozen model and the benchst protocol", "",
         "Masked MAE in the raw unit (mph); a target of 0 is missing.  A trained value is the mean ± standard deviation (ddof = 1) of 3 seeds.",
         "The regime columns are the mean of the 12 steps over the targets of a window with that regime label (absolute rule).", ""]
    for c in cities:
        ds = c["dataset"]
        L += [f"## {ds}", "", f"Published test split: {c['published_windows']} windows; common windows: {c['common_windows']}.  "
              f"Training rows: {c['train_rows_published']} under the published split, {c['train_rows_benchst']} under benchst.", "",
              "**The whole published test split, mean of the 12 steps.**", "", "| Model | Ours, 3 seeds | Published, one run | Difference |", "|---|---|---|---|"]
        for model, w in c["whole"].items():
            L.append(f"| {model} | {w['mean']:.4f} ± {w['sd']:.4f} | {w['published']:.2f} | {100 * (w['mean'] / w['published'] - 1):+.2f} % |")
        L += ["", "**The common windows.**", "", "| Model | " + " | ".join(COLS) + " |", "|---|" + "---|" * len(COLS)]
        for name, r in c["rows"].items():
            cells = [f"{m:.4f}" + (f" ± {s:.4f}" if r["sd"] else "") for m, s in zip(r["mean"], r["sd"] or r["mean"])]
            L.append(f"| {name} | " + " | ".join(cells) + " |")
        fz = np.array(c["rows"]["chronos2_joint, zero-shot"]["mean"])
        L += ["", "| Trained model | Frozen minus trained, mean of 12 | In sigma_seed | Read |", "|---|---|---|---|"]
        for name, r in c["rows"].items():
            if r["sd"]:
                gap = fz[3] - r["mean"][3]
                k = gap / r["sd"][3]
                L.append(f"| {name} | {gap:+.4f} | {k:+.1f} | {'the trained model wins' if k > 2 else 'the frozen model wins' if k < -2 else 'no winner'} |")
        L.append("")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n")
    out.with_suffix(".json").write_text(json.dumps(cities, indent=1))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
