# FROZEN: results/handdesign/expytky_h12 — two hand-designed models under the pipeline of the benchmark

Reference runs for the best architecture of the shared list at this city (`results/benchst/expytky_h12`). The models are STID and
STAEformer with their published sizes (`pilot/hand_models.py`). Everything outside the model is the benchst protocol: the loader,
the split, the scaler, the optimiser, the schedule of 20 epochs (patience 5, minimum 8), the zero mask in the loss and in the
metrics (`pilot.train_arch --mask-zeros`), h = 12, the MAE loss, seeds 0 to 2.

- `archs.jsonl`: two records, STID by two clocks. STAEformer is absent at this city: its attention over the sensors grows with the square of the sensor count (1,843 links), and the estimate from the peak memory at pems04 is above the memory of the GPU slice. `pipeclock`: the time features of the loader as every list architecture
  gets them (one hour per step). `trueclock`: the loader is called with the frequency of the benchmark file, so the features are
  the minute of the hour, the hour of the day and the day of the week of the data clock.
- Both models read the last 12 steps of the window; a list architecture reads 96.
- `data/`: a byte copy of `results/benchst/expytky_h12/data`; probe batch sha1 4b446cb0ad2b6. No proxy is scored in this root.
- Command: `JOB_NAME=hand_expytky TRAIN_EXTRA=--mask-zeros SCORE_PROXIES=0 SEED_SUBSET=4 pilot/submit.sh train results/handdesign/expytky_h12 expytky 12`.
