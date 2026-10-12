"""Result-tree layout.  One experiment holds one root per (dataset, horizon) setting plus a compare/ directory:

    results/<experiment>/<dataset>_h<horizon>/   e.g. results/stzero/pems04_h12, results/stzero/pems08_h12
    results/<experiment>/compare/                 tables and figures that put several settings side by side

    <root>/archs.jsonl  archs/  data/<ds>_probe_batch.pt  data/<ds>_adj.npy  data/<ds>_adj_perm_<j>.npy
    <root>/proxies/v1  proxies/spatial_v2  train/  tables/  figs/  FROZEN.md  RESULTS.md  DECISION.md

Every script takes ``--root`` (plus optional ``--dataset`` / ``--horizon`` overrides) and derives its defaults from it;
explicit path arguments still win.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from pilot.datasets import DEFAULT_DATASET, DEFAULT_HORIZON, benchmark_for, setting_from_benchmark_name

DEFAULT_BASE = "results/stzero"
DEFAULT_ROOT = f"{DEFAULT_BASE}/pems04_h12"
COMPARE_DIR = f"{DEFAULT_BASE}/compare"
_SETTING_RE = re.compile(r"^(?P<dataset>[a-z0-9]+)_h(?P<horizon>\d+)$")


class Root:
    def __init__(self, root_dir: str | Path = DEFAULT_ROOT, dataset: str | None = None, horizon: int | None = None,
                 tables: str | None = None):
        self.dir = Path(root_dir)
        self.tables_name = tables or "tables"  # e.g. "tables_n150": the tables of a subset of the root's architectures
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
    def for_setting(cls, dataset: str, horizon: int, base: str | Path = DEFAULT_BASE) -> "Root":
        """The conventional root of a setting: ``base/<ds>_h<h>``."""
        return cls(Path(base) / f"{dataset}_h{int(horizon)}", dataset, horizon)

    @classmethod
    def from_tables_dir(cls, path: str | Path) -> "Root":
        """A root given either as its directory or as one of its tables directories (``<root>/tables_n150``)."""
        p = Path(path)
        if p.name.startswith("tables"):
            return cls(p.parent, tables=p.name)
        return cls(p)

    @classmethod
    def for_benchmark_name(cls, name: str, base: str | Path = DEFAULT_BASE) -> "Root":
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
        return self.dir / self.tables_name

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
        extra = f", tables={self.tables_name!r}" if self.tables_name != "tables" else ""
        return f"Root({str(self.dir)!r}, dataset={self.dataset!r}, horizon={self.horizon}{extra})"

    # ---- argparse plumbing
    @staticmethod
    def add_args(ap: argparse.ArgumentParser) -> None:
        ap.add_argument("--root", default=DEFAULT_ROOT, help=f"results root of one (dataset, horizon) setting (default: {DEFAULT_ROOT})")
        ap.add_argument("--dataset", default=None, help="pems04 | pems08 | metrla (default: from the root name or its data/ files)")
        ap.add_argument("--horizon", type=int, default=None, help="forecast horizon (default: from the root name, else 12)")

    @classmethod
    def from_args(cls, args) -> "Root":
        return cls(args.root, getattr(args, "dataset", None), getattr(args, "horizon", None))


def default_adj_for_dims(dims: dict, base: str | Path = DEFAULT_BASE) -> Path:
    """The adjacency file of the setting a probe batch / loader ``dims`` came from (``dims['benchmark']`` = 'pems04_12')."""
    return Root.for_benchmark_name(dims["benchmark"], base).adj
