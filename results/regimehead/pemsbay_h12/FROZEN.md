# FROZEN: results/regimehead/pemsbay_h12 — the two trained models of fmroute at this city, with five other training losses

- `archs.jsonl`: 10 records, written by `python -m pilot.regimehead root --dataset pemsbay`.  A record is a record of
  `results/fmroute/pemsbay_h12/archs.jsonl` with the key `train_loss` in its genotype and the loss name at the end of its `arch_id`.
  The losses: mse, huber, focal, wmae2, wmae4 (`pilot.regimehead.make_loss`).  The regime rule of the weighted losses is `absolute`.
- The MAE head is not trained here: its 6 runs are `results/fmroute/pemsbay_h12/train/<arch_id>/seed<s>`.
- `data/`: a byte copy of `results/fmroute/pemsbay_h12/data`.
- Everything else is the protocol of `results/fmroute/pemsbay_h12/FROZEN.md`: 20 epochs (patience 5, minimum 8), the early stop on the
  validation MAE, the zero mask, h = 12, seeds 0 to 2, the forecast dump of the best epoch.
- Command: `JOB_NAME=rh_pemsbay TRAIN_EXTRA="--mask-zeros --dump-forecasts" SCORE_PROXIES=0 SEED_SUBSET=10 pilot/submit.sh train results/regimehead/pemsbay_h12 pemsbay 12`.
