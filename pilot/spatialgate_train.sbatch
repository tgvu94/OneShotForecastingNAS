#!/usr/bin/env bash
# The neural stage of spatialgate: the runs "arch_id seed" of $ROOT/$RUNS, one array task per shard (line i runs in task i mod NSHARD).
# ROOT / DATASET / HORIZON / RUNS / NSHARD come from the environment (pilot/submit.sh sgtrain exports them).  A finished run is
# skipped and a run that was cut continues from its checkpoint, so a task that ends with TIMEOUT is submitted again.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"     # submit.sh submits from the repo root
ROOT="${ROOT:?}"; DATASET="${DATASET:?}"; HORIZON="${HORIZON:-12}"; RUNS="${RUNS:-runs_main.txt}"; NSHARD="${NSHARD:-1}"
shard="${SLURM_ARRAY_TASK_ID:-0}"
echo "spatialgate task $shard of $NSHARD on $(hostname) root $ROOT runs $RUNS start $(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
i=0
while read -r arch seed; do
  [ -z "$arch" ] && continue
  if [ $((i % NSHARD)) -eq "$shard" ]; then
    python -m pilot.train_arch --root "$ROOT" --dataset "$DATASET" --horizon "$HORIZON" --arch-id "$arch" --seed "$seed" \
      --mask-zeros --sensor-errors --prune-ckpt 2>&1 | grep -v "Warning\|warn\|W0[0-9]\|coefficients\|_VF"
  fi
  i=$((i + 1))
done < "$ROOT/$RUNS"
echo "spatialgate task end $(date -Is)"
