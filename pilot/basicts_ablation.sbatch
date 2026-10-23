#!/usr/bin/env bash
# The single-part ablation replication of STID on one dataset under the BasicTS pipeline: 6 variants x 3 seeds = 18 runs
# in one job, each run the stock 100 epochs.  The config is $NAS_ROOT/BasicTS/baselines/STID/ablation.py (one part changed
# per variant, selected by ABL_DATASET / ABL_VARIANT / ABL_SEED).  A run whose test_metrics.json exists is skipped and an
# interrupted run resumes from its last checkpoint, so a killed job is simply resubmitted.  DATASET comes from the
# environment (pilot/submit.sh exports it); VARIANTS and SEEDS override the defaults.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"                 # sets NAS_ROOT; submit.sh submits from the repo root
source "$HOME/basicts-venv/bin/activate"
cd "$NAS_ROOT/BasicTS"
case "${DATASET:-pems04}" in
  pems03) name=PEMS03 ;; pems04) name=PEMS04 ;; pems07) name=PEMS07 ;; pems08) name=PEMS08 ;;
  metrla) name=METR-LA ;; pemsbay) name=PEMS-BAY ;; *) name="$DATASET" ;;
esac
echo "start $(date -Is) host $(hostname) dataset $name basicts $(git rev-parse --short HEAD)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
for v in ${VARIANTS:-full input operator loss norm schedule}; do
  for s in ${SEEDS:-0 1 2}; do
    done_file=$(ls checkpoints/STID_ablation/$name/${v}_s${s}/*/test_metrics.json 2>/dev/null | head -1)
    if [ -n "$done_file" ]; then echo "skip $name $v seed $s: $done_file"; continue; fi
    t0=$(date +%s)
    ABL_DATASET=$name ABL_VARIANT=$v ABL_SEED=$s python experiments/train.py -c baselines/STID/ablation.py -g 0 2>&1 \
      | grep -E "Epoch 100|Result <test>|Result <test @|Loading Checkpoint|Error|error" | tail -5
    echo "run $name $v seed $s elapsed $(( $(date +%s) - t0 )) s"
  done
done
echo "end $(date -Is)"
