# Cross-setting comparison — PEMS04-12, PEMS08-12, PEMS04-36, METRLA-12

Spearman of the proxy (mean over 3 init seeds) with −val MAE (seed 0) on each setting, 95 % bootstrap CI, partial ρ | log params. All roots use the same genotype space and schedule; only the data, the number of sensors and the adjacency differ.

| setting | tables | N | seed-noise ceiling (s0-s1 / s0-s2 / s1-s2) | within / across std |
|---|---|---|---|---|
| PEMS04-12 | `results/stzero/pems04_h12/tables` | 300 | 1.00 / 0.90 / 0.90 | 0.0003 / 0.0033 |
| PEMS08-12 | `results/stzero/pems08_h12/tables` | 150 | 1.00 / 1.00 / 1.00 | 0.0003 / 0.0046 |
| PEMS04-36 | `results/stzero/pems04_h36/tables` | 50 | 0.20 / 0.60 / 0.60 | 0.0013 / 0.0064 |
| METRLA-12 | `results/stzero/metrla_h12/tables` | 150 | 0.60 / 0.90 / 0.70 | 0.0021 / 0.0123 |

| proxy | PEMS04-12 ρ (95 % CI) | partial | PEMS08-12 ρ (95 % CI) | partial | PEMS04-36 ρ (95 % CI) | partial | METRLA-12 ρ (95 % CI) | partial |
|---|---|---|---|---|---|---|---|---|
| `zico_sizectrl` | 0.59 (0.51, 0.67) | 0.60 | 0.31 (0.15, 0.45) | 0.31 | 0.55 (0.32, 0.74) | 0.60 | 0.06 (-0.10, 0.22) | 0.06 |
| `zico` | 0.57 (0.48, 0.65) | 0.63 | 0.32 (0.15, 0.46) | 0.35 | 0.71 (0.52, 0.82) | 0.56 | 0.01 (-0.14, 0.16) | 0.06 |
| `l2_norm_all` | 0.50 (0.41, 0.59) | 0.55 | 0.25 (0.09, 0.41) | 0.30 | 0.59 (0.34, 0.76) | 0.37 | -0.00 (-0.16, 0.16) | 0.08 |
| `nwot` | 0.34 (0.24, 0.43) | 0.28 | 0.05 (-0.11, 0.22) | 0.01 | 0.03 (-0.27, 0.31) | -0.22 | -0.07 (-0.24, 0.09) | -0.08 |
| `flops` (complexity baseline) | 0.31 (0.21, 0.41) | — | 0.00 (-0.17, 0.16) | — | -0.03 (-0.34, 0.25) | — | -0.06 (-0.21, 0.10) | — |
| `swap` | 0.22 (0.11, 0.32) | 0.12 | 0.06 (-0.10, 0.23) | 0.00 | 0.09 (-0.19, 0.36) | -0.28 | -0.09 (-0.25, 0.06) | -0.08 |
| `params` (complexity baseline) | 0.19 (0.08, 0.31) | — | 0.10 (-0.06, 0.28) | — | 0.51 (0.27, 0.68) | — | -0.04 (-0.20, 0.12) | — |
| `synflow_all` | 0.19 (0.08, 0.30) | 0.19 | -0.01 (-0.18, 0.17) | -0.01 | -0.10 (-0.42, 0.20) | -0.11 | -0.20 (-0.35, -0.04) | -0.20 |
| `grasp_all` | 0.17 (0.06, 0.28) | 0.20 | 0.47 (0.32, 0.60) | 0.50 | 0.30 (0.02, 0.56) | 0.47 | 0.47 (0.33, 0.58) | 0.47 |
| `zen` | 0.12 (0.00, 0.24) | -0.15 | 0.00 (-0.15, 0.17) | -0.14 | 0.30 (0.01, 0.54) | -0.29 | -0.05 (-0.21, 0.11) | -0.02 |
| `swap_reg` | 0.08 (-0.04, 0.19) | 0.05 | 0.01 (-0.15, 0.17) | -0.01 | -0.16 (-0.44, 0.15) | -0.24 | 0.05 (-0.11, 0.21) | 0.07 |
| `fisher` | -0.08 (-0.19, 0.03) | -0.11 | -0.44 (-0.58, -0.29) | -0.47 | -0.26 (-0.53, 0.03) | -0.46 | -0.53 (-0.64, -0.40) | -0.54 |
| `plain_all` | -0.09 (-0.20, 0.02) | -0.11 | -0.47 (-0.59, -0.32) | -0.48 | -0.15 (-0.42, 0.15) | -0.28 | -0.49 (-0.61, -0.36) | -0.50 |
| `grad_norm_all` | -0.13 (-0.23, -0.01) | -0.18 | -0.40 (-0.53, -0.24) | -0.47 | -0.28 (-0.54, 0.01) | -0.51 | -0.47 (-0.58, -0.32) | -0.47 |
| `snip_all` | -0.14 (-0.24, -0.02) | -0.20 | -0.36 (-0.50, -0.20) | -0.44 | -0.29 (-0.55, -0.01) | -0.52 | -0.41 (-0.53, -0.26) | -0.42 |
| `jacov` | -0.29 (-0.39, -0.18) | -0.32 | -0.10 (-0.25, 0.07) | -0.12 | -0.15 (-0.40, 0.15) | -0.24 | 0.07 (-0.10, 0.24) | 0.08 |

## Does the proxy *ordering* transfer? (reference: PEMS04-12)

| pair | proxies | Spearman of the ρ vectors | Kendall | Pearson | same sign | top 3 (reference) | top 3 (other) |
|---|---|---|---|---|---|---|---|
| PEMS04-12 vs PEMS08-12 | 16 | 0.76 | 0.53 | 0.77 | 15/16 | zico_sizectrl,zico,l2_norm_all | grasp_all,zico,zico_sizectrl |
| PEMS04-12 vs PEMS04-36 | 16 | 0.82 | 0.63 | 0.81 | 13/16 | zico_sizectrl,zico,l2_norm_all | zico,l2_norm_all,zico_sizectrl |
| PEMS04-12 vs METRLA-12 | 16 | 0.34 | 0.27 | 0.46 | 8/16 | zico_sizectrl,zico,l2_norm_all | grasp_all,jacov,zico_sizectrl |

## PEMS04-12: N = 50 vs N = 300

| proxy | ρ at N = 50 (95 % CI) | half-width | ρ at N = 300 (95 % CI) | half-width | N = 300 estimate inside the N = 50 CI? | shift |
|---|---|---|---|---|---|---|
| `zico` | 0.65 (0.45, 0.78) | ±0.16 | 0.57 (0.48, 0.65) | ±0.08 | yes | -0.08 |
| `l2_norm_all` | 0.63 (0.40, 0.78) | ±0.19 | 0.50 (0.41, 0.59) | ±0.09 | yes | -0.13 |
| `nwot` | 0.17 (-0.14, 0.44) | ±0.29 | 0.34 (0.24, 0.43) | ±0.09 | yes | +0.17 |
| `flops` | 0.06 (-0.25, 0.34) | ±0.30 | 0.31 (0.21, 0.41) | ±0.10 | yes | +0.26 |
| `params` | 0.47 (0.23, 0.65) | ±0.21 | 0.19 (0.08, 0.31) | ±0.11 | no | -0.28 |
| `synflow_all` | -0.11 (-0.41, 0.18) | ±0.30 | 0.19 (0.08, 0.30) | ±0.11 | no | +0.30 |
| `grasp_all` | 0.35 (0.07, 0.57) | ±0.25 | 0.17 (0.06, 0.28) | ±0.11 | yes | -0.17 |
| `zen` | 0.33 (0.05, 0.55) | ±0.25 | 0.12 (0.00, 0.24) | ±0.12 | yes | -0.21 |
| `fisher` | -0.27 (-0.51, 0.01) | ±0.26 | -0.08 (-0.19, 0.03) | ±0.11 | yes | +0.18 |
| `plain_all` | -0.21 (-0.45, 0.07) | ±0.26 | -0.09 (-0.20, 0.02) | ±0.11 | yes | +0.12 |
| `grad_norm_all` | -0.25 (-0.51, 0.02) | ±0.26 | -0.13 (-0.23, -0.01) | ±0.11 | yes | +0.13 |
| `snip_all` | -0.26 (-0.52, 0.04) | ±0.28 | -0.14 (-0.24, -0.02) | ±0.11 | yes | +0.12 |
| `jacov` | -0.18 (-0.43, 0.10) | ±0.26 | -0.29 (-0.39, -0.18) | ±0.11 | yes | -0.10 |

Mean CI half-width: ±0.25 at N = 50 vs ±0.11 at N = 300 (Fisher-z expectation ±0.30 and ±0.12). The N = 300 estimate lies inside the N = 50 interval for 11/13 proxies (the N = 50 point estimate lies inside the narrower N = 300 interval for 1/13 — the expected direction of disagreement: the small-sample point estimates scatter by ±0.25 around values now known to ±0.11). The first 50 architectures are a subset of the larger set, so the two estimates are not independent.
