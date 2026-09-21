#!/usr/bin/env bash
# Experiment B for one root: base proxies under A and the 8 permuted adjacencies for every arch (no training).
# ROOT / DATASET / HORIZON come from the environment (pilot/submit.sh exports them); defaults = the Pilot 1 tree.
source "$HOME/nas/OneShotForecastingNAS/pilot/env.sh"
ROOT="${ROOT:-results}"; DATASET="${DATASET:-pems04}"; HORIZON="${HORIZON:-12}"
setting=(--root "$ROOT" --dataset "$DATASET" --horizon "$HORIZON")
tag="${DATASET}_h${HORIZON}"
echo "spatial job $SLURM_JOB_ID on $(hostname) root $ROOT ($tag) start $(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
python -m pilot.permute_adj "${setting[@]}" --k 8 --seed 0 2>&1 | tee -a "logs/perm_${tag}.log"
python -m pilot.score_spatial "${setting[@]}" --base nwot,zico,grad_norm_all,snip_all --seeds 0,1,2 2>&1 | tee -a "logs/spatial_${tag}.log" | grep -v "Warning\|warn\|W0[0-9]\|coefficients\|_VF"
if [ -d "$HOME/nas/TFAS" ]; then
  python -m pilot.tfas_probe "${setting[@]}" --tfas "$HOME/nas/TFAS" --seeds 0,1,2 2>&1 | tee -a "logs/tfas_${tag}.log" | grep -v "Warning\|warn\|W0[0-9]\|coefficients\|_VF" | tail -3
fi
python -m pilot.check --phase 7 --root "$ROOT" 2>&1 | grep -v "Warning\|warn\|W0[0-9]\|coefficients\|_VF" | tee -a "logs/check7_${tag}.log"
echo "spatial job end $(date -Is)"
