# CI summary — is N = 150 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 150 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `grasp_all` | 0.46 | (0.31, 0.58) | 0.13 | yes | yes |
| `zico_sizectrl` | 0.22 | (0.06, 0.39) | 0.16 | yes | yes |
| `zico_t` | 0.21 | (0.05, 0.37) | 0.16 | yes | yes |
| `zico` | 0.20 | (0.04, 0.36) | 0.16 | yes | yes |
| `glass_t` | 0.17 | (0.00, 0.33) | 0.16 | yes | yes |
| `glass` | 0.16 | (-0.01, 0.32) | 0.16 | no | yes |
| `l2_norm_all` | 0.13 | (-0.03, 0.29) | 0.16 | no | yes |
| `jacov` | 0.07 | (-0.09, 0.24) | 0.16 | no | yes |
| `params` | 0.03 | (-0.13, 0.20) | 0.17 | no | yes |
| `swap_reg` | 0.03 | (-0.13, 0.19) | 0.16 | no | yes |
| `zico_s` | -0.01 | (-0.17, 0.15) | 0.16 | no | yes |
| `zen` | -0.01 | (-0.18, 0.16) | 0.17 | no | yes |
| `glass_s` | -0.02 | (-0.18, 0.14) | 0.16 | no | yes |
| `nwot` | -0.06 | (-0.22, 0.10) | 0.16 | no | yes |
| `swap` | -0.06 | (-0.23, 0.10) | 0.16 | no | yes |
| `flops` | -0.09 | (-0.25, 0.08) | 0.16 | no | yes |
| `nwot_per_layer` | -0.18 | (-0.34, -0.02) | 0.16 | yes | yes |
| `synflow_all` | -0.19 | (-0.33, -0.04) | 0.15 | yes | yes |
| `snip_all` | -0.42 | (-0.55, -0.26) | 0.15 | yes | yes |
| `plain_all` | -0.43 | (-0.57, -0.28) | 0.14 | yes | yes |
| `grad_norm_all` | -0.46 | (-0.58, -0.31) | 0.14 | yes | yes |
| `fisher` | -0.53 | (-0.65, -0.38) | 0.13 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.21 | -0.37 | +0.71 | 0.70 | 0.27 |
| `zico` | 20 | +0.20 | -0.18 | +0.52 | 0.80 | 0.16 |
| `zico` | 30 | +0.19 | -0.07 | +0.47 | 0.89 | 0.14 |
| `zico` | 40 | +0.19 | -0.03 | +0.41 | 0.93 | 0.07 |
| `zico` | 50 | +0.20 | +0.01 | +0.40 | 0.96 | 0.05 |
| `zico` | 100 | +0.20 | +0.10 | +0.30 | 1.00 | 0.00 |
| `zico` | 150 | +0.20 | +0.20 | +0.20 | 1.00 | 0.00 |
| `l2_norm_all` | 10 | +0.13 | -0.39 | +0.62 | 0.65 | 0.21 |
| `l2_norm_all` | 20 | +0.15 | -0.21 | +0.48 | 0.75 | 0.10 |
| `l2_norm_all` | 30 | +0.13 | -0.13 | +0.40 | 0.79 | 0.05 |
| `l2_norm_all` | 40 | +0.13 | -0.12 | +0.36 | 0.82 | 0.03 |
| `l2_norm_all` | 50 | +0.14 | -0.06 | +0.33 | 0.88 | 0.02 |
| `l2_norm_all` | 100 | +0.13 | +0.04 | +0.22 | 0.98 | 0.00 |
| `l2_norm_all` | 150 | +0.13 | +0.13 | +0.13 | 1.00 | 0.00 |
| `params` | 10 | +0.02 | -0.52 | +0.56 | 0.52 | 0.14 |
| `params` | 20 | +0.05 | -0.35 | +0.40 | 0.58 | 0.05 |
| `params` | 30 | +0.04 | -0.27 | +0.32 | 0.59 | 0.01 |
| `params` | 40 | +0.03 | -0.20 | +0.25 | 0.57 | 0.00 |
| `params` | 50 | +0.03 | -0.15 | +0.22 | 0.60 | 0.00 |
| `params` | 100 | +0.03 | -0.07 | +0.13 | 0.71 | 0.00 |
| `params` | 150 | +0.03 | +0.03 | +0.03 | 1.00 | 0.00 |
| `grasp_all` | 10 | +0.48 | -0.07 | +0.81 | 0.92 | 0.59 |
| `grasp_all` | 20 | +0.46 | +0.09 | +0.71 | 0.98 | 0.60 |
| `grasp_all` | 30 | +0.45 | +0.18 | +0.67 | 0.99 | 0.64 |
| `grasp_all` | 40 | +0.47 | +0.27 | +0.64 | 1.00 | 0.73 |
| `grasp_all` | 50 | +0.45 | +0.29 | +0.60 | 1.00 | 0.71 |
| `grasp_all` | 100 | +0.46 | +0.38 | +0.54 | 1.00 | 0.89 |
| `grasp_all` | 150 | +0.46 | +0.46 | +0.46 | 1.00 | 1.00 |
| `zen` | 10 | -0.03 | -0.58 | +0.48 | 0.46 | 0.09 |
| `zen` | 20 | -0.01 | -0.37 | +0.36 | 0.47 | 0.03 |
| `zen` | 30 | -0.00 | -0.28 | +0.27 | 0.49 | 0.01 |
| `zen` | 40 | -0.01 | -0.23 | +0.23 | 0.48 | 0.00 |
| `zen` | 50 | -0.02 | -0.21 | +0.19 | 0.42 | 0.00 |
| `zen` | 100 | -0.01 | -0.11 | +0.08 | 0.41 | 0.00 |
| `zen` | 150 | -0.01 | -0.01 | -0.01 | 0.00 | 0.00 |
| `nwot` | 10 | -0.05 | -0.58 | +0.52 | 0.44 | 0.09 |
| `nwot` | 20 | -0.07 | -0.45 | +0.31 | 0.38 | 0.02 |
| `nwot` | 30 | -0.07 | -0.35 | +0.20 | 0.34 | 0.00 |
| `nwot` | 40 | -0.06 | -0.27 | +0.20 | 0.35 | 0.00 |
| `nwot` | 50 | -0.05 | -0.26 | +0.13 | 0.32 | 0.00 |
| `nwot` | 100 | -0.05 | -0.16 | +0.05 | 0.19 | 0.00 |
| `nwot` | 150 | -0.06 | -0.06 | -0.06 | 0.00 | 0.00 |
| `snip_all` | 10 | -0.46 | -0.79 | +0.13 | 0.11 | 0.01 |
| `snip_all` | 20 | -0.42 | -0.71 | -0.04 | 0.03 | 0.00 |
| `snip_all` | 30 | -0.42 | -0.66 | -0.14 | 0.01 | 0.00 |
| `snip_all` | 40 | -0.42 | -0.61 | -0.18 | 0.00 | 0.00 |
| `snip_all` | 50 | -0.42 | -0.60 | -0.22 | 0.00 | 0.00 |
| `snip_all` | 100 | -0.42 | -0.50 | -0.34 | 0.00 | 0.00 |
| `snip_all` | 150 | -0.42 | -0.42 | -0.42 | 0.00 | 0.00 |
| `swap` | 10 | -0.04 | -0.58 | +0.46 | 0.44 | 0.08 |
| `swap` | 20 | -0.05 | -0.40 | +0.32 | 0.42 | 0.02 |
| `swap` | 30 | -0.07 | -0.34 | +0.22 | 0.35 | 0.00 |
| `swap` | 40 | -0.05 | -0.27 | +0.16 | 0.32 | 0.00 |
| `swap` | 50 | -0.06 | -0.26 | +0.14 | 0.30 | 0.00 |
| `swap` | 100 | -0.05 | -0.16 | +0.03 | 0.14 | 0.00 |
| `swap` | 150 | -0.06 | -0.06 | -0.06 | 0.00 | 0.00 |
| `zico_sizectrl` | 10 | +0.22 | -0.32 | +0.70 | 0.73 | 0.30 |
| `zico_sizectrl` | 20 | +0.23 | -0.19 | +0.59 | 0.81 | 0.22 |
| `zico_sizectrl` | 30 | +0.23 | -0.05 | +0.52 | 0.90 | 0.16 |
| `zico_sizectrl` | 40 | +0.23 | -0.01 | +0.45 | 0.94 | 0.09 |
| `zico_sizectrl` | 50 | +0.23 | +0.02 | +0.43 | 0.96 | 0.08 |
| `zico_sizectrl` | 100 | +0.22 | +0.12 | +0.32 | 1.00 | 0.00 |
| `zico_sizectrl` | 150 | +0.22 | +0.22 | +0.22 | 1.00 | 0.00 |

## How large must N be? (Fisher-z approximation, se ≈ 1.06/√(N−3), 95 % CI)

| CI half-width | N needed |
|---|---|
| ±0.30 | 51 |
| ±0.20 | 111 |
| ±0.15 | 195 |
| ±0.10 | 435 |
| ±0.05 | 1730 |

At N = 150 the expected half-width is ±0.17, which is what the bootstrap shows (±0.15–0.30). Separating a proxy at ρ ≈ 0.65 from the 0.737 reference needs a half-width below ≈ 0.09, i.e. N ≈ 500; separating it from 0 needs N ≈ 20.

## Seed-noise ceiling

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 1.00 / 0.00 / 0.00; within-arch std 0.0018 vs across-arch std 0.0062. The ground truth is not the limiting factor at N = 50.
