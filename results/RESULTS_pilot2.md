# Pilot 2 results — plain-English reading (Phase 6, 2026-09-24)

**What was done.** Pilot 1's benchmark was taken to paper scale on the same search space (DARTS-TS Seq/Flat operators plus a
graph cell with GCN, diffusion, adaptive-adjacency and identity operators) and the same fixed schedule (20 epochs, batch 32,
seed 0; three seeds on five architectures). Three questions, in order. (1) *Does the road graph carry any accuracy signal on a
setting we can afford?* The frozen 50 were retrained at PEMS04 horizon 36 (`results/pems04_h36/`) and on METR-LA horizon 12
(`results/metrla_h12/`, 207 sensors, DCRNN adjacency); each root has its `DECISION.md`. (2) *Do the N = 50 correlations survive
N = 300?* 250 more architectures were sampled (seed 2027) and trained on PEMS04 horizon 12, so `results/` now holds 300; the
Pilot 1 tables are preserved in `results/tables_n50/` and `results/figs_n50/`. (3) *Do they transfer to a second road graph?*
150 architectures (seed 2028) were trained on PEMS08 (`results/pems08_h12/`, 170 sensors). Every architecture has all 19
proxy scores × 3 init seeds and the four spatial-sensitivity scores under 8 rewirings; ≈ 81 GPU-hours in total.
Tables: `results/tables/table_A.md`, `table_A_partial.md`, `table_A_naslib.md`, `table_B.md` (`table_B_zico.md`,
`table_B_nwot.md`, `table_B_grad_norm_all.md`, `table_B_snip_all.md`, `table_B_detection.csv`), `ci_summary.md`, `joined.csv`;
the same set under `results/pems08_h12/tables/`; the cross-setting comparison `results/tables_pilot2/cross_dataset.md`
(`cross_dataset.csv`, `rank_agreement.csv`, `n50_vs_n300.csv`). Figures: `results/figs/fig1_proxy_vs_mae_grid.png`,
`fig2_spearman_by_family.png`, `fig3_spatial_vs_naswot.png`, `fig3b_spatial_vs_zico.png` (same four under
`results/pems08_h12/figs/`), `results/figs_pilot2/fig4_n50_vs_n300.png`, `results/figs_pilot2/fig5_cross_dataset.png`.

**The graph does not matter anywhere we tested.** At horizon 36 the graph-using architectures are no better than the
graph-blind ones (median val MAE 0.2079 vs 0.2071, Mann–Whitney p = 0.69); on METR-LA, whose graph has six times PEMS04's
edges per sensor, the same (0.2439 vs 0.2425, p = 0.35); and at N = 300 on PEMS04 horizon 12 the spatial sensitivity score has no
correlation with accuracy on the 168 architectures that use the adjacency (−0.08), while detecting graph use perfectly (167/168
beyond 3σ of the rewiring band, 168/168 prefer the true graph). PEMS08 is the one setting with a hint in the other direction
(median 0.1740 vs 0.1754, p = 0.06), below the decision rule. So the plan's Section 4 branch was taken: the scale-up ran on
PEMS04 horizon 12, the learned spatial estimator (Route B) is deprioritized as a *spatial* route, and the size-controlled ZiCo
direction is Pilot 3's line.

**The ground truth is well resolved at scale.** The 300 PEMS04 architectures span val MAE 0.168–0.213 (std 0.0033, eleven
times the seed noise of 0.0003; the same five architectures rank identically under different seeds, Spearman 0.90–1.00), and
the 150 PEMS08 ones 0.169–0.217 (std 0.0046; seed Spearman 1.00). All beat the naive last-value forecast by a wide margin.
Two settings are weaker: at horizon 36 two single-seed outliers push the five-architecture seed Spearman to 0.20 although the
noise-to-spread ratio (0.21) is ordinary, and on METR-LA 41 of 50 runs early-stopped under the PEMS04-tuned schedule and the
loss head explains most of the spread — those two verdicts rest on the medians and the spatial score, not on proxy rankings.

**Table A at N = 300 — ZiCo and the L2 norm survive size and family control on PEMS04.** ZiCo reaches Spearman 0.57 (95 % CI
0.48–0.65; 0.63 after partialling out parameter count), the L2 norm 0.50 (0.55 partial), and both keep an interval that excludes
zero inside every operator family (graph-blind 0.49 and 0.35; GCN 0.56 and 0.44; diffusion 0.61 and 0.52). Parameter count
itself falls to 0.19 (0.47 at N = 50), FLOPs give 0.31. The "collapse per family" that Deng et al. report is real here for
*other* proxies: naswot scores 0.34 overall but ≈ 0 inside every family — its correlation is the graph-vs-blind composition of
the sample — and the gradient-magnitude family (SNIP, grad-norm, Fisher, plain) points the wrong way in every subgroup, as it
did at N = 50. Intervals are now ±0.11 wide (±0.25 at N = 50); the N = 300 estimate lies inside the N = 50 interval for 11 of 13
proxies, the exceptions being parameter count and synflow, which N = 50 had over- and under-stated.

**The ordering does not transfer across datasets.** On PEMS08 (N = 150) ZiCo drops to 0.32 (0.15–0.46) and the L2 norm to
0.25, GraSP leads at 0.47, and the gradient family is strongly negative (−0.36 … −0.47); on METR-LA (N = 50) ZiCo is −0.09, the
L2 norm 0.00, GraSP 0.43, Fisher −0.55. Rank agreement of the 13-proxy ordering with PEMS04 horizon 12 is 0.73 for PEMS08,
0.82 for PEMS04 horizon 36 and 0.52 for METR-LA (`rank_agreement.csv`). The same search space and schedule, three road
graphs, three different "best proxies": whatever a zero-cost proxy measures at initialization on this space is dataset-dependent.

**What this decides for the three-year plan.** (1) Idea 1's paper-grade claim is the positive resource result — "ZiCo and the
L2 norm keep ρ ≈ 0.5–0.65 after size control, in every operator family, at N = 300 on PEMS04" — framed by the cross-dataset
table, which is the benchmark's second contribution. (2) Idea 2 Route A is closed as a ranking proxy on every tested setting;
`S_spatial` remains a training-free "uses the graph" filter. Route B, relabeled as an operator-vocabulary predictor rather than a
spatial proxy, has its N = 300 ground truth and a hard transfer test (METR-LA) waiting. (3) Pilot 3's first experiment is the
size-controlled ZiCo-style proxy, evaluated on both PEMS04 and PEMS08 against ZiCo and the L2 norm after partialling out log
parameters, with METR-LA as the failure case to explain.

**Caveats.** One search space and one schedule; PEMS08 at N = 150 has intervals of ±0.16, so its subgroup numbers are
tendencies; the two probe settings are N = 50; METR-LA's ground truth is early-stopped and head-dominated; the METR-LA
adjacency inherits DCRNN's distance threshold; proxies were scored at random initialization in train mode with the RNG fixed
before every forward. The "graph does not matter" result is a property of this space and schedule, not of traffic forecasting.

**Archive.** `$NAS_ROOT/backups/results-pilot2.tgz` and `~/scratch/backups/results-pilot2.tgz` (6.3G, sha1 5dcb05ba2fe2…), the whole `results/` tree with checkpoints, made at fork commit `3b42d35`.
