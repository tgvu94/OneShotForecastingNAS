#!/usr/bin/env bash
# CompactST with its released code and weights at one city (Survey/experiments/compactst-plan.md).
#   DATASET   one city of pilot.compactst_data (chengdu | shenzhen | sd | gba | ca_d<k> | gba_n<n>)
#   DATASETS  a space list of cities that replaces DATASET; one process per city.  A city file that is absent is written first.
#   FORMS     a space list of forms of the adaptation (default C0, the released form); see pilot/compactst_run.py.
#             FORMS="" skips the runs from the pre-trained weights.
#   RANDOM_FORMS  a space list of forms that also run from a random start (default none)
#   SEEDS     a space list (default 999, the seed of the released script)
#   SHARE     the share of the training split (default 0.05);  INIT  pretrained | random;  MAX_EPOCHS;  OUT_SUB (default fit)
# The upstream tree is $NAS_ROOT/CompactST (pilot/compactst_setup.sh).  A finished run is skipped.  The job ends with status 1
# when a fit of a city fails; the other cities still run.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"
REPO="$PWD"; UP="$NAS_ROOT/CompactST"
echo "start $(date -Is) host $(hostname) commit $(git rev-parse --short HEAD) upstream $(git -C "$UP" rev-parse --short HEAD)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
t0=$(date +%s)
fit() {   # fit <init> <forms...>
  local init=$1; shift
  python -u -m pilot.compactst_run --up "$UP" --city "$D" --forms "$@" --seeds ${SEEDS:-999} --share "${SHARE:-0.05}" \
    --init "$init" ${MAX_EPOCHS:+--max-epochs "$MAX_EPOCHS"} --out "$R/${OUT_SUB:-fit}" 2>&1 \
    | tee -a "$R/log_${OUT_SUB:-fit}_$SLURM_JOB_ID.txt" | grep --line-buffered -E "^done|^skip|^The number|Error|Traceback|error"
  [ "${PIPESTATUS[0]}" -eq 0 ] || { echo "failed: city $D, start $init"; failed=1; }
}
failed=0
for D in ${DATASETS:-$DATASET}; do
  R="$REPO/results/compactst/${D}_in96_out48"; mkdir -p "$R"
  name=$(python -c "from pilot.compactst_data import CITIES; print(CITIES['$D'][0])")
  echo "city $D ($(( $(date +%s) - t0 )) s)"
  [ -s "$NAS_DATA_ROOT/compactst/data/$name.dat" ] || python -m pilot.compactst_data --city "$D" --shares 0.05 1.0 | tee "$R/data_$SLURM_JOB_ID.txt"
  forms="${FORMS-C0}"
  [ -n "$forms" ] && fit "${INIT:-pretrained}" $forms
  [ -n "$RANDOM_FORMS" ] && fit random $RANDOM_FORMS
done
echo "elapsed $(( $(date +%s) - t0 )) s"
echo "end $(date -Is)"
exit $failed
