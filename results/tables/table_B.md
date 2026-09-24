# Table B — Experiment B, base = nwot

Ranking: Spearman with −val MAE (positive = good), 95% bootstrap CI; LENAS naswot reference 0.737 on *its* space.

| Score | N | Spearman (95% CI) | Kendall | graph archs only (n=204) | uses-A archs only (n=168) | beats 0.737? |
|---|---|---|---|---|---|---|
| nwot alone (under A) | 300 | 0.34 (0.24, 0.43) | 0.23 | 0.09 | 0.10 | no |
| S_spatial (nwot) | 300 | 0.24 (0.14, 0.35) | 0.17 | -0.08 | -0.08 | no |
| z_spatial (nwot) | 300 | 0.27 (0.16, 0.37) | 0.19 | -0.01 | 0.01 | no |
| composite = z(nwot) + z(S_spatial) | 300 | 0.30 (0.20, 0.39) | 0.19 | -0.04 | -0.04 | no |
| composite = z(nwot) + z(z_spatial) | 300 | 0.32 (0.22, 0.42) | 0.21 | 0.03 | 0.04 | no |

Detection: z_spatial = (score(A) − mean_j score(π_j(A))) / std_j, mean over 3 init seeds (RNG re-seeded before every forward, spatial_v2).

| Base | controls n | controls max \|z\| | uses-A n | uses-A median z (min, max) | uses-A with \|z\| > 3 | uses-A with score(A) > permuted mean |
|---|---|---|---|---|---|---|
| `nwot` | 132 | 0.0e+00 | 168 | +21.2 (+0.1, +53.6) | 167/168 | 168/168 |
| `zico` | 132 | 0.0e+00 | 168 | +1.8 (-1.4, +10.7) | 44/168 | 155/168 |
| `grad_norm_all` | 132 | 0.0e+00 | 168 | +8.8 (-3.5, +26.2) | 145/168 | 164/168 |
| `snip_all` | 132 | 0.0e+00 | 168 | +5.9 (-5.0, +25.0) | 123/168 | 165/168 |
