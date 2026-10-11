# CI summary — is N = 300 enough, and does the sign convention match LENAS?

## Sign convention

Every score is correlated with **−val MAE**, so a *useful* proxy has a **positive** Spearman. LENAS (Klosa & Konen 2023) reports the naswot score against validation loss on its own space with the same reading (higher score ↔ lower loss, ρ = 0.737), so the reference is compared directly. No proxy is sign-flipped; the negative rows in Table A really point the wrong way.

## Bootstrap CIs (2000 resamples over the 300 architectures)

| Proxy | Spearman | 95% CI | CI half-width | excludes 0? | excludes 0.737? |
|---|---|---|---|---|---|
| `zico` | 0.57 | (0.48, 0.65) | 0.08 | yes | yes |
| `l2_norm_all` | 0.50 | (0.41, 0.59) | 0.09 | yes | yes |
| `nwot` | 0.34 | (0.24, 0.43) | 0.09 | yes | yes |
| `flops` | 0.31 | (0.21, 0.41) | 0.10 | yes | yes |
| `params` | 0.19 | (0.08, 0.31) | 0.11 | yes | yes |
| `synflow_all` | 0.19 | (0.08, 0.30) | 0.11 | yes | yes |
| `grasp_all` | 0.17 | (0.06, 0.28) | 0.11 | yes | yes |
| `zen` | 0.12 | (0.00, 0.24) | 0.12 | yes | yes |
| `fisher` | -0.08 | (-0.19, 0.03) | 0.11 | no | yes |
| `plain_all` | -0.09 | (-0.20, 0.02) | 0.11 | no | yes |
| `grad_norm_all` | -0.13 | (-0.23, -0.01) | 0.11 | yes | yes |
| `snip_all` | -0.14 | (-0.24, -0.02) | 0.11 | yes | yes |
| `jacov` | -0.29 | (-0.39, -0.18) | 0.11 | yes | yes |

## Sub-sampling curve (500 draws without replacement per N; median and 5–95 % range of Spearman)

| Proxy | N | median ρ | 5 % | 95 % | fraction of draws with ρ > 0 | fraction with ρ > 0.4 |
|---|---|---|---|---|---|---|
| `zico` | 10 | +0.58 | +0.09 | +0.87 | 0.98 | 0.73 |
| `zico` | 20 | +0.57 | +0.24 | +0.79 | 0.99 | 0.79 |
| `zico` | 30 | +0.57 | +0.33 | +0.75 | 1.00 | 0.89 |
| `zico` | 40 | +0.57 | +0.36 | +0.73 | 1.00 | 0.92 |
| `zico` | 50 | +0.57 | +0.39 | +0.71 | 1.00 | 0.94 |
| `zico` | 100 | +0.57 | +0.46 | +0.67 | 1.00 | 0.99 |
| `zico` | 150 | +0.57 | +0.50 | +0.64 | 1.00 | 1.00 |
| `zico` | 200 | +0.57 | +0.52 | +0.62 | 1.00 | 1.00 |
| `zico` | 250 | +0.57 | +0.54 | +0.60 | 1.00 | 1.00 |
| `zico` | 300 | +0.57 | +0.57 | +0.57 | 1.00 | 1.00 |
| `l2_norm_all` | 10 | +0.51 | -0.08 | +0.84 | 0.93 | 0.64 |
| `l2_norm_all` | 20 | +0.49 | +0.18 | +0.74 | 0.98 | 0.69 |
| `l2_norm_all` | 30 | +0.51 | +0.23 | +0.71 | 1.00 | 0.74 |
| `l2_norm_all` | 40 | +0.49 | +0.28 | +0.67 | 1.00 | 0.78 |
| `l2_norm_all` | 50 | +0.50 | +0.31 | +0.65 | 1.00 | 0.81 |
| `l2_norm_all` | 100 | +0.50 | +0.38 | +0.60 | 1.00 | 0.93 |
| `l2_norm_all` | 150 | +0.50 | +0.42 | +0.58 | 1.00 | 0.98 |
| `l2_norm_all` | 200 | +0.50 | +0.45 | +0.55 | 1.00 | 1.00 |
| `l2_norm_all` | 250 | +0.50 | +0.47 | +0.53 | 1.00 | 1.00 |
| `l2_norm_all` | 300 | +0.50 | +0.50 | +0.50 | 1.00 | 1.00 |
| `params` | 10 | +0.16 | -0.37 | +0.66 | 0.72 | 0.27 |
| `params` | 20 | +0.20 | -0.20 | +0.50 | 0.78 | 0.15 |
| `params` | 30 | +0.20 | -0.13 | +0.48 | 0.84 | 0.10 |
| `params` | 40 | +0.20 | -0.05 | +0.43 | 0.90 | 0.07 |
| `params` | 50 | +0.21 | -0.02 | +0.40 | 0.94 | 0.05 |
| `params` | 100 | +0.20 | +0.07 | +0.32 | 0.99 | 0.01 |
| `params` | 150 | +0.19 | +0.10 | +0.28 | 1.00 | 0.00 |
| `params` | 200 | +0.19 | +0.13 | +0.26 | 1.00 | 0.00 |
| `params` | 250 | +0.19 | +0.15 | +0.23 | 1.00 | 0.00 |
| `params` | 300 | +0.19 | +0.19 | +0.19 | 1.00 | 0.00 |
| `grasp_all` | 10 | +0.18 | -0.41 | +0.64 | 0.67 | 0.22 |
| `grasp_all` | 20 | +0.18 | -0.16 | +0.50 | 0.81 | 0.14 |
| `grasp_all` | 30 | +0.18 | -0.11 | +0.45 | 0.82 | 0.09 |
| `grasp_all` | 40 | +0.17 | -0.09 | +0.40 | 0.88 | 0.05 |
| `grasp_all` | 50 | +0.17 | -0.03 | +0.38 | 0.92 | 0.03 |
| `grasp_all` | 100 | +0.17 | +0.04 | +0.31 | 0.98 | 0.00 |
| `grasp_all` | 150 | +0.18 | +0.08 | +0.26 | 1.00 | 0.00 |
| `grasp_all` | 200 | +0.17 | +0.11 | +0.23 | 1.00 | 0.00 |
| `grasp_all` | 250 | +0.17 | +0.14 | +0.21 | 1.00 | 0.00 |
| `grasp_all` | 300 | +0.17 | +0.17 | +0.17 | 1.00 | 0.00 |
| `zen` | 10 | +0.14 | -0.47 | +0.66 | 0.68 | 0.23 |
| `zen` | 20 | +0.10 | -0.24 | +0.48 | 0.66 | 0.09 |
| `zen` | 30 | +0.12 | -0.18 | +0.39 | 0.74 | 0.04 |
| `zen` | 40 | +0.11 | -0.14 | +0.36 | 0.75 | 0.02 |
| `zen` | 50 | +0.11 | -0.10 | +0.31 | 0.80 | 0.01 |
| `zen` | 100 | +0.12 | -0.01 | +0.24 | 0.94 | 0.00 |
| `zen` | 150 | +0.12 | +0.02 | +0.23 | 0.97 | 0.00 |
| `zen` | 200 | +0.11 | +0.04 | +0.18 | 1.00 | 0.00 |
| `zen` | 250 | +0.12 | +0.07 | +0.16 | 1.00 | 0.00 |
| `zen` | 300 | +0.12 | +0.12 | +0.12 | 1.00 | 0.00 |
| `nwot` | 10 | +0.35 | -0.21 | +0.77 | 0.84 | 0.44 |
| `nwot` | 20 | +0.34 | -0.06 | +0.66 | 0.93 | 0.38 |
| `nwot` | 30 | +0.33 | +0.07 | +0.60 | 0.98 | 0.33 |
| `nwot` | 40 | +0.34 | +0.12 | +0.53 | 0.99 | 0.32 |
| `nwot` | 50 | +0.33 | +0.13 | +0.52 | 1.00 | 0.29 |
| `nwot` | 100 | +0.34 | +0.22 | +0.45 | 1.00 | 0.21 |
| `nwot` | 150 | +0.34 | +0.26 | +0.42 | 1.00 | 0.10 |
| `nwot` | 200 | +0.34 | +0.28 | +0.40 | 1.00 | 0.05 |
| `nwot` | 250 | +0.34 | +0.30 | +0.38 | 1.00 | 0.01 |
| `nwot` | 300 | +0.34 | +0.34 | +0.34 | 1.00 | 0.00 |
| `snip_all` | 10 | -0.13 | -0.61 | +0.42 | 0.35 | 0.05 |
| `snip_all` | 20 | -0.12 | -0.47 | +0.30 | 0.29 | 0.01 |
| `snip_all` | 30 | -0.14 | -0.41 | +0.19 | 0.22 | 0.00 |
| `snip_all` | 40 | -0.13 | -0.37 | +0.13 | 0.21 | 0.00 |
| `snip_all` | 50 | -0.14 | -0.35 | +0.09 | 0.14 | 0.00 |
| `snip_all` | 100 | -0.13 | -0.27 | -0.01 | 0.04 | 0.00 |
| `snip_all` | 150 | -0.13 | -0.24 | -0.04 | 0.01 | 0.00 |
| `snip_all` | 200 | -0.13 | -0.20 | -0.06 | 0.00 | 0.00 |
| `snip_all` | 250 | -0.13 | -0.18 | -0.09 | 0.00 | 0.00 |
| `snip_all` | 300 | -0.14 | -0.14 | -0.14 | 0.00 | 0.00 |

## How large must N be? (Fisher-z approximation, se ≈ 1.06/√(N−3), 95 % CI)

| CI half-width | N needed |
|---|---|
| ±0.30 | 51 |
| ±0.20 | 111 |
| ±0.15 | 195 |
| ±0.10 | 435 |
| ±0.05 | 1730 |

At N = 300 the expected half-width is ±0.12, which is what the bootstrap shows (±0.15–0.30). Separating a proxy at ρ ≈ 0.65 from the 0.737 reference needs a half-width below ≈ 0.09, i.e. N ≈ 500; separating it from 0 needs N ≈ 20.

## Seed-noise ceiling

Seed-0 vs seed-1 / 0 vs 2 / 1 vs 2 Spearman of val MAE on the 5 repeated archs: 1.00 / 0.90 / 0.90; within-arch std 0.0003 vs across-arch std 0.0033. The ground truth is not the limiting factor at N = 50.
