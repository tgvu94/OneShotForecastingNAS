# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=17) | mid third (n=16) | large third (n=17) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `grasp_all` | 0.43 | -0.16 | 0.42 | 0.44 | 0.48 | 0.51 | 0.32 | 0.43 | -0.06 |
| `nwot` | 0.05 | 0.37 | 0.04 | -0.00 | -0.27 | -0.04 | 0.30 | 0.02 | -0.11 |
| `flops` (complexity baseline) | 0.02 | 0.15 | 0.01 | — | -0.12 | -0.07 | 0.16 | 0.01 | -0.14 |
| `l2_norm_all` | 0.00 | 0.86 | 0.07 | 0.01 | -0.33 | -0.25 | 0.12 | -0.05 | -0.15 |
| `params` (complexity baseline) | -0.04 | 1.00 | — | -0.03 | -0.09 | -0.43 | -0.23 | -0.02 | -0.21 |
| `jacov` | -0.05 | 0.07 | -0.05 | -0.01 | 0.01 | 0.13 | -0.31 | -0.03 | -0.07 |
| `zen` | -0.05 | 0.89 | -0.02 | -0.05 | -0.35 | -0.15 | 0.10 | -0.02 | -0.13 |
| `zico` | -0.09 | 0.77 | -0.07 | -0.09 | -0.32 | -0.12 | -0.31 | -0.12 | -0.22 |
| `synflow_all` | -0.23 | 0.16 | -0.20 | -0.26 | -0.13 | -0.38 | -0.15 | -0.23 | -0.02 |
| `snip_all` | -0.39 | 0.31 | -0.39 | -0.39 | -0.45 | -0.49 | -0.28 | -0.39 | 0.03 |
| `grad_norm_all` | -0.44 | 0.34 | -0.44 | -0.44 | -0.47 | -0.49 | -0.34 | -0.44 | 0.01 |
| `plain_all` | -0.45 | 0.25 | -0.46 | -0.45 | -0.54 | -0.48 | -0.44 | -0.42 | 0.09 |
| `fisher` | -0.55 | 0.27 | -0.55 | -0.55 | -0.63 | -0.52 | -0.66 | -0.52 | 0.05 |
