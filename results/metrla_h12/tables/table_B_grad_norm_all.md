# Table B — Experiment B, base = grad_norm_all

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=34) | uses-A archs only (n=28) | beats 0.737? |
|---|---|---|---|---|---|---|
| grad_norm_all alone (under A) | 50 | -0.44 (-0.66, -0.15) | -0.29 | -0.37 | -0.29 | no |
| S_spatial (grad_norm_all) | 50 | -0.11 (-0.39, 0.20) | -0.08 | -0.31 | -0.43 | no |
| z_spatial (grad_norm_all) | 50 | -0.01 (-0.30, 0.28) | -0.02 | -0.13 | -0.18 | no |
| composite = z(grad_norm_all) + z(S_spatial) | 50 | -0.47 (-0.66, -0.21) | -0.31 | -0.51 | -0.47 | no |
| composite = z(grad_norm_all) + z(z_spatial) | 50 | -0.44 (-0.65, -0.17) | -0.29 | -0.44 | -0.40 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 22 | 0.0e+00 | 28 | +93.0 (+45.6, +161.5) | 28/28 | 28/28 |
| `zico` | 22 | 0.0e+00 | 28 | +1.9 (-1.3, +11.7) | 6/28 | 23/28 |
| `grad_norm_all` | 22 | 0.0e+00 | 28 | +5.6 (-17.9, +33.2) | 17/28 | 22/28 |
| `snip_all` | 22 | 0.0e+00 | 28 | +4.2 (-11.4, +28.5) | 17/28 | 21/28 |
