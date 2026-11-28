#!/usr/bin/env bash
# EvoST with its released code at one district (Survey/experiments/evost-plan.md).
#   DATASET   one district (pems03 | pems06 | ...), with its files from pilot/evost_setup.sh
#   STEPS     a space list of train | export | maintain (default "train")
#   YEARS     the years of the checkpoints for `train` (default "2015 2020 2025")
#   SEEDS     the checkpoint seeds for `train` (default "42 43 44")
#   TARGETS   the target years for `export` and `maintain` (default "2020 2025")
#   EVAL_SEEDS  the evaluation seeds for `export` and `maintain` (default "51 52 53"; seed s reads the checkpoint of seed s - 9)
#   STUDIES   the studies for `maintain` (default "maintenance prompt": the upstream studies; "closed": pilot/evost_closed.py)
#   MAX_EPOCHS, MAX_WINDOWS   bounded checks only;  WORKERS  worker processes of the upstream loaders (upstream: 32)
# The upstream tree is $NAS_ROOT/EvoST and the Python is $EVOST_VENV (default ~/evost-venv).  A finished run is skipped.
# The job ends with status 1 when a step fails; the later steps do not run.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"
PY="${EVOST_VENV:-$HOME/evost-venv}/bin/python"; UP="$NAS_ROOT/EvoST"
echo "start $(date -Is) host $(hostname) commit $(git rev-parse --short HEAD) upstream $(git -C "$UP" rev-parse --short HEAD)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
t0=$(date +%s)
for step in ${STEPS:-train}; do
  echo "step $step ($(( $(date +%s) - t0 )) s)"
  case "$step" in
    train)    "$PY" -u -m pilot.evost_run train --district "$DATASET" --years ${YEARS:-2015 2020 2025} --seeds ${SEEDS:-42 43 44} \
                ${MAX_EPOCHS:+--max-epochs "$MAX_EPOCHS"} ${WORKERS:+--workers "$WORKERS"} || { echo "failed: $step"; exit 1; } ;;
    export)   "$PY" -u -m pilot.evost_run export --district "$DATASET" --years ${TARGETS:-2020 2025} --seeds ${EVAL_SEEDS:-51 52 53} || { echo "failed: $step"; exit 1; } ;;
    maintain) for y in ${TARGETS:-2020 2025}; do
                "$PY" -u -m pilot.evost_run maintain --district "$DATASET" --year "$y" --seeds ${EVAL_SEEDS:-51 52 53} --studies ${STUDIES:-maintenance prompt} \
                  ${MAX_WINDOWS:+--max-windows "$MAX_WINDOWS"} || { echo "failed: $step $y"; exit 1; }
              done ;;
    *) echo "unknown step $step"; exit 1 ;;
  esac
done
echo "elapsed $(( $(date +%s) - t0 )) s"
echo "end $(date -Is)"
