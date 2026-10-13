# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=50) | mid third (n=50) | large third (n=50) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `zico_sizectrl` | 0.66 | 0.04 | 0.67 | 0.62 | 0.43 | 0.79 | 0.74 | 0.61 | 0.56 |
| `zico` | 0.57 | 0.74 | 0.67 | 0.52 | 0.39 | 0.80 | 0.68 | 0.53 | 0.46 |
| `l2_norm_all` | 0.50 | 0.80 | 0.59 | 0.44 | 0.34 | 0.70 | 0.65 | 0.48 | 0.44 |
| `nwot` | 0.39 | 0.30 | 0.31 | 0.15 | 0.20 | 0.40 | 0.39 | 0.36 | 0.40 |
| `flops` (complexity baseline) | 0.35 | 0.14 | 0.31 | — | 0.16 | 0.42 | 0.37 | 0.31 | 0.39 |
| `swap` | 0.26 | 0.63 | 0.20 | 0.02 | 0.10 | 0.26 | 0.37 | 0.26 | 0.25 |
| `grasp_all` | 0.20 | -0.10 | 0.23 | 0.24 | 0.33 | 0.18 | 0.22 | 0.32 | -0.17 |
| `params` (complexity baseline) | 0.19 | 1.00 | — | 0.16 | -0.02 | 0.40 | 0.07 | 0.19 | 0.15 |
| `synflow_all` | 0.18 | -0.04 | 0.19 | -0.03 | 0.10 | 0.20 | 0.25 | 0.15 | 0.26 |
| `zen` | 0.16 | 0.89 | -0.07 | 0.10 | -0.07 | 0.20 | 0.03 | 0.15 | 0.14 |
| `swap_reg` | 0.13 | 0.17 | 0.10 | 0.01 | 0.02 | 0.31 | 0.08 | 0.14 | 0.12 |
| `fisher` | -0.10 | 0.10 | -0.13 | -0.15 | -0.26 | -0.11 | -0.08 | -0.27 | 0.30 |
| `plain_all` | -0.14 | 0.05 | -0.15 | -0.18 | -0.20 | -0.14 | -0.10 | -0.30 | 0.32 |
| `grad_norm_all` | -0.16 | 0.24 | -0.22 | -0.20 | -0.29 | -0.24 | -0.17 | -0.29 | 0.16 |
| `snip_all` | -0.19 | 0.26 | -0.25 | -0.21 | -0.30 | -0.28 | -0.17 | -0.30 | 0.09 |
| `jacov` | -0.41 | 0.16 | -0.46 | -0.25 | -0.28 | -0.59 | -0.44 | -0.38 | -0.44 |
