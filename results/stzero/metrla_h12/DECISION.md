# DECISION — probe on METRLA-12 (PEMS/metrla/metrla_12)

**Verdict: graph does not matter at METRLA-12.**

Rule: graph matters if (A) the median val MAE of the uses-A archs is below the graph-blind median by more than 3 x the within-arch seed std *and* Mann-Whitney p < 0.05, *or* (B) |Spearman(S_spatial(nwot), -val MAE)| > 0.28 within the uses-A archs.

| Quantity | Value |
|---|---|
| uses-A archs (n) | 28 |
| graph-blind archs (n) | 16 |
| median val MAE, uses-A | 0.2439 |
| median val MAE, graph-blind | 0.2425 |
| gap (blind - uses-A) | -0.0013 |
| 3 x within-arch seed std | 0.0064 (std 0.0021, 5 archs x 3 seeds) |
| Mann-Whitney U, H1 uses-A < blind, p | 0.353 |
| rule A | False |
| Spearman(S_spatial(nwot), -val MAE), uses-A only | -0.011 |
| rule B (|rho| > 0.28) | False |
| seed-noise ceiling (Spearman seed 0 vs 1) | 0.60 |
| seed-0 runs done | 50/50 |

Files: `results/stzero/metrla_h12/tables/table_A.md`, `results/stzero/metrla_h12/tables/table_B.md`, `results/stzero/metrla_h12/figs/`.  Written by `pilot.check --check probe --root results/stzero/metrla_h12`.
