# CI summary — is N = 50 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 50 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `zico` | 0.65 | (0.45, 0.78) | 0.16 | yes | no |
| `l2_norm_all` | 0.63 | (0.40, 0.78) | 0.19 | yes | no |
| `params` | 0.47 | (0.23, 0.65) | 0.21 | yes | yes |
| `grasp_all` | 0.35 | (0.07, 0.57) | 0.25 | yes | yes |
| `zen` | 0.33 | (0.05, 0.55) | 0.25 | yes | yes |
| `nwot` | 0.17 | (-0.14, 0.44) | 0.29 | no | yes |
| `flops` | 0.06 | (-0.25, 0.34) | 0.30 | no | yes |
| `synflow_all` | -0.11 | (-0.41, 0.18) | 0.30 | no | yes |
| `jacov` | -0.18 | (-0.43, 0.10) | 0.26 | no | yes |
| `plain_all` | -0.21 | (-0.45, 0.07) | 0.26 | no | yes |
| `grad_norm_all` | -0.25 | (-0.51, 0.02) | 0.26 | no | yes |
| `snip_all` | -0.26 | (-0.52, 0.04) | 0.28 | no | yes |
| `fisher` | -0.27 | (-0.51, 0.01) | 0.26 | no | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.61 | +0.20 | +0.85 | 0.99 | 0.83 |
| `zico` | 20 | +0.65 | +0.45 | +0.79 | 1.00 | 0.96 |
| `zico` | 30 | +0.65 | +0.52 | +0.75 | 1.00 | 1.00 |
| `zico` | 40 | +0.65 | +0.57 | +0.72 | 1.00 | 1.00 |
| `zico` | 50 | +0.65 | +0.65 | +0.65 | 1.00 | 1.00 |
| `l2_norm_all` | 10 | +0.62 | +0.21 | +0.88 | 0.99 | 0.83 |
| `l2_norm_all` | 20 | +0.62 | +0.41 | +0.78 | 1.00 | 0.95 |
| `l2_norm_all` | 30 | +0.63 | +0.49 | +0.75 | 1.00 | 0.99 |
| `l2_norm_all` | 40 | +0.63 | +0.55 | +0.70 | 1.00 | 1.00 |
| `l2_norm_all` | 50 | +0.63 | +0.63 | +0.63 | 1.00 | 1.00 |
| `params` | 10 | +0.47 | +0.04 | +0.77 | 0.97 | 0.62 |
| `params` | 20 | +0.46 | +0.22 | +0.66 | 1.00 | 0.65 |
| `params` | 30 | +0.46 | +0.30 | +0.60 | 1.00 | 0.77 |
| `params` | 40 | +0.47 | +0.37 | +0.55 | 1.00 | 0.88 |
| `params` | 50 | +0.47 | +0.47 | +0.47 | 1.00 | 1.00 |
| `grasp_all` | 10 | +0.33 | -0.19 | +0.73 | 0.84 | 0.42 |
| `grasp_all` | 20 | +0.34 | +0.05 | +0.61 | 0.97 | 0.37 |
| `grasp_all` | 30 | +0.34 | +0.17 | +0.54 | 1.00 | 0.30 |
| `grasp_all` | 40 | +0.35 | +0.24 | +0.46 | 1.00 | 0.20 |
| `grasp_all` | 50 | +0.35 | +0.35 | +0.35 | 1.00 | 0.00 |
| `zen` | 10 | +0.33 | -0.19 | +0.67 | 0.86 | 0.40 |
| `zen` | 20 | +0.32 | +0.03 | +0.56 | 0.96 | 0.31 |
| `zen` | 30 | +0.33 | +0.16 | +0.49 | 1.00 | 0.21 |
| `zen` | 40 | +0.33 | +0.21 | +0.42 | 1.00 | 0.09 |
| `zen` | 50 | +0.33 | +0.33 | +0.33 | 1.00 | 0.00 |
| `nwot` | 10 | +0.18 | -0.35 | +0.64 | 0.68 | 0.25 |
| `nwot` | 20 | +0.17 | -0.13 | +0.46 | 0.82 | 0.09 |
| `nwot` | 30 | +0.17 | -0.03 | +0.37 | 0.92 | 0.02 |
| `nwot` | 40 | +0.17 | +0.05 | +0.28 | 0.99 | 0.00 |
| `nwot` | 50 | +0.17 | +0.17 | +0.17 | 1.00 | 0.00 |
| `snip_all` | 10 | -0.24 | -0.75 | +0.35 | 0.24 | 0.03 |
| `snip_all` | 20 | -0.23 | -0.53 | +0.06 | 0.10 | 0.00 |
| `snip_all` | 30 | -0.27 | -0.46 | -0.05 | 0.01 | 0.00 |
| `snip_all` | 40 | -0.25 | -0.39 | -0.14 | 0.00 | 0.00 |
| `snip_all` | 50 | -0.26 | -0.26 | -0.26 | 0.00 | 0.00 |

## How large must N be? (Fisher-z approximation, se ≈ 1.06/√(N−3), 95 % CI)

| CI half-width | N needed |
|---|---|
| ±0.30 | 51 |
| ±0.20 | 111 |
| ±0.15 | 195 |
| ±0.10 | 435 |
| ±0.05 | 1730 |

At N = 50 the expected half-width is ±0.30, which is what the bootstrap shows (±0.15–0.30). Separating a proxy at ρ ≈ 0.65 from the 0.737 reference needs a half-width below ≈ 0.09, i.e. N ≈ 500; separating it from 0 needs N ≈ 20.

## Seed-noise ceiling

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 1.00 / 0.90 / 0.90; within-arch std 0.0003 vs across-arch std 0.0021. The ground truth is not the limiting factor at N = 50.
