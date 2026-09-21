"""Sample N random genotypes -> append to <root>/archs.jsonl (append-only, de-duplicated by arch_id)
and write <root>/archs/<arch_id>.json.  Re-running the same command is a no-op.

P3: ``--space dartsts_graph_v1`` adds the graph cell (``--p-graph`` = probability that it is present,
``--require-graph-op`` redraws until the cell has at least one non-identity graph op)."""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import random
from pathlib import Path

from pilot.genotype import SPACE_V1, arch_id, graph_family, has_graph_op, load_archs, random_genotype, summarize
from pilot.paths import Root

# Section 3.5 stratification of the 50: 16 graph-blind, 34 with a graph cell of which >= 10 contain gcn, >= 10 contain
# diffusion and >= 6 are adaptive/identity-only (the built-in S_spatial = 0 control); the remaining 8 are any graph cell.
STRATA = {"none": 16, "gcn": 10, "diffusion": 10, "control": 6, "any_graph": 8}


def scaled_quota(n: int) -> dict:
    """The strata quotas scaled to n (rounded; the 'any graph' remainder absorbs the rounding)."""
    scale = n / sum(STRATA.values())
    quota = {k: int(round(v * scale)) for k, v in STRATA.items()}
    quota["any_graph"] += n - sum(quota.values())
    return quota


def stratum_candidates(g: dict) -> list[str]:
    """Strata a genotype can fill, most specific first."""
    fam = graph_family(g)
    if fam == "none":
        return ["none"]
    if fam in ("identity-only", "adaptive-only"):
        return ["control", "any_graph"]
    out = []
    if fam in ("gcn", "mixed"):
        out.append("gcn")
    if fam in ("diffusion", "mixed"):
        out.append("diffusion")
    return out + ["any_graph"]


def stratified_genotypes(rng, space, edges_per_node, n, existing_ids):
    """Rejection sampling until every stratum quota is filled (scaled to n); returns (genotypes, counts, draws)."""
    quota = scaled_quota(n)
    filled = {k: 0 for k in quota}
    out, seen, draws = [], set(existing_ids), 0
    while len(out) < n:
        draws += 1
        if draws > 200000:
            raise RuntimeError(f"stratified sampling stalled: filled {filled} of {quota}")
        need_none = filled["none"] < quota["none"]
        g = random_genotype(rng, space, edges_per_node, p_graph=0.0 if need_none and rng.random() < 0.5 else 1.0)
        aid = arch_id(g)
        if aid in seen:
            continue
        for stratum in stratum_candidates(g):
            if filled[stratum] < quota[stratum]:
                filled[stratum] += 1
                out.append((g, stratum))
                seen.add(aid)
                break
    return out, filled, draws



def main():
    ap = argparse.ArgumentParser()
    Root.add_args(ap)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--space", default=SPACE_V1)
    ap.add_argument("--edges-per-node", type=int, default=2)
    ap.add_argument("--p-graph", type=float, default=1.0, help="graph space: probability of a graph cell")
    ap.add_argument("--require-graph-op", action="store_true", help="redraw until >= 1 non-identity graph op")
    ap.add_argument("--stratify", action="store_true", help="graph space: fill the Section 3.5 strata (16/10/10/6/8 for n=50)")
    ap.add_argument("--overwrite", action="store_true", help="start a fresh file instead of appending")
    ap.add_argument("--out", default=None, help="default: <root>/archs.jsonl")
    args = ap.parse_args()

    out = Path(args.out) if args.out else Root.from_args(args).archs_jsonl
    out.parent.mkdir(parents=True, exist_ok=True)
    per_arch_dir = out.parent / "archs"
    per_arch_dir.mkdir(exist_ok=True)
    if args.overwrite and out.exists():
        out.unlink()
    existing = {r["arch_id"] for r in load_archs(out)} if out.exists() else set()

    rng = random.Random(args.seed)
    added, skipped, redraws = 0, 0, 0
    strata_counts = None
    if args.stratify:
        drawn, strata_counts, redraws = stratified_genotypes(rng, args.space, args.edges_per_node, args.n, existing)
        print(f"stratified: {strata_counts} after {redraws} draws")
    with open(out, "a") as f:
        for k in range(args.n):
            stratum = None
            if args.stratify:
                g, stratum = drawn[k]
            else:
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
                               "p_graph": args.p_graph, "require_graph_op": args.require_graph_op,
                               "stratify": args.stratify, "stratum": stratum, "graph_family": graph_family(g)},
                   "sampled_at": _dt.datetime.now().isoformat(timespec="seconds")}
            f.write(json.dumps(rec, sort_keys=True) + "\n")
            f.flush()
            (per_arch_dir / f"{aid}.json").write_text(json.dumps(rec, indent=2, sort_keys=True))
            existing.add(aid)
            added += 1
            print(f"[{k}] {aid} {summarize(g)}")
    print(f"added {added}, skipped {skipped}, redraws {redraws}; {out} now has {len(existing)} architectures")
    if args.stratify:
        from collections import Counter
        fams = Counter(graph_family(r["genotype"]) for r in load_archs(out))
        print("graph_family counts:", dict(fams))


if __name__ == "__main__":
    main()
