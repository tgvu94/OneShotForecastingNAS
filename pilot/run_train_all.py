"""Resumable runner (Section 4.2): loops archs x seeds, skips finished runs, LOCKs the one it is on, and calls
``pilot.train_arch`` in a subprocess so one crash never kills the batch.  Safe to run several copies side by side
(each skips fresh LOCKs); ``--shard k/n`` additionally partitions the (arch, seed) list.

    python -m pilot.run_train_all --root results --seeds 0,1,2 --max-epochs 20 --patience 5
    python -m pilot.run_train_all --root results/pems08_h12 --seeds 0 --max-epochs 20 --patience 5 --shard 0/2
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from pilot.genotype import load_archs
from pilot.paths import Root


def lock_is_fresh(lock: Path, minutes: float) -> bool:
    try:
        pid, ts = lock.read_text().split()[:2]
        fresh = time.time() - float(ts) < minutes * 60
        alive = _pid_alive(int(pid))
        return fresh and alive
    except Exception:  # noqa: BLE001
        return False


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    Root.add_args(ap)
    ap.add_argument("--archs", default=None, help="default: <root>/archs.jsonl")
    ap.add_argument("--seeds", default="0")
    ap.add_argument("--max-epochs", type=int, default=20)
    ap.add_argument("--patience", type=int, default=5)
    ap.add_argument("--min-epochs", type=int, default=8)
    ap.add_argument("--out-root", default=None, help="default: <root>/train")
    ap.add_argument("--limit", type=int, default=None, help="first N archs only")
    ap.add_argument("--shard", default=None, help="k/n: take every n-th (arch, seed) starting at k")
    ap.add_argument("--retry-failed", action="store_true")
    ap.add_argument("--lock-minutes", type=float, default=90)
    ap.add_argument("--prune-ckpt", action="store_true")
    ap.add_argument("--extra", default="", help="extra args passed through to pilot.train_arch")
    args = ap.parse_args(argv)
    root = Root.from_args(args)
    args.archs = str(args.archs or root.archs_jsonl)
    args.out_root = str(args.out_root or root.train)

    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    archs = load_archs(args.archs)
    if args.limit:
        archs = archs[: args.limit]
    jobs = [(r["arch_id"], s) for r in archs for s in seeds]
    if args.shard:
        k, n = (int(v) for v in args.shard.split("/"))
        jobs = jobs[k::n]
    print(f"{len(jobs)} (arch, seed) jobs; max_epochs={args.max_epochs} patience={args.patience} pid={os.getpid()}")

    n_done = n_skip = n_run = n_fail = 0
    for aid, seed in jobs:
        d = Path(args.out_root) / aid / f"seed{seed}"
        d.mkdir(parents=True, exist_ok=True)
        m, lock = d / "metrics.json", d / "LOCK"
        if m.exists():
            try:
                status = json.load(open(m)).get("status")
            except Exception:  # noqa: BLE001
                status = "corrupt"
            if status == "done":
                n_done += 1
                continue
            if status == "failed" and not args.retry_failed:
                print(f"{aid} seed {seed}: failed earlier; pass --retry-failed to retry")
                n_skip += 1
                continue
        if lock.exists() and lock_is_fresh(lock, args.lock_minutes):
            print(f"{aid} seed {seed}: LOCK held by another runner -> skip")
            n_skip += 1
            continue
        lock.write_text(f"{os.getpid()} {time.time()}\n")
        cmd = [sys.executable, "-m", "pilot.train_arch", "--arch-id", aid, "--seed", str(seed),
               "--epochs", str(args.max_epochs), "--patience", str(args.patience), "--min-epochs", str(args.min_epochs),
               "--root", str(root.dir), "--dataset", root.dataset, "--horizon", str(root.horizon),
               "--archs", args.archs, "--out-root", args.out_root] + (["--prune-ckpt"] if args.prune_ckpt else []) \
              + args.extra.split()
        print(f"=== {_dt.datetime.now().isoformat(timespec='seconds')} {aid} seed {seed}: {' '.join(cmd[2:])}", flush=True)
        t0 = time.time()
        try:
            cp = subprocess.run(cmd, text=True, capture_output=True)
            tail = (cp.stdout[-3000:] + "\n" + cp.stderr[-3000:])
            (d / "runner.log").write_text(tail)
            status = json.load(open(m)).get("status") if m.exists() else None
            if cp.returncode != 0 or status not in ("done", "failed"):
                rec = json.load(open(m)) if m.exists() else {"arch_id": aid, "seed": seed}
                rec.update({"status": "failed", "error": f"train_arch rc={cp.returncode}, status={status}",
                            "stderr_tail": cp.stderr[-2000:]})
                m.write_text(json.dumps(rec, indent=2))
                n_fail += 1
                print(f"    FAILED rc={cp.returncode}: {cp.stderr.strip().splitlines()[-1] if cp.stderr.strip() else ''}")
            else:
                n_run += 1
                rec = json.load(open(m))
                print(f"    {status}: epochs={rec.get('epochs_run')} val_mae={rec.get('val_mae')} "
                      f"test_mae={rec.get('test_mae')} in {time.time() - t0:.0f}s", flush=True)
        finally:
            lock.unlink(missing_ok=True)
    print(f"finished: {n_run} trained now, {n_done} already done, {n_skip} skipped, {n_fail} failed")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
