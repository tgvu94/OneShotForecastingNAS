"""Weekly pass/fail checks.  ``python -m pilot.check --week 1``  -> prints PASS or FAIL, exit code 0/1."""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from pathlib import Path


def _ok(flag: bool, msg: str) -> bool:
    print(("  [ok]   " if flag else "  [FAIL] ") + msg)
    return flag


def week1(args) -> bool:
    import torch

    from pilot.build_net import build_discrete_net
    from pilot.data import load_probe_batch
    from pilot.genotype import arch_id, genotype_from_meta, load_archs

    good = True
    archs_path = Path(args.archs)
    good &= _ok(archs_path.exists(), f"{archs_path} exists")
    if not archs_path.exists():
        return False
    archs = load_archs(archs_path)
    good &= _ok(len(archs) >= 1, f"{len(archs)} architecture(s) in {archs_path}")

    probe_path = Path(args.probe)
    good &= _ok(probe_path.exists(), f"probe batch {probe_path} exists")
    if not probe_path.exists():
        return False
    probe, sha1 = load_probe_batch(probe_path)
    b0 = probe["batches"][0]
    good &= _ok(len(probe["batches"]) == 4 and b0["x_past"].dim() == 3,
                f"probe batch: {len(probe['batches'])} batches, x_past {tuple(b0['x_past'].shape)}, sha1 {sha1[:12]}")

    for rec in archs[: args.limit]:
        g, aid = rec["genotype"], rec["arch_id"]
        # 1) genotype round trip through the built network
        good &= _ok(arch_id(g) == aid, f"{aid}: stored arch_id matches hash of stored genotype")
        net = build_discrete_net(g, probe["dims"])
        g2 = genotype_from_meta(net.meta_info, g["space"])
        good &= _ok(arch_id(g2) == aid, f"{aid}: genotype -> build_net -> meta_info -> genotype gives the same arch_id")
        with torch.no_grad():
            out = net(b0["x_past"], b0["x_future"])
        out = out[-1] if isinstance(out, (list, tuple)) else out
        good &= _ok(tuple(out.shape) == tuple(b0["target"].shape),
                    f"{aid}: CPU forward gives {tuple(out.shape)} == target {tuple(b0['target'].shape)}")
        # 2) proxies
        ppath = Path(args.proxies_dir) / f"{aid}.json"
        good &= _ok(ppath.exists(), f"{aid}: proxy file {ppath} exists")
        if ppath.exists():
            p = json.load(open(ppath))
            for name in ["params", "grad_norm_all", "nwot"]:
                v = p.get("scores", {}).get(name, {}).get("0")
                good &= _ok(v is not None and math.isfinite(v), f"{aid}: {name}[seed 0] = {v}")
            good &= _ok(p.get("probe_batch_sha1") == sha1, f"{aid}: proxy file records the current probe sha1")
        # 3) training
        mpath = Path(args.train_dir) / aid / f"seed{args.seed}" / "metrics.json"
        good &= _ok(mpath.exists(), f"{aid}: {mpath} exists")
        if mpath.exists():
            m = json.load(open(mpath))
            good &= _ok(m.get("status") == "done", f"{aid}: status = {m.get('status')}")
            good &= _ok(m.get("epochs_run") == args.epochs, f"{aid}: epochs_run = {m.get('epochs_run')} (expected {args.epochs})")
            for k in ["val_mae", "test_mae"]:
                v = m.get(k)
                good &= _ok(v is not None and math.isfinite(v), f"{aid}: {k} = {v}")
            for f in ["log.csv", "ckpt.pt"]:
                good &= _ok((mpath.parent / f).exists(), f"{aid}: {f} exists")
        # 4) idempotent re-run
        t0 = time.time()
        cp = subprocess.run([sys.executable, "-m", "pilot.train_arch", "--arch-id", aid, "--epochs", str(args.epochs),
                             "--seed", str(args.seed), "--archs", str(archs_path), "--out-root", args.train_dir],
                            capture_output=True, text=True)
        dt = time.time() - t0
        good &= _ok(cp.returncode == 0 and "already done" in cp.stdout and dt < 5.0,
                    f"{aid}: second train_arch call exits in {dt:.1f}s with 'already done' (rc={cp.returncode})")
    return bool(good)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--archs", default="results/archs.jsonl")
    ap.add_argument("--probe", default="results/data/pems04_probe_batch.pt")
    ap.add_argument("--proxies-dir", default="results/proxies/v1")
    ap.add_argument("--train-dir", default="results/train")
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--limit", type=int, default=1)
    args = ap.parse_args()
    checks = {1: week1}
    if args.week not in checks:
        raise SystemExit(f"no check for week {args.week}; have {sorted(checks)}")
    print(f"== pilot.check week {args.week}")
    ok = checks[args.week](args)
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
