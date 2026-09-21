#!/usr/bin/env bash
# Submits the ground-truth runner as a job array: 6 tasks, at most 2 running, 8 h each (<= 48 GPU-h in total).
# Each task resumes whatever is unfinished and exits in seconds when nothing is left (setup/README.md section 6).
# This is the only way jobs get submitted; never call sbatch directly.
set -euo pipefail
cd "$HOME/nas/OneShotForecastingNAS"
n=$(squeue -u "$USER" -h --name=stzero | wc -l)
if [ "$n" -ge 1 ]; then echo "refusing: a stzero array is already queued/running ($n tasks) for $USER"; exit 1; fi
n_all=$(squeue -u "$USER" -h | wc -l)
if [ "$n_all" -ge 2 ]; then echo "refusing: $n_all jobs already queued/running for $USER"; exit 1; fi
mkdir -p "$HOME/nas/logs"
sbatch --array=0-5%2 --time=08:00:00 --cpus-per-task=8 --mem=32G \
       --account=def-rwpazzi_gpu --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1 \
       --job-name=stzero --output="$HOME/nas/logs/stzero_%A_%a.log" pilot/run_train_all.sbatch
