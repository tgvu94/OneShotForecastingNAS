#!/usr/bin/env bash
# Puts the released code of CompactST next to the nas tree (Survey/experiments/compactst-plan.md).
# Run on a login node (it needs the network).  Idempotent.
#   $NAS_ROOT/CompactST                      the upstream repository at commit $COMPACTST_COMMIT, unchanged
#   $NAS_ROOT/CompactST/checkpoint/stmixer.pt   the released pre-trained weights (949,830 bytes)
# The dataset files in the format of its loader come from:  python -m pilot.compactst_data --city <city>
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/env.sh"
UP="$NAS_ROOT/CompactST"; COMMIT="${COMPACTST_COMMIT:-9c4300c}"
if [ ! -d "$UP/.git" ]; then git clone -q https://github.com/usail-hkust/CompactST "$UP"; fi
git -C "$UP" checkout -q "$COMMIT"
[ "$(stat -c %s "$UP/checkpoint/stmixer.pt")" = 949830 ] || { echo "checkpoint/stmixer.pt has an unexpected size"; exit 1; }
echo "upstream $(git -C "$UP" rev-parse --short HEAD) at $UP"; ls -l "$UP/checkpoint"
