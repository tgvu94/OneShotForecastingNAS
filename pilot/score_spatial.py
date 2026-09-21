"""Experiment B (Phase 7): base proxies under the true adjacency A and under k degree-preserving permutations pi_j(A).

For each arch, init seed and base proxy:  score(A) (recomputed, and compared with results/proxies/v1), score(pi_j(A)) for
j = 0..k-1, their mean / std, S_spatial = |score(A) - mean_j| and z_spatial = (score(A) - mean_j) / std_j (Section 3.4).
Graph-blind archs never see A, so their S_spatial is 0 up to float noise (the built-in control).

    python -m pilot.score_spatial --archs results/archs.jsonl --base nwot,zico --seeds 0,1,2 \
        --perms results/data/pems04_adj_perm_*.npy --out results/proxies/spatial_v1
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import math
import statistics
import subprocess
import time
import traceback
from pathlib import Path

import numpy as np
import torch

from pilot.adjacency import DEFAULT_ADJ, load_adj
from pilot.build_net import build_discrete_net
from pilot.data import DEFAULT_PROBE, load_probe_batch, seed_everything
from pilot.genotype import graph_family, load_archs
from pilot.proxies import extra
from pilot.proxies.wrapper import ProxyWrapper, loss_fn

SPATIAL_VERSION = "spatial_v2"  # v1: no RNG control between the A / pi_j(A) forwards (dropout noise floor ~1-3%)
BASES = {  # base proxy -> how to call it on a fresh wrapper copy (same code as score_proxies)
    "nwot": lambda w, x, t, b, d: extra.nwot(w, x),
    "zico": lambda w, x, t, b, d: extra.zico(w, b, loss_fn, d),
    "grad_norm_all": lambda w, x, t, b, d: extra.grad_group_all(w, x, t, loss_fn)["grad_norm_all"],
    "snip_all": lambda w, x, t, b, d: extra.grad_group_all(w, x, t, loss_fn)["snip_all"],
    "zen": lambda w, x, t, b, d: extra.zen(w, x),
}


def fork_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def score_under(wrapper, A: np.ndarray, base: str, x, target, batches, device, seed: int):
    """Score one adjacency on a fresh copy.  The RNG is re-seeded right before the forward so that the dropout masks
    (the nets are scored in train mode, as in score_proxies) are identical under A and under every pi_j(A): the only
    thing that differs between the calls is the adjacency.  spatial_v1 did not do this and its controls showed a 1-3 %
    "sensitivity" that was pure dropout noise."""
    cp = wrapper.get_prunable_copy()
    if hasattr(cp.net, "graph_net"):
        cp.net.graph_net.set_adjacency(A)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    value, meta = BASES[base](cp, x, target, batches, device)
    del cp
    return float(value), meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archs", default="results/archs.jsonl")
    ap.add_argument("--base", default="nwot,zico")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--adj", default=DEFAULT_ADJ)
    ap.add_argument("--perms", nargs="+", required=True)
    ap.add_argument("--v1", default="results/proxies/v1", help="scores under A already computed in Phases 2/5 (compared, not reused; they carry dropout noise)")
    ap.add_argument("--out", default=f"results/proxies/{SPATIAL_VERSION}")
    ap.add_argument("--probe", default=DEFAULT_PROBE)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    bases = [b.strip() for b in args.base.split(",") if b.strip()]
    unknown = [b for b in bases if b not in BASES]
    if unknown:
        raise SystemExit(f"unknown base proxies {unknown}; known {sorted(BASES)}")
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    A = load_adj(args.adj)
    perm_files = sorted(args.perms)
    perms = [load_adj(f) for f in perm_files]
    for f, P in zip(perm_files, perms):
        assert np.array_equal(P.sum(1), A.sum(1)), f"{f}: degree sequence differs from A"
    perm_sha1 = hashlib.sha1(b"".join(P.tobytes() for P in perms)).hexdigest()
    probe, probe_sha1 = load_probe_batch(args.probe)
    dims, batches = probe["dims"], probe["batches"]
    b0 = batches[0]
    x, target = b0["x_past"].to(device), b0["target"].to(device)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    commit = fork_commit()
    archs = load_archs(args.archs)[: args.limit] if args.limit else load_archs(args.archs)
    print(f"{len(archs)} archs, bases {bases}, seeds {seeds}, {len(perms)} permutations, device {device}")

    t_all = time.time()
    for k, rec_arch in enumerate(archs):
        g, aid = rec_arch["genotype"], rec_arch["arch_id"]
        path = out / f"{aid}.json"
        rec = json.load(open(path)) if path.exists() and not args.force else {
            "arch_id": aid, "space": g["space"], "version": SPATIAL_VERSION, "graph_family": graph_family(g), "bases": {}, "errors": {}}
        rec.update({"perm_files": perm_files, "perm_sha1": perm_sha1, "probe_batch_sha1": probe_sha1, "fork_commit": commit,
                    "torch": torch.__version__, "updated": _dt.datetime.now().isoformat(timespec="seconds")})
        v1 = json.load(open(Path(args.v1) / f"{aid}.json")) if (Path(args.v1) / f"{aid}.json").exists() else {"scores": {}}
        t0 = time.time()
        for seed in seeds:
            todo = [b for b in bases if str(seed) not in rec["bases"].get(b, {}).get("A", {})]
            if not todo:
                continue
            seed_everything(seed, deterministic=True)
            net = build_discrete_net(g, dims).to(device)
            wrapper = ProxyWrapper(net, {"x_future": b0["x_future"], "loc": b0["loc"], "scale": b0["scale"]}).to(device)
            for base in todo:
                br = rec["bases"].setdefault(base, {"A": {}, "A_v1": {}, "perm": {}, "perm_mean": {}, "perm_std": {},
                                                    "S_spatial": {}, "z_spatial": {}, "meta": {}})
                try:
                    vA, mA = score_under(wrapper, A, base, x, target, batches, device, seed)
                    vals = [score_under(wrapper, P, base, x, target, batches, device, seed)[0] for P in perms]
                    mean_j, std_j = statistics.mean(vals), statistics.pstdev(vals)
                    br["A"][str(seed)] = vA
                    br["A_v1"][str(seed)] = v1["scores"].get(base, {}).get(str(seed))
                    br["perm"][str(seed)] = vals
                    br["perm_mean"][str(seed)], br["perm_std"][str(seed)] = mean_j, std_j
                    br["S_spatial"][str(seed)] = abs(vA - mean_j)
                    br["z_spatial"][str(seed)] = (vA - mean_j) / std_j if std_j > 0 else 0.0
                    br["meta"][str(seed)] = {k: v for k, v in mA.items() if k in ("n_hooks", "n_fired", "n_batches", "n_param_tensors_used")}
                    rec["errors"].pop(base, None)
                except Exception as e:  # noqa: BLE001
                    rec["errors"][base] = {"seed": seed, "error": repr(e)[:300], "traceback": traceback.format_exc()[-1500:]}
                    print(f"  {aid} seed {seed} {base}: ERROR {repr(e)[:120]}")
            del wrapper, net
            torch.cuda.empty_cache()
            path.write_text(json.dumps(rec, indent=2))
        for base in bases:
            br = rec["bases"].get(base)
            if br and br["S_spatial"]:
                br["S_spatial_mean_over_seeds"] = statistics.mean(br["S_spatial"].values())
                br["z_spatial_mean_over_seeds"] = statistics.mean(br["z_spatial"].values())
                br["A_mean_over_seeds"] = statistics.mean(br["A"].values())
                br["perm_mean_over_seeds"] = statistics.mean(br["perm_mean"].values())
        path.write_text(json.dumps(rec, indent=2))
        summ = ", ".join(f"{b}: S={rec['bases'][b].get('S_spatial_mean_over_seeds', float('nan')):.4g} z={rec['bases'][b].get('z_spatial_mean_over_seeds', float('nan')):+.2f}"
                         for b in bases if b in rec["bases"])
        print(f"[{k}] {aid} ({rec['graph_family']}) {summ}  ({time.time() - t0:.1f}s)", flush=True)
    print(f"done in {time.time() - t_all:.0f}s")


if __name__ == "__main__":
    main()
