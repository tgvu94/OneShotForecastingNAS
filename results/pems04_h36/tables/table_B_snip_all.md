# Table B — Experiment B, base = snip_all

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=34) | uses-A archs only (n=28) | beats 0.737? |
|---|---|---|---|---|---|---|
| snip_all alone (under A) | 50 | -0.29 (-0.55, -0.01) | -0.22 | -0.32 | -0.31 | no |
| S_spatial (snip_all) | 50 | -0.13 (-0.42, 0.16) | -0.09 | -0.16 | -0.11 | no |
| z_spatial (snip_all) | 50 | -0.14 (-0.44, 0.15) | -0.10 | -0.18 | -0.15 | no |
| composite = z(snip_all) + z(S_spatial) | 50 | -0.30 (-0.56, -0.02) | -0.21 | -0.34 | -0.29 | no |
| composite = z(snip_all) + z(z_spatial) | 50 | -0.34 (-0.60, -0.05) | -0.24 | -0.40 | -0.38 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 22 | 0.0e+00 | 28 | +18.5 (+3.0, +49.2) | 28/28 | 28/28 |
| `zico` | 22 | 0.0e+00 | 28 | +1.4 (-1.3, +5.9) | 6/28 | 26/28 |
| `grad_norm_all` | 22 | 0.0e+00 | 28 | +7.6 (-0.4, +24.7) | 21/28 | 27/28 |
| `snip_all` | 22 | 0.0e+00 | 28 | +5.8 (+0.1, +25.9) | 16/28 | 28/28 |
