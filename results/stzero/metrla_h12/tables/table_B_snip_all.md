# Table B — Experiment B, base = snip_all

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| snip_all alone (under A) | 150 | -0.41 (-0.53, -0.26) | -0.27 | -0.46 | -0.44 | no |
| S_spatial (snip_all) | 150 | -0.20 (-0.36, -0.04) | -0.15 | -0.29 | -0.41 | no |
| z_spatial (snip_all) | 150 | -0.24 (-0.39, -0.10) | -0.18 | -0.31 | -0.39 | no |
| composite = z(snip_all) + z(S_spatial) | 150 | -0.49 (-0.60, -0.34) | -0.31 | -0.56 | -0.54 | no |
| composite = z(snip_all) + z(z_spatial) | 150 | -0.48 (-0.60, -0.33) | -0.32 | -0.55 | -0.52 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +87.9 (+45.6, +161.5) | 84/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +1.8 (-1.3, +11.7) | 20/84 | 71/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +7.2 (-17.9, +43.6) | 60/84 | 70/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +5.7 (-11.4, +35.5) | 60/84 | 73/84 |
