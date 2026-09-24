"""Phase 8 figures from <root>/tables/joined.csv (static PNGs, matplotlib).   python -m pilot.plots --root results

fig1_proxy_vs_mae_grid.png  : 13 scatter panels, proxy vs val MAE, hue = group (graph-blind / control / uses A), marker = graph family
fig2_spearman_by_family.png : grouped bars of Spearman(proxy, -val MAE) per proxy for all / graph-blind / has-graph, 95% bootstrap whiskers
fig3_spatial_vs_naswot.png  : nwot vs val MAE and S_spatial(nwot) vs val MAE;  fig3b: the same for zico

Palette: the dataviz reference instance, first three categorical slots (validated all-pairs): blue #2a78d6, orange #eb6834,
aqua #1baf7a on the light surface #fcfcfb; ink #0b0b0b / #52514e / #898781; gridline #e1e0d9.  Text never wears series colour.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

from pilot.paths import Root  # noqa: E402

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
GROUP_COLOR = {"graph-blind": "#2a78d6", "uses A": "#eb6834", "control": "#1baf7a"}
FAMILY_MARKER = {"none": "o", "identity-only": "v", "adaptive-only": "D", "gcn": "o", "diffusion": "^", "mixed": "s"}
PROXIES = ["nwot", "zico", "synflow_all", "snip_all", "grad_norm_all", "grasp_all", "plain_all", "fisher", "jacov", "zen",
           "l2_norm_all", "params", "flops"]
LOGX = {"synflow_all", "params", "flops", "fisher", "l2_norm_all"}

plt.rcParams.update({"font.family": "sans-serif", "font.size": 9, "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.titlecolor": INK, "figure.facecolor": SURFACE,
                     "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "legend.frameon": False})


def rho_ci(x, y, n_boot=2000, seed=0):
    x, y = np.asarray(x, float), -np.asarray(y, float)
    rho = spearmanr(x, y).correlation
    rng = np.random.default_rng(seed)
    b = []
    for _ in range(n_boot):
        i = rng.integers(0, len(x), len(x))
        if np.std(x[i]) > 0:
            b.append(spearmanr(x[i], y[i]).correlation)
    lo, hi = np.nanpercentile(b, [2.5, 97.5])
    return rho, lo, hi


def scatter(ax, df, xcol, ycol="val_mae", logx=False):
    for fam, sub in df.groupby("graph_family"):
        grp = sub.group3.iloc[0]
        ax.scatter(sub[xcol], sub[ycol], s=34, marker=FAMILY_MARKER[fam], c=GROUP_COLOR[grp], edgecolors=SURFACE, linewidths=1.2,
                   alpha=0.95, zorder=3)
    if logx:
        ax.set_xscale("log")
        ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax.xaxis.set_major_locator(matplotlib.ticker.LogLocator(numticks=4))
    ax.tick_params(length=2)


def legend_handles():
    h = [Line2D([], [], marker="o", ls="", color=GROUP_COLOR["graph-blind"], markeredgecolor=SURFACE, ms=7, label="graph-blind (none)"),
         Line2D([], [], marker="v", ls="", color=GROUP_COLOR["control"], markeredgecolor=SURFACE, ms=7, label="control: identity-only"),
         Line2D([], [], marker="D", ls="", color=GROUP_COLOR["control"], markeredgecolor=SURFACE, ms=6, label="control: adaptive-only"),
         Line2D([], [], marker="o", ls="", color=GROUP_COLOR["uses A"], markeredgecolor=SURFACE, ms=7, label="uses A: gcn"),
         Line2D([], [], marker="^", ls="", color=GROUP_COLOR["uses A"], markeredgecolor=SURFACE, ms=7, label="uses A: diffusion"),
         Line2D([], [], marker="s", ls="", color=GROUP_COLOR["uses A"], markeredgecolor=SURFACE, ms=7, label="uses A: mixed")]
    return h


def fig1(df, out, label="PEMS04-12"):
    fig, axes = plt.subplots(3, 5, figsize=(15, 9.6))
    axes = axes.ravel()
    for k, p in enumerate(PROXIES):
        ax = axes[k]
        scatter(ax, df, p, logx=p in LOGX)
        rho, lo, hi = rho_ci(df[p], df.val_mae)
        ax.set_title(f"{p}\nρ = {rho:+.2f}  [{lo:+.2f}, {hi:+.2f}]", fontsize=8.5, loc="left")
        ax.set_xlabel(p + (" (log)" if p in LOGX else ""), fontsize=8)
        if k % 5 == 0:
            ax.set_ylabel("val MAE (seed 0)")
    for ax in axes[len(PROXIES):]:
        ax.axis("off")
    axes[len(PROXIES)].legend(handles=legend_handles(), loc="center left", fontsize=9, title="architecture group", title_fontsize=9)
    fig.suptitle(f"Fig. 1 — Zero-cost proxies vs. 20-epoch val MAE on {label}, N = {len(df)} random DARTS-TS(+graph) architectures. "
                 "ρ = Spearman with −val MAE (positive = useful), 95% bootstrap CI.", fontsize=10, x=0.01, ha="left", color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out / "fig1_proxy_vs_mae_grid.png", dpi=160)
    plt.close(fig)


def fig2(df, out):
    groups = [("all (n=%d)" % len(df), df, "#898781"), ("graph-blind (n=%d)" % (~df.has_graph).sum(), df[~df.has_graph], GROUP_COLOR["graph-blind"]),
              ("has graph (n=%d)" % df.has_graph.sum(), df[df.has_graph], GROUP_COLOR["uses A"])]
    fig, ax = plt.subplots(figsize=(13, 4.8))
    w = 0.26
    xs = np.arange(len(PROXIES))
    for gi, (lab, sub, col) in enumerate(groups):
        vals = [rho_ci(sub[p], sub.val_mae) for p in PROXIES]
        r = [v[0] for v in vals]
        err = [[v[0] - v[1] for v in vals], [v[2] - v[0] for v in vals]]
        ax.bar(xs + (gi - 1) * w, r, width=w - 0.03, color=col, edgecolor=SURFACE, linewidth=1, label=lab, zorder=3)
        ax.errorbar(xs + (gi - 1) * w, r, yerr=err, fmt="none", ecolor=INK2, elinewidth=0.9, capsize=2, zorder=4)
    ax.axhline(0, color="#c3c2b7", lw=1, zorder=2)
    ax.axhline(0.737, color=MUTED, lw=0.9, ls="--", zorder=2)
    ax.text(len(PROXIES) - 0.5, 0.71, "LENAS naswot reference 0.737 (its space)", ha="right", va="top", fontsize=8, color=INK2)
    ax.set_xticks(xs)
    ax.set_xticklabels(PROXIES, rotation=30, ha="right")
    ax.set_ylabel("Spearman ρ with −val MAE")
    ax.set_ylim(-1, 1)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("Fig. 2 — Spearman per proxy by architecture group (whiskers: 95% bootstrap CI)", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(out / "fig2_spearman_by_family.png", dpi=160)
    plt.close(fig)


def fig3(df, out, base="nwot", name="fig3_spatial_vs_naswot.png"):
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    scatter(axes[0], df, base)
    rho, lo, hi = rho_ci(df[base], df.val_mae)
    axes[0].set_title(f"{base} under the true A\nρ = {rho:+.2f}  [{lo:+.2f}, {hi:+.2f}]", loc="left", fontsize=9)
    axes[0].set_xlabel(f"{base} (mean over 3 init seeds)")
    axes[0].set_ylabel("val MAE (seed 0)")
    col = f"S_spatial_{base}"
    scatter(axes[1], df, col)
    axes[1].set_xscale("symlog", linthresh=max(df.loc[df.uses_A, col].min() * 0.5, 1e-12))
    sens = df[df.uses_A]
    rho_s, lo_s, hi_s = rho_ci(sens[col], sens.val_mae)
    axes[1].set_title(f"S_spatial({base}) = |score(A) − mean score(π(A))|\nρ on the {len(sens)} uses-A archs = {rho_s:+.2f}  [{lo_s:+.2f}, {hi_s:+.2f}]", loc="left", fontsize=9)
    axes[1].set_xlabel(f"S_spatial({base}), symlog (controls sit at exactly 0)")
    fig.legend(handles=legend_handles(), loc="lower center", fontsize=8, ncol=6, bbox_to_anchor=(0.5, 0.0))
    fig.suptitle(f"Fig. 3 — Experiment B with base {base}: the proxy itself (left) and its adjacency sensitivity (right) vs. val MAE", fontsize=10, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.07, 1, 0.94))
    fig.savefig(out / name, dpi=160)
    plt.close(fig)


SERIES_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#898781"]   # the three validated categorical slots + the muted ink


def fig_ci_bars(panels, out, name, title, proxies=PROXIES):
    """Grouped bars of Spearman ρ with 95 % CI whiskers; one bar per (proxy, panel).  panels = [(label, table_A DataFrame)]."""
    fig, ax = plt.subplots(figsize=(13, 4.8))
    k = len(panels)
    w = 0.8 / k
    xs = np.arange(len(proxies))
    for gi, (lab, t) in enumerate(panels):
        t = t.set_index("proxy") if "proxy" in t.columns else t
        r = np.array([t.loc[p, "spearman"] if p in t.index else np.nan for p in proxies], float)
        lo = np.array([t.loc[p, "ci_lo"] if p in t.index else np.nan for p in proxies], float)
        hi = np.array([t.loc[p, "ci_hi"] if p in t.index else np.nan for p in proxies], float)
        pos = xs + (gi - (k - 1) / 2) * w
        ax.bar(pos, np.nan_to_num(r), width=w - 0.03, color=SERIES_COLORS[gi % len(SERIES_COLORS)], edgecolor=SURFACE, linewidth=1, label=lab, zorder=3)
        ax.errorbar(pos, r, yerr=[r - lo, hi - r], fmt="none", ecolor=INK2, elinewidth=0.9, capsize=2, zorder=4)
    ax.axhline(0, color="#c3c2b7", lw=1, zorder=2)
    ax.set_xticks(xs)
    ax.set_xticklabels(proxies, rotation=30, ha="right")
    ax.set_ylabel("Spearman ρ with −val MAE")
    ax.set_ylim(-1, 1)
    ax.legend(loc="upper right", fontsize=9, ncol=min(k, 4))
    ax.set_title(title, loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(out / name, dpi=160)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    Root.add_args(ap)
    ap.add_argument("--tables", default=None, help="default: <root>/tables")
    ap.add_argument("--out", default=None, help="default: <root>/figs")
    ap.add_argument("--compare", nargs="+", default=None, help="Phase 5: roots (first = reference) -> fig5_cross_dataset.png in --out")
    ap.add_argument("--n50", default=None, help="with --compare: N = 50 table_A.csv of the reference -> fig4_n50_vs_n300.png")
    args = ap.parse_args()
    if args.compare:
        roots = [Root(r) for r in args.compare]
        out = Path(args.out or "results/figs_pilot2")
        out.mkdir(parents=True, exist_ok=True)
        panels = [(f"{r.label} (N = {len(pd.read_csv(r.tables / 'joined.csv'))})", pd.read_csv(r.tables / "table_A.csv")) for r in roots]
        fig_ci_bars(panels, out, "fig5_cross_dataset.png",
                    "Fig. 5 — Spearman per proxy on every setting (whiskers: 95 % bootstrap CI; same genotype space and schedule everywhere)")
        if args.n50 and Path(args.n50).exists():
            ref = roots[0]
            fig_ci_bars([(f"{ref.label}, N = 50 (Pilot 1)", pd.read_csv(args.n50)), panels[0]], out, "fig4_n50_vs_n300.png",
                        f"Fig. 4 — {ref.label}: the same 13 proxies at N = 50 and at N = {len(pd.read_csv(ref.tables / 'joined.csv'))} (whiskers: 95 % bootstrap CI)")
        print("figures ->", sorted(p.name for p in out.glob("*.png")))
        return
    root = Root.from_args(args)
    df = pd.read_csv(Path(args.tables or root.tables) / "joined.csv")
    out = Path(args.out or root.figs)
    out.mkdir(parents=True, exist_ok=True)
    fig1(df, out, root.label)
    fig2(df, out)
    fig3(df, out, "nwot", "fig3_spatial_vs_naswot.png")
    if "S_spatial_zico" in df:
        fig3(df, out, "zico", "fig3b_spatial_vs_zico.png")
    print("figures ->", sorted(p.name for p in out.glob("*.png")))


if __name__ == "__main__":
    main()
