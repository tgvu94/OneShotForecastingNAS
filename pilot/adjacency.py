"""PEMS04 adjacency (Section 3.4 / P3): binary symmetric ``A`` from the distance list, GCN normalisation,
diffusion transition matrices, and degree-preserving permutations for Experiment B.

    python -m pilot.adjacency --distance-csv ~/scratch/all_datasets/PEMS/PEMS04.csv --out results/data/pems04_adj.npy \
        --cross-check ~/scratch/all_datasets/PEMS/adj_PEMS04.pkl --perms 8
"""
from __future__ import annotations

import argparse
import csv
import json
import pickle
from pathlib import Path

import numpy as np
import torch

DEFAULT_ADJ = "results/data/pems04_adj.npy"


def load_pems04_adj(distance_csv: str | Path, n: int = 307) -> np.ndarray:
    """Binary, symmetric, zero-diagonal (n, n) float32 matrix from a ``from,to,cost`` list (ids 0..n-1)."""
    A = np.zeros((n, n), dtype=np.float32)
    with open(distance_csv) as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header[:2] == ["from", "to"], header
        for row in reader:
            if len(row) < 2:
                continue
            i, j = int(row[0]), int(row[1])
            if i != j:
                A[i, j] = 1.0
                A[j, i] = 1.0
    return A


def check_adj(A: np.ndarray) -> dict:
    return {"shape": list(A.shape), "symmetric": bool(np.array_equal(A, A.T)), "binary": bool(set(np.unique(A)) <= {0.0, 1.0}),
            "zero_diag": bool((np.diag(A) == 0).all()), "n_undirected_edges": int(A.sum() // 2),
            "isolated_nodes": int((A.sum(1) == 0).sum()), "max_degree": int(A.sum(1).max())}


def normalize_gcn(A: np.ndarray) -> np.ndarray:
    """D^-1/2 (A + I) D^-1/2 (Kipf & Welling)."""
    A_hat = A + np.eye(A.shape[0], dtype=A.dtype)
    d = A_hat.sum(1)
    d_inv_sqrt = np.where(d > 0, 1.0 / np.sqrt(d), 0.0).astype(A.dtype)
    return (d_inv_sqrt[:, None] * A_hat * d_inv_sqrt[None, :]).astype(np.float32)


def transition_matrices(A: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(D_out^-1 A, D_in^-1 A^T): forward and backward random-walk matrices (DCRNN / Graph WaveNet)."""
    def rw(M):
        d = M.sum(1)
        d_inv = np.where(d > 0, 1.0 / d, 0.0).astype(M.dtype)
        return (d_inv[:, None] * M).astype(np.float32)
    return rw(A), rw(A.T.copy())


def adj_pack(A: np.ndarray, device=None) -> dict[str, torch.Tensor]:
    """Everything a graph op may need, as float32 tensors: ``A``, ``gcn`` (normalised), ``p_fwd``, ``p_bwd``."""
    p_fwd, p_bwd = transition_matrices(A)
    pack = {"A": A.astype(np.float32), "gcn": normalize_gcn(A), "p_fwd": p_fwd, "p_bwd": p_bwd}
    return {k: torch.from_numpy(np.ascontiguousarray(v)).to(device) if device is not None else torch.from_numpy(np.ascontiguousarray(v))
            for k, v in pack.items()}


def degree_preserving_permutations(A: np.ndarray, k: int = 8, seed: int = 0) -> list[np.ndarray]:
    """Maslov-Sneppen double-edge swaps (Section 3.4): every node keeps its degree, the neighbour sets change."""
    import networkx as nx

    G0 = nx.from_numpy_array(A)
    m = G0.number_of_edges()
    out = []
    for j in range(k):
        G = G0.copy()
        nx.double_edge_swap(G, nswap=10 * m, max_tries=200 * m, seed=seed + j)
        P = nx.to_numpy_array(G, nodelist=range(A.shape[0]), dtype=A.dtype)
        assert np.array_equal(P.sum(1), A.sum(1)) and np.array_equal(P, P.T) and (np.diag(P) == 0).all()
        out.append(P.astype(np.float32))
    return out


def load_adj(path: str | Path = DEFAULT_ADJ) -> np.ndarray:
    return np.load(path).astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--distance-csv", required=True)
    ap.add_argument("--n", type=int, default=307)
    ap.add_argument("--out", default=DEFAULT_ADJ)
    ap.add_argument("--cross-check", default=None, help="adj_PEMS04.pkl (ndarray) to compare against")
    ap.add_argument("--perms", type=int, default=8)
    ap.add_argument("--perm-seed", type=int, default=0)
    args = ap.parse_args()

    A = load_pems04_adj(args.distance_csv, args.n)
    info = check_adj(A)
    print("A:", json.dumps(info))
    if args.cross_check:
        ref = pickle.load(open(args.cross_check, "rb"), encoding="latin1")
        ref = np.asarray(ref[-1] if isinstance(ref, (list, tuple)) else ref, dtype=np.float32)
        ref_sym = np.maximum(ref, ref.T)
        np.fill_diagonal(ref_sym, 0)
        info["matches_pickle_after_symmetrization"] = bool(np.array_equal((ref_sym > 0).astype(np.float32), A))
        info["pickle_nnz"] = int((ref != 0).sum())
        print("cross-check:", info["matches_pickle_after_symmetrization"], "pickle nnz", info["pickle_nnz"])
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.save(out, A)
    perm_files = []
    if args.perms:
        for j, P in enumerate(degree_preserving_permutations(A, args.perms, args.perm_seed)):
            pf = out.with_name(f"{out.stem}_perm_{j}.npy")
            np.save(pf, P)
            perm_files.append(str(pf))
            same = int((P * A).sum() // 2)
            print(f"perm {j}: {pf}  edges shared with A: {same}/{info['n_undirected_edges']}")
    info.update({"source": str(args.distance_csv), "out": str(out), "perm_files": perm_files, "perm_seed": args.perm_seed})
    out.with_suffix(".json").write_text(json.dumps(info, indent=2))
    print("saved", out)


if __name__ == "__main__":
    main()
