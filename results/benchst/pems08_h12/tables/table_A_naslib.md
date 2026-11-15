# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=48) | has graph (n=102) | uses A (n=84) | gcn (incl. mixed) (n=69) | diffusion (incl. mixed) (n=72) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `l2_norm` | 150 | 0.34 (0.18, 0.47) | — | 0.23 | 2.61e-05 | 0.46 | 0.001 | 0.29 | 0.36 | 0.38 | 0.30 | 0.38 |
| `grasp` | 150 | 0.09 (-0.08, 0.27) | — | 0.06 | 0.249 | 0.11 | 0.713 | -0.17 | 0.26 | 0.30 | 0.18 | 0.32 |
| `synflow` | 150 | -0.03 (-0.19, 0.14) | — | -0.02 | 0.724 | -0.04 | 0.026 | 0.27 | -0.17 | -0.09 | -0.04 | -0.02 |
| `plain` | 150 | -0.43 (-0.56, -0.29) | — | -0.29 | 4.44e-08 | -0.46 | 0.502 | -0.18 | -0.52 | -0.50 | -0.49 | -0.51 |
| `snip` | 150 | -0.43 (-0.56, -0.29) | — | -0.29 | 2.92e-08 | -0.49 | 0.061 | -0.52 | -0.36 | -0.31 | -0.36 | -0.28 |
| `grad_norm` | 150 | -0.47 (-0.59, -0.33) | — | -0.32 | 1.33e-09 | -0.53 | 0.064 | -0.53 | -0.41 | -0.37 | -0.40 | -0.34 |
| `swap_b8` | 150 | — (—, —) | — | — | nan | 0.07 | 0.000 | — | — | — | — | — |
