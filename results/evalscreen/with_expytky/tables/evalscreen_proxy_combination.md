# evalscreen proxy_combination: a model on the proxy scores, fit on the other cities

Inputs: the 27 stored scores as ranks inside the city (set `proxies`), with the head one-hot (`proxies_head`), or the ZiCo family and the parameter count alone (`zico_family_params`). Models: ridge, gradient boosting (300 trees, depth 3, mean of 3 fit seeds). Target of the fit: within-city rank of -test MAE of the three training cities. Pass: inside the heads rho >= 0.5 and above the best single proxy at three of four cities, the paired CI of the difference excludes 0 at two cities or more, and the n-weighted Kendall on a held-out family at the held-out city is >= 0.5 at three of four cities. The best single proxy is chosen with the labels of the held-out city, which favours the baseline.

### Verdict per model

| model | cities_rho_ge_05_and_above | cities_ci_excludes_0 | cities_family_kendall_ge_05 | pass |
|---|---|---|---|---|
| gbr_proxies | 4 | 3 | 0 | False |
| gbr_proxies_head | 4 | 3 | 1 | False |
| gbr_zico_family_params | 3 | 2 | 0 | False |
| ridge_proxies | 0 | 0 | 0 | False |
| ridge_proxies_head | 1 | 0 | 1 | False |
| ridge_zico_family_params | 1 | 0 | 0 | False |

### Inside the heads: the model against the best single proxy

diff = within-head rho of the model minus that of the best single proxy; CI from 1000 paired stratified resamples.

| city | model | rho_within_head | best_single_proxy | best_single_within | diff | diff_ci_lo | diff_ci_hi |
|---|---|---|---|---|---|---|---|
| metrla | ridge_proxies_head | 0.438 | glass_t | 0.406 | 0.032 | -0.039 | 0.108 |
| pems04 | ridge_proxies_head | 0.557 | glass | 0.686 | -0.129 | -0.217 | -0.043 |
| chengdu | ridge_proxies_head | 0.549 | zico_t | 0.585 | -0.036 | -0.121 | 0.035 |
| shenzhen | ridge_proxies_head | 0.659 | zico_t | 0.628 | 0.031 | -0.042 | 0.100 |
| expytky | ridge_proxies_head | 0.355 | glass_t | 0.345 | 0.009 | -0.060 | 0.077 |
| metrla | gbr_proxies_head | 0.561 | glass_t | 0.406 | 0.155 | 0.049 | 0.264 |
| pems04 | gbr_proxies_head | 0.619 | glass | 0.686 | -0.067 | -0.165 | 0.032 |
| chengdu | gbr_proxies_head | 0.610 | zico_t | 0.585 | 0.025 | -0.095 | 0.130 |
| shenzhen | gbr_proxies_head | 0.809 | zico_t | 0.628 | 0.181 | 0.094 | 0.271 |
| expytky | gbr_proxies_head | 0.527 | glass_t | 0.345 | 0.181 | 0.087 | 0.275 |
| metrla | ridge_proxies | 0.443 | glass_t | 0.406 | 0.037 | -0.060 | 0.129 |
| pems04 | ridge_proxies | 0.467 | glass | 0.686 | -0.219 | -0.320 | -0.116 |
| chengdu | ridge_proxies | 0.490 | zico_t | 0.585 | -0.095 | -0.189 | -0.008 |
| shenzhen | ridge_proxies | 0.585 | zico_t | 0.628 | -0.043 | -0.136 | 0.043 |
| expytky | ridge_proxies | 0.383 | glass_t | 0.345 | 0.037 | -0.047 | 0.116 |
| metrla | gbr_proxies | 0.521 | glass_t | 0.406 | 0.115 | 0.003 | 0.222 |
| pems04 | gbr_proxies | 0.578 | glass | 0.686 | -0.108 | -0.215 | -0.006 |
| chengdu | gbr_proxies | 0.617 | zico_t | 0.585 | 0.032 | -0.077 | 0.138 |
| shenzhen | gbr_proxies | 0.793 | zico_t | 0.628 | 0.164 | 0.077 | 0.258 |
| expytky | gbr_proxies | 0.528 | glass_t | 0.345 | 0.182 | 0.071 | 0.277 |
| metrla | ridge_zico_family_params | 0.421 | glass_t | 0.406 | 0.015 | -0.055 | 0.081 |
| pems04 | ridge_zico_family_params | 0.501 | glass | 0.686 | -0.185 | -0.282 | -0.094 |
| chengdu | ridge_zico_family_params | 0.579 | zico_t | 0.585 | -0.005 | -0.080 | 0.067 |
| shenzhen | ridge_zico_family_params | 0.640 | zico_t | 0.628 | 0.012 | -0.051 | 0.077 |
| expytky | ridge_zico_family_params | 0.388 | glass_t | 0.345 | 0.042 | -0.010 | 0.092 |
| metrla | gbr_zico_family_params | 0.528 | glass_t | 0.406 | 0.122 | 0.009 | 0.233 |
| pems04 | gbr_zico_family_params | 0.541 | glass | 0.686 | -0.145 | -0.254 | -0.043 |
| chengdu | gbr_zico_family_params | 0.598 | zico_t | 0.585 | 0.013 | -0.087 | 0.107 |
| shenzhen | gbr_zico_family_params | 0.747 | zico_t | 0.628 | 0.119 | 0.041 | 0.206 |
| expytky | gbr_zico_family_params | 0.428 | glass_t | 0.345 | 0.083 | -0.017 | 0.182 |

### City and operator family held out together

Kendall with -test MAE on the held-out family at the held-out city; n-weighted over the families with 8 architectures or more.

| city | model | families | kendall_weighted | families_ge_0.5 |
|---|---|---|---|---|
| chengdu | gbr_operator_counts | 12.000 | 0.439 | 4.000 |
| chengdu | gbr_proxies | 12.000 | 0.300 | 1.000 |
| chengdu | gbr_proxies_head | 12.000 | 0.391 | 4.000 |
| chengdu | gbr_zico_family_params | 12.000 | 0.247 | 0.000 |
| chengdu | ridge_operator_counts | 12.000 | 0.433 | 5.000 |
| chengdu | ridge_proxies | 12.000 | 0.279 | 1.000 |
| chengdu | ridge_proxies_head | 12.000 | 0.383 | 4.000 |
| chengdu | ridge_zico_family_params | 12.000 | 0.324 | 0.000 |
| expytky | gbr_operator_counts | 12.000 | 0.438 | 2.000 |
| expytky | gbr_proxies | 12.000 | 0.334 | 2.000 |
| expytky | gbr_proxies_head | 12.000 | 0.447 | 5.000 |
| expytky | gbr_zico_family_params | 12.000 | 0.139 | 0.000 |
| expytky | ridge_operator_counts | 12.000 | 0.457 | 5.000 |
| expytky | ridge_proxies | 12.000 | 0.267 | 1.000 |
| expytky | ridge_proxies_head | 12.000 | 0.394 | 4.000 |
| expytky | ridge_zico_family_params | 12.000 | 0.246 | 1.000 |
| metrla | gbr_operator_counts | 12.000 | 0.521 | 7.000 |
| metrla | gbr_proxies | 12.000 | 0.365 | 2.000 |
| metrla | gbr_proxies_head | 12.000 | 0.484 | 5.000 |
| metrla | gbr_zico_family_params | 12.000 | 0.096 | 0.000 |
| metrla | ridge_operator_counts | 12.000 | 0.511 | 7.000 |
| metrla | ridge_proxies | 12.000 | 0.303 | 1.000 |
| metrla | ridge_proxies_head | 12.000 | 0.515 | 8.000 |
| metrla | ridge_zico_family_params | 12.000 | 0.179 | 0.000 |
| pems04 | gbr_operator_counts | 12.000 | 0.444 | 3.000 |
| pems04 | gbr_proxies | 12.000 | 0.325 | 1.000 |
| pems04 | gbr_proxies_head | 12.000 | 0.415 | 3.000 |
| pems04 | gbr_zico_family_params | 12.000 | 0.199 | 0.000 |
| pems04 | ridge_operator_counts | 12.000 | 0.465 | 4.000 |
| pems04 | ridge_proxies | 12.000 | 0.295 | 2.000 |
| pems04 | ridge_proxies_head | 12.000 | 0.433 | 4.000 |
| pems04 | ridge_zico_family_params | 12.000 | 0.313 | 2.000 |
| shenzhen | gbr_operator_counts | 12.000 | 0.578 | 11.000 |
| shenzhen | gbr_proxies | 12.000 | 0.410 | 4.000 |
| shenzhen | gbr_proxies_head | 12.000 | 0.509 | 8.000 |
| shenzhen | gbr_zico_family_params | 12.000 | 0.256 | 0.000 |
| shenzhen | ridge_operator_counts | 12.000 | 0.589 | 10.000 |
| shenzhen | ridge_proxies | 12.000 | 0.389 | 5.000 |
| shenzhen | ridge_proxies_head | 12.000 | 0.498 | 7.000 |
| shenzhen | ridge_zico_family_params | 12.000 | 0.361 | 2.000 |

### Kendall on the held-out gru family

| model | chengdu | expytky | metrla | pems04 | shenzhen |
|---|---|---|---|---|---|
| gbr_operator_counts | 0.513 | 0.103 | 0.051 | 0.385 | 0.308 |
| gbr_proxies | 0.205 | -0.077 | 0.051 | -0.231 | -0.026 |
| gbr_proxies_head | 0.308 | 0.103 | 0.410 | 0.077 | 0.256 |
| gbr_zico_family_params | 0.231 | -0.051 | -0.077 | -0.077 | 0.026 |
| ridge_operator_counts | 0.462 | 0.000 | 0.308 | 0.359 | 0.359 |
| ridge_proxies | 0.179 | -0.077 | 0.103 | -0.333 | -0.205 |
| ridge_proxies_head | 0.436 | 0.000 | 0.333 | 0.051 | 0.077 |
| ridge_zico_family_params | 0.103 | -0.231 | -0.051 | -0.128 | -0.103 |

### metrla: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.436 | 1.000 |
| gbr_proxies_head | proxy combination, other cities | 2.555 | 8.054 | 3.000 | 1.077 | 3.276 | 1.000 | 3.378 | 2.000 |
| gbr_proxies | proxy combination, other cities | 2.555 | 8.054 | 3.000 | 0.919 | 2.796 | 1.000 | 3.382 | 3.000 |
| ridge_proxies_head | proxy combination, other cities | 2.555 | 8.054 | 3.000 | 1.077 | 3.276 | 1.000 | 3.419 | 2.000 |
| ridge_proxies | proxy combination, other cities | 6.634 | 49.664 |  |  |  | 0.765 | 12.065 | 10.000 |
| ridge_zico_family_params | proxy combination, other cities | 4.263 | 24.161 |  |  |  | 0.375 |  |  |
| gbr_zico_family_params | proxy combination, other cities | 2.555 | 8.054 |  |  |  | 0.425 |  |  |
| best_single_proxy (glass_t) | zero-cost proxy | 5.816 | 39.597 |  |  |  | 0.345 |  |  |

### metrla: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.745 | 0.620 | 0.494 | 0.713 | 0.667 | 0.625 | 0.581 | 0.000 | 0.000 |
| gbr_proxies_head | proxy combination, other cities | 0.757 | 0.561 | 0.419 | 0.667 | 0.608 | 0.563 | 0.525 | 2.555 | 28.205 |
| gbr_zico_family_params | proxy combination, other cities | 0.548 | 0.528 | 0.391 | 0.630 | 0.514 | 0.497 | 0.569 | 2.555 | 28.205 |
| gbr_proxies | proxy combination, other cities | 0.690 | 0.521 | 0.377 | 0.640 | 0.588 | 0.480 | 0.512 | 2.555 | 28.205 |
| ridge_proxies | proxy combination, other cities | 0.519 | 0.443 | 0.285 | 0.553 | 0.557 | 0.237 | 0.565 | 2.555 | 28.205 |
| ridge_proxies_head | proxy combination, other cities | 0.766 | 0.438 | 0.291 | 0.566 | 0.541 | 0.255 | 0.545 | 2.555 | 28.205 |
| ridge_zico_family_params | proxy combination, other cities | 0.294 | 0.421 | 0.265 | 0.536 | 0.513 | 0.227 | 0.548 | 2.555 | 28.205 |
| best_single_proxy (glass_t) | zero-cost proxy | 0.194 | 0.406 | 0.249 | 0.520 | 0.433 | 0.251 | 0.542 | 2.555 | 28.205 |

### pems04: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| ridge_proxies_head | proxy combination, other cities | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.990 | 0.864 | 1.000 |
| gbr_proxies_head | proxy combination, other cities | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.990 | 0.864 | 1.000 |
| gbr_proxies | proxy combination, other cities | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.980 | 0.864 | 1.000 |
| gbr_zico_family_params | proxy combination, other cities | 0.000 | 0.000 | 1.000 | 0.286 | 0.998 | 0.925 | 1.508 | 1.000 |
| transfer_pooled | transfer | 6.574 | 21.477 | 2.000 | 0.295 | 1.031 | 0.990 | 1.556 | 2.000 |
| ridge_proxies | proxy combination, other cities | 8.601 | 36.913 | 8.000 | 1.666 | 5.815 | 0.915 | 5.702 | 5.000 |
| best_single_proxy (glass) | zero-cost proxy | 1.157 | 2.013 | 8.000 | 1.971 | 6.878 | 0.960 | 7.086 | 5.000 |
| ridge_zico_family_params | proxy combination, other cities | 4.784 | 12.752 |  |  |  | 0.045 |  |  |

### pems04: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| best_single_proxy (glass) | zero-cost proxy | 0.588 | 0.686 | 0.575 | 0.759 | 0.618 | 0.622 | 0.799 | 0.000 | 0.000 |
| transfer_pooled | transfer | 0.676 | 0.640 | 0.528 | 0.725 | 0.623 | 0.720 | 0.574 | 6.574 | 46.154 |
| gbr_proxies_head | proxy combination, other cities | 0.644 | 0.619 | 0.512 | 0.713 | 0.595 | 0.715 | 0.540 | 0.846 | 2.564 |
| gbr_proxies | proxy combination, other cities | 0.615 | 0.578 | 0.456 | 0.678 | 0.522 | 0.664 | 0.532 | 0.846 | 2.564 |
| ridge_proxies_head | proxy combination, other cities | 0.601 | 0.557 | 0.418 | 0.656 | 0.503 | 0.521 | 0.632 | 0.846 | 2.564 |
| gbr_zico_family_params | proxy combination, other cities | 0.591 | 0.541 | 0.410 | 0.654 | 0.469 | 0.625 | 0.510 | 0.000 | 0.000 |
| ridge_zico_family_params | proxy combination, other cities | 0.433 | 0.501 | 0.359 | 0.607 | 0.366 | 0.530 | 0.571 | 0.000 | 0.000 |
| ridge_proxies | proxy combination, other cities | 0.478 | 0.467 | 0.327 | 0.586 | 0.368 | 0.396 | 0.610 | 0.000 | 0.000 |

### chengdu: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 2.287 | 6.040 | 3.000 | 0.357 | 1.695 | 0.755 | 2.489 | 3.000 |
| gbr_proxies_head | proxy combination, other cities | 4.685 | 22.148 | 10.000 | 1.454 | 6.904 | 0.755 | 8.642 | 8.000 |
| ridge_proxies_head | proxy combination, other cities | 2.941 | 9.396 |  |  |  | 0.750 | 9.098 | 8.000 |
| gbr_zico_family_params | proxy combination, other cities | 2.941 | 9.396 |  |  |  | 0.745 | 10.279 | 8.000 |
| ridge_proxies | proxy combination, other cities | 9.726 | 72.483 |  |  |  | 0.115 |  |  |
| gbr_proxies | proxy combination, other cities | 4.685 | 22.148 |  |  |  | 0.290 |  |  |
| ridge_zico_family_params | proxy combination, other cities | 4.657 | 21.477 |  |  |  | 0.115 |  |  |
| best_single_proxy (zico_t) | zero-cost proxy | 2.939 | 8.725 |  |  |  | 0.080 |  |  |

### chengdu: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.680 | 0.645 | 0.513 | 0.738 | 0.715 | 0.615 | 0.624 | 2.287 | 12.821 |
| gbr_proxies | proxy combination, other cities | 0.662 | 0.617 | 0.478 | 0.715 | 0.688 | 0.518 | 0.663 | 4.685 | 38.462 |
| gbr_proxies_head | proxy combination, other cities | 0.657 | 0.610 | 0.465 | 0.703 | 0.606 | 0.582 | 0.640 | 4.685 | 38.462 |
| gbr_zico_family_params | proxy combination, other cities | 0.645 | 0.598 | 0.457 | 0.698 | 0.687 | 0.583 | 0.547 | 2.941 | 17.949 |
| best_single_proxy (zico_t) | zero-cost proxy | 0.516 | 0.585 | 0.444 | 0.688 | 0.653 | 0.585 | 0.535 | 2.941 | 17.949 |
| ridge_zico_family_params | proxy combination, other cities | 0.481 | 0.579 | 0.429 | 0.667 | 0.708 | 0.535 | 0.530 | 2.941 | 17.949 |
| ridge_proxies_head | proxy combination, other cities | 0.582 | 0.549 | 0.397 | 0.654 | 0.686 | 0.548 | 0.450 | 2.941 | 17.949 |
| ridge_proxies | proxy combination, other cities | 0.515 | 0.490 | 0.353 | 0.603 | 0.633 | 0.537 | 0.339 | 4.361 | 30.769 |

### shenzhen: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.926 | 1.000 |
| ridge_proxies_head | proxy combination, other cities | 2.965 | 2.685 | 2.000 | 0.564 | 1.765 | 0.955 | 2.646 | 2.000 |
| gbr_proxies_head | proxy combination, other cities | 3.767 | 6.711 | 3.000 | 0.697 | 2.180 | 1.000 | 3.150 | 3.000 |
| gbr_proxies | proxy combination, other cities | 2.965 | 2.685 | 3.000 | 0.697 | 2.180 | 1.000 | 3.223 | 3.000 |
| ridge_proxies | proxy combination, other cities | 4.826 | 15.436 |  |  |  | 0.740 | 9.735 | 8.000 |
| ridge_zico_family_params | proxy combination, other cities | 6.101 | 21.477 |  |  |  | 0.040 |  |  |
| gbr_zico_family_params | proxy combination, other cities | 5.402 | 18.121 |  |  |  | 0.185 |  |  |
| best_single_proxy (zico_t) | zero-cost proxy | 5.123 | 16.779 |  |  |  | 0.060 |  |  |

### shenzhen: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.879 | 0.843 | 0.771 | 0.881 | 0.862 | 0.870 | 0.801 | 0.965 | 2.564 |
| gbr_proxies_head | proxy combination, other cities | 0.847 | 0.809 | 0.728 | 0.850 | 0.774 | 0.866 | 0.777 | 3.767 | 15.385 |
| gbr_proxies | proxy combination, other cities | 0.837 | 0.793 | 0.708 | 0.844 | 0.771 | 0.820 | 0.781 | 2.965 | 7.692 |
| gbr_zico_family_params | proxy combination, other cities | 0.775 | 0.747 | 0.653 | 0.815 | 0.775 | 0.786 | 0.688 | 2.965 | 7.692 |
| ridge_proxies_head | proxy combination, other cities | 0.754 | 0.659 | 0.540 | 0.742 | 0.808 | 0.554 | 0.657 | 2.965 | 7.692 |
| ridge_zico_family_params | proxy combination, other cities | 0.515 | 0.640 | 0.519 | 0.724 | 0.746 | 0.517 | 0.685 | 2.965 | 7.692 |
| best_single_proxy (zico_t) | zero-cost proxy | 0.502 | 0.628 | 0.504 | 0.718 | 0.677 | 0.544 | 0.676 | 2.965 | 7.692 |
| ridge_proxies | proxy combination, other cities | 0.662 | 0.585 | 0.449 | 0.677 | 0.748 | 0.512 | 0.539 | 2.965 | 7.692 |

### expytky: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| gbr_proxies_head | proxy combination, other cities | 0.635 | 0.671 | 1.000 | 0.123 | 0.218 | 1.000 | 0.337 | 1.000 |
| gbr_proxies | proxy combination, other cities | 0.635 | 0.671 | 1.000 | 0.123 | 0.218 | 0.990 | 0.337 | 1.000 |
| transfer_pooled | transfer | 1.455 | 2.013 | 5.000 | 1.276 | 2.257 | 1.000 | 1.754 | 3.000 |
| ridge_proxies_head | proxy combination, other cities | 4.487 | 5.369 | 5.000 | 1.237 | 2.188 | 0.965 | 2.238 | 3.000 |
| ridge_proxies | proxy combination, other cities | 4.958 | 10.738 |  |  |  | 0.800 | 6.241 | 9.000 |
| gbr_zico_family_params | proxy combination, other cities | 4.487 | 5.369 |  |  |  | 0.695 | 8.774 | 8.000 |
| ridge_zico_family_params | proxy combination, other cities | 6.305 | 18.121 |  |  |  | 0.715 | 9.721 | 8.000 |
| best_single_proxy (glass_t) | zero-cost proxy | 7.789 | 32.215 |  |  |  | 0.190 |  |  |

### expytky: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.789 | 0.641 | 0.522 | 0.730 | 0.681 | 0.579 | 0.672 | 1.455 | 7.692 |
| gbr_proxies | proxy combination, other cities | 0.713 | 0.528 | 0.410 | 0.620 | 0.567 | 0.347 | 0.681 | 0.635 | 2.564 |
| gbr_proxies_head | proxy combination, other cities | 0.733 | 0.527 | 0.404 | 0.637 | 0.628 | 0.323 | 0.657 | 0.635 | 2.564 |
| gbr_zico_family_params | proxy combination, other cities | 0.521 | 0.428 | 0.294 | 0.560 | 0.487 | 0.213 | 0.601 | 4.487 | 17.949 |
| ridge_zico_family_params | proxy combination, other cities | 0.383 | 0.388 | 0.238 | 0.493 | 0.489 | -0.005 | 0.707 | 4.487 | 17.949 |
| ridge_proxies | proxy combination, other cities | 0.517 | 0.383 | 0.246 | 0.502 | 0.548 | 0.097 | 0.548 | 4.487 | 17.949 |
| ridge_proxies_head | proxy combination, other cities | 0.627 | 0.355 | 0.215 | 0.476 | 0.439 | 0.048 | 0.601 | 4.487 | 17.949 |
| best_single_proxy (glass_t) | zero-cost proxy | 0.293 | 0.345 | 0.204 | 0.472 | 0.404 | 0.009 | 0.639 | 4.487 | 17.949 |
