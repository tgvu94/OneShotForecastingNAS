# Cross-setting comparison — PEMS04-12, PEMS08-12, METRLA-12, PEMS04-36

Spearman of the proxy (mean over 3 init seeds) with −val MAE (seed 0) on each setting, 95 % bootstrap CI, partial ρ | log params. All roots use the same genotype space and schedule; only the data, the number of sensors and the adjacency differ.

| setting | tables | N | seed-noise ceiling (s0-s1 / s0-s2 / s1-s2) | within / across std |
|---|---|---|---|---|
| PEMS04-12 | `results/stzero/pems04_h12/tables_n150` | 150 | 1.00 / 0.90 / 0.90 | 0.0003 / 0.0039 |
| PEMS08-12 | `results/stzero/pems08_h12/tables` | 150 | 1.00 / 1.00 / 1.00 | 0.0003 / 0.0046 |
| METRLA-12 | `results/stzero/metrla_h12/tables` | 50 | 0.60 / 0.90 / 0.70 | 0.0021 / 0.0129 |
| PEMS04-36 | `results/stzero/pems04_h36/tables` | 50 | 0.20 / 0.60 / 0.60 | 0.0013 / 0.0064 |

| proxy | PEMS04-12 ρ (95 % CI) | partial | PEMS08-12 ρ (95 % CI) | partial | METRLA-12 ρ (95 % CI) | partial | PEMS04-36 ρ (95 % CI) | partial |
|---|---|---|---|---|---|---|---|---|
| `zico` | 0.57 (0.44, 0.67) | 0.67 | 0.32 (0.15, 0.46) | 0.35 | -0.09 (-0.36, 0.20) | -0.07 | 0.71 (0.52, 0.82) | 0.56 |
| `l2_norm_all` | 0.50 (0.36, 0.62) | 0.59 | 0.25 (0.09, 0.41) | 0.30 | 0.00 (-0.30, 0.29) | 0.07 | 0.59 (0.34, 0.76) | 0.37 |
| `nwot` | 0.39 (0.24, 0.52) | 0.31 | 0.05 (-0.11, 0.22) | 0.01 | 0.05 (-0.25, 0.34) | 0.04 | 0.03 (-0.27, 0.31) | -0.22 |
| `flops` (complexity baseline) | 0.35 (0.19, 0.48) | — | 0.00 (-0.17, 0.16) | — | 0.02 (-0.26, 0.31) | — | -0.03 (-0.34, 0.25) | — |
| `grasp_all` | 0.20 (0.03, 0.34) | 0.23 | 0.47 (0.32, 0.60) | 0.50 | 0.43 (0.15, 0.64) | 0.42 | 0.30 (0.02, 0.56) | 0.47 |
| `params` (complexity baseline) | 0.19 (0.04, 0.34) | — | 0.10 (-0.06, 0.28) | — | -0.04 (-0.32, 0.26) | — | 0.51 (0.27, 0.68) | — |
| `synflow_all` | 0.18 (0.02, 0.33) | 0.19 | -0.01 (-0.18, 0.17) | -0.01 | -0.23 (-0.48, 0.05) | -0.20 | -0.10 (-0.42, 0.20) | -0.11 |
| `zen` | 0.16 (0.02, 0.30) | -0.07 | 0.00 (-0.15, 0.17) | -0.14 | -0.05 (-0.36, 0.26) | -0.02 | 0.30 (0.01, 0.54) | -0.29 |
| `fisher` | -0.10 (-0.25, 0.06) | -0.13 | -0.44 (-0.58, -0.29) | -0.47 | -0.55 (-0.72, -0.28) | -0.55 | -0.26 (-0.53, 0.03) | -0.46 |
| `plain_all` | -0.14 (-0.29, 0.03) | -0.15 | -0.47 (-0.59, -0.32) | -0.48 | -0.45 (-0.65, -0.20) | -0.46 | -0.15 (-0.42, 0.15) | -0.28 |
| `grad_norm_all` | -0.16 (-0.31, -0.00) | -0.22 | -0.40 (-0.53, -0.24) | -0.47 | -0.44 (-0.66, -0.15) | -0.44 | -0.28 (-0.54, 0.01) | -0.51 |
| `snip_all` | -0.19 (-0.34, -0.03) | -0.25 | -0.36 (-0.50, -0.20) | -0.44 | -0.39 (-0.62, -0.08) | -0.39 | -0.29 (-0.55, -0.01) | -0.52 |
| `jacov` | -0.41 (-0.53, -0.29) | -0.46 | -0.10 (-0.25, 0.07) | -0.12 | -0.05 (-0.31, 0.23) | -0.05 | -0.15 (-0.40, 0.15) | -0.24 |

## Does the proxy *ordering* transfer? (reference: PEMS04-12)

| pair | proxies | Spearman of the ρ vectors | Kendall | Pearson | same sign | top 3 (reference) | top 3 (other) |
|---|---|---|---|---|---|---|---|
| PEMS04-12 vs PEMS08-12 | 13 | 0.79 | 0.56 | 0.74 | 12/13 | zico,l2_norm_all,nwot | grasp_all,zico,l2_norm_all |
| PEMS04-12 vs METRLA-12 | 13 | 0.59 | 0.36 | 0.52 | 9/13 | zico,l2_norm_all,nwot | grasp_all,nwot,flops |
| PEMS04-12 vs PEMS04-36 | 13 | 0.84 | 0.67 | 0.76 | 11/13 | zico,l2_norm_all,nwot | zico,l2_norm_all,params |
