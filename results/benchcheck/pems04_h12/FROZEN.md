# FROZEN: results/benchcheck/pems04_h12 — the seed subset of the shared list under three cosine cycles

A check of the benchmark label: the first 50 architectures of the shared list (the seed subset of `results/benchst/pems04_h12`), trained for 60 epochs
with no early stop, which is three cycles of the schedule (cosine annealing with warm restarts, T_0 = 20, T_mult = 1). Everything else
is the benchst protocol: seed 0, the zero mask in the loss and in the metrics (`pilot.train_arch --mask-zeros`), h = 12.

- `archs.jsonl`: the first 50 lines of `results/benchst/pems04_h12/archs.jsonl` (sha1 11eac76e13dd5); sha1 of this file 459b1db47a878.
- `data/`: a byte copy of `results/benchst/pems04_h12/data`; probe batch sha1 32cb820843662.
- Command: `MAX_EPOCHS=60 PATIENCE=60 MIN_EPOCHS=60 TRAIN_EXTRA=--mask-zeros SCORE_PROXIES=0 SEED_SUBSET=0 pilot/submit.sh train results/benchcheck/pems04_h12 pems04 12`.
- The label of a run after k epochs is read from `log.csv`: the test MAE at the epoch with the lowest validation MAE among the first k.
- No proxy is scored and no further seed is trained in this root.
