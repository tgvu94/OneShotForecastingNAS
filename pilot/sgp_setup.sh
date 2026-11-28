#!/usr/bin/env bash
# Puts the released code of SGP [cini2023sgp] next to the nas tree (Survey/experiments/sgp-plan.md).  Run on a login node (it
# needs the network).  Idempotent.  The runner pilot/sgp_run.py does not import this tree: its venv lacks the packages that the
# release needs.  `python -m pilot.sgp_run check` reads the reservoir source of the tree and compares it with the runner.
#   $NAS_ROOT/sgp      the upstream repository at commit $SGP_COMMIT, unchanged
# The files of the two cities are the files of the project under $NAS_DATA_ROOT/PEMS (the .h5 with the time stamps, the DCRNN
# graph pickle, the raw distances); the script stops when one is absent.
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/env.sh"
UP="$NAS_ROOT/sgp"; COMMIT="${SGP_COMMIT:-ae1abd5}"
if [ ! -d "$UP/.git" ]; then git clone -q https://github.com/Graph-Machine-Learning-Group/sgp "$UP"; fi
git -C "$UP" checkout -q "$COMMIT"
for f in METR-LA.h5 METR-LA.npz adj_METR-LA.pkl metrla_distances_la_2012.csv PEMS-BAY.h5 PEMS-BAY.npz adj_mx_bay.pkl bay_distances.csv; do
  [ -s "$NAS_DATA_ROOT/PEMS/$f" ] || { echo "absent: $NAS_DATA_ROOT/PEMS/$f"; exit 1; }
done
echo "upstream $(git -C "$UP" rev-parse HEAD) at $UP; data $NAS_DATA_ROOT/PEMS"
