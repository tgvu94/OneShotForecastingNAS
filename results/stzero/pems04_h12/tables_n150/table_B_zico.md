# Table B — Experiment B, base = zico

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=83) | uses-A archs only (n=75) | beats 0.737? |
|---|---|---|---|---|---|---|
| zico alone (under A) | 150 | 0.57 (0.44, 0.67) | 0.40 | 0.60 | 0.55 | no |
| S_spatial (zico) | 150 | 0.33 (0.17, 0.47) | 0.24 | -0.06 | -0.07 | no |
| z_spatial (zico) | 150 | 0.18 (0.01, 0.34) | 0.12 | -0.28 | -0.32 | no |
| composite = z(zico) + z(S_spatial) | 150 | 0.58 (0.45, 0.69) | 0.41 | 0.36 | 0.37 | no |
| composite = z(zico) + z(z_spatial) | 150 | 0.53 (0.40, 0.64) | 0.36 | 0.23 | 0.21 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 75 | 0.0e+00 | 75 | +21.1 (+3.4, +49.8) | 75/75 | 75/75 |
| `zico` | 75 | 0.0e+00 | 75 | +1.9 (-1.1, +7.2) | 22/75 | 68/75 |
| `grad_norm_all` | 75 | 0.0e+00 | 75 | +9.3 (-3.5, +26.2) | 63/75 | 73/75 |
| `snip_all` | 75 | 0.0e+00 | 75 | +6.0 (-5.0, +25.0) | 55/75 | 72/75 |
