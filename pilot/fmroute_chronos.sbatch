#!/usr/bin/env bash
# The frozen side of fmroute for one city: Chronos-2, zero-shot, on every window of the val and the test split, in the two
# settings of the plan (joint: every sensor of the city in one item; alone: one sensor per item).  No training.
# ROOT / DATASET come from the environment (pilot/submit.sh exports them).  The run uses the second venv (CHRONOS_VENV, default
# ~/chronos-venv), which holds chronos-forecasting beside the pinned torch, and the weights under HF_HOME (default: hf/ next to
# the nas tree), downloaded on a login node because most compute nodes have no internet.
# Output: $ROOT/frozen/chronos2_<setting>/{forecast,quantiles}_<split>.npy and chronos_<split>.json.  Resumable: a finished
# split is skipped, and an unfinished one continues from its part files.
export NAS_VENV="${CHRONOS_VENV:-$HOME/chronos-venv}"
source "$SLURM_SUBMIT_DIR/pilot/env.sh"     # submit.sh submits from the repo root
export HF_HOME="${HF_HOME:-$(dirname "$NAS_ROOT")/hf}" HF_HUB_OFFLINE=1
ROOT="${ROOT:?}"; DATASET="${DATASET:?}"
echo "chronos job $SLURM_JOB_ID on $(hostname) root $ROOT ($DATASET) start $(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
for setting in ${SETTINGS:-joint alone}; do
  for split in ${SPLITS:-test val}; do
    out="$ROOT/frozen/chronos2_$setting"
    if [ -s "$out/forecast_$split.npy" ]; then echo "$setting $split: done"; continue; fi
    python -m pilot.fmroute chronos --dataset "$DATASET" --split "$split" --setting "$setting" --out "$out" 2>&1 | grep -v -i "warn" | awk 'NR % 20 == 1 || /^\{/'
  done
done
echo "chronos job end $(date -Is)"
