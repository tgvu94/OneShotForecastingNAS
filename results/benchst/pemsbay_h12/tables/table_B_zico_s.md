# Table B — Experiment B, base = zico_s

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| zico_s alone (under A) | 150 | 0.04 (-0.13, 0.19) | 0.03 | 0.10 | 0.06 | no |
| S_spatial (zico_s) | 150 | -0.08 (-0.24, 0.07) | -0.06 | -0.15 | -0.24 | no |
| z_spatial (zico_s) | 150 | -0.10 (-0.25, 0.05) | -0.07 | -0.15 | -0.22 | no |
| composite = z(zico_s) + z(S_spatial) | 150 | -0.03 (-0.20, 0.12) | -0.02 | -0.06 | -0.13 | no |
| composite = z(zico_s) + z(z_spatial) | 150 | -0.04 (-0.20, 0.12) | -0.02 | -0.06 | -0.16 | no |

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
