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

    python -m pilot.fidelity proxy --city results/benchst/shenzhen_h12 --roots results/fidelity/shenzhen_h12_both_s25_t25 ...

``proxy`` reads the seed-0 runs of proxy-task roots (pilot.subset) against the label of the city root.  Score of a proxy task:
the best validation MAE of its run; and, per k, the validation MAE after k epochs of the proxy run.  Cost share = the logged
seconds of the proxy runs (plus the one test evaluation for the whole run) over the logged seconds of the full training of the
same architectures at the city.  A pick is trained from the start at the city, so the cost to one sigma adds the whole full
training of the picks.  ``baseline_at_cost`` = the epoch fidelity of the city at the same cost share (linear between two k);
``d`` = rho inside the heads less that baseline.  Tables: proxy_<city>.csv, proxy_<city>.md.

    python -m pilot.fidelity twotier --city results/benchst/shenzhen_h12 --roots results/fidelity/shenzhen_h12_both_s25_t25 ...

``twotier`` replays a rule of two stages on the stored logs (no GPU).  Stage A: every architecture runs kA epochs of the proxy
task; a share of them stays (the best of each head, or the best over all).  Stage B: the ones that stay run kB epochs at the
city; the picks are the best by the validation MAE there.  Cost share = the seconds of stage A and stage B over the full
training of all; ``cost_final5`` adds the rest of the full training of the first 5 picks.  The comparison rows use the same
measures: the epoch fidelity of the city alone, and successive halving on the city curves.  A third rule runs stage A and
then successive halving at the city on the ones that stay.  Table: twotier_<city>.csv.

    python -m pilot.fidelity filter --city results/benchst/shenzhen_h12 --roots results/fidelity/shenzhen_h12_list_both_s25_t25 --n-archs 150

``filter`` reads a proxy-task root with a longer part of the list.  Label = the seed-0 test MAE of the city; sigma_seed comes
from the architectures with 3 seeds.  A filter keeps a share of the list by a score after k epochs (the proxy task, or the
city itself); per filter: how many of the best 5 and of the best 10 % by label stay, rho inside the heads, the cost share,
and successive halving at the city (r0 = 2, eta = 3) on the ones that stay.  Table: filter_<city>.csv.
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


def measure(c: dict, score: np.ndarray, eval_secs: np.ndarray, kind: str, name: str, extra: dict | None = None, resume: bool = True) -> dict:
    """score: higher = better; eval_secs[i] = seconds the evaluator spent on architecture i (a pick continues from there)."""
    df, curves = c["df"], c["curves"]
    y, head, sigma = df.label.values, df["head"].values, c["sigma"]
    full = np.array([float(curves[a].seconds.sum()) for a in df.arch_id])
    order = np.argsort(-np.where(np.isfinite(score), score, -np.inf), kind="stable")
    best = y.min()
    reg = lambda b: float(y[order[:b]].min() - best) / sigma
    lo, hi = boot_within(score, -y, head)
    b_sigma = next((b for b in range(1, len(y) + 1) if y[order[:b]].min() - best <= sigma), None)
    rest = full - eval_secs if resume else full   # a proxy-task pick starts again at the city
    cost_sigma = float((eval_secs.sum() + rest[order[:b_sigma]].sum()) / full.sum()) if b_sigma else float("nan")
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


def cmd_proxy(city_root: Root, proxy_roots: list[Path], n_archs: int, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    c = load_city(city_root, n_archs)
    df = c["df"]
    base = pd.DataFrame([r for r in city_rows(c, []) if r["kind"] == "epoch fidelity"]).sort_values("cost_share")
    at_cost = lambda x: float(np.interp(x, base.cost_share.values, base.rho_within_head.values)) if np.isfinite(x) else float("nan")
    rows = []
    for pr in proxy_roots:
        hist, tsec, n_sens = {}, {}, None
        for a in df.arch_id:
            p = pr / "train" / a / "seed0" / "metrics.json"
            m = json.load(open(p)) if p.exists() else {}
            if m.get("status") == "done":
                hist[a] = pd.DataFrame(m["history"]); tsec[a] = float(m.get("test_seconds") or 0.0)
                n_sens = (m.get("schedule", {}).get("subset") or {}).get("n_sensors", n_sens)
        name = pr.name.replace(f"{city_root.dataset}_h{city_root.horizon}_", "")
        if len(hist) < len(df):
            print(f"{name}: {len(hist)} of {len(df)} runs done -> rows over the finished runs are not written"); continue
        H = [hist[a] for a in df.arch_id]
        ex = {"setting": name, "n_sensors": n_sens, "epochs_mean": float(np.mean([len(h) for h in H]))}
        s = np.array([-float(h.val_mae.min()) for h in H])
        secs = np.array([float(h.seconds.sum()) + tsec[a] for h, a in zip(H, df.arch_id)])
        rows.append(measure(c, s, secs, "proxy task", f"{name}: best val MAE of the run", {**ex, "k": None}, resume=False))
        for k in KS:
            s = np.array([-float(h.val_mae.iloc[min(k, len(h)) - 1]) for h in H])
            secs = np.array([float(h.seconds.iloc[:min(k, len(h))].sum()) for h in H])
            rows.append(measure(c, s, secs, "proxy task, k epochs", f"{name}: val MAE after {k} epochs", {**ex, "k": k}, resume=False))
    t = pd.DataFrame(rows)
    if len(t):
        t["baseline_at_cost"] = [at_cost(x) for x in t.cost_share]
        t["d"] = t.rho_within_head - t.baseline_at_cost
    t.to_csv(out / f"proxy_{city_root.dataset}.csv", index=False)
    f = lambda v, d=2: "" if v is None or (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.{d}f}" if isinstance(v, float) else str(v))
    md = [f"# fidelity: proxy tasks at {city_root.dataset}", "",
          f"N = {len(df)}; label = mean test MAE of seeds 0 to 2 at the city; sigma_seed {c['sigma']:.5f}. Proxy runs: seed 0. "
          "Baseline = the epoch fidelity of the city at the same cost share (linear between two k). d = rho inside heads less the baseline.", "",
          "| setting | score | rho | rho inside heads (95 % interval) | baseline at this cost | d | regret b = 1 | regret b = 5 | cost share | cost to one sigma |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in t.iterrows():
        k = r.get("k"); score = "best val MAE of the run" if k is None or not np.isfinite(k) else f"val MAE after {int(k)} epochs"
        md.append(f"| {r['setting']} | {score} | {f(r['rho'])} | {f(r['rho_within_head'])} ({f(r['within_ci_lo'])}, {f(r['within_ci_hi'])}) | {f(r['baseline_at_cost'])} | "
                  f"{f(r['d'])} | {f(r['regret_b1_sigma'])} | {f(r['regret_b5_sigma'])} | {f(r['cost_share'], 3)} | {f(r['cost_to_sigma_share'], 3)} |")
    (out / f"proxy_{city_root.dataset}.md").write_text("\n".join(md) + "\n")
    print(f"wrote {out}/proxy_{city_root.dataset}.csv and .md: {len(t)} rows")


def _picks(c: dict, order: np.ndarray, spent: np.ndarray, full: np.ndarray, extra: dict) -> dict:
    y, sigma = c["df"].label.values, c["sigma"]
    reg = lambda b: float(y[order[:b]].min() - y.min()) / sigma
    return {**extra, "regret_b1_sigma": reg(1), "regret_b5_sigma": reg(5), "cost_share": float(spent.sum() / full.sum()),
            "cost_final5": float((spent.sum() + (full - spent)[order[:5]].sum()) / full.sum())}


def cmd_twotier(city_root: Root, proxy_roots: list[Path], n_archs: int, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    c = load_city(city_root, n_archs)
    df, curves = c["df"], c["curves"]
    y, head, sigma = df.label.values, df["head"].values, c["sigma"]
    full = np.array([float(curves[a].seconds.sum()) for a in df.arch_id])
    val = lambda k: np.array([float(curves[a].val_mae.iloc[min(k, len(curves[a])) - 1]) for a in df.arch_id])
    sec = lambda k: np.array([float(curves[a].seconds.iloc[:min(k, len(curves[a]))].sum()) for a in df.arch_id])
    rows, stage_a = [], []
    for k in KS:
        rows.append(_picks(c, np.argsort(val(k), kind="stable"), sec(k), full, {"rule": "epoch fidelity", "setting": "city", "kB": k}))
    for pr in proxy_roots:
        name = pr.name.replace(f"{city_root.dataset}_h{city_root.horizon}_", "")
        H = []
        for a in df.arch_id:
            p = pr / "train" / a / "seed0" / "metrics.json"
            m = json.load(open(p)) if p.exists() else {}
            H.append(pd.DataFrame(m["history"]) if m.get("status") == "done" else None)
        if any(h is None for h in H):
            print(f"{name}: not every run is done -> skipped"); continue
        for kA in (2, 3, 5, 8):
            sA = np.array([float(h.val_mae.iloc[min(kA, len(h)) - 1]) for h in H])
            cA = np.array([float(h.seconds.iloc[:min(kA, len(h))].sum()) for h in H])
            for keep in (0.5, 0.3, 0.2):
                for how in ("per head", "over all"):
                    if how == "per head":
                        stay = np.concatenate([np.where(head == h)[0][np.argsort(sA[head == h], kind="stable")[:int(np.ceil(keep * (head == h).sum()))]] for h in HEADS])
                    else:
                        stay = np.argsort(sA, kind="stable")[:int(np.ceil(keep * len(y)))]
                        stage_a.append((name, kA, keep, stay, float(cA.sum())))
                    for kB in (2, 4, 8, 20):
                        vB = val(kB)
                        order = stay[np.argsort(vB[stay], kind="stable")]
                        spent = cA.copy(); spent[stay] += sec(kB)[stay]
                        rows.append(_picks(c, order, spent, full, {"rule": "two stages", "setting": name, "kA": kA, "keep": keep, "how": how, "kB": kB,
                                                                   "n_stay": len(stay), "best_stays": bool(int(np.argmin(y)) in stay),
                                                                   "best_staying_sigma": float(y[stay].min() - y.min()) / sigma}))
    d = df.rename(columns={"label": "target"})
    max_ep = int(max(len(v) for v in curves.values()))
    for name, kA, keep, stay, cA in stage_a:   # stage A, then successive halving at the city on the ones that stay
        ds = d.iloc[stay].reset_index(drop=True)
        off = float(ds.target.min() - y.min()) / sigma   # successive_halving counts its regret from the best that stays
        for r0, eta in SH:
            h = ec.successive_halving(ds, curves, "target", r0, eta, max_ep)
            rows.append({"rule": "proxy stage, then successive halving", "setting": f"{name}, r0 = {r0}, eta = {eta}", "kA": kA, "keep": keep, "how": "over all",
                         "n_stay": len(stay), "regret_b1_sigma": h["regret_top1"] / sigma + off, "regret_b5_sigma": h["regret_best_of_5"] / sigma + off,
                         "cost_share": (cA + h["gpu_hours"] * 3600) / full.sum()})
    for r0, eta in SH:
        h = ec.successive_halving(d, curves, "target", r0, eta, max_ep)
        rows.append({"rule": "successive halving", "setting": f"city, r0 = {r0}, eta = {eta}", "regret_b1_sigma": h["regret_top1"] / sigma,
                     "regret_b5_sigma": h["regret_best_of_5"] / sigma, "cost_share": h["gpu_hours"] * 3600 / full.sum()})
    t = pd.DataFrame(rows)
    t.to_csv(out / f"twotier_{city_root.dataset}.csv", index=False)
    print(f"wrote {out}/twotier_{city_root.dataset}.csv: {len(t)} rows")


def cmd_filter(city_root: Root, proxy_roots: list[Path], n_archs: int, out: Path, keep: float = 0.2) -> None:
    out.mkdir(parents=True, exist_ok=True)
    sigma = load_city(city_root, 50)["sigma"]
    rows = []
    for pr in proxy_roots:
        name = pr.name.replace(f"{city_root.dataset}_h{city_root.horizon}_", "")
        recs, curves, H = [], {}, []
        for ln in open(pr / "archs.jsonl").readlines()[:n_archs]:
            rec = json.loads(ln); a = rec["arch_id"]
            pc, pp = city_root.train / a / "seed0" / "metrics.json", pr / "train" / a / "seed0" / "metrics.json"
            mc, mp = (json.load(open(p)) if p.exists() else {} for p in (pc, pp))
            if mc.get("status") != "done" or mp.get("status") != "done":
                continue
            recs.append({"arch_id": a, "head": rec["genotype"]["head"], "target": float(mc["test_mae"])})
            curves[a] = pd.DataFrame(mc["history"]); H.append(pd.DataFrame(mp["history"]))
        df = pd.DataFrame(recs)
        n = len(df); y, head = df.target.values, df["head"].values
        full = np.array([float(curves[a].seconds.sum()) for a in df.arch_id])
        top5, top10p, m = set(np.argsort(y)[:5]), set(np.argsort(y)[:max(1, n // 10)]), int(np.ceil(keep * n))
        max_ep = int(max(len(v) for v in curves.values()))
        sh_all = ec.successive_halving(df, curves, "target", 2, 3, max_ep)
        rows.append({"setting": name, "filter": "none: successive halving at the city on all", "n": n, "n_stay": n,
                     "sh_regret_b1_sigma": sh_all["regret_top1"] / sigma, "sh_regret_b5_sigma": sh_all["regret_best_of_5"] / sigma,
                     "total_cost_share": sh_all["gpu_hours"] * 3600 / full.sum()})
        def one(label, score, secs, k):
            stay = np.argsort(score, kind="stable")[:m]
            lo, hi = boot_within(-score, -y, head)
            ds = df.iloc[stay].reset_index(drop=True)
            h = ec.successive_halving(ds, curves, "target", 2, 3, max_ep)
            off = float(ds.target.min() - y.min()) / sigma
            rows.append({"setting": name, "filter": label, "k": k, "n": n, "n_stay": m, "best_stays": bool(int(np.argmin(y)) in set(stay)),
                         "top5_stay": len(top5 & set(stay)), "top10pct_stay": len(top10p & set(stay)), "top10pct_n": len(top10p),
                         "best_staying_sigma": off, "rho": rho(-score, -y), "rho_within_head": within_head(-score, -y, head),
                         "within_ci_lo": lo, "within_ci_hi": hi, "cost_share": float(secs.sum() / full.sum()),
                         "sh_regret_b1_sigma": h["regret_top1"] / sigma + off, "sh_regret_b5_sigma": h["regret_best_of_5"] / sigma + off,
                         "total_cost_share": float((secs.sum() + h["gpu_hours"] * 3600) / full.sum())})
        for k in sorted({k for k in (2, 3, 5, 8) if k <= min(len(h) for h in H)}):
            one("proxy task", np.array([float(h.val_mae.iloc[k - 1]) for h in H]), np.array([float(h.seconds.iloc[:k].sum()) for h in H]), k)
        for k in (1, 2, 4):   # the city itself as the filter; its epochs are not used again by the second stage in this count
            one("city", np.array([float(curves[a].val_mae.iloc[min(k, len(curves[a])) - 1]) for a in df.arch_id]),
                np.array([float(curves[a].seconds.iloc[:min(k, len(curves[a]))].sum()) for a in df.arch_id]), k)
    t = pd.DataFrame(rows)
    t.to_csv(out / f"filter_{city_root.dataset}.csv", index=False)
    print(f"wrote {out}/filter_{city_root.dataset}.csv: {len(t)} rows")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["baselines", "proxy", "twotier", "filter"])
    ap.add_argument("--roots", nargs="+", required=True)
    ap.add_argument("--city", default=None, help="proxy: the benchst root of the city (labels)")
    ap.add_argument("--n-archs", type=int, default=50)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    if a.cmd == "baselines":
        cmd_baselines([Root(r) for r in a.roots], a.n_archs, Path(a.out))
    elif a.cmd == "proxy":
        cmd_proxy(Root(a.city), [Path(r) for r in a.roots], a.n_archs, Path(a.out))
    elif a.cmd == "filter":
        cmd_filter(Root(a.city), [Path(r) for r in a.roots], a.n_archs, Path(a.out))
    else:
        cmd_twotier(Root(a.city), [Path(r) for r in a.roots], a.n_archs, Path(a.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
