"""regimehead: a training loss per traffic regime on one trained model (Survey/experiments/regimehead-plan.md).

    python -m pilot.regimehead root --dataset pemsbay      # results/regimehead/pemsbay_h12: archs.jsonl, FROZEN.md, data/
    python -m pilot.regimehead cells --dataset pemsbay     # on the cluster of the city: <root>/cells.npz from the forecast dumps
    python -m pilot.regimehead measures --datasets pemsbay chengdu metrla --out results/regimehead/compare/MEASURES.md

The two models of a city are the records of ``results/fmroute/<city>_h12/archs.jsonl``.  Their runs there are the MAE head.  A
record of this root is the same genotype with one more key, ``train_loss``; ``pilot.train_arch`` then trains with that loss
(``make_loss``) and changes nothing else: the early stop reads the validation MAE, and the zero mask holds.
  mse    : squared error
  huber  : Huber, delta = 1 in the dataset-normalised unit
  focal  : MAE-Focal, |e| * (2 * sigmoid(0.2 * |e_raw|) - 1), e_raw = the error in the raw unit of the city
  wmae2, wmae4 : MAE with the weight 2 or 4 on the targets of a window that has a regime label other than free flow (the rule
           that the line reads at the city, pilot.fmroute.LINE_RULE); a window with a missing speed keeps the weight 1
Cells: sums of the absolute and of the squared error and counts of valid targets per sensor and regime, per model, head, seed,
split and regime rule.  Measures: the table per head and regime, the composites and the lines of the plan.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np

from pilot.fmroute import (CITY, FREE_MPH, FREE_REL, LINE_RULE, MPH, REGIMES, RULES, free_flow_speed, load_raw,
                           regime_labels, targets)

BASE, SOURCE = Path("results/regimehead"), Path("results/fmroute")
NEW_HEADS = ("mse", "huber", "focal", "wmae2", "wmae4")
HEADS = ("mae",) + NEW_HEADS
SEEDS = (0, 1, 2)
SCOPES = REGIMES + ("labelled",)
FROZEN_NAME = "chronos2_joint"


def make_loss(name: str, dataset: str):
    """loss(target, prediction, mask) on [B, H, N] tensors in the dataset-normalised unit; mask True = observed target."""
    import torch
    import torch.nn.functional as F

    raw = load_raw(dataset)[:, :, 0]
    n_train = int(len(raw) * 0.6)
    mu, sd = raw[:n_train].mean(0), raw[:n_train].std(0)
    sd = np.where(sd == 0, 1.0, sd)
    sd_t = torch.tensor(sd, dtype=torch.float32)
    weight = {"wmae2": 2.0, "wmae4": 4.0}.get(name)
    if weight is not None:
        spec = CITY[dataset]
        if spec["speed_channel"] != 0:
            raise ValueError(f"{dataset}: the target is not the speed channel; the weighted loss reads the regime from the target")
        if LINE_RULE[dataset] == "absolute":
            hi = np.full(len(mu), FREE_MPH * (MPH if spec["unit"] == "km/h" else 1.0))
        else:
            hi = FREE_REL * free_flow_speed(dataset)
        hi_t = torch.tensor((hi - mu) / sd, dtype=torch.float32)       # the free-flow threshold in the normalised unit
    elif name not in ("mse", "huber", "focal"):
        raise ValueError(f"train_loss {name!r}: one of {NEW_HEADS}")

    def mean(elem, w):
        return (elem * w).sum() / w.sum().clamp_min(1.0)

    def loss(target, prediction, mask=None):
        target, prediction = target.float(), prediction.float()
        m = torch.ones_like(target) if mask is None else mask.to(target.dtype)
        err = prediction - target
        if name == "mse":
            return mean(err ** 2, m)
        if name == "huber":
            return mean(F.huber_loss(prediction, target, reduction="none", delta=1.0), m)
        if name == "focal":
            a = err.abs()
            return mean(a * (2 * torch.sigmoid(0.2 * a * sd_t.to(a.device)) - 1), m)
        labelled = (m > 0).all(1, keepdim=True)                         # [B, 1, N]: every speed of the target window is observed
        free = (target > hi_t.to(target.device)).all(1, keepdim=True)
        w = torch.where(labelled & ~free, weight, 1.0).to(target.dtype)
        return mean(err.abs(), m * w)

    return loss


def cmd_root(args) -> int:
    ds = args.dataset
    src, root = SOURCE / f"{ds}_h12", BASE / f"{ds}_h12"
    root.mkdir(parents=True, exist_ok=True)
    recs = [json.loads(line) for line in open(src / "archs.jsonl") if line.strip()]
    out = []
    for r in recs:
        for h in NEW_HEADS:
            g = dict(r["genotype"])
            g["train_loss"] = h
            out.append({**r, "arch_id": f"{r['arch_id']}_{h}", "genotype": g, "source_arch_id": r["arch_id"]})
    (root / "archs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in out))
    (root / "FROZEN.md").write_text(
        f"# FROZEN: {root} — the two trained models of fmroute at this city, with five other training losses\n\n"
        f"- `archs.jsonl`: {len(out)} records, written by `python -m pilot.regimehead root --dataset {ds}`.  A record is a record of\n"
        f"  `{src}/archs.jsonl` with the key `train_loss` in its genotype and the loss name at the end of its `arch_id`.\n"
        f"  The losses: {', '.join(NEW_HEADS)} (`pilot.regimehead.make_loss`).  The regime rule of the weighted losses is "
        f"`{LINE_RULE[ds]}`.\n"
        f"- The MAE head is not trained here: its 6 runs are `{src}/train/<arch_id>/seed<s>`.\n"
        f"- `data/`: a byte copy of `{src}/data`.\n"
        f"- Everything else is the protocol of `{src}/FROZEN.md`: 20 epochs (patience 5, minimum 8), the early stop on the\n"
        f"  validation MAE, the zero mask, h = 12, seeds 0 to 2, the forecast dump of the best epoch.\n"
        f"- Command: `JOB_NAME=rh_{ds} TRAIN_EXTRA=\"--mask-zeros --dump-forecasts\" SCORE_PROXIES=0 SEED_SUBSET={len(out)} "
        f"pilot/submit.sh train {root} {ds} 12`.\n")
    if (src / "data").is_dir() and not (root / "data").exists():
        shutil.copytree(src / "data", root / "data")
    print(f"{root}: {len(out)} records; data/ {'present' if (root / 'data').exists() else 'absent (copy it on the cluster of the city)'}")
    return 0


def _runs(ds: str):
    """{(model, head): folder of the three seeds}."""
    src, root = SOURCE / f"{ds}_h12", BASE / f"{ds}_h12"
    models = [json.loads(line)["arch_id"] for line in open(src / "archs.jsonl") if line.strip()]
    return models, {(m, h): (src / "train" / m if h == "mae" else root / "train" / f"{m}_{h}") for m in models for h in HEADS}


def cmd_cells(args) -> int:
    ds = args.dataset
    root = BASE / f"{ds}_h12"
    raw = load_raw(ds)
    models, runs = _runs(ds)
    n = raw.shape[1]
    shape = (len(models), len(HEADS), len(SEEDS), 2, len(RULES), n, 3)
    abs_s, sq_s = np.full(shape, np.nan), np.full(shape, np.nan)
    counts = np.zeros((2, len(RULES), n, 3))
    frozen = np.full((len(RULES), n, 3), np.nan)
    for si, split in enumerate(("val", "test")):
        y, valid, rows = targets(ds, split, raw)
        labs = [regime_labels(ds, split, raw, rule) for rule in RULES]
        for ri, lab in enumerate(labs):
            for r in range(3):
                counts[si, ri, :, r] = (valid & (lab == r)[:, None, :]).sum((0, 1))
        for (m, h), folder in runs.items():
            for k, s in enumerate(SEEDS):
                d = folder / f"seed{s}"
                rec = json.load(open(d / "metrics.json"))
                if rec.get("status") != "done" or rec["forecast_dump"][split]["first_target_row"] != int(rows[0]):
                    raise SystemExit(f"{d}: status {rec.get('status')}, or the windows of the dump are not those of the split")
                err = np.where(valid, np.load(d / f"forecast_{split}.npy").astype(np.float64) - y, 0.0)
                a, q = np.abs(err).sum(1), (err ** 2).sum(1)                       # [windows, sensors]
                for ri, lab in enumerate(labs):
                    for r in range(3):
                        sel = lab == r
                        abs_s[models.index(m), HEADS.index(h), k, si, ri, :, r] = (a * sel).sum(0)
                        sq_s[models.index(m), HEADS.index(h), k, si, ri, :, r] = (q * sel).sum(0)
                print(json.dumps({"split": split, "model": m, "head": h, "seed": s, "mae": float(a.sum() / valid.sum())}), flush=True)
    fz = SOURCE / f"{ds}_h12" / "cells" / "test" / f"{FROZEN_NAME}.npz"
    if fz.exists():
        z = np.load(fz)
        for ri, rule in enumerate(RULES):
            frozen[ri] = z[f"sums_{rule}"].sum(-1)
            assert np.allclose(z[f"counts_{rule}"].sum(-1), counts[1, ri]), "the counts of the frozen cells differ"
    np.savez_compressed(root / "cells.npz", models=np.array(models), heads=np.array(HEADS), rules=np.array(RULES),
                        abs=abs_s, sq=sq_s, counts=counts, frozen_abs=frozen)
    print(f"wrote {root / 'cells.npz'}")
    return 0


def city_measures(ds: str) -> dict:
    """The measures of stage 0 at one city under the rule that the line reads.  Index order of an error array: [head, seed,
    split (0 val, 1 test), sensor, regime]."""
    z = np.load(BASE / f"{ds}_h12" / "cells.npz")
    ri = list(z["rules"]).index(LINE_RULE[ds])
    cnt = z["counts"][:, ri]                                                       # [split, sensor, regime]
    out = {"dataset": ds, "rule": LINE_RULE[ds], "unit": CITY[ds]["unit"], "share": (cnt[1].sum(0) / cnt[1].sum()).tolist(), "models": {}}
    fz = z["frozen_abs"][ri]
    frozen = None if np.isnan(fz).any() else _scopes(fz, cnt[1], False)

    for mi, model in enumerate(z["models"]):
        res = {}
        for metric, key in (("mae", "abs"), ("rmse", "sq")):
            E = z[key][mi, :, :, :, ri]                                            # [head, seed, split, sensor, regime]
            root = metric == "rmse"
            per = np.array([[_scopes(E[h, k, 1], cnt[1], root) for k in range(len(SEEDS))] for h in range(len(HEADS))])  # [head, seed, scope]
            ref, sigma = per[0].mean(0), per[0].std(0, ddof=1)
            # the choice of a head: by the error on the validation split, mean of the seeds (one choice per model)
            val = E[:, :, 0].mean(1)                                               # [head, sensor, regime]
            pick_regime = np.argmin(_rate(val.sum(1), cnt[0].sum(0), root), 0)     # [regime]
            with np.errstate(invalid="ignore", divide="ignore"):
                cell = np.where(cnt[0][None] > 0, val / np.maximum(cnt[0][None], 1), np.inf)
            pick_cell = np.where(np.isinf(cell).all(0), 0, np.argmin(cell, 0))     # [sensor, regime]; no validation target -> MAE head
            comp_regime, comp_cell, ceil_regime, ceil_cell = [], [], [], []
            for k in range(len(SEEDS)):
                T = E[:, k, 1]                                                     # [head, sensor, regime]
                comp_regime.append(_scopes(_take(T, np.broadcast_to(pick_regime, T.shape[1:])), cnt[1], root))
                comp_cell.append(_scopes(_take(T, pick_cell), cnt[1], root))
                others = E[:, [j for j in range(len(SEEDS)) if j != k], 1].mean(1)  # the test error of the two other seeds
                c_regime = np.argmin(others.sum(1), 0)
                ceil_regime.append(_scopes(_take(T, np.broadcast_to(c_regime, T.shape[1:])), cnt[1], root))
                ceil_cell.append(_scopes(_take(T, np.argmin(others, 0)), cnt[1], root))
            res[metric] = {
                "per_head": {h: {"mean": per[i].mean(0).tolist(), "sd": per[i].std(0, ddof=1).tolist()} for i, h in enumerate(HEADS)},
                "ref": ref.tolist(), "sigma": sigma.tolist(), "pick_regime": [HEADS[i] for i in pick_regime],
                "pick_cell_share": {h: float((pick_cell == i).mean()) for i, h in enumerate(HEADS)},
                **{name: {"mean": np.mean(v, 0).tolist(), "sd": np.std(v, 0, ddof=1).tolist()}
                   for name, v in (("comp_regime", comp_regime), ("comp_cell", comp_cell), ("ceil_regime", ceil_regime), ("ceil_cell", ceil_cell))}}
        m = res["mae"]
        if frozen is not None:
            m["frozen"] = frozen.tolist()
            with np.errstate(invalid="ignore", divide="ignore"):
                m["gap_closed"] = ((np.array(m["ref"]) - np.array(m["comp_regime"]["mean"])) / (np.array(m["ref"]) - frozen)).tolist()
        for metric in ("mae", "rmse"):
            r = res[metric]
            ref, sg = np.array(r["ref"]), np.array(r["sigma"])
            gain = lambda name: (ref - np.array(r[name]["mean"])) / sg              # noqa: E731  in sigma_seed, per scope
            g_comp, g_ceil = gain("comp_regime"), gain("ceil_regime")
            r["gain_sigma"] = {name: gain(name).tolist() for name in ("comp_regime", "comp_cell", "ceil_regime", "ceil_cell")}
            r["pass"] = bool((g_comp[1] > 2 or g_comp[2] > 2) and g_comp[3] >= -1)
            r["ceiling_within"] = bool((g_ceil[:3] <= 2).all())
        out["models"][str(model)] = res
    return out


def _rate(s, c, root):
    with np.errstate(invalid="ignore", divide="ignore"):
        v = np.where(c > 0, s / np.maximum(c, 1), np.nan)
    return np.sqrt(v) if root else v


def _scopes(s, c, root):
    """s, c [sensor, regime] -> the error in the three regimes and over the labelled targets."""
    s, c = s.sum(0), c.sum(0)
    return _rate(np.append(s, s.sum()), np.append(c, c.sum()), root)


def _take(T, pick):
    """T [head, sensor, regime], pick [sensor, regime] -> the sums of the picked head."""
    return np.take_along_axis(T, pick[None], 0)[0]


def cmd_measures(args) -> int:
    cities = [city_measures(ds) for ds in args.datasets]
    L = ["# regimehead: the head per regime, the composites and the lines of stage 0", "",
         "Test split, h = 12, mean of 12 steps, raw unit, zero mask, targets with a regime label.  A value is the mean of 3 seeds.",
         "sigma_seed of a scope is the standard deviation (ddof = 1) of the MAE head over its 3 seeds in that scope.  The choice of a",
         "head uses the validation split (mean of the seeds); the ceiling of a seed uses the test split of the two other seeds.",
         "A gain is the MAE head minus the composite, in sigma_seed.", ""]
    verdict = {"mae": [], "rmse": []}
    for c in cities:
        L += [f"## {c['dataset']} (rule {c['rule']}, {c['unit']}); share of the targets: " +
              ", ".join(f"{r} {s:.3f}" for r, s in zip(REGIMES, c["share"])), ""]
        for model, res in c["models"].items():
            for metric in ("mae", "rmse"):
                r = res[metric]
                L += [f"### `{model}`, {metric.upper()}", "", "| Row | " + " | ".join(SCOPES) + " |", "|---|" + "---|" * len(SCOPES)]
                for h in HEADS:
                    L.append(f"| head {h} | " + " | ".join(f"{a:.4f} ± {b:.4f}" for a, b in zip(r["per_head"][h]["mean"], r["per_head"][h]["sd"])) + " |")
                for name, label in (("comp_regime", "composite per regime, validation choice"), ("comp_cell", "composite per sensor and regime, validation choice"),
                                    ("ceil_regime", "ceiling per regime"), ("ceil_cell", "ceiling per sensor and regime")):
                    L.append(f"| {label} | " + " | ".join(f"{a:.4f} ({g:+.1f} σ)" for a, g in zip(r[name]["mean"], r["gain_sigma"][name])) + " |")
                if metric == "mae" and "frozen" in r:
                    L.append(f"| {FROZEN_NAME} | " + " | ".join(f"{a:.4f}" for a in r["frozen"]) + " |")
                    L.append("| share of the gap to the frozen model that the composite per regime closes | " + " | ".join(f"{a:.3f}" for a in r["gap_closed"]) + " |")
                L += ["", f"Head chosen per regime on the validation split: {', '.join(f'{a} {b}' for a, b in zip(REGIMES, r['pick_regime']))}.  "
                      f"Share of the sensor-regime cells per head: {', '.join(f'{h} {v:.2f}' for h, v in r['pick_cell_share'].items())}.  "
                      f"Pass clause: {r['pass']}.  Ceiling within 2 σ in every regime: {r['ceiling_within']}.", ""]
        for metric in ("mae", "rmse"):
            verdict[metric].append((c["dataset"], any(res[metric]["pass"] for res in c["models"].values()),
                                    all(res[metric]["ceiling_within"] for res in c["models"].values())))
    L += ["## The lines", "", "| Metric | City | Pass clause, one model at least | Ceiling within 2 σ in every regime, both models |", "|---|---|---|---|"]
    for metric in ("mae", "rmse"):
        L += [f"| {metric.upper()} | {ds} | {p} | {f} |" for ds, p, f in verdict[metric]]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n")
    out.with_suffix(".json").write_text(json.dumps(cities, indent=1))
    print("\n".join(L[-(3 + 2 * len(cities)):]))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="regimehead: a training loss per traffic regime")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("root", "cells"):
        sub.add_parser(name).add_argument("--dataset", required=True, choices=sorted(CITY))
    p = sub.add_parser("measures"); p.add_argument("--datasets", nargs="+", required=True); p.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    return {"root": cmd_root, "cells": cmd_cells, "measures": cmd_measures}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
