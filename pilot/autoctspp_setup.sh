#!/usr/bin/env bash
# Puts the released code of AutoCTS++ next to the nas tree and links the PEMS-BAY files where that code reads them
# (Survey/experiments/autoctspp-plan.md).  Run on a login node (it needs the network).  Idempotent.
#   $NAS_ROOT/AutoCTS_plusplus                      the upstream repository at commit $AUTOCTSPP_COMMIT, unchanged
#   $NAS_ROOT/AutoCTS_plusplus/data/PEMS-BAY/       pems-bay.h5 and adj_mx_bay.pkl, links into $NAS_DATA_ROOT/PEMS
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/env.sh"
UP="$NAS_ROOT/AutoCTS_plusplus"; COMMIT="${AUTOCTSPP_COMMIT:-1dd7db4}"
if [ ! -d "$UP/.git" ]; then git clone -q https://github.com/decisionintelligence/AutoCTS_plusplus "$UP"; fi
git -C "$UP" checkout -q "$COMMIT"
for f in PEMS-BAY.h5 adj_mx_bay.pkl; do [ -s "$NAS_DATA_ROOT/PEMS/$f" ] || { echo "missing $NAS_DATA_ROOT/PEMS/$f"; exit 1; }; done
mkdir -p "$UP/data/PEMS-BAY"
ln -sfn "$NAS_DATA_ROOT/PEMS/PEMS-BAY.h5" "$UP/data/PEMS-BAY/pems-bay.h5"
ln -sfn "$NAS_DATA_ROOT/PEMS/adj_mx_bay.pkl" "$UP/data/PEMS-BAY/adj_mx_bay.pkl"
echo "upstream $(git -C "$UP" rev-parse --short HEAD) at $UP"; ls -l "$UP/data/PEMS-BAY" "$UP/NAS_Net/AHC/AHC_param"
