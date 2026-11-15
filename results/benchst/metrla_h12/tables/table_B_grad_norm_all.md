# Table B — Experiment B, base = grad_norm_all

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| grad_norm_all alone (under A) | 150 | -0.46 (-0.58, -0.31) | -0.31 | -0.49 | -0.45 | no |
| S_spatial (grad_norm_all) | 150 | -0.23 (-0.39, -0.07) | -0.16 | -0.31 | -0.43 | no |
| z_spatial (grad_norm_all) | 150 | -0.23 (-0.37, -0.08) | -0.16 | -0.29 | -0.37 | no |
| composite = z(grad_norm_all) + z(S_spatial) | 150 | -0.53 (-0.64, -0.39) | -0.35 | -0.58 | -0.56 | no |
| composite = z(grad_norm_all) + z(z_spatial) | 150 | -0.52 (-0.62, -0.39) | -0.35 | -0.55 | -0.54 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +87.9 (+45.6, +161.5) | 84/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +1.9 (-0.9, +14.7) | 29/84 | 70/84 |
| `zico_t` | 66 | 0.0e+00 | 84 | +0.2 (-1.7, +3.2) | 2/84 | 54/84 |
| `zico_s` | 66 | 0.0e+00 | 84 | +8.9 (-0.8, +35.5) | 70/84 | 80/84 |
| `glass` | 66 | 0.0e+00 | 84 | +2.1 (-2.1, +8.0) | 19/84 | 73/84 |
| `glass_t` | 66 | 0.0e+00 | 84 | +0.2 (-2.9, +3.4) | 1/84 | 48/84 |
| `glass_s` | 66 | 0.0e+00 | 84 | +8.2 (-1.2, +35.5) | 69/84 | 81/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +6.6 (-24.9, +41.3) | 61/84 | 69/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +6.1 (-20.8, +41.9) | 60/84 | 70/84 |
