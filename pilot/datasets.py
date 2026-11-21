"""Dataset registry: everything that differs between PEMS04, PEMS08 and METR-LA in one place.

The genotype space is identical across datasets; only the number of sensors (``d_output`` / ``n_nodes``), the data file and
the adjacency source differ.  Raw data lives under ``$PILOT_DATA_ROOT``, else ``$NAS_DATA_ROOT/PEMS`` (exported by
``pilot/env.sh``: the ``all_datasets`` tree next to the ``nas/`` tree), else the legacy ``~/scratch/all_datasets/PEMS``; a horizon
is a benchmark yaml ``experiments/configs/benchmark/<benchmark_dir>/<dataset>_<horizon>.yaml`` .

    python -m pilot.datasets --list            # one line per dataset with the files that exist
    python -m pilot.datasets --list --verify   # also open every .npz and compare its node count with the registry
    python -m pilot.datasets --clock           # the clock of every file: whole days, and the time stamps where a source has them

The clock.  No .npz holds a time stamp; the loader counts the clock from the row position.  A file with rows absent has every
later time feature behind the clock of the data.  ``absent_rows`` of a dataset lists its holes as (first row after the hole,
absent rows); ``stamps`` names an HDF5 source file with the time stamps, against which ``--clock`` checks the list.
pilot.data repairs the time features from ``absent_rows``.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO / "experiments" / "configs"
DATA_ROOT = Path(os.environ.get("PILOT_DATA_ROOT")
                 or (os.path.join(os.environ["NAS_DATA_ROOT"], "PEMS") if os.environ.get("NAS_DATA_ROOT") else "~/scratch/all_datasets/PEMS")).expanduser()
DEFAULT_DATASET = "pems04"
DEFAULT_HORIZON = 12

# relative paths are under DATA_ROOT; absolute or ~ paths are taken as given; None = no such source for this dataset
DATASETS = {
    "pems04": {"benchmark_dir": "PEMS/pems04", "file_name": "PEMS04.npz", "distance_csv": "PEMS04.csv",
               "adj_pickle": "adj_PEMS04.pkl", "n_nodes": 307},
    "pems08": {"benchmark_dir": "PEMS/pems08", "file_name": "PEMS08.npz", "distance_csv": "PEMS08.csv",
               "adj_pickle": "adj_PEMS08.pkl", "n_nodes": 170},
    # METR-LA: DCRNN adj_mx.pkl = [sensor_ids, id2idx, adj] (207 x 207, Gaussian-kernel weights, thresholded, directed, self-loops);
    # its distance list uses the real sensor ids, so the adjacency is built from the pickle, not from a 0..n-1 csv
    # (files fetched from github.com/liyaguang/DCRNN/data/sensor_graph into DATA_ROOT).
    "metrla": {"benchmark_dir": "PEMS/metrla", "file_name": "METR-LA.npz", "distance_csv": None,
               "adj_pickle": "adj_METR-LA.pkl", "sensor_ids": "metrla_graph_sensor_ids.txt", "stamps": "METR-LA.h5",
               "raw_distances": "metrla_distances_la_2012.csv", "n_nodes": 207},
    # Candidate cities of the shared-list benchmark (statistics first, roots only if chosen).  PEMS03's distance list uses the
    # real sensor ids (PEMS03.txt gives the order); PEMS07 ships a ready 883 x 883 adjacency pickle.
    "pems03": {"benchmark_dir": "PEMS/pems03", "file_name": "PEMS03.npz", "distance_csv": None,
               "adj_pickle": None, "sensor_ids": "PEMS03.txt", "raw_distances": "PEMS03_distances.csv", "n_nodes": 358},
    "pems07": {"benchmark_dir": "PEMS/pems07", "file_name": "PEMS07.npz", "distance_csv": None,
               "adj_pickle": "adj_PEMS07.pkl", "n_nodes": 883},
    # PEMS-BAY: one hour is absent (the change to summer time); every later row is 12 steps behind the clock of the data.
    "pemsbay": {"benchmark_dir": "PEMS/pemsbay", "file_name": "PEMS-BAY.npz", "distance_csv": None,
                "stamps": "PEMS-BAY.h5", "absent_rows": [(20184, 12)],
                "adj_pickle": "adj_mx_bay.pkl", "sensor_ids": "PEMS-BAY_sensor_ids.txt", "raw_distances": "bay_distances.csv", "n_nodes": 325},
    # Non-California candidates, prepared by pilot.prepare_city (10-minute steps; speed).
    "chengdu": {"benchmark_dir": "PEMS/chengdu", "file_name": "CHENGDU.npz", "distance_csv": None,
                "adj_pickle": "adj_CHENGDU.pkl", "n_nodes": 524},
    "shenzhen": {"benchmark_dir": "PEMS/shenzhen", "file_name": "SHENZHEN.npz", "distance_csv": None,
                 "adj_pickle": "adj_SHENZHEN.pkl", "n_nodes": 627},
    "expytky": {"benchmark_dir": "PEMS/expytky", "file_name": "EXPYTKY.npz", "distance_csv": None,
                "adj_pickle": "adj_EXPYTKY.pkl", "sensor_ids": "EXPYTKY_link_ids.txt", "n_nodes": 1843},
    # LargeST 2019 flow at 15-minute steps, prepared by pilot.spatialgate_root (sensors with no training data dropped).
    "largestsd": {"benchmark_dir": "PEMS/largestsd", "file_name": "LARGESTSD.npz", "distance_csv": None,
                  "adj_pickle": "adj_LARGESTSD.pkl", "n_nodes": 705},
    "largestgla": {"benchmark_dir": "PEMS/largestgla", "file_name": "LARGESTGLA.npz", "distance_csv": None,
                   "adj_pickle": "adj_LARGESTGLA.pkl", "n_nodes": 3805},
}
_BENCH_RE = re.compile(r"^(?P<dataset>[a-z0-9]+)_(?P<horizon>\d+)$")


def info(dataset: str) -> dict:
    if dataset not in DATASETS:
        raise KeyError(f"unknown dataset {dataset!r}; known {sorted(DATASETS)}")
    return DATASETS[dataset]


def _resolve(p: str | None) -> Path | None:
    if p is None:
        return None
    p = Path(p).expanduser()
    return p if p.is_absolute() else DATA_ROOT / p


def n_nodes(dataset: str) -> int:
    return int(info(dataset)["n_nodes"])


def npz_path(dataset: str) -> Path:
    return _resolve(info(dataset)["file_name"])


def distance_csv_path(dataset: str) -> Path | None:
    return _resolve(info(dataset)["distance_csv"])


def adj_pickle_path(dataset: str) -> Path | None:
    return _resolve(info(dataset)["adj_pickle"])


def benchmark_for(dataset: str, horizon: int) -> str:
    """Hydra benchmark name, e.g. ('pems04', 36) -> 'PEMS/pems04/pems04_36'."""
    return f"{info(dataset)['benchmark_dir']}/{dataset}_{int(horizon)}"


def benchmark_yaml(dataset: str, horizon: int) -> Path:
    return CONFIG_DIR / "benchmark" / f"{benchmark_for(dataset, horizon)}.yaml"


def available_horizons(dataset: str) -> list[int]:
    d = CONFIG_DIR / "benchmark" / info(dataset)["benchmark_dir"]
    out = []
    for f in d.glob(f"{dataset}_*.yaml"):
        m = _BENCH_RE.match(f.stem)
        if m:
            out.append(int(m["horizon"]))
    return sorted(out)


def setting_from_benchmark_name(name: str) -> tuple[str, int]:
    """'pems04_12' (cfg.benchmark.name, also dims['benchmark']) -> ('pems04', 12)."""
    m = _BENCH_RE.match(name)
    if not m or m["dataset"] not in DATASETS:
        raise ValueError(f"benchmark name {name!r} is not <dataset>_<horizon> for a registered dataset")
    return m["dataset"], int(m["horizon"])


def files_status(dataset: str) -> dict:
    """Which of the dataset's sources exist on this machine."""
    d = info(dataset)
    return {
        "npz": npz_path(dataset), "npz_exists": npz_path(dataset).exists(),
        "distance_csv": distance_csv_path(dataset),
        "distance_csv_exists": bool(distance_csv_path(dataset) and distance_csv_path(dataset).exists()),
        "adj_pickle": adj_pickle_path(dataset),
        "adj_pickle_exists": bool(adj_pickle_path(dataset) and adj_pickle_path(dataset).exists()),
        "horizons": available_horizons(dataset), "n_nodes": d["n_nodes"],
    }


def verify_npz(dataset: str) -> dict:
    """Open the .npz and report (T, N, F) against the registry's n_nodes."""
    import numpy as np

    shape = tuple(int(v) for v in np.load(npz_path(dataset))["data"].shape)
    return {"shape": shape, "n_nodes_match": len(shape) >= 2 and shape[1] == n_nodes(dataset)}


def absent_rows(dataset: str) -> list[tuple[int, int]]:
    """Holes of the file as (first row after the hole, absent rows); [] = the row position is the clock."""
    return [(int(a), int(k)) for a, k in info(dataset).get("absent_rows", [])]


def freq_of(dataset: str) -> str:
    """The step of the benchmark file ('5min'), from its base yaml."""
    info(dataset)
    f = CONFIG_DIR / "benchmark" / "PEMS" / f"{dataset}_base.yaml"
    m = re.search(r"^freq:\s*['\"]?(\w+)", f.read_text(), re.M) if f.exists() else None
    if m:
        return m[1]
    raise KeyError(f"no freq in the benchmark yaml files of {dataset}")


def stamp_holes(dataset: str) -> list[tuple[int, int]] | None:
    """Holes read from the time stamps of the HDF5 source (pandas fixed format: <group>/axis1); None = no such source here."""
    import h5py
    import numpy as np

    p = _resolve(info(dataset).get("stamps"))
    if p is None or not p.exists():
        return None
    with h5py.File(p, "r") as f:
        t = np.asarray(f[list(f.keys())[0]]["axis1"][:], dtype=np.int64)
    d = np.diff(t)
    step = int(np.bincount((d // d.min()).astype(np.int64)).argmax()) * int(d.min())
    return [(int(i) + 1, int(d[i] // step) - 1) for i in np.nonzero(d != step)[0]]


def clock_check(dataset: str) -> dict:
    """Rows of the file against whole days, and the registered holes against the time stamps."""
    import numpy as np
    import pandas as pd

    rows = int(np.load(npz_path(dataset), mmap_mode="r")["data"].shape[0])
    per_day = int(pd.Timedelta(days=1) / pd.Timedelta(freq_of(dataset)))
    holes = absent_rows(dataset)
    stamps = stamp_holes(dataset)
    return {"rows": rows, "steps_per_day": per_day, "absent_rows": holes, "stamp_holes": stamps,
            "whole_days": (rows + sum(k for _, k in holes)) % per_day == 0,
            "stamps_agree": None if stamps is None else stamps == holes}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="pilot dataset registry")
    ap.add_argument("--clock", action="store_true", help="check the clock of every file that exists")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--verify", action="store_true", help="with --list: open every .npz and check its node count")
    args = ap.parse_args(argv)
    if args.clock:
        rc = 0
        for ds in DATASETS:
            if not npz_path(ds).exists():
                print(f"{ds:11s} no file")
                continue
            c = clock_check(ds)
            ok = c["whole_days"] and c["stamps_agree"] is not False
            rc |= 0 if ok else 1
            print(f"{ds:11s} rows {c['rows']:6d}  steps per day {c['steps_per_day']:4d}  days {(c['rows'] + sum(k for _, k in c['absent_rows'])) / c['steps_per_day']:.2f}  "
                  f"absent rows {c['absent_rows'] or 'none'}  time stamps {'no source' if c['stamp_holes'] is None else c['stamp_holes'] or 'no hole'}  "
                  f"{'ok' if ok else 'FAIL'}")
        return rc
    if not args.list:
        ap.print_help()
        return 0
    print(f"data root: {DATA_ROOT}")
    rc = 0
    for ds in DATASETS:
        st = files_status(ds)
        flag = lambda b: "ok" if b else "MISSING"  # noqa: E731
        line = (f"{ds:7s} n_nodes={st['n_nodes']:<4d} horizons={st['horizons']}  npz {flag(st['npz_exists'])} ({st['npz']})  "
                f"distance_csv {flag(st['distance_csv_exists']) if st['distance_csv'] else 'n/a'}  "
                f"adj_pickle {flag(st['adj_pickle_exists'])} ({st['adj_pickle']})")
        if args.verify and st["npz_exists"]:
            v = verify_npz(ds)
            line += f"  npz shape {v['shape']} node count {'ok' if v['n_nodes_match'] else 'MISMATCH'}"
            rc |= 0 if v["n_nodes_match"] else 1
        print(line)
        rc |= 0 if (st["npz_exists"] and st["horizons"]) else 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
