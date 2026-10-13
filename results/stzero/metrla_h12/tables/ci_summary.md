# CI summary — is N = 150 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 150 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `grasp_all` | 0.47 | (0.33, 0.58) | 0.13 | yes | yes |
| `jacov` | 0.07 | (-0.10, 0.24) | 0.17 | no | yes |
| `zico_sizectrl` | 0.06 | (-0.10, 0.22) | 0.16 | no | yes |
| `swap_reg` | 0.05 | (-0.11, 0.21) | 0.16 | no | yes |
| `zico` | 0.01 | (-0.14, 0.16) | 0.15 | no | yes |
| `l2_norm_all` | -0.00 | (-0.16, 0.16) | 0.16 | no | yes |
| `params` | -0.04 | (-0.20, 0.12) | 0.16 | no | yes |
| `zen` | -0.05 | (-0.21, 0.11) | 0.16 | no | yes |
| `flops` | -0.06 | (-0.21, 0.10) | 0.16 | no | yes |
| `nwot` | -0.07 | (-0.24, 0.09) | 0.16 | no | yes |
| `swap` | -0.09 | (-0.25, 0.06) | 0.15 | no | yes |
| `synflow_all` | -0.20 | (-0.35, -0.04) | 0.15 | yes | yes |
| `snip_all` | -0.41 | (-0.53, -0.26) | 0.14 | yes | yes |
| `grad_norm_all` | -0.47 | (-0.58, -0.32) | 0.13 | yes | yes |
| `plain_all` | -0.49 | (-0.61, -0.36) | 0.12 | yes | yes |
| `fisher` | -0.53 | (-0.64, -0.40) | 0.12 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.01 | -0.54 | +0.54 | 0.52 | 0.12 |
| `zico` | 20 | +0.02 | -0.34 | +0.36 | 0.53 | 0.03 |
| `zico` | 30 | +0.01 | -0.24 | +0.28 | 0.52 | 0.01 |
| `zico` | 40 | +0.01 | -0.21 | +0.22 | 0.53 | 0.00 |
| `zico` | 50 | +0.01 | -0.19 | +0.20 | 0.55 | 0.00 |
| `zico` | 100 | +0.01 | -0.09 | +0.11 | 0.57 | 0.00 |
| `zico` | 150 | +0.01 | +0.01 | +0.01 | 1.00 | 0.00 |
| `l2_norm_all` | 10 | -0.01 | -0.53 | +0.54 | 0.50 | 0.11 |
| `l2_norm_all` | 20 | +0.01 | -0.36 | +0.37 | 0.51 | 0.04 |
| `l2_norm_all` | 30 | -0.01 | -0.27 | +0.26 | 0.48 | 0.00 |
| `l2_norm_all` | 40 | -0.01 | -0.25 | +0.22 | 0.48 | 0.00 |
| `l2_norm_all` | 50 | +0.01 | -0.18 | +0.19 | 0.54 | 0.00 |
| `l2_norm_all` | 100 | -0.00 | -0.10 | +0.09 | 0.49 | 0.00 |
| `l2_norm_all` | 150 | -0.00 | -0.00 | -0.00 | 0.00 | 0.00 |
| `params` | 10 | -0.02 | -0.58 | +0.50 | 0.47 | 0.09 |
| `params` | 20 | -0.04 | -0.40 | +0.30 | 0.44 | 0.02 |
| `params` | 30 | -0.04 | -0.32 | +0.23 | 0.43 | 0.01 |
| `params` | 40 | -0.05 | -0.29 | +0.16 | 0.36 | 0.00 |
| `params` | 50 | -0.04 | -0.21 | +0.13 | 0.35 | 0.00 |
| `params` | 100 | -0.05 | -0.14 | +0.05 | 0.22 | 0.00 |
| `params` | 150 | -0.04 | -0.04 | -0.04 | 0.00 | 0.00 |
| `grasp_all` | 10 | +0.47 | -0.15 | +0.79 | 0.92 | 0.61 |
| `grasp_all` | 20 | +0.45 | +0.14 | +0.68 | 0.99 | 0.62 |
| `grasp_all` | 30 | +0.47 | +0.20 | +0.65 | 1.00 | 0.67 |
| `grasp_all` | 40 | +0.48 | +0.28 | +0.63 | 1.00 | 0.77 |
| `grasp_all` | 50 | +0.47 | +0.31 | +0.59 | 1.00 | 0.79 |
| `grasp_all` | 100 | +0.47 | +0.39 | +0.54 | 1.00 | 0.93 |
| `grasp_all` | 150 | +0.47 | +0.47 | +0.47 | 1.00 | 1.00 |
| `zen` | 10 | -0.07 | -0.58 | +0.48 | 0.41 | 0.07 |
| `zen` | 20 | -0.05 | -0.40 | +0.27 | 0.41 | 0.01 |
| `zen` | 30 | -0.04 | -0.31 | +0.24 | 0.40 | 0.00 |
| `zen` | 40 | -0.05 | -0.26 | +0.20 | 0.38 | 0.00 |
| `zen` | 50 | -0.05 | -0.23 | +0.14 | 0.37 | 0.00 |
| `zen` | 100 | -0.05 | -0.14 | +0.05 | 0.17 | 0.00 |
| `zen` | 150 | -0.05 | -0.05 | -0.05 | 0.00 | 0.00 |
| `nwot` | 10 | -0.07 | -0.56 | +0.52 | 0.44 | 0.11 |
| `nwot` | 20 | -0.08 | -0.45 | +0.29 | 0.35 | 0.02 |
| `nwot` | 30 | -0.09 | -0.39 | +0.21 | 0.33 | 0.01 |
| `nwot` | 40 | -0.07 | -0.31 | +0.16 | 0.30 | 0.00 |
| `nwot` | 50 | -0.08 | -0.28 | +0.11 | 0.26 | 0.00 |
| `nwot` | 100 | -0.06 | -0.17 | +0.04 | 0.12 | 0.00 |
| `nwot` | 150 | -0.07 | -0.07 | -0.07 | 0.00 | 0.00 |
| `snip_all` | 10 | -0.44 | -0.79 | +0.13 | 0.10 | 0.01 |
| `snip_all` | 20 | -0.40 | -0.65 | -0.04 | 0.03 | 0.00 |
| `snip_all` | 30 | -0.41 | -0.62 | -0.15 | 0.01 | 0.00 |
| `snip_all` | 40 | -0.41 | -0.59 | -0.19 | 0.00 | 0.00 |
| `snip_all` | 50 | -0.41 | -0.57 | -0.22 | 0.00 | 0.00 |
| `snip_all` | 100 | -0.41 | -0.49 | -0.33 | 0.00 | 0.00 |
| `snip_all` | 150 | -0.41 | -0.41 | -0.41 | 0.00 | 0.00 |
| `swap` | 10 | -0.04 | -0.58 | +0.44 | 0.43 | 0.07 |
| `swap` | 20 | -0.07 | -0.42 | +0.30 | 0.38 | 0.02 |
| `swap` | 30 | -0.09 | -0.36 | +0.18 | 0.27 | 0.00 |
| `swap` | 40 | -0.08 | -0.29 | +0.13 | 0.28 | 0.00 |
| `swap` | 50 | -0.09 | -0.27 | +0.12 | 0.23 | 0.00 |
| `swap` | 100 | -0.09 | -0.19 | +0.00 | 0.06 | 0.00 |
| `swap` | 150 | -0.09 | -0.09 | -0.09 | 0.00 | 0.00 |
| `zico_sizectrl` | 10 | +0.06 | -0.47 | +0.54 | 0.57 | 0.14 |
| `zico_sizectrl` | 20 | +0.07 | -0.35 | +0.43 | 0.59 | 0.07 |
| `zico_sizectrl` | 30 | +0.05 | -0.24 | +0.34 | 0.63 | 0.02 |
| `zico_sizectrl` | 40 | +0.05 | -0.15 | +0.27 | 0.69 | 0.01 |
| `zico_sizectrl` | 50 | +0.06 | -0.14 | +0.26 | 0.69 | 0.00 |
| `zico_sizectrl` | 100 | +0.06 | -0.04 | +0.15 | 0.80 | 0.00 |
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

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 0.60 / 0.90 / 0.70; within-arch std 0.0021 vs across-arch std 0.0123. The ground truth is not the limiting factor at N = 50.
