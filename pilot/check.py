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


def week2(args) -> bool:
    """All 13 proxies on >= 5 archs: finite and not all equal; nwot hooked; 20-epoch schedule fits in 50 min."""
    import statistics

    from pilot.score_proxies import ORDER, PLAN_NAMES

    good = True
    archs = load_archs_safe(args.archs)
    good &= _ok(len(archs) >= 5, f"{len(archs)} architectures in {args.archs} (need >= 5)")
    archs = archs[:5]
    seeds = [s.strip() for s in args.seeds.split(",")]
    recs = {}
    for rec in archs:
        p = Path(args.proxies_dir) / f"{rec['arch_id']}.json"
        good &= _ok(p.exists(), f"{rec['arch_id']}: proxy file exists")
        if p.exists():
            recs[rec["arch_id"]] = json.load(open(p))
    if not recs:
        return False
    for plan_name, stored in PLAN_NAMES.items():
        for name in stored:
            vals = []
            missing = []
            for aid, r in recs.items():
                for s in seeds:
                    v = r.get("scores", {}).get(name, {}).get(s)
                    if v is None or not math.isfinite(v):
                        missing.append(f"{aid}:{s}={v}")
                    else:
                        vals.append(v)
            means = []
            for aid, r in recs.items():
                vs = [r.get("scores", {}).get(name, {}).get(s) for s in seeds]
                vs = [v for v in vs if v is not None and math.isfinite(v)]
                if vs:
                    means.append(statistics.mean(vs))
            spread = statistics.pstdev(means) if len(means) > 1 else 0.0
            err = next((r["errors"].get(name, {}).get("error", "")[:80] for r in recs.values() if name in r.get("errors", {})), "")
            good &= _ok(not missing and spread > 0,
                        f"{name:14s}: {len(vals)}/{len(recs) * len(seeds)} finite values, std over {len(means)} arch means = {spread:.4g}"
                        + (f"  missing {missing[:3]}" if missing else "") + (f"  err: {err}" if err else ""))
    for aid, r in recs.items():
        for s in seeds:
            nh = r.get("meta", {}).get("nwot", {}).get(s, {}).get("n_hooks")
            good &= _ok(nh is not None and nh > 0, f"{aid} seed {s}: nwot n_hooks = {nh}")
    # timing
    tpath = Path(args.timing_csv)
    good &= _ok(tpath.exists(), f"{tpath} exists")
    if tpath.exists():
        import csv as _csv
        rows = [r for r in _csv.DictReader(open(tpath)) if r.get("status") == "done" and r.get("sec_per_epoch") not in ("", None)]
        good &= _ok(len(rows) >= 1, f"{len(rows)} done runs in timing table")
        if rows:
            spe = max(float(r["sec_per_epoch"]) for r in rows)
            mem = max(float(r["peak_mem_gb"] or 0) for r in rows)
            good &= _ok(spe * 20 <= 50 * 60, f"slowest run {spe:.1f} s/epoch x 20 epochs = {spe * 20 / 60:.1f} min <= 50 min; peak mem {mem:.2f} GB")
    return bool(good)


def load_archs_safe(path):
    from pilot.genotype import load_archs
    return load_archs(path) if Path(path).exists() else []


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
    ap.add_argument("--seeds", default="0,1,2", help="week 2: init seeds expected in the proxy files")
    ap.add_argument("--timing-csv", default="results/tables/timing_w2.csv")
    args = ap.parse_args()
    checks = {1: week1, 2: week2}
    if args.week not in checks:
        raise SystemExit(f"no check for week {args.week}; have {sorted(checks)}")
    print(f"== pilot.check week {args.week}")
    ok = checks[args.week](args)
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
