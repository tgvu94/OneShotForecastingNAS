# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=50) | mid third (n=50) | large third (n=50) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `grasp_all` | 0.46 | — | 0.48 | 0.45 | 0.44 | 0.40 | 0.56 | 0.32 | -0.49 |
| `zico_t` | 0.22 | — | 0.20 | 0.22 | 0.28 | 0.28 | 0.15 | 0.29 | 0.32 |
| `glass_t` | 0.21 | — | 0.19 | 0.21 | 0.27 | 0.25 | 0.12 | 0.28 | 0.33 |
| `zico` | 0.20 | — | 0.17 | 0.22 | 0.22 | 0.23 | 0.20 | 0.27 | 0.31 |
| `glass` | 0.20 | — | 0.16 | 0.21 | 0.22 | 0.22 | 0.18 | 0.26 | 0.32 |
| `zico_sizectrl` | 0.17 | — | 0.18 | 0.18 | 0.21 | 0.19 | 0.17 | 0.23 | 0.27 |
| `jacov` | 0.13 | -0.01 | 0.13 | 0.07 | 0.11 | 0.28 | -0.04 | 0.12 | -0.08 |
| `params` (complexity baseline) | 0.11 | 1.00 | — | 0.13 | 0.13 | 0.23 | 0.02 | 0.14 | 0.15 |
| `l2_norm_all` | 0.04 | 0.60 | -0.02 | 0.12 | -0.12 | -0.06 | 0.26 | 0.11 | 0.14 |
| `zen` | 0.02 | 0.80 | -0.09 | 0.03 | -0.14 | 0.12 | -0.18 | 0.06 | 0.16 |
| `swap_reg` | -0.04 | 0.15 | -0.05 | 0.00 | -0.05 | -0.13 | -0.05 | -0.08 | -0.04 |
| `zico_s` | -0.08 | — | -0.07 | 0.04 | -0.27 | -0.20 | 0.24 | -0.10 | -0.00 |
| `glass_s` | -0.08 | — | -0.07 | 0.04 | -0.28 | -0.19 | 0.24 | -0.10 | -0.00 |
| `nwot` | -0.11 | 0.37 | -0.17 | -0.04 | -0.30 | -0.22 | 0.14 | -0.14 | 0.04 |
| `swap` | -0.11 | 0.53 | -0.19 | -0.03 | -0.28 | -0.17 | -0.01 | -0.15 | 0.06 |
| `flops` (complexity baseline) | -0.12 | 0.14 | -0.15 | — | -0.26 | -0.20 | 0.12 | -0.16 | -0.02 |
| `nwot_per_layer` | -0.15 | -0.61 | -0.10 | -0.18 | 0.06 | -0.31 | -0.08 | -0.20 | -0.23 |
| `synflow_all` | -0.24 | 0.13 | -0.25 | -0.20 | -0.11 | -0.37 | -0.24 | -0.24 | -0.02 |
| `snip_all` | -0.38 | 0.18 | -0.41 | -0.38 | -0.36 | -0.36 | -0.46 | -0.23 | 0.43 |
| `grad_norm_all` | -0.43 | 0.17 | -0.46 | -0.42 | -0.39 | -0.43 | -0.51 | -0.27 | 0.46 |
| `plain_all` | -0.46 | 0.13 | -0.49 | -0.45 | -0.33 | -0.50 | -0.59 | -0.32 | 0.41 |
| `fisher` | -0.49 | 0.14 | -0.52 | -0.48 | -0.36 | -0.55 | -0.58 | -0.33 | 0.41 |
