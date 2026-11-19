"""Fidelity study: the rank of a cheap training against the full-training label, on the seed subset of a city.

    python -m pilot.fidelity baselines --roots results/benchst/shenzhen_h12 results/benchst/expytky_h12 ...

``baselines`` reads the stored runs only (no GPU).  Per city, on the first N architectures that have 3 seeds:
* label = mean test MAE of seeds 0 to 2; sigma_seed = mean over the architectures of the standard deviation over the seeds;
* ceiling = Spearman inside the heads between seed 0 and the mean of seeds 1 and 2;
* epoch fidelity = the validation MAE of seed 0 after k epochs (the last logged epoch if the run stopped before k);
* successive halving on the logged curves of seed 0 (pilot.evalcost.successive_halving);
* the pooled transfer rank of the other cities (mean rank of the seed-0 test MAE); reported, cost zero at the target.
Every row: Spearman over all and inside the heads (count-weighted mean, bootstrap interval), the regret of the best of
the first 1 and 5 picks in sigma_seed, the cost share (logged seconds over the logged seconds of the full training of the
same architectures), and the cost to one sigma (the evaluator on all architectures plus the rest of the full training of
its picks, until a pick lies within one sigma_seed of the best label).
Tables: results/fidelity/compare/tables/baselines.csv, baselines.md.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

from pilot import evalcost as ec
from pilot.paths import Root

HEADS = ["mae", "mse", "quantile"]
OUT = "results/fidelity/compare/tables"
KS = list(range(1, 21))
SH = [(1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
POOL = ["metrla", "pems04", "chengdu", "shenzhen", "expytky", "pemsbay"]   # the cities of the evalscreen readings


def rho(a, b) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 4 or np.std(a[ok]) == 0 or np.std(b[ok]) == 0:
        return float("nan")
    return float(spearmanr(a[ok], b[ok]).correlation)


def within_head(score, y, head, idx=None) -> float:
    rs, ws = [], []
    for h in HEADS:
        i = np.where(head == h)[0] if idx is None else idx[h]
        r = rho(score[i], y[i])
        if np.isfinite(r):
            rs.append(r); ws.append(len(i))
    return float(np.average(rs, weights=ws)) if ws else float("nan")


def boot_within(score, y, head, n_boot: int = 1000, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    idx = {h: np.where(head == h)[0] for h in HEADS}
    b = [within_head(score, y, head, {h: rng.choice(idx[h], len(idx[h])) for h in HEADS}) for _ in range(n_boot)]
    return float(np.nanpercentile(b, 2.5)), float(np.nanpercentile(b, 97.5))


def load_city(root: Root, n_archs: int) -> dict:
    """The first n_archs of the list with 3 finished seeds: label, per-seed test MAE, head, the seed-0 curve."""
    rows, curves = [], {}
    for ln in open(root.archs_jsonl).readlines()[:n_archs]:
        rec = json.loads(ln); aid = rec["arch_id"]
        ms = []
        for s in (0, 1, 2):
            p = root.train / aid / f"seed{s}" / "metrics.json"
            m = json.load(open(p)) if p.exists() else {}
            if m.get("status") != "done":
                ms = None; break
            ms.append(m)
        if ms is None:
            continue
        t = [float(m["test_mae"]) for m in ms]
        rows.append({"arch_id": aid, "head": rec["genotype"]["head"], "label": float(np.mean(t)), "seed_std": float(np.std(t, ddof=1)),
                     "test0": t[0], "test12": float(np.mean(t[1:]))})
        curves[aid] = pd.DataFrame(ms[0]["history"])
    df = pd.DataFrame(rows)
    return {"name": root.dataset, "df": df, "curves": curves, "sigma": float(df.seed_std.mean()), "cost": ec.load_cost(root)}


def measure(c: dict, score: np.ndarray, eval_secs: np.ndarray, kind: str, name: str, extra: dict | None = None) -> dict:
    """score: higher = better; eval_secs[i] = seconds the evaluator spent on architecture i (a pick continues from there)."""
    df, curves = c["df"], c["curves"]
    y, head, sigma = df.label.values, df["head"].values, c["sigma"]
    full = np.array([float(curves[a].seconds.sum()) for a in df.arch_id])
    order = np.argsort(-np.where(np.isfinite(score), score, -np.inf), kind="stable")
    best = y.min()
    reg = lambda b: float(y[order[:b]].min() - best) / sigma
    lo, hi = boot_within(score, -y, head)
    b_sigma = next((b for b in range(1, len(y) + 1) if y[order[:b]].min() - best <= sigma), None)
    cost_sigma = float((eval_secs.sum() + (full - eval_secs)[order[:b_sigma]].sum()) / full.sum()) if b_sigma else float("nan")
    return {"city": c["name"], "kind": kind, "evaluator": name, "n": len(y), "rho": rho(score, -y), "rho_within_head": within_head(score, -y, head),
            "within_ci_lo": lo, "within_ci_hi": hi, "regret_b1_sigma": reg(1), "regret_b5_sigma": reg(5),
            "cost_share": float(eval_secs.sum() / full.sum()), "b_sigma": b_sigma, "cost_to_sigma_share": cost_sigma, **(extra or {})}


def pooled_rank(c: dict, source_roots: list[Root]) -> np.ndarray | None:
    ranks = []
    for r in source_roots:
        j = r.tables / "joined.csv"
        if r.dataset == c["name"] or r.dataset not in POOL or not j.exists():
            continue
        t = pd.read_csv(j).set_index("arch_id")["test_mae"]
        if not set(c["df"].arch_id) <= set(t.index):
            continue
        ranks.append(rankdata(t.values)[[list(t.index).index(a) for a in c["df"].arch_id]] / len(t))
    return -np.mean(ranks, axis=0) if ranks else None


def city_rows(c: dict, pool_roots: list[Root]) -> list[dict]:
    df, curves = c["df"], c["curves"]
    y, head = df.label.values, df["head"].values
    full = np.array([float(curves[a].seconds.sum()) for a in df.arch_id])
    lo, hi = boot_within(-df.test0.values, -df.test12.values, head)
    rows = [{"city": c["name"], "kind": "ceiling", "evaluator": "seed 0 against the mean of seeds 1 and 2", "n": len(y),
             "rho": rho(df.test0, df.test12), "rho_within_head": within_head(df.test0.values, df.test12.values, head),
             "within_ci_lo": lo, "within_ci_hi": hi, "cost_share": 1.0}]
    rows.append(measure(c, -df.test0.values, full, "full training", "seed 0, 20 epochs"))
    for k in KS:
        s = np.array([-float(curves[a].val_mae.iloc[min(k, len(curves[a])) - 1]) for a in df.arch_id])
        secs = np.array([float(curves[a].seconds.iloc[:min(k, len(curves[a]))].sum()) for a in df.arch_id])
        rows.append(measure(c, s, secs, "epoch fidelity", f"val MAE after {k} epochs", {"k": k}))
    d = df.rename(columns={"label": "target"})
    max_ep = int(max(len(v) for v in curves.values()))
    for r0, eta in SH:
        h = ec.successive_halving(d, curves, "target", r0, eta, max_ep)
        rows.append({"city": c["name"], "kind": "successive halving", "evaluator": f"r0 = {r0}, eta = {eta}", "n": len(y),
                     "regret_b1_sigma": h["regret_top1"] / c["sigma"], "regret_b5_sigma": h["regret_best_of_5"] / c["sigma"],
                     "cost_share": h["gpu_hours"] * 3600 / full.sum()})
    p = pooled_rank(c, pool_roots)
    if p is not None:
        rows.append(measure(c, p, np.zeros(len(y)), "transfer", "pooled rank of the other cities"))
    rng = np.random.default_rng(0)
    r1 = [y[rng.integers(len(y))] - y.min() for _ in range(5000)]
    r5 = [y[rng.choice(len(y), 5, replace=False)].min() - y.min() for _ in range(5000)]
    rows.append({"city": c["name"], "kind": "random", "evaluator": "random picks (mean of 5,000 draws)", "n": len(y),
                 "regret_b1_sigma": float(np.mean(r1)) / c["sigma"], "regret_b5_sigma": float(np.mean(r5)) / c["sigma"], "cost_share": 0.0})
    return rows


def cmd_baselines(roots: list[Root], n_archs: int, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    rows, meta = [], []
    for r in roots:
        c = load_city(r, n_archs)
        if len(c["df"]) < 20:
            print(f"{r.dataset}: {len(c['df'])} architectures with 3 seeds -> skipped"); continue
        rows += city_rows(c, roots)
        full_h = sum(float(v.seconds.sum()) for v in c["curves"].values()) / 3600
        meta.append({"city": c["name"], "n": len(c["df"]), "sigma_seed": c["sigma"], "heads": ", ".join(f"{h} {int((c['df']['head'] == h).sum())}" for h in HEADS),
                     "label_std_over_sigma": float(c["df"].label.std() / c["sigma"]), "full_hours_seed0": full_h,
                     "full_hours_seed0_ref": full_h / c["cost"]["cost_ratio"], "cluster": c["cost"]["cluster"]})
    t = pd.DataFrame(rows)
    t.to_csv(out / "baselines.csv", index=False)
    f = lambda v, d=2: "" if v is None or (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.{d}f}" if isinstance(v, float) else str(v))
    md = ["# fidelity baselines: stored runs of the seed subset", "",
          "Label = mean test MAE of seeds 0 to 2 (20 epochs, zero mask). Scores come from seed 0. rho is Spearman with the label; "
          "\"inside heads\" is the count-weighted mean of the per-head values with a bootstrap interval (1,000 draws). Regret is that of the best of the first b picks, "
          "in sigma_seed. Cost share = logged seconds over the logged seconds of the full training of the same architectures (seed 0). "
          "Cost to one sigma = the evaluator on all architectures plus the rest of the full training of its picks, until a pick lies within one sigma_seed of the best label.", ""]
    for m in meta:
        md += [f"## {m['city']}", "",
               f"N = {m['n']}; heads {m['heads']}; sigma_seed {m['sigma_seed']:.5f}; std of the label {m['label_std_over_sigma']:.2f} sigma_seed; "
               f"full training of seed 0: {m['full_hours_seed0']:.1f} GPU-hours logged on {m['cluster']}, {m['full_hours_seed0_ref']:.1f} on the reference unit.", "",
               "| kind | evaluator | rho | rho inside heads (95 % interval) | regret b = 1 | regret b = 5 | cost share | picks to one sigma | cost to one sigma |",
               "|---|---|---|---|---|---|---|---|---|"]
        for _, r in t[t.city == m["city"]].iterrows():
            ci = f" ({f(r.get('within_ci_lo'))}, {f(r.get('within_ci_hi'))})" if np.isfinite(r.get("within_ci_lo", np.nan)) else ""
            b = r.get("b_sigma"); b = "" if b is None or not np.isfinite(b) else str(int(b))
            md.append(f"| {r['kind']} | {r['evaluator']} | {f(r.get('rho'))} | {f(r.get('rho_within_head'))}{ci} | {f(r.get('regret_b1_sigma'))} | "
                      f"{f(r.get('regret_b5_sigma'))} | {f(r.get('cost_share'), 3)} | {b} | {f(r.get('cost_to_sigma_share'), 3)} |")
        md.append("")
    (out / "baselines.md").write_text("\n".join(md))
    print(f"wrote {out}/baselines.csv, baselines.md: {len(t)} rows, {len(meta)} cities")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["baselines"])
    ap.add_argument("--roots", nargs="+", required=True)
    ap.add_argument("--n-archs", type=int, default=50)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    if a.cmd == "baselines":
        cmd_baselines([Root(r) for r in a.roots], a.n_archs, Path(a.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
