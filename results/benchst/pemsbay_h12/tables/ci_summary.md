# CI summary — is N = 150 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 150 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `grasp_all` | 0.57 | (0.45, 0.66) | 0.10 | yes | yes |
| `zico_t` | 0.13 | (-0.03, 0.28) | 0.16 | no | yes |
| `zico` | 0.13 | (-0.03, 0.28) | 0.16 | no | yes |
| `l2_norm_all` | 0.12 | (-0.05, 0.28) | 0.16 | no | yes |
| `glass_t` | 0.10 | (-0.06, 0.25) | 0.16 | no | yes |
| `glass` | 0.09 | (-0.07, 0.25) | 0.16 | no | yes |
| `params` | 0.09 | (-0.08, 0.26) | 0.17 | no | yes |
| `swap_reg` | 0.09 | (-0.07, 0.23) | 0.15 | no | yes |
| `zico_sizectrl` | 0.06 | (-0.09, 0.22) | 0.16 | no | yes |
| `zico_s` | 0.04 | (-0.13, 0.19) | 0.16 | no | yes |
| `jacov` | 0.03 | (-0.13, 0.20) | 0.17 | no | yes |
| `glass_s` | 0.03 | (-0.14, 0.18) | 0.16 | no | yes |
| `zen` | 0.02 | (-0.15, 0.20) | 0.17 | no | yes |
| `nwot` | 0.02 | (-0.15, 0.18) | 0.16 | no | yes |
| `swap` | -0.00 | (-0.18, 0.17) | 0.17 | no | yes |
| `flops` | -0.01 | (-0.16, 0.15) | 0.15 | no | yes |
| `nwot_per_layer` | -0.10 | (-0.26, 0.07) | 0.17 | no | yes |
| `synflow_all` | -0.27 | (-0.41, -0.12) | 0.14 | yes | yes |
| `snip_all` | -0.51 | (-0.62, -0.37) | 0.12 | yes | yes |
| `grad_norm_all` | -0.55 | (-0.64, -0.42) | 0.11 | yes | yes |
| `fisher` | -0.63 | (-0.72, -0.51) | 0.11 | yes | yes |
| `plain_all` | -0.67 | (-0.74, -0.57) | 0.09 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.12 | -0.46 | +0.65 | 0.62 | 0.20 |
| `zico` | 20 | +0.12 | -0.25 | +0.44 | 0.70 | 0.09 |
| `zico` | 30 | +0.12 | -0.14 | +0.40 | 0.76 | 0.05 |
| `zico` | 40 | +0.13 | -0.09 | +0.33 | 0.81 | 0.02 |
| `zico` | 50 | +0.12 | -0.06 | +0.31 | 0.86 | 0.01 |
| `zico` | 100 | +0.13 | +0.03 | +0.22 | 0.99 | 0.00 |
| `zico` | 150 | +0.13 | +0.13 | +0.13 | 1.00 | 0.00 |
| `l2_norm_all` | 10 | +0.10 | -0.44 | +0.65 | 0.62 | 0.20 |
| `l2_norm_all` | 20 | +0.12 | -0.22 | +0.46 | 0.71 | 0.09 |
| `l2_norm_all` | 30 | +0.12 | -0.15 | +0.37 | 0.74 | 0.03 |
| `l2_norm_all` | 40 | +0.11 | -0.14 | +0.34 | 0.77 | 0.02 |
| `l2_norm_all` | 50 | +0.12 | -0.09 | +0.32 | 0.82 | 0.01 |
| `l2_norm_all` | 100 | +0.12 | +0.02 | +0.21 | 0.97 | 0.00 |
| `l2_norm_all` | 150 | +0.12 | +0.12 | +0.12 | 1.00 | 0.00 |
| `params` | 10 | +0.09 | -0.49 | +0.61 | 0.58 | 0.19 |
| `params` | 20 | +0.09 | -0.27 | +0.45 | 0.66 | 0.09 |
| `params` | 30 | +0.08 | -0.21 | +0.36 | 0.70 | 0.03 |
| `params` | 40 | +0.09 | -0.15 | +0.31 | 0.71 | 0.01 |
| `params` | 50 | +0.09 | -0.10 | +0.29 | 0.78 | 0.01 |
| `params` | 100 | +0.09 | -0.01 | +0.20 | 0.93 | 0.00 |
| `params` | 150 | +0.09 | +0.09 | +0.09 | 1.00 | 0.00 |
| `grasp_all` | 10 | +0.58 | +0.07 | +0.83 | 0.97 | 0.74 |
| `grasp_all` | 20 | +0.57 | +0.28 | +0.74 | 1.00 | 0.82 |
| `grasp_all` | 30 | +0.57 | +0.36 | +0.72 | 1.00 | 0.90 |
| `grasp_all` | 40 | +0.58 | +0.41 | +0.70 | 1.00 | 0.96 |
| `grasp_all` | 50 | +0.57 | +0.44 | +0.68 | 1.00 | 0.98 |
| `grasp_all` | 100 | +0.58 | +0.51 | +0.64 | 1.00 | 1.00 |
| `grasp_all` | 150 | +0.57 | +0.57 | +0.57 | 1.00 | 1.00 |
| `zen` | 10 | +0.02 | -0.55 | +0.53 | 0.52 | 0.11 |
| `zen` | 20 | +0.01 | -0.36 | +0.38 | 0.51 | 0.03 |
| `zen` | 30 | +0.04 | -0.27 | +0.32 | 0.56 | 0.01 |
| `zen` | 40 | +0.02 | -0.23 | +0.28 | 0.54 | 0.01 |
| `zen` | 50 | +0.02 | -0.18 | +0.21 | 0.55 | 0.00 |
| `zen` | 100 | +0.02 | -0.08 | +0.13 | 0.62 | 0.00 |
| `zen` | 150 | +0.02 | +0.02 | +0.02 | 1.00 | 0.00 |
| `nwot` | 10 | +0.01 | -0.52 | +0.59 | 0.52 | 0.15 |
| `nwot` | 20 | +0.03 | -0.37 | +0.41 | 0.54 | 0.05 |
| `nwot` | 30 | -0.00 | -0.29 | +0.27 | 0.49 | 0.01 |
| `nwot` | 40 | +0.01 | -0.21 | +0.26 | 0.53 | 0.01 |
| `nwot` | 50 | +0.02 | -0.18 | +0.21 | 0.56 | 0.00 |
| `nwot` | 100 | +0.02 | -0.07 | +0.12 | 0.65 | 0.00 |
| `nwot` | 150 | +0.02 | +0.02 | +0.02 | 1.00 | 0.00 |
| `snip_all` | 10 | -0.54 | -0.82 | -0.01 | 0.05 | 0.01 |
| `snip_all` | 20 | -0.49 | -0.72 | -0.17 | 0.02 | 0.00 |
| `snip_all` | 30 | -0.51 | -0.69 | -0.27 | 0.00 | 0.00 |
| `snip_all` | 40 | -0.50 | -0.68 | -0.32 | 0.00 | 0.00 |
| `snip_all` | 50 | -0.50 | -0.66 | -0.35 | 0.00 | 0.00 |
| `snip_all` | 100 | -0.51 | -0.58 | -0.43 | 0.00 | 0.00 |
| `snip_all` | 150 | -0.51 | -0.51 | -0.51 | 0.00 | 0.00 |
| `swap` | 10 | +0.01 | -0.56 | +0.54 | 0.51 | 0.12 |
| `swap` | 20 | -0.00 | -0.39 | +0.37 | 0.49 | 0.04 |
| `swap` | 30 | -0.02 | -0.29 | +0.28 | 0.46 | 0.01 |
| `swap` | 40 | +0.01 | -0.22 | +0.22 | 0.52 | 0.00 |
| `swap` | 50 | -0.00 | -0.21 | +0.20 | 0.49 | 0.00 |
| `swap` | 100 | -0.00 | -0.11 | +0.10 | 0.49 | 0.00 |
| `swap` | 150 | -0.00 | -0.00 | -0.00 | 0.00 | 0.00 |
| `zico_sizectrl` | 10 | +0.07 | -0.47 | +0.59 | 0.57 | 0.15 |
| `zico_sizectrl` | 20 | +0.07 | -0.33 | +0.44 | 0.62 | 0.07 |
| `zico_sizectrl` | 30 | +0.07 | -0.20 | +0.36 | 0.65 | 0.02 |
| `zico_sizectrl` | 40 | +0.06 | -0.17 | +0.28 | 0.67 | 0.01 |
| `zico_sizectrl` | 50 | +0.06 | -0.15 | +0.25 | 0.67 | 0.00 |
| `zico_sizectrl` | 100 | +0.06 | -0.04 | +0.16 | 0.84 | 0.00 |
| `zico_sizectrl` | 150 | +0.06 | +0.06 | +0.06 | 1.00 | 0.00 |

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

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 50 repeated archs: 0.84 / 0.85 / 0.91; within-arch std 0.0009 vs across-arch std 0.0062. The ground truth is not the limiting factor at N = 50.
