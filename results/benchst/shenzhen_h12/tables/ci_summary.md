# CI summary — is N = 150 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 150 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `grasp_all` | 0.46 | (0.32, 0.58) | 0.13 | yes | yes |
| `zico_t` | 0.41 | (0.27, 0.54) | 0.14 | yes | yes |
| `glass_t` | 0.41 | (0.26, 0.54) | 0.14 | yes | yes |
| `zico` | 0.39 | (0.24, 0.52) | 0.14 | yes | yes |
| `glass` | 0.39 | (0.24, 0.53) | 0.14 | yes | yes |
| `zico_sizectrl` | 0.33 | (0.17, 0.48) | 0.16 | yes | yes |
| `l2_norm_all` | 0.27 | (0.11, 0.42) | 0.15 | yes | yes |
| `params` | 0.19 | (0.03, 0.34) | 0.16 | yes | yes |
| `zen` | 0.09 | (-0.08, 0.25) | 0.17 | no | yes |
| `jacov` | 0.06 | (-0.11, 0.21) | 0.16 | no | yes |
| `swap_reg` | 0.04 | (-0.12, 0.20) | 0.16 | no | yes |
| `swap` | -0.03 | (-0.20, 0.14) | 0.17 | no | yes |
| `nwot` | -0.05 | (-0.22, 0.12) | 0.17 | no | yes |
| `glass_s` | -0.06 | (-0.22, 0.11) | 0.16 | no | yes |
| `zico_s` | -0.06 | (-0.22, 0.11) | 0.16 | no | yes |
| `flops` | -0.07 | (-0.24, 0.11) | 0.17 | no | yes |
| `synflow_all` | -0.16 | (-0.31, 0.00) | 0.16 | no | yes |
| `nwot_per_layer` | -0.29 | (-0.44, -0.13) | 0.16 | yes | yes |
| `snip_all` | -0.32 | (-0.47, -0.16) | 0.15 | yes | yes |
| `plain_all` | -0.36 | (-0.50, -0.21) | 0.15 | yes | yes |
| `grad_norm_all` | -0.38 | (-0.50, -0.24) | 0.13 | yes | yes |
| `fisher` | -0.39 | (-0.53, -0.24) | 0.14 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.36 | -0.15 | +0.81 | 0.88 | 0.44 |
| `zico` | 20 | +0.38 | +0.02 | +0.66 | 0.96 | 0.47 |
| `zico` | 30 | +0.40 | +0.15 | +0.60 | 1.00 | 0.49 |
| `zico` | 40 | +0.39 | +0.18 | +0.55 | 1.00 | 0.47 |
| `zico` | 50 | +0.39 | +0.23 | +0.54 | 1.00 | 0.48 |
| `zico` | 100 | +0.39 | +0.31 | +0.47 | 1.00 | 0.43 |
| `zico` | 150 | +0.39 | +0.39 | +0.39 | 1.00 | 0.00 |
| `l2_norm_all` | 10 | +0.30 | -0.31 | +0.72 | 0.80 | 0.35 |
| `l2_norm_all` | 20 | +0.28 | -0.09 | +0.57 | 0.90 | 0.26 |
| `l2_norm_all` | 30 | +0.26 | +0.00 | +0.50 | 0.96 | 0.18 |
| `l2_norm_all` | 40 | +0.27 | +0.05 | +0.47 | 0.98 | 0.14 |
| `l2_norm_all` | 50 | +0.28 | +0.07 | +0.45 | 0.98 | 0.12 |
| `l2_norm_all` | 100 | +0.27 | +0.19 | +0.36 | 1.00 | 0.00 |
| `l2_norm_all` | 150 | +0.27 | +0.27 | +0.27 | 1.00 | 0.00 |
| `params` | 10 | +0.18 | -0.36 | +0.61 | 0.69 | 0.23 |
| `params` | 20 | +0.18 | -0.16 | +0.50 | 0.80 | 0.12 |
| `params` | 30 | +0.18 | -0.10 | +0.44 | 0.85 | 0.09 |
| `params` | 40 | +0.18 | -0.05 | +0.39 | 0.90 | 0.04 |
| `params` | 50 | +0.18 | -0.00 | +0.37 | 0.95 | 0.04 |
| `params` | 100 | +0.19 | +0.10 | +0.28 | 1.00 | 0.00 |
| `params` | 150 | +0.19 | +0.19 | +0.19 | 1.00 | 0.00 |
| `grasp_all` | 10 | +0.44 | -0.08 | +0.82 | 0.91 | 0.56 |
| `grasp_all` | 20 | +0.45 | +0.12 | +0.68 | 0.98 | 0.61 |
| `grasp_all` | 30 | +0.45 | +0.18 | +0.66 | 1.00 | 0.64 |
| `grasp_all` | 40 | +0.46 | +0.27 | +0.64 | 1.00 | 0.71 |
| `grasp_all` | 50 | +0.45 | +0.28 | +0.61 | 1.00 | 0.69 |
| `grasp_all` | 100 | +0.46 | +0.38 | +0.53 | 1.00 | 0.89 |
| `grasp_all` | 150 | +0.46 | +0.46 | +0.46 | 1.00 | 1.00 |
| `zen` | 10 | +0.07 | -0.46 | +0.56 | 0.57 | 0.17 |
| `zen` | 20 | +0.08 | -0.28 | +0.44 | 0.65 | 0.07 |
| `zen` | 30 | +0.09 | -0.17 | +0.33 | 0.72 | 0.03 |
| `zen` | 40 | +0.08 | -0.14 | +0.34 | 0.74 | 0.02 |
| `zen` | 50 | +0.09 | -0.10 | +0.28 | 0.75 | 0.00 |
| `zen` | 100 | +0.09 | +0.00 | +0.19 | 0.95 | 0.00 |
| `zen` | 150 | +0.09 | +0.09 | +0.09 | 1.00 | 0.00 |
| `nwot` | 10 | -0.05 | -0.59 | +0.55 | 0.45 | 0.09 |
| `nwot` | 20 | -0.06 | -0.40 | +0.31 | 0.39 | 0.02 |
| `nwot` | 30 | -0.07 | -0.37 | +0.21 | 0.35 | 0.00 |
| `nwot` | 40 | -0.05 | -0.30 | +0.19 | 0.36 | 0.00 |
| `nwot` | 50 | -0.05 | -0.24 | +0.16 | 0.33 | 0.00 |
| `nwot` | 100 | -0.05 | -0.15 | +0.06 | 0.23 | 0.00 |
| `nwot` | 150 | -0.05 | -0.05 | -0.05 | 0.00 | 0.00 |
| `snip_all` | 10 | -0.35 | -0.75 | +0.21 | 0.19 | 0.02 |
| `snip_all` | 20 | -0.31 | -0.62 | +0.08 | 0.10 | 0.00 |
| `snip_all` | 30 | -0.31 | -0.55 | -0.04 | 0.03 | 0.00 |
| `snip_all` | 40 | -0.31 | -0.52 | -0.09 | 0.01 | 0.00 |
| `snip_all` | 50 | -0.32 | -0.52 | -0.13 | 0.00 | 0.00 |
| `snip_all` | 100 | -0.32 | -0.41 | -0.23 | 0.00 | 0.00 |
| `snip_all` | 150 | -0.32 | -0.32 | -0.32 | 0.00 | 0.00 |
| `swap` | 10 | -0.02 | -0.56 | +0.50 | 0.46 | 0.09 |
| `swap` | 20 | -0.03 | -0.38 | +0.34 | 0.45 | 0.02 |
| `swap` | 30 | -0.05 | -0.32 | +0.23 | 0.40 | 0.01 |
| `swap` | 40 | -0.03 | -0.26 | +0.20 | 0.41 | 0.00 |
| `swap` | 50 | -0.03 | -0.22 | +0.16 | 0.39 | 0.00 |
| `swap` | 100 | -0.03 | -0.12 | +0.06 | 0.29 | 0.00 |
| `swap` | 150 | -0.03 | -0.03 | -0.03 | 0.00 | 0.00 |
| `zico_sizectrl` | 10 | +0.31 | -0.25 | +0.78 | 0.82 | 0.37 |
| `zico_sizectrl` | 20 | +0.34 | -0.09 | +0.68 | 0.89 | 0.40 |
| `zico_sizectrl` | 30 | +0.34 | +0.03 | +0.57 | 0.96 | 0.33 |
| `zico_sizectrl` | 40 | +0.34 | +0.07 | +0.54 | 0.98 | 0.32 |
| `zico_sizectrl` | 50 | +0.33 | +0.12 | +0.52 | 0.99 | 0.27 |
| `zico_sizectrl` | 100 | +0.33 | +0.23 | +0.42 | 1.00 | 0.09 |
| `zico_sizectrl` | 150 | +0.33 | +0.33 | +0.33 | 1.00 | 0.00 |

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

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 0.50 / 0.40 / 0.70; within-arch std 0.0011 vs across-arch std 0.0041. The ground truth is not the limiting factor at N = 50.
