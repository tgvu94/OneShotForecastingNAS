# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=48) | has graph (n=102) | uses A (n=84) | gcn (incl. mixed) (n=72) | diffusion (incl. mixed) (n=63) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `grasp` | 150 | 0.34 (0.18, 0.50) | — | 0.21 | 1.58e-05 | 0.35 | 0.727 | 0.43 | 0.32 | 0.44 | 0.47 | 0.50 |
| `l2_norm` | 150 | 0.21 (0.04, 0.35) | — | 0.14 | 0.0116 | 0.14 | 0.001 | 0.13 | 0.22 | 0.19 | 0.16 | 0.13 |
| `synflow` | 150 | 0.07 (-0.10, 0.21) | — | 0.04 | 0.42 | 0.06 | 0.026 | 0.01 | 0.06 | -0.03 | -0.02 | 0.01 |
| `snip` | 150 | -0.40 (-0.54, -0.24) | — | -0.25 | 3.68e-07 | -0.48 | 0.058 | -0.61 | -0.25 | -0.25 | -0.34 | -0.30 |
| `grad_norm` | 150 | -0.41 (-0.55, -0.26) | — | -0.26 | 1.41e-07 | -0.49 | 0.070 | -0.62 | -0.26 | -0.25 | -0.33 | -0.30 |
| `plain` | 150 | -0.50 (-0.62, -0.36) | — | -0.32 | 6.5e-11 | -0.55 | 0.278 | -0.66 | -0.41 | -0.45 | -0.50 | -0.49 |
| `swap_b8` | 150 | — (—, —) | — | — | nan | -0.01 | 0.000 | — | — | — | — | — |
