# Table A (partial) — is the correlation just parameter count?

All values are Spearman with −MAE (positive = useful), point estimates (CIs for the main column are in Table A). ρ(proxy, log params) says how size-like a proxy is; partial ρ removes rank(log params) or rank(log flops) from both proxy and target (rank-residual method); the tercile columns re-rank *within* a size band; the last two columns swap the target.

| Proxy | ρ (val MAE) | ρ(proxy, log params) | partial ρ \| log params | partial ρ \| log flops | small third (n=50) | mid third (n=50) | large third (n=50) | ρ (test MAE) | ρ (val MSE) |
|---|---|---|---|---|---|---|---|---|---|
| `zico` | 0.64 | 0.68 | 0.65 | 0.64 | 0.52 | 0.72 | 0.62 | 0.59 | 0.60 |
| `glass` | 0.63 | 0.69 | 0.65 | 0.63 | 0.51 | 0.72 | 0.62 | 0.59 | 0.61 |
| `zico_sizectrl` | 0.61 | 0.04 | 0.63 | 0.61 | 0.39 | 0.75 | 0.67 | 0.57 | 0.54 |
| `l2_norm_all` | 0.60 | 0.76 | 0.64 | 0.58 | 0.56 | 0.64 | 0.66 | 0.55 | 0.59 |
| `zico_t` | 0.60 | 0.68 | 0.59 | 0.62 | 0.45 | 0.68 | 0.55 | 0.56 | 0.56 |
| `glass_t` | 0.60 | 0.68 | 0.59 | 0.62 | 0.47 | 0.68 | 0.55 | 0.56 | 0.57 |
| `zico_s` | 0.29 | 0.02 | 0.31 | 0.20 | 0.11 | 0.27 | 0.55 | 0.23 | 0.30 |
| `glass_s` | 0.29 | 0.02 | 0.31 | 0.19 | 0.11 | 0.27 | 0.54 | 0.23 | 0.30 |
| `nwot` | 0.27 | 0.34 | 0.18 | 0.06 | 0.13 | 0.11 | 0.47 | 0.20 | 0.32 |
| `params` (complexity baseline) | 0.27 | 1.00 | — | 0.24 | 0.28 | 0.11 | -0.01 | 0.24 | 0.30 |
| `flops` (complexity baseline) | 0.24 | 0.14 | 0.19 | — | 0.08 | 0.16 | 0.48 | 0.18 | 0.29 |
| `grasp_all` | 0.17 | -0.13 | 0.20 | 0.17 | 0.01 | 0.14 | 0.35 | 0.27 | -0.28 |
| `swap` | 0.16 | 0.67 | -0.01 | -0.05 | 0.11 | -0.07 | 0.15 | 0.11 | 0.26 |
| `synflow_all` | 0.13 | 0.08 | 0.11 | 0.01 | 0.15 | 0.11 | 0.05 | 0.11 | 0.26 |
| `zen` | 0.12 | 0.85 | -0.24 | 0.11 | -0.05 | -0.15 | -0.17 | 0.12 | 0.17 |
| `swap_reg` | 0.08 | 0.17 | 0.05 | -0.01 | 0.25 | -0.06 | 0.08 | 0.07 | 0.06 |
| `plain_all` | -0.05 | 0.17 | -0.10 | -0.05 | 0.06 | 0.01 | -0.30 | -0.19 | 0.42 |
| `fisher` | -0.10 | 0.19 | -0.15 | -0.10 | 0.07 | -0.06 | -0.37 | -0.22 | 0.39 |
| `grad_norm_all` | -0.13 | 0.24 | -0.21 | -0.13 | 0.02 | -0.15 | -0.38 | -0.23 | 0.29 |
| `snip_all` | -0.15 | 0.24 | -0.22 | -0.13 | -0.01 | -0.18 | -0.37 | -0.23 | 0.23 |
| `jacov` | -0.23 | 0.05 | -0.25 | -0.13 | -0.20 | -0.22 | -0.36 | -0.18 | -0.25 |
| `nwot_per_layer` | -0.45 | -0.60 | -0.37 | -0.44 | -0.34 | -0.55 | -0.26 | -0.42 | -0.44 |
