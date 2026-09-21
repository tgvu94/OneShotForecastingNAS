# FROZEN: the 50 pilot architectures

Frozen on 2026-09-20 (Phase 4 gate passed: best dev graph arch val MAE 0.1688 <= 1.10 x 0.1722, the best P2 graph-blind arch).

- Sampler: `python -m pilot.sample_archs --n 50 --seed 2026 --space dartsts_graph_v1 --stratify --out results/archs.jsonl --overwrite`
- Space: `dartsts_graph_v1` = DARTS-TS `mixed_concat_darts.yaml` operators (seq: 2 cells x 4 nodes, d_model 32; flat: 2 cells x 4 nodes) + graph cell (1 cell x 4 nodes x 1 input node, C = 32, ops graph_identity / gcn / diffusion(K=2) / adaptive); 2 incoming edges per node; the seq decoder shares the encoder topology
- Sampling seed: 2026 (`random.Random`), edges_per_node 2; 50 architectures, 50 distinct arch_ids
- Fork commit of the sampler / space code at freeze time: `518ecec` (tgvu94/OneShotForecastingNAS, branch graph-ops)
- Strata (Section 3.5): {'none': 16, 'gcn': 10, 'diffusion': 10, 'any_graph': 8, 'control': 6}
- graph_family counts: {'none': 16, 'gcn': 3, 'mixed': 16, 'diffusion': 9, 'adaptive-only': 5, 'identity-only': 1} -> 19 contain gcn, 25 contain diffusion, 6 adaptive/identity-only controls (S_spatial = 0 by construction), 16 graph-blind
- heads: {'mae': 14, 'quantile': 16, 'mse': 20}; seq decoders: {'linear': 24, 'seq': 26}
- Adjacency: `results/data/pems04_adj.npy` (from PEMS04.csv, 307 nodes, 340 undirected edges); permutations `results/data/pems04_adj_perm_0..7.npy` (double-edge swaps, seed 0)
- Ground-truth schedule (Section 4.1, confirmed P2): PEMS/pems04/pems04_12, batch 32, 20 epochs, patience 5 (min 8) on val_mae, repo eval optimiser (Adam 1e-3, wd 0, CosineAnnealingWarmRestarts T_0 = 20, eta_min 1e-8, grad clip 0.1, AMP, TargetScaler standard); seed 0 for all 50, seeds 1 and 2 additionally for the first 5 arch_ids of this file
- Proxy protocol (Section 3.3): probe batch `results/data/pems04_probe_batch.pt` (sha1 32cb8208...), init seeds 0/1/2, cudnn deterministic; stored under `results/proxies/v1/`
- Not part of the 50: the P2 five graph-blind archs (`results/archs_p2.jsonl`, space dartsts_v1; timing / seed-noise data) and the P3 dev archs (`results/archs_dev.jsonl`, seed 100; gate data)

## TFAS (Phase 7 probe, 2026-09-21)

- tfas: not applicable — TFAS not usable as a distinct proxy: its score is ZiCo on Conv/Linear/Conv1d weights; the time-frequency awareness is an input augmentation (STL residual, |FFT|, Haar DWT) implemented only by its own TimesNet-family backbones. Composite temporal term = base proxy. Degenerate value stored as tfas_zico_cl. (TFAS commit `fd9150d`)

## Archive (Phase 12, 2026-09-21)

- Final results archive: `~/nas/backups/results-final.tgz` and `~/scratch/backups/results-final.tgz` (820 MB, sha1 800ebe661db4), made at fork commit `b802e16` (`b802e16` = P10).
- Everything except checkpoints and raw per-run JSONs is also in git on `tgvu94/OneShotForecastingNAS:graph-ops`: `results/{archs.jsonl,archs_p2.jsonl,archs_dev.jsonl,FROZEN.md,RESULTS.md,autocts_precheck.*,tables/*.md,tables/*.csv,figs/*.png}`.
- Phase checks 1-10 all PASS at this commit (`python -m pilot.check --phase N`).
