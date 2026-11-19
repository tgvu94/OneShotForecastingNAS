"""spatialgate, the neural stage: the dataset files, the root, the sensor sets and the run lists of one LargeST set.

    python -m pilot.spatialgate_root prepare --set sd      # LARGESTSD.npz, its adjacency, results/spatialgate/largestsd_h12/
    python -m pilot.spatialgate_root oracle  --set sd      # after the base and the full model have 3 seeds: the oracle sets
    python -m pilot.spatialgate_root read    --set sd      # the table of the trained runs

prepare
  data   : $NAS_DATA_ROOT/PEMS/LARGEST<SET>.npz, ``data`` [T, N, 1], 2019 flow at 15-minute steps (pilot.spatialgate.load_largest);
           a missing value is 0, which the masked pipeline skips.  A sensor with fewer than half of its training rows valid is
           dropped (the rule of the linear stage), so N is below the published count; the kept sensors are in <root>/sensors.csv.
  senders: <root>/data/<dataset>_senders.npy [N, 16]: for each sensor the linked sensors with the highest weight of the LargeST
           adjacency (the larger of the two directions), nearest first, -1 where a sensor has fewer links.
  sets   : <root>/sets/<name>.json, receivers of the gated model, each at the shares 0.10, 0.25 and 0.50 of the kept sensors:
           lin = highest linear gain d of the linear stage (fit on train, read on validation); c1s = highest residual score c1;
           deg = highest degree; rnd<share><a|b|c> = three random draws.  Ties keep the sensor order.
  archs  : <root>/archs.jsonl: stid (no module), full (every sensor a receiver), gate_<set>.
  runs   : <root>/runs_cost.txt (stid and full, seed 0) and <root>/runs_main.txt, one "arch_id seed" per line.
oracle
  ora = highest gain of the full model over the base model in test MAE per sensor, mean of the seeds.  It reads the test split
  and is an upper bound only.  Appends its three archs and writes <root>/runs_oracle.txt.
"""
from __future__ import annotations

import argparse
import json
import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from pilot import spatialgate as sg

BASE = Path("results/spatialgate")
SHARES = (10, 25, 50)
K_MAX = 16
SEEDS = (0, 1, 2)
N_KEPT = {"largestsd": 705, "largestgla": 3805}     # pilot.datasets holds the same counts


def _genotype(root: Path, set_name: str) -> dict:
    return {"hand_model": "stid_spatial", "clock": "true", "head": "mae", "graph": None, "space": "hand_v1",
            "spatial": {"root": str(root), "set": set_name, "k": K_MAX}}


def _top(v: np.ndarray, k: int) -> list[int]:
    return sorted(int(i) for i in np.argsort(-np.nan_to_num(v, nan=-np.inf), kind="stable")[:k])


def _write_set(root: Path, name: str, sensors: list[int], note: str) -> None:
    (root / "sets").mkdir(parents=True, exist_ok=True)
    json.dump({"name": name, "n": len(sensors), "note": note, "sensors": sensors}, open(root / "sets" / f"{name}.json", "w"))


def prepare(args) -> int:
    ds = f"largest{args.set}"
    name = ds.upper()
    root = BASE / f"{ds}_h12"
    data_root = Path(os.environ["NAS_DATA_ROOT"])
    x, A, _ = sg.load_largest(ds)
    T, n_all = x.shape
    n_train = int(T * sg.TRAIN_SHARE)
    valid = np.isfinite(x) & (x != 0)
    excluded = valid[:n_train].mean(0) < sg.MIN_TRAIN_VALID
    lin = pd.read_csv(Path(args.linear) / f"linear_sensors_{ds}.csv")
    assert len(lin) == n_all and np.array_equal(lin["excluded"].to_numpy().astype(bool), excluded), "the linear stage excluded other sensors"
    kept = np.flatnonzero(~excluded)
    n = len(kept)
    assert n == N_KEPT[ds], (n, N_KEPT[ds])
    data = np.where(valid, x, 0)[:, kept].astype(np.float32)
    adj = A[np.ix_(kept, kept)].astype(np.float32)
    np.savez_compressed(data_root / "PEMS" / f"{name}.npz", data=data[:, :, None])
    pickle.dump(adj, open(data_root / "PEMS" / f"adj_{name}.pkl", "wb"))
    (data_root / "PEMS" / f"{name}_README.md").write_text(
        f"# {name}\n\nLargeST 2019 flow, 15-minute steps (mean of the valid 5-minute values), sensor set {args.set}; {n_all - n} of {n_all} "
        f"sensors dropped (fewer than half of the training rows valid); a missing value is 0; adjacency = LargeST adjacency > 0, "
        f"symmetric, zero diagonal.\n\ndata {data.shape}, zeros {float((data == 0).mean()):.4f}, edges {int(adj.sum() // 2)}.\n")

    meta = pd.read_csv(sg._largest_dir() / "ca_meta.csv")
    in_set = np.arange(len(meta)) if sg.LARGEST[ds] is None else np.flatnonzero(meta["District"].isin(sg.LARGEST[ds]).to_numpy())
    W = np.load(sg._largest_dir() / "adjacency.npy", mmap_mode="r")
    W = np.asarray(W[np.ix_(in_set[kept], in_set[kept])], dtype=np.float32)
    W = np.maximum(W, W.T)
    np.fill_diagonal(W, 0)
    order = np.argsort(-W, axis=1, kind="stable")[:, :K_MAX]
    senders = np.where(np.take_along_axis(W, order, 1) > 0, order, -1).astype(np.int64)
    (root / "data").mkdir(parents=True, exist_ok=True)
    np.save(root / "data" / f"{ds}_senders.npy", senders)
    pd.DataFrame({"sensor": np.arange(n), "index_in_set": kept, "id": meta["ID"].to_numpy()[in_set[kept]]}).to_csv(root / "sensors.csv", index=False)

    lin = lin.iloc[kept].reset_index(drop=True)
    signals = {"lin": lin["d"].to_numpy(), "c1s": lin["c1"].to_numpy(), "deg": lin["degree"].to_numpy().astype(float)}
    archs = [("stid", "none"), ("full", "all")]
    runs = [("stid", s) for s in SEEDS] + [("full", s) for s in SEEDS]
    for share in SHARES:
        k = int(np.ceil(share / 100 * n))
        for key, v in signals.items():
            sname = f"{key}{share}"
            _write_set(root, sname, _top(v, k), f"top {share} % of {n} sensors by {key}")
            archs.append((f"gate_{sname}", sname))
            runs += [(f"gate_{sname}", s) for s in (SEEDS if key == "lin" else SEEDS[:1])]
        for j, letter in enumerate("abc"):
            sname = f"rnd{share}{letter}"
            rng = np.random.default_rng(1000 * share + j)
            _write_set(root, sname, sorted(int(i) for i in rng.choice(n, size=k, replace=False)), f"random {share} % of {n} sensors, draw {letter}")
            archs.append((f"gate_{sname}", sname))
            runs.append((f"gate_{sname}", SEEDS[j]))
    with open(root / "archs.jsonl", "w") as f:
        for aid, sname in archs:
            f.write(json.dumps({"arch_id": aid, "genotype": _genotype(root, sname)}) + "\n")
    (root / "runs_cost.txt").write_text("stid 0\nfull 0\n")
    (root / "runs_main.txt").write_text("".join(f"{a} {s}\n" for a, s in runs))
    print(f"{ds}: data {data.shape}, dropped {n_all - n}, edges {int(adj.sum() // 2)}, sensors without a sender {int((senders[:, 0] < 0).sum())}, "
          f"mean senders {float((senders >= 0).sum(1).mean()):.1f}; {len(archs)} archs, {len(runs)} runs -> {root}")
    return 0


def _sensor_mae(root: Path, arch: str, split: str) -> np.ndarray:
    """[seeds, N] MAE per sensor in the raw unit, for the seeds that are done."""
    out = []
    for s in SEEDS:
        f = root / "train" / arch / f"seed{s}" / "sensor_mae.npz"
        if f.exists():
            out.append(np.load(f)[f"{split}_mae_raw"])
    return np.stack(out) if out else np.zeros((0, 0))


def oracle(args) -> int:
    ds = f"largest{args.set}"
    root = BASE / f"{ds}_h12"
    base, full = _sensor_mae(root, "stid", "test"), _sensor_mae(root, "full", "test")
    assert len(base) == len(SEEDS) and len(full) == len(SEEDS), f"need {len(SEEDS)} seeds of stid and full, have {len(base)} and {len(full)}"
    gain = base.mean(0) - full.mean(0)
    n = len(gain)
    known = {json.loads(l)["arch_id"] for l in open(root / "archs.jsonl")}
    runs = []
    with open(root / "archs.jsonl", "a") as f:
        for share in SHARES:
            sname = f"ora{share}"
            _write_set(root, sname, _top(gain, int(np.ceil(share / 100 * n))), f"top {share} % of {n} sensors by the test gain of full over stid (upper bound)")
            if f"gate_{sname}" not in known:
                f.write(json.dumps({"arch_id": f"gate_{sname}", "genotype": _genotype(root, sname)}) + "\n")
            runs.append(f"gate_{sname} 0\n")
    (root / "runs_oracle.txt").write_text("".join(runs))
    print(f"{ds}: oracle sets written; summed test gain {float(np.nansum(gain)):.2f} over {n} sensors")
    return 0


def read(args) -> int:
    ds = f"largest{args.set}"
    root = BASE / f"{ds}_h12"
    rows = []
    for line in open(root / "archs.jsonl"):
        aid = json.loads(line)["arch_id"]
        for s in SEEDS:
            f = root / "train" / aid / f"seed{s}" / "metrics.json"
            if not f.exists():
                continue
            m = json.load(open(f))
            if m.get("status") != "done":
                continue
            sm = root / "train" / aid / f"seed{s}" / "sensor_mae.npz"
            z = np.load(sm) if sm.exists() else None
            rows.append({"arch_id": aid, "seed": s, "val_mae": m["val_mae"], "test_mae": m["test_mae"],
                         "test_mae_raw": float(z["test_mae_raw_all"]) if z is not None else float("nan"),
                         "best_epoch": m["best_epoch"], "epochs_run": m["epochs_run"], "train_seconds": m["train_seconds"],
                         "seconds_per_epoch": m["train_seconds"] / max(m["epochs_run"], 1), "peak_mem_gb": m["peak_mem_gb"], "params": m["params"]})
    df = pd.DataFrame(rows)
    (root / "tables").mkdir(exist_ok=True)
    df.to_csv(root / "tables" / "runs.csv", index=False, float_format="%.6g")
    if len(df):
        g = df.groupby("arch_id").agg(seeds=("seed", "count"), test_mae=("test_mae", "mean"), test_sd=("test_mae", "std"),
                                      test_mae_raw=("test_mae_raw", "mean"), raw_sd=("test_mae_raw", "std"),
                                      seconds_per_epoch=("seconds_per_epoch", "mean"), peak_mem_gb=("peak_mem_gb", "max")).reset_index()
        g.to_csv(root / "tables" / "archs.csv", index=False, float_format="%.6g")
        cols = ["arch_id", "seeds", "test_mae_raw", "raw_sd", "seconds_per_epoch", "peak_mem_gb"]
        lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        lines += ["| " + " | ".join(f"{v:.3f}" if isinstance(v, float) else str(v) for v in r) + " |" for r in g[cols].itertuples(index=False)]
        (root / "tables" / "archs.md").write_text(f"# {ds}: test MAE in the raw unit, mean and standard deviation of the seeds\n\n" + "\n".join(lines) + "\n")
        print(g.to_string(index=False))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="spatialgate: root of the neural stage")
    ap.add_argument("mode", choices=["prepare", "oracle", "read"])
    ap.add_argument("--set", required=True, choices=["sd", "gla"])
    ap.add_argument("--linear", default="results/spatialgate/compare/tables", help="tables of the linear stage")
    args = ap.parse_args(argv)
    return {"prepare": prepare, "oracle": oracle, "read": read}[args.mode](args)


if __name__ == "__main__":
    raise SystemExit(main())
