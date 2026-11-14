# Table B — Experiment B, base = glass_t

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| glass_t alone (under A) | 150 | 0.53 (0.40, 0.64) | 0.37 | 0.50 | 0.51 | no |
| S_spatial (glass_t) | 150 | -0.23 (-0.38, -0.07) | -0.16 | -0.02 | 0.05 | no |
| z_spatial (glass_t) | 150 | 0.00 (-0.16, 0.16) | -0.00 | -0.00 | 0.01 | no |
| composite = z(glass_t) + z(S_spatial) | 150 | 0.21 (0.05, 0.36) | 0.15 | 0.28 | 0.33 | no |
| composite = z(glass_t) + z(z_spatial) | 150 | 0.42 (0.27, 0.55) | 0.29 | 0.36 | 0.35 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +6.1 (+0.9, +9.4) | 81/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +0.2 (-1.7, +3.0) | 0/84 | 51/84 |
| `zico_t` | 66 | 0.0e+00 | 84 | -0.2 (-2.0, +2.2) | 0/84 | 37/84 |
| `zico_s` | 66 | 0.0e+00 | 84 | +1.1 (-3.2, +5.1) | 6/84 | 68/84 |
| `glass` | 66 | 0.0e+00 | 84 | -0.0 (-1.8, +2.2) | 0/84 | 49/84 |
| `glass_t` | 66 | 0.0e+00 | 84 | -0.1 (-1.8, +2.2) | 0/84 | 40/84 |
| `glass_s` | 66 | 0.0e+00 | 84 | +0.7 (-3.2, +5.1) | 4/84 | 68/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +2.2 (-2.5, +8.6) | 30/84 | 74/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +1.4 (-2.1, +7.6) | 23/84 | 72/84 |
