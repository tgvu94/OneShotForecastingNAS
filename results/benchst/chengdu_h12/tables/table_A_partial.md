# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=50) | mid third (n=50) | large third (n=50) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `zico_t` | 0.53 | 0.67 | 0.53 | 0.54 | 0.46 | 0.58 | 0.29 | 0.52 | 0.54 |
| `glass_t` | 0.53 | 0.68 | 0.52 | 0.54 | 0.47 | 0.58 | 0.30 | 0.51 | 0.55 |
| `zico` | 0.50 | 0.68 | 0.48 | 0.53 | 0.43 | 0.53 | 0.27 | 0.47 | 0.53 |
| `glass` | 0.50 | 0.69 | 0.48 | 0.53 | 0.43 | 0.53 | 0.27 | 0.47 | 0.54 |
| `zico_sizectrl` | 0.44 | 0.03 | 0.44 | 0.46 | 0.40 | 0.57 | 0.32 | 0.38 | 0.45 |
| `l2_norm_all` | 0.25 | 0.72 | 0.14 | 0.35 | 0.10 | 0.21 | 0.08 | 0.14 | 0.31 |
| `params` (complexity baseline) | 0.22 | 1.00 | — | 0.27 | 0.14 | -0.04 | -0.09 | 0.23 | 0.25 |
| `grasp_all` | 0.22 | -0.12 | 0.24 | 0.22 | 0.07 | 0.42 | 0.21 | 0.20 | -0.35 |
| `jacov` | 0.21 | 0.03 | 0.22 | 0.10 | 0.29 | 0.11 | 0.22 | 0.30 | 0.13 |
| `zen` | 0.10 | 0.85 | -0.16 | 0.12 | -0.01 | -0.24 | -0.14 | 0.12 | 0.16 |
| `synflow_all` | 0.03 | 0.10 | 0.01 | 0.12 | 0.03 | -0.02 | 0.05 | 0.04 | 0.22 |
| `swap_reg` | -0.02 | 0.17 | -0.06 | 0.05 | -0.01 | -0.27 | 0.06 | -0.03 | -0.03 |
| `plain_all` | -0.09 | 0.18 | -0.14 | -0.10 | 0.08 | -0.38 | -0.09 | -0.06 | 0.48 |
| `swap` | -0.10 | 0.63 | -0.32 | 0.08 | -0.29 | -0.31 | -0.25 | -0.13 | 0.04 |
| `fisher` | -0.13 | 0.18 | -0.17 | -0.13 | 0.03 | -0.36 | -0.13 | -0.10 | 0.45 |
| `snip_all` | -0.14 | 0.23 | -0.19 | -0.16 | -0.05 | -0.32 | -0.13 | -0.11 | 0.33 |
| `grad_norm_all` | -0.15 | 0.23 | -0.20 | -0.16 | -0.05 | -0.37 | -0.13 | -0.13 | 0.38 |
| `nwot` | -0.20 | 0.35 | -0.30 | -0.04 | -0.30 | -0.32 | -0.19 | -0.30 | -0.08 |
| `glass_s` | -0.22 | 0.03 | -0.22 | -0.01 | -0.34 | -0.21 | -0.11 | -0.34 | -0.13 |
| `zico_s` | -0.23 | 0.02 | -0.23 | -0.03 | -0.34 | -0.22 | -0.12 | -0.35 | -0.13 |
| `flops` (complexity baseline) | -0.23 | 0.14 | -0.28 | — | -0.36 | -0.25 | -0.19 | -0.31 | -0.11 |
| `nwot_per_layer` | -0.33 | -0.60 | -0.24 | -0.36 | -0.22 | -0.36 | -0.10 | -0.31 | -0.35 |
