# Pilot results — plain-English reading (Phase 10, 2026-09-21)

**What was done.** Fifty random architectures were sampled from the DARTS-TS search space extended with a graph cell
(`results/FROZEN.md`): 16 use no graph operator, 6 use only operators that ignore the road graph (identity / adaptive
adjacency), and 28 use GCN or diffusion convolutions on the real PEMS04 road graph. Every architecture was trained once on
PEMS04 (12-step horizon, 20 epochs, fixed schedule) and five of them three times, to measure seed noise. Thirteen zero-cost
proxies were scored on one fixed batch with three initialisation seeds, and four of them were scored again under eight
degree-preserving rewirings of the road graph. Tables: `results/tables/table_A.md`, `results/tables/table_A_partial.md`,
`results/tables/table_A_naslib.md`, `results/tables/table_B.md` (`table_B_zico.md`, `table_B_nwot.md`,
`table_B_grad_norm_all.md`, `table_B_snip_all.md`, `table_B_detection.csv`), `results/tables/ci_summary.md`,
`results/tables/joined.csv`; figures `results/figs/fig1_proxy_vs_mae_grid.png`, `fig2_spearman_by_family.png`,
`fig3_spatial_vs_naswot.png`, `fig3b_spatial_vs_zico.png`.

**The ground truth is well resolved.** The 50 architectures span val MAE 0.169–0.179 (z-score units); the spread across
architectures (std 0.0021) is seven times the seed noise (0.0003), and the same architectures rank the same way under
different seeds (Spearman 0.90–1.00). Adding graph operators neither helps nor hurts at this schedule (mean val MAE 0.1728
with a graph cell vs 0.1733 without).

**Table A — which proxies rank this space?** Three do, in the useful direction: ZiCo (Spearman 0.65, 95 % CI 0.45–0.78),
the parameter L2 norm (0.63) and the parameter count itself (0.47). Both ZiCo and the L2 norm are strongly size-like, but keep
about half their signal after the parameter count is partialled out (0.50, 0.51; `table_A_partial.md`); GRASP over all
parameters is the one size-independent positive proxy (0.35, partial 0.41). Zen's 0.33 is entirely size. NASWOT, the proxy
LENAS used on its own spatio-temporal space (0.737 there), reaches only 0.17 here (CI includes 0). The gradient-magnitude
family — SNIP, grad-norm, Fisher, plain, and synflow — points the wrong way (−0.11 … −0.27), more so after size control
(−0.44): at random initialisation, larger gradients go with worse trained error on this space. The Conv/Linear-only
variants of the same measures agree with the all-parameter ones (`table_A_naslib.md`). Deng et al.'s "all proxies collapse"
finding on the graph-blind DARTS-TS space is therefore not reproduced on PEMS04 at N = 50 (ZiCo reaches 0.84 on the 16
graph-blind architectures), but every useful proxy gets weaker once graph operators are in the space.

**Table B — does sensitivity to the road graph help?** Two separate answers. *Detection works:* with the random-number state
fixed, every proxy is exactly unchanged on the 22 architectures that ignore the adjacency and shifts far outside the
rewiring band on the 28 that use it (NASWOT: all 28 beyond three standard deviations, median z = +20; grad-norm 25/28;
SNIP 22/28; ZiCo 9/28). The true road graph always gives a *higher* score than a rewired graph with the same degrees. So
`S_spatial` is a training-free test of whether an architecture uses spatial structure. *Ranking does not:* `S_spatial` has
no correlation with accuracy (−0.01 to +0.01, CI ±0.27), and adding it to the best base proxy lowers the composite from 0.65
to 0.44–0.47. This follows from the ground truth — on this space and schedule, using the graph changes nothing, so a
measure of "how much the graph is used" has nothing to predict. Nothing beats the 0.737 reference, which was measured on a
different space.

**Are these numbers trustworthy?** (`ci_summary.md`) With N = 50 the bootstrap intervals are ±0.16–0.30 wide. That is
enough to separate useful from useless proxies (five intervals exclude zero) and to show ZiCo is at least as good as the
parameter count, but not enough to place ZiCo relative to 0.737 (N ≈ 500 needed) or to support sub-group claims at n = 16–34.
ZiCo's estimate is stable from N = 20 upward; NASWOT's is indistinguishable from zero below N = 40. Test MAE as target gives
the same ordering; val MSE changes the gradient family's sign, which is noted. The adjacency matches the data's node order
(connected sensors correlate at 0.87 vs 0.77 for unconnected; `adj_sanity.json`). TFAS could not be included as a distinct
proxy: its score is ZiCo, and its time-frequency part is an input augmentation only its own backbones accept.

**What this decides for the three-year plan.** (1) Idea 1 (ST-Zero benchmark): the space, schedule and pipeline scale
without change; go to N = 300 (expected interval ±0.12) and add a second dataset before drawing family-level conclusions.
(2) Idea 2, Route A (adjacency-sensitivity proxy): the ranking signal is ≈ 0 at N = 50, below the < 0.4 threshold, so the
plan's rule points to Route B; the detection result is a usable by-product (a cheap filter for "does this architecture use
the graph"), not a ranking proxy. (3) The most promising direction for a spatio-temporal proxy on this evidence is a
size-controlled ZiCo-style gradient-consistency measure, not activation-pattern (NASWOT) or gradient-magnitude measures.

**Caveats.** One dataset, one horizon (12 steps), one schedule (20 epochs, no early stopping triggered), random-init
proxies in train mode (dropout noise ≈ 0.3 % on gradient proxies), 50 architectures, the graph cell as built here (one cell,
C = 32, residual ops). The "graph does not matter" result is a property of this setup, not of traffic forecasting.
