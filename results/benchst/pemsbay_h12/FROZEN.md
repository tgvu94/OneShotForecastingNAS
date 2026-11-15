# FROZEN: results/benchst/pemsbay_h12 — the shared list under the zero-masked pipeline

The benchmark of the shared list: one architecture list trained at every city under one pipeline, with the raw zeros
(missing sensor readings) masked in the training loss and in the val/test metrics (`pilot.train_arch --mask-zeros`).
Everything else is the stzero protocol: same schedule (20 epochs, patience 5, min 8, early stopping on val MAE), same
optimiser and scaler, same splits, same probe batch and adjacency.

- `archs.jsonl`: byte copy of `results/benchst/metrla_h12/archs.jsonl` (150 architectures, sampler seeds 2026 and 2029,
  space `dartsts_graph_v1`; sha1 `11eac76e13dd5`...). The same file sits in every benchst root.
- `data/`: built here by `pilot.adjacency` (from `adj_mx_bay.pkl`, 2079 edges, 8 degree-preserving permutations) and
  `pilot.data --save-probe-batch` (seed 0, 4 batches of 32; sha1 `2afa33cc29a3`...).
- `train/`: written by the benchst jobs only. This city has no stzero root. PEMS-BAY has no raw zeros, so the mask
  changes no value here; the flag stays on so that the command is the same at every city.
- Cluster: Narval, one `a100_3g.20gb` slice. The cost ratio against the Nibi slice goes into `COST.json`.
- The same city holds a second list in `results/freshlist/pemsbay_h12`.
