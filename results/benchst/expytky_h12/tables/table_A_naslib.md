# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=48) | has graph (n=102) | uses A (n=84) | gcn (incl. mixed) (n=69) | diffusion (incl. mixed) (n=72) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `grasp` | 150 | 0.55 (0.42, 0.66) | — | 0.38 | 3.32e-13 | 0.56 | 0.629 | 0.44 | 0.54 | 0.53 | 0.49 | 0.55 |
| `l2_norm` | 150 | 0.21 (0.04, 0.36) | — | 0.14 | 0.0112 | 0.24 | 0.001 | 0.16 | 0.27 | 0.32 | 0.26 | 0.33 |
| `synflow` | 150 | -0.24 (-0.38, -0.09) | — | -0.16 | 0.00362 | -0.25 | 0.023 | -0.16 | -0.21 | -0.16 | -0.08 | -0.14 |
| `snip` | 150 | -0.38 (-0.51, -0.23) | — | -0.25 | 1.66e-06 | -0.41 | 0.077 | -0.32 | -0.42 | -0.36 | -0.39 | -0.38 |
| `grad_norm` | 150 | -0.42 (-0.54, -0.28) | — | -0.28 | 8.31e-08 | -0.45 | 0.099 | -0.34 | -0.46 | -0.41 | -0.41 | -0.44 |
| `plain` | 150 | -0.47 (-0.59, -0.34) | — | -0.33 | 9.05e-10 | -0.49 | 0.177 | -0.41 | -0.51 | -0.50 | -0.49 | -0.53 |
| `swap_b8` | 150 | — (—, —) | — | — | nan | -0.02 | 0.000 | — | — | — | — | — |
