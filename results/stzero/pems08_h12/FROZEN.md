# FROZEN: results/stzero/pems08_h12 — 150 architectures on PEMS08, horizon 12

- Sampler: `python -m pilot.sample_archs --root results/stzero/pems08_h12 --n 150 --seed 2028 --space dartsts_graph_v1 --stratify` (`random.Random(2028)`, edges_per_node 2; quotas scaled from 16/10/10/6/8 to 48/30/30/18/24). Same genotype space as the PEMS04 sets; only `d_output` (170 sensors) and the adjacency differ.
- sha1 of `archs.jsonl` (150 lines): `16aee65905cf6ae76f69c3ba98cbd4491a0cf21c`.
- Setting: `PEMS/pems08/pems08_12` (`PEMS08.npz`, 17856 x 170 x 3, flow; window 96, horizon 12, 60/20/20 splits, normalisation as PEMS04).
- Adjacency: `data/pems08_adj.npy` from `PEMS08.csv` (ids 0-169, 295 rows) via `pilot.adjacency --root results/stzero/pems08_h12 --perms 8 --cross-check adj_PEMS08.pkl`; 8 degree-preserving permutations, seed 0. Node order checked with `pilot.adj_sanity` (`tables/adj_sanity.json`).
- Probe batch: `data/pems08_probe_batch.pt` (seed 0, 4 train batches of 32; sha1 in `data/pems08_probe_batch.json`).
- Ground-truth schedule and proxy protocol: unchanged from PEMS04 h12 (batch 32, 20 epochs, patience 5, min 8 on val_mae; init seeds 0/1/2); seed 0 for all 150, seeds 1 and 2 for the first 5 arch_ids.

## TFAS probe

- tfas: not applicable — TFAS not usable as a distinct proxy: its score is ZiCo on Conv/Linear/Conv1d weights; the time-frequency awareness is an input augmentation (STL residual, |FFT|, Haar DWT) implemented only by its own TimesNet-family backbones. Composite temporal term = base proxy. Degenerate value stored as tfas_zico_cl. (TFAS commit `fd9150d`)

## Archive

- Archive: `$NAS_ROOT/backups/stzero.tgz` and `~/scratch/backups/stzero.tgz` (the whole `results/stzero/` tree incl. checkpoints of all four roots; size and sha1 in `results/stzero/compare/COMPARE.md`'s archive line).
- Everything except checkpoints and raw per-run JSONs is in git: `archs.jsonl`, `FROZEN.md`, `DECISION.md` (probe roots), `tables/*.md`, `tables/*.csv`, `figs/*.png` of every root, plus `results/stzero/pems04_h12/tables_n50`, `results/stzero/pems04_h12/figs_n50`, `results/stzero/compare/tables`, `results/stzero/compare/figs`, `results/stzero/compare/COMPARE.md`.
- The gates extend, scale, compare and archive PASS at this commit (`python -m pilot.check --check <gate> --root <root> --n <N>`); roots and probe are point-in-time gates (see the DECISION.md files).
