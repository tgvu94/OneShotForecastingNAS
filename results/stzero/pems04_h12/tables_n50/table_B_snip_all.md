# Table B — Experiment B, base = snip_all

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=34) | uses-A archs only (n=28) | beats 0.737? |
|---|---|---|---|---|---|---|
| snip_all alone (under A) | 50 | -0.26 (-0.52, 0.04) | -0.17 | -0.24 | -0.20 | no |
| S_spatial (snip_all) | 50 | -0.08 (-0.38, 0.22) | -0.06 | -0.33 | -0.39 | no |
| z_spatial (snip_all) | 50 | -0.05 (-0.35, 0.23) | -0.03 | -0.28 | -0.29 | no |
| composite = z(snip_all) + z(S_spatial) | 50 | -0.31 (-0.56, -0.02) | -0.20 | -0.43 | -0.38 | no |
| composite = z(snip_all) + z(z_spatial) | 50 | -0.30 (-0.55, -0.00) | -0.20 | -0.52 | -0.45 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 22 | 0.0e+00 | 28 | +20.2 (+3.4, +49.8) | 28/28 | 28/28 |
| `zico` | 22 | 0.0e+00 | 28 | +2.2 (-1.1, +5.9) | 9/28 | 25/28 |
| `grad_norm_all` | 22 | 0.0e+00 | 28 | +8.8 (+1.4, +23.0) | 25/28 | 28/28 |
| `snip_all` | 22 | 0.0e+00 | 28 | +5.9 (+0.2, +23.6) | 22/28 | 28/28 |
