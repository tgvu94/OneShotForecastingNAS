#!/usr/bin/env bash
# The linear stage of spatialgate: per-sensor linear fits on the raw datasets, no GPU and no training run.
# SG_DATASETS (comma list) comes from the environment; pilot/submit.sh linear submits this file.  Finished datasets are skipped.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"     # submit.sh submits from the repo root
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"
SG_DATASETS="${SG_DATASETS:-metrla,pems04,pems08,pemsbay,chengdu,shenzhen,expytky,largestsd,largestgba,largestgla,largestca}"
echo "spatialgate linear job $SLURM_JOB_ID on $(hostname) datasets $SG_DATASETS start $(date -Is)"
python -m pilot.spatialgate linear --datasets "$SG_DATASETS" --out results/spatialgate/compare/tables 2>&1 | tee -a "logs/spatialgate_linear.log"
echo "spatialgate linear job end $(date -Is)"
