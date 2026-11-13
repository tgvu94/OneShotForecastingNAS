#!/usr/bin/env bash
# One array task = one shard of the ground truth for one (dataset, horizon) root:
#   pass 0 (tasks 0 and 3): all proxies x 3 init seeds for every arch (idempotent; one task per wave of 3 so two tasks never write one file)
#   pass 1: seed 0 for all archs;  pass 2: seeds 1 and 2 for the first 5 arch_ids (seed-noise ceiling);
#   pass 3: retry runs that failed once.  Every pass skips finished runs and honours other tasks' LOCK files.
# ROOT / DATASET / HORIZON come from the environment (pilot/submit.sh exports them); defaults = PEMS04 h12.
# Optional env: MAX_EPOCHS PATIENCE MIN_EPOCHS (schedule), TRAIN_EXTRA (passed to pilot.train_arch, e.g. --mask-zeros),
#   SCORE_PROXIES=0 skips pass 0, SEED_SUBSET=k trains seeds 1,2 for the first k archs (0 = skip), LIMIT=n trains the first n archs only.
#   Without SLURM_ARRAY_TASK_ID (mode trainone) the task runs unsharded.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"     # submit.sh submits from the repo root
ROOT="${ROOT:-results/stzero/pems04_h12}"; DATASET="${DATASET:-pems04}"; HORIZON="${HORIZON:-12}"
setting=(--root "$ROOT" --dataset "$DATASET" --horizon "$HORIZON")
tag="${DATASET}_h${HORIZON}"
MAX_EPOCHS="${MAX_EPOCHS:-20}"; PATIENCE="${PATIENCE:-5}"; MIN_EPOCHS="${MIN_EPOCHS:-8}"; TRAIN_EXTRA="${TRAIN_EXTRA:-}"
SCORE_PROXIES="${SCORE_PROXIES:-1}"; SEED_SUBSET="${SEED_SUBSET:-5}"; LIMIT="${LIMIT:-}"
sched=(--max-epochs "$MAX_EPOCHS" --patience "$PATIENCE" --min-epochs "$MIN_EPOCHS" "--extra=$TRAIN_EXTRA")
lim=(); [ -n "$LIMIT" ] && lim=(--limit "$LIMIT")
if [ -n "${SLURM_ARRAY_TASK_ID:-}" ]; then shard="$((SLURM_ARRAY_TASK_ID % 3))/3"; shardargs=(--shard "$shard"); first=$((SLURM_ARRAY_TASK_ID % 3 == 0));
else shard="none"; shardargs=(); first=1; SLURM_ARRAY_TASK_ID=single; fi
echo "schedule: ${sched[*]} limit=${LIMIT:-all} seed_subset=$SEED_SUBSET score_proxies=$SCORE_PROXIES"
echo "task $SLURM_ARRAY_TASK_ID on $(hostname) root $ROOT ($tag) shard $shard start $(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
if [ "$first" -eq 1 ] && [ "$SCORE_PROXIES" = 1 ]; then
  MASKARG=(); case " $TRAIN_EXTRA " in *" --mask-zeros "*) MASKARG=(--mask-zeros);; esac
  python -m pilot.score_proxies "${setting[@]}" --proxies all --seeds 0,1,2 "${MASKARG[@]}" 2>&1 | tee -a "logs/proxies_${tag}.log" | grep -v "Warning\|warn\|W0[0-9]\|coefficients\|_VF"
fi
python -m pilot.run_train_all "${setting[@]}" --seeds 0 "${sched[@]}" "${lim[@]}" "${shardargs[@]}"
if [ "$SEED_SUBSET" != 0 ]; then python -m pilot.run_train_all "${setting[@]}" --limit "$SEED_SUBSET" --seeds 1,2 "${sched[@]}" "${shardargs[@]}"; fi
python -m pilot.run_train_all "${setting[@]}" --seeds 0 "${sched[@]}" "${lim[@]}" --retry-failed
if [ "$SEED_SUBSET" != 0 ]; then python -m pilot.run_train_all "${setting[@]}" --limit "$SEED_SUBSET" --seeds 1,2 "${sched[@]}" --retry-failed; fi
python -m pilot.status --root "$ROOT" --timing-csv "$ROOT/tables/status.csv" | tail -4
echo "task $SLURM_ARRAY_TASK_ID end $(date -Is)"
