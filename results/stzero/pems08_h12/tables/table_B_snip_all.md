# Table B — Experiment B, base = snip_all

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| snip_all alone (under A) | 150 | -0.36 (-0.50, -0.20) | -0.25 | -0.42 | -0.31 | no |
| S_spatial (snip_all) | 150 | -0.03 (-0.20, 0.14) | -0.01 | -0.24 | -0.39 | no |
| z_spatial (snip_all) | 150 | -0.10 (-0.27, 0.07) | -0.07 | -0.33 | -0.50 | no |
| composite = z(snip_all) + z(S_spatial) | 150 | -0.39 (-0.53, -0.23) | -0.26 | -0.49 | -0.42 | no |
| composite = z(snip_all) + z(z_spatial) | 150 | -0.42 (-0.56, -0.25) | -0.29 | -0.55 | -0.51 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +13.1 (+2.3, +34.7) | 81/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +0.3 (-2.0, +2.5) | 0/84 | 53/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +3.9 (-1.2, +13.3) | 48/84 | 80/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +2.6 (-3.5, +12.6) | 39/84 | 77/84 |
