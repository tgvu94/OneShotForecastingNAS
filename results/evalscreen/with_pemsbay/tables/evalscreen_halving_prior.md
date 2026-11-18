# evalscreen halving_prior: successive halving with a prior (r0 = 1, eta = 3)

filter = the prior keeps the top third with no training, then plain halving; blend = rung score 0.5 z(prior) + 0.5 z(-val MAE) at the first rung, the prior weight halved at each later rung. Warm priors are fit on the other cities: pooled = mean label rank, opcount = boosting on operator counts, proxymix = boosting on the proxies and the head. The cold prior is the size-controlled ZiCo of the city. eff = the median cost share over the subsets, or 100 when fewer than 90 % of the subsets meet the line. The setting of each held-out city is the one with the lowest mean eff on the other three cities.

### Verdict

| setting | cities_le_10pct | cities_below_all_refs | cities_fewer_drops | pass |
|---|---|---|---|---|
| cold | 0 | 2 | 3 | False |
| warm | 0 | 3 | 6 | False |

### The setting chosen on the other cities, read at the held-out city

| setting | held_out | chosen_on_other_cities | eff_cost | sub_share | dropped_first_rung | plain_dropped_first_rung | ref_sh_plain | ref_zico_sizectrl_half_then_k5 | ref_early_val_k5 | ref_transfer_pooled | le_10pct | below_all_refs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| warm | metrla | sh_warm_opcount_filter | 100.000 | 0.835 | 2.000 | 3.000 | 17.418 | 18.341 | 32.241 | 1.424 | False | False |
| warm | pems04 | sh_warm_proxymix_blend | 14.785 | 0.990 | 2.000 | 8.000 | 100.000 | 14.809 | 26.736 | 1.556 | False | True |
| warm | chengdu | sh_warm_proxymix_blend | 100.000 | 0.755 | 5.000 | 9.000 | 100.000 | 100.000 | 100.000 | 100.000 | False | False |
| warm | shenzhen | sh_warm_proxymix_blend | 14.431 | 1.000 | 5.000 | 7.000 | 15.131 | 16.308 | 28.775 | 0.940 | False | True |
| warm | expytky | sh_warm_proxymix_blend | 17.574 | 1.000 | 3.000 | 5.000 | 18.214 | 20.647 | 37.006 | 0.925 | False | True |
| warm | pemsbay | sh_warm_proxymix_blend | 14.961 | 1.000 | 1.000 | 2.000 | 14.576 | 16.892 | 29.917 | 1.065 | False | False |
| cold | metrla | sh_cold_zico_sizectrl_blend | 18.078 | 1.000 | 3.000 | 3.000 | 17.418 | 18.341 | 32.241 | 1.424 | False | False |
| cold | pems04 | sh_cold_zico_sizectrl_blend | 15.025 | 0.965 | 2.000 | 8.000 | 100.000 | 14.809 | 26.736 | 1.556 | False | False |
| cold | chengdu | sh_cold_zico_sizectrl_blend | 100.000 | 0.755 | 4.000 | 9.000 | 100.000 | 100.000 | 100.000 | 100.000 | False | False |
| cold | shenzhen | sh_cold_zico_sizectrl_blend | 15.046 | 0.970 | 3.000 | 7.000 | 15.131 | 16.308 | 28.775 | 0.940 | False | True |
| cold | expytky | sh_cold_zico_sizectrl_blend | 17.962 | 1.000 | 6.000 | 5.000 | 18.214 | 20.647 | 37.006 | 0.925 | False | True |
| cold | pemsbay | sh_cold_zico_sizectrl_blend | 16.095 | 0.945 | 5.000 | 2.000 | 14.576 | 16.892 | 29.917 | 1.065 | False | False |

### eff, every setting

| evaluator | chengdu | expytky | metrla | pems04 | pemsbay | shenzhen |
|---|---|---|---|---|---|---|
| early_val_k5 | 100.000 | 37.006 | 32.241 | 26.736 | 29.917 | 28.775 |
| sh_cold_zico_sizectrl_blend | 100.000 | 17.962 | 18.078 | 15.025 | 16.095 | 15.046 |
| sh_cold_zico_sizectrl_filter | 100.000 | 6.208 | 6.346 | 100.000 | 5.224 | 100.000 |
| sh_plain | 100.000 | 18.214 | 17.418 | 100.000 | 14.576 | 15.131 |
| sh_warm_opcount_blend | 100.000 | 17.282 | 17.783 | 14.771 | 15.223 | 14.522 |
| sh_warm_opcount_filter | 100.000 | 5.440 | 100.000 | 9.637 | 4.935 | 9.133 |
| sh_warm_pooled_blend | 100.000 | 17.766 | 17.366 | 14.729 | 14.959 | 14.466 |
| sh_warm_pooled_filter | 100.000 | 5.734 | 100.000 | 6.907 | 4.692 | 100.000 |
| sh_warm_proxymix_blend | 100.000 | 17.574 | 17.344 | 14.785 | 14.961 | 14.431 |
| sh_warm_proxymix_filter | 100.000 | 5.628 | 100.000 | 6.890 | 4.632 | 100.000 |
| transfer_pooled | 100.000 | 0.925 | 1.424 | 1.556 | 1.065 | 0.940 |
| zico_sizectrl_half_then_k5 | 100.000 | 20.647 | 18.341 | 14.809 | 16.892 | 16.308 |

### Top-15 architectures dropped at the first rung

| evaluator | chengdu | expytky | metrla | pems04 | pemsbay | shenzhen |
|---|---|---|---|---|---|---|
| early_val_k5 |  |  |  |  |  |  |
| sh_cold_zico_sizectrl_blend | 4.000 | 6.000 | 3.000 | 2.000 | 5.000 | 3.000 |
| sh_cold_zico_sizectrl_filter | 2.000 | 8.000 | 6.000 | 4.000 | 8.000 | 4.000 |
| sh_plain | 9.000 | 5.000 | 3.000 | 8.000 | 2.000 | 7.000 |
| sh_warm_opcount_blend | 5.000 | 3.000 | 2.000 | 2.000 | 1.000 | 5.000 |
| sh_warm_opcount_filter | 1.000 | 4.000 | 2.000 | 1.000 | 4.000 | 1.000 |
| sh_warm_pooled_blend | 6.000 | 3.000 | 2.000 | 2.000 | 1.000 | 5.000 |
| sh_warm_pooled_filter | 2.000 | 1.000 | 2.000 | 1.000 | 3.000 | 1.000 |
| sh_warm_proxymix_blend | 5.000 | 3.000 | 1.000 | 2.000 | 1.000 | 5.000 |
| sh_warm_proxymix_filter | 2.000 | 1.000 | 1.000 | 1.000 | 2.000 | 2.000 |
| transfer_pooled |  |  |  |  |  |  |
| zico_sizectrl_half_then_k5 |  |  |  |  |  |  |
