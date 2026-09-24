# Table B — Experiment B, base = nwot

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=34) | uses-A archs only (n=28) | beats 0.737? |
|---|---|---|---|---|---|---|
| nwot alone (under A) | 50 | 0.17 (-0.14, 0.44) | 0.11 | 0.05 | 0.05 | no |
| S_spatial (nwot) | 50 | 0.01 (-0.27, 0.27) | -0.01 | -0.18 | -0.12 | no |
| z_spatial (nwot) | 50 | 0.08 (-0.19, 0.34) | 0.06 | -0.02 | 0.13 | no |
| composite = z(nwot) + z(S_spatial) | 50 | 0.10 (-0.20, 0.34) | 0.05 | -0.13 | -0.10 | no |
| composite = z(nwot) + z(z_spatial) | 50 | 0.16 (-0.12, 0.40) | 0.10 | 0.01 | 0.11 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 22 | 0.0e+00 | 28 | +20.2 (+3.4, +49.8) | 28/28 | 28/28 |
| `zico` | 22 | 0.0e+00 | 28 | +2.2 (-1.1, +5.9) | 9/28 | 25/28 |
| `grad_norm_all` | 22 | 0.0e+00 | 28 | +8.8 (+1.4, +23.0) | 25/28 | 28/28 |
| `snip_all` | 22 | 0.0e+00 | 28 | +5.9 (+0.2, +23.6) | 22/28 | 28/28 |
