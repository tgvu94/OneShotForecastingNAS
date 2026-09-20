"""Score zero-cost proxies for every architecture in results/archs.jsonl on the fixed probe batch.

Idempotent: results/proxies/<version>/<arch_id>.json is merged, and a (proxy, seed) that already has a value is
skipped unless --force.  Each JSON records torch version, fork commit, probe-batch SHA-1 and the NASLib commit,
so later runs can be compared like-for-like.

``--proxies`` takes the plan's 13 names (``fisher,flops,params,grad_norm,l2_norm,plain,grasp,jacov,nwot,snip,
synflow,zen,zico``), ``all``, or stored names.  A plan name that has both a NASLib (Conv/Linear-only) and an
all-parameter implementation expands to both, e.g. ``grad_norm`` -> ``grad_norm`` + ``grad_norm_all``.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
import time
import traceback
from pathlib import Path

import torch

from pilot.build_net import build_discrete_net
from pilot.data import DEFAULT_PROBE, load_probe_batch, seed_everything
from pilot.genotype import load_archs
from pilot.proxies import extra
from pilot.proxies.naslib import NASLIB_COMMIT, NASLIB_MEASURES, naslib_measure
from pilot.proxies.wrapper import ProxyWrapper, loss_fn

PROXY_VERSION = "v1"

# plan name -> stored names (NASLib copy first, all-parameter variant second)
PLAN_NAMES = {
    "fisher": ["fisher"], "flops": ["flops"], "params": ["params"],
    "grad_norm": ["grad_norm", "grad_norm_all"], "l2_norm": ["l2_norm", "l2_norm_all"],
    "plain": ["plain", "plain_all"], "grasp": ["grasp", "grasp_all"], "jacov": ["jacov"], "nwot": ["nwot"],
    "snip": ["snip", "snip_all"], "synflow": ["synflow", "synflow_all"], "zen": ["zen"], "zico": ["zico"],
}
# cheap and robust first, zico (4 batches) last
ORDER = ["params", "flops", "l2_norm", "l2_norm_all", "grad_norm", "grad_norm_all", "snip", "snip_all", "plain",
         "plain_all", "fisher", "synflow", "synflow_all", "jacov", "nwot", "zen", "grasp", "grasp_all", "zico"]
ALL_STORED = set(ORDER)
assert ALL_STORED == set(NASLIB_MEASURES) | set(extra.REGISTRY), (ALL_STORED ^ (set(NASLIB_MEASURES) | set(extra.REGISTRY)))


def expand(spec: str) -> list[str]:
    names = []
    for tok in [t.strip() for t in spec.split(",") if t.strip()]:
        if tok == "all":
            names += ORDER
        elif tok in PLAN_NAMES:
            names += PLAN_NAMES[tok]
        elif tok in ALL_STORED:
            names.append(tok)
        else:
            raise SystemExit(f"unknown proxy {tok!r}; plan names {sorted(PLAN_NAMES)}, stored names {ORDER}")
    seen, out = set(), []
    for n in ORDER:
        if n in names and n not in seen:
            out.append(n)
            seen.add(n)
    return out


def fork_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def score_one(g: dict, dims: dict, batches: list[dict], proxies: list[str], seed: int, device: torch.device, rec: dict):
    batch = batches[0]
    x = batch["x_past"].to(device)
    target = batch["target"].to(device)
    seed_everything(seed, deterministic=True)  # immediately before build (Section 3.3)
    net = build_discrete_net(g, dims).to(device)
    wrapper = ProxyWrapper(net, {"x_future": batch["x_future"], "loc": batch["loc"], "scale": batch["scale"]}).to(device)
    # The DARTS-TS net keeps intermediate tensors as attributes after a forward with grad, and torch refuses to
    # deepcopy non-leaf tensors -> the built wrapper is never forwarded itself; every measure gets a fresh copy
    # (the NASLib measures copy internally via get_prunable_copy, the extra ones get one here).
    fresh = wrapper.get_prunable_copy
    group_cache: dict = {}
    for name in proxies:
        t0 = time.time()
        try:
            if name in NASLIB_MEASURES:
                value, meta = naslib_measure(name, wrapper, x, target)
            else:
                kind, fn = extra.REGISTRY[name]
                if kind == "net":
                    value, meta = fn(wrapper)
                elif kind == "x":
                    value, meta = fn(fresh(), x)
                elif kind == "loss":
                    value, meta = fn(fresh(), x, target, loss_fn)
                elif kind == "group":
                    if fn not in group_cache:
                        group_cache[fn] = fn(fresh(), x, target, loss_fn)
                    value, meta = group_cache[fn][name]
                elif kind == "zico":
                    value, meta = fn(fresh(), batches, loss_fn, device)
                else:
                    raise KeyError(kind)
            value = float(value)
            rec["scores"].setdefault(name, {})[str(seed)] = value
            if meta:
                rec["meta"].setdefault(name, {})[str(seed)] = meta
            rec["errors"].pop(name, None)
            print(f"  seed {seed} {name:14s} = {value:.6g}  ({time.time() - t0:.1f}s)")
        except Exception as e:  # noqa: BLE001 - record and continue, one failing proxy must not kill the run
            rec["errors"][name] = {"seed": seed, "error": repr(e)[:500], "traceback": traceback.format_exc()[-2000:]}
            print(f"  seed {seed} {name:14s} ERROR {repr(e)[:200]}")
        finally:
            if device.type == "cuda":
                torch.cuda.empty_cache()
        rec["seconds"].setdefault(name, {})[str(seed)] = round(time.time() - t0, 3)
    del wrapper, net
    if device.type == "cuda":
        torch.cuda.empty_cache()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archs", default="results/archs.jsonl")
    ap.add_argument("--proxies", default="all")
    ap.add_argument("--seeds", default="0")
    ap.add_argument("--out", default=f"results/proxies/{PROXY_VERSION}")
    ap.add_argument("--probe", default=DEFAULT_PROBE)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--limit", type=int, default=None, help="score only the first N archs")
    args = ap.parse_args()

    proxies = expand(args.proxies)
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    device = torch.device(args.device)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    probe, probe_sha1 = load_probe_batch(args.probe)
    dims, batches = probe["dims"], probe["batches"]
    print(f"probe {args.probe} sha1={probe_sha1[:12]} x_past={tuple(batches[0]['x_past'].shape)} device={device}")
    print(f"proxies ({len(proxies)}): {proxies}; seeds {seeds}")
    commit = fork_commit()
    archs = load_archs(args.archs)
    if args.limit:
        archs = archs[: args.limit]

    t_all = time.time()
    for k, rec_arch in enumerate(archs):
        g, aid = rec_arch["genotype"], rec_arch["arch_id"]
        path = out / f"{aid}.json"
        rec = json.load(open(path)) if path.exists() else {
            "arch_id": aid, "space": g["space"], "proxy_version": PROXY_VERSION, "benchmark": dims.get("benchmark"),
            "scores": {}, "meta": {}, "errors": {}, "seconds": {}}
        rec.update({"probe_batch_sha1": probe_sha1, "fork_commit": commit, "naslib_commit": NASLIB_COMMIT,
                    "torch": torch.__version__, "device": str(device),
                    "gpu": torch.cuda.get_device_name(0) if device.type == "cuda" else None,
                    "updated": _dt.datetime.now().isoformat(timespec="seconds")})
        for seed in seeds:
            todo = [p for p in proxies if args.force or str(seed) not in rec["scores"].get(p, {})]
            if not todo:
                print(f"[{k}] {aid} seed {seed}: all {len(proxies)} proxies present -> skip")
                continue
            print(f"[{k}] {aid} seed {seed}: {todo}")
            score_one(g, dims, batches, todo, seed, device, rec)
            path.write_text(json.dumps(rec, indent=2))
        path.write_text(json.dumps(rec, indent=2))
    print(f"done in {time.time() - t_all:.0f}s")


if __name__ == "__main__":
    main()
