#!/usr/bin/env bash
# The only way jobs get submitted; never call sbatch directly.  Guards: no job of the same name queued, < 2 jobs in total.
#   pilot/submit.sh            -> ground-truth runner as a job array: 6 tasks, at most 2 running, 8 h each (<= 48 GPU-h)
#   pilot/submit.sh spatial    -> Phase 7 spatial-sensitivity proxies: one 2 h job (no training)
# Every script resumes / skips finished work, so a killed job is simply resubmitted (setup/README.md section 6).
set -euo pipefail
cd "$HOME/nas/OneShotForecastingNAS"
mode="${1:-train}"
common=(--cpus-per-task=8 --mem=32G --account=def-rwpazzi_gpu --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1)
case "$mode" in
  train)   name=stzero;  extra=(--array=0-5%2 --time=08:00:00 --output="$HOME/nas/logs/stzero_%A_%a.log");  script=pilot/run_train_all.sbatch ;;
  spatial) name=spatial; extra=(--time=02:00:00 --output="$HOME/nas/logs/spatial_%j.log");                    script=pilot/score_spatial.sbatch ;;
  *) echo "unknown mode $mode (train | spatial)"; exit 1 ;;
esac
n=$(squeue -u "$USER" -h --name="$name" | wc -l)
if [ "$n" -ge 1 ]; then echo "refusing: a $name job is already queued/running ($n) for $USER"; exit 1; fi
n_all=$(squeue -u "$USER" -h | wc -l)
if [ "$n_all" -ge 2 ]; then echo "refusing: $n_all jobs already queued/running for $USER"; exit 1; fi
mkdir -p "$HOME/nas/logs"
sbatch "${common[@]}" "${extra[@]}" --job-name="$name" "$script"
