#!/usr/bin/env bash
# Phase 7, Experiment B: base proxies under A and the 8 permuted adjacencies for the frozen 50 (no training).
source "$HOME/nas/OneShotForecastingNAS/pilot/env.sh"
echo "spatial job $SLURM_JOB_ID on $(hostname) start $(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
python -m pilot.permute_adj --adj results/data/pems04_adj.npy --k 8 --seed 0 2>&1 | tee -a logs/p7_perm.log
python -m pilot.score_spatial --archs results/archs.jsonl --base nwot,zico,grad_norm_all,snip_all --seeds 0,1,2 \
       --perms results/data/pems04_adj_perm_*.npy --out results/proxies/spatial_v2 2>&1 | tee -a logs/p7_spatial.log | grep -v "Warning\|warn\|W0[0-9]\|coefficients\|_VF"
python -m pilot.tfas_probe --tfas "$HOME/nas/TFAS" --seeds 0,1,2 2>&1 | tee -a logs/p7_tfas.log | grep -v "Warning\|warn\|W0[0-9]\|coefficients\|_VF" | tail -3
python -m pilot.check --phase 7 2>&1 | grep -v "Warning\|warn\|W0[0-9]\|coefficients\|_VF" | tee -a logs/p7_check.log
echo "spatial job end $(date -Is)"
