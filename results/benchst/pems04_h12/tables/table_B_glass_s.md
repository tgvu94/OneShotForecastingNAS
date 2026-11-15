# Table B — Experiment B, base = glass_s

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| glass_s alone (under A) | 150 | 0.29 (0.14, 0.44) | 0.20 | 0.10 | 0.14 | no |
| S_spatial (glass_s) | 150 | 0.14 (-0.02, 0.29) | 0.10 | -0.11 | -0.08 | no |
| z_spatial (glass_s) | 150 | 0.13 (-0.03, 0.29) | 0.09 | -0.13 | -0.11 | no |
| composite = z(glass_s) + z(S_spatial) | 150 | 0.24 (0.08, 0.39) | 0.17 | -0.01 | 0.03 | no |
| composite = z(glass_s) + z(z_spatial) | 150 | 0.23 (0.07, 0.39) | 0.16 | -0.02 | 0.02 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +23.7 (+3.4, +49.8) | 84/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +1.6 (-0.9, +7.0) | 19/84 | 77/84 |
| `zico_t` | 66 | 0.0e+00 | 84 | +0.1 (-1.6, +2.7) | 0/84 | 49/84 |
| `zico_s` | 66 | 0.0e+00 | 84 | +7.5 (+0.4, +16.5) | 76/84 | 84/84 |
| `glass` | 66 | 0.0e+00 | 84 | +1.5 (-0.8, +8.0) | 17/84 | 80/84 |
| `glass_t` | 66 | 0.0e+00 | 84 | +0.1 (-1.6, +2.4) | 0/84 | 46/84 |
| `glass_s` | 66 | 0.0e+00 | 84 | +7.4 (+1.4, +16.0) | 75/84 | 84/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +8.5 (-2.1, +27.0) | 72/84 | 83/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +6.1 (-3.1, +25.1) | 66/84 | 82/84 |
