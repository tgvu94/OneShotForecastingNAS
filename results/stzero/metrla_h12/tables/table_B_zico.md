# Table B — Experiment B, base = zico

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| zico alone (under A) | 150 | 0.01 (-0.14, 0.16) | 0.01 | 0.05 | 0.05 | no |
| S_spatial (zico) | 150 | 0.00 (-0.16, 0.15) | 0.00 | 0.15 | 0.27 | no |
| z_spatial (zico) | 150 | -0.07 (-0.21, 0.09) | -0.04 | -0.06 | -0.06 | no |
| composite = z(zico) + z(S_spatial) | 150 | 0.01 (-0.15, 0.15) | 0.00 | 0.12 | 0.20 | no |
| composite = z(zico) + z(z_spatial) | 150 | -0.07 (-0.22, 0.08) | -0.05 | -0.03 | -0.02 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +87.9 (+45.6, +161.5) | 84/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +1.8 (-1.3, +11.7) | 20/84 | 71/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +7.2 (-17.9, +43.6) | 60/84 | 70/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +5.7 (-11.4, +35.5) | 60/84 | 73/84 |
