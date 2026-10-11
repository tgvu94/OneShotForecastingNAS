# Table B — Experiment B, base = nwot

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=102) | uses-A archs only (n=84) | beats 0.737? |
|---|---|---|---|---|---|---|
| nwot alone (under A) | 150 | 0.05 (-0.11, 0.22) | 0.04 | -0.03 | 0.01 | no |
| S_spatial (nwot) | 150 | 0.14 (-0.02, 0.30) | 0.10 | 0.10 | 0.10 | no |
| z_spatial (nwot) | 150 | 0.19 (0.03, 0.34) | 0.13 | 0.20 | 0.25 | no |
| composite = z(nwot) + z(S_spatial) | 150 | 0.10 (-0.06, 0.26) | 0.06 | 0.07 | 0.09 | no |
| composite = z(nwot) + z(z_spatial) | 150 | 0.14 (-0.02, 0.30) | 0.09 | 0.16 | 0.23 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 66 | 0.0e+00 | 84 | +13.1 (+2.3, +34.7) | 81/84 | 84/84 |
| `zico` | 66 | 0.0e+00 | 84 | +0.3 (-2.0, +2.5) | 0/84 | 53/84 |
| `grad_norm_all` | 66 | 0.0e+00 | 84 | +3.9 (-1.2, +13.3) | 48/84 | 80/84 |
| `snip_all` | 66 | 0.0e+00 | 84 | +2.6 (-3.5, +12.6) | 39/84 | 77/84 |
