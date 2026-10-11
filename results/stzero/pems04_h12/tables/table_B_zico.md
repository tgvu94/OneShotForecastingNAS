# Table B — Experiment B, base = zico

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=204) | uses-A archs only (n=168) | beats 0.737? |
|---|---|---|---|---|---|---|
| zico alone (under A) | 300 | 0.57 (0.48, 0.65) | 0.40 | 0.62 | 0.58 | no |
| S_spatial (zico) | 300 | 0.28 (0.18, 0.38) | 0.20 | 0.01 | 0.05 | no |
| z_spatial (zico) | 300 | 0.13 (0.02, 0.24) | 0.09 | -0.17 | -0.21 | no |
| composite = z(zico) + z(S_spatial) | 300 | 0.55 (0.47, 0.63) | 0.39 | 0.43 | 0.46 | no |
| composite = z(zico) + z(z_spatial) | 300 | 0.49 (0.39, 0.57) | 0.33 | 0.31 | 0.30 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 132 | 0.0e+00 | 168 | +21.2 (+0.1, +53.6) | 167/168 | 168/168 |
| `zico` | 132 | 0.0e+00 | 168 | +1.8 (-1.4, +10.7) | 44/168 | 155/168 |
| `grad_norm_all` | 132 | 0.0e+00 | 168 | +8.8 (-3.5, +26.2) | 145/168 | 164/168 |
| `snip_all` | 132 | 0.0e+00 | 168 | +5.9 (-5.0, +25.0) | 123/168 | 165/168 |
