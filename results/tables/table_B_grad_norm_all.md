# Table B — Experiment B, base = grad_norm_all

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=204) | uses-A archs only (n=168) | beats 0.737? |
|---|---|---|---|---|---|---|
| grad_norm_all alone (under A) | 300 | -0.13 (-0.23, -0.01) | -0.08 | -0.07 | -0.11 | no |
| S_spatial (grad_norm_all) | 300 | 0.21 (0.10, 0.31) | 0.15 | -0.14 | -0.18 | no |
| z_spatial (grad_norm_all) | 300 | 0.14 (0.04, 0.25) | 0.10 | -0.23 | -0.30 | no |
| composite = z(grad_norm_all) + z(S_spatial) | 300 | -0.06 (-0.17, 0.05) | -0.04 | -0.14 | -0.18 | no |
| composite = z(grad_norm_all) + z(z_spatial) | 300 | -0.02 (-0.13, 0.09) | -0.01 | -0.26 | -0.33 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 132 | 0.0e+00 | 168 | +21.2 (+0.1, +53.6) | 167/168 | 168/168 |
| `zico` | 132 | 0.0e+00 | 168 | +1.8 (-1.4, +10.7) | 44/168 | 155/168 |
| `grad_norm_all` | 132 | 0.0e+00 | 168 | +8.8 (-3.5, +26.2) | 145/168 | 164/168 |
| `snip_all` | 132 | 0.0e+00 | 168 | +5.9 (-5.0, +25.0) | 123/168 | 165/168 |
