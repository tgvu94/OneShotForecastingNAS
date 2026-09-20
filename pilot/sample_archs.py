"""Sample N random genotypes -> append to results/archs.jsonl (append-only, de-duplicated by arch_id)
and write results/archs/<arch_id>.json.  Re-running the same command is a no-op."""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import random
from pathlib import Path

from pilot.genotype import SPACE_V1, arch_id, load_archs, random_genotype, summarize


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--space", default=SPACE_V1)
    ap.add_argument("--edges-per-node", type=int, default=2)
    ap.add_argument("--out", default="results/archs.jsonl")
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    per_arch_dir = out.parent / "archs"
    per_arch_dir.mkdir(exist_ok=True)
    existing = {r["arch_id"] for r in load_archs(out)} if out.exists() else set()

    rng = random.Random(args.seed)
    added, skipped = 0, 0
    with open(out, "a") as f:
        for k in range(args.n):
            g = random_genotype(rng, args.space, args.edges_per_node)
            aid = arch_id(g)
            if aid in existing:
                skipped += 1
                print(f"[{k}] {aid} already in {out} -> skip")
                continue
            rec = {"arch_id": aid, "genotype": g,
                   "sampler": {"seed": args.seed, "index": k, "edges_per_node": args.edges_per_node},
                   "sampled_at": _dt.datetime.now().isoformat(timespec="seconds")}
            f.write(json.dumps(rec, sort_keys=True) + "\n")
            f.flush()
            (per_arch_dir / f"{aid}.json").write_text(json.dumps(rec, indent=2, sort_keys=True))
            existing.add(aid)
            added += 1
            print(f"[{k}] {aid} {summarize(g)}")
    print(f"added {added}, skipped {skipped}; {out} now has {len(existing)} architectures")


if __name__ == "__main__":
    main()
