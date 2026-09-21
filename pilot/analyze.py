"""Phase 8 analysis (Section 5): one script from the JSON files to results/tables/{joined.csv, table_A.*, table_B*.*}.

    python -m pilot.analyze --archs results/archs.jsonl --proxies results/proxies/v1 --spatial results/proxies/spatial_v2 \
        --train results/train --out results/tables

Sign convention (Section 5): every score is correlated with -val_mae, so a *good* proxy has positive Spearman and the
LENAS naswot reference (0.737 on its space) compares directly.  No proxy is sign-flipped.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, rankdata, spearmanr

from pilot.genotype import graph_family, load_archs

PROXIES_PRIMARY = ["nwot", "zico", "synflow_all", "snip_all", "grad_norm_all", "grasp_all", "plain_all", "fisher", "jacov", "zen",
                   "l2_norm_all", "params", "flops"]                      # the 13 of Table A (_all variants as primary)
PROXIES_NASLIB = ["synflow", "snip", "grad_norm", "grasp", "plain", "l2_norm"]  # Conv/Linear-only copies, appendix rows
EXTRA = ["tfas_zico_cl"]
CONTROL_FAMILIES = ("none", "identity-only", "adaptive-only")


def family_labels(g: dict) -> dict:
    fam = graph_family(g)
    seq_ops = [op for _, _, op in g["seq"]["encoder"] if op is not None]
    flat_ops = [op for _, _, op in g["flat"]["cell"] if op is not None]
    return {"graph_family": fam, "has_graph": fam != "none", "uses_A": fam not in CONTROL_FAMILIES,
            "group3": "graph-blind" if fam == "none" else ("control" if fam in CONTROL_FAMILIES else "uses A"),
            "seq_family": Counter(seq_ops).most_common(1)[0][0] if seq_ops else "none",
            "flat_family": Counter(flat_ops).most_common(1)[0][0] if flat_ops else "none",
            "head": g["head"], "decoder": g["seq"]["decoder_type"]}


def load_joined(archs, proxies_dir, spatial_dir, train_dir, seed=0) -> pd.DataFrame:
    rows = []
    for r in archs:
        g, aid = r["genotype"], r["arch_id"]
        m = Path(train_dir) / aid / f"seed{seed}" / "metrics.json"
        if not m.exists():
            continue
        met = json.load(open(m))
        if met.get("status") != "done":
            continue
        row = {"arch_id": aid, "val_mae": met["val_mae"], "val_mse": met["val_mse"], "test_mae": met["test_mae"],
               "test_mse": met["test_mse"], "test_rmse": math.sqrt(met["test_mse"]), "params": met["params"], "flops": met["flops"],
               "train_seconds": met["train_seconds"], "epochs_run": met["epochs_run"], "best_epoch": met["best_epoch"],
               "peak_mem_gb": met["peak_mem_gb"], **family_labels(g)}
        seeds = {}
        for s in (1, 2):
            ms = Path(train_dir) / aid / f"seed{s}" / "metrics.json"
            if ms.exists() and json.load(open(ms)).get("status") == "done":
                seeds[s] = json.load(open(ms))["val_mae"]
        row["val_mae_seed1"], row["val_mae_seed2"] = seeds.get(1, np.nan), seeds.get(2, np.nan)
        p = json.load(open(Path(proxies_dir) / f"{aid}.json"))
        for name, per_seed in p["scores"].items():
            vals = [v for v in per_seed.values() if v is not None and np.isfinite(v)]
            row[name] = float(np.mean(vals)) if vals else np.nan
            row[name + "_seedstd"] = float(np.std(vals)) if len(vals) > 1 else np.nan
        sp_path = Path(spatial_dir) / f"{aid}.json"
        if sp_path.exists():
            sp = json.load(open(sp_path))
            for base, br in sp["bases"].items():
                row[f"S_spatial_{base}"] = br.get("S_spatial_mean_over_seeds", np.nan)
                row[f"z_spatial_{base}"] = br.get("z_spatial_mean_over_seeds", np.nan)
                row[f"{base}_underA_v2"] = br.get("A_mean_over_seeds", np.nan)
                row[f"{base}_permmean"] = br.get("perm_mean_over_seeds", np.nan)
        rows.append(row)
    return pd.DataFrame(rows)


def corr(df: pd.DataFrame, proxy: str, target: str = "val_mae", n_boot: int = 2000, seed: int = 0) -> dict:
    """Spearman / Kendall of proxy with -target (positive = higher proxy, lower MAE) with a 95% bootstrap CI."""
    d = df[[proxy, target]].dropna()
    x, y = d[proxy].values.astype(float), -d[target].values.astype(float)
    if len(x) < 3 or np.std(x) == 0:
        return dict(n=len(x), spearman=np.nan, ci_lo=np.nan, ci_hi=np.nan, kendall=np.nan, p=np.nan)
    rho, p = spearmanr(x, y)
    tau = kendalltau(x, y).correlation
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        i = rng.integers(0, len(x), len(x))
        if np.std(x[i]) > 0 and np.std(y[i]) > 0:
            boots.append(spearmanr(x[i], y[i]).correlation)
    lo, hi = np.nanpercentile(boots, [2.5, 97.5]) if boots else (np.nan, np.nan)
    return dict(n=int(len(x)), spearman=float(rho), ci_lo=float(lo), ci_hi=float(hi), kendall=float(tau), p=float(p))


def partial_spearman(df: pd.DataFrame, proxy: str, control: str = "params", target: str = "val_mae") -> float:
    d = df[[proxy, control, target]].dropna()
    if len(d) < 4:
        return np.nan
    rx, rc, ry = rankdata(d[proxy]), rankdata(np.log(d[control])), rankdata(-d[target])

    def resid(a, b):
        b1 = np.c_[np.ones_like(b), b]
        return a - b1 @ np.linalg.lstsq(b1, a, rcond=None)[0]
    return float(spearmanr(resid(rx, rc), resid(ry, rc)).correlation)


def z(s: pd.Series) -> pd.Series:
    return (s - s.mean()) / s.std(ddof=0)


def fmt(v, nd=2):
    return "—" if v is None or (isinstance(v, float) and not np.isfinite(v)) else f"{v:.{nd}f}"


def table_A(df: pd.DataFrame, proxies: list[str], min_n: int = 8) -> pd.DataFrame:
    out = []
    subsets = [("graph-blind", df[~df.has_graph]), ("has graph", df[df.has_graph]), ("uses A", df[df.uses_A]),
               ("gcn (incl. mixed)", df[df.graph_family.isin(["gcn", "mixed"])]),
               ("diffusion (incl. mixed)", df[df.graph_family.isin(["diffusion", "mixed"])])]
    for h in ["mse", "mae", "quantile"]:
        subsets.append((f"head={h}", df[df["head"] == h]))
    for p in proxies:
        if p not in df:
            continue
        r = {"proxy": p, **corr(df, p)}
        r["partial_params"] = partial_spearman(df, p) if p not in ("params", "flops") else np.nan
        r["seed_cv"] = float(np.nanmedian(df[p + "_seedstd"] / df[p].abs())) if p + "_seedstd" in df else np.nan
        for lab, sub in subsets:  # point estimates only (their CIs at n = 16-34 are wide; the figure shows them)
            r[lab] = corr(sub, p, n_boot=0)["spearman"] if len(sub) >= min_n else np.nan
            r[lab + " (n)"] = len(sub)
        out.append(r)
    return pd.DataFrame(out).sort_values("spearman", ascending=False)


def table_B(df: pd.DataFrame, base: str) -> pd.DataFrame:
    df = df.copy()
    temporal = base  # TFAS not applicable (Phase 7) -> the temporal term is the base proxy itself
    df["composite"] = z(df[base]) + z(df[f"S_spatial_{base}"])
    df["composite_z_spatial"] = z(df[base]) + z(df[f"z_spatial_{base}"])
    rows = [(f"{base} alone (under A)", base), (f"S_spatial ({base})", f"S_spatial_{base}"), (f"z_spatial ({base})", f"z_spatial_{base}"),
            (f"composite = z({temporal}) + z(S_spatial)", "composite"), (f"composite = z({temporal}) + z(z_spatial)", "composite_z_spatial")]
    out = []
    for lab, col in rows:
        c = corr(df, col)
        out.append({"score": lab, **c, "graph_archs_only": corr(df[df.has_graph], col)["spearman"],
                    "uses_A_only": corr(df[df.uses_A], col)["spearman"], "beats_0.737": bool(c["spearman"] > 0.737)})
    return pd.DataFrame(out)


def detection_table(df: pd.DataFrame, bases: list[str]) -> pd.DataFrame:
    out = []
    for base in bases:
        col = f"z_spatial_{base}"
        if col not in df:
            continue
        ctrl, sens = df[~df.uses_A][col], df[df.uses_A][col]
        out.append({"base": base, "controls n": len(ctrl), "controls max |z|": float(ctrl.abs().max()),
                    "uses-A n": len(sens), "uses-A median z": float(sens.median()), "uses-A min z": float(sens.min()),
                    "uses-A max z": float(sens.max()), "uses-A |z|>3": int((sens.abs() > 3).sum()),
                    "uses-A score(A) > perm mean": int((df[df.uses_A][f"{base}_underA_v2"] > df[df.uses_A][f"{base}_permmean"]).sum())})
    return pd.DataFrame(out)


def seed_ceiling(df: pd.DataFrame) -> dict:
    d = df.dropna(subset=["val_mae_seed1", "val_mae_seed2"])
    if len(d) < 3:
        return {"n": len(d)}
    return {"n": int(len(d)), "spearman_s0_s1": float(spearmanr(d.val_mae, d.val_mae_seed1).correlation),
            "spearman_s0_s2": float(spearmanr(d.val_mae, d.val_mae_seed2).correlation),
            "spearman_s1_s2": float(spearmanr(d.val_mae_seed1, d.val_mae_seed2).correlation),
            "within_arch_std_mean": float(np.mean(np.std(d[["val_mae", "val_mae_seed1", "val_mae_seed2"]].values, axis=1))),
            "across_arch_std": float(df.val_mae.std(ddof=0))}


def md_table_A(tA: pd.DataFrame, ceiling: dict, title: str) -> str:
    cols = ["graph-blind", "has graph", "uses A", "gcn (incl. mixed)", "diffusion (incl. mixed)"]
    ns = {c: int(tA[c + " (n)"].iloc[0]) for c in cols}
    lines = [f"# {title}", "", "Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. "
             "95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.", "",
             f"| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \\| log params | seed CV | " + " | ".join(f"{c} (n={ns[c]})" for c in cols) + " |",
             "|---|---|---|---|---|---|---|---|" + "---|" * len(cols)]
    if ceiling.get("n", 0) >= 3:
        lines.append(f"| seed-noise ceiling (val MAE seed 0 vs 1 / 0 vs 2 / 1 vs 2) | {ceiling['n']} | {fmt(ceiling['spearman_s0_s1'])} / {fmt(ceiling['spearman_s0_s2'])} / {fmt(ceiling['spearman_s1_s2'])} | 1.00 | — | — | — | within-arch std {ceiling['within_arch_std_mean']:.4f} vs across-arch {ceiling['across_arch_std']:.4f} | " + " | ".join("—" for _ in cols) + " |")
    ceil = ceiling.get("spearman_s0_s1")
    for _, r in tA.iterrows():
        name = f"`{r.proxy}` (complexity baseline)" if r.proxy in ("params", "flops") else f"`{r.proxy}`"
        ratio = f"{r.spearman / ceil:+.2f}" if ceil else "—"
        lines.append(f"| {name} | {r.n} | {fmt(r.spearman)} ({fmt(r.ci_lo)}, {fmt(r.ci_hi)}) | {ratio} | {fmt(r.kendall)} | {r.p:.3g} | {fmt(r.partial_params)} | {fmt(r.seed_cv, 3)} | "
                     + " | ".join(fmt(r[c]) for c in cols) + " |")
    if ceil:
        lines.append("")
        lines.append(f"ρ/ceiling = Spearman divided by the seed-noise ceiling {ceil:.2f} (seed-0 vs seed-1 val MAE on the 5 repeated archs): the fraction of the achievable rank agreement a proxy reaches.")
    return "\n".join(lines) + "\n"


def md_table_B(tB: pd.DataFrame, det: pd.DataFrame, base: str) -> str:
    lines = [f"# Table B — Experiment B, base = {base}", "",
             "Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.", "",
             "| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=34) | uses-A archs only (n=28) | beats 0.737? |", "|---|---|---|---|---|---|---|"]
    for _, r in tB.iterrows():
        lines.append(f"| {r.score} | {r.n} | {fmt(r.spearman)} ({fmt(r.ci_lo)}, {fmt(r.ci_hi)}) | {fmt(r.kendall)} | {fmt(r.graph_archs_only)} | {fmt(r.uses_A_only)} | {'yes' if r['beats_0.737'] else 'no'} |")
    lines += ["", "Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).", "",
              "| Base | controls n | controls max \\|z\\| | uses-A n | uses-A median z (min, max) | uses-A with \\|z\\| > 3 | uses-A with score(A) > permuted mean |", "|---|---|---|---|---|---|---|"]
    for _, r in det.iterrows():
        lines.append(f"| `{r.base}` | {r['controls n']} | {r['controls max |z|']:.1e} | {r['uses-A n']} | {r['uses-A median z']:+.1f} ({r['uses-A min z']:+.1f}, {r['uses-A max z']:+.1f}) | {r['uses-A |z|>3']}/{r['uses-A n']} | {r['uses-A score(A) > perm mean']}/{r['uses-A n']} |")
    return "\n".join(lines) + "\n"


def table_A_partial(df: pd.DataFrame, proxies: list[str]) -> pd.DataFrame:
    """Committee question 1: is it just parameter count?  Size-likeness, partials on log params / log flops, within-size-tercile
    Spearman, and alternative targets (test MAE, val MSE)."""
    d = df.copy()
    d["size_tercile"] = pd.qcut(np.log(d.params), 3, labels=["small", "mid", "large"])
    out = []
    for p in proxies:
        if p not in d:
            continue
        r = {"proxy": p, "spearman": corr(d, p, n_boot=0)["spearman"],
             "rho_with_log_params": float(spearmanr(d[p], np.log(d.params)).correlation),
             "partial_params": partial_spearman(d, p, "params") if p != "params" else np.nan,
             "partial_flops": partial_spearman(d, p, "flops") if p != "flops" else np.nan,
             "rho_test_mae": corr(d, p, target="test_mae", n_boot=0)["spearman"],
             "rho_val_mse": corr(d, p, target="val_mse", n_boot=0)["spearman"]}
        for t in ["small", "mid", "large"]:
            sub = d[d.size_tercile == t]
            r[f"tercile_{t}"] = corr(sub, p, n_boot=0)["spearman"]
            r[f"tercile_{t}_n"] = len(sub)
        out.append(r)
    return pd.DataFrame(out).sort_values("spearman", ascending=False)


def md_table_A_partial(t: pd.DataFrame) -> str:
    ns = {k: int(t[f"tercile_{k}_n"].iloc[0]) for k in ("small", "mid", "large")}
    lines = ["# Table A (partial) — is the correlation just parameter count?", "",
             "All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). "
             "ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target "
             "(rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.", "",
             f"| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \\| log params | partial ρ \\| log flops | small third (n={ns['small']}) | mid third (n={ns['mid']}) | large third (n={ns['large']}) | ρ (test MAE) | ρ (val MSE) |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in t.iterrows():
        name = f"`{r.proxy}` (complexity baseline)" if r.proxy in ("params", "flops") else f"`{r.proxy}`"
        lines.append(f"| {name} | {fmt(r.spearman)} | {fmt(r.rho_with_log_params)} | {fmt(r.partial_params)} | {fmt(r.partial_flops)} | {fmt(r.tercile_small)} | {fmt(r.tercile_mid)} | {fmt(r.tercile_large)} | {fmt(r.rho_test_mae)} | {fmt(r.rho_val_mse)} |")
    return "\n".join(lines) + "\n"


def subsample_curve(df: pd.DataFrame, proxies: list[str], sizes=(10, 20, 30, 40, 50), n_rep: int = 500, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    out = []
    for p in proxies:
        x, y = df[p].values.astype(float), -df.val_mae.values.astype(float)
        for n in sizes:
            vals = []
            for _ in range(n_rep if n < len(x) else 1):
                i = rng.choice(len(x), n, replace=False)
                vals.append(spearmanr(x[i], y[i]).correlation)
            out.append({"proxy": p, "N": n, "median": float(np.nanmedian(vals)), "p5": float(np.nanpercentile(vals, 5)),
                        "p95": float(np.nanpercentile(vals, 95)), "frac_positive": float(np.mean(np.array(vals) > 0)),
                        "frac_above_0.4": float(np.mean(np.array(vals) > 0.4))})
    return pd.DataFrame(out)


def required_n(half_width: float, conf_z: float = 1.96) -> int:
    """Fisher-z approximation for Spearman: se ≈ 1.06 / sqrt(N - 3)."""
    return int(math.ceil(3 + (1.06 * conf_z / half_width) ** 2))


def md_ci_summary(tA: pd.DataFrame, curve: pd.DataFrame, ceiling: dict) -> str:
    lines = ["# CI summary — is N = 50 enough, and does the sign convention match LENAS?", "",
             "## Sign convention", "",
             "Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot "
             "score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared "
             "directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.", "",
             "## Bootstrap CIs (2000 resamples over the 50 architectures)", "",
             "| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |", "|---|---|---|---|---|---|"]
    for _, r in tA.iterrows():
        hw = (r.ci_hi - r.ci_lo) / 2
        lines.append(f"| `{r.proxy}` | {fmt(r.spearman)} | ({fmt(r.ci_lo)}, {fmt(r.ci_hi)}) | {hw:.2f} | {'yes' if (r.ci_lo > 0 or r.ci_hi < 0) else 'no'} | {'yes' if r.ci_hi < 0.737 else 'no'} |")
    lines += ["", "## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)", "",
              "| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |", "|---|---|---|---|---|---|---|"]
    for _, r in curve.iterrows():
        lines.append(f"| `{r.proxy}` | {int(r.N)} | {r['median']:+.2f} | {r.p5:+.2f} | {r.p95:+.2f} | {r.frac_positive:.2f} | {r['frac_above_0.4']:.2f} |")
    lines += ["", "## How large must N be? (Fisher-z approximation, se ≈ 1.06/√(N−3), 95 % CI)", "",
              "| CI half-width | N needed |", "|---|---|"] + [f"| ±{hw:.2f} | {required_n(hw)} |" for hw in (0.30, 0.20, 0.15, 0.10, 0.05)]
    lines += ["", f"At N = 50 the expected half-width is ±{1.06 * 1.96 / math.sqrt(47):.2f}, which is what the bootstrap shows (±0.15–0.30). "
              "Separating a proxy at ρ ≈ 0.65 from the 0.737 reference needs a half-width below ≈ 0.09, i.e. N ≈ 500; separating it from 0 needs N ≈ 20.", "",
              "## Seed-noise ceiling", "",
              f"Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the {ceiling.get('n')} repeated archs: "
              f"{fmt(ceiling.get('spearman_s0_s1'))} / {fmt(ceiling.get('spearman_s0_s2'))} / {fmt(ceiling.get('spearman_s1_s2'))}; "
              f"within-arch std {ceiling.get('within_arch_std_mean', float('nan')):.4f} vs across-arch std {ceiling.get('across_arch_std', float('nan')):.4f}. "
              "The ground truth is not the limiting factor at N = 50.", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archs", default="results/archs.jsonl")
    ap.add_argument("--proxies", default="results/proxies/v1")
    ap.add_argument("--spatial", default="results/proxies/spatial_v2")
    ap.add_argument("--train", default="results/train")
    ap.add_argument("--out", default="results/tables")
    ap.add_argument("--n-boot", type=int, default=2000)
    args = ap.parse_args()
    t0 = time.time()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    archs = load_archs(args.archs)
    df = load_joined(archs, args.proxies, args.spatial, args.train)
    df.to_csv(out / "joined.csv", index=False)
    n_done = sum(1 for r in archs if (Path(args.train) / r["arch_id"] / "seed0" / "metrics.json").exists()
                 and json.load(open(Path(args.train) / r["arch_id"] / "seed0" / "metrics.json")).get("status") == "done")
    print(f"joined.csv: {len(df)} rows ({n_done} done trainings); families {df.graph_family.value_counts().to_dict()}")
    ceiling = seed_ceiling(df)
    print("seed ceiling:", ceiling)
    tA = table_A(df, PROXIES_PRIMARY)
    tA.to_csv(out / "table_A.csv", index=False)
    (out / "table_A.md").write_text(md_table_A(tA, ceiling, "Table A — Experiment A (13 proxies, all-parameter variants as primary)"))
    tA2 = table_A(df, PROXIES_NASLIB + [e for e in EXTRA if e in df])
    tA2.to_csv(out / "table_A_naslib.csv", index=False)
    (out / "table_A_naslib.md").write_text(md_table_A(tA2, {}, "Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score"))
    bases = [c[len("S_spatial_"):] for c in df.columns if c.startswith("S_spatial_")]
    det = detection_table(df, bases)
    det.to_csv(out / "table_B_detection.csv", index=False)
    for base in bases:
        tB = table_B(df, base)
        tB.to_csv(out / f"table_B_{base}.csv", index=False)
        (out / f"table_B_{base}.md").write_text(md_table_B(tB, det, base))
    if "nwot" in bases:
        (out / "table_B.md").write_text((out / "table_B_nwot.md").read_text())
        (out / "table_B.csv").write_text((out / "table_B_nwot.csv").read_text())
    # Phase 9: robustness tables
    tP = table_A_partial(df, PROXIES_PRIMARY)
    tP.to_csv(out / "table_A_partial.csv", index=False)
    (out / "table_A_partial.md").write_text(md_table_A_partial(tP))
    curve = subsample_curve(df, ["zico", "l2_norm_all", "params", "grasp_all", "zen", "nwot", "snip_all"])
    curve.to_csv(out / "subsample_curve.csv", index=False)
    (out / "ci_summary.md").write_text(md_ci_summary(tA, curve, ceiling))
    json.dump({"n_rows": int(len(df)), "n_done": n_done, "seed_ceiling": ceiling, "bases": bases, "seconds": round(time.time() - t0, 1)},
              open(out / "analyze_summary.json", "w"), indent=2)
    print(tA[["proxy", "n", "spearman", "ci_lo", "ci_hi", "kendall", "partial_params"]].to_string(index=False, float_format=lambda v: f"{v:+.2f}"))
    print(f"done in {time.time() - t0:.1f}s -> {out}")


if __name__ == "__main__":
    main()
