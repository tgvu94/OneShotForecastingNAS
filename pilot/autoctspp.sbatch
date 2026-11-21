#!/usr/bin/env bash
# AutoCTS++ with its released code at PEMS-BAY (Survey/experiments/autoctspp-plan.md).  STEPS is a space list:
#   feature   the task embedding of the released script (TS2Vec, 20 epochs, 100 samples), timed; its encode step holds the
#             embedding of every sensor and step in memory (325 sensors: above 32 GB), so submit with MEM=96G
#   search    the released zero-shot search with the released comparator (SAMPLE_SCALE candidates, default 300000), timed;
#             writes results/autoctspp/<city>_p<P>/searched.npy
#   train     pilot.autoctspp_run train on ARCHS (default: searched.npy) with SEEDS, EPOCHS, EVAL_BATCH, SHARD, LIMIT, OUT_SUB
# The upstream tree is $NAS_ROOT/AutoCTS_plusplus (pilot/autoctspp_setup.sh).  A finished run is skipped.
source "$SLURM_SUBMIT_DIR/pilot/env.sh"
REPO="$PWD"; UP="$NAS_ROOT/AutoCTS_plusplus"; P="${SEQ_LEN:-12}"; R="$REPO/results/autoctspp/${DATASET:-pemsbay}_p$P"
mkdir -p "$R"
echo "start $(date -Is) host $(hostname) commit $(git rev-parse --short HEAD) upstream $(git -C "$UP" rev-parse --short HEAD) steps ${STEPS:-train}"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
export PYTHONPATH="$UP:$REPO:$PYTHONPATH"
for step in ${STEPS:-train}; do
  t0=$(date +%s)
  case "$step" in
    feature) (cd "$UP/scripts" && python -u -m pilot.autoctspp_upstream ../exps/generate_task_feature.py --dataset PEMS-BAY/pems-bay run --loader h5 --repr_dims 256 --seq_len "$P" --sample_num 100 --epochs 20 --ratio 0.7 0.1 0.2 2>&1 | tee "$R/log_feature.txt" | grep -E "Training time|Finished|Error|Traceback" | tail -5)
             cp "$UP/task_feature/PEMS-BAY/pems-bay/${P}_ts2vec_task_feature.npy" "$R/task_feature.npy" || { echo "step $step failed; the later steps do not run"; break; } ;;
    search)  (cd "$UP/scripts" && python -u -m pilot.autoctspp_upstream ../exps/random_search.py --dataset PEMS-BAY/pems-bay --mode search --exp_id 0 --sample_scale "${SAMPLE_SCALE:-300000}" --seq_len "$P" 2>&1 | tee "$R/log_search.txt" | grep -E "pred time|^\[\[|Error|Traceback" | tail -5)
             cp "$UP/results/searched_archs/PEMS-BAY/pems-bay/${P}_param_0.npy" "$R/searched.npy" || { echo "step $step failed; the later steps do not run"; break; } ;;
    train)   for eb in ${EVAL_BATCH:-1}; do      # more than one value: one output folder per value (a timing of the evaluation)
               sub="${OUT_SUB:-train}"; [ "${EVAL_BATCH:-1}" != "$eb" ] && sub="${sub}_evalbatch$eb"
               python -m pilot.autoctspp_run train --up "$UP" --seq-len "$P" --archs "${ARCHS:-$R/searched.npy}" --seeds ${SEEDS:-0} --epochs "${EPOCHS:-100}" \
                 --eval-batch "$eb" ${SHARD:+--shard "$SHARD"} ${LIMIT:+--limit "$LIMIT"} --out "$R/$sub" 2>&1 | tee "$R/log_$sub.txt" | grep -E "^data|^done|^skip|Error|Traceback|error"
             done ;;
    *) echo "unknown step $step" ;;
  esac
  echo "step $step elapsed $(( $(date +%s) - t0 )) s"
done
echo "end $(date -Is)"
