# evalscreen proxy_combination: a model on the proxy scores, fit on the other cities

Inputs: the 27 stored scores as ranks inside the city (set `proxies`), with the head one-hot (`proxies_head`), or the ZiCo family and the parameter count alone (`zico_family_params`). Models: ridge, gradient boosting (300 trees, depth 3, mean of 3 fit seeds). Target of the fit: within-city rank of -test MAE of the three training cities. Pass: inside the heads rho >= 0.5 and above the best single proxy at three of four cities, the paired CI of the difference excludes 0 at two cities or more, and the n-weighted Kendall on a held-out family at the held-out city is >= 0.5 at three of four cities. The best single proxy is chosen with the labels of the held-out city, which favours the baseline.

### Verdict per model

| model | cities_rho_ge_05_and_above | cities_ci_excludes_0 | cities_family_kendall_ge_05 | pass |
|---|---|---|---|---|
| gbr_proxies | 3 | 3 | 0 | False |
| gbr_proxies_head | 3 | 3 | 2 | False |
| gbr_zico_family_params | 2 | 1 | 0 | False |
| ridge_proxies | 0 | 0 | 0 | False |
| ridge_proxies_head | 1 | 0 | 1 | False |
| ridge_zico_family_params | 0 | 0 | 0 | False |

### Inside the heads: the model against the best single proxy

diff = within-head rho of the model minus that of the best single proxy; CI from 1000 paired stratified resamples.

| city | model | rho_within_head | best_single_proxy | best_single_within | diff | diff_ci_lo | diff_ci_hi |
|---|---|---|---|---|---|---|---|
| metrla | ridge_proxies_head | 0.449 | glass_t | 0.406 | 0.044 | -0.029 | 0.118 |
| pems04 | ridge_proxies_head | 0.561 | glass | 0.686 | -0.125 | -0.221 | -0.033 |
| chengdu | ridge_proxies_head | 0.508 | zico_t | 0.585 | -0.077 | -0.173 | 0.004 |
| shenzhen | ridge_proxies_head | 0.658 | zico_t | 0.628 | 0.030 | -0.044 | 0.102 |
| expytky | ridge_proxies_head | 0.361 | glass_t | 0.345 | 0.016 | -0.058 | 0.082 |
| pemsbay | ridge_proxies_head | 0.073 | params | 0.158 | -0.084 | -0.269 | 0.095 |
| metrla | gbr_proxies_head | 0.594 | glass_t | 0.406 | 0.188 | 0.075 | 0.293 |
| pems04 | gbr_proxies_head | 0.601 | glass | 0.686 | -0.085 | -0.184 | 0.015 |
| chengdu | gbr_proxies_head | 0.547 | zico_t | 0.585 | -0.037 | -0.158 | 0.081 |
| shenzhen | gbr_proxies_head | 0.779 | zico_t | 0.628 | 0.151 | 0.063 | 0.245 |
| expytky | gbr_proxies_head | 0.576 | glass_t | 0.345 | 0.231 | 0.127 | 0.346 |
| pemsbay | gbr_proxies_head | 0.254 | params | 0.158 | 0.096 | -0.104 | 0.277 |
| metrla | ridge_proxies | 0.433 | glass_t | 0.406 | 0.027 | -0.083 | 0.125 |
| pems04 | ridge_proxies | 0.429 | glass | 0.686 | -0.257 | -0.377 | -0.135 |
| chengdu | ridge_proxies | 0.412 | zico_t | 0.585 | -0.173 | -0.288 | -0.070 |
| shenzhen | ridge_proxies | 0.547 | zico_t | 0.628 | -0.081 | -0.192 | 0.017 |
| expytky | ridge_proxies | 0.381 | glass_t | 0.345 | 0.036 | -0.067 | 0.134 |
| pemsbay | ridge_proxies | 0.093 | params | 0.158 | -0.064 | -0.250 | 0.120 |
| metrla | gbr_proxies | 0.543 | glass_t | 0.406 | 0.137 | 0.022 | 0.251 |
| pems04 | gbr_proxies | 0.538 | glass | 0.686 | -0.148 | -0.263 | -0.040 |
| chengdu | gbr_proxies | 0.530 | zico_t | 0.585 | -0.054 | -0.174 | 0.070 |
| shenzhen | gbr_proxies | 0.767 | zico_t | 0.628 | 0.139 | 0.046 | 0.237 |
| expytky | gbr_proxies | 0.567 | glass_t | 0.345 | 0.221 | 0.098 | 0.334 |
| pemsbay | gbr_proxies | 0.234 | params | 0.158 | 0.077 | -0.118 | 0.265 |
| metrla | ridge_zico_family_params | 0.427 | glass_t | 0.406 | 0.021 | -0.044 | 0.092 |
| pems04 | ridge_zico_family_params | 0.457 | glass | 0.686 | -0.229 | -0.343 | -0.121 |
| chengdu | ridge_zico_family_params | 0.544 | zico_t | 0.585 | -0.041 | -0.130 | 0.044 |
| shenzhen | ridge_zico_family_params | 0.618 | zico_t | 0.628 | -0.010 | -0.079 | 0.059 |
| expytky | ridge_zico_family_params | 0.372 | glass_t | 0.345 | 0.027 | -0.029 | 0.082 |
| pemsbay | ridge_zico_family_params | 0.048 | params | 0.158 | -0.110 | -0.293 | 0.072 |
| metrla | gbr_zico_family_params | 0.549 | glass_t | 0.406 | 0.143 | 0.029 | 0.260 |
| pems04 | gbr_zico_family_params | 0.528 | glass | 0.686 | -0.158 | -0.268 | -0.043 |
| chengdu | gbr_zico_family_params | 0.563 | zico_t | 0.585 | -0.022 | -0.123 | 0.076 |
| shenzhen | gbr_zico_family_params | 0.698 | zico_t | 0.628 | 0.070 | -0.016 | 0.165 |
| expytky | gbr_zico_family_params | 0.436 | glass_t | 0.345 | 0.090 | -0.024 | 0.188 |
| pemsbay | gbr_zico_family_params | 0.192 | params | 0.158 | 0.035 | -0.143 | 0.210 |

### City and operator family held out together

Kendall with -test MAE on the held-out family at the held-out city; n-weighted over the families with 8 architectures or more.

| city | model | families | kendall_weighted | families_ge_0.5 |
|---|---|---|---|---|
| chengdu | gbr_operator_counts | 12.000 | 0.408 | 3.000 |
| chengdu | gbr_proxies | 12.000 | 0.291 | 1.000 |
| chengdu | gbr_proxies_head | 12.000 | 0.383 | 2.000 |
| chengdu | gbr_zico_family_params | 12.000 | 0.230 | 0.000 |
| chengdu | ridge_operator_counts | 12.000 | 0.392 | 3.000 |
| chengdu | ridge_proxies | 12.000 | 0.244 | 1.000 |
| chengdu | ridge_proxies_head | 12.000 | 0.347 | 2.000 |
| chengdu | ridge_zico_family_params | 12.000 | 0.266 | 0.000 |
| expytky | gbr_operator_counts | 12.000 | 0.447 | 4.000 |
| expytky | gbr_proxies | 12.000 | 0.335 | 2.000 |
| expytky | gbr_proxies_head | 12.000 | 0.462 | 5.000 |
| expytky | gbr_zico_family_params | 12.000 | 0.142 | 0.000 |
| expytky | ridge_operator_counts | 12.000 | 0.477 | 5.000 |
| expytky | ridge_proxies | 12.000 | 0.276 | 1.000 |
| expytky | ridge_proxies_head | 12.000 | 0.404 | 3.000 |
| expytky | ridge_zico_family_params | 12.000 | 0.264 | 2.000 |
| metrla | gbr_operator_counts | 12.000 | 0.632 | 11.000 |
| metrla | gbr_proxies | 12.000 | 0.409 | 4.000 |
| metrla | gbr_proxies_head | 12.000 | 0.566 | 10.000 |
| metrla | gbr_zico_family_params | 12.000 | 0.113 | 0.000 |
| metrla | ridge_operator_counts | 12.000 | 0.596 | 11.000 |
| metrla | ridge_proxies | 12.000 | 0.406 | 4.000 |
| metrla | ridge_proxies_head | 12.000 | 0.598 | 11.000 |
| metrla | ridge_zico_family_params | 12.000 | 0.322 | 1.000 |
| pems04 | gbr_operator_counts | 12.000 | 0.434 | 2.000 |
| pems04 | gbr_proxies | 12.000 | 0.306 | 1.000 |
| pems04 | gbr_proxies_head | 12.000 | 0.419 | 2.000 |
| pems04 | gbr_zico_family_params | 12.000 | 0.201 | 0.000 |
| pems04 | ridge_operator_counts | 12.000 | 0.445 | 4.000 |
| pems04 | ridge_proxies | 12.000 | 0.268 | 2.000 |
| pems04 | ridge_proxies_head | 12.000 | 0.404 | 3.000 |
| pems04 | ridge_zico_family_params | 12.000 | 0.280 | 1.000 |
| pemsbay | gbr_operator_counts | 12.000 | 0.467 | 4.000 |
| pemsbay | gbr_proxies | 12.000 | 0.338 | 1.000 |
| pemsbay | gbr_proxies_head | 12.000 | 0.468 | 4.000 |
| pemsbay | gbr_zico_family_params | 12.000 | -0.022 | 0.000 |
| pemsbay | ridge_operator_counts | 12.000 | 0.408 | 1.000 |
| pemsbay | ridge_proxies | 12.000 | 0.294 | 1.000 |
| pemsbay | ridge_proxies_head | 12.000 | 0.459 | 6.000 |
| pemsbay | ridge_zico_family_params | 12.000 | 0.160 | 0.000 |
| shenzhen | gbr_operator_counts | 12.000 | 0.562 | 11.000 |
| shenzhen | gbr_proxies | 12.000 | 0.425 | 4.000 |
| shenzhen | gbr_proxies_head | 12.000 | 0.520 | 8.000 |
| shenzhen | gbr_zico_family_params | 12.000 | 0.228 | 0.000 |
| shenzhen | ridge_operator_counts | 12.000 | 0.555 | 8.000 |
| shenzhen | ridge_proxies | 12.000 | 0.369 | 4.000 |
| shenzhen | ridge_proxies_head | 12.000 | 0.474 | 7.000 |
| shenzhen | ridge_zico_family_params | 12.000 | 0.322 | 0.000 |

### Kendall on the held-out gru family

| model | chengdu | expytky | metrla | pems04 | pemsbay | shenzhen |
|---|---|---|---|---|---|---|
| gbr_operator_counts | 0.487 | 0.128 | 0.385 | 0.385 | 0.308 | 0.385 |
| gbr_proxies | 0.308 | -0.026 | 0.231 | 0.077 | -0.103 | 0.256 |
| gbr_proxies_head | 0.308 | 0.231 | 0.487 | 0.256 | 0.462 | 0.359 |
| gbr_zico_family_params | 0.308 | -0.026 | -0.077 | 0.103 | -0.103 | 0.077 |
| ridge_operator_counts | 0.410 | 0.128 | 0.538 | 0.282 | 0.462 | 0.385 |
| ridge_proxies | 0.128 | 0.026 | 0.154 | -0.359 | 0.026 | -0.154 |
| ridge_proxies_head | 0.436 | 0.000 | 0.487 | 0.231 | 0.462 | -0.026 |
| ridge_zico_family_params | 0.179 | -0.128 | 0.077 | 0.000 | -0.103 | -0.051 |

### metrla: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.424 | 1.000 |
| gbr_proxies | proxy combination, other cities | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.455 | 1.000 |
| gbr_proxies_head | proxy combination, other cities | 1.379 | 2.013 | 2.000 | 0.664 | 2.022 | 1.000 | 1.594 | 1.000 |
| ridge_proxies_head | proxy combination, other cities | 2.555 | 8.054 | 3.000 | 1.077 | 3.276 | 1.000 | 3.361 | 2.000 |
| gbr_zico_family_params | proxy combination, other cities | 2.555 | 8.054 |  |  |  | 0.700 | 10.535 | 8.000 |
| ridge_proxies | proxy combination, other cities | 4.132 | 22.819 |  |  |  | 0.695 | 12.411 | 10.000 |
| ridge_zico_family_params | proxy combination, other cities | 5.849 | 40.268 |  |  |  | 0.215 |  |  |
| best_single_proxy (glass_t) | zero-cost proxy | 5.816 | 39.597 |  |  |  | 0.345 |  |  |

### metrla: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.819 | 0.656 | 0.538 | 0.741 | 0.668 | 0.686 | 0.618 | 0.000 | 0.000 |
| gbr_proxies_head | proxy combination, other cities | 0.841 | 0.594 | 0.467 | 0.690 | 0.600 | 0.616 | 0.568 | 1.379 | 7.692 |
| gbr_zico_family_params | proxy combination, other cities | 0.681 | 0.549 | 0.420 | 0.644 | 0.586 | 0.545 | 0.526 | 2.555 | 28.205 |
| gbr_proxies | proxy combination, other cities | 0.788 | 0.543 | 0.400 | 0.651 | 0.567 | 0.494 | 0.575 | 0.000 | 0.000 |
| ridge_proxies_head | proxy combination, other cities | 0.843 | 0.449 | 0.309 | 0.567 | 0.556 | 0.247 | 0.574 | 2.555 | 28.205 |
| ridge_proxies | proxy combination, other cities | 0.636 | 0.433 | 0.286 | 0.543 | 0.510 | 0.217 | 0.593 | 3.073 | 43.590 |
| ridge_zico_family_params | proxy combination, other cities | 0.523 | 0.427 | 0.275 | 0.548 | 0.500 | 0.256 | 0.544 | 3.270 | 48.718 |
| best_single_proxy (glass_t) | zero-cost proxy | 0.194 | 0.406 | 0.249 | 0.520 | 0.433 | 0.251 | 0.542 | 2.555 | 28.205 |

### pems04: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| ridge_proxies_head | proxy combination, other cities | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.995 | 0.864 | 1.000 |
| gbr_proxies | proxy combination, other cities | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.985 | 0.864 | 1.000 |
| gbr_zico_family_params | proxy combination, other cities | 0.000 | 0.000 | 1.000 | 0.286 | 0.998 | 0.895 | 1.508 | 1.000 |
| transfer_pooled | transfer | 6.574 | 21.477 | 2.000 | 0.295 | 1.031 | 0.980 | 1.556 | 2.000 |
| gbr_proxies_head | proxy combination, other cities | 3.413 | 10.738 | 3.000 | 0.429 | 1.497 | 0.995 | 2.247 | 3.000 |
| ridge_proxies | proxy combination, other cities | 8.601 | 36.913 | 8.000 | 1.648 | 5.753 | 0.940 | 6.147 | 5.000 |
| best_single_proxy (glass) | zero-cost proxy | 1.157 | 2.013 | 8.000 | 1.971 | 6.878 | 0.960 | 7.086 | 5.000 |
| ridge_zico_family_params | proxy combination, other cities | 8.522 | 34.899 |  |  |  | 0.015 |  |  |

### pems04: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| best_single_proxy (glass) | zero-cost proxy | 0.588 | 0.686 | 0.575 | 0.759 | 0.618 | 0.622 | 0.799 | 0.000 | 0.000 |
| transfer_pooled | transfer | 0.657 | 0.618 | 0.509 | 0.706 | 0.585 | 0.742 | 0.519 | 6.574 | 46.154 |
| gbr_proxies_head | proxy combination, other cities | 0.619 | 0.601 | 0.491 | 0.696 | 0.587 | 0.715 | 0.497 | 3.413 | 30.769 |
| ridge_proxies_head | proxy combination, other cities | 0.589 | 0.561 | 0.426 | 0.658 | 0.502 | 0.588 | 0.577 | 0.846 | 2.564 |
| gbr_proxies | proxy combination, other cities | 0.599 | 0.538 | 0.416 | 0.648 | 0.489 | 0.630 | 0.483 | 0.846 | 2.564 |
| gbr_zico_family_params | proxy combination, other cities | 0.593 | 0.528 | 0.399 | 0.634 | 0.442 | 0.615 | 0.504 | 0.000 | 0.000 |
| ridge_zico_family_params | proxy combination, other cities | 0.380 | 0.457 | 0.298 | 0.573 | 0.304 | 0.506 | 0.518 | 1.615 | 10.256 |
| ridge_proxies | proxy combination, other cities | 0.442 | 0.429 | 0.278 | 0.564 | 0.327 | 0.376 | 0.556 | 0.000 | 0.000 |

### chengdu: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 2.287 | 6.040 | 8.000 | 1.041 | 4.942 | 0.755 | 4.197 | 5.000 |
| gbr_proxies_head | proxy combination, other cities | 2.287 | 6.040 | 8.000 | 1.220 | 5.794 | 0.755 | 7.600 | 8.000 |
| gbr_proxies | proxy combination, other cities | 2.287 | 6.040 |  |  |  | 0.750 | 8.907 | 8.000 |
| ridge_proxies_head | proxy combination, other cities | 3.950 | 14.094 |  |  |  | 0.730 | 10.055 | 10.000 |
| ridge_proxies | proxy combination, other cities | 9.726 | 72.483 |  |  |  | 0.120 |  |  |
| ridge_zico_family_params | proxy combination, other cities | 4.657 | 21.477 |  |  |  | 0.115 |  |  |
| gbr_zico_family_params | proxy combination, other cities | 2.941 | 9.396 |  |  |  | 0.430 |  |  |
| best_single_proxy (zico_t) | zero-cost proxy | 2.939 | 8.725 |  |  |  | 0.080 |  |  |

### chengdu: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.640 | 0.594 | 0.463 | 0.694 | 0.663 | 0.570 | 0.569 | 2.287 | 12.821 |
| best_single_proxy (zico_t) | zero-cost proxy | 0.516 | 0.585 | 0.444 | 0.688 | 0.653 | 0.585 | 0.535 | 2.941 | 17.949 |
| gbr_zico_family_params | proxy combination, other cities | 0.615 | 0.563 | 0.425 | 0.666 | 0.638 | 0.563 | 0.509 | 2.941 | 17.949 |
| gbr_proxies_head | proxy combination, other cities | 0.609 | 0.547 | 0.402 | 0.651 | 0.552 | 0.533 | 0.558 | 2.287 | 12.821 |
| ridge_zico_family_params | proxy combination, other cities | 0.421 | 0.544 | 0.384 | 0.642 | 0.682 | 0.469 | 0.519 | 2.941 | 17.949 |
| gbr_proxies | proxy combination, other cities | 0.607 | 0.530 | 0.377 | 0.642 | 0.596 | 0.448 | 0.565 | 2.287 | 12.821 |
| ridge_proxies_head | proxy combination, other cities | 0.550 | 0.508 | 0.359 | 0.615 | 0.663 | 0.490 | 0.413 | 3.950 | 25.641 |
| ridge_proxies | proxy combination, other cities | 0.463 | 0.412 | 0.265 | 0.529 | 0.557 | 0.425 | 0.294 | 3.950 | 25.641 |

### shenzhen: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.940 | 1.000 |
| gbr_proxies_head | proxy combination, other cities | 3.767 | 6.711 | 2.000 | 0.331 | 1.036 | 1.000 | 1.555 | 2.000 |
| gbr_proxies | proxy combination, other cities | 3.767 | 6.711 | 2.000 | 0.331 | 1.036 | 1.000 | 1.560 | 2.000 |
| ridge_proxies_head | proxy combination, other cities | 2.965 | 2.685 | 2.000 | 0.564 | 1.765 | 0.995 | 2.646 | 2.000 |
| ridge_proxies | proxy combination, other cities | 4.826 | 15.436 | 10.000 | 2.282 | 7.139 | 0.780 | 8.506 | 8.000 |
| ridge_zico_family_params | proxy combination, other cities | 6.101 | 21.477 |  |  |  | 0.040 |  |  |
| gbr_zico_family_params | proxy combination, other cities | 5.402 | 18.121 |  |  |  | 0.330 |  |  |
| best_single_proxy (zico_t) | zero-cost proxy | 5.123 | 16.779 |  |  |  | 0.060 |  |  |

### shenzhen: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.856 | 0.816 | 0.747 | 0.858 | 0.822 | 0.867 | 0.762 | 0.965 | 2.564 |
| gbr_proxies_head | proxy combination, other cities | 0.826 | 0.779 | 0.705 | 0.833 | 0.768 | 0.849 | 0.718 | 3.767 | 15.385 |
| gbr_proxies | proxy combination, other cities | 0.818 | 0.767 | 0.681 | 0.822 | 0.752 | 0.803 | 0.743 | 3.767 | 15.385 |
| gbr_zico_family_params | proxy combination, other cities | 0.765 | 0.698 | 0.606 | 0.779 | 0.724 | 0.716 | 0.662 | 6.618 | 48.718 |
| ridge_proxies_head | proxy combination, other cities | 0.756 | 0.658 | 0.545 | 0.733 | 0.815 | 0.565 | 0.637 | 2.965 | 7.692 |
| best_single_proxy (zico_t) | zero-cost proxy | 0.502 | 0.628 | 0.504 | 0.718 | 0.677 | 0.544 | 0.676 | 2.965 | 7.692 |
| ridge_zico_family_params | proxy combination, other cities | 0.474 | 0.618 | 0.503 | 0.707 | 0.742 | 0.491 | 0.654 | 2.965 | 7.692 |
| ridge_proxies | proxy combination, other cities | 0.657 | 0.547 | 0.410 | 0.647 | 0.705 | 0.482 | 0.497 | 6.943 | 56.410 |

### expytky: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| gbr_proxies_head | proxy combination, other cities | 0.635 | 0.671 | 1.000 | 0.123 | 0.218 | 1.000 | 0.337 | 1.000 |
| gbr_proxies | proxy combination, other cities | 0.635 | 0.671 | 1.000 | 0.123 | 0.218 | 1.000 | 0.337 | 1.000 |
| transfer_pooled | transfer | 1.455 | 2.013 | 3.000 | 0.587 | 1.039 | 1.000 | 0.925 | 2.000 |
| ridge_proxies_head | proxy combination, other cities | 4.487 | 5.369 | 5.000 | 1.373 | 2.430 | 0.970 | 2.563 | 3.000 |
| ridge_proxies | proxy combination, other cities | 8.816 | 46.980 | 8.000 | 2.305 | 4.077 | 0.860 | 4.535 | 5.000 |
| gbr_zico_family_params | proxy combination, other cities | 7.780 | 31.544 | 8.000 | 3.847 | 6.806 | 0.840 | 6.160 | 5.000 |
| ridge_zico_family_params | proxy combination, other cities | 4.724 | 8.054 |  |  |  | 0.420 |  |  |
| best_single_proxy (glass_t) | zero-cost proxy | 7.789 | 32.215 |  |  |  | 0.190 |  |  |

### expytky: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.820 | 0.690 | 0.577 | 0.765 | 0.748 | 0.626 | 0.712 | 1.455 | 7.692 |
| gbr_proxies_head | proxy combination, other cities | 0.762 | 0.576 | 0.453 | 0.675 | 0.712 | 0.387 | 0.666 | 0.635 | 2.564 |
| gbr_proxies | proxy combination, other cities | 0.737 | 0.567 | 0.443 | 0.658 | 0.620 | 0.403 | 0.692 | 0.635 | 2.564 |
| gbr_zico_family_params | proxy combination, other cities | 0.557 | 0.436 | 0.298 | 0.553 | 0.501 | 0.209 | 0.615 | 5.057 | 33.333 |
| ridge_proxies | proxy combination, other cities | 0.548 | 0.381 | 0.242 | 0.508 | 0.543 | 0.107 | 0.539 | 0.000 | 0.000 |
| ridge_zico_family_params | proxy combination, other cities | 0.403 | 0.372 | 0.218 | 0.475 | 0.492 | -0.056 | 0.714 | 4.487 | 17.949 |
| ridge_proxies_head | proxy combination, other cities | 0.660 | 0.361 | 0.223 | 0.477 | 0.466 | 0.031 | 0.616 | 4.487 | 17.949 |
| best_single_proxy (glass_t) | zero-cost proxy | 0.293 | 0.345 | 0.204 | 0.472 | 0.404 | 0.009 | 0.639 | 4.487 | 17.949 |

### pemsbay: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.000 | 0.000 | 1.000 | 0.512 | 0.706 | 0.980 | 1.065 | 1.000 |
| gbr_proxies_head | proxy combination, other cities | 0.000 | 0.000 | 1.000 | 0.512 | 0.706 | 0.990 | 1.070 | 1.000 |
| gbr_proxies | proxy combination, other cities | 5.348 | 29.530 | 2.000 | 1.346 | 1.857 | 0.990 | 2.703 | 2.000 |
| ridge_proxies_head | proxy combination, other cities | 5.348 | 29.530 | 3.000 | 2.112 | 2.913 | 0.905 | 4.250 | 3.000 |
| gbr_zico_family_params | proxy combination, other cities | 3.421 | 12.081 |  |  |  | 0.725 | 11.274 | 10.000 |
| ridge_proxies | proxy combination, other cities | 4.600 | 20.805 |  |  |  | 0.055 |  |  |
| ridge_zico_family_params | proxy combination, other cities | 9.479 | 59.060 |  |  |  | 0.225 |  |  |
| best_single_proxy (params) | zero-cost proxy | 3.844 | 15.436 |  |  |  | 0.050 |  |  |

### pemsbay: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.675 | 0.268 | 0.111 | 0.425 | 0.336 | 0.330 | 0.157 | 0.000 | 0.000 |
| gbr_proxies_head | proxy combination, other cities | 0.735 | 0.254 | 0.089 | 0.426 | 0.244 | 0.259 | 0.256 | 0.000 | 0.000 |
| gbr_proxies | proxy combination, other cities | 0.702 | 0.234 | 0.066 | 0.414 | 0.294 | 0.191 | 0.234 | 5.348 | 71.795 |
| gbr_zico_family_params | proxy combination, other cities | 0.492 | 0.192 | 0.038 | 0.353 | 0.188 | 0.203 | 0.185 | 3.421 | 43.590 |
| best_single_proxy (params) | zero-cost proxy | 0.057 | 0.158 | 0.006 | 0.308 | 0.296 | -0.105 | 0.320 | 4.279 | 53.846 |
| ridge_proxies | proxy combination, other cities | 0.545 | 0.093 | -0.085 | 0.257 | 0.211 | -0.165 | 0.267 | 5.348 | 71.795 |
| ridge_proxies_head | proxy combination, other cities | 0.713 | 0.073 | -0.110 | 0.255 | 0.124 | -0.125 | 0.235 | 5.348 | 71.795 |
| ridge_zico_family_params | proxy combination, other cities | 0.292 | 0.048 | -0.116 | 0.217 | 0.056 | -0.117 | 0.207 | 5.767 | 82.051 |
