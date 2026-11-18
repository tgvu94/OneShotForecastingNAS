# Table A (appendix) — NASLib Conv/Linear-only variants and the degenerate TFAS score

Spearman / Kendall of the proxy (mean over 3 init seeds) with −val MAE (seed 0, 20 epochs): positive = higher proxy, lower error. 95% CI = 2000-sample bootstrap. partial ρ = Spearman after regressing ranks on rank(log params). Subgroups with n < 8 are not reported.

| Proxy | N | Spearman (95% CI) | ρ / ceiling | Kendall | p | partial ρ \| log params | seed CV | graph-blind (n=48) | has graph (n=102) | uses A (n=84) | gcn (incl. mixed) (n=69) | diffusion (incl. mixed) (n=72) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `grasp` | 150 | 0.59 (0.45, 0.70) | — | 0.39 | 2.53e-15 | 0.59 | 0.694 | 0.51 | 0.64 | 0.64 | 0.62 | 0.64 |
| `l2_norm` | 150 | 0.16 (-0.01, 0.31) | — | 0.11 | 0.0554 | 0.19 | 0.001 | 0.17 | 0.19 | 0.20 | 0.12 | 0.21 |
| `synflow` | 150 | -0.26 (-0.40, -0.11) | — | -0.18 | 0.00113 | -0.27 | 0.026 | -0.16 | -0.27 | -0.23 | -0.20 | -0.19 |
| `snip` | 150 | -0.51 (-0.62, -0.37) | — | -0.34 | 2.76e-11 | -0.54 | 0.062 | -0.40 | -0.51 | -0.47 | -0.52 | -0.46 |
| `grad_norm` | 150 | -0.54 (-0.64, -0.41) | — | -0.35 | 1.05e-12 | -0.57 | 0.070 | -0.42 | -0.55 | -0.51 | -0.53 | -0.51 |
| `plain` | 150 | -0.67 (-0.75, -0.58) | — | -0.47 | 3.47e-21 | -0.70 | 0.262 | -0.59 | -0.70 | -0.69 | -0.69 | -0.70 |
| `swap_b8` | 150 | — (—, —) | — | — | nan | — | 0.000 | — | — | — | — | — |
