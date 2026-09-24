"""Phase 8 analysis (Section 5): one script from the JSON files to <root>/tables/{joined.csv, table_A.*, table_B*.*}.

    python -m pilot.analyze --root results                       # the Pilot 1 tree (PEMS04 h12)
    python -m pilot.analyze --root results/pems08_h12 --n-boot 2000 --subgroup-ci
    python -m pilot.analyze --compare results results/pems08_h12 results/pems04_h36 results/metrla_h12 \
        --n50 results/tables_n50/table_A.csv --out results/tables_pilot2          # Phase 5 cross-setting table
(``--archs``, ``--proxies``, ``--spatial``, ``--train`` and ``--out`` default to the root's files.)

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
from pilot.paths import Root

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


def table_A(df: pd.DataFrame, proxies: list[str], min_n: int = 8, subgroup_ci: bool = False, n_boot: int = 2000) -> pd.DataFrame:
    out = []
    subsets = [("graph-blind", df[~df.has_graph]), ("has graph", df[df.has_graph]), ("uses A", df[df.uses_A]),
               ("gcn (incl. mixed)", df[df.graph_family.isin(["gcn", "mixed"])]),
               ("diffusion (incl. mixed)", df[df.graph_family.isin(["diffusion", "mixed"])])]
    for h in ["mse", "mae", "quantile"]:
        subsets.append((f"head={h}", df[df["head"] == h]))
    for p in proxies:
        if p not in df:
            continue
        r = {"proxy": p, **corr(df, p, n_boot=n_boot)}
        r["partial_params"] = partial_spearman(df, p) if p not in ("params", "flops") else np.nan
        r["seed_cv"] = float(np.nanmedian(df[p + "_seedstd"] / df[p].abs())) if p + "_seedstd" in df else np.nan
        for lab, sub in subsets:  # point estimates by default (their CIs at n = 16-34 are wide); --subgroup-ci adds bootstrap CIs
            c = corr(sub, p, n_boot=n_boot if subgroup_ci else 0) if len(sub) >= min_n else {"spearman": np.nan, "ci_lo": np.nan, "ci_hi": np.nan}
            r[lab] = c["spearman"]
            r[lab + " (n)"] = len(sub)
            if subgroup_ci:
                r[lab + " ci_lo"], r[lab + " ci_hi"] = c["ci_lo"], c["ci_hi"]
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
    def sub_cell(r, c):
        if c + " ci_lo" in r and np.isfinite(r[c + " ci_lo"]):
            return f"{fmt(r[c])} ({fmt(r[c + ' ci_lo'])}, {fmt(r[c + ' ci_hi'])})"
        return fmt(r[c])
    for _, r in tA.iterrows():
        name = f"`{r.proxy}` (complexity baseline)" if r.proxy in ("params", "flops") else f"`{r.proxy}`"
        ratio = f"{r.spearman / ceil:+.2f}" if ceil else "—"
        lines.append(f"| {name} | {r.n} | {fmt(r.spearman)} ({fmt(r.ci_lo)}, {fmt(r.ci_hi)}) | {ratio} | {fmt(r.kendall)} | {r.p:.3g} | {fmt(r.partial_params)} | {fmt(r.seed_cv, 3)} | "
                     + " | ".join(sub_cell(r, c) for c in cols) + " |")
    if ceil:
        lines.append("")
        lines.append(f"ρ/ceiling = Spearman divided by the seed-noise ceiling {ceil:.2f} (seed-0 vs seed-1 val MAE on the {ceiling.get('n')} repeated archs): the fraction of the achievable rank agreement a proxy reaches.")
    return "\n".join(lines) + "\n"


def md_table_B(tB: pd.DataFrame, det: pd.DataFrame, base: str, n_graph: int = 34, n_uses_a: int = 28) -> str:
    lines = [f"# Table B — Experiment B, base = {base}", "",
             "Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.", "",
             f"| Score | N | Spearman (95% CI) | Kendall | graph archs only (n={n_graph}) | uses-A archs only (n={n_uses_a}) | beats 0.737? |", "|---|---|---|---|---|---|---|"]
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


def curve_sizes(n: int) -> tuple:
    """(10, 20, 30, 40, 50) for N = 50; larger trees add 100, 150, ... up to N and always end at N."""
    sizes = [s for s in (10, 20, 30, 40, 50, 100, 150, 200, 250, 300, 400, 500) if s < n] + [n]
    return tuple(sizes)


def subsample_curve(df: pd.DataFrame, proxies: list[str], sizes=None, n_rep: int = 500, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    sizes = sizes or curve_sizes(len(df))
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


def md_ci_summary(tA: pd.DataFrame, curve: pd.DataFrame, ceiling: dict, n: int = 50, n_boot: int = 2000) -> str:
    lines = [f"# CI summary — is N = {n} enough, and does the sign convention match LENAS?", "",
             "## Sign convention", "",
             "Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot "
             "score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared "
             "directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.", "",
             f"## Bootstrap CIs ({n_boot} resamples over the {n} architectures)", "",
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
    lines += ["", f"At N = {n} the expected half-width is ±{1.06 * 1.96 / math.sqrt(n - 3):.2f}, which is what the bootstrap shows (±0.15–0.30). "
              "Separating a proxy at ρ ≈ 0.65 from the 0.737 reference needs a half-width below ≈ 0.09, i.e. N ≈ 500; separating it from 0 needs N ≈ 20.", "",
              "## Seed-noise ceiling", "",
              f"Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the {ceiling.get('n')} repeated archs: "
              f"{fmt(ceiling.get('spearman_s0_s1'))} / {fmt(ceiling.get('spearman_s0_s2'))} / {fmt(ceiling.get('spearman_s1_s2'))}; "
              f"within-arch std {ceiling.get('within_arch_std_mean', float('nan')):.4f} vs across-arch std {ceiling.get('across_arch_std', float('nan')):.4f}. "
              "The ground truth is not the limiting factor at N = 50.", ""]
    return "\n".join(lines)


def compare_roots(roots: list, out: Path, n50_csv=None, proxies=PROXIES_PRIMARY) -> dict:
    """Phase 5: one table with every root's Table A side by side, the rank agreement of the proxy *ordering* between the
    first root and each other root, and (with --n50) the N = 50 vs N = 300 comparison for the first root."""
    out.mkdir(parents=True, exist_ok=True)
    tabs, summs = {}, {}
    for r in roots:
        tabs[r.label] = pd.read_csv(r.tables / "table_A.csv").set_index("proxy")
        summs[r.label] = json.load(open(r.tables / "analyze_summary.json"))
    labels = [r.label for r in roots]
    rows = []
    for p in proxies:
        row = {"proxy": p}
        for lab in labels:
            t = tabs[lab]
            if p in t.index:
                row[f"{lab} n"] = int(t.loc[p, "n"])
                for k in ("spearman", "ci_lo", "ci_hi", "partial_params"):
                    row[f"{lab} {k}"] = float(t.loc[p, k])
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(out / "cross_dataset.csv", index=False)
    ref = labels[0]
    agree = []
    for lab in labels[1:]:
        a, b = df[f"{ref} spearman"], df[f"{lab} spearman"]
        m = a.notna() & b.notna()
        agree.append({"pair": f"{ref} vs {lab}", "n_proxies": int(m.sum()), "spearman_of_rhos": float(spearmanr(a[m], b[m]).correlation),
                      "kendall_of_rhos": float(kendalltau(a[m], b[m]).correlation), "pearson_of_rhos": float(np.corrcoef(a[m], b[m])[0, 1]),
                      "same_sign": int((np.sign(a[m]) == np.sign(b[m])).sum()),
                      "top3_ref": ",".join(df.loc[a[m].nlargest(3).index, "proxy"]), "top3_other": ",".join(df.loc[b[m].nlargest(3).index, "proxy"])})
    agree = pd.DataFrame(agree)
    agree.to_csv(out / "rank_agreement.csv", index=False)
    n50 = None
    if n50_csv and Path(n50_csv).exists():
        t50 = pd.read_csv(n50_csv).set_index("proxy")
        t = tabs[ref]
        rows = []
        for p in proxies:
            if p in t50.index and p in t.index:
                r50, rN = t50.loc[p], t.loc[p]
                rows.append({"proxy": p, "n50_spearman": float(r50.spearman), "n50_ci_lo": float(r50.ci_lo), "n50_ci_hi": float(r50.ci_hi),
                             "n50_halfwidth": float((r50.ci_hi - r50.ci_lo) / 2), f"n{int(rN.n)}_spearman": float(rN.spearman), f"n{int(rN.n)}_ci_lo": float(rN.ci_lo),
                             f"n{int(rN.n)}_ci_hi": float(rN.ci_hi), f"n{int(rN.n)}_halfwidth": float((rN.ci_hi - rN.ci_lo) / 2),
                             "n50_inside_large_ci": bool(rN.ci_lo <= r50.spearman <= rN.ci_hi), "large_inside_n50_ci": bool(r50.ci_lo <= rN.spearman <= r50.ci_hi)})
        n50 = pd.DataFrame(rows)
        n50.to_csv(out / "n50_vs_n300.csv", index=False)
    # markdown
    L = [f"# Cross-setting comparison — {', '.join(labels)}", "",
         "Spearman of the proxy (mean over 3 init seeds) with −val MAE (seed 0) on each setting, 95 % bootstrap CI, partial ρ | log params. "
         "All roots use the same genotype space and schedule; only the data, the number of sensors and the adjacency differ.", ""]
    L.append("| setting | root | N | seed-noise ceiling (s0-s1 / s0-s2 / s1-s2) | within / across std |")
    L.append("|---|---|---|---|---|")
    for r in roots:
        c = summs[r.label].get("seed_ceiling", {})
        L.append(f"| {r.label} | `{r.dir}` | {summs[r.label]['n_rows']} | {fmt(c.get('spearman_s0_s1'))} / {fmt(c.get('spearman_s0_s2'))} / {fmt(c.get('spearman_s1_s2'))} | "
                 f"{c.get('within_arch_std_mean', float('nan')):.4f} / {c.get('across_arch_std', float('nan')):.4f} |")
    L += ["", "| proxy | " + " | ".join(f"{lab} ρ (95 % CI) | partial" for lab in labels) + " |", "|---|" + "---|---|" * len(labels)]
    order = df[f"{ref} spearman"].fillna(-9).sort_values(ascending=False).index
    for i in order:
        r = df.loc[i]
        name = f"`{r.proxy}` (complexity baseline)" if r.proxy in ("params", "flops") else f"`{r.proxy}`"
        cells = []
        for lab in labels:
            if f"{lab} spearman" in r and np.isfinite(r[f"{lab} spearman"]):
                cells.append(f"{fmt(r[f'{lab} spearman'])} ({fmt(r[f'{lab} ci_lo'])}, {fmt(r[f'{lab} ci_hi'])}) | {fmt(r[f'{lab} partial_params'])}")
            else:
                cells.append("— | —")
        L.append(f"| {name} | " + " | ".join(cells) + " |")
    L += ["", f"## Does the proxy *ordering* transfer? (reference: {ref})", "",
          "| pair | proxies | Spearman of the ρ vectors | Kendall | Pearson | same sign | top 3 (reference) | top 3 (other) |", "|---|---|---|---|---|---|---|---|"]
    for _, a in agree.iterrows():
        L.append(f"| {a.pair} | {a.n_proxies} | {fmt(a.spearman_of_rhos)} | {fmt(a.kendall_of_rhos)} | {fmt(a.pearson_of_rhos)} | {a.same_sign}/{a.n_proxies} | {a.top3_ref} | {a.top3_other} |")
    if n50 is not None:
        big = [c for c in n50.columns if c.endswith("_spearman") and not c.startswith("n50")][0].split("_")[0]
        L += ["", f"## {ref}: N = 50 (Pilot 1) vs N = {big[1:]} (Pilot 2)", "",
              f"| proxy | ρ at N = 50 (95 % CI) | half-width | ρ at N = {big[1:]} (95 % CI) | half-width | N = {big[1:]} estimate inside the N = 50 CI? | shift |", "|---|---|---|---|---|---|---|"]
        for _, r in n50.sort_values(f"{big}_spearman", ascending=False).iterrows():
            L.append(f"| `{r.proxy}` | {fmt(r.n50_spearman)} ({fmt(r.n50_ci_lo)}, {fmt(r.n50_ci_hi)}) | ±{r.n50_halfwidth:.2f} | {fmt(r[f'{big}_spearman'])} ({fmt(r[f'{big}_ci_lo'])}, {fmt(r[f'{big}_ci_hi'])}) | ±{r[f'{big}_halfwidth']:.2f} | {'yes' if r.large_inside_n50_ci else 'no'} | {r[f'{big}_spearman'] - r.n50_spearman:+.2f} |")
        L.append("")
        L.append(f"Mean CI half-width: ±{n50.n50_halfwidth.mean():.2f} at N = 50 vs ±{n50[f'{big}_halfwidth'].mean():.2f} at N = {big[1:]} (Fisher-z expectation ±{1.06 * 1.96 / math.sqrt(47):.2f} and ±{1.06 * 1.96 / math.sqrt(int(big[1:]) - 3):.2f}). "
                 f"The N = {big[1:]} estimate lies inside the N = 50 interval for {int(n50.large_inside_n50_ci.sum())}/{len(n50)} proxies (the N = 50 point estimate lies inside the narrower N = {big[1:]} interval for {int(n50.n50_inside_large_ci.sum())}/{len(n50)} — the expected direction of disagreement: the small-sample point estimates scatter by ±0.25 around values now known to ±0.11). "
                 "The first 50 architectures are a subset of the larger set, so the two estimates are not independent.")
    (out / "cross_dataset.md").write_text("\n".join(L) + "\n")
    meta = {"roots": [str(r.dir) for r in roots], "labels": labels, "n50_csv": str(n50_csv) if n50_csv else None,
            "written": _now(), "files": sorted(p.name for p in out.iterdir())}
    (out / "compare_summary.json").write_text(json.dumps(meta, indent=2))
    return meta


def _now():
    import datetime as _dt
    return _dt.datetime.now().isoformat(timespec="seconds")


def main():
    ap = argparse.ArgumentParser()
    Root.add_args(ap)
    ap.add_argument("--compare", nargs="+", default=None, help="Phase 5: roots to compare (first = reference); writes --out/cross_dataset.*")
    ap.add_argument("--n50", default=None, help="with --compare: the N = 50 table_A.csv of the reference root (results/tables_n50/table_A.csv)")
    ap.add_argument("--archs", default=None, help="default: <root>/archs.jsonl")
    ap.add_argument("--proxies", default=None, help="default: <root>/proxies/v1")
    ap.add_argument("--spatial", default=None, help="default: <root>/proxies/spatial_v2")
    ap.add_argument("--train", default=None, help="default: <root>/train")
    ap.add_argument("--out", default=None, help="default: <root>/tables")
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--subgroup-ci", action="store_true", help="bootstrap CIs for every Table A subgroup column too")
    args = ap.parse_args()
    if args.compare:
        roots = [Root(r) for r in args.compare]
        meta = compare_roots(roots, Path(args.out or "results/tables_pilot2"), args.n50)
        print(json.dumps(meta, indent=2))
        return
    root = Root.from_args(args)
    args.archs, args.proxies, args.spatial = args.archs or root.archs_jsonl, args.proxies or root.proxies_v1, args.spatial or root.spatial_v2
    args.train, args.out = args.train or root.train, args.out or root.tables
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
    tA = table_A(df, PROXIES_PRIMARY, subgroup_ci=args.subgroup_ci, n_boot=args.n_boot)
    tA.to_csv(out / "table_A.csv", index=False)
    (out / "table_A.md").write_text(md_table_A(tA, ceiling, "Table A — Experiment A (13 proxies, all-parameter variants as primary)"))
    tA2 = table_A(df, PROXIES_NASLIB + [e for e in EXTRA if e in df], n_boot=args.n_boot)
    tA2.to_csv(out / "table_A_naslib.csv", index=False)
    (out / "table_A_naslib.md").write_text(md_table_A(tA2, {}, "Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score"))
    bases = [c[len("S_spatial_"):] for c in df.columns if c.startswith("S_spatial_")]
    det = detection_table(df, bases)
    det.to_csv(out / "table_B_detection.csv", index=False)
    for base in bases:
        tB = table_B(df, base)
        tB.to_csv(out / f"table_B_{base}.csv", index=False)
        (out / f"table_B_{base}.md").write_text(md_table_B(tB, det, base, int(df.has_graph.sum()), int(df.uses_A.sum())))
    if "nwot" in bases:
        (out / "table_B.md").write_text((out / "table_B_nwot.md").read_text())
        (out / "table_B.csv").write_text((out / "table_B_nwot.csv").read_text())
    # Phase 9: robustness tables
    tP = table_A_partial(df, PROXIES_PRIMARY)
    tP.to_csv(out / "table_A_partial.csv", index=False)
    (out / "table_A_partial.md").write_text(md_table_A_partial(tP))
    curve = subsample_curve(df, ["zico", "l2_norm_all", "params", "grasp_all", "zen", "nwot", "snip_all"])
    curve.to_csv(out / "subsample_curve.csv", index=False)
    (out / "ci_summary.md").write_text(md_ci_summary(tA, curve, ceiling, len(df), args.n_boot))
    json.dump({"root": str(root.dir), "dataset": root.dataset, "horizon": root.horizon, "n_rows": int(len(df)), "n_done": n_done,
               "seed_ceiling": ceiling, "bases": bases, "subgroup_ci": args.subgroup_ci, "seconds": round(time.time() - t0, 1)},
              open(out / "analyze_summary.json", "w"), indent=2)
    print(tA[["proxy", "n", "spearman", "ci_lo", "ci_hi", "kendall", "partial_params"]].to_string(index=False, float_format=lambda v: f"{v:+.2f}"))
    print(f"done in {time.time() - t0:.1f}s -> {out}")


if __name__ == "__main__":
    main()
