#!/usr/bin/env bash
# One array task = one shard of the ground truth for the frozen 50 (Phases 5-6):
#   pass 1: seed 0 for all 50;  pass 2: seeds 1 and 2 for the first 5 arch_ids (seed-noise ceiling);
#   pass 3: retry runs that failed once.  Every pass skips finished runs and honours other tasks' LOCK files.
source "$HOME/nas/OneShotForecastingNAS/pilot/env.sh"
shard="$((SLURM_ARRAY_TASK_ID % 2))/2"
echo "task $SLURM_ARRAY_TASK_ID on $(hostname) shard $shard start $(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
if [ "$((SLURM_ARRAY_TASK_ID % 2))" -eq 0 ]; then
  # pass 0 (even tasks only, so two tasks never write the same proxy file): all proxies x 3 init seeds for the 50 (idempotent)
  python -m pilot.score_proxies --archs results/archs.jsonl --proxies all --seeds 0,1,2 --out results/proxies/v1 2>&1 | tee -a logs/proxies_all.log | grep -v "Warning\|warn\|W0[0-9]\|coefficients\|_VF"
fi
python -m pilot.run_train_all --archs results/archs.jsonl --seeds 0 --max-epochs 20 --patience 5 --shard "$shard"
python -m pilot.run_train_all --archs results/archs.jsonl --limit 5 --seeds 1,2 --max-epochs 20 --patience 5 --shard "$shard"
python -m pilot.run_train_all --archs results/archs.jsonl --seeds 0 --max-epochs 20 --patience 5 --retry-failed
python -m pilot.run_train_all --archs results/archs.jsonl --limit 5 --seeds 1,2 --max-epochs 20 --patience 5 --retry-failed
python -m pilot.status --timing-csv results/tables/status.csv | tail -4
echo "task $SLURM_ARRAY_TASK_ID end $(date -Is)"
