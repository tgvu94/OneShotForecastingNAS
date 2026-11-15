# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=50) | mid third (n=50) | large third (n=50) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `grasp_all` | 0.53 | -0.13 | 0.55 | 0.53 | 0.43 | 0.63 | 0.54 | 0.48 | 0.46 |
| `glass` | 0.34 | 0.68 | 0.34 | 0.34 | 0.35 | 0.32 | 0.33 | 0.34 | 0.23 |
| `zico` | 0.34 | 0.68 | 0.33 | 0.33 | 0.31 | 0.35 | 0.31 | 0.33 | 0.22 |
| `glass_t` | 0.33 | 0.68 | 0.31 | 0.33 | 0.35 | 0.30 | 0.29 | 0.32 | 0.23 |
| `zico_t` | 0.33 | 0.67 | 0.31 | 0.33 | 0.33 | 0.31 | 0.28 | 0.32 | 0.23 |
| `zico_sizectrl` | 0.30 | 0.04 | 0.29 | 0.29 | 0.21 | 0.38 | 0.37 | 0.30 | 0.16 |
| `l2_norm_all` | 0.29 | 0.78 | 0.29 | 0.29 | 0.29 | 0.20 | 0.31 | 0.31 | 0.15 |
| `params` (complexity baseline) | 0.15 | 1.00 | — | 0.13 | 0.24 | -0.00 | -0.15 | 0.14 | 0.11 |
| `nwot` | 0.11 | 0.34 | 0.05 | 0.06 | 0.01 | -0.01 | 0.19 | 0.15 | -0.03 |
| `glass_s` | 0.10 | 0.02 | 0.12 | 0.12 | -0.07 | 0.09 | 0.28 | 0.16 | -0.06 |
| `zico_s` | 0.10 | 0.02 | 0.11 | 0.09 | -0.08 | 0.08 | 0.27 | 0.15 | -0.06 |
| `swap_reg` | 0.09 | 0.17 | 0.09 | 0.06 | 0.20 | -0.14 | 0.16 | 0.09 | 0.08 |
| `zen` | 0.07 | 0.85 | -0.10 | 0.07 | 0.01 | -0.10 | -0.05 | 0.08 | 0.10 |
| `flops` (complexity baseline) | 0.07 | 0.17 | 0.03 | — | -0.05 | -0.02 | 0.19 | 0.11 | -0.06 |
| `swap` | 0.06 | 0.66 | -0.05 | -0.00 | 0.03 | -0.12 | -0.01 | 0.07 | -0.03 |
| `synflow_all` | -0.03 | 0.07 | -0.04 | -0.08 | 0.19 | -0.09 | -0.18 | -0.01 | -0.06 |
| `jacov` | -0.08 | 0.01 | -0.08 | -0.05 | -0.01 | -0.04 | -0.14 | -0.13 | 0.02 |
| `nwot_per_layer` | -0.28 | -0.59 | -0.24 | -0.27 | -0.26 | -0.26 | -0.19 | -0.28 | -0.20 |
| `snip_all` | -0.43 | 0.25 | -0.49 | -0.43 | -0.35 | -0.54 | -0.49 | -0.40 | -0.39 |
| `plain_all` | -0.45 | 0.15 | -0.49 | -0.45 | -0.19 | -0.52 | -0.65 | -0.43 | -0.39 |
| `grad_norm_all` | -0.47 | 0.24 | -0.53 | -0.47 | -0.35 | -0.62 | -0.55 | -0.43 | -0.42 |
| `fisher` | -0.52 | 0.20 | -0.56 | -0.51 | -0.32 | -0.63 | -0.66 | -0.47 | -0.47 |
