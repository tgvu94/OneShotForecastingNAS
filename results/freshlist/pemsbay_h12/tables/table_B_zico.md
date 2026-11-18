# Table B — Experiment B, base = zico

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| zico alone (under A) | 150 | 0.22 (0.06, 0.37) | 0.15 | 0.29 | 0.24 | no |
| S_spatial (zico) | 150 | 0.12 (-0.05, 0.27) | 0.08 | 0.06 | -0.08 | no |
| z_spatial (zico) | 150 | -0.07 (-0.23, 0.09) | -0.05 | -0.18 | -0.34 | no |
| composite = z(zico) + z(S_spatial) | 150 | 0.19 (0.03, 0.34) | 0.13 | 0.20 | 0.10 | no |
| composite = z(zico) + z(z_spatial) | 150 | 0.09 (-0.08, 0.24) | 0.06 | 0.06 | -0.06 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +176.1 (+107.0, +235.2) | 84/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +1.8 (-1.3, +18.6) | 27/84 | 70/84 |
| `zico_t` | 66 | 0.0e+00 | 84 | +0.1 (-1.8, +4.5) | 2/84 | 44/84 |
| `zico_s` | 66 | 0.0e+00 | 84 | +9.2 (-7.7, +39.8) | 75/84 | 81/84 |
| `glass` | 66 | 0.0e+00 | 84 | +1.2 (-2.1, +12.3) | 21/84 | 69/84 |
| `glass_t` | 66 | 0.0e+00 | 84 | -0.0 (-2.9, +3.4) | 1/84 | 37/84 |
| `glass_s` | 66 | 0.0e+00 | 84 | +8.3 (-7.7, +39.8) | 71/84 | 77/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +12.8 (-20.0, +65.1) | 76/84 | 76/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +8.4 (-6.6, +52.5) | 70/84 | 76/84 |
