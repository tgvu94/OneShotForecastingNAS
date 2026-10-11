# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=17) | mid third (n=16) | large third (n=17) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `zico` | 0.65 | 0.79 | 0.50 | 0.65 | 0.20 | 0.61 | 0.57 | 0.56 | 0.72 |
| `l2_norm_all` | 0.63 | 0.84 | 0.51 | 0.67 | 0.07 | 0.41 | 0.71 | 0.56 | 0.68 |
| `params` (complexity baseline) | 0.47 | 1.00 | — | 0.49 | 0.10 | -0.01 | 0.17 | 0.44 | 0.50 |
| `grasp_all` | 0.35 | -0.07 | 0.41 | 0.35 | 0.25 | 0.35 | 0.64 | 0.46 | -0.18 |
| `zen` | 0.33 | 0.89 | -0.20 | 0.33 | -0.14 | -0.28 | 0.12 | 0.32 | 0.40 |
| `nwot` | 0.17 | 0.34 | -0.04 | 0.25 | 0.06 | -0.04 | -0.04 | 0.18 | 0.18 |
| `flops` (complexity baseline) | 0.06 | 0.14 | -0.03 | — | 0.10 | -0.04 | -0.07 | 0.06 | 0.08 |
| `synflow_all` | -0.11 | 0.17 | -0.21 | -0.18 | -0.01 | -0.21 | -0.34 | -0.16 | 0.15 |
| `jacov` | -0.18 | 0.12 | -0.28 | -0.20 | -0.01 | -0.39 | -0.19 | -0.18 | -0.15 |
| `plain_all` | -0.21 | 0.18 | -0.31 | -0.22 | -0.31 | -0.43 | -0.32 | -0.33 | 0.39 |
| `grad_norm_all` | -0.25 | 0.28 | -0.44 | -0.25 | -0.10 | -0.39 | -0.65 | -0.36 | 0.21 |
| `snip_all` | -0.26 | 0.27 | -0.44 | -0.26 | -0.07 | -0.42 | -0.61 | -0.35 | 0.14 |
| `fisher` | -0.27 | 0.26 | -0.43 | -0.28 | -0.24 | -0.46 | -0.72 | -0.42 | 0.31 |
