# Table B — Experiment B, base = zico

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=34) | uses-A archs only (n=28) | beats 0.737? |
|---|---|---|---|---|---|---|
| zico alone (under A) | 50 | 0.65 (0.45, 0.78) | 0.46 | 0.58 | 0.48 | no |
| S_spatial (zico) | 50 | -0.01 (-0.29, 0.25) | -0.00 | -0.19 | -0.16 | no |
| z_spatial (zico) | 50 | 0.00 (-0.27, 0.26) | 0.00 | -0.15 | -0.16 | no |
| composite = z(zico) + z(S_spatial) | 50 | 0.44 (0.16, 0.66) | 0.33 | 0.27 | 0.34 | no |
| composite = z(zico) + z(z_spatial) | 50 | 0.47 (0.18, 0.68) | 0.34 | 0.31 | 0.36 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 22 | 0.0e+00 | 28 | +20.2 (+3.4, +49.8) | 28/28 | 28/28 |
| `zico` | 22 | 0.0e+00 | 28 | +2.2 (-1.1, +5.9) | 9/28 | 25/28 |
| `grad_norm_all` | 22 | 0.0e+00 | 28 | +8.8 (+1.4, +23.0) | 25/28 | 28/28 |
| `snip_all` | 22 | 0.0e+00 | 28 | +5.9 (+0.2, +23.6) | 22/28 | 28/28 |
