# evalscreen halving_prior: successive halving with a prior (r0 = 1, eta = 3)

filter = the prior keeps the top third with no training, then plain halving; blend = rung score 0.5 z(prior) + 0.5 z(-val MAE) at the first rung, the prior weight halved at each later rung. Warm priors are fit on the other cities: pooled = mean label rank, opcount = boosting on operator counts, proxymix = boosting on the proxies and the head. The cold prior is the size-controlled ZiCo of the city. eff = the median cost share over the subsets, or 100 when fewer than 90 % of the subsets meet the line. The setting of each held-out city is the one with the lowest mean eff on the other three cities.

### Verdict

| setting | cities_le_10pct | cities_below_all_refs | cities_fewer_drops | pass |
|---|---|---|---|---|
| cold | 0 | 0 | 3 | False |
| warm | 0 | 1 | 4 | False |

### The setting chosen on the other cities, read at the held-out city

| setting | held_out | chosen_on_other_cities | eff_cost | sub_share | dropped_first_rung | plain_dropped_first_rung | ref_sh_plain | ref_zico_sizectrl_half_then_k5 | ref_early_val_k5 | ref_transfer_pooled | le_10pct | below_all_refs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| warm | metrla | sh_warm_proxymix_blend | 17.567 | 1.000 | 1.000 | 3.000 | 17.418 | 18.337 | 32.199 | 0.840 | False | False |
| warm | pems04 | sh_warm_proxymix_blend | 14.904 | 0.975 | 2.000 | 8.000 | 100.000 | 14.809 | 26.736 | 4.346 | False | False |
| warm | chengdu | sh_warm_opcount_filter | 100.000 | 0.775 | 0.000 | 9.000 | 100.000 | 17.313 | 31.053 | 1.828 | False | False |
| warm | shenzhen | sh_warm_pooled_blend | 14.782 | 1.000 | 4.000 | 7.000 | 15.131 | 16.308 | 28.775 | 0.926 | False | True |
| cold | metrla | sh_cold_zico_sizectrl_blend | 18.078 | 1.000 | 3.000 | 3.000 | 17.418 | 18.337 | 32.199 | 0.840 | False | False |
| cold | pems04 | sh_cold_zico_sizectrl_blend | 100.000 | 0.895 | 2.000 | 8.000 | 100.000 | 14.809 | 26.736 | 4.346 | False | False |
| cold | chengdu | sh_cold_zico_sizectrl_blend | 100.000 | 0.835 | 4.000 | 9.000 | 100.000 | 17.313 | 31.053 | 1.828 | False | False |
| cold | shenzhen | sh_cold_zico_sizectrl_filter | 100.000 | 0.160 | 4.000 | 7.000 | 15.131 | 16.308 | 28.775 | 0.926 | False | False |

### eff, every setting

| evaluator | chengdu | metrla | pems04 | shenzhen |
|---|---|---|---|---|
| early_val_k5 | 31.053 | 32.199 | 26.736 | 28.775 |
| sh_cold_zico_sizectrl_blend | 100.000 | 18.078 | 100.000 | 15.046 |
| sh_cold_zico_sizectrl_filter | 100.000 | 6.113 | 100.000 | 100.000 |
| sh_plain | 100.000 | 17.418 | 100.000 | 15.131 |
| sh_warm_opcount_blend | 15.933 | 17.860 | 100.000 | 14.507 |
| sh_warm_opcount_filter | 100.000 | 6.107 | 9.926 | 7.504 |
| sh_warm_pooled_blend | 15.937 | 17.392 | 14.843 | 14.782 |
| sh_warm_pooled_filter | 100.000 | 5.862 | 100.000 | 100.000 |
| sh_warm_proxymix_blend | 15.820 | 17.567 | 14.904 | 14.548 |
| sh_warm_proxymix_filter | 100.000 | 5.948 | 10.316 | 100.000 |
| transfer_pooled | 1.828 | 0.840 | 4.346 | 0.926 |
| zico_sizectrl_half_then_k5 | 17.313 | 18.337 | 14.809 | 16.308 |

### Top-15 architectures dropped at the first rung

| evaluator | chengdu | metrla | pems04 | shenzhen |
|---|---|---|---|---|
| early_val_k5 |  |  |  |  |
| sh_cold_zico_sizectrl_blend | 4.000 | 3.000 | 2.000 | 3.000 |
| sh_cold_zico_sizectrl_filter | 2.000 | 6.000 | 4.000 | 4.000 |
| sh_plain | 9.000 | 3.000 | 8.000 | 7.000 |
| sh_warm_opcount_blend | 4.000 | 2.000 | 2.000 | 5.000 |
| sh_warm_opcount_filter | 0.000 | 3.000 | 1.000 | 0.000 |
| sh_warm_pooled_blend | 4.000 | 3.000 | 2.000 | 4.000 |
| sh_warm_pooled_filter | 1.000 | 3.000 | 1.000 | 0.000 |
| sh_warm_proxymix_blend | 3.000 | 1.000 | 2.000 | 4.000 |
| sh_warm_proxymix_filter | 2.000 | 2.000 | 1.000 | 1.000 |
| transfer_pooled |  |  |  |  |
| zico_sizectrl_half_then_k5 |  |  |  |  |
