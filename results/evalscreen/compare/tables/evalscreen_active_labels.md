# evalscreen active_labels: an active choice of the labels at the target city

Rounds of 5 labels up to 15. random = random labels; prior = the next five of the prior, no refit; refit = a ridge on the operator counts and the prior, fit on the labels so far, picks four and one random architecture. Warm prior = the pooled transfer rank; cold prior = the size-controlled ZiCo of the city. The pick is the best labelled architecture. regret_n = regret after n labels on the full list (mean of 20 draws where the rule draws); sub_* = the 200 subsets; eff as in halving_prior.

### Verdict

| setting | cities_refit_meets_line | cities_refit_below_random_and_prior | pass |
|---|---|---|---|
| cold | 1 | 1 | False |
| warm | 4 | 0 | False |

### Every rule

| city | setting | rule | regret_n5_sigma | regret_n10_sigma | regret_n15_sigma | sub_share | sub_pct_median | sub_n_median | sub_regret_n5_sigma | sub_regret_n10_sigma | sub_regret_n15_sigma | eff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| metrla | warm | random | 1.325 | 0.914 | 0.834 | 0.765 | 9.858 | 10.000 | 1.156 | 0.748 | 0.611 | 100.000 |
| metrla | warm | prior | 0.000 | 0.000 | 0.000 | 1.000 | 6.477 | 5.000 | 0.000 | 0.000 | 0.000 | 6.477 |
| metrla | warm | refit | 0.000 | 0.000 | 0.000 | 1.000 | 6.477 | 5.000 | 0.000 | 0.000 | 0.000 | 6.477 |
| metrla | cold | random | 1.325 | 0.914 | 0.834 | 0.765 | 9.858 | 10.000 | 1.156 | 0.748 | 0.611 | 100.000 |
| metrla | cold | prior | 1.795 | 1.038 | 0.560 | 0.915 | 12.038 | 10.000 | 1.182 | 0.649 | 0.498 | 12.038 |
| metrla | cold | refit | 1.795 | 0.335 | 0.335 | 0.935 | 11.425 | 10.000 | 1.182 | 0.592 | 0.346 | 11.425 |
| pems04 | warm | random | 7.480 | 4.966 | 4.194 | 0.175 |  |  | 6.925 | 4.302 | 3.212 | 100.000 |
| pems04 | warm | prior | 0.000 | 0.000 | 0.000 | 0.995 | 5.286 | 5.000 | 0.147 | 0.063 | 0.027 | 5.286 |
| pems04 | warm | refit | 0.000 | 0.000 | 0.000 | 0.980 | 5.286 | 5.000 | 0.147 | 0.098 | 0.049 | 5.286 |
| pems04 | cold | random | 7.480 | 4.966 | 4.194 | 0.175 |  |  | 6.925 | 4.302 | 3.212 | 100.000 |
| pems04 | cold | prior | 1.795 | 0.000 | 0.000 | 0.975 | 6.484 | 5.000 | 1.065 | 0.209 | 0.193 | 6.484 |
| pems04 | cold | refit | 1.795 | 1.661 | 0.000 | 0.880 | 6.484 | 5.000 | 1.065 | 0.919 | 0.343 | 100.000 |
| chengdu | warm | random | 2.676 | 1.846 | 1.536 | 0.315 |  |  | 2.511 | 1.742 | 1.350 | 100.000 |
| chengdu | warm | prior | 0.000 | 0.000 | 0.000 | 0.960 | 5.158 | 5.000 | 0.268 | 0.201 | 0.201 | 5.158 |
| chengdu | warm | refit | 0.000 | 0.000 | 0.000 | 0.935 | 5.158 | 5.000 | 0.268 | 0.231 | 0.215 | 5.158 |
| chengdu | cold | random | 2.676 | 1.846 | 1.536 | 0.315 |  |  | 2.511 | 1.742 | 1.350 | 100.000 |
| chengdu | cold | prior | 2.144 | 1.445 | 1.445 | 0.240 |  |  | 1.941 | 1.474 | 1.097 | 100.000 |
| chengdu | cold | refit | 2.144 | 1.108 | 1.097 | 0.615 | 14.722 | 15.000 | 1.941 | 1.187 | 0.687 | 100.000 |
| shenzhen | warm | random | 3.799 | 2.986 | 2.517 | 0.250 |  |  | 3.513 | 2.564 | 2.086 | 100.000 |
| shenzhen | warm | prior | 0.000 | 0.000 | 0.000 | 1.000 | 5.052 | 5.000 | 0.019 | 0.019 | 0.008 | 5.052 |
| shenzhen | warm | refit | 0.000 | 0.000 | 0.000 | 1.000 | 5.052 | 5.000 | 0.019 | 0.013 | 0.011 | 5.052 |
| shenzhen | cold | random | 3.799 | 2.986 | 2.517 | 0.250 |  |  | 3.513 | 2.564 | 2.086 | 100.000 |
| shenzhen | cold | prior | 3.103 | 1.918 | 1.918 | 0.075 |  |  | 2.052 | 1.756 | 1.740 | 100.000 |
| shenzhen | cold | refit | 3.103 | 1.042 | 0.990 | 0.345 |  |  | 2.052 | 1.544 | 1.080 | 100.000 |
