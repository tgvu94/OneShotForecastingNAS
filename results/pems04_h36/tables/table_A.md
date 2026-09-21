# Table A — Experiment A (13 proxies, all-parameter variants as primary)

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=16) | has graph (n=34) | uses A (n=28) | gcn (incl. mixed) (n=19) | diffusion (incl. mixed) (n=25) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| seed-noise ceiling (val MAE seed 0 vs 1 / 0 vs 2 / 1 vs 2) | 5 | 0.20 / 0.60 / 0.60 | 1.00 | — | — | — | within-arch std 0.0013 vs across-arch 0.0064 | — | — | — | — | — |
| `zico` | 50 | 0.71 (0.52, 0.82) | +3.55 | 0.51 | 7.66e-09 | 0.56 | 0.006 | 0.85 | 0.62 | 0.53 | 0.52 | 0.56 |
| `l2_norm_all` | 50 | 0.59 (0.34, 0.76) | +2.97 | 0.42 | 5.64e-06 | 0.37 | 0.001 | 0.76 | 0.57 | 0.46 | 0.48 | 0.51 |
| `params` (complexity baseline) | 50 | 0.51 (0.27, 0.68) | +2.54 | 0.34 | 0.00017 | — | 0.000 | 0.49 | 0.48 | 0.43 | 0.44 | 0.43 |
| `grasp_all` | 50 | 0.30 (0.02, 0.56) | +1.52 | 0.22 | 0.0313 | 0.47 | 0.185 | 0.33 | 0.30 | 0.33 | 0.36 | 0.34 |
| `zen` | 50 | 0.30 (0.01, 0.54) | +1.51 | 0.22 | 0.033 | -0.29 | 0.001 | 0.14 | 0.32 | 0.27 | 0.34 | 0.23 |
| `nwot` | 50 | 0.03 (-0.27, 0.31) | +0.13 | 0.01 | 0.857 | -0.22 | 0.001 | 0.28 | 0.03 | 0.02 | 0.18 | -0.03 |
| `flops` (complexity baseline) | 50 | -0.03 (-0.34, 0.25) | -0.17 | -0.04 | 0.814 | — | 0.000 | 0.41 | -0.13 | -0.18 | 0.08 | -0.24 |
| `synflow_all` | 50 | -0.10 (-0.42, 0.20) | -0.52 | -0.08 | 0.472 | -0.11 | 0.021 | 0.26 | -0.32 | -0.22 | 0.06 | -0.32 |
| `jacov` | 50 | -0.15 (-0.40, 0.15) | -0.73 | -0.11 | 0.31 | -0.24 | 0.198 | -0.11 | -0.38 | -0.30 | -0.32 | -0.22 |
| `plain_all` | 50 | -0.15 (-0.42, 0.15) | -0.76 | -0.12 | 0.289 | -0.28 | 0.275 | -0.09 | -0.25 | -0.25 | -0.10 | -0.27 |
| `fisher` | 50 | -0.26 (-0.53, 0.03) | -1.31 | -0.20 | 0.0652 | -0.46 | 0.152 | -0.27 | -0.30 | -0.32 | -0.28 | -0.34 |
| `grad_norm_all` | 50 | -0.28 (-0.54, 0.01) | -1.39 | -0.21 | 0.0513 | -0.51 | 0.058 | -0.27 | -0.33 | -0.33 | -0.31 | -0.32 |
| `snip_all` | 50 | -0.29 (-0.55, -0.01) | -1.45 | -0.22 | 0.0409 | -0.52 | 0.059 | -0.32 | -0.32 | -0.31 | -0.29 | -0.33 |

ρ/ceiling = Spearman divided by the seed-noise ceiling 0.20 (seed-0 vs seed-1 val MAE on the 5 repeated archs): the fraction of the achievable rank agreement a proxy reaches.
