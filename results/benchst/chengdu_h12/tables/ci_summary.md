# CI summary — is N = 150 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 150 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `zico_t` | 0.53 | (0.41, 0.64) | 0.12 | yes | yes |
| `glass_t` | 0.53 | (0.40, 0.64) | 0.12 | yes | yes |
| `zico` | 0.50 | (0.37, 0.61) | 0.12 | yes | yes |
| `glass` | 0.50 | (0.37, 0.61) | 0.12 | yes | yes |
| `zico_sizectrl` | 0.44 | (0.29, 0.57) | 0.14 | yes | yes |
| `l2_norm_all` | 0.25 | (0.10, 0.40) | 0.15 | yes | yes |
| `params` | 0.22 | (0.08, 0.36) | 0.14 | yes | yes |
| `grasp_all` | 0.22 | (0.06, 0.36) | 0.15 | yes | yes |
| `jacov` | 0.21 | (0.06, 0.37) | 0.15 | yes | yes |
| `zen` | 0.10 | (-0.06, 0.25) | 0.16 | no | yes |
| `synflow_all` | 0.03 | (-0.12, 0.18) | 0.15 | no | yes |
| `swap_reg` | -0.02 | (-0.19, 0.14) | 0.16 | no | yes |
| `plain_all` | -0.09 | (-0.25, 0.07) | 0.16 | no | yes |
| `swap` | -0.10 | (-0.26, 0.05) | 0.16 | no | yes |
| `fisher` | -0.13 | (-0.28, 0.03) | 0.16 | no | yes |
| `snip_all` | -0.14 | (-0.29, 0.02) | 0.16 | no | yes |
| `grad_norm_all` | -0.15 | (-0.30, 0.00) | 0.15 | no | yes |
| `nwot` | -0.20 | (-0.35, -0.05) | 0.15 | yes | yes |
| `glass_s` | -0.22 | (-0.37, -0.06) | 0.16 | yes | yes |
| `zico_s` | -0.23 | (-0.38, -0.07) | 0.15 | yes | yes |
| `flops` | -0.23 | (-0.38, -0.07) | 0.15 | yes | yes |
| `nwot_per_layer` | -0.33 | (-0.46, -0.18) | 0.14 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.52 | +0.08 | +0.84 | 0.97 | 0.64 |
| `zico` | 20 | +0.48 | +0.18 | +0.71 | 0.99 | 0.69 |
| `zico` | 30 | +0.50 | +0.26 | +0.67 | 1.00 | 0.79 |
| `zico` | 40 | +0.50 | +0.30 | +0.66 | 1.00 | 0.83 |
| `zico` | 50 | +0.50 | +0.35 | +0.62 | 1.00 | 0.90 |
| `zico` | 100 | +0.50 | +0.43 | +0.58 | 1.00 | 0.98 |
| `zico` | 150 | +0.50 | +0.50 | +0.50 | 1.00 | 1.00 |
| `l2_norm_all` | 10 | +0.25 | -0.35 | +0.71 | 0.79 | 0.31 |
| `l2_norm_all` | 20 | +0.26 | -0.11 | +0.55 | 0.88 | 0.24 |
| `l2_norm_all` | 30 | +0.25 | -0.01 | +0.48 | 0.95 | 0.16 |
| `l2_norm_all` | 40 | +0.26 | +0.04 | +0.44 | 0.98 | 0.12 |
| `l2_norm_all` | 50 | +0.25 | +0.06 | +0.43 | 0.99 | 0.09 |
| `l2_norm_all` | 100 | +0.25 | +0.17 | +0.34 | 1.00 | 0.00 |
| `l2_norm_all` | 150 | +0.25 | +0.25 | +0.25 | 1.00 | 0.00 |
| `params` | 10 | +0.19 | -0.38 | +0.62 | 0.73 | 0.25 |
| `params` | 20 | +0.24 | -0.11 | +0.54 | 0.88 | 0.19 |
| `params` | 30 | +0.21 | -0.02 | +0.49 | 0.93 | 0.13 |
| `params` | 40 | +0.22 | +0.01 | +0.42 | 0.96 | 0.07 |
| `params` | 50 | +0.21 | +0.05 | +0.39 | 0.98 | 0.04 |
| `params` | 100 | +0.22 | +0.13 | +0.31 | 1.00 | 0.00 |
| `params` | 150 | +0.22 | +0.22 | +0.22 | 1.00 | 0.00 |
| `grasp_all` | 10 | +0.24 | -0.32 | +0.68 | 0.75 | 0.32 |
| `grasp_all` | 20 | +0.22 | -0.17 | +0.53 | 0.82 | 0.18 |
| `grasp_all` | 30 | +0.21 | -0.07 | +0.46 | 0.90 | 0.11 |
| `grasp_all` | 40 | +0.22 | -0.00 | +0.43 | 0.95 | 0.10 |
| `grasp_all` | 50 | +0.21 | +0.02 | +0.40 | 0.97 | 0.05 |
| `grasp_all` | 100 | +0.22 | +0.13 | +0.31 | 1.00 | 0.00 |
| `grasp_all` | 150 | +0.22 | +0.22 | +0.22 | 1.00 | 0.00 |
| `zen` | 10 | +0.07 | -0.44 | +0.55 | 0.59 | 0.15 |
| `zen` | 20 | +0.10 | -0.25 | +0.44 | 0.67 | 0.08 |
| `zen` | 30 | +0.11 | -0.17 | +0.35 | 0.72 | 0.02 |
| `zen` | 40 | +0.10 | -0.14 | +0.31 | 0.76 | 0.01 |
| `zen` | 50 | +0.10 | -0.10 | +0.28 | 0.79 | 0.00 |
| `zen` | 100 | +0.10 | +0.01 | +0.19 | 0.96 | 0.00 |
| `zen` | 150 | +0.10 | +0.10 | +0.10 | 1.00 | 0.00 |
| `nwot` | 10 | -0.22 | -0.66 | +0.37 | 0.25 | 0.04 |
| `nwot` | 20 | -0.20 | -0.53 | +0.17 | 0.18 | 0.00 |
| `nwot` | 30 | -0.21 | -0.47 | +0.05 | 0.10 | 0.00 |
| `nwot` | 40 | -0.20 | -0.42 | +0.03 | 0.08 | 0.00 |
| `nwot` | 50 | -0.21 | -0.38 | -0.00 | 0.04 | 0.00 |
| `nwot` | 100 | -0.20 | -0.30 | -0.11 | 0.00 | 0.00 |
| `nwot` | 150 | -0.20 | -0.20 | -0.20 | 0.00 | 0.00 |
| `snip_all` | 10 | -0.15 | -0.68 | +0.42 | 0.34 | 0.05 |
| `snip_all` | 20 | -0.15 | -0.47 | +0.22 | 0.24 | 0.01 |
| `snip_all` | 30 | -0.14 | -0.38 | +0.14 | 0.21 | 0.00 |
| `snip_all` | 40 | -0.14 | -0.36 | +0.10 | 0.17 | 0.00 |
| `snip_all` | 50 | -0.13 | -0.32 | +0.06 | 0.13 | 0.00 |
| `snip_all` | 100 | -0.14 | -0.23 | -0.04 | 0.01 | 0.00 |
| `snip_all` | 150 | -0.14 | -0.14 | -0.14 | 0.00 | 0.00 |
| `swap` | 10 | -0.12 | -0.62 | +0.43 | 0.35 | 0.07 |
| `swap` | 20 | -0.08 | -0.45 | +0.25 | 0.34 | 0.01 |
| `swap` | 30 | -0.10 | -0.37 | +0.17 | 0.27 | 0.00 |
| `swap` | 40 | -0.09 | -0.32 | +0.13 | 0.22 | 0.00 |
| `swap` | 50 | -0.10 | -0.28 | +0.08 | 0.19 | 0.00 |
| `swap` | 100 | -0.10 | -0.19 | -0.01 | 0.04 | 0.00 |
| `swap` | 150 | -0.10 | -0.10 | -0.10 | 0.00 | 0.00 |
| `zico_sizectrl` | 10 | +0.43 | -0.13 | +0.81 | 0.91 | 0.54 |
| `zico_sizectrl` | 20 | +0.45 | +0.10 | +0.72 | 0.98 | 0.58 |
| `zico_sizectrl` | 30 | +0.44 | +0.19 | +0.66 | 1.00 | 0.61 |
| `zico_sizectrl` | 40 | +0.43 | +0.21 | +0.63 | 1.00 | 0.62 |
| `zico_sizectrl` | 50 | +0.44 | +0.27 | +0.60 | 1.00 | 0.64 |
| `zico_sizectrl` | 100 | +0.44 | +0.36 | +0.52 | 1.00 | 0.78 |
| `zico_sizectrl` | 150 | +0.44 | +0.44 | +0.44 | 1.00 | 1.00 |

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

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 0.70 / 0.70 / 1.00; within-arch std 0.0013 vs across-arch std 0.0038. The ground truth is not the limiting factor at N = 50.
