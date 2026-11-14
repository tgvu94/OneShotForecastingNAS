# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=50) | mid third (n=50) | large third (n=50) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `grasp_all` | 0.46 | -0.15 | 0.46 | 0.46 | 0.36 | 0.56 | 0.47 | 0.48 | -0.19 |
| `zico_sizectrl` | 0.22 | 0.03 | 0.22 | 0.23 | 0.19 | 0.29 | 0.27 | 0.26 | 0.41 |
| `zico_t` | 0.21 | 0.66 | 0.25 | 0.21 | 0.21 | 0.29 | 0.17 | 0.24 | 0.44 |
| `zico` | 0.20 | 0.66 | 0.24 | 0.21 | 0.22 | 0.25 | 0.20 | 0.22 | 0.44 |
| `glass_t` | 0.17 | 0.67 | 0.19 | 0.16 | 0.18 | 0.23 | 0.09 | 0.19 | 0.46 |
| `glass` | 0.16 | 0.67 | 0.19 | 0.17 | 0.17 | 0.19 | 0.13 | 0.18 | 0.46 |
| `l2_norm_all` | 0.13 | 0.78 | 0.19 | 0.17 | 0.15 | 0.13 | 0.16 | 0.14 | 0.41 |
| `jacov` | 0.07 | 0.05 | 0.08 | 0.02 | 0.11 | 0.18 | -0.12 | 0.10 | -0.08 |
| `params` (complexity baseline) | 0.03 | 1.00 | — | 0.04 | 0.11 | -0.04 | -0.22 | 0.03 | 0.23 |
| `swap_reg` | 0.03 | 0.16 | 0.03 | 0.06 | 0.06 | -0.23 | 0.25 | 0.04 | -0.08 |
| `zico_s` | -0.01 | 0.01 | 0.00 | 0.23 | -0.08 | -0.14 | 0.20 | -0.05 | 0.04 |
| `zen` | -0.01 | 0.85 | -0.09 | -0.01 | -0.10 | -0.05 | -0.15 | -0.01 | 0.14 |
| `glass_s` | -0.02 | 0.01 | -0.01 | 0.20 | -0.09 | -0.16 | 0.19 | -0.06 | 0.04 |
| `nwot` | -0.06 | 0.37 | -0.09 | 0.02 | -0.09 | -0.22 | 0.05 | -0.09 | 0.09 |
| `swap` | -0.06 | 0.63 | -0.11 | -0.01 | -0.06 | -0.22 | -0.02 | -0.09 | 0.13 |
| `flops` (complexity baseline) | -0.09 | 0.16 | -0.10 | — | -0.09 | -0.26 | 0.04 | -0.12 | 0.01 |
| `nwot_per_layer` | -0.18 | -0.59 | -0.20 | -0.19 | -0.10 | -0.29 | -0.09 | -0.19 | -0.34 |
| `synflow_all` | -0.19 | 0.07 | -0.20 | -0.17 | -0.01 | -0.30 | -0.26 | -0.21 | 0.18 |
| `snip_all` | -0.42 | 0.25 | -0.44 | -0.43 | -0.36 | -0.48 | -0.49 | -0.43 | 0.17 |
| `plain_all` | -0.43 | 0.22 | -0.45 | -0.44 | -0.30 | -0.45 | -0.56 | -0.42 | 0.32 |
| `grad_norm_all` | -0.46 | 0.25 | -0.48 | -0.46 | -0.36 | -0.55 | -0.50 | -0.48 | 0.21 |
| `fisher` | -0.53 | 0.18 | -0.55 | -0.54 | -0.39 | -0.61 | -0.62 | -0.54 | 0.23 |
