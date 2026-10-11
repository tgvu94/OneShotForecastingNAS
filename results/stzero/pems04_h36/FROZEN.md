# FROZEN: results/stzero/pems04_h36 — the frozen 50 at horizon 36 (probe)

`archs.jsonl` and `archs/` are byte copies of `results/stzero/pems04_h12/archs.jsonl` / `results/stzero/pems04_h12/archs/` (the 50 architectures frozen with
sampler seed 2026, space `dartsts_graph_v1`; see `results/stzero/pems04_h12/FROZEN.md`). sha1 of `archs.jsonl`: `459b1db47a878f2c05a5023cc18e86bf20d19dbd`.

- Setting: `PEMS/pems04/pems04_36` (`experiments/configs/benchmark/PEMS/pems04/pems04_36.yaml`): window 96, horizon 36 (3 h), same data file, splits and normalisation as h12.
- Adjacency: `data/pems04_adj.npy` and `data/pems04_adj_perm_0..7.npy` rebuilt with the same commands and seeds; verified identical to the PEMS04 h12 files.
- Probe batch: `data/pems04_probe_batch.pt` (seed 0, 4 train batches of 32, repo scaler) — new file, x_future / target now have 36 steps (sha1 in `data/pems04_probe_batch.json`).
- Ground-truth schedule: unchanged from PEMS04 h12 (batch 32, 20 epochs, patience 5, min 8 on val_mae, repo eval optimiser, AMP); seed 0 for all 50, seeds 1 and 2 for the first 5 arch_ids.
- Proxy protocol: unchanged (init seeds 0/1/2, cudnn deterministic; `proxies/v1`, `proxies/spatial_v2` with the 8 permutations).
- Decision rule and verdict: `DECISION.md`, written by `python -m pilot.check --check probe --root results/stzero/pems04_h36`.

## TFAS probe

- tfas: not applicable — TFAS not usable as a distinct proxy: its score is ZiCo on Conv/Linear/Conv1d weights; the time-frequency awareness is an input augmentation (STL residual, |FFT|, Haar DWT) implemented only by its own TimesNet-family backbones. Composite temporal term = base proxy. Degenerate value stored as tfas_zico_cl. (TFAS commit `fd9150d`)

## Archive

- Archive: `$NAS_ROOT/backups/stzero.tgz` and `~/scratch/backups/stzero.tgz` (the whole `results/stzero/` tree incl. checkpoints of all four roots; size and sha1 in `results/stzero/compare/COMPARE.md`'s archive line).
- Everything except checkpoints and raw per-run JSONs is in git: `archs.jsonl`, `FROZEN.md`, `DECISION.md` (probe roots), `tables/*.md`, `tables/*.csv`, `figs/*.png` of every root, plus `results/stzero/pems04_h12/tables_n50`, `results/stzero/pems04_h12/figs_n50`, `results/stzero/compare/tables`, `results/stzero/compare/figs`, `results/stzero/compare/COMPARE.md`.
- The gates extend, scale, compare and archive PASS at this commit (`python -m pilot.check --check <gate> --root <root> --n <N>`); roots and probe are point-in-time gates (see the DECISION.md files).
