# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=48) | has graph (n=102) | uses A (n=84) | gcn (incl. mixed) (n=69) | diffusion (incl. mixed) (n=72) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `grasp` | 150 | 0.44 (0.28, 0.57) | — | 0.28 | 2.15e-08 | 0.45 | 0.698 | 0.37 | 0.42 | 0.38 | 0.33 | 0.36 |
| `l2_norm` | 150 | 0.15 (-0.02, 0.30) | — | 0.10 | 0.0739 | 0.26 | 0.001 | 0.10 | 0.19 | 0.20 | 0.14 | 0.20 |
| `synflow` | 150 | -0.18 (-0.32, -0.02) | — | -0.12 | 0.0282 | -0.18 | 0.028 | -0.09 | -0.17 | -0.09 | -0.05 | -0.02 |
| `snip` | 150 | -0.42 (-0.55, -0.26) | — | -0.28 | 8.32e-08 | -0.44 | 0.056 | -0.36 | -0.44 | -0.40 | -0.45 | -0.39 |
| `grad_norm` | 150 | -0.45 (-0.58, -0.30) | — | -0.30 | 5.92e-09 | -0.47 | 0.077 | -0.38 | -0.48 | -0.44 | -0.48 | -0.44 |
| `plain` | 150 | -0.47 (-0.59, -0.32) | — | -0.31 | 1.37e-09 | -0.49 | 0.306 | -0.40 | -0.52 | -0.50 | -0.49 | -0.47 |
| `swap_b8` | 150 | — (—, —) | — | — | nan | 0.05 | 0.000 | — | — | — | — | — |
