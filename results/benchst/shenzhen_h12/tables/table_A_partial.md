# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=50) | mid third (n=50) | large third (n=50) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `grasp_all` | 0.46 | -0.12 | 0.49 | 0.46 | 0.44 | 0.50 | 0.53 | 0.37 | -0.23 |
| `zico_t` | 0.41 | 0.68 | 0.37 | 0.41 | 0.30 | 0.47 | 0.24 | 0.50 | 0.50 |
| `glass_t` | 0.41 | 0.68 | 0.36 | 0.41 | 0.29 | 0.48 | 0.25 | 0.50 | 0.51 |
| `zico` | 0.39 | 0.68 | 0.35 | 0.40 | 0.28 | 0.43 | 0.27 | 0.46 | 0.49 |
| `glass` | 0.39 | 0.69 | 0.34 | 0.40 | 0.28 | 0.42 | 0.27 | 0.46 | 0.49 |
| `zico_sizectrl` | 0.33 | 0.02 | 0.33 | 0.33 | 0.21 | 0.43 | 0.36 | 0.37 | 0.41 |
| `l2_norm_all` | 0.27 | 0.70 | 0.20 | 0.31 | 0.26 | 0.16 | 0.22 | 0.25 | 0.34 |
| `params` (complexity baseline) | 0.19 | 1.00 | — | 0.20 | 0.16 | -0.02 | -0.21 | 0.25 | 0.23 |
| `zen` | 0.09 | 0.84 | -0.12 | 0.09 | -0.05 | -0.00 | -0.26 | 0.15 | 0.16 |
| `jacov` | 0.06 | 0.00 | 0.06 | 0.02 | 0.04 | 0.26 | -0.17 | 0.16 | 0.01 |
| `swap_reg` | 0.04 | 0.19 | 0.02 | 0.06 | 0.07 | -0.26 | 0.17 | 0.03 | 0.06 |
| `swap` | -0.03 | 0.75 | -0.26 | -0.01 | -0.00 | -0.30 | -0.26 | -0.06 | 0.08 |
| `nwot` | -0.05 | 0.36 | -0.14 | -0.00 | -0.07 | -0.27 | 0.03 | -0.15 | 0.01 |
| `glass_s` | -0.06 | 0.03 | -0.06 | 0.03 | -0.12 | -0.24 | 0.18 | -0.19 | -0.07 |
| `zico_s` | -0.06 | 0.03 | -0.06 | 0.03 | -0.12 | -0.24 | 0.17 | -0.19 | -0.06 |
| `flops` (complexity baseline) | -0.07 | 0.13 | -0.11 | — | -0.13 | -0.25 | 0.11 | -0.19 | -0.03 |
| `synflow_all` | -0.16 | 0.10 | -0.19 | -0.16 | -0.11 | -0.26 | -0.21 | -0.14 | 0.04 |
| `nwot_per_layer` | -0.29 | -0.60 | -0.23 | -0.30 | -0.15 | -0.31 | -0.13 | -0.33 | -0.33 |
| `snip_all` | -0.32 | 0.23 | -0.37 | -0.33 | -0.27 | -0.34 | -0.48 | -0.24 | 0.25 |
| `plain_all` | -0.36 | 0.21 | -0.43 | -0.36 | -0.27 | -0.45 | -0.52 | -0.23 | 0.32 |
| `grad_norm_all` | -0.38 | 0.22 | -0.44 | -0.38 | -0.35 | -0.43 | -0.50 | -0.29 | 0.28 |
| `fisher` | -0.39 | 0.19 | -0.45 | -0.39 | -0.29 | -0.48 | -0.54 | -0.28 | 0.32 |
