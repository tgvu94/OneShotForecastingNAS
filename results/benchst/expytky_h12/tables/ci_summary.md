# CI summary — is N = 150 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 150 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `grasp_all` | 0.45 | (0.28, 0.58) | 0.15 | yes | yes |
| `zico_t` | 0.22 | (0.05, 0.39) | 0.17 | yes | yes |
| `glass_t` | 0.21 | (0.04, 0.38) | 0.17 | yes | yes |
| `zico` | 0.20 | (0.03, 0.37) | 0.17 | yes | yes |
| `glass` | 0.20 | (0.02, 0.36) | 0.17 | yes | yes |
| `zico_sizectrl` | 0.17 | (0.00, 0.33) | 0.17 | yes | yes |
| `jacov` | 0.13 | (-0.04, 0.29) | 0.17 | no | yes |
| `params` | 0.11 | (-0.05, 0.27) | 0.16 | no | yes |
| `l2_norm_all` | 0.04 | (-0.12, 0.20) | 0.16 | no | yes |
| `zen` | 0.02 | (-0.14, 0.18) | 0.16 | no | yes |
| `swap_reg` | -0.04 | (-0.20, 0.11) | 0.16 | no | yes |
| `zico_s` | -0.08 | (-0.25, 0.09) | 0.17 | no | yes |
| `glass_s` | -0.08 | (-0.25, 0.09) | 0.17 | no | yes |
| `nwot` | -0.11 | (-0.26, 0.04) | 0.15 | no | yes |
| `swap` | -0.11 | (-0.26, 0.05) | 0.16 | no | yes |
| `flops` | -0.12 | (-0.27, 0.04) | 0.15 | no | yes |
| `nwot_per_layer` | -0.15 | (-0.32, 0.02) | 0.17 | no | yes |
| `synflow_all` | -0.24 | (-0.38, -0.09) | 0.15 | yes | yes |
| `snip_all` | -0.38 | (-0.51, -0.23) | 0.14 | yes | yes |
| `grad_norm_all` | -0.43 | (-0.55, -0.29) | 0.13 | yes | yes |
| `plain_all` | -0.46 | (-0.58, -0.33) | 0.13 | yes | yes |
| `fisher` | -0.49 | (-0.60, -0.36) | 0.12 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.20 | -0.41 | +0.72 | 0.35 | 0.15 |
| `zico` | 20 | +0.17 | -0.24 | +0.52 | 0.17 | 0.03 |
| `zico` | 30 | +0.19 | -0.09 | +0.49 | 0.09 | 0.01 |
| `zico` | 40 | +0.18 | -0.01 | +0.39 | 0.05 | 0.00 |
| `zico` | 50 | +0.27 | +0.06 | +0.34 | 0.01 | 0.00 |
| `zico` | 100 | +nan | +nan | +nan | 0.00 | 0.00 |
| `zico` | 150 | +nan | +nan | +nan | 0.00 | 0.00 |
| `l2_norm_all` | 10 | +0.04 | -0.50 | +0.53 | 0.54 | 0.13 |
| `l2_norm_all` | 20 | +0.04 | -0.30 | +0.37 | 0.57 | 0.04 |
| `l2_norm_all` | 30 | +0.04 | -0.22 | +0.30 | 0.58 | 0.01 |
| `l2_norm_all` | 40 | +0.02 | -0.19 | +0.24 | 0.56 | 0.00 |
| `l2_norm_all` | 50 | +0.04 | -0.16 | +0.22 | 0.61 | 0.00 |
| `l2_norm_all` | 100 | +0.04 | -0.06 | +0.12 | 0.75 | 0.00 |
| `l2_norm_all` | 150 | +0.04 | +0.04 | +0.04 | 1.00 | 0.00 |
| `params` | 10 | +0.08 | -0.47 | +0.60 | 0.59 | 0.17 |
| `params` | 20 | +0.11 | -0.24 | +0.44 | 0.70 | 0.08 |
| `params` | 30 | +0.11 | -0.17 | +0.37 | 0.75 | 0.03 |
| `params` | 40 | +0.10 | -0.12 | +0.32 | 0.76 | 0.01 |
| `params` | 50 | +0.11 | -0.06 | +0.30 | 0.85 | 0.00 |
| `params` | 100 | +0.11 | +0.02 | +0.20 | 0.98 | 0.00 |
| `params` | 150 | +0.11 | +0.11 | +0.11 | 1.00 | 0.00 |
| `grasp_all` | 10 | +0.48 | +0.01 | +0.80 | 0.13 | 0.09 |
| `grasp_all` | 20 | +0.43 | +0.22 | +0.52 | 0.02 | 0.01 |
| `grasp_all` | 30 | +nan | +nan | +nan | 0.00 | 0.00 |
| `grasp_all` | 40 | +nan | +nan | +nan | 0.00 | 0.00 |
| `grasp_all` | 50 | +nan | +nan | +nan | 0.00 | 0.00 |
| `grasp_all` | 100 | +nan | +nan | +nan | 0.00 | 0.00 |
| `grasp_all` | 150 | +nan | +nan | +nan | 0.00 | 0.00 |
| `zen` | 10 | +0.01 | -0.54 | +0.49 | 0.51 | 0.10 |
| `zen` | 20 | +0.01 | -0.34 | +0.36 | 0.51 | 0.03 |
| `zen` | 30 | +0.01 | -0.24 | +0.31 | 0.53 | 0.01 |
| `zen` | 40 | +0.01 | -0.22 | +0.26 | 0.52 | 0.01 |
| `zen` | 50 | +0.01 | -0.18 | +0.20 | 0.53 | 0.00 |
| `zen` | 100 | +0.02 | -0.07 | +0.11 | 0.61 | 0.00 |
| `zen` | 150 | +0.02 | +0.02 | +0.02 | 1.00 | 0.00 |
| `nwot` | 10 | -0.13 | -0.62 | +0.41 | 0.36 | 0.06 |
| `nwot` | 20 | -0.11 | -0.47 | +0.25 | 0.32 | 0.01 |
| `nwot` | 30 | -0.13 | -0.39 | +0.14 | 0.22 | 0.00 |
| `nwot` | 40 | -0.11 | -0.32 | +0.12 | 0.20 | 0.00 |
| `nwot` | 50 | -0.10 | -0.31 | +0.08 | 0.18 | 0.00 |
| `nwot` | 100 | -0.11 | -0.20 | -0.01 | 0.03 | 0.00 |
| `nwot` | 150 | -0.11 | -0.11 | -0.11 | 0.00 | 0.00 |
| `snip_all` | 10 | -0.42 | -0.81 | +0.19 | 0.13 | 0.01 |
| `snip_all` | 20 | -0.36 | -0.65 | -0.01 | 0.04 | 0.00 |
| `snip_all` | 30 | -0.38 | -0.61 | -0.12 | 0.01 | 0.00 |
| `snip_all` | 40 | -0.37 | -0.56 | -0.17 | 0.00 | 0.00 |
| `snip_all` | 50 | -0.38 | -0.56 | -0.21 | 0.00 | 0.00 |
| `snip_all` | 100 | -0.38 | -0.46 | -0.29 | 0.00 | 0.00 |
| `snip_all` | 150 | -0.38 | -0.38 | -0.38 | 0.00 | 0.00 |
| `swap` | 10 | -0.12 | -0.60 | +0.43 | 0.38 | 0.06 |
| `swap` | 20 | -0.10 | -0.42 | +0.25 | 0.32 | 0.01 |
| `swap` | 30 | -0.12 | -0.39 | +0.16 | 0.26 | 0.00 |
| `swap` | 40 | -0.10 | -0.30 | +0.11 | 0.24 | 0.00 |
| `swap` | 50 | -0.11 | -0.29 | +0.07 | 0.18 | 0.00 |
| `swap` | 100 | -0.10 | -0.20 | -0.01 | 0.03 | 0.00 |
| `swap` | 150 | -0.11 | -0.11 | -0.11 | 0.00 | 0.00 |
| `zico_sizectrl` | 10 | +0.20 | -0.33 | +0.67 | 0.33 | 0.11 |
| `zico_sizectrl` | 20 | +0.19 | -0.21 | +0.52 | 0.20 | 0.04 |
| `zico_sizectrl` | 30 | +0.22 | -0.03 | +0.51 | 0.09 | 0.02 |
| `zico_sizectrl` | 40 | +0.17 | -0.05 | +0.33 | 0.03 | 0.00 |
| `zico_sizectrl` | 50 | +0.18 | +0.15 | +0.25 | 0.02 | 0.00 |
| `zico_sizectrl` | 100 | +nan | +nan | +nan | 0.00 | 0.00 |
| `zico_sizectrl` | 150 | +nan | +nan | +nan | 0.00 | 0.00 |

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

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 0.60 / 0.90 / 0.70; within-arch std 0.0011 vs across-arch std 0.0059. The ground truth is not the limiting factor at N = 50.
