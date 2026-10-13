# Table B — Experiment B, base = nwot

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| nwot alone (under A) | 150 | -0.07 (-0.24, 0.09) | -0.05 | 0.04 | 0.02 | no |
| S_spatial (nwot) | 150 | -0.09 (-0.25, 0.06) | -0.07 | -0.05 | -0.04 | no |
| z_spatial (nwot) | 150 | -0.11 (-0.26, 0.04) | -0.07 | -0.08 | -0.08 | no |
| composite = z(nwot) + z(S_spatial) | 150 | -0.09 (-0.25, 0.07) | -0.06 | -0.02 | -0.02 | no |
| composite = z(nwot) + z(z_spatial) | 150 | -0.10 (-0.26, 0.05) | -0.06 | -0.04 | -0.05 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +87.9 (+45.6, +161.5) | 84/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +1.8 (-1.3, +11.7) | 20/84 | 71/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +7.2 (-17.9, +43.6) | 60/84 | 70/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +5.7 (-11.4, +35.5) | 60/84 | 73/84 |
