# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=16) | has graph (n=34) | uses A (n=28) | gcn (incl. mixed) (n=19) | diffusion (incl. mixed) (n=25) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `tfas_zico_cl` | 50 | 0.68 (0.47, 0.82) | — | 0.51 | 4.94e-08 | 0.53 | 0.004 | 0.87 | 0.60 | 0.52 | 0.57 | 0.51 |
| `l2_norm` | 50 | 0.66 (0.46, 0.80) | — | 0.47 | 1.4e-07 | 0.49 | 0.001 | 0.84 | 0.59 | 0.52 | 0.54 | 0.52 |
| `synflow` | 50 | -0.07 (-0.39, 0.23) | — | -0.06 | 0.611 | -0.07 | 0.023 | 0.26 | -0.30 | -0.19 | 0.12 | -0.28 |
| `grasp` | 50 | -0.08 (-0.36, 0.23) | — | -0.05 | 0.582 | -0.17 | 0.654 | -0.19 | -0.06 | 0.01 | -0.06 | 0.05 |
| `plain` | 50 | -0.13 (-0.40, 0.18) | — | -0.10 | 0.358 | -0.26 | 0.293 | 0.00 | -0.24 | -0.26 | -0.08 | -0.28 |
| `grad_norm` | 50 | -0.29 (-0.55, -0.01) | — | -0.22 | 0.0406 | -0.52 | 0.057 | -0.30 | -0.33 | -0.33 | -0.29 | -0.31 |
| `snip` | 50 | -0.30 (-0.55, -0.01) | — | -0.22 | 0.036 | -0.53 | 0.062 | -0.32 | -0.33 | -0.32 | -0.29 | -0.33 |
