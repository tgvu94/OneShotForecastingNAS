# FROZEN: results/stzero/metrla_h12 — the frozen 50 on METR-LA, horizon 12 (probe)

`archs.jsonl` and `archs/` are byte copies of `results/stzero/pems04_h12/archs.jsonl` / `results/stzero/pems04_h12/archs/` (the 50 architectures frozen with
sampler seed 2026, space `dartsts_graph_v1`; see `results/stzero/pems04_h12/FROZEN.md`). sha1 of `archs.jsonl`: `459b1db47a878f2c05a5023cc18e86bf20d19dbd`. The genotypes are dataset-agnostic:
only `d_output` (207 sensors) and the adjacency differ; the AdaptiveAdjOp embeddings are sized by the node count at build time.

- Setting: `PEMS/metrla/metrla_12` (`experiments/configs/benchmark/PEMS/metrla/metrla_12.yaml`): `METR-LA.npz` (34272 x 207 x 1, speed; converted from DCRNN's metr-la.h5), window 96, horizon 12, 60/20/20 splits and normalisation as for PEMS.
- Adjacency: `data/metrla_adj.npy` built with `pilot.adjacency --root results/stzero/metrla_h12 --perms 8` from DCRNN's `adj_mx.pkl` (`~/scratch/all_datasets/PEMS/adj_METR-LA.pkl`): an undirected edge wherever the thresholded Gaussian-kernel weight is nonzero in either direction, diagonal dropped (see `data/metrla_adj.json`). This binarisation inherits DCRNN's distance threshold; it is not a raw road-connectivity list like PEMS04.csv. 8 degree-preserving permutations, seed 0.
- Node order: the pickle's sensor ids are in the order of `graph_sensor_ids.txt`, the same order as the h5 columns the `.npz` was converted from (DCRNN convention); checked empirically with `pilot.adj_sanity --root results/stzero/metrla_h12` (`tables/adj_sanity.json`).
- Probe batch: `data/metrla_probe_batch.pt` (seed 0, 4 train batches of 32, repo scaler; sha1 in `data/metrla_probe_batch.json`).
- Ground-truth schedule and proxy protocol: unchanged from PEMS04 h12 (batch 32, 20 epochs, patience 5, min 8 on val_mae; init seeds 0/1/2; `proxies/v1`, `proxies/spatial_v2`).
- Decision rule and verdict: `DECISION.md`, written by `python -m pilot.check --check probe --root results/stzero/metrla_h12`.

## TFAS probe

- tfas: not applicable — TFAS not usable as a distinct proxy: its score is ZiCo on Conv/Linear/Conv1d weights; the time-frequency awareness is an input augmentation (STL residual, |FFT|, Haar DWT) implemented only by its own TimesNet-family backbones. Composite temporal term = base proxy. Degenerate value stored as tfas_zico_cl. (TFAS commit `fd9150d`)

## Archive

- Archive: `$NAS_ROOT/backups/stzero.tgz` and `~/scratch/backups/stzero.tgz` (the whole `results/stzero/` tree incl. checkpoints of all four roots; size and sha1 in `results/stzero/compare/COMPARE.md`'s archive line).
- Everything except checkpoints and raw per-run JSONs is in git: `archs.jsonl`, `FROZEN.md`, `DECISION.md` (probe roots), `tables/*.md`, `tables/*.csv`, `figs/*.png` of every root, plus `results/stzero/pems04_h12/tables_n50`, `results/stzero/pems04_h12/figs_n50`, `results/stzero/compare/tables`, `results/stzero/compare/figs`, `results/stzero/compare/COMPARE.md`.
- The gates extend, scale, compare and archive PASS at this commit (`python -m pilot.check --check <gate> --root <root> --n <N>`); roots and probe are point-in-time gates (see the DECISION.md files).
