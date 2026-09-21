"""Risk-ladder sanity check for the node ordering of A vs the .npz series: the highest-degree sensors in A should have flow
series more correlated with their A-neighbours than with random non-neighbours.  CPU, seconds."""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

from pilot import datasets
from pilot.adjacency import load_adj
from pilot.paths import Root


def main():
    ap = argparse.ArgumentParser()
    Root.add_args(ap)
    ap.add_argument("--npz", default=None, help="default: the root's dataset .npz under $PILOT_DATA_ROOT")
    ap.add_argument("--adj", default=None, help="default: <root>/data/<dataset>_adj.npy")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--out", default=None, help="default: <root>/tables/adj_sanity.json")
    args = ap.parse_args()
    root = Root.from_args(args)
    args.npz = args.npz or os.fspath(datasets.npz_path(root.dataset))
    args.adj = args.adj or root.adj
    args.out = args.out or root.tables / "adj_sanity.json"
    A = load_adj(args.adj)
    x = np.load(args.npz)["data"][:, :, 0].astype(np.float64)  # (T, N) flow
    C = np.corrcoef(x.T)
    deg = A.sum(1)
    rng = np.random.default_rng(0)
    rows, nb_all, rn_all = [], [], []
    for i in np.argsort(-deg)[: args.top]:
        nb = np.where(A[i] > 0)[0]
        non = np.setdiff1d(np.arange(A.shape[0]), np.append(nb, i))
        rn = rng.choice(non, size=len(nb), replace=False)
        rows.append({"sensor": int(i), "degree": int(deg[i]), "mean_corr_neighbours": float(np.mean(C[i, nb])),
                     "mean_corr_random": float(np.mean(C[i, rn]))})
        nb_all += list(C[i, nb]); rn_all += list(C[i, rn])
    # all edges vs all non-edges
    iu = np.triu_indices(A.shape[0], 1)
    edge_corr = C[iu][A[iu] > 0]
    non_corr = C[iu][A[iu] == 0]
    res = {"top_sensors": rows, "top_mean_neighbour_corr": float(np.mean(nb_all)), "top_mean_random_corr": float(np.mean(rn_all)),
           "all_edges_mean_corr": float(edge_corr.mean()), "all_nonedges_mean_corr": float(non_corr.mean()),
           "all_edges_median_corr": float(np.median(edge_corr)), "all_nonedges_median_corr": float(np.median(non_corr)),
           "n_edges": int(len(edge_corr)), "ordering_consistent": bool(np.mean(nb_all) > np.mean(rn_all) and edge_corr.mean() > non_corr.mean())}
    json.dump(res, open(args.out, "w"), indent=2)
    print(json.dumps({k: v for k, v in res.items() if k != "top_sensors"}, indent=1))
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
