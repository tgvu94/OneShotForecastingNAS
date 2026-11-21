#!/usr/bin/env bash
# The only way jobs get submitted; never call sbatch directly.  Guards: no job of the same name queued, < 5 jobs in total,
# the root exists and holds archs.jsonl.  Usage:
#   pilot/submit.sh train   [ROOT] [DATASET] [HORIZON]   -> ground-truth runner, job array: 6 tasks, at most $ARRAY_MAX (default 3) running, 8 h each
#   pilot/submit.sh trainone [ROOT] [DATASET] [HORIZON] -> one unsharded job (default 3 h, TIME overrides) of the same runner: pre-checks
#                                                          (LIMIT=2 trains two archs), no proxies and no seed subset unless set
#   Env for train/trainone: JOB_NAME, MAX_EPOCHS, PATIENCE, MIN_EPOCHS, TRAIN_EXTRA (e.g. --mask-zeros), SCORE_PROXIES, SEED_SUBSET, LIMIT
#   pilot/submit.sh spatial [ROOT] [DATASET] [HORIZON]   -> spatial-sensitivity proxies: one job (default 2 h, TIME overrides; no training);
#                                                          MASK_ZEROS=1 masks the raw zeros (benchst), SPATIAL_BASE lists the base proxies,
#                                                          JOB_NAME names the job (default spatial; needed for two roots at once, same for proxies)
#   pilot/submit.sh proxies [ROOT] [DATASET] [HORIZON]   -> score the proxies named in $PROXIES (default all: only the names missing
#                                                          from the stored files are computed) on ROOT and on $EXTRA_ROOTS: one 2 h job
#   pilot/submit.sh basicts [ROOT] [DATASET] [HORIZON]   -> one timed BasicTS baseline run (MODEL=STID by default, CONFIG overrides the
#                                                          config path) on $NAS_ROOT/BasicTS: one 2 h job; ROOT is unused
#   pilot/submit.sh sgtrain ROOT DATASET [HORIZON]       -> the neural stage of spatialgate (pilot/spatialgate_train.sbatch): the runs of
#                                                          $ROOT/$RUNS (default runs_main.txt) as a job array of NSHARD tasks
#                                                          (default 4), one GPU unit each, 8 h (TIME overrides); JOB_NAME names it
#   pilot/submit.sh linear                               -> the linear stage of spatialgate (pilot/spatialgate_linear.sbatch): one CPU job,
#                                                          8 cores, 64 GB (MEM overrides), 3 h (TIME overrides), account def-rwpazzi_cpu;
#                                                          SG_DATASETS lists the datasets; ROOT, DATASET and HORIZON are unused
#   pilot/submit.sh ablation [ROOT] [DATASET] [HORIZON]  -> the STID single-part ablation replication on DATASET (6 variants x 3 seeds,
#                                                          pilot/basicts_ablation.sbatch): one 8 h job named abl_<DATASET>; ROOT is unused
#   pilot/submit.sh chronos [ROOT] [DATASET]             -> the frozen side of fmroute (pilot/fmroute_chronos.sbatch): Chronos-2 on the val and
#                                                          test windows of DATASET, one 8 h job named fz_<DATASET>; needs ~/chronos-venv and
#                                                          the weights under hf/ next to the nas tree; the root needs no data/ folder
#   pilot/submit.sh autoctspp [ROOT] DATASET            -> AutoCTS++ with its released code (pilot/autoctspp.sbatch): one job named
#                                                          ap_<DATASET> (JOB_NAME overrides), 3 h (TIME overrides); STEPS lists
#                                                          feature, search, train; ROOT is unused
#   pilot/submit.sh calibparts [ROOT] DATASET            -> STID under BasicTS with one part of our pipeline at a time
#                                                          (pilot/calibration_parts.sbatch): one 3 h job named cp_<DATASET> (TIME
#                                                          overrides); VARIANTS and SEEDS select the runs; ROOT is unused
# Cluster: the resource flags come from $CC_CLUSTER.  Default (Nibi, Fir, Rorqual): one 3g.40gb slice of an H100, 8 CPUs, 32 GB,
#   account def-rwpazzi_gpu.  trillium: one whole H100 (no slices there; 24 cores and the memory share come with the card),
#   account def-rwpazzi; Trillium refuses --cpus-per-task, --mem and the slice string.  Submit there from the GPU login node, with
#   the clone in scratch.  narval: one 3g.20gb slice of an A100 40 GB (no H100 there), 8 CPUs, 32 GB, account def-rwpazzi_gpu;
#   NARVAL_GPU=a100 asks for the whole card.  A root trained on another unit than the Nibi slice carries its cost ratio in
#   <root>/COST.json (pilot.evalcost).
# TEST_ONLY=1 passes --test-only to sbatch: the scheduler checks the request and submits nothing.
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
case "${CC_CLUSTER:-}" in
  trillium) res=(--account=def-rwpazzi --nodes=1 --gpus-per-node=1) ;;
  narval)   res=(--cpus-per-task=8 --mem=32G --account=def-rwpazzi_gpu --gpus=${NARVAL_GPU:-a100_3g.20gb}:1) ;;
  *)        res=(--cpus-per-task=8 --mem=32G --account=def-rwpazzi_gpu --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1) ;;
esac
common=("${res[@]}" --export="ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON")   # --export stays last: the modes replace common[-1]
case "$mode" in
  train)   name=${JOB_NAME:-stzero};  extra=(--array=0-5%${ARRAY_MAX:-3} --time=08:00:00 --output="$NAS_ROOT/logs/${JOB_NAME:-stzero}_${tag}_%A_%a.log");  script=pilot/run_train_all.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,MAX_EPOCHS=${MAX_EPOCHS:-20},PATIENCE=${PATIENCE:-5},MIN_EPOCHS=${MIN_EPOCHS:-8},TRAIN_EXTRA=${TRAIN_EXTRA:-},SCORE_PROXIES=${SCORE_PROXIES:-1},SEED_SUBSET=${SEED_SUBSET:-5},LIMIT=${LIMIT:-}" ;;
  trainone) name=${JOB_NAME:-trainone}; extra=(--time=${TIME:-03:00:00} --output="$NAS_ROOT/logs/${JOB_NAME:-trainone}_${tag}_%j.log"); script=pilot/run_train_all.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,MAX_EPOCHS=${MAX_EPOCHS:-20},PATIENCE=${PATIENCE:-5},MIN_EPOCHS=${MIN_EPOCHS:-8},TRAIN_EXTRA=${TRAIN_EXTRA:-},SCORE_PROXIES=${SCORE_PROXIES:-0},SEED_SUBSET=${SEED_SUBSET:-0},LIMIT=${LIMIT:-}" ;;
  spatial) name=${JOB_NAME:-spatial}; extra=(--time=${TIME:-02:00:00} --output="$NAS_ROOT/logs/spatial_${tag}_%j.log");            script=pilot/score_spatial.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,MASK_ZEROS=${MASK_ZEROS:-0}" ;;   # SPATIAL_BASE is a comma list: ALL carries it; a listed value would be split
  proxies) name=${JOB_NAME:-proxies}; extra=(--time=02:00:00 --output="$NAS_ROOT/logs/proxies_${tag}_%j.log");                    script=pilot/score_proxies.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,EXTRA_ROOTS=${EXTRA_ROOTS:-},MASK_ZEROS=${MASK_ZEROS:-0},LIMIT=${LIMIT:-}" ;;   # PROXIES is a comma list: ALL carries it; LIMIT=n scores the first n archs
  basicts) name=basicts; extra=(--time=02:00:00 --output="$NAS_ROOT/logs/basicts_${MODEL:-STID}_${tag}_%j.log");     script=pilot/basicts_stid.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,MODEL=${MODEL:-STID},CONFIG=${CONFIG:-}" ;;
  ablation) name=abl_$DATASET; extra=(--time=08:00:00 --output="$NAS_ROOT/logs/ablation_STID_${tag}_%j.log");   script=pilot/basicts_ablation.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,VARIANTS=${VARIANTS:-},SEEDS=${SEEDS:-}" ;;
  sgtrain) name=${JOB_NAME:-sg_$DATASET}; extra=(--array=0-$((${NSHARD:-4} - 1)) --time=${TIME:-08:00:00} --output="$NAS_ROOT/logs/${JOB_NAME:-sg_$DATASET}_%A_%a.log"); script=pilot/spatialgate_train.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET,HORIZON=$HORIZON,RUNS=${RUNS:-runs_main.txt},NSHARD=${NSHARD:-4}" ;;
  linear)  name=sg_linear; extra=(--time=${TIME:-03:00:00} --output="$NAS_ROOT/logs/spatialgate_linear_%j.log"); script=pilot/spatialgate_linear.sbatch
           common=(--cpus-per-task=8 --mem=${MEM:-64G} --account=def-rwpazzi_cpu "--export=ALL") ;;   # no GPU; SG_DATASETS is a comma list: ALL carries it
  chronos) name=fz_$DATASET; extra=(--time=${TIME:-08:00:00} --output="$NAS_ROOT/logs/fmroute_chronos_${DATASET}_%j.log"); script=pilot/fmroute_chronos.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET" ;;   # SETTINGS and SPLITS are space lists: ALL carries them
  calibparts) name=cp_$DATASET; extra=(--time=${TIME:-03:00:00} --output="$NAS_ROOT/logs/calibration_parts_${DATASET}_%j.log"); script=pilot/calibration_parts.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET" ;;   # VARIANTS and SEEDS are space lists: ALL carries them
  calibours) name=${JOB_NAME:-co_$DATASET}; extra=(--time=${TIME:-03:00:00} --output="$NAS_ROOT/logs/calibration_ours_${JOB_NAME:-$DATASET}_%j.log"); script=pilot/calibration_ours.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET" ;;   # VARIANTS, SEEDS, ARCH_FILE, SHARD, OUT_SUB, DUMP, PATIENCE: ALL carries them
  autoctspp) name=${JOB_NAME:-ap_$DATASET}; extra=(--time=${TIME:-03:00:00} --output="$NAS_ROOT/logs/autoctspp_${JOB_NAME:-$DATASET}_%j.log"); script=pilot/autoctspp.sbatch
           common[-1]="--export=ALL,ROOT=$ROOT,DATASET=$DATASET" ;;   # STEPS, SEEDS, ARCHS, EPOCHS, EVAL_BATCH, SHARD, LIMIT, OUT_SUB, SAMPLE_SCALE: ALL carries them
  *) echo "unknown mode $mode (autoctspp | calibours | calibparts | train | trainone | spatial | proxies | basicts | ablation | linear | sgtrain | chronos)"; exit 1 ;;
esac
if [ "$mode" = basicts ] || [ "$mode" = ablation ] || [ "$mode" = calibparts ]; then
  if [ ! -d "$NAS_ROOT/BasicTS/datasets/$(tr a-z A-Z <<<"$DATASET" | sed "s/METRLA/METR-LA/;s/PEMSBAY/PEMS-BAY/")" ]; then echo "refusing: BasicTS dataset folder for $DATASET missing (run its scripts/data_preparation script)"; exit 1; fi
  if [ ! -x "$HOME/basicts-venv/bin/python" ]; then echo "refusing: ~/basicts-venv missing"; exit 1; fi
elif [ "$mode" = sgtrain ]; then
  if [ ! -s "$ROOT/${RUNS:-runs_main.txt}" ]; then echo "refusing: $ROOT/${RUNS:-runs_main.txt} missing or empty (python -m pilot.spatialgate_root prepare)"; exit 1; fi
elif [ "$mode" = chronos ]; then
  if [ ! -x "${CHRONOS_VENV:-$HOME/chronos-venv}/bin/python" ]; then echo "refusing: the chronos venv is missing"; exit 1; fi
  if [ ! -d "${HF_HOME:-$(dirname "$NAS_ROOT")/hf}/hub/models--amazon--chronos-2" ]; then echo "refusing: the weights of amazon/chronos-2 are missing under hf/"; exit 1; fi
  mkdir -p "$ROOT"
elif [ "$mode" = autoctspp ]; then
  if [ ! -s "$NAS_ROOT/AutoCTS_plusplus/NAS_Net/AHC/AHC_param/AHC_0.pth" ]; then echo "refusing: the upstream tree is missing (pilot/autoctspp_setup.sh)"; exit 1; fi
elif [ "$mode" = calibours ]; then
  if [ -n "${ARCH_FILE:-}" ]; then
    if [ ! -s "$ARCH_FILE" ]; then echo "refusing: $ARCH_FILE missing or empty"; exit 1; fi
    if [ ! -s "$ROOT/data/${DATASET}_adj.npy" ]; then echo "refusing: $ROOT/data/${DATASET}_adj.npy missing"; exit 1; fi
  elif ! grep -q '"stid_trueclock"' "$ROOT/archs.jsonl" 2>/dev/null; then echo "refusing: $ROOT/archs.jsonl has no record stid_trueclock"; exit 1; fi
elif [ "$mode" != linear ]; then
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
[ "${TEST_ONLY:-0}" = 1 ] && extra+=(--test-only)
echo "submitting $mode for ROOT=$ROOT DATASET=$DATASET HORIZON=$HORIZON on ${CC_CLUSTER:-unknown cluster}: ${res[*]}${TEST_ONLY:+ (test only)}"
sbatch "${common[@]}" "${extra[@]}" --job-name="$name" "$script"
