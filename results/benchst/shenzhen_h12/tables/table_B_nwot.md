# Table B — Experiment B, base = nwot

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| nwot alone (under A) | 150 | -0.05 (-0.22, 0.12) | -0.04 | 0.04 | 0.05 | no |
| S_spatial (nwot) | 150 | -0.11 (-0.27, 0.06) | -0.08 | -0.10 | -0.09 | no |
| z_spatial (nwot) | 150 | -0.06 (-0.22, 0.11) | -0.04 | 0.01 | 0.07 | no |
| composite = z(nwot) + z(S_spatial) | 150 | -0.08 (-0.25, 0.10) | -0.06 | -0.05 | -0.04 | no |
| composite = z(nwot) + z(z_spatial) | 150 | -0.05 (-0.23, 0.12) | -0.04 | 0.02 | 0.06 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +11.0 (+6.3, +17.6) | 84/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +0.1 (-2.0, +3.9) | 1/84 | 48/84 |
| `zico_t` | 66 | 0.0e+00 | 84 | +0.0 (-1.5, +3.4) | 1/84 | 43/84 |
| `zico_s` | 66 | 0.0e+00 | 84 | +1.1 (-2.0, +4.9) | 9/84 | 61/84 |
| `glass` | 66 | 0.0e+00 | 84 | -0.0 (-2.5, +3.2) | 1/84 | 44/84 |
| `glass_t` | 66 | 0.0e+00 | 84 | -0.2 (-2.7, +3.4) | 1/84 | 34/84 |
| `glass_s` | 66 | 0.0e+00 | 84 | +1.0 (-2.0, +5.0) | 5/84 | 62/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +2.1 (-3.6, +12.7) | 35/84 | 68/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +1.6 (-2.5, +10.2) | 23/84 | 69/84 |
