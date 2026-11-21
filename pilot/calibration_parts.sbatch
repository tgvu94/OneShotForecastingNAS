#!/usr/bin/env bash
# STID under the BasicTS pipeline with one part of our pipeline put in at a time (Survey/experiments/calibration-plan.md, Part 2).
# The config is pilot/basicts_stid_parts.py, copied to $NAS_ROOT/BasicTS/baselines/STID/pipeline_parts.py (BasicTS at commit
# 9a10e45, venv ~/basicts-venv).  One run = one training and one pass that writes the forecasts of the best checkpoint to
# checkpoints/STID_parts/<NAME>/<variant>_s<seed>/*/test_results/.  A run with forecasts is skipped, so a killed job is
# submitted again.  DATASET comes from the environment (pilot/submit.sh exports it); VARIANTS and SEEDS override the defaults.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"
cp "$SLURM_SUBMIT_DIR/pilot/basicts_stid_parts.py" "$NAS_ROOT/BasicTS/baselines/STID/pipeline_parts.py"
source "$HOME/basicts-venv/bin/activate"
cd "$NAS_ROOT/BasicTS"
case "${DATASET:-metrla}" in metrla) name=METR-LA ;; pemsbay) name=PEMS-BAY ;; *) name="$DATASET" ;; esac
echo "start $(date -Is) host $(hostname) dataset $name basicts $(git rev-parse --short HEAD) torch $(python -c 'import torch;print(torch.__version__)')"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
for v in ${VARIANTS:-stock split nodescale nodeloss instnorm clip sched all}; do
  for s in ${SEEDS:-0}; do
    dir=checkpoints/STID_parts/$name/${v}_s${s}
    if ls $dir/*/test_results/predictions.npy >/dev/null 2>&1; then echo "skip $name $v seed $s"; continue; fi
    t0=$(date +%s)
    PART_DATASET=$name PART_VARIANT=$v PART_SEED=$s python experiments/train.py -c baselines/STID/pipeline_parts.py -g 0 2>&1 \
      | grep -E "Error|error|Traceback" | tail -5
    ck=$(ls $dir/*/STID_best_val_MAE.pt 2>/dev/null | head -1)
    if [ -z "$ck" ]; then echo "FAILED $name $v seed $s: no checkpoint"; continue; fi
    PART_DATASET=$name PART_VARIANT=$v PART_SEED=$s python -c "
import os, sys
sys.path.append(os.getcwd())
import basicts
basicts.launch_evaluation(cfg='baselines/STID/pipeline_parts.py', ckpt_path='$ck', device_type='gpu', gpus='0')" 2>&1 \
      | grep -E "Result <test>|Error|Traceback" | sed "s/.*INFO - //"
    echo "run $name $v seed $s elapsed $(( $(date +%s) - t0 )) s"
  done
done
echo "end $(date -Is)"
