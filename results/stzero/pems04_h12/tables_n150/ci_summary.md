# CI summary — is N = 150 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 150 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `zico` | 0.57 | (0.44, 0.67) | 0.11 | yes | yes |
| `l2_norm_all` | 0.50 | (0.36, 0.62) | 0.13 | yes | yes |
| `nwot` | 0.39 | (0.24, 0.52) | 0.14 | yes | yes |
| `flops` | 0.35 | (0.19, 0.48) | 0.15 | yes | yes |
| `grasp_all` | 0.20 | (0.03, 0.34) | 0.16 | yes | yes |
| `params` | 0.19 | (0.04, 0.34) | 0.15 | yes | yes |
| `synflow_all` | 0.18 | (0.02, 0.33) | 0.16 | yes | yes |
| `zen` | 0.16 | (0.02, 0.30) | 0.14 | yes | yes |
| `fisher` | -0.10 | (-0.25, 0.06) | 0.16 | no | yes |
| `plain_all` | -0.14 | (-0.29, 0.03) | 0.16 | no | yes |
| `grad_norm_all` | -0.16 | (-0.31, -0.00) | 0.15 | yes | yes |
| `snip_all` | -0.19 | (-0.34, -0.03) | 0.16 | yes | yes |
| `jacov` | -0.41 | (-0.53, -0.29) | 0.12 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.55 | +0.09 | +0.84 | 0.96 | 0.71 |
| `zico` | 20 | +0.57 | +0.23 | +0.78 | 1.00 | 0.80 |
| `zico` | 30 | +0.56 | +0.33 | +0.75 | 1.00 | 0.87 |
| `zico` | 40 | +0.57 | +0.39 | +0.72 | 1.00 | 0.94 |
| `zico` | 50 | +0.57 | +0.43 | +0.69 | 1.00 | 0.97 |
| `zico` | 100 | +0.57 | +0.50 | +0.63 | 1.00 | 1.00 |
| `zico` | 150 | +0.57 | +0.57 | +0.57 | 1.00 | 1.00 |
| `l2_norm_all` | 10 | +0.48 | -0.07 | +0.82 | 0.93 | 0.61 |
| `l2_norm_all` | 20 | +0.48 | +0.16 | +0.73 | 0.99 | 0.70 |
| `l2_norm_all` | 30 | +0.51 | +0.26 | +0.69 | 1.00 | 0.74 |
| `l2_norm_all` | 40 | +0.50 | +0.29 | +0.66 | 1.00 | 0.77 |
| `l2_norm_all` | 50 | +0.49 | +0.34 | +0.64 | 1.00 | 0.82 |
| `l2_norm_all` | 100 | +0.50 | +0.42 | +0.57 | 1.00 | 0.98 |
| `l2_norm_all` | 150 | +0.50 | +0.50 | +0.50 | 1.00 | 1.00 |
| `params` | 10 | +0.16 | -0.39 | +0.64 | 0.70 | 0.23 |
| `params` | 20 | +0.18 | -0.18 | +0.52 | 0.79 | 0.13 |
| `params` | 30 | +0.18 | -0.07 | +0.43 | 0.87 | 0.06 |
| `params` | 40 | +0.19 | -0.05 | +0.37 | 0.92 | 0.02 |
| `params` | 50 | +0.19 | -0.00 | +0.37 | 0.95 | 0.03 |
| `params` | 100 | +0.19 | +0.11 | +0.29 | 1.00 | 0.00 |
| `params` | 150 | +0.19 | +0.19 | +0.19 | 1.00 | 0.00 |
| `grasp_all` | 10 | +0.20 | -0.31 | +0.67 | 0.72 | 0.26 |
| `grasp_all` | 20 | +0.18 | -0.17 | +0.51 | 0.80 | 0.14 |
| `grasp_all` | 30 | +0.18 | -0.08 | +0.45 | 0.87 | 0.09 |
| `grasp_all` | 40 | +0.19 | -0.04 | +0.41 | 0.93 | 0.06 |
| `grasp_all` | 50 | +0.19 | -0.01 | +0.36 | 0.95 | 0.02 |
| `grasp_all` | 100 | +0.20 | +0.11 | +0.29 | 1.00 | 0.00 |
| `grasp_all` | 150 | +0.20 | +0.20 | +0.20 | 1.00 | 0.00 |
| `zen` | 10 | +0.15 | -0.37 | +0.64 | 0.67 | 0.20 |
| `zen` | 20 | +0.16 | -0.22 | +0.48 | 0.75 | 0.12 |
| `zen` | 30 | +0.16 | -0.10 | +0.42 | 0.86 | 0.07 |
| `zen` | 40 | +0.16 | -0.05 | +0.35 | 0.88 | 0.02 |
| `zen` | 50 | +0.16 | -0.03 | +0.33 | 0.92 | 0.01 |
| `zen` | 100 | +0.16 | +0.07 | +0.25 | 1.00 | 0.00 |
| `zen` | 150 | +0.16 | +0.16 | +0.16 | 1.00 | 0.00 |
| `nwot` | 10 | +0.39 | -0.18 | +0.78 | 0.88 | 0.48 |
| `nwot` | 20 | +0.38 | +0.04 | +0.65 | 0.97 | 0.45 |
| `nwot` | 30 | +0.38 | +0.12 | +0.61 | 1.00 | 0.44 |
| `nwot` | 40 | +0.38 | +0.18 | +0.56 | 1.00 | 0.41 |
| `nwot` | 50 | +0.38 | +0.19 | +0.53 | 1.00 | 0.41 |
| `nwot` | 100 | +0.38 | +0.31 | +0.47 | 1.00 | 0.37 |
| `nwot` | 150 | +0.39 | +0.39 | +0.39 | 1.00 | 0.00 |
| `snip_all` | 10 | -0.20 | -0.71 | +0.36 | 0.30 | 0.04 |
| `snip_all` | 20 | -0.17 | -0.53 | +0.16 | 0.20 | 0.00 |
| `snip_all` | 30 | -0.18 | -0.45 | +0.08 | 0.13 | 0.00 |
| `snip_all` | 40 | -0.19 | -0.39 | +0.04 | 0.10 | 0.00 |
| `snip_all` | 50 | -0.19 | -0.39 | -0.02 | 0.04 | 0.00 |
| `snip_all` | 100 | -0.19 | -0.28 | -0.10 | 0.00 | 0.00 |
| `snip_all` | 150 | -0.19 | -0.19 | -0.19 | 0.00 | 0.00 |

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

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 1.00 / 0.90 / 0.90; within-arch std 0.0003 vs across-arch std 0.0039. The ground truth is not the limiting factor at N = 50.
