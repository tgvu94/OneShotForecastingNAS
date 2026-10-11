# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=48) | has graph (n=102) | uses A (n=84) | gcn (incl. mixed) (n=64) | diffusion (incl. mixed) (n=66) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `grasp` | 150 | 0.23 (0.05, 0.40) | — | 0.15 | 0.00459 | 0.21 | 0.691 | 0.03 | 0.43 | 0.53 | 0.49 | 0.60 |
| `tfas_zico_cl` | 150 | 0.23 (0.07, 0.38) | — | 0.16 | 0.00489 | 0.27 | 0.004 | 0.24 | 0.21 | 0.24 | 0.22 | 0.28 |
| `l2_norm` | 150 | 0.19 (0.02, 0.35) | — | 0.13 | 0.0208 | 0.25 | 0.001 | 0.09 | 0.21 | 0.27 | 0.26 | 0.29 |
| `synflow` | 150 | -0.02 (-0.20, 0.16) | — | -0.01 | 0.786 | -0.02 | 0.028 | 0.24 | -0.15 | -0.28 | -0.38 | -0.21 |
| `snip` | 150 | -0.36 (-0.50, -0.20) | — | -0.25 | 4.96e-06 | -0.44 | 0.066 | -0.21 | -0.42 | -0.31 | -0.21 | -0.38 |
| `grad_norm` | 150 | -0.39 (-0.53, -0.24) | — | -0.26 | 6.77e-07 | -0.46 | 0.062 | -0.20 | -0.47 | -0.37 | -0.27 | -0.44 |
| `plain` | 150 | -0.47 (-0.59, -0.31) | — | -0.32 | 1.9e-09 | -0.47 | 0.541 | -0.13 | -0.59 | -0.56 | -0.52 | -0.63 |
