#!/usr/bin/env bash
# SGP with our runner, and the closed-form readouts on its embedding (Survey/experiments/sgp-plan.md).
#   DATASET    metrla | pemsbay
#   SETTINGS   a space list of release | paper | nospace | gesn (default "release")
#   SPLITS     a space list of release | strict (default "release"; see pilot/sgp_run.py)
#   SEEDS      default "0 1 2"
#   FORMS      a space list of R0 .. R6 (default "R0"); the setting gesn always runs the form R7
#   EPOCHS, MAX_ROWS   bounded checks only
# Output: results/sgp/<city>_h12/train/<setting>_<split>/<form>_s<seed>/.  A finished run is skipped.
# The job ends with status 1 when a run fails; the later runs do not start.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"
echo "start $(date -Is) host $(hostname) dataset $DATASET commit $(git rev-parse --short HEAD)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
t0=$(date +%s)
for setting in ${SETTINGS:-release}; do
  for split in ${SPLITS:-release}; do
    for seed in ${SEEDS:-0 1 2}; do
      forms="${FORMS:-R0}"; [ "$setting" = gesn ] && forms=R7
      echo "run $setting $split seed $seed forms $forms ($(( $(date +%s) - t0 )) s)"
      python -u -m pilot.sgp_run fit --city "$DATASET" --setting "$setting" --split "$split" --seed "$seed" --forms $forms \
        ${EPOCHS:+--epochs "$EPOCHS"} ${MAX_ROWS:+--max-rows "$MAX_ROWS"} || { echo "failed: $setting $split $seed"; exit 1; }
    done
  done
done
echo "elapsed $(( $(date +%s) - t0 )) s"
echo "end $(date -Is)"
