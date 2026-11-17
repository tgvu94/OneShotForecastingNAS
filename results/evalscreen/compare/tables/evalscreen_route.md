# evalscreen route: a few probe trainings choose the recipe

Probes: the first 5 architectures of the list, trained 3 epochs. Features: the median ratio of the val MAE at epoch 3 to epoch 1, the spread of the probes at epoch 3, and the agreement of the prior with the probes. Rule: take the cheapest recipe of the training city whose probe features are nearest. fixed = the recipe with the lowest mean eff on the three training cities. oracle = the cheapest recipe of the held-out city. eff as in halving_prior; the rule pays the probes.

### Verdict

| setting | cities_within_1_25 | rule_mean | fixed_mean | oracle_mean | pass |
|---|---|---|---|---|---|
| cold | 1 | 78.498 | 58.281 | 31.537 | False |
| warm | 1 | 51.324 | 26.975 | 25.994 | False |

### Held-out decisions

| setting | held_out | oracle_recipe | oracle_eff | nearest_city | rule_recipe | rule_eff_with_probes | fixed_recipe | fixed_eff | rule_within_1.25_oracle |
|---|---|---|---|---|---|---|---|---|---|
| cold | metrla | sh_cold_zico_sizectrl_filter | 6.346 | shenzhen | zico_sizectrl_half_then_k3 | 12.379 | sh_cold_zico_sizectrl_blend | 18.078 | False |
| cold | pems04 | zico_sizectrl | 6.444 | metrla | sh_cold_zico_sizectrl_filter | 100.501 | zico_sizectrl_half_then_k3 | 100.000 | False |
| cold | chengdu | early_val_k2 | 100.000 | shenzhen | zico_sizectrl_half_then_k3 | 100.585 | sh_cold_zico_sizectrl_blend | 100.000 | True |
| cold | shenzhen | zico_sizectrl_half_then_k3 | 13.356 | metrla | sh_cold_zico_sizectrl_filter | 100.529 | sh_cold_zico_sizectrl_blend | 15.046 | False |
| warm | metrla | transfer_pooled | 2.185 | shenzhen | transfer_pooled | 2.755 | loco_gbr_arch | 4.783 | False |
| warm | pems04 | loco_gbr_arch | 0.864 | chengdu | early_val_k2 | 100.501 | transfer_pooled | 2.192 | False |
| warm | chengdu | early_val_k2 | 100.000 | shenzhen | transfer_pooled | 100.585 | transfer_pooled | 100.000 | True |
| warm | shenzhen | transfer_pooled | 0.926 | metrla | transfer_pooled | 1.456 | transfer_pooled | 0.926 | False |

### Probe features

| city | improve_1_to_3 | probe_cv_k3 | agree_cold_prior | agree_warm_prior |
|---|---|---|---|---|
| metrla | 0.958 | 0.013 | -0.500 | -0.300 |
| pems04 | 0.885 | 0.060 | 0.900 | -0.700 |
| chengdu | 0.945 | 0.008 | 0.600 | -0.600 |
| shenzhen | 0.940 | 0.005 | -0.300 | -0.500 |
