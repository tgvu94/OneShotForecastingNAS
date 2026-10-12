# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=67) | has graph (n=83) | uses A (n=75) | gcn (incl. mixed) (n=56) | diffusion (incl. mixed) (n=63) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `tfas_zico_cl` | 150 | 0.50 (0.37, 0.62) | — | 0.35 | 7.44e-11 | 0.62 | 0.004 | 0.45 | 0.53 | 0.50 | 0.54 | 0.48 |
| `l2_norm` | 150 | 0.38 (0.23, 0.51) | — | 0.26 | 1.6e-06 | 0.46 | 0.001 | 0.29 | 0.47 | 0.43 | 0.48 | 0.39 |
| `synflow` | 150 | 0.20 (0.04, 0.35) | — | 0.14 | 0.0129 | 0.22 | 0.021 | 0.12 | -0.08 | -0.06 | 0.06 | -0.08 |
| `plain` | 150 | -0.11 (-0.27, 0.05) | — | -0.07 | 0.182 | -0.12 | 0.462 | 0.09 | -0.29 | -0.30 | -0.19 | -0.25 |
| `grasp` | 150 | -0.16 (-0.31, 0.00) | — | -0.11 | 0.0535 | -0.18 | 0.761 | 0.03 | 0.05 | 0.13 | 0.15 | 0.12 |
| `grad_norm` | 150 | -0.17 (-0.32, -0.01) | — | -0.11 | 0.038 | -0.23 | 0.060 | -0.05 | -0.21 | -0.22 | -0.19 | -0.19 |
| `snip` | 150 | -0.19 (-0.34, -0.03) | — | -0.12 | 0.0196 | -0.25 | 0.059 | -0.06 | -0.21 | -0.22 | -0.19 | -0.19 |
