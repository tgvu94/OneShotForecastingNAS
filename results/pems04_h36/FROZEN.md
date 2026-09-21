# FROZEN: results/pems04_h36 — the Pilot 1 frozen 50 at horizon 36 (Pilot 2 Phase 2 probe)

Created 2026-09-21. `archs.jsonl` and `archs/` are byte copies of `results/archs.jsonl` / `results/archs/` (the 50 architectures frozen
on 2026-09-20, sampler seed 2026, space `dartsts_graph_v1`; see `results/FROZEN.md`). sha1 of `archs.jsonl`: `ed7419b5c2d68eb86f6730b733cbf008aa83d3d7`.

- Setting: `PEMS/pems04/pems04_36` (`experiments/configs/benchmark/PEMS/pems04/pems04_36.yaml`): window 96, horizon 36 (3 h), same data file, splits and normalisation as h12.
- Adjacency: `data/pems04_adj.npy` and `data/pems04_adj_perm_0..7.npy` rebuilt with the same commands and seeds; verified identical to the Pilot 1 files.
- Probe batch: `data/pems04_probe_batch.pt` (seed 0, 4 train batches of 32, repo scaler) — new file, x_future / target now have 36 steps (sha1 in `data/pems04_probe_batch.json`).
- Ground-truth schedule: unchanged from Pilot 1 (batch 32, 20 epochs, patience 5, min 8 on val_mae, repo eval optimiser, AMP); seed 0 for all 50, seeds 1 and 2 for the first 5 arch_ids.
- Proxy protocol: unchanged (init seeds 0/1/2, cudnn deterministic; `proxies/v1`, `proxies/spatial_v2` with the 8 permutations).
- Decision rule and verdict: `DECISION.md`, written by `python -m pilot.check --phase 2 --pilot 2 --root results/pems04_h36`.

## TFAS (Phase 7 probe, 2026-09-21)

- tfas: not applicable — TFAS not usable as a distinct proxy: its score is ZiCo on Conv/Linear/Conv1d weights; the time-frequency awareness is an input augmentation (STL residual, |FFT|, Haar DWT) implemented only by its own TimesNet-family backbones. Composite temporal term = base proxy. Degenerate value stored as tfas_zico_cl. (TFAS commit `fd9150d`)
