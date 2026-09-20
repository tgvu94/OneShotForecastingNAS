"""Score zero-cost proxies for every architecture in results/archs.jsonl on the fixed probe batch.

Idempotent: results/proxies/<version>/<arch_id>.json is merged, and a (proxy, seed) that already has a value is
skipped unless --force.  Each JSON records torch version, fork commit, probe-batch SHA-1 and the NASLib commit
(null until W2), so later runs can be compared like-for-like.
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
from pilot.proxies.extra import ALIASES, REGISTRY
from pilot.proxies.wrapper import ProxyWrapper

PROXY_VERSION = "v1"
NASLIB_COMMIT = None  # NASLib pruners are copied in W2


def fork_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def score_one(g: dict, dims: dict, batch: dict, proxies: list[str], seed: int, device: torch.device, rec: dict):
    x = batch["x_past"].to(device)
    target = batch["target"].to(device)
    seed_everything(seed, deterministic=True)  # immediately before build (Section 3.3)
    net = build_discrete_net(g, dims).to(device)
    wrapper = ProxyWrapper(net, {"x_future": batch["x_future"], "loc": batch["loc"], "scale": batch["scale"]}).to(device)
    for name in proxies:
        t0 = time.time()
        try:
            if name == "params":
                value, meta = REGISTRY[name](net)
            elif name == "grad_norm_all":
                value, meta = REGISTRY[name](wrapper, x, target, wrapper.loss_fn)
            elif name == "nwot":
                value, meta = REGISTRY[name](wrapper, x)
            else:
                raise KeyError(f"unknown proxy {name}")
            rec["scores"].setdefault(name, {})[str(seed)] = value
            if meta:
                rec["meta"].setdefault(name, {})[str(seed)] = meta
            rec["errors"].pop(name, None)
            print(f"  seed {seed} {name:14s} = {value:.6g}  ({time.time() - t0:.1f}s)")
        except Exception as e:  # noqa: BLE001 - record and continue, one failing proxy must not kill the run
            rec["errors"][name] = {"seed": seed, "error": repr(e), "traceback": traceback.format_exc()[-2000:]}
            print(f"  seed {seed} {name:14s} ERROR {e!r}")
        rec["seconds"].setdefault(name, {})[str(seed)] = round(time.time() - t0, 3)
    del wrapper, net
    if device.type == "cuda":
        torch.cuda.empty_cache()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archs", default="results/archs.jsonl")
    ap.add_argument("--proxies", default="params,grad_norm,nwot")
    ap.add_argument("--seeds", default="0")
    ap.add_argument("--out", default=f"results/proxies/{PROXY_VERSION}")
    ap.add_argument("--probe", default=DEFAULT_PROBE)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--limit", type=int, default=None, help="score only the first N archs")
    args = ap.parse_args()

    proxies = [ALIASES.get(p.strip(), p.strip()) for p in args.proxies.split(",") if p.strip()]
    unknown = [p for p in proxies if p not in REGISTRY]
    if unknown:
        raise SystemExit(f"unknown proxies {unknown}; known: {sorted(REGISTRY)} (aliases {ALIASES})")
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    device = torch.device(args.device)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    probe, probe_sha1 = load_probe_batch(args.probe)
    dims, batch0 = probe["dims"], probe["batches"][0]
    print(f"probe {args.probe} sha1={probe_sha1[:12]} x_past={tuple(batch0['x_past'].shape)} device={device}")
    commit = fork_commit()
    archs = load_archs(args.archs)
    if args.limit:
        archs = archs[: args.limit]

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
                print(f"[{k}] {aid} seed {seed}: all of {proxies} present -> skip")
                continue
            print(f"[{k}] {aid} seed {seed}: {todo}")
            score_one(g, dims, batch0, todo, seed, device, rec)
            path.write_text(json.dumps(rec, indent=2))
        path.write_text(json.dumps(rec, indent=2))
    print("done")


if __name__ == "__main__":
    main()
