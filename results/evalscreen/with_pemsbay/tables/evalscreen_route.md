# evalscreen route: a few probe trainings choose the recipe

Probes: the first 5 architectures of the list, trained 3 epochs. Features: the median ratio of the val MAE at epoch 3 to epoch 1, the spread of the probes at epoch 3, and the agreement of the prior with the probes. Rule: take the cheapest recipe of the training city whose probe features are nearest. fixed = the recipe with the lowest mean eff on the three training cities. oracle = the cheapest recipe of the held-out city. eff as in halving_prior; the rule pays the probes.

### Verdict

| setting | cities_within_1_25 | rule_mean | fixed_mean | oracle_mean | pass |
|---|---|---|---|---|---|
| cold | 2 | 55.831 | 44.530 | 22.930 | False |
| warm | 1 | 20.303 | 17.661 | 17.600 | False |

### Held-out decisions

| setting | held_out | oracle_recipe | oracle_eff | nearest_city | rule_recipe | rule_eff_with_probes | fixed_recipe | fixed_eff | rule_within_1.25_oracle |
|---|---|---|---|---|---|---|---|---|---|
| cold | metrla | sh_cold_zico_sizectrl_filter | 6.346 | shenzhen | zico_sizectrl_half_then_k3 | 12.379 | sh_cold_zico_sizectrl_blend | 18.078 | False |
| cold | pems04 | zico_sizectrl | 6.444 | pemsbay | sh_cold_zico_sizectrl_filter | 100.501 | zico_sizectrl_half_then_k3 | 100.000 | False |
| cold | chengdu | early_val_k2 | 100.000 | pemsbay | sh_cold_zico_sizectrl_filter | 100.585 | sh_cold_zico_sizectrl_blend | 100.000 | True |
| cold | shenzhen | zico_sizectrl_half_then_k3 | 13.356 | metrla | sh_cold_zico_sizectrl_filter | 100.529 | sh_cold_zico_sizectrl_blend | 15.046 | False |
| cold | expytky | sh_cold_zico_sizectrl_filter | 6.208 | metrla | sh_cold_zico_sizectrl_filter | 6.871 | sh_cold_zico_sizectrl_blend | 17.962 | True |
| cold | pemsbay | sh_cold_zico_sizectrl_filter | 5.224 | chengdu | early_val_k2 | 14.124 | sh_cold_zico_sizectrl_blend | 16.095 | False |
| warm | metrla | transfer_pooled | 1.424 | shenzhen | transfer_pooled | 1.993 | loco_gbr_arch | 1.462 | False |
| warm | pems04 | loco_gbr_arch | 1.556 | pemsbay | transfer_pooled | 2.057 | loco_gbr_arch | 1.556 | False |
| warm | chengdu | early_val_k2 | 100.000 | shenzhen | transfer_pooled | 100.585 | loco_gbr_arch | 100.000 | True |
| warm | shenzhen | transfer_pooled | 0.940 | metrla | transfer_pooled | 1.469 | loco_gbr_arch | 0.945 | False |
| warm | expytky | loco_gbr_arch | 0.618 | pemsbay | transfer_pooled | 1.588 | transfer_pooled | 0.925 | False |
| warm | pemsbay | transfer_pooled | 1.065 | chengdu | early_val_k2 | 14.124 | loco_gbr_arch | 1.078 | False |

### Probe features

| city | improve_1_to_3 | probe_cv_k3 | agree_cold_prior | agree_warm_prior |
|---|---|---|---|---|
| metrla | 0.958 | 0.013 | -0.500 | -0.400 |
| pems04 | 0.885 | 0.060 | 0.900 | -1.000 |
| chengdu | 0.945 | 0.008 | 0.600 | -0.900 |
| shenzhen | 0.940 | 0.005 | -0.300 | -0.600 |
| expytky | 0.980 | 0.031 | -0.300 | 0.700 |
| pemsbay | 0.962 | 0.032 | 0.600 | -0.300 |
