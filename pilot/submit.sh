#!/usr/bin/env bash
# The only way jobs get submitted; never call sbatch directly.  Guards: no job of the same name queued, < 3 jobs in total,
# the root exists and holds archs.jsonl.  Usage:
#   pilot/submit.sh train   [ROOT] [DATASET] [HORIZON]   -> ground-truth runner, job array: 6 tasks, at most 3 running, 8 h each (<= 48 GPU-h)
#   pilot/submit.sh spatial [ROOT] [DATASET] [HORIZON]   -> spatial-sensitivity proxies: one 2 h job (no training)
# Defaults: ROOT=results DATASET=pems04 HORIZON=12 (the Pilot 1 tree).  E.g.  pilot/submit.sh train results/pems04_h36 pems04 36
# Every script resumes / skips finished work, so a killed job is simply resubmitted (setup/README.md section 6).
set -euo pipefail
cd "$HOME/nas/OneShotForecastingNAS"
mode="${1:-train}"
ROOT="${2:-results}"; DATASET="${3:-pems04}"; HORIZON="${4:-12}"
tag="${DATASET}h${HORIZON}"
common=(--cpus-per-task=8 --mem=32G --account=def-rwpazzi_gpu --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
        --export="ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON")
case "$mode" in
  train)   name=stzero;  extra=(--array=0-5%3 --time=08:00:00 --output="$HOME/nas/logs/stzero_${tag}_%A_%a.log");  script=pilot/run_train_all.sbatch ;;
  spatial) name=spatial; extra=(--time=02:00:00 --output="$HOME/nas/logs/spatial_${tag}_%j.log");                    script=pilot/score_spatial.sbatch ;;
  *) echo "unknown mode $mode (train | spatial)"; exit 1 ;;
esac
if [ ! -s "$ROOT/archs.jsonl" ]; then echo "refusing: $ROOT/archs.jsonl missing or empty"; exit 1; fi
if [ ! -s "$ROOT/data/${DATASET}_probe_batch.pt" ]; then echo "refusing: $ROOT/data/${DATASET}_probe_batch.pt missing (python -m pilot.data --save-probe-batch --root $ROOT)"; exit 1; fi
if [ ! -s "$ROOT/data/${DATASET}_adj.npy" ]; then echo "refusing: $ROOT/data/${DATASET}_adj.npy missing (python -m pilot.adjacency --root $ROOT)"; exit 1; fi
n=$(squeue -u "$USER" -h --name="$name" | wc -l)
if [ "$n" -ge 1 ]; then echo "refusing: a $name job is already queued/running ($n) for $USER"; exit 1; fi
n_all=$(squeue -u "$USER" -h | wc -l)
if [ "$n_all" -ge 3 ]; then echo "refusing: $n_all jobs already queued/running for $USER (cap 3)"; exit 1; fi
mkdir -p "$HOME/nas/logs"
echo "submitting $mode for ROOT=$ROOT DATASET=$DATASET HORIZON=$HORIZON"
sbatch "${common[@]}" "${extra[@]}" --job-name="$name" "$script"
