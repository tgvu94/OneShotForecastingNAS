# Table B — Experiment B, base = nwot

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| nwot alone (under A) | 150 | -0.06 (-0.22, 0.10) | -0.04 | 0.10 | 0.10 | no |
| S_spatial (nwot) | 150 | -0.12 (-0.28, 0.04) | -0.09 | -0.09 | -0.11 | no |
| z_spatial (nwot) | 150 | -0.10 (-0.26, 0.06) | -0.07 | -0.05 | -0.05 | no |
| composite = z(nwot) + z(S_spatial) | 150 | -0.12 (-0.27, 0.04) | -0.08 | -0.05 | -0.06 | no |
| composite = z(nwot) + z(z_spatial) | 150 | -0.08 (-0.23, 0.08) | -0.05 | 0.03 | 0.04 | no |

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
