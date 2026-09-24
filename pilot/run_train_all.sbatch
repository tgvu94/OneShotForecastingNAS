#!/usr/bin/env bash
# One array task = one shard of the ground truth for one (dataset, horizon) root (Pilot 1 Phases 5-6, Pilot 2 Phases 2/4):
#   pass 0 (tasks 0 and 3): all proxies x 3 init seeds for every arch (idempotent; one task per wave of 3 so two tasks never write one file)
#   pass 1: seed 0 for all archs;  pass 2: seeds 1 and 2 for the first 5 arch_ids (seed-noise ceiling);
#   pass 3: retry runs that failed once.  Every pass skips finished runs and honours other tasks' LOCK files.
# ROOT / DATASET / HORIZON come from the environment (pilot/submit.sh exports them); defaults = the Pilot 1 tree.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"     # submit.sh submits from the repo root
ROOT="${ROOT:-results}"; DATASET="${DATASET:-pems04}"; HORIZON="${HORIZON:-12}"
setting=(--root "$ROOT" --dataset "$DATASET" --horizon "$HORIZON")
tag="${DATASET}_h${HORIZON}"
shard="$((SLURM_ARRAY_TASK_ID % 3))/3"
echo "task $SLURM_ARRAY_TASK_ID on $(hostname) root $ROOT ($tag) shard $shard start $(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
if [ "$((SLURM_ARRAY_TASK_ID % 3))" -eq 0 ]; then
  python -m pilot.score_proxies "${setting[@]}" --proxies all --seeds 0,1,2 2>&1 | tee -a "logs/proxies_${tag}.log" | grep -v "Warning\|warn\|W0[0-9]\|coefficients\|_VF"
fi
python -m pilot.run_train_all "${setting[@]}" --seeds 0 --max-epochs 20 --patience 5 --shard "$shard"
python -m pilot.run_train_all "${setting[@]}" --limit 5 --seeds 1,2 --max-epochs 20 --patience 5 --shard "$shard"
python -m pilot.run_train_all "${setting[@]}" --seeds 0 --max-epochs 20 --patience 5 --retry-failed
python -m pilot.run_train_all "${setting[@]}" --limit 5 --seeds 1,2 --max-epochs 20 --patience 5 --retry-failed
python -m pilot.status --root "$ROOT" --timing-csv "$ROOT/tables/status.csv" | tail -4
echo "task $SLURM_ARRAY_TASK_ID end $(date -Is)"
