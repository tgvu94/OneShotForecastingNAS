# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=16) | has graph (n=34) | uses A (n=28) | gcn (incl. mixed) (n=19) | diffusion (incl. mixed) (n=25) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `tfas_zico_cl` | 50 | 0.61 (0.40, 0.76) | — | 0.43 | 2.56e-06 | 0.42 | 0.005 | 0.83 | 0.54 | 0.46 | 0.59 | 0.48 |
| `l2_norm` | 50 | 0.59 (0.38, 0.74) | — | 0.41 | 6.62e-06 | 0.39 | 0.001 | 0.67 | 0.58 | 0.54 | 0.61 | 0.54 |
| `grasp` | 50 | -0.09 (-0.39, 0.23) | — | -0.06 | 0.552 | -0.10 | 0.744 | -0.06 | -0.05 | 0.15 | 0.32 | 0.16 |
| `synflow` | 50 | -0.10 (-0.40, 0.19) | — | -0.08 | 0.493 | -0.21 | 0.021 | 0.27 | -0.34 | -0.23 | 0.01 | -0.21 |
| `plain` | 50 | -0.17 (-0.42, 0.10) | — | -0.11 | 0.245 | -0.27 | 0.576 | 0.09 | -0.27 | -0.28 | -0.08 | -0.28 |
| `snip` | 50 | -0.26 (-0.52, 0.04) | — | -0.17 | 0.0684 | -0.44 | 0.056 | -0.27 | -0.24 | -0.20 | -0.14 | -0.19 |
| `grad_norm` | 50 | -0.27 (-0.52, 0.02) | — | -0.17 | 0.0601 | -0.45 | 0.070 | -0.24 | -0.25 | -0.22 | -0.16 | -0.21 |
