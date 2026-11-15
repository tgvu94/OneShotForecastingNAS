# CI summary — is N = 150 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 150 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `zico` | 0.64 | (0.53, 0.72) | 0.10 | yes | yes |
| `glass` | 0.63 | (0.53, 0.72) | 0.10 | yes | yes |
| `zico_sizectrl` | 0.61 | (0.49, 0.71) | 0.11 | yes | yes |
| `l2_norm_all` | 0.60 | (0.50, 0.70) | 0.10 | yes | yes |
| `zico_t` | 0.60 | (0.49, 0.69) | 0.10 | yes | yes |
| `glass_t` | 0.60 | (0.49, 0.69) | 0.10 | yes | yes |
| `zico_s` | 0.29 | (0.14, 0.44) | 0.15 | yes | yes |
| `glass_s` | 0.29 | (0.14, 0.44) | 0.15 | yes | yes |
| `nwot` | 0.27 | (0.12, 0.41) | 0.15 | yes | yes |
| `params` | 0.27 | (0.12, 0.41) | 0.14 | yes | yes |
| `flops` | 0.24 | (0.08, 0.40) | 0.16 | yes | yes |
| `grasp_all` | 0.17 | (0.01, 0.31) | 0.15 | yes | yes |
| `swap` | 0.16 | (0.00, 0.30) | 0.15 | yes | yes |
| `synflow_all` | 0.13 | (-0.03, 0.29) | 0.16 | no | yes |
| `zen` | 0.12 | (-0.03, 0.26) | 0.15 | no | yes |
| `swap_reg` | 0.08 | (-0.08, 0.25) | 0.16 | no | yes |
| `plain_all` | -0.05 | (-0.20, 0.11) | 0.15 | no | yes |
| `fisher` | -0.10 | (-0.25, 0.06) | 0.15 | no | yes |
| `grad_norm_all` | -0.13 | (-0.28, 0.03) | 0.16 | no | yes |
| `snip_all` | -0.15 | (-0.30, 0.02) | 0.16 | no | yes |
| `jacov` | -0.23 | (-0.39, -0.07) | 0.16 | yes | yes |
| `nwot_per_layer` | -0.45 | (-0.57, -0.31) | 0.13 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.62 | +0.23 | +0.88 | 0.99 | 0.82 |
| `zico` | 20 | +0.62 | +0.36 | +0.81 | 1.00 | 0.92 |
| `zico` | 30 | +0.64 | +0.44 | +0.78 | 1.00 | 0.97 |
| `zico` | 40 | +0.64 | +0.46 | +0.75 | 1.00 | 0.99 |
| `zico` | 50 | +0.63 | +0.52 | +0.75 | 1.00 | 1.00 |
| `zico` | 100 | +0.64 | +0.57 | +0.69 | 1.00 | 1.00 |
| `zico` | 150 | +0.64 | +0.64 | +0.64 | 1.00 | 1.00 |
| `l2_norm_all` | 10 | +0.59 | +0.10 | +0.88 | 0.97 | 0.77 |
| `l2_norm_all` | 20 | +0.61 | +0.32 | +0.80 | 1.00 | 0.90 |
| `l2_norm_all` | 30 | +0.59 | +0.40 | +0.75 | 1.00 | 0.95 |
| `l2_norm_all` | 40 | +0.60 | +0.43 | +0.73 | 1.00 | 0.97 |
| `l2_norm_all` | 50 | +0.61 | +0.47 | +0.72 | 1.00 | 0.99 |
| `l2_norm_all` | 100 | +0.60 | +0.54 | +0.66 | 1.00 | 1.00 |
| `l2_norm_all` | 150 | +0.60 | +0.60 | +0.60 | 1.00 | 1.00 |
| `params` | 10 | +0.25 | -0.30 | +0.70 | 0.79 | 0.34 |
| `params` | 20 | +0.25 | -0.09 | +0.55 | 0.90 | 0.23 |
| `params` | 30 | +0.25 | -0.01 | +0.49 | 0.94 | 0.16 |
| `params` | 40 | +0.26 | +0.04 | +0.47 | 0.97 | 0.13 |
| `params` | 50 | +0.26 | +0.09 | +0.43 | 0.99 | 0.10 |
| `params` | 100 | +0.27 | +0.18 | +0.35 | 1.00 | 0.00 |
| `params` | 150 | +0.27 | +0.27 | +0.27 | 1.00 | 0.00 |
| `grasp_all` | 10 | +0.16 | -0.33 | +0.65 | 0.71 | 0.23 |
| `grasp_all` | 20 | +0.16 | -0.19 | +0.49 | 0.77 | 0.12 |
| `grasp_all` | 30 | +0.16 | -0.11 | +0.44 | 0.84 | 0.07 |
| `grasp_all` | 40 | +0.17 | -0.05 | +0.39 | 0.91 | 0.04 |
| `grasp_all` | 50 | +0.16 | -0.01 | +0.33 | 0.93 | 0.02 |
| `grasp_all` | 100 | +0.17 | +0.08 | +0.26 | 1.00 | 0.00 |
| `grasp_all` | 150 | +0.17 | +0.17 | +0.17 | 1.00 | 0.00 |
| `zen` | 10 | +0.12 | -0.41 | +0.64 | 0.65 | 0.18 |
| `zen` | 20 | +0.11 | -0.20 | +0.45 | 0.70 | 0.09 |
| `zen` | 30 | +0.13 | -0.13 | +0.35 | 0.81 | 0.02 |
| `zen` | 40 | +0.12 | -0.09 | +0.33 | 0.80 | 0.02 |
| `zen` | 50 | +0.12 | -0.07 | +0.29 | 0.86 | 0.00 |
| `zen` | 100 | +0.12 | +0.03 | +0.21 | 0.97 | 0.00 |
| `zen` | 150 | +0.12 | +0.12 | +0.12 | 1.00 | 0.00 |
| `nwot` | 10 | +0.24 | -0.29 | +0.72 | 0.76 | 0.32 |
| `nwot` | 20 | +0.26 | -0.10 | +0.57 | 0.88 | 0.25 |
| `nwot` | 30 | +0.25 | -0.04 | +0.51 | 0.92 | 0.18 |
| `nwot` | 40 | +0.28 | +0.04 | +0.47 | 0.97 | 0.16 |
| `nwot` | 50 | +0.26 | +0.08 | +0.44 | 0.99 | 0.11 |
| `nwot` | 100 | +0.27 | +0.18 | +0.37 | 1.00 | 0.01 |
| `nwot` | 150 | +0.27 | +0.27 | +0.27 | 1.00 | 0.00 |
| `snip_all` | 10 | -0.14 | -0.65 | +0.43 | 0.34 | 0.06 |
| `snip_all` | 20 | -0.13 | -0.48 | +0.22 | 0.26 | 0.00 |
| `snip_all` | 30 | -0.15 | -0.42 | +0.14 | 0.20 | 0.00 |
| `snip_all` | 40 | -0.14 | -0.39 | +0.07 | 0.15 | 0.00 |
| `snip_all` | 50 | -0.14 | -0.35 | +0.06 | 0.14 | 0.00 |
| `snip_all` | 100 | -0.14 | -0.24 | -0.06 | 0.00 | 0.00 |
| `snip_all` | 150 | -0.15 | -0.15 | -0.15 | 0.00 | 0.00 |
| `swap` | 10 | +0.15 | -0.41 | +0.62 | 0.67 | 0.22 |
| `swap` | 20 | +0.14 | -0.17 | +0.48 | 0.77 | 0.12 |
| `swap` | 30 | +0.17 | -0.13 | +0.43 | 0.81 | 0.07 |
| `swap` | 40 | +0.16 | -0.07 | +0.37 | 0.86 | 0.03 |
| `swap` | 50 | +0.17 | -0.04 | +0.33 | 0.91 | 0.00 |
| `swap` | 100 | +0.16 | +0.05 | +0.25 | 1.00 | 0.00 |
| `swap` | 150 | +0.16 | +0.16 | +0.16 | 1.00 | 0.00 |
| `zico_sizectrl` | 10 | +0.58 | +0.12 | +0.89 | 0.97 | 0.75 |
| `zico_sizectrl` | 20 | +0.62 | +0.29 | +0.81 | 1.00 | 0.90 |
| `zico_sizectrl` | 30 | +0.62 | +0.41 | +0.78 | 1.00 | 0.96 |
| `zico_sizectrl` | 40 | +0.61 | +0.43 | +0.75 | 1.00 | 0.96 |
| `zico_sizectrl` | 50 | +0.61 | +0.46 | +0.74 | 1.00 | 0.98 |
| `zico_sizectrl` | 100 | +0.61 | +0.54 | +0.69 | 1.00 | 1.00 |
| `zico_sizectrl` | 150 | +0.61 | +0.61 | +0.61 | 1.00 | 1.00 |

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

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 1.00 / 1.00 / 1.00; within-arch std 0.0003 vs across-arch std 0.0025. The ground truth is not the limiting factor at N = 50.
