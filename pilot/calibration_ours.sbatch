#!/usr/bin/env bash
# Architectures under OUR pipeline (pilot.train_arch, benchst protocol) with settings of the trainer changed
# (Survey/experiments/calibration-plan.md).  A variant is a list of Hydra overrides, and a repair of the clock when its name
# ends in "clock":
#   base        none: the stored run, on this cluster
#   noinstnorm  train.targe_scaler=none       no standardisation of a window over its 96 steps
#   clip5       train.grad_clip=5.0           the clip norm of the published protocol
#   both        the two together
#   both_noamp  the two, and train.amp_enable=false
#   clock, noinstnorm_clock                   the time features follow the clock of the data (pilot/calibration_ours.py)
# Output: results/calibration/<city>/<OUT_SUB>/<variant>/<arch>/seed<s>/ (metrics.json; forecast_test.npy with DUMP=1).  A run
# with metrics.json is skipped.  ROOT (the root that holds archs.jsonl and data/) and DATASET come from pilot/submit.sh.
# Optional: VARIANTS, SEEDS, ARCH_FILE (a file with one arch_id per line, the first column of a csv; default stid_trueclock),
# SHARD=k/n (every n-th architecture of the file from the k-th), OUT_SUB (default ours), DUMP (default 1),
# PATIENCE (epochs of the early stop, default 5; 20 = every run has 20 epochs).
source "$SLURM_SUBMIT_DIR/pilot/env.sh"
DATASET="${DATASET:-metrla}"; ROOT="${ROOT:-results/fmroute/${DATASET}_h12}"; OUT_SUB="${OUT_SUB:-ours}"
if [ -n "${ARCH_FILE:-}" ]; then archs=$(grep -v "^arch_id\|^#" "$ARCH_FILE" | cut -d, -f1); else archs=stid_trueclock; fi
if [ -n "${SHARD:-}" ]; then archs=$(echo "$archs" | awk -v k="${SHARD%/*}" -v n="${SHARD#*/}" 'NR % n == k'); fi
dump=(--dump-forecasts); [ "${DUMP:-1}" = 0 ] && dump=()
echo "start $(date -Is) host $(hostname) dataset $DATASET root $ROOT commit $(git rev-parse --short HEAD) archs $(echo $archs | wc -w) shard ${SHARD:-none}"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
for v in ${VARIANTS:-base noinstnorm clip5 both both_noamp}; do
  case "${v%_clock}" in
    base|clock) ov="" ;; noinstnorm) ov="train.targe_scaler=none" ;; clip5) ov="train.grad_clip=5.0" ;;
    both) ov="train.targe_scaler=none train.grad_clip=5.0" ;;
    both_noamp) ov="train.targe_scaler=none train.grad_clip=5.0 train.amp_enable=false" ;;
    *) echo "unknown variant $v"; continue ;;
  esac
  clock=0; case "$v" in *clock) clock=1 ;; esac
  for a in $archs; do
    for s in ${SEEDS:-0 1 2}; do
      out=results/calibration/$DATASET/$OUT_SUB/$v
      if [ -s "$out/$a/seed$s/metrics.json" ]; then echo "skip $DATASET $v $a seed $s"; continue; fi
      t0=$(date +%s)
      CALIB_OVERRIDES="$ov" CALIB_TRUE_CLOCK=$clock python -m pilot.calibration_ours --arch-id "$a" --seed "$s" --epochs 20 --patience "${PATIENCE:-5}" --min-epochs 8 \
        --root "$ROOT" --dataset "$DATASET" --horizon 12 --out-root "$out" --prune-ckpt --mask-zeros "${dump[@]}" 2>&1 \
        | grep -E "^config overrides|^true clock|^done|^forecast dump test|Error|Traceback" | tail -6
      if [ -s "$out/$a/seed$s/metrics.json" ]; then echo "run $DATASET $v $a seed $s elapsed $(( $(date +%s) - t0 )) s"; else echo "FAILED $DATASET $v $a seed $s"; fi
    done
  done
done
echo "end $(date -Is)"
