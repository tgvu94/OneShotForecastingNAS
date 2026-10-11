# CI summary — is N = 50 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 50 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `zico` | 0.71 | (0.52, 0.82) | 0.15 | yes | no |
| `l2_norm_all` | 0.59 | (0.34, 0.76) | 0.21 | yes | no |
| `params` | 0.51 | (0.27, 0.68) | 0.21 | yes | yes |
| `grasp_all` | 0.30 | (0.02, 0.56) | 0.27 | yes | yes |
| `zen` | 0.30 | (0.01, 0.54) | 0.27 | yes | yes |
| `nwot` | 0.03 | (-0.27, 0.31) | 0.29 | no | yes |
| `flops` | -0.03 | (-0.34, 0.25) | 0.30 | no | yes |
| `synflow_all` | -0.10 | (-0.42, 0.20) | 0.31 | no | yes |
| `jacov` | -0.15 | (-0.40, 0.15) | 0.27 | no | yes |
| `plain_all` | -0.15 | (-0.42, 0.15) | 0.28 | no | yes |
| `fisher` | -0.26 | (-0.53, 0.03) | 0.28 | no | yes |
| `grad_norm_all` | -0.28 | (-0.54, 0.01) | 0.27 | no | yes |
| `snip_all` | -0.29 | (-0.55, -0.01) | 0.27 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.68 | +0.26 | +0.89 | 0.99 | 0.88 |
| `zico` | 20 | +0.71 | +0.52 | +0.82 | 1.00 | 0.99 |
| `zico` | 30 | +0.71 | +0.58 | +0.79 | 1.00 | 1.00 |
| `zico` | 40 | +0.71 | +0.63 | +0.77 | 1.00 | 1.00 |
| `zico` | 50 | +0.71 | +0.71 | +0.71 | 1.00 | 1.00 |
| `l2_norm_all` | 10 | +0.60 | +0.14 | +0.87 | 0.98 | 0.77 |
| `l2_norm_all` | 20 | +0.59 | +0.32 | +0.77 | 1.00 | 0.89 |
| `l2_norm_all` | 30 | +0.59 | +0.45 | +0.73 | 1.00 | 0.98 |
| `l2_norm_all` | 40 | +0.59 | +0.50 | +0.67 | 1.00 | 1.00 |
| `l2_norm_all` | 50 | +0.59 | +0.59 | +0.59 | 1.00 | 1.00 |
| `params` | 10 | +0.48 | +0.03 | +0.81 | 0.96 | 0.64 |
| `params` | 20 | +0.50 | +0.24 | +0.71 | 1.00 | 0.73 |
| `params` | 30 | +0.49 | +0.35 | +0.64 | 1.00 | 0.83 |
| `params` | 40 | +0.50 | +0.42 | +0.60 | 1.00 | 0.97 |
| `params` | 50 | +0.51 | +0.51 | +0.51 | 1.00 | 1.00 |
| `grasp_all` | 10 | +0.27 | -0.22 | +0.76 | 0.81 | 0.36 |
| `grasp_all` | 20 | +0.30 | +0.01 | +0.60 | 0.96 | 0.28 |
| `grasp_all` | 30 | +0.30 | +0.10 | +0.50 | 1.00 | 0.20 |
| `grasp_all` | 40 | +0.30 | +0.19 | +0.43 | 1.00 | 0.10 |
| `grasp_all` | 50 | +0.30 | +0.30 | +0.30 | 1.00 | 0.00 |
| `zen` | 10 | +0.31 | -0.26 | +0.70 | 0.84 | 0.39 |
| `zen` | 20 | +0.30 | -0.01 | +0.55 | 0.95 | 0.26 |
| `zen` | 30 | +0.31 | +0.12 | +0.50 | 0.99 | 0.19 |
| `zen` | 40 | +0.30 | +0.19 | +0.41 | 1.00 | 0.06 |
| `zen` | 50 | +0.30 | +0.30 | +0.30 | 1.00 | 0.00 |
| `nwot` | 10 | +0.04 | -0.50 | +0.52 | 0.54 | 0.11 |
| `nwot` | 20 | +0.02 | -0.26 | +0.32 | 0.54 | 0.02 |
| `nwot` | 30 | +0.03 | -0.16 | +0.22 | 0.62 | 0.00 |
| `nwot` | 40 | +0.03 | -0.10 | +0.15 | 0.64 | 0.00 |
| `nwot` | 50 | +0.03 | +0.03 | +0.03 | 1.00 | 0.00 |
| `snip_all` | 10 | -0.27 | -0.77 | +0.28 | 0.20 | 0.01 |
| `snip_all` | 20 | -0.26 | -0.58 | +0.05 | 0.07 | 0.00 |
| `snip_all` | 30 | -0.30 | -0.49 | -0.10 | 0.00 | 0.00 |
| `snip_all` | 40 | -0.29 | -0.41 | -0.17 | 0.00 | 0.00 |
| `snip_all` | 50 | -0.29 | -0.29 | -0.29 | 0.00 | 0.00 |

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

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 0.20 / 0.60 / 0.60; within-arch std 0.0013 vs across-arch std 0.0064. The ground truth is not the limiting factor at N = 50.
