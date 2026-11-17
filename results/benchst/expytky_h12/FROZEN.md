# FROZEN: results/benchst/expytky_h12 — the shared list under the zero-masked pipeline

The benchmark of the shared list: one architecture list trained at every city under one pipeline, with the raw zeros
(missing sensor readings) masked in the training loss and in the val/test metrics (`pilot.train_arch --mask-zeros`).
Everything else is the stzero protocol: same schedule (20 epochs, patience 5, min 8, early stopping on val MAE), same
optimiser and scaler, same splits, same probe batch and adjacency.

- `archs.jsonl`: byte copy of `results/stzero/metrla_h12/archs.jsonl` (150 architectures, sampler seeds 2026 and 2029,
  space `dartsts_graph_v1`; sha1 `11eac76e13dd2`...). The same file sits in every benchst root.
- `data/`: byte copies built here by `pilot.adjacency` (from `adj_EXPYTKY.pkl`, symmetrised, 8 degree-preserving permutations) and `pilot.data --save-probe-batch` (seed 0, 4 batches of 32).
- `train/`: written by the benchst jobs only. This city has no stzero root; the raw data were prepared by `pilot.prepare_city`. Labels are masked MAE as in
  `results/stzero/expytky_h12`; the history rows also keep `val_mae_unmasked` and `test_mae_unmasked`.
- Proxies: not scored in the first wave (`SCORE_PROXIES=0`); scored later under the masked loss together with GLASS.
- Proxies, two units: the proxy pass ran on the rorqual slice (H100 3g.40gb) with the training array. `zico`, `zico_t`,
  `zico_s`, `glass`, `glass_t`, `glass_s` at 10 architectures, `grasp` at 14 and `grasp_all` at 20 did not fit in 40 GB
  (1,843 links). These values, and only these, were scored on a whole H100 80 GB (trillium job 1356386) from the same
  probe batch (sha1 `4b446cb0ad2b6`...) and the same list; no score that existed was scored again. The `gpu` field of every
  proxy file names the last unit that opened the file, not the unit of each score. No cost number comes from trillium.
