# Source this in every shell / tmux window that runs pilot code:  source pilot/env.sh
source ~/nas/.venv/bin/activate
cd ~/nas/OneShotForecastingNAS
export PYTHONPATH="$PYTHONPATH:$PWD"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export HYDRA_FULL_ERROR=1
export WANDB_MODE=disabled          # the repo imports wandb; without this it prompts for a login
export TQDM_DISABLE=1               # keeps the per-batch progress bars out of the logs
mkdir -p logs results/archs results/proxies results/train results/tables results/figs results/data
