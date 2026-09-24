# CI summary — is N = 150 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 150 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `grasp_all` | 0.47 | (0.32, 0.60) | 0.14 | yes | yes |
| `zico` | 0.32 | (0.15, 0.46) | 0.15 | yes | yes |
| `l2_norm_all` | 0.25 | (0.09, 0.41) | 0.16 | yes | yes |
| `params` | 0.10 | (-0.06, 0.28) | 0.17 | no | yes |
| `nwot` | 0.05 | (-0.11, 0.22) | 0.16 | no | yes |
| `zen` | 0.00 | (-0.15, 0.17) | 0.16 | no | yes |
| `flops` | 0.00 | (-0.17, 0.16) | 0.16 | no | yes |
| `synflow_all` | -0.01 | (-0.18, 0.17) | 0.17 | no | yes |
| `jacov` | -0.10 | (-0.25, 0.07) | 0.16 | no | yes |
| `snip_all` | -0.36 | (-0.50, -0.20) | 0.15 | yes | yes |
| `grad_norm_all` | -0.40 | (-0.53, -0.24) | 0.15 | yes | yes |
| `fisher` | -0.44 | (-0.58, -0.29) | 0.14 | yes | yes |
| `plain_all` | -0.47 | (-0.59, -0.32) | 0.14 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.32 | -0.26 | +0.73 | 0.79 | 0.43 |
| `zico` | 20 | +0.32 | -0.03 | +0.64 | 0.93 | 0.33 |
| `zico` | 30 | +0.31 | +0.04 | +0.56 | 0.97 | 0.28 |
| `zico` | 40 | +0.31 | +0.12 | +0.50 | 0.99 | 0.23 |
| `zico` | 50 | +0.31 | +0.13 | +0.49 | 1.00 | 0.21 |
| `zico` | 100 | +0.32 | +0.23 | +0.40 | 1.00 | 0.05 |
| `zico` | 150 | +0.32 | +0.32 | +0.32 | 1.00 | 0.00 |
| `l2_norm_all` | 10 | +0.25 | -0.31 | +0.70 | 0.76 | 0.31 |
| `l2_norm_all` | 20 | +0.26 | -0.14 | +0.56 | 0.87 | 0.24 |
| `l2_norm_all` | 30 | +0.24 | -0.03 | +0.48 | 0.93 | 0.16 |
| `l2_norm_all` | 40 | +0.25 | +0.02 | +0.47 | 0.96 | 0.13 |
| `l2_norm_all` | 50 | +0.25 | +0.07 | +0.44 | 0.98 | 0.09 |
| `l2_norm_all` | 100 | +0.26 | +0.15 | +0.34 | 1.00 | 0.00 |
| `l2_norm_all` | 150 | +0.25 | +0.25 | +0.25 | 1.00 | 0.00 |
| `params` | 10 | +0.10 | -0.42 | +0.66 | 0.62 | 0.20 |
| `params` | 20 | +0.09 | -0.26 | +0.45 | 0.64 | 0.09 |
| `params` | 30 | +0.10 | -0.21 | +0.37 | 0.71 | 0.04 |
| `params` | 40 | +0.09 | -0.16 | +0.34 | 0.72 | 0.02 |
| `params` | 50 | +0.10 | -0.10 | +0.28 | 0.79 | 0.01 |
| `params` | 100 | +0.10 | +0.00 | +0.20 | 0.95 | 0.00 |
| `params` | 150 | +0.10 | +0.10 | +0.10 | 1.00 | 0.00 |
| `grasp_all` | 10 | +0.47 | -0.07 | +0.84 | 0.92 | 0.58 |
| `grasp_all` | 20 | +0.48 | +0.11 | +0.73 | 0.98 | 0.67 |
| `grasp_all` | 30 | +0.45 | +0.20 | +0.68 | 1.00 | 0.64 |
| `grasp_all` | 40 | +0.47 | +0.24 | +0.65 | 1.00 | 0.68 |
| `grasp_all` | 50 | +0.47 | +0.30 | +0.63 | 1.00 | 0.75 |
| `grasp_all` | 100 | +0.47 | +0.38 | +0.55 | 1.00 | 0.92 |
| `grasp_all` | 150 | +0.47 | +0.47 | +0.47 | 1.00 | 1.00 |
| `zen` | 10 | +0.01 | -0.56 | +0.54 | 0.52 | 0.13 |
| `zen` | 20 | +0.01 | -0.37 | +0.38 | 0.52 | 0.04 |
| `zen` | 30 | +0.02 | -0.26 | +0.30 | 0.54 | 0.01 |
| `zen` | 40 | -0.00 | -0.22 | +0.22 | 0.50 | 0.00 |
| `zen` | 50 | +0.00 | -0.19 | +0.19 | 0.51 | 0.00 |
| `zen` | 100 | +0.01 | -0.10 | +0.10 | 0.55 | 0.00 |
| `zen` | 150 | +0.00 | +0.00 | +0.00 | 1.00 | 0.00 |
| `nwot` | 10 | +0.05 | -0.52 | +0.55 | 0.56 | 0.13 |
| `nwot` | 20 | +0.06 | -0.30 | +0.43 | 0.59 | 0.07 |
| `nwot` | 30 | +0.04 | -0.22 | +0.33 | 0.59 | 0.02 |
| `nwot` | 40 | +0.05 | -0.20 | +0.31 | 0.62 | 0.02 |
| `nwot` | 50 | +0.06 | -0.12 | +0.26 | 0.68 | 0.00 |
| `nwot` | 100 | +0.05 | -0.04 | +0.16 | 0.80 | 0.00 |
| `nwot` | 150 | +0.05 | +0.05 | +0.05 | 1.00 | 0.00 |
| `snip_all` | 10 | -0.33 | -0.76 | +0.24 | 0.17 | 0.02 |
| `snip_all` | 20 | -0.35 | -0.67 | -0.01 | 0.05 | 0.00 |
| `snip_all` | 30 | -0.36 | -0.60 | -0.07 | 0.02 | 0.00 |
| `snip_all` | 40 | -0.36 | -0.55 | -0.15 | 0.00 | 0.00 |
| `snip_all` | 50 | -0.36 | -0.53 | -0.19 | 0.00 | 0.00 |
| `snip_all` | 100 | -0.37 | -0.46 | -0.27 | 0.00 | 0.00 |
| `snip_all` | 150 | -0.36 | -0.36 | -0.36 | 0.00 | 0.00 |

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

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 1.00 / 1.00 / 1.00; within-arch std 0.0003 vs across-arch std 0.0046. The ground truth is not the limiting factor at N = 50.
