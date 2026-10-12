#!/usr/bin/env bash
# Score zero-cost proxies for one or more roots without training (idempotent: names already stored are skipped).
# ROOT / DATASET / HORIZON / EXTRA_ROOTS / PROXIES come from the environment (pilot/submit.sh exports them).
# PROXIES defaults to "all": the scorer then computes only the (name, seed) pairs that are missing from each stored file.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"     # submit.sh submits from the repo root
ROOT="${ROOT:-results/stzero/pems04_h12}"; DATASET="${DATASET:-pems04}"; HORIZON="${HORIZON:-12}"
PROXIES="${PROXIES:-all}"
echo "proxies job $SLURM_JOB_ID on $(hostname) roots $ROOT $EXTRA_ROOTS proxies $PROXIES start $(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
for root in $ROOT $EXTRA_ROOTS; do
  tag="$(basename "$root")"
  python -m pilot.score_proxies --root "$root" --proxies "$PROXIES" --seeds 0,1,2 2>&1 | tee -a "logs/proxies_${tag}.log" | grep -v "Warning\|warn\|W0[0-9]\|coefficients\|_VF" | grep -v "present -> skip" | tail -5
  python -m pilot.check --check proxies --root "$root" 2>&1 | tail -3 | tee -a "logs/check_proxies_${tag}.log"
done
echo "proxies job end $(date -Is)"
