# Table B — Experiment B, base = grad_norm_all

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| grad_norm_all alone (under A) | 150 | -0.40 (-0.53, -0.24) | -0.27 | -0.47 | -0.37 | no |
| S_spatial (grad_norm_all) | 150 | -0.06 (-0.23, 0.11) | -0.03 | -0.29 | -0.47 | no |
| z_spatial (grad_norm_all) | 150 | -0.08 (-0.25, 0.09) | -0.06 | -0.33 | -0.51 | no |
| composite = z(grad_norm_all) + z(S_spatial) | 150 | -0.42 (-0.55, -0.25) | -0.27 | -0.53 | -0.46 | no |
| composite = z(grad_norm_all) + z(z_spatial) | 150 | -0.41 (-0.54, -0.24) | -0.27 | -0.57 | -0.55 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +13.1 (+2.3, +34.7) | 81/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +0.3 (-2.0, +2.5) | 0/84 | 53/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +3.9 (-1.2, +13.3) | 48/84 | 80/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +2.6 (-3.5, +12.6) | 39/84 | 77/84 |
