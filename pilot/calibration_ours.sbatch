#!/usr/bin/env bash
# stid_trueclock under OUR pipeline (pilot.train_arch, benchst protocol) with the settings of the trainer that the parts runs
# name as causes taken out (Survey/experiments/calibration-plan.md).  A variant is a list of Hydra overrides:
#   base        none: the stored run of results/fmroute/<city>_h12, on this cluster
#   noinstnorm  train.targe_scaler=none       no standardisation of a window over its 96 steps
#   clip5       train.grad_clip=5.0           the clip norm of the published protocol
#   both        the two together
#   both_noamp  the two, and train.amp_enable=false
# Output: results/calibration/<city>/ours/<variant>/stid_trueclock/seed<s>/ (metrics.json, forecast_test.npy).  A run with
# metrics.json is skipped.  ROOT (the root that holds archs.jsonl with stid_trueclock) and DATASET come from pilot/submit.sh;
# VARIANTS and SEEDS override the defaults.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"
DATASET="${DATASET:-metrla}"; ROOT="${ROOT:-results/fmroute/${DATASET}_h12}"
echo "start $(date -Is) host $(hostname) dataset $DATASET root $ROOT commit $(git rev-parse --short HEAD)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
for v in ${VARIANTS:-base noinstnorm clip5 both both_noamp}; do
  case "$v" in
    base) ov="" ;; noinstnorm) ov="train.targe_scaler=none" ;; clip5) ov="train.grad_clip=5.0" ;;
    both) ov="train.targe_scaler=none train.grad_clip=5.0" ;;
    both_noamp) ov="train.targe_scaler=none train.grad_clip=5.0 train.amp_enable=false" ;;
    *) echo "unknown variant $v"; continue ;;
  esac
  for s in ${SEEDS:-0 1 2}; do
    out=results/calibration/$DATASET/ours/$v
    if [ -s "$out/stid_trueclock/seed$s/metrics.json" ]; then echo "skip $DATASET $v seed $s"; continue; fi
    t0=$(date +%s)
    CALIB_OVERRIDES="$ov" python -m pilot.calibration_ours --arch-id stid_trueclock --seed "$s" --epochs 20 --patience 5 --min-epochs 8 \
      --root "$ROOT" --dataset "$DATASET" --horizon 12 --out-root "$out" --prune-ckpt --mask-zeros --dump-forecasts ${OURS_EXTRA:-} 2>&1 \
      | grep -E "^config overrides|^done|^forecast dump test|Error|Traceback" | tail -6
    if [ -s "$out/stid_trueclock/seed$s/metrics.json" ]; then echo "run $DATASET $v seed $s elapsed $(( $(date +%s) - t0 )) s"; else echo "FAILED $DATASET $v seed $s"; fi
  done
done
echo "end $(date -Is)"
