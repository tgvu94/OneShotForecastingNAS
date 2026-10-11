# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=50) | mid third (n=50) | large third (n=50) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `grasp_all` | 0.47 | -0.19 | 0.50 | 0.47 | 0.34 | 0.64 | 0.51 | 0.42 | 0.39 |
| `zico` | 0.32 | 0.68 | 0.35 | 0.33 | 0.32 | 0.32 | 0.38 | 0.30 | 0.18 |
| `l2_norm_all` | 0.25 | 0.77 | 0.30 | 0.27 | 0.27 | 0.29 | 0.34 | 0.26 | 0.07 |
| `params` (complexity baseline) | 0.10 | 1.00 | — | 0.10 | 0.03 | 0.19 | -0.01 | 0.06 | 0.05 |
| `nwot` | 0.05 | 0.37 | 0.01 | 0.10 | -0.06 | 0.09 | 0.06 | 0.13 | -0.11 |
| `zen` | 0.00 | 0.86 | -0.14 | 0.01 | -0.16 | -0.07 | -0.01 | -0.02 | -0.02 |
| `flops` (complexity baseline) | 0.00 | 0.21 | -0.03 | — | -0.14 | 0.13 | -0.01 | 0.08 | -0.12 |
| `synflow_all` | -0.01 | 0.02 | -0.01 | -0.00 | 0.10 | -0.05 | -0.09 | 0.01 | -0.07 |
| `jacov` | -0.10 | 0.16 | -0.12 | -0.11 | -0.06 | -0.21 | -0.10 | -0.18 | -0.03 |
| `snip_all` | -0.36 | 0.39 | -0.44 | -0.36 | -0.24 | -0.57 | -0.46 | -0.34 | -0.31 |
| `grad_norm_all` | -0.40 | 0.35 | -0.47 | -0.40 | -0.29 | -0.61 | -0.46 | -0.37 | -0.34 |
| `fisher` | -0.44 | 0.20 | -0.47 | -0.44 | -0.36 | -0.61 | -0.45 | -0.42 | -0.37 |
| `plain_all` | -0.47 | 0.13 | -0.48 | -0.47 | -0.35 | -0.64 | -0.45 | -0.44 | -0.41 |
