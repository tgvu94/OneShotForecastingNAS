# FROZEN: results/pems08_h12 — 150 architectures on PEMS08, horizon 12 (Pilot 2 Phase 3)

Created 2026-09-22 at fork commit `0d8e732`.

- Sampler: `python -m pilot.sample_archs --root results/pems08_h12 --n 150 --seed 2028 --space dartsts_graph_v1 --stratify` (`random.Random(2028)`, edges_per_node 2; quotas scaled from 16/10/10/6/8 to 48/30/30/18/24). Same genotype space as the PEMS04 sets; only `d_output` (170 sensors) and the adjacency differ.
- sha1 of `archs.jsonl` (150 lines): `d8b13b5d58355c25965e80fe144e74c442f17b83`.
- Setting: `PEMS/pems08/pems08_12` (`PEMS08.npz`, 17856 x 170 x 3, flow; window 96, horizon 12, 60/20/20 splits, normalisation as PEMS04).
- Adjacency: `data/pems08_adj.npy` from `PEMS08.csv` (ids 0-169, 295 rows) via `pilot.adjacency --root results/pems08_h12 --perms 8 --cross-check adj_PEMS08.pkl`; 8 degree-preserving permutations, seed 0. Node order checked with `pilot.adj_sanity` (`tables/adj_sanity.json`).
- Probe batch: `data/pems08_probe_batch.pt` (seed 0, 4 train batches of 32; sha1 in `data/pems08_probe_batch.json`).
- Ground-truth schedule and proxy protocol: unchanged from Pilot 1 (batch 32, 20 epochs, patience 5, min 8 on val_mae; init seeds 0/1/2); seed 0 for all 150, seeds 1 and 2 for the first 5 arch_ids.

## TFAS (Phase 7 probe, 2026-09-24)

- tfas: not applicable — TFAS not usable as a distinct proxy: its score is ZiCo on Conv/Linear/Conv1d weights; the time-frequency awareness is an input augmentation (STL residual, |FFT|, Haar DWT) implemented only by its own TimesNet-family backbones. Composite temporal term = base proxy. Degenerate value stored as tfas_zico_cl. (TFAS commit `fd9150d`)

## Archive (Pilot 2 Phase 6, 2026-09-24)

- Pilot 2 archive: `$NAS_ROOT/backups/results-pilot2.tgz` and `~/scratch/backups/results-pilot2.tgz` (the whole `results/` tree incl. checkpoints of all four roots; size and sha1 in `results/RESULTS_pilot2.md`'s archive line and in `pilot2-results.md`), made at fork commit `3b42d35` after the Phase 5 outputs.
- Everything except checkpoints and raw per-run JSONs is in git on `tgvu94/OneShotForecastingNAS:graph-ops`: `archs.jsonl`, `FROZEN.md`, `DECISION.md` (probe roots), `tables/*.md`, `tables/*.csv`, `figs/*.png` of every root, plus `results/tables_n50`, `results/figs_n50`, `results/tables_pilot2`, `results/figs_pilot2`, `results/RESULTS_pilot2.md`.
- Pilot 2 phase checks 3, 4, 5, 6 PASS at this commit (`python -m pilot.check --phase N --pilot 2 --root <root> --n <N>`); phases 1 and 2 are point-in-time gates (see `pilot2-results.md`).
