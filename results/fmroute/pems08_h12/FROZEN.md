# FROZEN: results/fmroute/pems08_h12 — the trained side of fmroute at this city

Two models trained at the city, 3 seeds each, with the forecasts of the best epoch on the val and the test split
(`pilot.train_arch --dump-forecasts`: `train/<arch_id>/seed<s>/forecast_{val,test}.npy`, raw unit, in the order of the split).
Everything else is the benchst protocol: the loader, the split, the scaler, the optimiser, the schedule of 20 epochs (patience 5,
minimum 8), the zero mask in the loss and in the metrics, h = 12, the MAE loss, seeds 0 to 2.

- `archs.jsonl`: two records. `43d20fa260`: the architecture of the shared list with the lowest validation MAE of seed 0 in
  `results/benchst/pems08_h12`; its record is a copy of the line of that root. `stid_trueclock`: STID with its published size
  (`pilot/hand_models.py`) and the time features of the data clock.
- `data/`: a byte copy of `results/benchst/pems08_h12/data`. No proxy is scored in this root.
- Command: `JOB_NAME=fm_pems08 TRAIN_EXTRA="--mask-zeros --dump-forecasts" SCORE_PROXIES=0 SEED_SUBSET=2 pilot/submit.sh train results/fmroute/pems08_h12 pems08 12`.
- The forecast files are large and stay on the cluster of the root until they are scored (`python -m pilot.fmroute score`).
