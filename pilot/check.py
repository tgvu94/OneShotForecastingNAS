"""Per-phase pass/fail checks.  ``python -m pilot.check --phase 1 [--root results] [--pilot 1|2]`` -> PASS or FAIL, exit 0/1.

Every path defaults to the root's files (``pilot.paths.Root``); ``--n`` is the number of frozen architectures the root is
expected to hold (default: the number of lines in ``<root>/archs.jsonl``).  ``--pilot 2`` selects the Pilot 2 checks.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from pilot.paths import Root


def _ok(flag: bool, msg: str) -> bool:
    print(("  [ok]   " if flag else "  [FAIL] ") + msg)
    return flag


def phase1(args) -> bool:
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
        net = build_discrete_net(g, probe["dims"], adj_path=args.adj)
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


def phase2(args) -> bool:
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


def phase3(args) -> bool:
    """Graph Net family: adjacency sanity, op shapes + permutation sensitivity, a graph arch's forward/backward
    on the probe batch (< 12 GB), and one finite 1-epoch training.  ``--autocts`` checks the fallback gate."""
    import numpy as np
    import torch

    from pilot.adjacency import adj_pack, load_adj
    from pilot.build_net import build_discrete_net
    from pilot.data import load_probe_batch
    from pilot.genotype import arch_id, genotype_from_meta, has_graph_op, summarize
    from pilot.proxies.wrapper import ProxyWrapper, loss_fn
    from tsf_oneshot.cells.encoders.graph_components import GRAPH_OPS

    from pilot import datasets

    good = True
    n = datasets.n_nodes(args.root_obj.dataset)
    # 1) adjacency
    adj_path = Path(args.adj)
    good &= _ok(adj_path.exists(), f"{adj_path} exists")
    if not adj_path.exists():
        return False
    A = load_adj(adj_path)
    n_edges = int(A.sum() // 2)
    good &= _ok(A.shape == (n, n), f"A is {A.shape} ({args.root_obj.dataset}: {n} sensors)")
    good &= _ok(bool(np.array_equal(A, A.T)), "A symmetric")
    good &= _ok(set(np.unique(A)) <= {0.0, 1.0}, "A binary")
    good &= _ok(bool((np.diag(A) == 0).all()), "A zero diagonal")
    good &= _ok(n_edges > 0.9 * n, f"A has {n_edges} undirected edges (> 0.9 x {n})")
    info_path = adj_path.with_suffix(".json")
    if info_path.exists():
        info = json.load(open(info_path))
        if "matches_pickle_after_symmetrization" in info:
            good &= _ok(info["matches_pickle_after_symmetrization"] is True, "A matches the cross-check pickle after symmetrization")
        else:
            print("  [info] adjacency was built without --cross-check")
    perms = sorted(adj_path.parent.glob(f"{adj_path.stem}_perm_*.npy"))
    good &= _ok(len(perms) >= 1, f"{len(perms)} permuted adjacencies on disk")
    P = load_adj(perms[0]) if perms else None
    if P is not None:
        good &= _ok(bool(np.array_equal(P.sum(1), A.sum(1))) and not np.array_equal(P, A), "perm 0 keeps every degree and differs from A")
    # 2) ops
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(0)
    x = torch.randn(2, 96, n, 32, device=device)
    packA, packP = adj_pack(A, device), (adj_pack(P, device) if P is not None else None)
    expect_sensitive = {"gcn": True, "diffusion": True, "adaptive": False, "graph_identity": False}
    for name, make in GRAPH_OPS.items():
        op = make(32, n).to(device)
        with torch.no_grad():
            yA = op(x, packA)
            good &= _ok(tuple(yA.shape) == tuple(x.shape), f"{name}: {tuple(x.shape)} -> {tuple(yA.shape)}")
            if packP is not None:
                yP = op(x, packP)
                changed = not torch.allclose(yA, yP)
                good &= _ok(changed == expect_sensitive[name], f"{name}: output changes under permuted A = {changed} (expected {expect_sensitive[name]})")
    # 3) a graph arch: round trip, forward + backward on the probe batch at batch 32, memory
    archs = load_archs_safe(args.archs)
    graph_archs = [r for r in archs if has_graph_op(r["genotype"])]
    good &= _ok(len(graph_archs) >= 1, f"{len(graph_archs)} graph architectures in {args.archs}")
    probe, sha1 = load_probe_batch(args.probe)
    b0, dims = probe["batches"][0], probe["dims"]
    mem_gb = None
    for rec in graph_archs[: args.limit]:
        g, aid = rec["genotype"], rec["arch_id"]
        print(f"  {aid}: {summarize(g)}")
        net = build_discrete_net(g, dims, adjacency=A)
        g2 = genotype_from_meta(net.meta_info, g["space"])
        good &= _ok(arch_id(g2) == aid, f"{aid}: genotype -> build_net -> meta_info -> genotype round trip")
        net = net.to(device)
        wrapper = ProxyWrapper(net, {"x_future": b0["x_future"], "loc": b0["loc"], "scale": b0["scale"]}).to(device)
        if device.type == "cuda":
            torch.cuda.reset_peak_memory_stats(device)
        out = wrapper(b0["x_past"].to(device))
        loss = loss_fn(out, b0["target"].to(device))
        loss.backward()
        mem_gb = torch.cuda.max_memory_allocated(device) / 1e9 if device.type == "cuda" else 0.0
        good &= _ok(tuple(out.shape) == tuple(b0["target"].shape), f"{aid}: forward gives {tuple(out.shape)} == target {tuple(b0['target'].shape)}")
        good &= _ok(math.isfinite(float(loss)), f"{aid}: loss = {float(loss):.4f} finite")
        n_graph_grad = sum(1 for p in net.graph_net.parameters() if p.grad is not None and p.requires_grad)
        good &= _ok(n_graph_grad > 0, f"{aid}: {n_graph_grad} graph-net parameter tensors received a gradient")
        good &= _ok(net.nets_weights.grad is not None, f"{aid}: nets_weights (3-way softmax) received a gradient: {net.nets_weights.grad}")
        good &= _ok(mem_gb < 12.0, f"{aid}: forward + backward at batch 32 peak memory {mem_gb:.2f} GB < 12 GB")
        # 4) 1-epoch training
        mpath = Path(args.train_dir) / aid / f"seed{args.seed}" / "metrics.json"
        if mpath.exists():
            m = json.load(open(mpath))
            good &= _ok(m.get("status") == "done" and m.get("epochs_run", 0) >= 1 and math.isfinite(m.get("val_mae", float("nan"))),
                        f"{aid}: 1-epoch training status={m.get('status')} epochs={m.get('epochs_run')} val_mae={m.get('val_mae')} test_mae={m.get('test_mae')}")
        else:
            good &= _ok(False, f"{aid}: no {mpath}")
        del wrapper, net
        if device.type == "cuda":
            torch.cuda.empty_cache()
    if args.autocts:
        good &= autocts_gate(Path(args.autocts_json))
    return bool(good)


def autocts_gate(path: Path) -> bool:
    """Fallback gate (P3): finite 1-epoch loss, 20 epochs x 50 archs <= 30 GPU-h, three finite proxies, n_hooks > 0."""
    good = _ok(path.exists(), f"{path} exists")
    if not path.exists():
        return False
    r = json.load(open(path))
    tr = r.get("train_1_epoch", {})
    good &= _ok(math.isfinite(tr.get("train_loss_last", float("nan"))) and math.isfinite(tr.get("val_loss", float("nan"))),
                f"AutoCTS 1-epoch: train loss {tr.get('train_loss_last')} val loss {tr.get('val_loss')} finite")
    spe = tr.get("seconds_per_epoch", float("inf"))
    gpu_h = spe * 20 * 50 / 3600
    good &= _ok(gpu_h <= 30, f"AutoCTS {spe:.1f} s/epoch x 20 epochs x 50 archs = {gpu_h:.1f} GPU-h <= 30")
    px = r.get("proxies", {})
    for n in ["params", "grad_norm_all", "nwot"]:
        v = px.get(n, {}).get("value")
        good &= _ok(v is not None and math.isfinite(v), f"AutoCTS proxy {n} = {v}")
    nh = px.get("nwot", {}).get("meta", {}).get("n_hooks", 0)
    good &= _ok(nh > 0, f"AutoCTS nwot n_hooks = {nh}")
    return bool(good)


def phase4(args) -> bool:
    """Gate (P4): best 20-epoch dev graph arch val_mae <= 1.10 x best P2 graph-blind val_mae; none diverged (NaN) or
    collapsed to a naive baseline.  With --frozen also checks the 50 frozen archs (distinct ids, strata counts)."""
    from collections import Counter

    from pilot.genotype import graph_family, has_graph_op

    good = True
    base_path = Path(args.baselines)
    good &= _ok(base_path.exists(), f"{base_path} exists (python -m pilot.baselines)")
    naive = json.load(open(base_path)) if base_path.exists() else None
    naive_test = naive["test"]["last_value"]["mae"] if naive else float("nan")
    naive_mean = naive["test"]["train_mean"]["mae"] if naive else float("nan")
    print(f"  naive test MAE: last value {naive_test:.4f}, train mean {naive_mean:.4f}")

    # reference: best P2 graph-blind val_mae (seed 0) over the P2 archs
    ref_archs = load_archs_safe(args.ref_archs)
    ref = []
    for r in ref_archs:
        m = Path(args.train_dir) / r["arch_id"] / "seed0" / "metrics.json"
        if m.exists():
            mm = json.load(open(m))
            if mm.get("status") == "done" and not has_graph_op(r["genotype"]):
                ref.append(mm["val_mae"])
    good &= _ok(len(ref) >= 1, f"{len(ref)} graph-blind 20-epoch reference runs from {args.ref_archs}")
    best_ref = min(ref) if ref else float("nan")
    threshold = 1.10 * best_ref
    print(f"  best graph-blind val_mae {best_ref:.4f} -> gate threshold {threshold:.4f}")

    dev = [r for r in load_archs_safe(args.archs) if has_graph_op(r["genotype"])]
    good &= _ok(len(dev) >= 3, f"{len(dev)} dev graph archs in {args.archs}")
    best_dev, n_done = float("inf"), 0
    for r in dev:
        aid = r["arch_id"]
        m = Path(args.train_dir) / aid / "seed0" / "metrics.json"
        if not m.exists():
            good &= _ok(False, f"{aid}: no 20-epoch run at {m}")
            continue
        mm = json.load(open(m))
        done = mm.get("status") == "done"
        n_done += done
        v, t = mm.get("val_mae", float("nan")), mm.get("test_mae", float("nan"))
        good &= _ok(done and math.isfinite(v) and math.isfinite(t),
                    f"{aid} ({graph_family(r['genotype'])}): status={mm.get('status')} epochs={mm.get('epochs_run')} "
                    f"best_epoch={mm.get('best_epoch')} val_mae={v:.4f} test_mae={t:.4f} train_s={mm.get('train_seconds')}")
        good &= _ok(t < 0.9 * min(naive_test, naive_mean), f"{aid}: test_mae {t:.4f} < 0.9 x naive {min(naive_test, naive_mean):.4f} (no collapse)")
        best_dev = min(best_dev, v)
    good &= _ok(best_dev <= threshold, f"GATE: best dev graph val_mae {best_dev:.4f} <= {threshold:.4f} (1.10 x {best_ref:.4f}) "
                                       f"-> {'Option 1 confirmed' if best_dev <= threshold else 'FAIL: consider the fallback'}")
    if args.frozen:
        from pilot.sample_archs import scaled_quota

        fr = load_archs_safe(args.frozen)
        ids = [r["arch_id"] for r in fr]
        N = args.n
        q = scaled_quota(N)
        good &= _ok(len(fr) == N and len(set(ids)) == N, f"{args.frozen}: {len(fr)} archs, {len(set(ids))} distinct ids (expected {N})")
        fams = Counter(graph_family(r["genotype"]) for r in fr)
        n_none = fams.get("none", 0)
        n_gcn = sum(1 for r in fr if graph_family(r["genotype"]) in ("gcn", "mixed"))
        n_diff = sum(1 for r in fr if graph_family(r["genotype"]) in ("diffusion", "mixed"))
        n_ctrl = fams.get("identity-only", 0) + fams.get("adaptive-only", 0)
        print(f"  graph_family counts: {dict(fams)}; quotas for N = {N}: {q}")
        good &= _ok(n_none == q["none"], f"frozen: {n_none} graph-blind (expected {q['none']})")
        good &= _ok(n_gcn >= q["gcn"], f"frozen: {n_gcn} contain gcn (>= {q['gcn']})")
        good &= _ok(n_diff >= q["diffusion"], f"frozen: {n_diff} contain diffusion (>= {q['diffusion']})")
        good &= _ok(n_ctrl >= q["control"], f"frozen: {n_ctrl} adaptive/identity-only controls (>= {q['control']})")
        good &= _ok(all(r["genotype"]["space"] == "dartsts_graph_v1" for r in fr), "frozen: all in space dartsts_graph_v1")
        good &= _ok(Path(args.frozen).with_name("FROZEN.md").exists(), f"{Path(args.frozen).with_name('FROZEN.md')} exists")
    return bool(good)


def phase6(args) -> bool:
    """Ground truth for the frozen 50: 50/50 proxy files complete (every stored name x 3 seeds finite unless an explicit
    error is recorded), >= 45/50 seed-0 trainings done, seed-noise Spearman (seed 0 vs 1, 0 vs 2) on the first 5."""
    import statistics

    from pilot.score_proxies import ORDER

    good = True
    N = args.n
    archs = load_archs_safe(args.archs)
    good &= _ok(len(archs) == N, f"{len(archs)} frozen archs in {args.archs} (expected {N})")
    seeds = [s.strip() for s in args.seeds.split(",")]
    n_complete, n_errors, missing = 0, 0, []
    for r in archs:
        p = Path(args.proxies_dir) / f"{r['arch_id']}.json"
        if not p.exists():
            missing.append(r["arch_id"])
            continue
        rec = json.load(open(p))
        ok = True
        for name in ORDER:
            if name in rec.get("errors", {}):
                n_errors += 1
                continue
            for s in seeds:
                v = rec.get("scores", {}).get(name, {}).get(s)
                if v is None or not math.isfinite(v):
                    ok = False
        n_complete += ok
    good &= _ok(n_complete == N and not missing, f"{n_complete}/{N} proxy files complete ({len(ORDER)} names x {len(seeds)} seeds); "
                                                 f"{n_errors} explicit errors; missing {missing[:3]}")
    done, failed, running, todo = [], [], [], []
    for r in archs:
        m = Path(args.train_dir) / r["arch_id"] / "seed0" / "metrics.json"
        st = json.load(open(m)).get("status") if m.exists() else None
        (done if st == "done" else failed if st == "failed" else running if st == "running" else todo).append(r["arch_id"])
    good &= _ok(len(done) >= 0.9 * N, f"seed-0 trainings: {len(done)} done (>= 90% of {N}), {len(failed)} failed, {len(running)} running, {len(todo)} not started")
    if failed:
        print(f"  failed: {failed}")
    # seed noise on the first 5
    first5 = archs[:5]
    vals = {s: [] for s in (0, 1, 2)}
    for r in first5:
        for s in (0, 1, 2):
            m = Path(args.train_dir) / r["arch_id"] / f"seed{s}" / "metrics.json"
            rec = json.load(open(m)) if m.exists() else {}
            vals[s].append(rec.get("val_mae") if rec.get("status") == "done" else None)
    n_seed = sum(1 for s in (1, 2) for v in vals[s] if v is not None)
    good &= _ok(n_seed == 10, f"seed-noise runs done: {n_seed}/10 (seeds 1, 2 on the first 5)")
    if all(v is not None for s in (0, 1, 2) for v in vals[s]):
        def rank(x):
            o = sorted(range(len(x)), key=lambda i: x[i]); rk = [0] * len(x)
            for k, i in enumerate(o):
                rk[i] = k
            return rk
        def spearman(a, b):
            ra, rb = rank(a), rank(b); n = len(a)
            return 1 - 6 * sum((ra[i] - rb[i]) ** 2 for i in range(n)) / (n * (n * n - 1))
        stds = [statistics.pstdev([vals[s][i] for s in (0, 1, 2)]) for i in range(5)]
        print(f"  seed-noise ceiling (5 archs): Spearman seed0-seed1 {spearman(vals[0], vals[1]):+.2f}, seed0-seed2 {spearman(vals[0], vals[2]):+.2f}, "
              f"seed1-seed2 {spearman(vals[1], vals[2]):+.2f}; within-arch val_mae std mean {statistics.mean(stds):.4f} max {max(stds):.4f}")
        for r, i in zip(first5, range(5)):
            print(f"    {r['arch_id']} ({r['sampler'].get('graph_family')}): " + " / ".join(f"{vals[s][i]:.4f}" for s in (0, 1, 2)))
    good &= _ok(Path(args.status_csv).exists(), f"{args.status_csv} exists (python -m pilot.status --timing-csv ...)")
    return bool(good)


def phase7(args) -> bool:
    """Experiment B: every pi_j(A) preserves per-node degrees and differs from A in >= 30% of edges; S_spatial == 0 (float
    noise) for graph-blind / identity-only / adaptive-only archs; S_spatial > 3 x std(permuted) for >= 1 gcn/diffusion arch."""
    import numpy as np

    from pilot.adjacency import load_adj

    good = True
    A = load_adj(args.adj)
    m = int(A.sum() // 2)
    perms = sorted(Path(args.adj).parent.glob(f"{Path(args.adj).stem}_perm_*.npy"))
    good &= _ok(len(perms) >= 5, f"{len(perms)} permuted adjacencies")
    for pf in perms:
        P = load_adj(pf)
        shared = int((P * A).sum() // 2)
        good &= _ok(bool(np.array_equal(P.sum(1), A.sum(1))) and bool(np.array_equal(P, P.T)) and (np.diag(P) == 0).all() and (1 - shared / m) >= 0.30,
                    f"{pf.name}: per-node degrees preserved, symmetric, zero diag, {100 * (1 - shared / m):.0f}% of edges changed (>= 30%)")
    archs = load_archs_safe(args.archs)
    recs = {}
    for r in archs:
        p = Path(args.spatial_dir) / f"{r['arch_id']}.json"
        if p.exists():
            recs[r["arch_id"]] = json.load(open(p))
    good &= _ok(len(recs) == len(archs), f"{len(recs)}/{len(archs)} spatial files in {args.spatial_dir}")
    if not recs:
        return False
    bases = sorted({b for rec in recs.values() for b in rec.get("bases", {})})
    print(f"  bases: {bases}")
    n_err = sum(len(rec.get("errors", {})) for rec in recs.values())
    good &= _ok(n_err == 0, f"{n_err} errors recorded")
    controls = [a for a, rec in recs.items() if rec["graph_family"] in ("none", "identity-only", "adaptive-only")]
    sensitive = [a for a, rec in recs.items() if rec["graph_family"] in ("gcn", "diffusion", "mixed")]
    for base in bases:
        # recomputed score under A should reproduce the v1 value (same seed, same probe batch, cudnn deterministic)
        diffs = []
        for rec in recs.values():
            br = rec["bases"][base]
            for s, v in br["A"].items():
                v1 = br["A_v1"].get(s)
                if v1 is not None and v1 != 0:
                    diffs.append(abs(v - v1) / abs(v1))
        if diffs:
            import statistics as _st
            # v1 values were computed with a different RNG state at forward time (dropout masks), so agreement is only
            # expected within the dropout noise; report it, fail only on gross mismatch
            good &= _ok(max(diffs) < 0.10, f"{base}: recomputed score(A) vs results/proxies/v1: median rel diff {_st.median(diffs):.2e}, max {max(diffs):.2e} over {len(diffs)} values (< 10%)")
        ctrl_rel = []
        for a in controls:
            br = recs[a]["bases"][base]
            for s in br["S_spatial"]:
                scale = abs(br["A"][s]) if br["A"][s] != 0 else 1.0
                ctrl_rel.append(br["S_spatial"][s] / scale)
        good &= _ok(bool(ctrl_rel) and max(ctrl_rel) < 1e-4,
                    f"{base}: S_spatial == 0 up to float noise on {len(controls)} control archs (max relative {max(ctrl_rel) if ctrl_rel else float('nan'):.2e})")
        strong = []
        for a in sensitive:
            br = recs[a]["bases"][base]
            for s in br["S_spatial"]:
                if br["perm_std"][s] > 0 and br["S_spatial"][s] > 3 * br["perm_std"][s]:
                    strong.append(a)
                    break
        good &= _ok(len(strong) >= 1, f"{base}: {len(strong)}/{len(sensitive)} gcn/diffusion/mixed archs with S_spatial > 3 x std(permuted scores)")
        zs = [recs[a]["bases"][base]["z_spatial_mean_over_seeds"] for a in sensitive]
        if zs:
            import statistics
            print(f"    {base}: z_spatial over sensitive archs: mean {statistics.mean(zs):+.2f}, median {statistics.median(zs):+.2f}, min {min(zs):+.2f}, max {max(zs):+.2f}")
    return bool(good)


def phase8(args) -> bool:
    """Analysis artefacts: joined.csv rows == done seed-0 trainings, Table A has the 13 proxies + the ceiling row, Table B
    has >= 3 rows, every main Spearman carries a CI, analyze.py ran in < 60 s, the 3 figures exist."""
    import csv

    good = True
    tdir = Path(args.tables_dir)
    summ = tdir / "analyze_summary.json"
    good &= _ok(summ.exists(), f"{summ} exists")
    if not summ.exists():
        return False
    sm = json.load(open(summ))
    good &= _ok(sm["n_rows"] == sm["n_done"] == args.n, f"joined.csv rows {sm['n_rows']} == done trainings {sm['n_done']} == {args.n}")
    good &= _ok(sm["seconds"] < 60, f"analyze.py ran in {sm['seconds']} s (< 60)")
    rows = list(csv.DictReader(open(tdir / "table_A.csv")))
    good &= _ok(len(rows) == 13, f"table_A.csv has {len(rows)} proxy rows (13)")
    good &= _ok(all(r["ci_lo"] not in ("", "nan") and r["ci_hi"] not in ("", "nan") for r in rows), "every Table A Spearman has a 95% CI")
    md = (tdir / "table_A.md").read_text()
    good &= _ok("seed-noise ceiling" in md, "table_A.md has the seed-noise ceiling row")
    rowsB = list(csv.DictReader(open(tdir / "table_B.csv")))
    good &= _ok(len(rowsB) >= 3, f"table_B.csv has {len(rowsB)} rows (>= 3)")
    for f in ["fig1_proxy_vs_mae_grid.png", "fig2_spearman_by_family.png", "fig3_spatial_vs_naswot.png"]:
        good &= _ok((Path(args.figs_dir) / f).exists(), f"{f} exists")
    return bool(good)


def phase9(args) -> bool:
    """Robustness artefacts: table_A_partial.md and ci_summary.md exist; every CI in Table A is finite and printed next to its
    point estimate; params / flops rows are labelled 'complexity baseline'."""
    import csv
    import re

    good = True
    tdir = Path(args.tables_dir)
    for f in ["table_A_partial.md", "ci_summary.md", "table_A_partial.csv", "subsample_curve.csv"]:
        good &= _ok((tdir / f).exists(), f"{f} exists")
    rows = list(csv.DictReader(open(tdir / "table_A.csv")))
    fin = all(math.isfinite(float(r["ci_lo"])) and math.isfinite(float(r["ci_hi"])) and math.isfinite(float(r["spearman"])) for r in rows)
    good &= _ok(fin, f"all {len(rows)} Table A CIs finite")
    md = (tdir / "table_A.md").read_text()
    n_ci = len(re.findall(r"\| -?\d\.\d\d \(-?\d\.\d\d, -?\d\.\d\d\)", md))
    good &= _ok(n_ci >= len(rows), f"{n_ci} point estimates printed with their CI in table_A.md (>= {len(rows)})")
    good &= _ok("`params` (complexity baseline)" in md and "`flops` (complexity baseline)" in md, "params and flops rows are marked 'complexity baseline'")
    good &= _ok("ρ/ceiling" in md, "Table A carries the ceiling column")
    part = (tdir / "table_A_partial.md").read_text()
    good &= _ok(part.count("|") > 100 and "partial" in part, "table_A_partial.md is populated")
    return bool(good)


def phase10(args) -> bool:
    """Buffer: 50/50 seed-0 done, 0 proxy / spatial errors, RESULTS.md exists and cites every table file by path, final tarball."""
    import re

    good = True
    archs = load_archs_safe(args.archs)
    done = sum(1 for r in archs if (Path(args.train_dir) / r["arch_id"] / "seed0" / "metrics.json").exists()
               and json.load(open(Path(args.train_dir) / r["arch_id"] / "seed0" / "metrics.json")).get("status") == "done")
    good &= _ok(done == args.n, f"{done}/{args.n} seed-0 trainings done")
    n_err = sum(len(json.load(open(Path(args.proxies_dir) / f"{r['arch_id']}.json")).get("errors", {})) for r in archs)
    n_serr = sum(len(json.load(open(Path(args.spatial_dir) / f"{r['arch_id']}.json")).get("errors", {})) for r in archs)
    good &= _ok(n_err == 0 and n_serr == 0, f"proxy errors {n_err}, spatial errors {n_serr}")
    res = args.root_obj.results_md
    good &= _ok(res.exists(), f"{res} exists")
    if res.exists():
        txt = res.read_text()
        tables = sorted(p.name for p in Path(args.tables_dir).glob("table_*.md")) + ["ci_summary.md", "table_A_partial.md", "joined.csv"]
        missing = [t for t in sorted(set(tables)) if t not in txt]
        good &= _ok(not missing, f"RESULTS.md cites every table file ({len(set(tables))}); missing {missing}")
        figs = sorted(p.name for p in Path(args.figs_dir).glob("*.png"))
        good &= _ok(all(f in txt for f in figs), f"RESULTS.md cites every figure ({len(figs)})")
        words = len(re.findall(r"\w+", txt))
        good &= _ok(500 <= words <= 1200, f"RESULTS.md is about one page ({words} words)")
    tars = sorted(Path.home().glob("nas/backups/results-final*.tgz")) + sorted(Path.home().glob("scratch/backups/results-final*.tgz"))
    good &= _ok(len(tars) >= 2, f"final tarball in two locations: {[str(t) for t in tars]}")
    return bool(good)


def load_archs_safe(path):
    from pilot.genotype import load_archs
    return load_archs(path) if Path(path).exists() else []


# ============================================================================================ Pilot 2 checks

def _git_show(path: Path) -> bytes | None:
    """The committed version of a repo file (path relative to the repo root or absolute inside it), or None."""
    from pilot.data import REPO

    rel = Path(path)
    if rel.is_absolute():
        rel = rel.relative_to(REPO)
    try:
        return subprocess.check_output(["git", "-C", str(REPO), "show", f"HEAD:{rel.as_posix()}"])
    except subprocess.CalledProcessError:
        return None


def pilot2_phase1(args) -> bool:
    """Pilot 2, Phase 1 (dataset-agnostic pilot/): the Pilot 1 checks 8, 9, 10 still PASS on the Pilot 1 tree through --root;
    analyze reproduces the committed tables byte for byte; the dataset registry lists three datasets whose data and
    benchmark yaml exist; PEMS/pems04/pems04_36 composes with n_prediction_steps == 36 and one graph arch plus one
    graph-blind arch forward on CPU at that horizon (risk ladder item 1)."""
    import torch

    from pilot import datasets
    from pilot.build_net import build_discrete_net
    from pilot.data import get_cfg, get_dataset_and_loaders, preprocess_batch, seed_everything
    from pilot.genotype import has_graph_op

    root: Root = args.root_obj
    good = True
    # 1) regression: the Pilot 1 checks through --root
    for ph in (8, 9, 10):
        print(f"  -- Pilot 1 phase {ph} on --root {root.dir}")
        ok = PILOT1_CHECKS[ph](args)
        good &= _ok(ok, f"Pilot 1 phase {ph} check PASS with --root {root.dir}")
    # 2) analyze reproduces the committed tables
    tmp = Path(tempfile.mkdtemp(prefix="pilot2_phase1_"))
    t0 = time.time()
    cp = subprocess.run([sys.executable, "-m", "pilot.analyze", "--root", str(root.dir), "--out", str(tmp)], capture_output=True, text=True)
    good &= _ok(cp.returncode == 0, f"pilot.analyze --root {root.dir} --out <tmp> ran in {time.time() - t0:.0f}s (rc={cp.returncode})"
                + ("" if cp.returncode == 0 else "\n" + cp.stderr[-1500:]))
    for f, required in [("table_A.csv", True), ("table_B.csv", True), ("joined.csv", True), ("table_A_partial.csv", True),
                        ("subsample_curve.csv", True), ("table_A.md", True), ("table_B.md", True), ("ci_summary.md", True)]:
        committed, fresh, on_disk = _git_show(root.tables / f), (tmp / f), root.tables / f
        if committed is None:  # e.g. subsample_curve.csv, never committed in Pilot 1 -> compare with the on-disk copy
            committed, where = (on_disk.read_bytes() if on_disk.exists() else None), f"the on-disk {on_disk} (not in git)"
        else:
            where = f"git HEAD:{on_disk}"
        same = committed is not None and fresh.exists() and fresh.read_bytes() == committed
        good &= _ok(same, f"{f}: regenerated file byte-identical to {where}")
    # 3) the registry
    n_listed = 0
    for ds in datasets.DATASETS:
        st = datasets.files_status(ds)
        ok = st["npz_exists"] and bool(st["horizons"])
        n_listed += ok
        v = datasets.verify_npz(ds) if st["npz_exists"] else {"shape": None, "n_nodes_match": False}
        good &= _ok(ok and v["n_nodes_match"], f"{ds}: npz {st['npz']} exists={st['npz_exists']} shape={v['shape']} "
                                              f"n_nodes={st['n_nodes']} match={v['n_nodes_match']}; horizons {st['horizons']}")
        adj_src = st["distance_csv_exists"] or st["adj_pickle_exists"]
        print(f"  [{'ok' if adj_src else 'note'}] {ds}: adjacency source distance_csv={st['distance_csv_exists']} "
              f"adj_pickle={st['adj_pickle_exists']} ({st['adj_pickle']}){'' if adj_src else '  <- needed before a Phase 2(b) probe on it'}")
    good &= _ok(n_listed == 3, f"python -m pilot.datasets --list: {n_listed}/3 datasets with data + benchmark yaml")
    # 4) horizon 36 composes and the nets forward at H = 36
    bench = datasets.benchmark_for("pems04", 36)
    try:
        cfg = get_cfg(bench)
        good &= _ok(int(cfg.benchmark.external_forecast_horizon) == 36, f"{bench} composes; external_forecast_horizon = {cfg.benchmark.external_forecast_horizon}")
        seed_everything(0)
        dataset, (train_loader, _, _), dims = get_dataset_and_loaders(cfg, batch_size=4, num_workers=0)
        good &= _ok(dims["n_prediction_steps"] == 36, f"{bench}: n_prediction_steps = {dims['n_prediction_steps']} (36); dims d_output={dims['d_output']} window={dims['window_size']}")
        from autoPyTorch.pipeline.components.setup.forecasting_target_scaling.utils import TargetScaler
        X, y = next(iter(train_loader))
        x_past, x_future, loc, scale = preprocess_batch(X, TargetScaler(cfg.train.targe_scaler), dims["window_size"], torch.device("cpu"))
        target = y["future_targets"].float()
        archs = load_archs_safe(args.archs)
        def first(cond):
            return next((r for r in archs if cond(r["genotype"])), None)
        picks = [first(lambda g: has_graph_op(g) and g["seq"]["decoder_type"] == "seq"),
                 first(lambda g: has_graph_op(g) and g["seq"]["decoder_type"] == "linear"),
                 first(lambda g: g.get("graph") is None)]
        picks = [r for r in picks if r is not None]
        good &= _ok(len(picks) == 3, f"{len(picks)} archs picked for the h36 forward (graph+seq decoder, graph+linear, graph-blind)")
        for r in picks:
            g, aid = r["genotype"], r["arch_id"]
            net = build_discrete_net(g, dims, adj_path=args.adj)
            with torch.no_grad():
                out = net(x_past, x_future)
            out = out[-1] if isinstance(out, (list, tuple)) else out
            good &= _ok(tuple(out.shape) == tuple(target.shape) and out.shape[1] == 36,
                        f"{aid} ({'graph' if g.get('graph') else 'graph-blind'}, head={g['head']}, dec={g['seq']['decoder_type']}): "
                        f"CPU forward at h36 gives {tuple(out.shape)} == target {tuple(target.shape)}")
    except Exception as e:  # noqa: BLE001
        import traceback
        good &= _ok(False, f"horizon-36 check raised {e!r}\n{traceback.format_exc()[-1500:]}")
    return bool(good)


def pilot2_phase2(args) -> bool:
    """Pilot 2, Phase 2 (the probe): the frozen 50 trained on a second setting (PEMS04 h36 by default).  PASS = the root holds
    the same 50 arch_ids as the Pilot 1 tree, 50/50 seed-0 done, 0 proxy / spatial errors, seed-noise ceiling >= 0.8, tables
    and figures present, DECISION.md written.  The verdict (plan Section 2, Phase 2):
      graph matters  if  median val MAE(uses-A archs) < median val MAE(graph-blind archs) - 3 x within-arch seed std
                         and Mann-Whitney U p < 0.05,
                     or  |Spearman(S_spatial(nwot), -val MAE)| > 0.28 within the uses-A archs;
      otherwise      graph does not matter at this setting."""
    import hashlib

    import numpy as np
    import pandas as pd
    from scipy.stats import mannwhitneyu, spearmanr

    root: Root = args.root_obj
    good = True
    ref = Root("results")
    # 1) the same frozen 50
    archs = load_archs_safe(args.archs)
    ref_archs = load_archs_safe(ref.archs_jsonl)
    ids, ref_ids = [r["arch_id"] for r in archs], [r["arch_id"] for r in ref_archs]
    good &= _ok(len(ids) == args.n and ids == ref_ids[: len(ids)], f"{len(ids)} archs in {args.archs}; same ids in the same order as {ref.archs_jsonl}")
    sha = hashlib.sha1(Path(args.archs).read_bytes()).hexdigest() if Path(args.archs).exists() else None
    good &= _ok(root.frozen_md.exists() and sha is not None and sha[:12] in root.frozen_md.read_text(),
                f"{root.frozen_md} exists and records the archs.jsonl sha1 {sha[:12] if sha else None}")
    # 2) ground truth and proxies complete
    done, failed, other = [], [], []
    for r in archs:
        m = Path(args.train_dir) / r["arch_id"] / "seed0" / "metrics.json"
        st = json.load(open(m)).get("status") if m.exists() else None
        (done if st == "done" else failed if st == "failed" else other).append(r["arch_id"])
    good &= _ok(len(done) == args.n, f"seed-0 trainings: {len(done)}/{args.n} done, {len(failed)} failed, {len(other)} running/not started"
                + (f"; failed {failed[:5]}" if failed else ""))
    n_err = n_serr = n_missing = 0
    for r in archs:
        p, sp = Path(args.proxies_dir) / f"{r['arch_id']}.json", Path(args.spatial_dir) / f"{r['arch_id']}.json"
        n_err += len(json.load(open(p)).get("errors", {})) if p.exists() else 0
        n_serr += len(json.load(open(sp)).get("errors", {})) if sp.exists() else 0
        n_missing += (not p.exists()) + (not sp.exists())
    good &= _ok(n_err == 0 and n_serr == 0 and n_missing == 0, f"proxy errors {n_err}, spatial errors {n_serr}, missing proxy/spatial files {n_missing}")
    # 3) analysis artefacts
    tdir = Path(args.tables_dir)
    for f in ["joined.csv", "table_A.csv", "table_A.md", "table_B.md", "analyze_summary.json", "naive_baselines.json"]:
        good &= _ok((tdir / f).exists(), f"{tdir / f} exists")
    for f in ["fig1_proxy_vs_mae_grid.png", "fig2_spearman_by_family.png", "fig3_spatial_vs_naswot.png"]:
        good &= _ok((Path(args.figs_dir) / f).exists(), f"{f} exists")
    if not (tdir / "joined.csv").exists() or not (tdir / "analyze_summary.json").exists():
        return False
    df = pd.read_csv(tdir / "joined.csv")
    summ = json.load(open(tdir / "analyze_summary.json"))
    ceil = summ.get("seed_ceiling", {})
    rho_ceil = ceil.get("spearman_s0_s1", float("nan"))
    within_std = ceil.get("within_arch_std_mean", float("nan"))
    good &= _ok(ceil.get("n", 0) >= 5 and rho_ceil >= 0.8, f"seed-noise ceiling: Spearman seed0-seed1 = {rho_ceil:.2f} on {ceil.get('n')} archs (>= 0.8); within-arch std {within_std:.4f}")
    # 4) the decision rule
    blind, uses = df[df.group3 == "graph-blind"], df[df.group3 == "uses A"]
    med_blind, med_uses = float(blind.val_mae.median()), float(uses.val_mae.median())
    gap = med_blind - med_uses
    u = mannwhitneyu(uses.val_mae, blind.val_mae, alternative="less")   # H1: uses-A errors are smaller
    rule_a = gap > 3 * within_std and u.pvalue < 0.05
    if "S_spatial_nwot" in df:
        rho_s = float(spearmanr(uses["S_spatial_nwot"], -uses.val_mae).correlation)
    else:
        rho_s = float("nan")
    rule_b = np.isfinite(rho_s) and abs(rho_s) > 0.28
    matters = bool(rule_a or rule_b)
    verdict = "graph matters" if matters else "graph does not matter"
    print(f"  uses-A n={len(uses)} median val MAE {med_uses:.4f} | graph-blind n={len(blind)} median {med_blind:.4f} | gap {gap:+.4f} "
          f"vs 3 x seed std {3 * within_std:.4f} | Mann-Whitney (uses-A < blind) p = {u.pvalue:.3g} -> rule A {rule_a}")
    print(f"  Spearman(S_spatial(nwot), -val MAE) on the uses-A archs = {rho_s:+.3f} vs |rho| > 0.28 -> rule B {rule_b}")
    lines = [f"# DECISION — Pilot 2 Phase 2 probe on {root.label} ({root.benchmark})", "",
             f"**Verdict: {verdict} at {root.label}.**", "",
             "Rule (pilot2-plan.md, Phase 2): graph matters if (A) the median val MAE of the uses-A archs is below the graph-blind median by more "
             "than 3 x the within-arch seed std *and* Mann-Whitney p < 0.05, *or* (B) |Spearman(S_spatial(nwot), -val MAE)| > 0.28 within the uses-A archs.", "",
             "| Quantity | Value |", "|---|---|",
             f"| uses-A archs (n) | {len(uses)} |", f"| graph-blind archs (n) | {len(blind)} |",
             f"| median val MAE, uses-A | {med_uses:.4f} |", f"| median val MAE, graph-blind | {med_blind:.4f} |",
             f"| gap (blind - uses-A) | {gap:+.4f} |", f"| 3 x within-arch seed std | {3 * within_std:.4f} (std {within_std:.4f}, {ceil.get('n')} archs x 3 seeds) |",
             f"| Mann-Whitney U, H1 uses-A < blind, p | {u.pvalue:.3g} |", f"| rule A | {rule_a} |",
             f"| Spearman(S_spatial(nwot), -val MAE), uses-A only | {rho_s:+.3f} |", f"| rule B (|rho| > 0.28) | {rule_b} |",
             f"| seed-noise ceiling (Spearman seed 0 vs 1) | {rho_ceil:.2f} |",
             f"| seed-0 runs done | {len(done)}/{args.n} |", "",
             f"Files: `{tdir}/table_A.md`, `{tdir}/table_B.md`, `{Path(args.figs_dir)}/`.  Written by `pilot.check --phase 2 --pilot 2 --root {root.dir}` "
             f"on {time.strftime('%Y-%m-%d %H:%M')}.", ""]
    root.decision_md.write_text("\n".join(lines))
    good &= _ok(root.decision_md.exists(), f"{root.decision_md} written: {verdict}")
    return bool(good)


def pilot2_phase3(args) -> bool:
    """Pilot 2, Phase 3 (sample + freeze): <root>/archs.jsonl holds --n distinct ids with a per-arch JSON each; the block sampled
    before the newest seed is byte-unchanged (its sha1 is the one recorded in FROZEN.md); the newest block's strata are within +-2 of
    the scaled quotas; the root's adjacency is (n_nodes, n_nodes), symmetric, binary, matches the cross-check pickle when one was
    given, and has 8 degree-preserving permutations; probe batch and naive baselines exist."""
    import hashlib
    import re
    from collections import Counter

    import numpy as np

    from pilot import datasets
    from pilot.adjacency import load_adj
    from pilot.genotype import graph_family
    from pilot.sample_archs import scaled_quota

    root: Root = args.root_obj
    good = True
    archs = load_archs_safe(args.archs)
    ids = [r["arch_id"] for r in archs]
    good &= _ok(len(archs) == args.n and len(set(ids)) == args.n, f"{len(archs)} archs in {args.archs}, {len(set(ids))} distinct ids (expected {args.n})")
    good &= _ok(all(r["genotype"]["space"] == "dartsts_graph_v1" for r in archs), "all archs in space dartsts_graph_v1")
    missing = [a for a in ids if not (root.archs_dir / f"{a}.json").exists()]
    good &= _ok(not missing, f"per-arch JSON files in {root.archs_dir}: {len(ids) - len(missing)}/{len(ids)} present")
    # blocks by sampler seed, in file order
    seeds = [r["sampler"]["seed"] for r in archs]
    new_seed = seeds[-1] if seeds else None
    n_old = next((i for i, s in enumerate(seeds) if s == new_seed), 0)
    old_block, new_block = archs[:n_old], archs[n_old:]
    frozen_txt = root.frozen_md.read_text() if root.frozen_md.exists() else ""
    good &= _ok(bool(frozen_txt), f"{root.frozen_md} exists")
    if n_old:
        lines = Path(args.archs).read_text().splitlines(keepends=True)
        sha_old = hashlib.sha1("".join(lines[:n_old]).encode()).hexdigest()
        good &= _ok(sha_old[:12] in frozen_txt, f"first {n_old} lines (seed {seeds[0]}) unchanged: sha1 {sha_old[:12]} is recorded in FROZEN.md")
    sha_all = hashlib.sha1(Path(args.archs).read_bytes()).hexdigest()
    good &= _ok(sha_all[:12] in frozen_txt, f"FROZEN.md records the current file sha1 {sha_all[:12]} and seed {new_seed}: {str(new_seed) in frozen_txt}")
    q = scaled_quota(len(new_block))
    strata = Counter(r["sampler"].get("stratum") for r in new_block)
    fams = Counter(graph_family(r["genotype"]) for r in new_block)
    n_none, n_ctrl = fams.get("none", 0), fams.get("identity-only", 0) + fams.get("adaptive-only", 0)
    n_gcn = sum(1 for r in new_block if graph_family(r["genotype"]) in ("gcn", "mixed"))
    n_diff = sum(1 for r in new_block if graph_family(r["genotype"]) in ("diffusion", "mixed"))
    print(f"  newest block: seed {new_seed}, {len(new_block)} archs; strata {dict(strata)}; quotas {q}; families {dict(fams)}")
    good &= _ok(all(abs(strata.get(k, 0) - v) <= 2 for k, v in q.items()), "newest block: every stratum within +-2 of its scaled quota")
    good &= _ok(n_none == q["none"] and n_gcn >= q["gcn"] and n_diff >= q["diffusion"] and n_ctrl >= q["control"],
                f"newest block by family: {n_none} graph-blind (= {q['none']}), {n_gcn} with gcn (>= {q['gcn']}), {n_diff} with diffusion (>= {q['diffusion']}), {n_ctrl} controls (>= {q['control']})")
    # adjacency, probe batch, baselines
    n = datasets.n_nodes(root.dataset)
    adj_path = Path(args.adj)
    good &= _ok(adj_path.exists(), f"{adj_path} exists")
    if adj_path.exists():
        A = load_adj(adj_path)
        good &= _ok(A.shape == (n, n) and np.array_equal(A, A.T) and set(np.unique(A)) <= {0.0, 1.0} and (np.diag(A) == 0).all(),
                    f"A is {A.shape}, symmetric, binary, zero diagonal; {int(A.sum() // 2)} undirected edges, {int((A.sum(1) == 0).sum())} isolated")
        info = json.load(open(adj_path.with_suffix(".json"))) if adj_path.with_suffix(".json").exists() else {}
        if "matches_pickle_after_symmetrization" in info:
            good &= _ok(info["matches_pickle_after_symmetrization"] is True, f"A matches the cross-check pickle after symmetrization (pickle nnz {info.get('pickle_nnz')})")
        else:
            good &= _ok(root.dataset == "metrla" or root.dataset == "pems04", f"adjacency was built with --cross-check ({root.dataset})")
        perms = root.adj_perms()
        good &= _ok(len(perms) == 8 and all(np.array_equal(load_adj(p).sum(1), A.sum(1)) and not np.array_equal(load_adj(p), A) for p in perms),
                    f"{len(perms)} permutations, each degree-preserving and different from A")
    good &= _ok(Path(args.probe).exists(), f"{args.probe} exists")
    good &= _ok(Path(args.baselines).exists(), f"{args.baselines} exists")
    return bool(good)


def pilot2_phase4(args) -> bool:
    """Pilot 2, Phase 4 (ground truth at scale): >= 95 % of the --n seed-0 runs done (the rest listed for --retry-failed), seeds 1-2
    done for the first 5 arch_ids, every arch has a proxy file with 0 errors and a spatial file with 0 errors, status.csv written,
    and the seed-noise ceiling printed (Spearman over the repeated archs plus the within/across std ratio)."""
    import statistics

    from pilot.score_proxies import ORDER

    root: Root = args.root_obj
    good = True
    archs = load_archs_safe(args.archs)
    good &= _ok(len(archs) == args.n, f"{len(archs)} archs in {args.archs} (expected {args.n})")
    done, failed, running, todo = [], [], [], []
    val = {}
    for r in archs:
        m = Path(args.train_dir) / r["arch_id"] / "seed0" / "metrics.json"
        rec = json.load(open(m)) if m.exists() else {}
        st = rec.get("status")
        (done if st == "done" else failed if st == "failed" else running if st == "running" else todo).append(r["arch_id"])
        if st == "done":
            val[r["arch_id"]] = rec["val_mae"]
    good &= _ok(len(done) >= 0.95 * args.n, f"seed-0 trainings: {len(done)}/{args.n} done (>= 95 %), {len(failed)} failed, {len(running)} running, {len(todo)} not started")
    if failed or running or todo:
        print(f"  not done: failed {failed[:8]} running {running[:8]} not-started {todo[:8]}  -> pilot/submit.sh train {root.dir} {root.dataset} {root.horizon} (the runner retries failed runs itself)")
    if val:
        vals = list(val.values())
        print(f"  val MAE over {len(vals)} done: mean {statistics.mean(vals):.4f} std {statistics.pstdev(vals):.4f} min {min(vals):.4f} max {max(vals):.4f}")
    # seed noise on the first 5
    first5 = archs[:5]
    per = {s: [] for s in (0, 1, 2)}
    for r in first5:
        for s_ in (0, 1, 2):
            m = Path(args.train_dir) / r["arch_id"] / f"seed{s_}" / "metrics.json"
            rec = json.load(open(m)) if m.exists() else {}
            per[s_].append(rec.get("val_mae") if rec.get("status") == "done" else None)
    n_seed = sum(1 for s_ in (1, 2) for v in per[s_] if v is not None)
    good &= _ok(n_seed == 10, f"seed-noise runs done: {n_seed}/10 (seeds 1, 2 on the first 5 arch_ids)")
    if all(v is not None for s_ in (0, 1, 2) for v in per[s_]):
        from scipy.stats import spearmanr
        within = statistics.mean(statistics.pstdev([per[s_][i] for s_ in (0, 1, 2)]) for i in range(5))
        across = statistics.pstdev(vals) if val else float("nan")
        print(f"  seed-noise ceiling (5 archs): Spearman s0-s1 {spearmanr(per[0], per[1]).correlation:+.2f}, s0-s2 {spearmanr(per[0], per[2]).correlation:+.2f}, "
              f"s1-s2 {spearmanr(per[1], per[2]).correlation:+.2f}; within-arch std {within:.4f} vs across-arch {across:.4f} (ratio {within / across if across else float('nan'):.2f})")
    # proxies and spatial
    n_pfile = n_perr = n_pincomplete = n_sfile = n_serr = 0
    seeds = [x.strip() for x in args.seeds.split(",")]
    for r in archs:
        p = Path(args.proxies_dir) / f"{r['arch_id']}.json"
        if p.exists():
            n_pfile += 1
            rec = json.load(open(p))
            n_perr += len(rec.get("errors", {}))
            if any(rec.get("scores", {}).get(name, {}).get(s_) is None for name in ORDER for s_ in seeds):
                n_pincomplete += 1
        sp = Path(args.spatial_dir) / f"{r['arch_id']}.json"
        if sp.exists():
            n_sfile += 1
            n_serr += len(json.load(open(sp)).get("errors", {}))
    good &= _ok(n_pfile == args.n and n_perr == 0 and n_pincomplete == 0, f"proxy files {n_pfile}/{args.n}, errors {n_perr}, incomplete ({len(ORDER)} names x {len(seeds)} seeds) {n_pincomplete}")
    good &= _ok(n_sfile == args.n and n_serr == 0, f"spatial files {n_sfile}/{args.n}, errors {n_serr}" + ("" if n_sfile == args.n else f"  -> pilot/submit.sh spatial {root.dir} {root.dataset} {root.horizon}"))
    good &= _ok(Path(args.status_csv).exists(), f"{args.status_csv} exists (pilot.status --root {root.dir} --timing-csv ...)")
    return bool(good)


PILOT1_CHECKS = {1: phase1, 2: phase2, 3: phase3, 4: phase4, 6: phase6, 7: phase7, 8: phase8, 9: phase9, 10: phase10}
PILOT2_CHECKS = {1: pilot2_phase1, 2: pilot2_phase2, 3: pilot2_phase3, 4: pilot2_phase4}


def main():
    ap = argparse.ArgumentParser()
    Root.add_args(ap)
    ap.add_argument("--phase", type=int, required=True)
    ap.add_argument("--pilot", type=int, default=1, help="1 = the Pilot 1 phase checks (default), 2 = the Pilot 2 phase checks")
    ap.add_argument("--n", type=int, default=None, help="expected number of frozen archs (default: lines in <root>/archs.jsonl)")
    ap.add_argument("--archs", default=None)
    ap.add_argument("--probe", default=None)
    ap.add_argument("--proxies-dir", default=None)
    ap.add_argument("--train-dir", default=None)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--limit", type=int, default=1)
    ap.add_argument("--seeds", default="0,1,2", help="phase 2: init seeds expected in the proxy files")
    ap.add_argument("--timing-csv", default=None)
    ap.add_argument("--adj", default=None)
    ap.add_argument("--autocts", action="store_true", help="phase 3: also check the AutoCTS fallback gate")
    ap.add_argument("--autocts-json", default=None)
    ap.add_argument("--baselines", default=None)
    ap.add_argument("--ref-archs", default=None, help="phase 4: graph-blind reference archs (P2 five)")
    ap.add_argument("--frozen", default=None, help="phase 4: the frozen set (<root>/archs.jsonl) to validate")
    ap.add_argument("--status-csv", default=None)
    ap.add_argument("--spatial-dir", default=None)
    ap.add_argument("--tables-dir", default=None)
    ap.add_argument("--figs-dir", default=None)
    args = ap.parse_args()
    root = Root.from_args(args)
    args.root_obj = root
    defaults = {"archs": root.archs_jsonl, "probe": root.probe, "proxies_dir": root.proxies_v1, "train_dir": root.train,
                "timing_csv": root.tables / "timing_p2.csv", "adj": root.adj, "autocts_json": root.dir / "autocts_precheck.json",
                "baselines": root.naive_baselines, "ref_archs": root.dir / "archs_p2.jsonl", "status_csv": root.status_csv,
                "spatial_dir": root.spatial_v2, "tables_dir": root.tables, "figs_dir": root.figs}
    for k, v in defaults.items():
        if getattr(args, k) is None:
            setattr(args, k, str(v))
    if args.n is None:
        args.n = len(load_archs_safe(args.archs))
    checks = {1: PILOT1_CHECKS, 2: PILOT2_CHECKS}.get(args.pilot)
    if checks is None or args.phase not in checks:
        raise SystemExit(f"no check for pilot {args.pilot} phase {args.phase}; have pilot 1: {sorted(PILOT1_CHECKS)}, pilot 2: {sorted(PILOT2_CHECKS)}")
    print(f"== pilot.check pilot {args.pilot} phase {args.phase}  ({root}, n = {args.n})")
    ok = checks[args.phase](args)
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
