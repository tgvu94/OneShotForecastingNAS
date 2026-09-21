"""Per-phase pass/fail checks.  ``python -m pilot.check --phase 1``  -> prints PASS or FAIL, exit code 0/1."""
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

    good = True
    # 1) adjacency
    adj_path = Path(args.adj)
    good &= _ok(adj_path.exists(), f"{adj_path} exists")
    if not adj_path.exists():
        return False
    A = load_adj(adj_path)
    n_edges = int(A.sum() // 2)
    good &= _ok(A.shape == (307, 307), f"A is {A.shape}")
    good &= _ok(bool(np.array_equal(A, A.T)), "A symmetric")
    good &= _ok(set(np.unique(A)) <= {0.0, 1.0}, "A binary")
    good &= _ok(bool((np.diag(A) == 0).all()), "A zero diagonal")
    good &= _ok(n_edges > 300, f"A has {n_edges} undirected edges (> 300)")
    info_path = adj_path.with_suffix(".json")
    if info_path.exists():
        info = json.load(open(info_path))
        good &= _ok(info.get("matches_pickle_after_symmetrization") is True, "A matches adj_PEMS04.pkl after symmetrization")
    perms = sorted(adj_path.parent.glob(f"{adj_path.stem}_perm_*.npy"))
    good &= _ok(len(perms) >= 1, f"{len(perms)} permuted adjacencies on disk")
    P = load_adj(perms[0]) if perms else None
    if P is not None:
        good &= _ok(bool(np.array_equal(P.sum(1), A.sum(1))) and not np.array_equal(P, A), "perm 0 keeps every degree and differs from A")
    # 2) ops
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(0)
    x = torch.randn(2, 96, 307, 32, device=device)
    packA, packP = adj_pack(A, device), (adj_pack(P, device) if P is not None else None)
    expect_sensitive = {"gcn": True, "diffusion": True, "adaptive": False, "graph_identity": False}
    for name, make in GRAPH_OPS.items():
        op = make(32, 307).to(device)
        with torch.no_grad():
            yA = op(x, packA)
            good &= _ok(tuple(yA.shape) == tuple(x.shape), f"{name}: (2, 96, 307, 32) -> {tuple(yA.shape)}")
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
        net = build_discrete_net(g, dims)
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
        fr = load_archs_safe(args.frozen)
        ids = [r["arch_id"] for r in fr]
        good &= _ok(len(fr) == 50 and len(set(ids)) == 50, f"{args.frozen}: {len(fr)} archs, {len(set(ids))} distinct ids")
        fams = Counter(graph_family(r["genotype"]) for r in fr)
        n_none = fams.get("none", 0)
        n_gcn = sum(1 for r in fr if graph_family(r["genotype"]) in ("gcn", "mixed"))
        n_diff = sum(1 for r in fr if graph_family(r["genotype"]) in ("diffusion", "mixed"))
        n_ctrl = fams.get("identity-only", 0) + fams.get("adaptive-only", 0)
        print(f"  graph_family counts: {dict(fams)}")
        good &= _ok(n_none == 16, f"frozen: {n_none} graph-blind (expected 16)")
        good &= _ok(n_gcn >= 10, f"frozen: {n_gcn} contain gcn (>= 10)")
        good &= _ok(n_diff >= 10, f"frozen: {n_diff} contain diffusion (>= 10)")
        good &= _ok(n_ctrl >= 6, f"frozen: {n_ctrl} adaptive/identity-only controls (>= 6)")
        good &= _ok(all(r["genotype"]["space"] == "dartsts_graph_v1" for r in fr), "frozen: all in space dartsts_graph_v1")
        good &= _ok(Path(args.frozen).with_name("FROZEN.md").exists(), "results/FROZEN.md exists")
    return bool(good)


def phase6(args) -> bool:
    """Ground truth for the frozen 50: 50/50 proxy files complete (every stored name x 3 seeds finite unless an explicit
    error is recorded), >= 45/50 seed-0 trainings done, seed-noise Spearman (seed 0 vs 1, 0 vs 2) on the first 5."""
    import statistics

    from pilot.score_proxies import ORDER

    good = True
    archs = load_archs_safe(args.archs)
    good &= _ok(len(archs) == 50, f"{len(archs)} frozen archs in {args.archs}")
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
    good &= _ok(n_complete == 50 and not missing, f"{n_complete}/50 proxy files complete ({len(ORDER)} names x {len(seeds)} seeds); "
                                                  f"{n_errors} explicit errors; missing {missing[:3]}")
    done, failed, running, todo = [], [], [], []
    for r in archs:
        m = Path(args.train_dir) / r["arch_id"] / "seed0" / "metrics.json"
        st = json.load(open(m)).get("status") if m.exists() else None
        (done if st == "done" else failed if st == "failed" else running if st == "running" else todo).append(r["arch_id"])
    good &= _ok(len(done) >= 45, f"seed-0 trainings: {len(done)} done, {len(failed)} failed, {len(running)} running, {len(todo)} not started")
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


def load_archs_safe(path):
    from pilot.genotype import load_archs
    return load_archs(path) if Path(path).exists() else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", type=int, required=True)
    ap.add_argument("--archs", default="results/archs.jsonl")
    ap.add_argument("--probe", default="results/data/pems04_probe_batch.pt")
    ap.add_argument("--proxies-dir", default="results/proxies/v1")
    ap.add_argument("--train-dir", default="results/train")
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--limit", type=int, default=1)
    ap.add_argument("--seeds", default="0,1,2", help="phase 2: init seeds expected in the proxy files")
    ap.add_argument("--timing-csv", default="results/tables/timing_p2.csv")
    ap.add_argument("--adj", default="results/data/pems04_adj.npy")
    ap.add_argument("--autocts", action="store_true", help="phase 3: also check the AutoCTS fallback gate")
    ap.add_argument("--autocts-json", default="results/autocts_precheck.json")
    ap.add_argument("--baselines", default="results/tables/naive_baselines.json")
    ap.add_argument("--ref-archs", default="results/archs_p2.jsonl", help="phase 4: graph-blind reference archs (P2 five)")
    ap.add_argument("--frozen", default=None, help="phase 4: the frozen 50 (results/archs.jsonl) to validate")
    ap.add_argument("--status-csv", default="results/tables/status.csv")
    args = ap.parse_args()
    checks = {1: phase1, 2: phase2, 3: phase3, 4: phase4, 6: phase6}
    if args.phase not in checks:
        raise SystemExit(f"no check for phase {args.phase}; have {sorted(checks)}")
    print(f"== pilot.check phase {args.phase}")
    ok = checks[args.phase](args)
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
