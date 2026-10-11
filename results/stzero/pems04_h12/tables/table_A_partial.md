# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=100) | mid third (n=100) | large third (n=100) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `zico` | 0.57 | 0.71 | 0.63 | 0.53 | 0.56 | 0.64 | 0.65 | 0.53 | 0.46 |
| `l2_norm_all` | 0.50 | 0.75 | 0.55 | 0.44 | 0.48 | 0.54 | 0.62 | 0.46 | 0.46 |
| `nwot` | 0.34 | 0.31 | 0.28 | 0.11 | 0.26 | 0.29 | 0.36 | 0.30 | 0.36 |
| `flops` (complexity baseline) | 0.31 | 0.10 | 0.29 | — | 0.22 | 0.30 | 0.35 | 0.27 | 0.36 |
| `params` (complexity baseline) | 0.19 | 1.00 | — | 0.17 | 0.13 | 0.21 | 0.12 | 0.19 | 0.15 |
| `synflow_all` | 0.19 | 0.00 | 0.19 | 0.01 | 0.10 | 0.21 | 0.27 | 0.14 | 0.28 |
| `grasp_all` | 0.17 | -0.09 | 0.20 | 0.20 | 0.28 | 0.20 | 0.10 | 0.29 | -0.21 |
| `zen` | 0.12 | 0.89 | -0.15 | 0.08 | 0.05 | -0.02 | -0.07 | 0.12 | 0.08 |
| `fisher` | -0.08 | 0.11 | -0.11 | -0.12 | -0.18 | -0.17 | 0.02 | -0.23 | 0.32 |
| `plain_all` | -0.09 | 0.09 | -0.11 | -0.13 | -0.22 | -0.15 | 0.04 | -0.24 | 0.34 |
| `grad_norm_all` | -0.13 | 0.23 | -0.18 | -0.14 | -0.20 | -0.25 | -0.06 | -0.23 | 0.19 |
| `snip_all` | -0.14 | 0.27 | -0.20 | -0.14 | -0.17 | -0.30 | -0.08 | -0.22 | 0.13 |
| `jacov` | -0.29 | 0.13 | -0.32 | -0.13 | -0.18 | -0.42 | -0.30 | -0.25 | -0.32 |
