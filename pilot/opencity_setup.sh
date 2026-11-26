#!/usr/bin/env bash
# Puts the released code, weights and DiDi files of OpenCity next to the nas tree (Survey/experiments/opencity-plan.md).
# Run on a login node (it needs the network).  Idempotent.
#   $NAS_ROOT/OpenCity                                   the upstream repository at commit $OPENCITY_COMMIT, unchanged
#   $NAS_ROOT/OpenCity/model_weights/OpenCity/*.pth      the released weights of the three sizes
#   $NAS_DATA_ROOT/opencity/<NAME>/<NAME>.npz, <NAME>_rn_adj.npy   the released files of CD_DIDI and SZ_DIDI
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/env.sh"
UP="$NAS_ROOT/OpenCity"; COMMIT="${OPENCITY_COMMIT:-eca64c9}"; HF=https://huggingface.co
if [ ! -d "$UP/.git" ]; then git clone -q https://github.com/HKUDS/OpenCity "$UP"; fi
git -C "$UP" checkout -q "$COMMIT"
get() {   # get <url> <file> <bytes>
  [ -s "$2" ] && [ "$(stat -c %s "$2")" = "$3" ] && return 0
  curl -sSL --fail -o "$2" "$1"
  [ "$(stat -c %s "$2")" = "$3" ] || { echo "$2 has an unexpected size"; exit 1; }
}
W="$UP/model_weights/OpenCity"; mkdir -p "$W"
get $HF/hkuds/OpenCity-Mini/resolve/main/OpenCity-mini.pth "$W/OpenCity-mini.pth" 6773383
get $HF/hkuds/OpenCity-Base/resolve/main/OpenCity-base.pth "$W/OpenCity-base.pth" 19019847
get $HF/hkuds/OpenCity-Plus/resolve/main/OpenCity-plus.pth "$W/OpenCity-plus.pth" 104163305
D="$NAS_DATA_ROOT/opencity"; mkdir -p "$D"
for pair in CD_DIDI:52716375 SZ_DIDI:68056957; do
  n=${pair%%:*}
  if [ ! -s "$D/$n/$n.npz" ] || [ ! -s "$D/$n/${n}_rn_adj.npy" ]; then
    get $HF/datasets/hkuds/OpenCity-dataset/resolve/main/$n.zip "$D/$n.zip" "${pair##*:}"
    mkdir -p "$D/$n"; unzip -o -q -j "$D/$n.zip" "*$n.npz" "*${n}_rn_adj.npy" -d "$D/$n"
  fi
done
echo "upstream $(git -C "$UP" rev-parse --short HEAD) at $UP"; sha1sum "$W"/*.pth "$D"/*/*.npz "$D"/*/*_rn_adj.npy
