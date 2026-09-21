# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=17) | mid third (n=16) | large third (n=17) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `zico` | 0.71 | 0.79 | 0.56 | 0.71 | 0.30 | 0.68 | 0.62 | 0.70 | 0.76 |
| `l2_norm_all` | 0.59 | 0.85 | 0.37 | 0.64 | 0.13 | 0.18 | 0.66 | 0.57 | 0.64 |
| `params` (complexity baseline) | 0.51 | 1.00 | — | 0.51 | 0.05 | 0.22 | 0.23 | 0.50 | 0.51 |
| `grasp_all` | 0.30 | -0.12 | 0.47 | 0.31 | 0.25 | 0.34 | 0.69 | 0.31 | -0.01 |
| `zen` | 0.30 | 0.87 | -0.29 | 0.29 | -0.24 | -0.26 | 0.11 | 0.32 | 0.34 |
| `nwot` | 0.03 | 0.33 | -0.22 | 0.08 | 0.09 | -0.32 | -0.32 | 0.03 | 0.07 |
| `flops` (complexity baseline) | -0.03 | 0.13 | -0.10 | — | 0.15 | -0.26 | -0.25 | -0.05 | 0.00 |
| `synflow_all` | -0.10 | 0.05 | -0.11 | -0.11 | 0.08 | -0.32 | -0.18 | -0.12 | 0.00 |
| `jacov` | -0.15 | 0.10 | -0.24 | -0.20 | -0.15 | -0.30 | -0.11 | -0.10 | -0.15 |
| `plain_all` | -0.15 | 0.14 | -0.28 | -0.16 | -0.31 | -0.39 | -0.17 | -0.21 | 0.20 |
| `fisher` | -0.26 | 0.19 | -0.46 | -0.27 | -0.20 | -0.47 | -0.74 | -0.31 | 0.07 |
| `grad_norm_all` | -0.28 | 0.24 | -0.51 | -0.28 | -0.21 | -0.41 | -0.74 | -0.29 | 0.02 |
| `snip_all` | -0.29 | 0.23 | -0.52 | -0.29 | -0.20 | -0.41 | -0.78 | -0.29 | -0.02 |
