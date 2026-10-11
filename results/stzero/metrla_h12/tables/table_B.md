# Table B — Experiment B, base = nwot

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=34) | uses-A archs only (n=28) | beats 0.737? |
|---|---|---|---|---|---|---|
| nwot alone (under A) | 50 | 0.05 (-0.25, 0.34) | 0.04 | 0.09 | 0.05 | no |
| S_spatial (nwot) | 50 | 0.03 (-0.26, 0.30) | 0.02 | -0.02 | -0.01 | no |
| z_spatial (nwot) | 50 | -0.02 (-0.29, 0.26) | -0.00 | -0.11 | -0.15 | no |
| composite = z(nwot) + z(S_spatial) | 50 | 0.03 (-0.24, 0.31) | 0.02 | 0.01 | -0.01 | no |
| composite = z(nwot) + z(z_spatial) | 50 | 0.00 (-0.27, 0.29) | 0.02 | -0.03 | -0.06 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 22 | 0.0e+00 | 28 | +93.0 (+45.6, +161.5) | 28/28 | 28/28 |
| `zico` | 22 | 0.0e+00 | 28 | +1.9 (-1.3, +11.7) | 6/28 | 23/28 |
| `grad_norm_all` | 22 | 0.0e+00 | 28 | +5.6 (-17.9, +33.2) | 17/28 | 22/28 |
| `snip_all` | 22 | 0.0e+00 | 28 | +4.2 (-11.4, +28.5) | 17/28 | 21/28 |
