"""Sample N random genotypes -> append to results/archs.jsonl (append-only, de-duplicated by arch_id)
and write results/archs/<arch_id>.json.  Re-running the same command is a no-op.

W3: ``--space dartsts_graph_v1`` adds the graph cell (``--p-graph`` = probability that it is present,
``--require-graph-op`` redraws until the cell has at least one non-identity graph op)."""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import random
from pathlib import Path

from pilot.genotype import SPACE_V1, arch_id, has_graph_op, load_archs, random_genotype, summarize


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--space", default=SPACE_V1)
    ap.add_argument("--edges-per-node", type=int, default=2)
    ap.add_argument("--p-graph", type=float, default=1.0, help="graph space: probability of a graph cell")
    ap.add_argument("--require-graph-op", action="store_true", help="redraw until >= 1 non-identity graph op")
    ap.add_argument("--out", default="results/archs.jsonl")
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    per_arch_dir = out.parent / "archs"
    per_arch_dir.mkdir(exist_ok=True)
    existing = {r["arch_id"] for r in load_archs(out)} if out.exists() else set()

    rng = random.Random(args.seed)
    added, skipped, redraws = 0, 0, 0
    with open(out, "a") as f:
        for k in range(args.n):
            for attempt in range(1000):
                g = random_genotype(rng, args.space, args.edges_per_node, p_graph=args.p_graph)
                if not args.require_graph_op or has_graph_op(g):
                    break
                redraws += 1
            else:
                raise RuntimeError("could not draw a genotype with a non-identity graph op")
            aid = arch_id(g)
            if aid in existing:
                skipped += 1
                print(f"[{k}] {aid} already in {out} -> skip")
                continue
            rec = {"arch_id": aid, "genotype": g,
                   "sampler": {"seed": args.seed, "index": k, "edges_per_node": args.edges_per_node,
                               "p_graph": args.p_graph, "require_graph_op": args.require_graph_op},
                   "sampled_at": _dt.datetime.now().isoformat(timespec="seconds")}
            f.write(json.dumps(rec, sort_keys=True) + "\n")
            f.flush()
            (per_arch_dir / f"{aid}.json").write_text(json.dumps(rec, indent=2, sort_keys=True))
            existing.add(aid)
            added += 1
            print(f"[{k}] {aid} {summarize(g)}")
    print(f"added {added}, skipped {skipped}, redraws {redraws}; {out} now has {len(existing)} architectures")


if __name__ == "__main__":
    main()
