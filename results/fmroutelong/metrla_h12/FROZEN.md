# FROZEN: results/fmroutelong/metrla_h12 — the trained side of fmroute at this city with a schedule of 100 epochs

The same two models, seeds, windows and forecast dump as `results/fmroute/metrla_h12`. One thing differs: the schedule has at most
100 epochs (patience 25, minimum 40), not 20 (patience 5, minimum 8). The scheduler is the one of the benchst protocol
(CosineAnnealingWarmRestarts, T_0 = 20), so the 100 epochs are 5 cycles; a patience of 25 lets a run reach the end of the next
cycle before it stops. In the root of 20 epochs every run had its best epoch among the last two, so the schedule had stopped the
run, not the validation error.

- `archs.jsonl`: a byte copy of `results/fmroute/metrla_h12/archs.jsonl` (`261470bcc0` and `stid_trueclock`).
- `data/`: a byte copy of `results/fmroute/metrla_h12/data`.
- `frozen/`: the forecasts of the frozen side are those of `results/fmroute/metrla_h12/frozen` (a link on the cluster of the root);
  the frozen side has no training.
- Cluster: Trillium, as the root of 20 epochs.
- Command: `JOB_NAME=fml_metrla MAX_EPOCHS=100 PATIENCE=25 MIN_EPOCHS=40 TRAIN_EXTRA="--mask-zeros --dump-forecasts" SCORE_PROXIES=0 SEED_SUBSET=2 pilot/submit.sh train results/fmroutelong/metrla_h12 metrla 12`.
