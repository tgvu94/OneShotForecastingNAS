#!/usr/bin/env bash
# Puts the released code of EvoST, its Python environment and the EvoXXLTraffic files of some districts next to the nas tree
# (Survey/experiments/evost-plan.md).  Run on a login node (it needs the network).  Idempotent.
#   $NAS_ROOT/EvoST                                   the upstream repository at commit $EVOST_COMMIT, unchanged
#   $EVOST_VENV (default ~/evost-venv)                torch, PyTorch Geometric, biopython, networkx, tqdm: the baseline pipeline
#                                                     of the upstream tree imports them; the nas venv stays as it is
#   $NAS_DATA_ROOT/evoxxl/hf/...                      the downloaded files, at their paths in the dataset yind7/EvoXXLTraffic
#   $NAS_DATA_ROOT/evoxxl/<district>/RawData/<year>.npz, graph/<year>_adj.npz     links in the layout that the upstream code reads
#   $NAS_DATA_ROOT/evoxxl/sensor_metadata/<district>/<year>/sensor_metadata.csv   sensor IDs in column order, from the catalog
# Env: DISTRICTS (default "pems03 pems06"), YEARS (default "2015 2020 2025"), CACHES=0 leaves out the benchmark caches
# (they serve the data check only).  The data licence is CC BY-NC 4.0.
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/env.sh"
UP="$NAS_ROOT/EvoST"; COMMIT="${EVOST_COMMIT:-afecfd7}"
if [ ! -d "$UP/.git" ]; then git clone -q https://github.com/lixus7/EvoST "$UP"; fi
git -C "$UP" checkout -q "$COMMIT"

EV="${EVOST_VENV:-$HOME/evost-venv}"
if [ ! -x "$EV/bin/python" ]; then
  deactivate 2>/dev/null || true
  module load python/3.11
  virtualenv --no-download "$EV"
  "$EV/bin/pip" install --no-index -q torch==2.14.0 numpy torch_geometric biopython networkx tqdm
fi

D="$NAS_DATA_ROOT/evoxxl"; HF=https://huggingface.co/datasets/yind7/EvoXXLTraffic/resolve/main
get() {   # get <path in the dataset>: download once, then check the SHA-256 of the lists of the dataset
  local f="$D/hf/$1" want
  if [ ! -s "$f" ]; then
    mkdir -p "$(dirname "$f")"
    curl -sSL --fail --retry 3 -o "$f.part" "$HF/$1"; mv "$f.part" "$f"
  fi
  case "$1" in SHA256SUMS*) return 0 ;; esac
  want=$(cat "$D/hf/SHA256SUMS" "$D/hf/SHA256SUMS.full_year" | awk -v p="$1" '$2 == p {print $1; exit}')
  [ -n "$want" ] || { echo "no checksum line for $1"; exit 1; }
  [ "$(sha256sum "$f" | cut -d" " -f1)" = "$want" ] || { echo "checksum of $1 differs from the list"; exit 1; }
}
get SHA256SUMS; get SHA256SUMS.full_year; get full_year/catalog.json
for d in ${DISTRICTS:-pems03 pems06}; do
  mkdir -p "$D/$d/RawData" "$D/$d/graph"
  for y in ${YEARS:-2015 2020 2025}; do
    get "full_year/$d/$y.npz"; get "full_year/$d/graph/${y}_adj.npz"
    ln -sfn "$D/hf/full_year/$d/$y.npz" "$D/$d/RawData/$y.npz"
    ln -sfn "$D/hf/full_year/$d/graph/${y}_adj.npz" "$D/$d/graph/${y}_adj.npz"
    if [ "${CACHES:-1}" = 1 ]; then get "caches/$d/$y/data.npz"; fi
  done
done
"$EV/bin/python" -m pilot.evost_run metadata --districts ${DISTRICTS:-pems03 pems06} --years ${YEARS:-2015 2020 2025}
echo "upstream $(git -C "$UP" rev-parse --short HEAD) at $UP; venv $EV; data $D"
"$EV/bin/python" -c "import torch, numpy, torch_geometric; print('torch', torch.__version__, 'numpy', numpy.__version__, 'torch_geometric', torch_geometric.__version__)"
du -sh "$D/hf" | cut -f1
