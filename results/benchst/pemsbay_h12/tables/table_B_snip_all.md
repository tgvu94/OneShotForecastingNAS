# Table B — Experiment B, base = snip_all

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| snip_all alone (under A) | 150 | -0.51 (-0.62, -0.37) | -0.33 | -0.51 | -0.46 | no |
| S_spatial (snip_all) | 150 | -0.19 (-0.35, -0.02) | -0.13 | -0.37 | -0.58 | no |
| z_spatial (snip_all) | 150 | -0.13 (-0.29, 0.02) | -0.10 | -0.29 | -0.45 | no |
| composite = z(snip_all) + z(S_spatial) | 150 | -0.57 (-0.67, -0.45) | -0.37 | -0.62 | -0.60 | no |
| composite = z(snip_all) + z(z_spatial) | 150 | -0.55 (-0.64, -0.43) | -0.36 | -0.60 | -0.61 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +179.0 (+110.7, +249.8) | 84/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +2.5 (-3.1, +18.4) | 36/84 | 74/84 |
| `zico_t` | 66 | 0.0e+00 | 84 | +0.1 (-2.2, +2.7) | 0/84 | 46/84 |
| `zico_s` | 66 | 0.0e+00 | 84 | +11.7 (-0.5, +29.7) | 71/84 | 78/84 |
| `glass` | 66 | 0.0e+00 | 84 | +2.1 (-1.4, +8.9) | 30/84 | 74/84 |
| `glass_t` | 66 | 0.0e+00 | 84 | +0.2 (-2.2, +2.9) | 0/84 | 49/84 |
| `glass_s` | 66 | 0.0e+00 | 84 | +10.7 (-4.1, +30.5) | 72/84 | 77/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +13.2 (-19.1, +75.9) | 74/84 | 81/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +10.0 (-13.3, +66.8) | 65/84 | 75/84 |
