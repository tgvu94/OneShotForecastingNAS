# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=50) | mid third (n=50) | large third (n=50) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `grasp_all` | 0.44 | -0.25 | 0.49 | 0.44 | 0.31 | 0.51 | 0.62 | 0.43 | -0.45 |
| `zico` | 0.22 | 0.74 | 0.16 | 0.19 | 0.43 | 0.03 | 0.24 | 0.11 | -0.14 |
| `l2_norm_all` | 0.21 | 0.75 | 0.12 | 0.17 | 0.42 | 0.02 | 0.19 | 0.09 | -0.09 |
| `zico_t` | 0.21 | 0.76 | 0.14 | 0.18 | 0.41 | -0.01 | 0.24 | 0.10 | -0.15 |
| `glass` | 0.20 | 0.75 | 0.13 | 0.17 | 0.42 | 0.00 | 0.20 | 0.09 | -0.13 |
| `glass_t` | 0.19 | 0.76 | 0.11 | 0.17 | 0.40 | -0.02 | 0.21 | 0.09 | -0.13 |
| `nwot` | 0.19 | 0.39 | 0.12 | 0.14 | 0.29 | 0.18 | 0.06 | 0.10 | 0.04 |
| `params` (complexity baseline) | 0.16 | 1.00 | — | 0.13 | 0.42 | 0.07 | 0.13 | 0.08 | 0.04 |
| `swap` | 0.15 | 0.77 | 0.04 | 0.07 | 0.34 | 0.07 | -0.02 | 0.07 | 0.09 |
| `zico_s` | 0.15 | -0.02 | 0.14 | 0.07 | 0.17 | 0.23 | 0.09 | 0.10 | -0.04 |
| `glass_s` | 0.14 | -0.02 | 0.13 | 0.05 | 0.17 | 0.22 | 0.09 | 0.09 | -0.03 |
| `flops` (complexity baseline) | 0.13 | 0.15 | 0.09 | — | 0.16 | 0.19 | 0.06 | 0.07 | -0.01 |
| `swap_reg` | 0.12 | 0.19 | 0.08 | 0.07 | 0.46 | 0.06 | -0.17 | 0.15 | 0.10 |
| `zico_sizectrl` | 0.09 | 0.03 | 0.10 | 0.07 | 0.09 | -0.00 | 0.24 | -0.00 | -0.33 |
| `zen` | 0.07 | 0.89 | -0.17 | 0.05 | 0.30 | -0.29 | 0.00 | 0.02 | 0.07 |
| `synflow_all` | 0.07 | 0.09 | 0.06 | 0.04 | 0.25 | 0.03 | -0.05 | 0.04 | -0.06 |
| `jacov` | -0.10 | 0.24 | -0.14 | -0.03 | -0.07 | -0.05 | -0.27 | -0.08 | 0.05 |
| `nwot_per_layer` | -0.13 | -0.69 | -0.04 | -0.11 | -0.25 | 0.03 | -0.11 | -0.04 | 0.07 |
| `snip_all` | -0.40 | 0.37 | -0.48 | -0.39 | -0.29 | -0.47 | -0.61 | -0.41 | 0.41 |
| `grad_norm_all` | -0.42 | 0.36 | -0.50 | -0.42 | -0.32 | -0.49 | -0.60 | -0.43 | 0.40 |
| `fisher` | -0.49 | 0.26 | -0.53 | -0.48 | -0.38 | -0.54 | -0.65 | -0.49 | 0.40 |
| `plain_all` | -0.49 | 0.28 | -0.54 | -0.49 | -0.36 | -0.57 | -0.59 | -0.52 | 0.32 |
