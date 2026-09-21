"""Degree-preserving permutations of a root's adjacency (Section 3.4) -> <root>/data/<ds>_adj_perm_{0..k-1}.npy.
Thin CLI over ``pilot.adjacency.degree_preserving_permutations`` (the same files were first produced in Phase 3 by
``python -m pilot.adjacency --perms 8``); re-running with the same seed reproduces the same matrices."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from pilot.adjacency import degree_preserving_permutations, load_adj
from pilot.paths import Root


def main():
    ap = argparse.ArgumentParser()
    Root.add_args(ap)
    ap.add_argument("--adj", default=None, help="default: <root>/data/<dataset>_adj.npy")
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    args.adj = args.adj or Root.from_args(args).adj
    A = load_adj(args.adj)
    out = Path(args.adj)
    m = int(A.sum() // 2)
    rows = []
    for j, P in enumerate(degree_preserving_permutations(A, args.k, args.seed)):
        pf = out.with_name(f"{out.stem}_perm_{j}.npy")
        if pf.exists() and np.array_equal(np.load(pf), P):
            status = "unchanged"
        else:
            np.save(pf, P)
            status = "written"
        shared = int((P * A).sum() // 2)
        rows.append({"file": str(pf), "shared_edges": shared, "frac_changed": 1 - shared / m, "status": status})
        print(f"perm {j}: {status}; edges shared with A {shared}/{m} ({100 * (1 - shared / m):.1f}% changed); degrees preserved: "
              f"{np.array_equal(P.sum(1), A.sum(1))}")
    out.with_name(f"{out.stem}_perms.json").write_text(json.dumps({"seed": args.seed, "k": args.k, "n_edges": m, "perms": rows}, indent=2))


if __name__ == "__main__":
    main()
