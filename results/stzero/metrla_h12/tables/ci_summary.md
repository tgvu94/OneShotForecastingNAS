# CI summary — is N = 50 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 50 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `grasp_all` | 0.43 | (0.15, 0.64) | 0.25 | yes | yes |
| `nwot` | 0.05 | (-0.25, 0.34) | 0.29 | no | yes |
| `flops` | 0.02 | (-0.26, 0.31) | 0.29 | no | yes |
| `l2_norm_all` | 0.00 | (-0.30, 0.29) | 0.29 | no | yes |
| `params` | -0.04 | (-0.32, 0.26) | 0.29 | no | yes |
| `jacov` | -0.05 | (-0.31, 0.23) | 0.27 | no | yes |
| `zen` | -0.05 | (-0.36, 0.26) | 0.31 | no | yes |
| `zico` | -0.09 | (-0.36, 0.20) | 0.28 | no | yes |
| `synflow_all` | -0.23 | (-0.48, 0.05) | 0.27 | no | yes |
| `snip_all` | -0.39 | (-0.62, -0.08) | 0.27 | yes | yes |
| `grad_norm_all` | -0.44 | (-0.66, -0.15) | 0.26 | yes | yes |
| `plain_all` | -0.45 | (-0.65, -0.20) | 0.23 | yes | yes |
| `fisher` | -0.55 | (-0.72, -0.28) | 0.22 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | -0.07 | -0.58 | +0.47 | 0.44 | 0.08 |
| `zico` | 20 | -0.09 | -0.41 | +0.23 | 0.32 | 0.00 |
| `zico` | 30 | -0.10 | -0.28 | +0.11 | 0.21 | 0.00 |
| `zico` | 40 | -0.08 | -0.21 | +0.04 | 0.13 | 0.00 |
| `zico` | 50 | -0.09 | -0.09 | -0.09 | 0.00 | 0.00 |
| `l2_norm_all` | 10 | -0.03 | -0.55 | +0.60 | 0.47 | 0.14 |
| `l2_norm_all` | 20 | +0.00 | -0.34 | +0.35 | 0.51 | 0.02 |
| `l2_norm_all` | 30 | -0.00 | -0.21 | +0.23 | 0.50 | 0.00 |
| `l2_norm_all` | 40 | +0.00 | -0.13 | +0.12 | 0.51 | 0.00 |
| `l2_norm_all` | 50 | +0.00 | +0.00 | +0.00 | 1.00 | 0.00 |
| `params` | 10 | -0.02 | -0.53 | +0.55 | 0.48 | 0.11 |
| `params` | 20 | -0.03 | -0.37 | +0.31 | 0.43 | 0.02 |
| `params` | 30 | -0.05 | -0.25 | +0.17 | 0.38 | 0.00 |
| `params` | 40 | -0.04 | -0.16 | +0.09 | 0.33 | 0.00 |
| `params` | 50 | -0.04 | -0.04 | -0.04 | 0.00 | 0.00 |
| `grasp_all` | 10 | +0.43 | -0.09 | +0.77 | 0.92 | 0.54 |
| `grasp_all` | 20 | +0.45 | +0.15 | +0.66 | 0.99 | 0.60 |
| `grasp_all` | 30 | +0.43 | +0.24 | +0.58 | 1.00 | 0.61 |
| `grasp_all` | 40 | +0.44 | +0.33 | +0.54 | 1.00 | 0.73 |
| `grasp_all` | 50 | +0.43 | +0.43 | +0.43 | 1.00 | 1.00 |
| `zen` | 10 | -0.05 | -0.60 | +0.52 | 0.46 | 0.10 |
| `zen` | 20 | -0.06 | -0.39 | +0.24 | 0.39 | 0.02 |
| `zen` | 30 | -0.05 | -0.26 | +0.19 | 0.36 | 0.00 |
| `zen` | 40 | -0.05 | -0.17 | +0.07 | 0.24 | 0.00 |
| `zen` | 50 | -0.05 | -0.05 | -0.05 | 0.00 | 0.00 |
| `nwot` | 10 | +0.07 | -0.53 | +0.56 | 0.57 | 0.14 |
| `nwot` | 20 | +0.06 | -0.29 | +0.37 | 0.60 | 0.04 |
| `nwot` | 30 | +0.04 | -0.16 | +0.25 | 0.61 | 0.00 |
| `nwot` | 40 | +0.06 | -0.07 | +0.18 | 0.74 | 0.00 |
| `nwot` | 50 | +0.05 | +0.05 | +0.05 | 1.00 | 0.00 |
| `snip_all` | 10 | -0.39 | -0.73 | +0.13 | 0.10 | 0.00 |
| `snip_all` | 20 | -0.40 | -0.66 | -0.06 | 0.02 | 0.00 |
| `snip_all` | 30 | -0.40 | -0.57 | -0.19 | 0.00 | 0.00 |
| `snip_all` | 40 | -0.39 | -0.49 | -0.25 | 0.00 | 0.00 |
| `snip_all` | 50 | -0.39 | -0.39 | -0.39 | 0.00 | 0.00 |

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

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 0.60 / 0.90 / 0.70; within-arch std 0.0021 vs across-arch std 0.0129. The ground truth is not the limiting factor at N = 50.
