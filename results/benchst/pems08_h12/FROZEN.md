# FROZEN: results/benchst/pems08_h12 — the shared list under the zero-masked pipeline

The benchmark of the shared list: one architecture list trained at every city under one pipeline, with the raw zeros
(missing sensor readings) masked in the training loss and in the val/test metrics (`pilot.train_arch --mask-zeros`).
Everything else is the stzero protocol: same schedule (20 epochs, patience 5, min 8, early stopping on val MAE), same
optimiser and scaler, same splits, same probe batch and adjacency.

- `archs.jsonl`: byte copy of `results/stzero/metrla_h12/archs.jsonl` (150 architectures, sampler seeds 2026 and 2029,
  space `dartsts_graph_v1`; sha1 `11eac76e13dd5`...). The same file sits in every benchst root. It shares no architecture
  with the list of `results/stzero/pems08_h12` (sampler seed 2028).
- `data/`: byte copies of the stzero root of this city (`pems08_adj.npy`, `pems08_adj.json`, the 8 degree-preserving
  permutations `pems08_adj_perm_*.npy` with `pems08_adj_perms.json`, `pems08_probe_batch.*`).
- `train/`: written by the benchst jobs only. Labels here are masked MAE and are not comparable with the unmasked labels of
  `results/stzero/pems08_h12`; the history rows also keep `val_mae_unmasked` and `test_mae_unmasked`.
- Cluster: every run of this root is assigned to Trillium, on one whole H100 per job (Trillium has no 3g.40gb slice).
  `COST.json` holds the cost ratio against the reference unit (one 3g.40gb slice of Nibi); `pilot.evalcost` reads it.
- Proxies: scored in pass 0 of the training array under the masked loss (`SCORE_PROXIES=1`).
