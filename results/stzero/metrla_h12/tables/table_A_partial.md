# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=50) | mid third (n=50) | large third (n=50) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `grasp_all` | 0.47 | -0.16 | 0.47 | 0.47 | 0.41 | 0.50 | 0.48 | 0.53 | -0.22 |
| `jacov` | 0.07 | 0.05 | 0.08 | 0.07 | 0.06 | 0.24 | -0.11 | -0.01 | 0.02 |
| `zico_sizectrl` | 0.06 | 0.03 | 0.06 | 0.06 | -0.03 | 0.08 | 0.20 | -0.01 | -0.16 |
| `swap_reg` | 0.05 | 0.16 | 0.07 | 0.08 | 0.07 | -0.21 | 0.25 | 0.02 | -0.05 |
| `zico` | 0.01 | 0.66 | 0.06 | 0.02 | -0.03 | 0.10 | 0.12 | -0.09 | -0.08 |
| `l2_norm_all` | -0.00 | 0.78 | 0.08 | 0.02 | 0.08 | -0.07 | 0.16 | -0.09 | -0.01 |
| `params` (complexity baseline) | -0.04 | 1.00 | — | -0.03 | 0.09 | 0.10 | -0.20 | -0.11 | 0.11 |
| `zen` | -0.05 | 0.85 | -0.02 | -0.04 | -0.07 | 0.13 | -0.11 | -0.12 | 0.11 |
| `flops` (complexity baseline) | -0.06 | 0.16 | -0.05 | — | 0.00 | -0.20 | 0.04 | -0.02 | 0.02 |
| `nwot` | -0.07 | 0.37 | -0.08 | -0.05 | -0.01 | -0.24 | 0.05 | -0.06 | 0.03 |
| `swap` | -0.09 | 0.63 | -0.08 | -0.06 | 0.03 | -0.22 | -0.02 | -0.10 | 0.09 |
| `synflow_all` | -0.20 | 0.07 | -0.20 | -0.20 | 0.02 | -0.29 | -0.30 | -0.14 | -0.01 |
| `snip_all` | -0.41 | 0.25 | -0.42 | -0.42 | -0.41 | -0.39 | -0.44 | -0.49 | 0.22 |
| `grad_norm_all` | -0.47 | 0.26 | -0.47 | -0.47 | -0.43 | -0.49 | -0.47 | -0.54 | 0.23 |
| `plain_all` | -0.49 | 0.21 | -0.50 | -0.50 | -0.50 | -0.48 | -0.48 | -0.54 | 0.25 |
| `fisher` | -0.53 | 0.19 | -0.54 | -0.53 | -0.46 | -0.58 | -0.55 | -0.59 | 0.23 |
