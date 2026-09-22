# Table A — Experiment A (13 proxies, all-parameter variants as primary)

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=16) | has graph (n=34) | uses A (n=28) | gcn (incl. mixed) (n=19) | diffusion (incl. mixed) (n=25) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| seed-noise ceiling (val MAE seed 0 vs 1 / 0 vs 2 / 1 vs 2) | 5 | 0.60 / 0.90 / 0.70 | 1.00 | — | — | — | within-arch std 0.0021 vs across-arch 0.0129 | — | — | — | — | — |
| `grasp_all` | 50 | 0.43 (0.15, 0.64) | +0.72 | 0.28 | 0.00161 | 0.42 | 0.240 | 0.58 | 0.39 | 0.33 | 0.39 | 0.38 |
| `nwot` | 50 | 0.05 (-0.25, 0.34) | +0.09 | 0.04 | 0.708 | 0.04 | 0.001 | -0.23 | 0.09 | 0.05 | 0.22 | 0.12 |
| `flops` (complexity baseline) | 50 | 0.02 (-0.26, 0.31) | +0.03 | 0.02 | 0.885 | — | 0.000 | -0.29 | -0.01 | -0.04 | 0.13 | 0.05 |
| `l2_norm_all` | 50 | 0.00 (-0.30, 0.29) | +0.00 | 0.01 | 0.999 | 0.07 | 0.001 | -0.29 | 0.08 | 0.03 | 0.26 | 0.01 |
| `params` (complexity baseline) | 50 | -0.04 (-0.32, 0.26) | -0.06 | -0.02 | 0.795 | — | 0.000 | -0.23 | 0.07 | 0.09 | 0.23 | 0.09 |
| `jacov` | 50 | -0.05 (-0.31, 0.23) | -0.08 | -0.03 | 0.751 | -0.05 | 0.359 | 0.23 | -0.02 | 0.09 | 0.17 | 0.10 |
| `zen` | 50 | -0.05 (-0.36, 0.26) | -0.08 | -0.03 | 0.742 | -0.02 | 0.001 | -0.21 | 0.07 | 0.04 | 0.13 | 0.03 |
| `zico` | 50 | -0.09 (-0.36, 0.20) | -0.15 | -0.06 | 0.543 | -0.07 | 0.006 | -0.11 | -0.01 | -0.05 | 0.09 | -0.10 |
| `synflow_all` | 50 | -0.23 (-0.48, 0.05) | -0.38 | -0.17 | 0.107 | -0.20 | 0.036 | -0.29 | -0.23 | -0.05 | 0.05 | 0.00 |
| `snip_all` | 50 | -0.39 (-0.62, -0.08) | -0.65 | -0.26 | 0.00523 | -0.39 | 0.054 | -0.56 | -0.32 | -0.26 | -0.28 | -0.30 |
| `grad_norm_all` | 50 | -0.44 (-0.66, -0.15) | -0.74 | -0.29 | 0.00134 | -0.44 | 0.076 | -0.63 | -0.37 | -0.29 | -0.29 | -0.33 |
| `plain_all` | 50 | -0.45 (-0.65, -0.20) | -0.75 | -0.29 | 0.000964 | -0.46 | 0.249 | -0.48 | -0.43 | -0.33 | -0.16 | -0.37 |
| `fisher` | 50 | -0.55 (-0.72, -0.28) | -0.91 | -0.35 | 3.84e-05 | -0.55 | 0.140 | -0.63 | -0.50 | -0.46 | -0.43 | -0.52 |

ρ/ceiling = Spearman divided by the seed-noise ceiling 0.60 (seed-0 vs seed-1 val MAE on the 5 repeated archs): the fraction of the achievable rank agreement a proxy reaches.
