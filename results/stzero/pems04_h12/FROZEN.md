# FROZEN: results/stzero/pems04_h12 — the frozen architectures on PEMS04, horizon 12

The first 50 architectures were frozen when the gate passed: best dev graph arch val MAE 0.1688 <= 1.10 x 0.1722, the best graph-blind reference arch.

- Sampler: `python -m pilot.sample_archs --n 50 --seed 2026 --space dartsts_graph_v1 --stratify --out results/stzero/pems04_h12/archs.jsonl --overwrite`
- Space: `dartsts_graph_v1` = DARTS-TS `mixed_concat_darts.yaml` operators (seq: 2 cells x 4 nodes, d_model 32; flat: 2 cells x 4 nodes) + graph cell (1 cell x 4 nodes x 1 input node, C = 32, ops graph_identity / gcn / diffusion(K=2) / adaptive); 2 incoming edges per node; the seq decoder shares the encoder topology
- Sampling seed: 2026 (`random.Random`), edges_per_node 2; 50 architectures, 50 distinct arch_ids
- Strata: {'none': 16, 'gcn': 10, 'diffusion': 10, 'any_graph': 8, 'control': 6}
- graph_family counts: {'none': 16, 'gcn': 3, 'mixed': 16, 'diffusion': 9, 'adaptive-only': 5, 'identity-only': 1} -> 19 contain gcn, 25 contain diffusion, 6 adaptive/identity-only controls (S_spatial = 0 by construction), 16 graph-blind
- heads: {'mae': 14, 'quantile': 16, 'mse': 20}; seq decoders: {'linear': 24, 'seq': 26}
- Adjacency: `data/pems04_adj.npy` (from PEMS04.csv, 307 nodes, 340 undirected edges); permutations `data/pems04_adj_perm_0..7.npy` (double-edge swaps, seed 0)
- Ground-truth schedule: PEMS/pems04/pems04_12, batch 32, 20 epochs, patience 5 (min 8) on val_mae, repo eval optimiser (Adam 1e-3, wd 0, CosineAnnealingWarmRestarts T_0 = 20, eta_min 1e-8, grad clip 0.1, AMP, TargetScaler standard); seed 0 for all 50, seeds 1 and 2 additionally for the first 5 arch_ids of this file
- Proxy protocol: probe batch `data/pems04_probe_batch.pt` (sha1 32cb8208...), init seeds 0/1/2, cudnn deterministic; stored under `proxies/v1/`
- Not part of the 50: the five graph-blind reference archs (`archs_graphblind.jsonl`, space dartsts_v1; timing / seed-noise data) and the dev archs (`archs_dev.jsonl`, seed 100; gate data)

## TFAS probe

- tfas: not applicable — TFAS not usable as a distinct proxy: its score is ZiCo on Conv/Linear/Conv1d weights; the time-frequency awareness is an input augmentation (STL residual, |FFT|, Haar DWT) implemented only by its own TimesNet-family backbones. Composite temporal term = base proxy. Degenerate value stored as tfas_zico_cl. (TFAS commit `fd9150d`)

## Archive at N = 50

- Archive: `$NAS_ROOT/backups/stzero-n50.tgz` and `~/scratch/backups/stzero-n50.tgz` (820 MB, sha1 800ebe661db4).
- Everything except checkpoints and raw per-run JSONs is also in git: `archs.jsonl`, `archs_graphblind.jsonl`, `archs_dev.jsonl`, `FROZEN.md`, `RESULTS.md`, `autocts_precheck.*`, `tables_n50/`, `figs_n50/`.
- The gates smoke to report all PASS at that point (`python -m pilot.check --check <gate>`).

## The frozen 50 as a block

- sha1 of the first 50 lines of `archs.jsonl` (unchanged since the freeze): `459b1db47a878f2c05a5023cc18e86bf20d19dbd`. Used by the gates; `results/stzero/pems04_h36/archs.jsonl` and `results/stzero/metrla_h12/archs.jsonl` are byte copies.

## Extension to 300

- Lines 1-50: the frozen 50, unchanged (sha1 of those 50 lines: `459b1db47a878f2c05a5023cc18e86bf20d19dbd`).
- Lines 51-300: 250 new architectures, `python -m pilot.sample_archs --root results/stzero/pems04_h12 --n 250 --seed 2027 --space dartsts_graph_v1 --stratify`
  (`random.Random(2027)`, edges_per_node 2, de-duplicated against the first 50; quotas scaled from 16/10/10/6/8 to 80/50/50/30/40).
- sha1 of the 300-line file: `58aa67c9c503a4a986bfa452d173e15c4f806276`.
- Setting for the scale-up: PEMS04 h12 (this tree), chosen by the probe decision (graph matters nowhere tested: h12, h36, METR-LA).

## Archive at N = 300

- Archive: `$NAS_ROOT/backups/stzero.tgz` and `~/scratch/backups/stzero.tgz` (the whole `results/stzero/` tree incl. checkpoints of all four roots; size and sha1 in `results/stzero/compare/COMPARE.md`'s archive line).
- Everything except checkpoints and raw per-run JSONs is in git: `archs.jsonl`, `FROZEN.md`, `DECISION.md` (probe roots), `tables/*.md`, `tables/*.csv`, `figs/*.png` of every root, plus `tables_n50/`, `figs_n50/`, `results/stzero/compare/tables`, `results/stzero/compare/figs`, `results/stzero/compare/COMPARE.md`.
- The gates extend, scale, compare and archive PASS at this commit (`python -m pilot.check --check <gate> --root <root> --n <N>`); roots and probe are point-in-time gates (see the DECISION.md files).
