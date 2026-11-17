# evalscreen active_labels: an active choice of the labels at the target city

Rounds of 5 labels up to 15. random = random labels; prior = the next five of the prior, no refit; refit = a ridge on the operator counts and the prior, fit on the labels so far, picks four and one random architecture. Warm prior = the pooled transfer rank; cold prior = the size-controlled ZiCo of the city. The pick is the best labelled architecture. regret_n = regret after n labels on the full list (mean of 20 draws where the rule draws); sub_* = the 200 subsets; eff as in halving_prior.

### Verdict

| setting | cities_refit_meets_line | cities_refit_below_random_and_prior | pass |
|---|---|---|---|
| cold | 1 | 0 | False |
| warm | 3 | 0 | False |

### Every rule

| city | setting | rule | regret_n5_sigma | regret_n10_sigma | regret_n15_sigma | sub_share | sub_pct_median | sub_n_median | sub_regret_n5_sigma | sub_regret_n10_sigma | sub_regret_n15_sigma | eff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| metrla | warm | random | 3.262 | 2.250 | 2.054 | 0.365 |  |  | 2.847 | 1.843 | 1.506 | 100.000 |
| metrla | warm | prior | 0.000 | 0.000 | 0.000 | 1.000 | 6.477 | 5.000 | 0.000 | 0.000 | 0.000 | 6.477 |
| metrla | warm | refit | 0.000 | 0.000 | 0.000 | 1.000 | 6.477 | 5.000 | 0.000 | 0.000 | 0.000 | 6.477 |
| metrla | cold | random | 3.262 | 2.250 | 2.054 | 0.365 |  |  | 2.847 | 1.843 | 1.506 | 100.000 |
| metrla | cold | prior | 4.420 | 2.555 | 1.379 | 0.335 |  |  | 2.911 | 1.599 | 1.227 | 100.000 |
| metrla | cold | refit | 4.420 | 0.826 | 0.826 | 0.710 | 14.003 | 15.000 | 2.911 | 1.458 | 0.852 | 100.000 |
| pems04 | warm | random | 4.822 | 3.201 | 2.704 | 0.285 |  |  | 4.464 | 2.773 | 2.071 | 100.000 |
| pems04 | warm | prior | 0.000 | 0.000 | 0.000 | 0.995 | 5.249 | 5.000 | 0.095 | 0.041 | 0.017 | 5.249 |
| pems04 | warm | refit | 0.000 | 0.000 | 0.000 | 0.990 | 5.249 | 5.000 | 0.095 | 0.063 | 0.031 | 5.249 |
| pems04 | cold | random | 4.822 | 3.201 | 2.704 | 0.285 |  |  | 4.464 | 2.773 | 2.071 | 100.000 |
| pems04 | cold | prior | 1.157 | 0.000 | 0.000 | 0.985 | 6.484 | 5.000 | 0.686 | 0.135 | 0.124 | 6.484 |
| pems04 | cold | refit | 1.157 | 1.071 | 0.000 | 0.920 | 6.484 | 5.000 | 0.686 | 0.593 | 0.221 | 6.484 |
| chengdu | warm | random | 3.669 | 2.531 | 2.107 | 0.250 |  |  | 3.443 | 2.388 | 1.852 | 100.000 |
| chengdu | warm | prior | 0.000 | 0.000 | 0.000 | 0.755 | 5.232 | 5.000 | 0.368 | 0.275 | 0.275 | 100.000 |
| chengdu | warm | refit | 0.000 | 0.000 | 0.000 | 0.770 | 5.232 | 5.000 | 0.368 | 0.317 | 0.294 | 100.000 |
| chengdu | cold | random | 3.669 | 2.531 | 2.107 | 0.250 |  |  | 3.443 | 2.388 | 1.852 | 100.000 |
| chengdu | cold | prior | 2.939 | 1.981 | 1.981 | 0.120 |  |  | 2.661 | 2.021 | 1.504 | 100.000 |
| chengdu | cold | refit | 2.939 | 1.519 | 1.504 | 0.515 | 16.326 | 15.000 | 2.661 | 1.627 | 0.942 | 100.000 |
| shenzhen | warm | random | 4.591 | 3.608 | 3.042 | 0.250 |  |  | 4.246 | 3.099 | 2.522 | 100.000 |
| shenzhen | warm | prior | 0.000 | 0.000 | 0.000 | 1.000 | 5.052 | 5.000 | 0.023 | 0.023 | 0.010 | 5.052 |
| shenzhen | warm | refit | 0.000 | 0.000 | 0.000 | 1.000 | 5.052 | 5.000 | 0.023 | 0.016 | 0.013 | 5.052 |
| shenzhen | cold | random | 4.591 | 3.608 | 3.042 | 0.250 |  |  | 4.246 | 3.099 | 2.522 | 100.000 |
| shenzhen | cold | prior | 3.751 | 2.318 | 2.318 | 0.040 |  |  | 2.481 | 2.122 | 2.103 | 100.000 |
| shenzhen | cold | refit | 3.751 | 1.260 | 1.197 | 0.345 |  |  | 2.481 | 1.866 | 1.306 | 100.000 |
