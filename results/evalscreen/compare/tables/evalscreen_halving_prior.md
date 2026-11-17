# evalscreen halving_prior: successive halving with a prior (r0 = 1, eta = 3)

filter = the prior keeps the top third with no training, then plain halving; blend = rung score 0.5 z(prior) + 0.5 z(-val MAE) at the first rung, the prior weight halved at each later rung. Warm priors are fit on the other cities: pooled = mean label rank, opcount = boosting on operator counts, proxymix = boosting on the proxies and the head. The cold prior is the size-controlled ZiCo of the city. eff = the median cost share over the subsets, or 100 when fewer than 90 % of the subsets meet the line. The setting of each held-out city is the one with the lowest mean eff on the other three cities.

### Verdict

| setting | cities_le_10pct | cities_below_all_refs | cities_fewer_drops | pass |
|---|---|---|---|---|
| cold | 0 | 1 | 3 | False |
| warm | 0 | 1 | 3 | False |

### The setting chosen on the other cities, read at the held-out city

| setting | held_out | chosen_on_other_cities | eff_cost | sub_share | dropped_first_rung | plain_dropped_first_rung | ref_sh_plain | ref_zico_sizectrl_half_then_k5 | ref_early_val_k5 | ref_transfer_pooled | le_10pct | below_all_refs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| warm | metrla | sh_warm_opcount_filter | 100.000 | 0.840 | 3.000 | 3.000 | 17.418 | 18.341 | 32.241 | 2.185 | False | False |
| warm | pems04 | sh_warm_proxymix_blend | 14.888 | 0.990 | 2.000 | 8.000 | 100.000 | 14.809 | 26.736 | 2.192 | False | False |
| warm | chengdu | sh_warm_proxymix_blend | 100.000 | 0.755 | 3.000 | 9.000 | 100.000 | 100.000 | 100.000 | 100.000 | False | False |
| warm | shenzhen | sh_warm_pooled_blend | 14.782 | 1.000 | 4.000 | 7.000 | 15.131 | 16.308 | 28.775 | 0.926 | False | True |
| cold | metrla | sh_cold_zico_sizectrl_blend | 18.078 | 1.000 | 3.000 | 3.000 | 17.418 | 18.341 | 32.241 | 2.185 | False | False |
| cold | pems04 | sh_cold_zico_sizectrl_blend | 15.025 | 0.965 | 2.000 | 8.000 | 100.000 | 14.809 | 26.736 | 2.192 | False | False |
| cold | chengdu | sh_cold_zico_sizectrl_blend | 100.000 | 0.755 | 4.000 | 9.000 | 100.000 | 100.000 | 100.000 | 100.000 | False | False |
| cold | shenzhen | sh_cold_zico_sizectrl_blend | 15.046 | 0.970 | 3.000 | 7.000 | 15.131 | 16.308 | 28.775 | 0.926 | False | True |

### eff, every setting

| evaluator | chengdu | metrla | pems04 | shenzhen |
|---|---|---|---|---|
| early_val_k5 | 100.000 | 32.241 | 26.736 | 28.775 |
| sh_cold_zico_sizectrl_blend | 100.000 | 18.078 | 15.025 | 15.046 |
| sh_cold_zico_sizectrl_filter | 100.000 | 6.346 | 100.000 | 100.000 |
| sh_plain | 100.000 | 17.418 | 100.000 | 15.131 |
| sh_warm_opcount_blend | 100.000 | 17.860 | 14.762 | 14.507 |
| sh_warm_opcount_filter | 100.000 | 100.000 | 7.019 | 7.504 |
| sh_warm_pooled_blend | 100.000 | 17.392 | 14.837 | 14.782 |
| sh_warm_pooled_filter | 100.000 | 100.000 | 6.927 | 100.000 |
| sh_warm_proxymix_blend | 100.000 | 17.567 | 14.888 | 14.548 |
| sh_warm_proxymix_filter | 100.000 | 100.000 | 7.168 | 100.000 |
| transfer_pooled | 100.000 | 2.185 | 2.192 | 0.926 |
| zico_sizectrl_half_then_k5 | 100.000 | 18.341 | 14.809 | 16.308 |

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
