"""TFAS probe (Phase 7, time-boxed).  Verdict from reading github.com/kaist-dmlab/TFAS (commit fd9150d):

* ``zc_proxies/TimeZC/main_proxy.py::compute_zc_score`` is ZiCo (a copy of SLDGroup/ZiCo's compute_zico) over the weights of
  ``nn.Conv2d`` / ``nn.Linear`` / ``nn.Conv1d`` modules, accumulated over the training batches.
* The "time-frequency aware" part is not in the score: ``searcher.py`` precomputes per-batch STL residuals, |FFT| and Haar-DWT
  tensors and passes them as ``td_input / dft_input / dwt_input`` kwargs to the *augmented* backbone
  (``search_space.py`` / ``models/*`` take these extra inputs).  An arbitrary ``nn.Module`` without those inputs is scored by
  the same function with ``td_infos=None``, i.e. plain ZiCo on Conv/Linear weights.
* Verdict: **not usable as a distinct temporal proxy for our discrete DARTS-TS(+graph) nets** -- the temporal term of the
  composite (Section 3.4) is therefore the base proxy itself.  For completeness this script computes the degenerate value
  with TFAS's own ``getgrad`` / ``caculate_zico`` on our 4 probe batches and stores it as ``tfas_zico_cl`` in
  ``results/proxies/v1/<id>.json`` (not part of the 19-name ``ORDER`` list).

    python -m pilot.tfas_probe --tfas $NAS_ROOT/TFAS --seeds 0,1,2
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

import torch

from pilot.build_net import build_discrete_net
from pilot.data import load_probe_batch, seed_everything
from pilot.genotype import load_archs
from pilot.paths import Root
from pilot.proxies.wrapper import ProxyWrapper, loss_fn

VERDICT = ("TFAS not usable as a distinct proxy: its score is ZiCo on Conv/Linear/Conv1d weights; the time-frequency awareness "
           "is an input augmentation (STL residual, |FFT|, Haar DWT) implemented only by its own TimesNet-family backbones. "
           "Composite temporal term = base proxy. Degenerate value stored as tfas_zico_cl.")


def main():
    ap = argparse.ArgumentParser()
    Root.add_args(ap)
    ap.add_argument("--tfas", default=os.path.join(os.environ.get("NAS_ROOT", os.path.expanduser("~/nas")), "TFAS"))
    ap.add_argument("--archs", default=None)
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--v1", default=None)
    ap.add_argument("--probe", default=None)
    ap.add_argument("--adj", default=None)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--frozen-md", default=None)
    args = ap.parse_args()
    root = Root.from_args(args)
    args.archs, args.v1, args.probe = args.archs or root.archs_jsonl, args.v1 or root.proxies_v1, args.probe or root.probe
    args.adj, args.frozen_md = args.adj or root.adj, args.frozen_md or root.frozen_md

    sys.path.insert(0, str(Path(args.tfas) / "zc_proxies" / "TimeZC"))
    commit = subprocess.check_output(["git", "-C", args.tfas, "rev-parse", "--short", "HEAD"], text=True).strip()
    from main_proxy import caculate_zico, getgrad  # TFAS's own code

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    probe, probe_sha1 = load_probe_batch(args.probe)
    dims, batches = probe["dims"], probe["batches"]
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    archs = load_archs(args.archs)[: args.limit] if args.limit else load_archs(args.archs)
    t0 = time.time()
    n_done = 0
    for k, r in enumerate(archs):
        g, aid = r["genotype"], r["arch_id"]
        path = Path(args.v1) / f"{aid}.json"
        rec = json.load(open(path)) if path.exists() else {"arch_id": aid, "scores": {}, "meta": {}, "errors": {}, "seconds": {}}
        for seed in seeds:
            if str(seed) in rec["scores"].get("tfas_zico_cl", {}):
                continue
            ts = time.time()
            seed_everything(seed, deterministic=True)
            net = build_discrete_net(g, dims, adj_path=args.adj).to(device)
            wrapper = ProxyWrapper(net, {"x_future": batches[0]["x_future"], "loc": batches[0]["loc"], "scale": batches[0]["scale"]}).to(device)
            wrapper.train()
            grad_dict = {}
            for i, b in enumerate(batches):
                wrapper.batch_extras = {"x_future": b["x_future"], "loc": b["loc"], "scale": b["scale"]}
                wrapper.zero_grad()
                out = wrapper(b["x_past"].to(device))
                loss = loss_fn(out, b["target"].to(device))
                loss.backward()
                grad_dict = getgrad(wrapper, grad_dict, i)
            score = float(caculate_zico(grad_dict))
            rec["scores"].setdefault("tfas_zico_cl", {})[str(seed)] = score
            rec["meta"].setdefault("tfas_zico_cl", {})[str(seed)] = {"n_modules": len(grad_dict), "n_batches": len(batches),
                                                                     "tfas_commit": commit, "note": "TFAS compute_zc_score without td/dft/dwt augmentation = ZiCo on Conv/Linear/Conv1d weights"}
            rec["seconds"].setdefault("tfas_zico_cl", {})[str(seed)] = round(time.time() - ts, 3)
            n_done += 1
            del wrapper, net
            torch.cuda.empty_cache()
        rec["tfas_verdict"] = VERDICT
        path.write_text(json.dumps(rec, indent=2))
        print(f"[{k}] {aid} tfas_zico_cl " + " ".join(f"s{s}={rec['scores']['tfas_zico_cl'][str(s)]:.4g}" for s in seeds), flush=True)
    fm = Path(args.frozen_md)
    if fm.exists() and "TFAS" not in fm.read_text():
        with open(fm, "a") as f:
            f.write(f"\n## TFAS (Phase 7 probe, {_dt.date.today().isoformat()})\n\n- tfas: not applicable — {VERDICT} (TFAS commit `{commit}`)\n")
    print(f"{n_done} (arch, seed) values in {time.time() - t0:.0f}s")
    print("TFAS: not usable — " + VERDICT)


if __name__ == "__main__":
    main()
