#!/usr/bin/env bash
# The only way jobs get submitted; never call sbatch directly.  Guards: no job of the same name queued, < 5 jobs in total,
# the root exists and holds archs.jsonl.  Usage:
#   pilot/submit.sh train   [ROOT] [DATASET] [HORIZON]   -> ground-truth runner, job array: 6 tasks, at most $ARRAY_MAX (default 3) running, 8 h each
#   pilot/submit.sh trainone [ROOT] [DATASET] [HORIZON] -> one unsharded job (default 3 h, TIME overrides) of the same runner: pre-checks
#                                                          (LIMIT=2 trains two archs), no proxies and no seed subset unless set
#   Env for train/trainone: JOB_NAME, MAX_EPOCHS, PATIENCE, MIN_EPOCHS, TRAIN_EXTRA (e.g. --mask-zeros), SCORE_PROXIES, SEED_SUBSET, LIMIT
#   pilot/submit.sh spatial [ROOT] [DATASET] [HORIZON]   -> spatial-sensitivity proxies: one 2 h job (no training)
#   pilot/submit.sh proxies [ROOT] [DATASET] [HORIZON]   -> score the proxies named in $PROXIES (default all: only the names missing
#                                                          from the stored files are computed) on ROOT and on $EXTRA_ROOTS: one 2 h job
#   pilot/submit.sh basicts [ROOT] [DATASET] [HORIZON]   -> one timed BasicTS baseline run (MODEL=STID by default, CONFIG overrides the
#                                                          config path) on $NAS_ROOT/BasicTS: one 2 h job; ROOT is unused
#   pilot/submit.sh ablation [ROOT] [DATASET] [HORIZON]  -> the STID single-part ablation replication on DATASET (6 variants x 3 seeds,
#                                                          pilot/basicts_ablation.sbatch): one 8 h job named abl_<DATASET>; ROOT is unused
# AFTER=<jobid> adds --dependency=afterany:<jobid>; a dependent job waits, so only *running* jobs count toward the cap of 5.
# CAP (default 5) is the total number of queued or running jobs allowed; ARRAY_MAX (default 3) throttles the train array.
# Defaults: ROOT=results/stzero/pems04_h12 DATASET=pems04 HORIZON=12.  E.g.  pilot/submit.sh train results/stzero/pems04_h36 pems04 36
# Every script resumes / skips finished work, so a killed job is simply resubmitted (resubmit it).
set -euo pipefail
cd "$(cd "$(dirname "$0")/.." && pwd)"          # the repo, wherever it lives; NAS_ROOT is its parent
NAS_ROOT="$(dirname "$PWD")"
mode="${1:-train}"
ROOT="${2:-results/stzero/pems04_h12}"; DATASET="${3:-pems04}"; HORIZON="${4:-12}"
tag="${DATASET}h${HORIZON}"
common=(--cpus-per-task=8 --mem=32G --account=def-rwpazzi_gpu --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
        --export="ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON")
case "$mode" in
  train)   name=${JOB_NAME:-stzero};  extra=(--array=0-5%${ARRAY_MAX:-3} --time=08:00:00 --output="$NAS_ROOT/logs/${JOB_NAME:-stzero}_${tag}_%A_%a.log");  script=pilot/run_train_all.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,MAX_EPOCHS=${MAX_EPOCHS:-20},PATIENCE=${PATIENCE:-5},MIN_EPOCHS=${MIN_EPOCHS:-8},TRAIN_EXTRA=${TRAIN_EXTRA:-},SCORE_PROXIES=${SCORE_PROXIES:-1},SEED_SUBSET=${SEED_SUBSET:-5},LIMIT=${LIMIT:-}" ;;
  trainone) name=${JOB_NAME:-trainone}; extra=(--time=${TIME:-03:00:00} --output="$NAS_ROOT/logs/${JOB_NAME:-trainone}_${tag}_%j.log"); script=pilot/run_train_all.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,MAX_EPOCHS=${MAX_EPOCHS:-20},PATIENCE=${PATIENCE:-5},MIN_EPOCHS=${MIN_EPOCHS:-8},TRAIN_EXTRA=${TRAIN_EXTRA:-},SCORE_PROXIES=${SCORE_PROXIES:-0},SEED_SUBSET=${SEED_SUBSET:-0},LIMIT=${LIMIT:-}" ;;
  spatial) name=spatial; extra=(--time=02:00:00 --output="$NAS_ROOT/logs/spatial_${tag}_%j.log");                    script=pilot/score_spatial.sbatch ;;
  proxies) name=proxies; extra=(--time=02:00:00 --output="$NAS_ROOT/logs/proxies_${tag}_%j.log");                    script=pilot/score_proxies.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,EXTRA_ROOTS=${EXTRA_ROOTS:-},PROXIES=${PROXIES:-}" ;;
  basicts) name=basicts; extra=(--time=02:00:00 --output="$NAS_ROOT/logs/basicts_${MODEL:-STID}_${tag}_%j.log");     script=pilot/basicts_stid.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,MODEL=${MODEL:-STID},CONFIG=${CONFIG:-}" ;;
  ablation) name=abl_$DATASET; extra=(--time=08:00:00 --output="$NAS_ROOT/logs/ablation_STID_${tag}_%j.log");   script=pilot/basicts_ablation.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,VARIANTS=${VARIANTS:-},SEEDS=${SEEDS:-}" ;;
  *) echo "unknown mode $mode (train | trainone | spatial | proxies | basicts | ablation)"; exit 1 ;;
esac
if [ "$mode" = basicts ] || [ "$mode" = ablation ]; then
  if [ ! -d "$NAS_ROOT/BasicTS/datasets/$(tr a-z A-Z <<<"$DATASET" | sed "s/METRLA/METR-LA/;s/PEMSBAY/PEMS-BAY/")" ]; then echo "refusing: BasicTS dataset folder for $DATASET missing (run its scripts/data_preparation script)"; exit 1; fi
  if [ ! -x "$HOME/basicts-venv/bin/python" ]; then echo "refusing: ~/basicts-venv missing"; exit 1; fi
else
  if [ ! -s "$ROOT/archs.jsonl" ]; then echo "refusing: $ROOT/archs.jsonl missing or empty"; exit 1; fi
  if [ ! -s "$ROOT/data/${DATASET}_probe_batch.pt" ]; then echo "refusing: $ROOT/data/${DATASET}_probe_batch.pt missing (python -m pilot.data --save-probe-batch --root $ROOT)"; exit 1; fi
  if [ ! -s "$ROOT/data/${DATASET}_adj.npy" ]; then echo "refusing: $ROOT/data/${DATASET}_adj.npy missing (python -m pilot.adjacency --root $ROOT)"; exit 1; fi
fi
n=$(squeue -u "$USER" -h --name="$name" | wc -l)
if [ "$n" -ge 1 ]; then echo "refusing: a $name job is already queued/running ($n) for $USER"; exit 1; fi
if [ -n "${AFTER:-}" ]; then
  extra+=(--dependency="afterany:$AFTER")
  n_all=$(squeue -u "$USER" -h -t RUNNING | wc -l)
else
  n_all=$(squeue -u "$USER" -h | wc -l)
fi
CAP=${CAP:-5}
if [ "$n_all" -ge "$CAP" ]; then echo "refusing: $n_all jobs already queued/running for $USER (cap $CAP)"; exit 1; fi
mkdir -p "$NAS_ROOT/logs"
echo "submitting $mode for ROOT=$ROOT DATASET=$DATASET HORIZON=$HORIZON"
sbatch "${common[@]}" "${extra[@]}" --job-name="$name" "$script"
