# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=96) | has graph (n=204) | uses A (n=168) | gcn (incl. mixed) (n=125) | diffusion (incl. mixed) (n=136) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `tfas_zico_cl` | 300 | 0.51 (0.41, 0.59) | — | 0.35 | 3.4e-21 | 0.60 | 0.004 | 0.41 | 0.53 | 0.51 | 0.49 | 0.53 |
| `l2_norm` | 300 | 0.38 (0.27, 0.49) | — | 0.26 | 6.41e-12 | 0.43 | 0.001 | 0.27 | 0.44 | 0.42 | 0.41 | 0.44 |
| `synflow` | 300 | 0.21 (0.10, 0.32) | — | 0.14 | 0.000234 | 0.22 | 0.026 | 0.17 | 0.02 | 0.04 | 0.08 | 0.02 |
| `plain` | 300 | -0.08 (-0.19, 0.03) | — | -0.05 | 0.165 | -0.10 | 0.543 | 0.05 | -0.10 | -0.15 | -0.06 | -0.16 |
| `grasp` | 300 | -0.09 (-0.19, 0.03) | — | -0.05 | 0.14 | -0.10 | 0.689 | -0.04 | 0.18 | 0.23 | 0.21 | 0.23 |
| `grad_norm` | 300 | -0.13 (-0.24, -0.02) | — | -0.09 | 0.0207 | -0.19 | 0.060 | -0.07 | -0.07 | -0.11 | -0.04 | -0.14 |
| `snip` | 300 | -0.14 (-0.25, -0.03) | — | -0.09 | 0.0162 | -0.20 | 0.057 | -0.09 | -0.05 | -0.09 | -0.01 | -0.11 |
