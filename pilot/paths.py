"""Result-tree layout (Pilot 2, Phase 1).  Every (dataset, horizon) setting has one root with the Pilot 1 layout:

    results/                        PEMS04 horizon 12 -- the Pilot 1 tree, unchanged
    results/<dataset>_h<horizon>/   every other setting, e.g. results/pems04_h36, results/pems08_h12

    <root>/archs.jsonl  archs/  data/<ds>_probe_batch.pt  data/<ds>_adj.npy  data/<ds>_adj_perm_<j>.npy
    <root>/proxies/v1  proxies/spatial_v2  train/  tables/  figs/  FROZEN.md  RESULTS.md  DECISION.md

Every script takes ``--root`` (plus optional ``--dataset`` / ``--horizon`` overrides) and derives its defaults from it;
explicit path arguments still win, so every Pilot 1 command line keeps working.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from pilot.datasets import DEFAULT_DATASET, DEFAULT_HORIZON, benchmark_for, setting_from_benchmark_name

DEFAULT_ROOT = "results"
_SETTING_RE = re.compile(r"^(?P<dataset>[a-z0-9]+)_h(?P<horizon>\d+)$")


class Root:
    def __init__(self, root_dir: str | Path = DEFAULT_ROOT, dataset: str | None = None, horizon: int | None = None):
        self.dir = Path(root_dir)
        m = _SETTING_RE.match(self.dir.name)
        self.dataset = dataset or (m["dataset"] if m else self._infer_dataset())
        self.horizon = int(horizon if horizon is not None else (m["horizon"] if m else DEFAULT_HORIZON))

    def _infer_dataset(self) -> str:
        for pat in ("*_adj.npy", "*_probe_batch.pt"):
            hits = sorted(self.data.glob(pat))
            if hits:
                return hits[0].name.split("_")[0]
        return DEFAULT_DATASET

    @classmethod
    def for_setting(cls, dataset: str, horizon: int, base: str | Path = DEFAULT_ROOT) -> "Root":
        """The conventional root of a setting: ``base`` itself for (pems04, 12), ``base/<ds>_h<h>`` otherwise."""
        if dataset == DEFAULT_DATASET and int(horizon) == DEFAULT_HORIZON:
            return cls(base, dataset, horizon)
        return cls(Path(base) / f"{dataset}_h{int(horizon)}", dataset, horizon)

    @classmethod
    def for_benchmark_name(cls, name: str, base: str | Path = DEFAULT_ROOT) -> "Root":
        """From ``cfg.benchmark.name`` / ``dims['benchmark']`` such as 'pems04_36'."""
        return cls.for_setting(*setting_from_benchmark_name(name), base=base)

    # ---- derived names
    @property
    def benchmark(self) -> str:
        return benchmark_for(self.dataset, self.horizon)

    @property
    def label(self) -> str:
        return f"{self.dataset.upper()}-{self.horizon}"

    @property
    def archs_jsonl(self) -> Path:
        return self.dir / "archs.jsonl"

    @property
    def archs_dir(self) -> Path:
        return self.dir / "archs"

    @property
    def data(self) -> Path:
        return self.dir / "data"

    @property
    def probe(self) -> Path:
        return self.data / f"{self.dataset}_probe_batch.pt"

    @property
    def adj(self) -> Path:
        return self.data / f"{self.dataset}_adj.npy"

    def adj_perms(self) -> list[Path]:
        return sorted(self.data.glob(f"{self.dataset}_adj_perm_*.npy"))

    @property
    def proxies_v1(self) -> Path:
        return self.dir / "proxies" / "v1"

    @property
    def spatial_v2(self) -> Path:
        return self.dir / "proxies" / "spatial_v2"

    @property
    def train(self) -> Path:
        return self.dir / "train"

    @property
    def tables(self) -> Path:
        return self.dir / "tables"

    @property
    def figs(self) -> Path:
        return self.dir / "figs"

    @property
    def frozen_md(self) -> Path:
        return self.dir / "FROZEN.md"

    @property
    def results_md(self) -> Path:
        return self.dir / "RESULTS.md"

    @property
    def decision_md(self) -> Path:
        return self.dir / "DECISION.md"

    @property
    def naive_baselines(self) -> Path:
        return self.tables / "naive_baselines.json"

    @property
    def status_csv(self) -> Path:
        return self.tables / "status.csv"

    def mkdirs(self) -> "Root":
        for d in (self.archs_dir, self.data, self.proxies_v1, self.spatial_v2, self.train, self.tables, self.figs):
            d.mkdir(parents=True, exist_ok=True)
        return self

    def __repr__(self) -> str:
        return f"Root({str(self.dir)!r}, dataset={self.dataset!r}, horizon={self.horizon})"

    # ---- argparse plumbing
    @staticmethod
    def add_args(ap: argparse.ArgumentParser) -> None:
        ap.add_argument("--root", default=DEFAULT_ROOT, help="results root of one (dataset, horizon) setting (default: results)")
        ap.add_argument("--dataset", default=None, help="pems04 | pems08 | metrla (default: from the root name or its data/ files)")
        ap.add_argument("--horizon", type=int, default=None, help="forecast horizon (default: from the root name, else 12)")

    @classmethod
    def from_args(cls, args) -> "Root":
        return cls(args.root, getattr(args, "dataset", None), getattr(args, "horizon", None))


def default_adj_for_dims(dims: dict, base: str | Path = DEFAULT_ROOT) -> Path:
    """The adjacency file of the setting a probe batch / loader ``dims`` came from (``dims['benchmark']`` = 'pems04_12')."""
    return Root.for_benchmark_name(dims["benchmark"], base).adj
