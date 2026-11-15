# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=48) | has graph (n=102) | uses A (n=84) | gcn (incl. mixed) (n=69) | diffusion (incl. mixed) (n=72) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `tfas_zico_cl` | 150 | 0.58 (0.46, 0.67) | — | 0.40 | 8.19e-15 | 0.63 | 0.004 | 0.52 | 0.60 | 0.65 | 0.66 | 0.68 |
| `l2_norm` | 150 | 0.48 (0.35, 0.59) | — | 0.33 | 6.88e-10 | 0.52 | 0.001 | 0.35 | 0.52 | 0.58 | 0.56 | 0.61 |
| `synflow` | 150 | 0.15 (-0.01, 0.31) | — | 0.11 | 0.0625 | 0.13 | 0.024 | 0.52 | -0.08 | 0.03 | 0.10 | 0.02 |
| `plain` | 150 | -0.04 (-0.19, 0.11) | — | -0.02 | 0.619 | -0.09 | 0.636 | 0.21 | -0.14 | -0.14 | -0.06 | -0.17 |
| `grasp` | 150 | -0.14 (-0.30, 0.02) | — | -0.08 | 0.0927 | -0.13 | 0.764 | -0.20 | 0.09 | 0.14 | 0.12 | 0.16 |
| `grad_norm` | 150 | -0.14 (-0.29, 0.02) | — | -0.10 | 0.0855 | -0.22 | 0.060 | -0.18 | -0.06 | -0.04 | 0.00 | -0.06 |
| `snip` | 150 | -0.15 (-0.30, 0.01) | — | -0.10 | 0.0668 | -0.23 | 0.055 | -0.22 | -0.05 | -0.01 | 0.02 | -0.03 |
| `swap_b8` | 150 | — (—, —) | — | — | nan | — | 0.000 | — | — | — | — | — |
