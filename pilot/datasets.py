"""Dataset registry (Pilot 2, Phase 1): everything that differs between PEMS04, PEMS08 and METR-LA in one place.

The genotype space is identical across datasets; only the number of sensors (``d_output`` / ``n_nodes``), the data file and
the adjacency source differ.  Raw data lives under ``$PILOT_DATA_ROOT`` (default ``~/scratch/all_datasets/PEMS``); a horizon
is a benchmark yaml ``experiments/configs/benchmark/<benchmark_dir>/<dataset>_<horizon>.yaml`` (the route Pilot 1 used).

    python -m pilot.datasets --list            # one line per dataset with the files that exist
    python -m pilot.datasets --list --verify   # also open every .npz and compare its node count with the registry
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO / "experiments" / "configs"
DATA_ROOT = Path(os.environ.get("PILOT_DATA_ROOT", "~/scratch/all_datasets/PEMS")).expanduser()
DEFAULT_DATASET = "pems04"
DEFAULT_HORIZON = 12

# relative paths are under DATA_ROOT; absolute or ~ paths are taken as given; None = no such source for this dataset
DATASETS = {
    "pems04": {"benchmark_dir": "PEMS/pems04", "file_name": "PEMS04.npz", "distance_csv": "PEMS04.csv",
               "adj_pickle": "adj_PEMS04.pkl", "n_nodes": 307},
    "pems08": {"benchmark_dir": "PEMS/pems08", "file_name": "PEMS08.npz", "distance_csv": "PEMS08.csv",
               "adj_pickle": "adj_PEMS08.pkl", "n_nodes": 170},
    "metrla": {"benchmark_dir": "PEMS/metrla", "file_name": "METR-LA.npz", "distance_csv": None,
               "adj_pickle": "~/nas-traffic/adj_METR-LA.pkl", "n_nodes": 207},
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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="pilot dataset registry")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--verify", action="store_true", help="with --list: open every .npz and check its node count")
    args = ap.parse_args(argv)
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
