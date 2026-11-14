# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=48) | has graph (n=102) | uses A (n=84) | gcn (incl. mixed) (n=69) | diffusion (incl. mixed) (n=72) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `grasp` | 150 | 0.42 (0.28, 0.56) | — | 0.28 | 7.43e-08 | 0.47 | 0.742 | 0.32 | 0.44 | 0.50 | 0.45 | 0.47 |
| `l2_norm` | 150 | 0.35 (0.19, 0.50) | — | 0.25 | 8.94e-06 | 0.39 | 0.001 | 0.36 | 0.37 | 0.39 | 0.33 | 0.40 |
| `synflow` | 150 | -0.16 (-0.30, 0.01) | — | -0.10 | 0.0582 | -0.18 | 0.025 | 0.09 | -0.23 | -0.14 | -0.08 | -0.08 |
| `snip` | 150 | -0.32 (-0.47, -0.17) | — | -0.22 | 5.98e-05 | -0.38 | 0.052 | -0.21 | -0.40 | -0.38 | -0.42 | -0.34 |
| `grad_norm` | 150 | -0.38 (-0.51, -0.24) | — | -0.26 | 1.52e-06 | -0.44 | 0.065 | -0.25 | -0.46 | -0.45 | -0.44 | -0.42 |
| `plain` | 150 | -0.38 (-0.52, -0.23) | — | -0.26 | 1.35e-06 | -0.44 | 0.241 | -0.22 | -0.49 | -0.48 | -0.42 | -0.44 |
| `swap_b8` | 150 | — (—, —) | — | — | nan | 0.05 | 0.000 | — | — | — | — | — |
