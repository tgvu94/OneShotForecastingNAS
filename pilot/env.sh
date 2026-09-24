# Source this in every shell / tmux window / job that runs pilot code:   source pilot/env.sh
# Self-locating: the repo is the parent of this file's directory; the datasets sit next to the nas tree
# (…/nas/OneShotForecastingNAS, …/all_datasets).  The venv is $NAS_VENV, else …/nas/.venv, else ~/nas-venv: on Nibi it
# stays in $HOME because the project filesystem handles small files slowly (measured 2026-09-24: ~4 creates/s, reads
# 4x slower than home), which would hurt every Python start.  Nothing here depends on ~/nas.
NAS_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export NAS_ROOT="$(dirname "$NAS_REPO")"
if [ -z "${NAS_DATA_ROOT:-}" ]; then
  if [ -d "$NAS_ROOT/../all_datasets" ]; then export NAS_DATA_ROOT="$(cd "$NAS_ROOT/../all_datasets" && pwd)"
  else export NAS_DATA_ROOT="$HOME/scratch/all_datasets"; fi      # legacy layout (Fir until it is moved)
fi
if [ -n "${NAS_VENV:-}" ]; then VENV="$NAS_VENV"
elif [ -d "$NAS_ROOT/.venv" ]; then VENV="$NAS_ROOT/.venv"
else VENV="$HOME/nas-venv"; fi
export NAS_VENV="$VENV"
source "$VENV/bin/activate"
cd "$NAS_REPO"
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$PWD"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export HYDRA_FULL_ERROR=1
export WANDB_MODE=disabled          # the repo imports wandb; without this it prompts for a login
export TQDM_DISABLE=1               # keeps the per-batch progress bars out of the logs
mkdir -p "$NAS_ROOT/logs" logs results/archs results/proxies results/train results/tables results/figs results/data
