# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=48) | has graph (n=102) | uses A (n=84) | gcn (incl. mixed) (n=69) | diffusion (incl. mixed) (n=72) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `l2_norm` | 150 | 0.35 (0.21, 0.48) | — | 0.23 | 1.32e-05 | 0.32 | 0.001 | 0.41 | 0.40 | 0.45 | 0.44 | 0.45 |
| `grasp` | 150 | 0.30 (0.15, 0.45) | — | 0.21 | 0.000162 | 0.31 | 0.756 | 0.12 | 0.27 | 0.27 | 0.19 | 0.22 |
| `synflow` | 150 | 0.03 (-0.12, 0.18) | — | 0.02 | 0.693 | 0.02 | 0.025 | 0.40 | -0.04 | 0.03 | 0.08 | 0.10 |
| `plain` | 150 | -0.12 (-0.27, 0.03) | — | -0.08 | 0.131 | -0.16 | 0.285 | -0.00 | -0.24 | -0.23 | -0.16 | -0.18 |
| `snip` | 150 | -0.14 (-0.29, 0.02) | — | -0.10 | 0.0872 | -0.19 | 0.058 | -0.21 | -0.16 | -0.15 | -0.15 | -0.12 |
| `grad_norm` | 150 | -0.15 (-0.31, -0.01) | — | -0.11 | 0.0593 | -0.21 | 0.070 | -0.21 | -0.19 | -0.17 | -0.15 | -0.13 |
| `swap_b8` | 150 | — (—, —) | — | — | nan | 0.02 | 0.000 | — | — | — | — | — |
