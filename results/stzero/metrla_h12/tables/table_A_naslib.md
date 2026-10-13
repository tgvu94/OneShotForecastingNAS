# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=48) | has graph (n=102) | uses A (n=84) | gcn (incl. mixed) (n=69) | diffusion (incl. mixed) (n=72) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `grasp` | 150 | 0.54 (0.39, 0.65) | — | 0.36 | 1.3e-12 | 0.54 | 0.695 | 0.55 | 0.53 | 0.53 | 0.48 | 0.54 |
| `l2_norm` | 150 | 0.03 (-0.12, 0.18) | — | 0.02 | 0.682 | 0.16 | 0.001 | 0.01 | 0.07 | 0.06 | 0.05 | 0.08 |
| `tfas_zico_cl` | 150 | 0.01 (-0.15, 0.17) | — | 0.01 | 0.876 | 0.08 | 0.004 | -0.02 | 0.05 | 0.04 | 0.05 | 0.07 |
| `synflow` | 150 | -0.19 (-0.34, -0.03) | — | -0.12 | 0.0218 | -0.18 | 0.028 | -0.20 | -0.14 | -0.08 | -0.04 | -0.00 |
| `snip` | 150 | -0.41 (-0.53, -0.25) | — | -0.27 | 1.97e-07 | -0.42 | 0.054 | -0.30 | -0.46 | -0.44 | -0.47 | -0.46 |
| `grad_norm` | 150 | -0.46 (-0.57, -0.32) | — | -0.29 | 3.54e-09 | -0.46 | 0.071 | -0.34 | -0.51 | -0.50 | -0.52 | -0.51 |
| `plain` | 150 | -0.52 (-0.62, -0.39) | — | -0.33 | 1.21e-11 | -0.53 | 0.267 | -0.44 | -0.57 | -0.55 | -0.53 | -0.55 |
| `swap_b8` | 150 | — (—, —) | — | — | nan | 0.04 | 0.000 | — | — | — | — | — |
