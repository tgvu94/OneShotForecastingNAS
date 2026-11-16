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
| metrla | ridge_proxies_head | 0.444 | glass_t | 0.406 | 0.038 | -0.031 | 0.111 |
| pems04 | ridge_proxies_head | 0.557 | glass | 0.686 | -0.129 | -0.215 | -0.046 |
| chengdu | ridge_proxies_head | 0.556 | zico_t | 0.585 | -0.029 | -0.110 | 0.044 |
| shenzhen | ridge_proxies_head | 0.654 | zico_t | 0.628 | 0.026 | -0.045 | 0.094 |
| expytky | ridge_proxies_head | 0.334 | glass_t | 0.350 | -0.015 | -0.103 | 0.068 |
| metrla | gbr_proxies_head | 0.551 | glass_t | 0.406 | 0.145 | 0.041 | 0.249 |
| pems04 | gbr_proxies_head | 0.613 | glass | 0.686 | -0.073 | -0.168 | 0.025 |
| chengdu | gbr_proxies_head | 0.608 | zico_t | 0.585 | 0.023 | -0.091 | 0.128 |
| shenzhen | gbr_proxies_head | 0.799 | zico_t | 0.628 | 0.171 | 0.086 | 0.263 |
| expytky | gbr_proxies_head | 0.525 | glass_t | 0.350 | 0.176 | 0.072 | 0.282 |
| metrla | ridge_proxies | 0.439 | glass_t | 0.406 | 0.033 | -0.058 | 0.119 |
| pems04 | ridge_proxies | 0.474 | glass | 0.686 | -0.212 | -0.311 | -0.110 |
| chengdu | ridge_proxies | 0.491 | zico_t | 0.585 | -0.093 | -0.184 | -0.007 |
| shenzhen | ridge_proxies | 0.594 | zico_t | 0.628 | -0.034 | -0.123 | 0.050 |
| expytky | ridge_proxies | 0.375 | glass_t | 0.350 | 0.025 | -0.091 | 0.133 |
| metrla | gbr_proxies | 0.520 | glass_t | 0.406 | 0.114 | 0.006 | 0.220 |
| pems04 | gbr_proxies | 0.574 | glass | 0.686 | -0.112 | -0.221 | -0.007 |
| chengdu | gbr_proxies | 0.613 | zico_t | 0.585 | 0.028 | -0.083 | 0.130 |
| shenzhen | gbr_proxies | 0.797 | zico_t | 0.628 | 0.169 | 0.081 | 0.263 |
| expytky | gbr_proxies | 0.531 | glass_t | 0.350 | 0.181 | 0.069 | 0.286 |
| metrla | ridge_zico_family_params | 0.424 | glass_t | 0.406 | 0.018 | -0.050 | 0.084 |
| pems04 | ridge_zico_family_params | 0.504 | glass | 0.686 | -0.182 | -0.279 | -0.090 |
| chengdu | ridge_zico_family_params | 0.582 | zico_t | 0.585 | -0.003 | -0.069 | 0.066 |
| shenzhen | ridge_zico_family_params | 0.637 | zico_t | 0.628 | 0.009 | -0.054 | 0.074 |
| expytky | ridge_zico_family_params | 0.355 | glass_t | 0.350 | 0.005 | -0.056 | 0.066 |
| metrla | gbr_zico_family_params | 0.529 | glass_t | 0.406 | 0.123 | 0.022 | 0.232 |
| pems04 | gbr_zico_family_params | 0.530 | glass | 0.686 | -0.156 | -0.263 | -0.051 |
| chengdu | gbr_zico_family_params | 0.590 | zico_t | 0.585 | 0.005 | -0.092 | 0.102 |
| shenzhen | gbr_zico_family_params | 0.751 | zico_t | 0.628 | 0.123 | 0.045 | 0.209 |
| expytky | gbr_zico_family_params | 0.397 | glass_t | 0.350 | 0.047 | -0.059 | 0.147 |

### City and operator family held out together

Kendall with -test MAE on the held-out family at the held-out city; n-weighted over the families with 8 architectures or more.

| city | model | families | kendall_weighted | families_ge_0.5 |
|---|---|---|---|---|
| chengdu | gbr_operator_counts | 12.000 | 0.439 | 4.000 |
| chengdu | gbr_proxies | 12.000 | 0.297 | 0.000 |
| chengdu | gbr_proxies_head | 12.000 | 0.394 | 4.000 |
| chengdu | gbr_zico_family_params | 12.000 | 0.260 | 0.000 |
| chengdu | ridge_operator_counts | 12.000 | 0.433 | 5.000 |
| chengdu | ridge_proxies | 12.000 | 0.305 | 1.000 |
| chengdu | ridge_proxies_head | 12.000 | 0.385 | 3.000 |
| chengdu | ridge_zico_family_params | 12.000 | 0.321 | 0.000 |
| expytky | gbr_operator_counts | 12.000 | 0.438 | 2.000 |
| expytky | gbr_proxies | 12.000 | 0.321 | 1.000 |
| expytky | gbr_proxies_head | 12.000 | 0.429 | 3.000 |
| expytky | gbr_zico_family_params | 12.000 | 0.124 | 0.000 |
| expytky | ridge_operator_counts | 12.000 | 0.457 | 5.000 |
| expytky | ridge_proxies | 12.000 | 0.256 | 0.000 |
| expytky | ridge_proxies_head | 12.000 | 0.368 | 2.000 |
| expytky | ridge_zico_family_params | 12.000 | 0.224 | 2.000 |
| metrla | gbr_operator_counts | 12.000 | 0.521 | 7.000 |
| metrla | gbr_proxies | 12.000 | 0.344 | 2.000 |
| metrla | gbr_proxies_head | 12.000 | 0.483 | 4.000 |
| metrla | gbr_zico_family_params | 12.000 | 0.096 | 0.000 |
| metrla | ridge_operator_counts | 12.000 | 0.511 | 7.000 |
| metrla | ridge_proxies | 12.000 | 0.303 | 1.000 |
| metrla | ridge_proxies_head | 12.000 | 0.530 | 10.000 |
| metrla | ridge_zico_family_params | 12.000 | 0.181 | 0.000 |
| pems04 | gbr_operator_counts | 12.000 | 0.444 | 3.000 |
| pems04 | gbr_proxies | 12.000 | 0.320 | 1.000 |
| pems04 | gbr_proxies_head | 12.000 | 0.418 | 3.000 |
| pems04 | gbr_zico_family_params | 12.000 | 0.191 | 1.000 |
| pems04 | ridge_operator_counts | 12.000 | 0.465 | 4.000 |
| pems04 | ridge_proxies | 12.000 | 0.312 | 2.000 |
| pems04 | ridge_proxies_head | 12.000 | 0.438 | 5.000 |
| pems04 | ridge_zico_family_params | 12.000 | 0.315 | 2.000 |
| shenzhen | gbr_operator_counts | 12.000 | 0.578 | 11.000 |
| shenzhen | gbr_proxies | 12.000 | 0.409 | 5.000 |
| shenzhen | gbr_proxies_head | 12.000 | 0.512 | 9.000 |
| shenzhen | gbr_zico_family_params | 12.000 | 0.265 | 0.000 |
| shenzhen | ridge_operator_counts | 12.000 | 0.589 | 10.000 |
| shenzhen | ridge_proxies | 12.000 | 0.399 | 6.000 |
| shenzhen | ridge_proxies_head | 12.000 | 0.491 | 7.000 |
| shenzhen | ridge_zico_family_params | 12.000 | 0.357 | 1.000 |

### Kendall on the held-out gru family

| model | chengdu | expytky | metrla | pems04 | shenzhen |
|---|---|---|---|---|---|
| gbr_operator_counts | 0.513 | 0.103 | 0.051 | 0.385 | 0.308 |
| gbr_proxies | 0.179 | -0.103 | -0.103 | -0.205 | -0.051 |
| gbr_proxies_head | 0.282 | 0.128 | 0.308 | 0.077 | 0.179 |
| gbr_zico_family_params | 0.282 | -0.128 | -0.103 | -0.051 | -0.026 |
| ridge_operator_counts | 0.462 | 0.000 | 0.308 | 0.359 | 0.359 |
| ridge_proxies | 0.256 | 0.000 | 0.051 | -0.333 | -0.179 |
| ridge_proxies_head | 0.359 | -0.026 | 0.308 | 0.077 | 0.000 |
| ridge_zico_family_params | 0.128 | -0.359 | -0.026 | -0.128 | -0.103 |

### metrla: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.436 | 1.000 |
| gbr_proxies_head | proxy combination, other cities | 0.560 | 2.013 | 1.000 | 0.347 | 1.057 | 1.000 | 1.602 | 1.000 |
| ridge_proxies_head | proxy combination, other cities | 1.038 | 8.054 | 2.000 | 0.759 | 2.311 | 1.000 | 1.913 | 1.000 |
| gbr_proxies | proxy combination, other cities | 1.038 | 8.054 | 3.000 | 0.919 | 2.796 | 1.000 | 3.074 | 2.000 |
| gbr_zico_family_params | proxy combination, other cities | 1.038 | 8.054 | 5.000 | 1.234 | 3.754 | 1.000 | 3.640 | 3.000 |
| ridge_proxies | proxy combination, other cities | 2.694 | 49.664 | 10.000 | 2.674 | 8.138 | 0.970 | 9.285 | 8.000 |
| ridge_zico_family_params | proxy combination, other cities | 1.731 | 24.161 |  |  |  | 0.855 | 9.583 | 8.000 |
| best_single_proxy (glass_t) | zero-cost proxy | 2.362 | 39.597 |  |  |  | 0.625 | 12.388 | 10.000 |

### metrla: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.745 | 0.620 | 0.494 | 0.713 | 0.667 | 0.625 | 0.581 | 0.000 | 0.000 |
| gbr_proxies_head | proxy combination, other cities | 0.753 | 0.551 | 0.407 | 0.664 | 0.625 | 0.539 | 0.509 | 0.560 | 7.692 |
| gbr_zico_family_params | proxy combination, other cities | 0.523 | 0.529 | 0.391 | 0.631 | 0.556 | 0.463 | 0.577 | 1.038 | 28.205 |
| gbr_proxies | proxy combination, other cities | 0.679 | 0.520 | 0.374 | 0.641 | 0.607 | 0.478 | 0.498 | 1.038 | 28.205 |
| ridge_proxies_head | proxy combination, other cities | 0.777 | 0.444 | 0.290 | 0.565 | 0.555 | 0.258 | 0.550 | 1.038 | 28.205 |
| ridge_proxies | proxy combination, other cities | 0.526 | 0.439 | 0.287 | 0.553 | 0.563 | 0.224 | 0.563 | 1.038 | 28.205 |
| ridge_zico_family_params | proxy combination, other cities | 0.292 | 0.424 | 0.265 | 0.540 | 0.519 | 0.234 | 0.546 | 1.038 | 28.205 |
| best_single_proxy (glass_t) | zero-cost proxy | 0.194 | 0.406 | 0.249 | 0.520 | 0.433 | 0.251 | 0.542 | 1.038 | 28.205 |

### pems04: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| gbr_proxies | proxy combination, other cities | 1.312 | 0.671 | 3.000 | 0.586 | 2.046 | 0.980 | 2.274 | 2.000 |
| ridge_proxies_head | proxy combination, other cities | 1.312 | 0.671 | 2.000 | 0.449 | 1.567 | 0.985 | 2.291 | 2.000 |
| gbr_zico_family_params | proxy combination, other cities | 9.174 | 16.779 | 2.000 | 0.446 | 1.558 | 0.925 | 2.341 | 2.000 |
| transfer_pooled | transfer | 10.197 | 21.477 | 5.000 | 0.840 | 2.933 | 0.985 | 4.199 | 5.000 |
| ridge_proxies | proxy combination, other cities | 13.341 | 36.913 | 5.000 | 1.203 | 4.200 | 0.915 | 5.642 | 5.000 |
| gbr_proxies_head | proxy combination, other cities | 5.295 | 10.738 | 10.000 | 1.849 | 6.454 | 0.985 | 6.926 | 8.000 |
| best_single_proxy (glass) | zero-cost proxy | 1.795 | 2.013 | 8.000 | 1.971 | 6.878 | 0.925 | 7.099 | 5.000 |
| ridge_zico_family_params | proxy combination, other cities | 7.421 | 12.752 |  |  |  | 0.035 |  |  |

### pems04: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| best_single_proxy (glass) | zero-cost proxy | 0.588 | 0.686 | 0.575 | 0.759 | 0.618 | 0.622 | 0.799 | 0.000 | 0.000 |
| transfer_pooled | transfer | 0.676 | 0.640 | 0.528 | 0.725 | 0.623 | 0.720 | 0.574 | 10.197 | 46.154 |
| gbr_proxies_head | proxy combination, other cities | 0.642 | 0.613 | 0.501 | 0.706 | 0.581 | 0.714 | 0.536 | 5.295 | 30.769 |
| gbr_proxies | proxy combination, other cities | 0.613 | 0.574 | 0.450 | 0.676 | 0.526 | 0.666 | 0.517 | 1.312 | 2.564 |
| ridge_proxies_head | proxy combination, other cities | 0.604 | 0.557 | 0.423 | 0.652 | 0.491 | 0.519 | 0.642 | 1.312 | 2.564 |
| gbr_zico_family_params | proxy combination, other cities | 0.573 | 0.530 | 0.393 | 0.653 | 0.369 | 0.616 | 0.560 | 0.000 | 0.000 |
| ridge_zico_family_params | proxy combination, other cities | 0.433 | 0.504 | 0.364 | 0.611 | 0.373 | 0.532 | 0.572 | 0.000 | 0.000 |
| ridge_proxies | proxy combination, other cities | 0.480 | 0.474 | 0.334 | 0.596 | 0.362 | 0.401 | 0.628 | 0.000 | 0.000 |

### chengdu: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 2.287 | 6.040 | 3.000 | 0.357 | 1.695 | 0.755 | 2.489 | 3.000 |
| gbr_proxies_head | proxy combination, other cities | 4.685 | 22.148 | 10.000 | 1.454 | 6.904 | 0.755 | 8.677 | 8.000 |
| ridge_proxies_head | proxy combination, other cities | 2.941 | 9.396 |  |  |  | 0.675 | 10.406 | 10.000 |
| gbr_zico_family_params | proxy combination, other cities | 2.941 | 9.396 |  |  |  | 0.740 | 11.160 | 8.000 |
| ridge_proxies | proxy combination, other cities | 9.726 | 72.483 |  |  |  | 0.115 |  |  |
| gbr_proxies | proxy combination, other cities | 2.941 | 9.396 |  |  |  | 0.370 |  |  |
| ridge_zico_family_params | proxy combination, other cities | 4.657 | 21.477 |  |  |  | 0.115 |  |  |
| best_single_proxy (zico_t) | zero-cost proxy | 2.939 | 8.725 |  |  |  | 0.080 |  |  |

### chengdu: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.680 | 0.645 | 0.513 | 0.738 | 0.715 | 0.615 | 0.624 | 2.287 | 12.821 |
| gbr_proxies | proxy combination, other cities | 0.654 | 0.613 | 0.463 | 0.702 | 0.649 | 0.538 | 0.662 | 2.941 | 17.949 |
| gbr_proxies_head | proxy combination, other cities | 0.652 | 0.608 | 0.467 | 0.704 | 0.590 | 0.592 | 0.638 | 4.685 | 38.462 |
| gbr_zico_family_params | proxy combination, other cities | 0.636 | 0.590 | 0.456 | 0.685 | 0.648 | 0.592 | 0.546 | 2.941 | 17.949 |
| best_single_proxy (zico_t) | zero-cost proxy | 0.516 | 0.585 | 0.444 | 0.688 | 0.653 | 0.585 | 0.535 | 2.941 | 17.949 |
| ridge_zico_family_params | proxy combination, other cities | 0.491 | 0.582 | 0.430 | 0.672 | 0.710 | 0.555 | 0.516 | 2.941 | 17.949 |
| ridge_proxies_head | proxy combination, other cities | 0.584 | 0.556 | 0.412 | 0.661 | 0.693 | 0.545 | 0.468 | 2.941 | 17.949 |
| ridge_proxies | proxy combination, other cities | 0.513 | 0.491 | 0.353 | 0.597 | 0.644 | 0.524 | 0.347 | 4.361 | 30.769 |

### shenzhen: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.926 | 1.000 |
| ridge_proxies_head | proxy combination, other cities | 2.965 | 2.685 | 2.000 | 0.564 | 1.765 | 0.955 | 2.646 | 2.000 |
| gbr_proxies_head | proxy combination, other cities | 3.767 | 6.711 | 3.000 | 0.697 | 2.180 | 1.000 | 3.173 | 3.000 |
| gbr_proxies | proxy combination, other cities | 3.767 | 6.711 | 3.000 | 0.697 | 2.180 | 1.000 | 3.221 | 3.000 |
| ridge_proxies | proxy combination, other cities | 4.826 | 15.436 | 10.000 | 2.554 | 7.987 | 0.740 | 9.361 | 8.000 |
| gbr_zico_family_params | proxy combination, other cities | 5.402 | 18.121 |  |  |  | 0.685 | 9.796 | 10.000 |
| ridge_zico_family_params | proxy combination, other cities | 6.101 | 21.477 |  |  |  | 0.040 |  |  |
| best_single_proxy (zico_t) | zero-cost proxy | 5.123 | 16.779 |  |  |  | 0.060 |  |  |

### shenzhen: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.879 | 0.843 | 0.771 | 0.881 | 0.862 | 0.870 | 0.801 | 0.965 | 2.564 |
| gbr_proxies_head | proxy combination, other cities | 0.847 | 0.799 | 0.716 | 0.844 | 0.771 | 0.843 | 0.775 | 3.767 | 15.385 |
| gbr_proxies | proxy combination, other cities | 0.840 | 0.797 | 0.711 | 0.846 | 0.782 | 0.815 | 0.790 | 3.767 | 15.385 |
| gbr_zico_family_params | proxy combination, other cities | 0.771 | 0.751 | 0.659 | 0.810 | 0.760 | 0.784 | 0.711 | 2.965 | 7.692 |
| ridge_proxies_head | proxy combination, other cities | 0.754 | 0.654 | 0.533 | 0.737 | 0.821 | 0.534 | 0.653 | 2.965 | 7.692 |
| ridge_zico_family_params | proxy combination, other cities | 0.511 | 0.637 | 0.520 | 0.719 | 0.743 | 0.511 | 0.686 | 2.965 | 7.692 |
| best_single_proxy (zico_t) | zero-cost proxy | 0.502 | 0.628 | 0.504 | 0.718 | 0.677 | 0.544 | 0.676 | 2.965 | 7.692 |
| ridge_proxies | proxy combination, other cities | 0.666 | 0.594 | 0.466 | 0.689 | 0.778 | 0.494 | 0.560 | 3.148 | 12.821 |

### expytky: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 1.421 | 2.013 | 5.000 | 1.276 | 2.257 | 1.000 | 1.754 | 3.000 |
| gbr_proxies | proxy combination, other cities | 4.382 | 5.369 | 2.000 | 0.689 | 1.219 | 0.995 | 1.829 | 2.000 |
| gbr_proxies_head | proxy combination, other cities | 4.382 | 5.369 | 2.000 | 0.689 | 1.219 | 1.000 | 1.842 | 2.000 |
| ridge_proxies_head | proxy combination, other cities | 4.382 | 5.369 | 5.000 | 1.237 | 2.188 | 0.980 | 2.238 | 3.000 |
| gbr_zico_family_params | proxy combination, other cities | 8.609 | 46.980 | 8.000 | 2.775 | 4.910 | 0.710 | 5.367 | 5.000 |
| ridge_proxies | proxy combination, other cities | 8.609 | 46.980 |  |  |  | 0.775 | 6.878 | 10.000 |
| ridge_zico_family_params | proxy combination, other cities | 6.158 | 18.121 |  |  |  | 0.735 | 8.276 | 8.000 |
| best_single_proxy (glass_t) | zero-cost proxy | 7.607 | 32.215 |  |  |  | 0.265 |  |  |

### expytky: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.789 | 0.641 | 0.522 | 0.730 | 0.681 | 0.579 | 0.672 | 1.421 | 7.692 |
| gbr_proxies | proxy combination, other cities | 0.705 | 0.531 | 0.401 | 0.625 | 0.580 | 0.366 | 0.660 | 4.382 | 17.949 |
| gbr_proxies_head | proxy combination, other cities | 0.725 | 0.525 | 0.400 | 0.639 | 0.650 | 0.353 | 0.606 | 4.382 | 17.949 |
| gbr_zico_family_params | proxy combination, other cities | 0.456 | 0.397 | 0.247 | 0.524 | 0.483 | 0.197 | 0.533 | 1.290 | 5.128 |
| ridge_proxies | proxy combination, other cities | 0.491 | 0.375 | 0.247 | 0.493 | 0.580 | 0.111 | 0.489 | 6.461 | 48.718 |
| ridge_zico_family_params | proxy combination, other cities | 0.344 | 0.355 | 0.204 | 0.477 | 0.464 | 0.008 | 0.622 | 4.382 | 17.949 |
| best_single_proxy (glass_t) | zero-cost proxy | 0.283 | 0.350 | 0.203 | 0.484 | 0.419 | 0.018 | 0.631 | 4.382 | 17.949 |
| ridge_proxies_head | proxy combination, other cities | 0.601 | 0.334 | 0.195 | 0.465 | 0.459 | 0.030 | 0.547 | 4.382 | 17.949 |
