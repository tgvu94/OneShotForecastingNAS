# FROZEN: results/metrla_h12 — the Pilot 1 frozen 50 on METR-LA, horizon 12 (Pilot 2 Phase 2(b) probe)

Created 2026-09-21. `archs.jsonl` and `archs/` are byte copies of `results/archs.jsonl` / `results/archs/` (the 50 architectures frozen on
2026-09-20, sampler seed 2026, space `dartsts_graph_v1`; see `results/FROZEN.md`). sha1 of `archs.jsonl`: `ed7419b5c2d68eb86f6730b733cbf008aa83d3d7`. The genotypes are dataset-agnostic:
only `d_output` (207 sensors) and the adjacency differ; the AdaptiveAdjOp embeddings are sized by the node count at build time.

- Setting: `PEMS/metrla/metrla_12` (`experiments/configs/benchmark/PEMS/metrla/metrla_12.yaml`): `METR-LA.npz` (34272 x 207 x 1, speed; converted from DCRNN's metr-la.h5), window 96, horizon 12, 60/20/20 splits and normalisation as for PEMS.
- Adjacency: `data/metrla_adj.npy` built with `pilot.adjacency --root results/metrla_h12 --perms 8` from DCRNN's `adj_mx.pkl` (`~/scratch/all_datasets/PEMS/adj_METR-LA.pkl`): an undirected edge wherever the thresholded Gaussian-kernel weight is nonzero in either direction, diagonal dropped (see `data/metrla_adj.json`). This binarisation inherits DCRNN's distance threshold; it is not a raw road-connectivity list like PEMS04.csv. 8 degree-preserving permutations, seed 0.
- Node order: the pickle's sensor ids are in the order of `graph_sensor_ids.txt`, the same order as the h5 columns the `.npz` was converted from (DCRNN convention); checked empirically with `pilot.adj_sanity --root results/metrla_h12` (`tables/adj_sanity.json`).
- Probe batch: `data/metrla_probe_batch.pt` (seed 0, 4 train batches of 32, repo scaler; sha1 in `data/metrla_probe_batch.json`).
- Ground-truth schedule and proxy protocol: unchanged from Pilot 1 (batch 32, 20 epochs, patience 5, min 8 on val_mae; init seeds 0/1/2; `proxies/v1`, `proxies/spatial_v2`).
- Decision rule and verdict: `DECISION.md`, written by `python -m pilot.check --phase 2 --pilot 2 --root results/metrla_h12`.
