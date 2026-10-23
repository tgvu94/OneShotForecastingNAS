#!/usr/bin/env bash
# One timed training run of a BasicTS baseline config (default STID) under the BasicTS pipeline.  The checkout lives next to
# the repo at $NAS_ROOT/BasicTS (commit 9a10e45, the last one before its reconstruction, with baselines/<MODEL>/<DATASET>.py) and its venv at
# ~/basicts-venv (built by scratch_scripts/basicts_venv.sh).  The elapsed time of one full run sets the cost of the
# single-part ablation replication.  DATASET and HORIZON come from the environment (pilot/submit.sh exports them);
# MODEL (default STID) and CONFIG (an explicit config path) override the default config.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"                 # sets NAS_ROOT; submit.sh submits from the repo root
BTS="$NAS_ROOT/BasicTS"
source "$HOME/basicts-venv/bin/activate"
cd "$BTS"
case "${DATASET:-pems04}" in
  pems03) name=PEMS03 ;; pems04) name=PEMS04 ;; pems07) name=PEMS07 ;; pems08) name=PEMS08 ;;
  metrla) name=METR-LA ;; pemsbay) name=PEMS-BAY ;; *) name="$DATASET" ;;
esac
cfg="${CONFIG:-baselines/${MODEL:-STID}/${name}.py}"
echo "start $(date -Is) host $(hostname) config $cfg basicts $(git rev-parse --short HEAD) torch $(python -c 'import torch;print(torch.__version__)')"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
t0=$(date +%s)
python experiments/train.py -c "$cfg" -g 0 2>&1 | grep -v "Warning\|warn"
echo "end $(date -Is) elapsed $(( $(date +%s) - t0 )) s"
