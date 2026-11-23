#!/usr/bin/env bash
# CompactST with its released code and weights at one city (Survey/experiments/compactst-plan.md).
#   DATASET   chengdu | shenzhen | sd | gba (the files of pilot.compactst_data must exist)
#   FORMS     a space list of forms of the adaptation (default C0, the released form); see pilot/compactst_run.py
#   SEEDS     a space list (default 999, the seed of the released script)
#   SHARE     the share of the training split (default 0.05);  INIT  pretrained | random;  MAX_EPOCHS;  OUT_SUB (default fit)
# The upstream tree is $NAS_ROOT/CompactST (pilot/compactst_setup.sh).  A finished run is skipped.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"
REPO="$PWD"; UP="$NAS_ROOT/CompactST"; R="$REPO/results/compactst/${DATASET}_in96_out48"
mkdir -p "$R"
echo "start $(date -Is) host $(hostname) commit $(git rev-parse --short HEAD) upstream $(git -C "$UP" rev-parse --short HEAD)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
t0=$(date +%s)
python -u -m pilot.compactst_run --up "$UP" --city "$DATASET" --forms ${FORMS:-C0} --seeds ${SEEDS:-999} --share "${SHARE:-0.05}" \
  --init "${INIT:-pretrained}" ${MAX_EPOCHS:+--max-epochs "$MAX_EPOCHS"} --out "$R/${OUT_SUB:-fit}" 2>&1 \
  | tee -a "$R/log_${OUT_SUB:-fit}_$SLURM_JOB_ID.txt" | grep -E "^done|^skip|^epoch|^The number|Error|Traceback|error"
echo "elapsed $(( $(date +%s) - t0 )) s"
echo "end $(date -Is)"
