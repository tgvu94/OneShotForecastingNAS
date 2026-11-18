# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=50) | mid third (n=50) | large third (n=50) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `grasp_all` | 0.57 | -0.12 | 0.58 | 0.57 | 0.56 | 0.65 | 0.56 | 0.57 | -0.42 |
| `zico_t` | 0.13 | 0.67 | 0.09 | 0.13 | 0.04 | 0.18 | 0.10 | 0.07 | -0.12 |
| `zico` | 0.13 | 0.67 | 0.10 | 0.13 | 0.03 | 0.14 | 0.13 | 0.06 | -0.11 |
| `l2_norm_all` | 0.12 | 0.75 | 0.10 | 0.13 | 0.10 | 0.04 | 0.25 | 0.05 | 0.06 |
| `glass_t` | 0.10 | 0.68 | 0.04 | 0.10 | 0.01 | 0.13 | 0.03 | 0.04 | -0.09 |
| `glass` | 0.09 | 0.68 | 0.04 | 0.09 | 0.01 | 0.09 | 0.07 | 0.03 | -0.08 |
| `params` (complexity baseline) | 0.09 | 1.00 | — | 0.09 | 0.20 | 0.08 | -0.15 | 0.06 | 0.13 |
| `swap_reg` | 0.09 | 0.18 | 0.07 | 0.08 | 0.16 | -0.21 | 0.22 | 0.08 | 0.05 |
| `zico_sizectrl` | 0.06 | 0.03 | 0.06 | 0.06 | -0.10 | 0.14 | 0.18 | -0.00 | -0.27 |
| `zico_s` | 0.04 | 0.02 | 0.04 | 0.13 | 0.01 | -0.15 | 0.26 | 0.00 | 0.05 |
| `jacov` | 0.03 | 0.08 | 0.02 | 0.07 | -0.03 | 0.11 | -0.07 | 0.04 | -0.18 |
| `glass_s` | 0.03 | 0.03 | 0.03 | 0.10 | 0.00 | -0.15 | 0.26 | -0.01 | 0.05 |
| `zen` | 0.02 | 0.85 | -0.09 | 0.02 | 0.04 | -0.07 | -0.10 | 0.02 | 0.11 |
| `nwot` | 0.02 | 0.38 | -0.03 | 0.02 | 0.05 | -0.20 | 0.18 | -0.02 | 0.14 |
| `swap` | -0.00 | 0.72 | -0.08 | -0.00 | 0.09 | -0.20 | 0.04 | -0.04 | 0.17 |
| `flops` (complexity baseline) | -0.01 | 0.14 | -0.03 | — | 0.08 | -0.22 | 0.13 | -0.03 | 0.08 |
| `nwot_per_layer` | -0.10 | -0.60 | -0.05 | -0.10 | 0.08 | -0.11 | -0.07 | -0.06 | 0.11 |
| `synflow_all` | -0.27 | 0.09 | -0.28 | -0.31 | -0.04 | -0.34 | -0.42 | -0.30 | -0.11 |
| `snip_all` | -0.51 | 0.23 | -0.54 | -0.50 | -0.45 | -0.61 | -0.51 | -0.51 | 0.39 |
| `grad_norm_all` | -0.55 | 0.22 | -0.58 | -0.55 | -0.49 | -0.67 | -0.57 | -0.55 | 0.39 |
| `fisher` | -0.63 | 0.17 | -0.66 | -0.63 | -0.50 | -0.72 | -0.69 | -0.62 | 0.33 |
| `plain_all` | -0.67 | 0.17 | -0.69 | -0.67 | -0.55 | -0.74 | -0.72 | -0.67 | 0.23 |
