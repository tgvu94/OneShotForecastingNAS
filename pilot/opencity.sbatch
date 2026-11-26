#!/usr/bin/env bash
# OpenCity with its released code and weights at one city (Survey/experiments/opencity-plan.md).
#   DATASET   one city of pilot.opencity_run (cd_didi | sz_didi; sd | ca_d6 | ca_d10 after pilot.opencity_data)
#   DATASETS  a space list of cities that replaces DATASET; one process per city
#   SIZES     a space list of mini | base | plus (default mini)
#   FORMS     a space list of forms of the adaptation (default H0, the released fit; H8 is zero-shot); see pilot/opencity_run.py.
#             FORMS="" skips the runs from the released weights.
#   RANDOM_FORMS  a space list of forms that also run from a random start (default none)
#   SEEDS     a space list (default 12, the seed of the released configuration)
#   SHARE     the share of the training split (default 1);  SHARES  a space list that replaces SHARE, in the given order;
#   DAYS      the first days of the series (default all);
#   MAX_EPOCHS;  BATCH_SIZE (default 64);  OUT_SUB (default fit)
# The upstream tree is $NAS_ROOT/OpenCity (pilot/opencity_setup.sh).  A finished run is skipped.  The job ends with status 1
# when a fit of a city fails; the other cities still run.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"
REPO="$PWD"; UP="$NAS_ROOT/OpenCity"
echo "start $(date -Is) host $(hostname) commit $(git rev-parse --short HEAD) upstream $(git -C "$UP" rev-parse --short HEAD)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
t0=$(date +%s)
fit() {   # fit <init> <forms...>
  local init=$1; shift
  python -u -m pilot.opencity_run --up "$UP" --city "$D" --sizes ${SIZES:-mini} --forms "$@" --seeds ${SEEDS:-12} --share "$G" \
    --days "${DAYS:-0}" --init "$init" ${MAX_EPOCHS:+--max-epochs "$MAX_EPOCHS"} ${BATCH_SIZE:+--batch-size "$BATCH_SIZE"} \
    --out "$R/${OUT_SUB:-fit}" 2>&1 \
    | tee -a "$R/log_${OUT_SUB:-fit}_$SLURM_JOB_ID.txt" | grep --line-buffered -E "^done|^skip|^no training|Error|Traceback|error"
  [ "${PIPESTATUS[0]}" -eq 0 ] || { echo "failed: city $D, start $init"; failed=1; }
}
failed=0
for D in ${DATASETS:-$DATASET}; do
  R="$REPO/results/opencity/${D}_in1day_out1day"; mkdir -p "$R"
  echo "city $D ($(( $(date +%s) - t0 )) s)"
  forms="${FORMS-H0}"
  for G in ${SHARES:-${SHARE:-1}}; do
    echo "share $G ($(( $(date +%s) - t0 )) s)"
    [ -n "$forms" ] && fit "${INIT:-pretrained}" $forms
    [ -n "${RANDOM_FORMS:-}" ] && fit random $RANDOM_FORMS
  done
done
echo "elapsed $(( $(date +%s) - t0 )) s"
echo "end $(date -Is)"
exit $failed
