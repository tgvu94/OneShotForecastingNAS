# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=16) | has graph (n=34) | uses A (n=28) | gcn (incl. mixed) (n=19) | diffusion (incl. mixed) (n=25) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `grasp` | 50 | 0.48 (0.21, 0.68) | — | 0.33 | 0.000373 | 0.49 | 0.741 | 0.54 | 0.46 | 0.38 | 0.29 | 0.45 |
| `l2_norm` | 50 | 0.02 (-0.27, 0.32) | — | 0.02 | 0.871 | 0.12 | 0.001 | -0.14 | 0.08 | 0.09 | 0.19 | 0.07 |
| `tfas_zico_cl` | 50 | -0.08 (-0.35, 0.20) | — | -0.05 | 0.599 | -0.08 | 0.004 | -0.19 | 0.00 | -0.03 | 0.13 | -0.04 |
| `synflow` | 50 | -0.23 (-0.48, 0.05) | — | -0.17 | 0.113 | -0.19 | 0.036 | -0.29 | -0.21 | -0.02 | 0.11 | 0.04 |
| `snip` | 50 | -0.38 (-0.62, -0.08) | — | -0.26 | 0.00622 | -0.39 | 0.051 | -0.54 | -0.31 | -0.25 | -0.28 | -0.29 |
| `grad_norm` | 50 | -0.42 (-0.65, -0.13) | — | -0.28 | 0.00217 | -0.42 | 0.071 | -0.59 | -0.36 | -0.28 | -0.29 | -0.32 |
| `plain` | 50 | -0.50 (-0.69, -0.25) | — | -0.33 | 0.000221 | -0.51 | 0.302 | -0.50 | -0.50 | -0.44 | -0.29 | -0.49 |
