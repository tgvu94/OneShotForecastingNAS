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
| metrla | ridge_proxies_head | 0.435 | glass_t | 0.406 | 0.029 | -0.046 | 0.107 |
| pems04 | ridge_proxies_head | 0.562 | glass | 0.686 | -0.124 | -0.210 | -0.039 |
| chengdu | ridge_proxies_head | 0.557 | zico_t | 0.585 | -0.028 | -0.108 | 0.044 |
| shenzhen | ridge_proxies_head | 0.657 | zico_t | 0.628 | 0.028 | -0.048 | 0.098 |
| expytky | ridge_proxies_head | 0.337 | glass_t | 0.350 | -0.013 | -0.098 | 0.073 |
| metrla | gbr_proxies_head | 0.550 | glass_t | 0.406 | 0.144 | 0.039 | 0.246 |
| pems04 | gbr_proxies_head | 0.608 | glass | 0.686 | -0.078 | -0.178 | 0.023 |
| chengdu | gbr_proxies_head | 0.605 | zico_t | 0.585 | 0.020 | -0.097 | 0.123 |
| shenzhen | gbr_proxies_head | 0.807 | zico_t | 0.628 | 0.179 | 0.095 | 0.270 |
| expytky | gbr_proxies_head | 0.526 | glass_t | 0.350 | 0.176 | 0.070 | 0.281 |
| metrla | ridge_proxies | 0.437 | glass_t | 0.406 | 0.031 | -0.064 | 0.120 |
| pems04 | ridge_proxies | 0.468 | glass | 0.686 | -0.218 | -0.316 | -0.116 |
| chengdu | ridge_proxies | 0.494 | zico_t | 0.585 | -0.091 | -0.180 | -0.005 |
| shenzhen | ridge_proxies | 0.602 | zico_t | 0.628 | -0.027 | -0.111 | 0.056 |
| expytky | ridge_proxies | 0.377 | glass_t | 0.350 | 0.027 | -0.089 | 0.132 |
| metrla | gbr_proxies | 0.518 | glass_t | 0.406 | 0.112 | 0.004 | 0.217 |
| pems04 | gbr_proxies | 0.572 | glass | 0.686 | -0.114 | -0.221 | -0.010 |
| chengdu | gbr_proxies | 0.617 | zico_t | 0.585 | 0.032 | -0.082 | 0.137 |
| shenzhen | gbr_proxies | 0.797 | zico_t | 0.628 | 0.169 | 0.079 | 0.265 |
| expytky | gbr_proxies | 0.537 | glass_t | 0.350 | 0.187 | 0.072 | 0.291 |
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
| chengdu | gbr_proxies | 12.000 | 0.294 | 1.000 |
| chengdu | gbr_proxies_head | 12.000 | 0.390 | 4.000 |
| chengdu | gbr_zico_family_params | 12.000 | 0.260 | 0.000 |
| chengdu | ridge_operator_counts | 12.000 | 0.433 | 5.000 |
| chengdu | ridge_proxies | 12.000 | 0.300 | 1.000 |
| chengdu | ridge_proxies_head | 12.000 | 0.385 | 4.000 |
| chengdu | ridge_zico_family_params | 12.000 | 0.321 | 0.000 |
| expytky | gbr_operator_counts | 12.000 | 0.438 | 2.000 |
| expytky | gbr_proxies | 12.000 | 0.324 | 1.000 |
| expytky | gbr_proxies_head | 12.000 | 0.430 | 2.000 |
| expytky | gbr_zico_family_params | 12.000 | 0.124 | 0.000 |
| expytky | ridge_operator_counts | 12.000 | 0.457 | 5.000 |
| expytky | ridge_proxies | 12.000 | 0.255 | 0.000 |
| expytky | ridge_proxies_head | 12.000 | 0.375 | 2.000 |
| expytky | ridge_zico_family_params | 12.000 | 0.224 | 2.000 |
| metrla | gbr_operator_counts | 12.000 | 0.521 | 7.000 |
| metrla | gbr_proxies | 12.000 | 0.350 | 1.000 |
| metrla | gbr_proxies_head | 12.000 | 0.486 | 4.000 |
| metrla | gbr_zico_family_params | 12.000 | 0.096 | 0.000 |
| metrla | ridge_operator_counts | 12.000 | 0.511 | 7.000 |
| metrla | ridge_proxies | 12.000 | 0.309 | 1.000 |
| metrla | ridge_proxies_head | 12.000 | 0.524 | 9.000 |
| metrla | ridge_zico_family_params | 12.000 | 0.181 | 0.000 |
| pems04 | gbr_operator_counts | 12.000 | 0.444 | 3.000 |
| pems04 | gbr_proxies | 12.000 | 0.321 | 1.000 |
| pems04 | gbr_proxies_head | 12.000 | 0.426 | 3.000 |
| pems04 | gbr_zico_family_params | 12.000 | 0.191 | 1.000 |
| pems04 | ridge_operator_counts | 12.000 | 0.465 | 4.000 |
| pems04 | ridge_proxies | 12.000 | 0.312 | 2.000 |
| pems04 | ridge_proxies_head | 12.000 | 0.439 | 5.000 |
| pems04 | ridge_zico_family_params | 12.000 | 0.315 | 2.000 |
| shenzhen | gbr_operator_counts | 12.000 | 0.578 | 11.000 |
| shenzhen | gbr_proxies | 12.000 | 0.417 | 4.000 |
| shenzhen | gbr_proxies_head | 12.000 | 0.517 | 9.000 |
| shenzhen | gbr_zico_family_params | 12.000 | 0.265 | 0.000 |
| shenzhen | ridge_operator_counts | 12.000 | 0.589 | 10.000 |
| shenzhen | ridge_proxies | 12.000 | 0.399 | 6.000 |
| shenzhen | ridge_proxies_head | 12.000 | 0.494 | 7.000 |
| shenzhen | ridge_zico_family_params | 12.000 | 0.357 | 1.000 |

### Kendall on the held-out gru family

| model | chengdu | expytky | metrla | pems04 | shenzhen |
|---|---|---|---|---|---|
| gbr_operator_counts | 0.513 | 0.103 | 0.051 | 0.385 | 0.308 |
| gbr_proxies | 0.154 | -0.128 | -0.051 | -0.205 | 0.000 |
| gbr_proxies_head | 0.282 | 0.128 | 0.359 | 0.051 | 0.179 |
| gbr_zico_family_params | 0.282 | -0.128 | -0.103 | -0.051 | -0.026 |
| ridge_operator_counts | 0.462 | 0.000 | 0.308 | 0.359 | 0.359 |
| ridge_proxies | 0.231 | 0.000 | 0.103 | -0.385 | -0.256 |
| ridge_proxies_head | 0.359 | -0.026 | 0.308 | 0.051 | -0.026 |
| ridge_zico_family_params | 0.128 | -0.359 | -0.026 | -0.128 | -0.103 |

### metrla: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.436 | 1.000 |
| gbr_proxies | proxy combination, other cities | 2.274 | 8.054 | 3.000 | 0.919 | 2.796 | 1.000 | 3.335 | 2.000 |
| ridge_proxies_head | proxy combination, other cities | 2.274 | 8.054 | 3.000 | 1.077 | 3.276 | 1.000 | 3.419 | 2.000 |
| gbr_proxies_head | proxy combination, other cities | 1.226 | 2.013 | 5.000 | 1.644 | 5.001 | 1.000 | 4.512 | 3.000 |
| ridge_proxies | proxy combination, other cities | 5.902 | 49.664 |  |  |  | 0.750 | 12.019 | 10.000 |
| ridge_zico_family_params | proxy combination, other cities | 3.793 | 24.161 |  |  |  | 0.390 |  |  |
| gbr_zico_family_params | proxy combination, other cities | 2.274 | 8.054 |  |  |  | 0.345 |  |  |
| best_single_proxy (glass_t) | zero-cost proxy | 5.175 | 39.597 |  |  |  | 0.345 |  |  |

### metrla: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.745 | 0.620 | 0.494 | 0.713 | 0.667 | 0.625 | 0.581 | 0.000 | 0.000 |
| gbr_proxies_head | proxy combination, other cities | 0.751 | 0.550 | 0.411 | 0.662 | 0.623 | 0.538 | 0.510 | 1.226 | 7.692 |
| gbr_zico_family_params | proxy combination, other cities | 0.523 | 0.529 | 0.391 | 0.631 | 0.556 | 0.463 | 0.577 | 2.274 | 28.205 |
| gbr_proxies | proxy combination, other cities | 0.683 | 0.518 | 0.367 | 0.640 | 0.603 | 0.474 | 0.500 | 2.274 | 28.205 |
| ridge_proxies | proxy combination, other cities | 0.522 | 0.437 | 0.287 | 0.551 | 0.570 | 0.215 | 0.562 | 2.274 | 28.205 |
| ridge_proxies_head | proxy combination, other cities | 0.772 | 0.435 | 0.291 | 0.557 | 0.539 | 0.249 | 0.546 | 2.274 | 28.205 |
| ridge_zico_family_params | proxy combination, other cities | 0.292 | 0.424 | 0.265 | 0.540 | 0.519 | 0.234 | 0.546 | 2.274 | 28.205 |
| best_single_proxy (glass_t) | zero-cost proxy | 0.194 | 0.406 | 0.249 | 0.520 | 0.433 | 0.251 | 0.542 | 2.274 | 28.205 |

### pems04: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| gbr_proxies | proxy combination, other cities | 0.835 | 0.671 | 1.000 | 0.163 | 0.568 | 0.980 | 0.864 | 1.000 |
| ridge_proxies_head | proxy combination, other cities | 0.000 | 0.000 | 1.000 | 0.286 | 0.998 | 0.990 | 1.482 | 1.000 |
| gbr_proxies_head | proxy combination, other cities | 3.369 | 10.738 | 2.000 | 0.292 | 1.018 | 0.990 | 1.532 | 2.000 |
| transfer_pooled | transfer | 6.488 | 21.477 | 2.000 | 0.295 | 1.031 | 0.990 | 1.556 | 2.000 |
| gbr_zico_family_params | proxy combination, other cities | 5.837 | 16.779 | 2.000 | 0.446 | 1.558 | 0.925 | 2.341 | 2.000 |
| ridge_proxies | proxy combination, other cities | 8.489 | 36.913 | 5.000 | 1.203 | 4.200 | 0.925 | 5.642 | 5.000 |
| best_single_proxy (glass) | zero-cost proxy | 1.142 | 2.013 | 8.000 | 1.971 | 6.878 | 0.960 | 7.086 | 5.000 |
| ridge_zico_family_params | proxy combination, other cities | 4.722 | 12.752 |  |  |  | 0.060 |  |  |

### pems04: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| best_single_proxy (glass) | zero-cost proxy | 0.588 | 0.686 | 0.575 | 0.759 | 0.618 | 0.622 | 0.799 | 0.000 | 0.000 |
| transfer_pooled | transfer | 0.676 | 0.640 | 0.528 | 0.725 | 0.623 | 0.720 | 0.574 | 6.488 | 46.154 |
| gbr_proxies_head | proxy combination, other cities | 0.642 | 0.608 | 0.498 | 0.701 | 0.576 | 0.711 | 0.529 | 3.369 | 30.769 |
| gbr_proxies | proxy combination, other cities | 0.617 | 0.572 | 0.449 | 0.674 | 0.526 | 0.649 | 0.528 | 0.835 | 2.564 |
| ridge_proxies_head | proxy combination, other cities | 0.605 | 0.562 | 0.430 | 0.657 | 0.497 | 0.527 | 0.644 | 0.000 | 0.000 |
| gbr_zico_family_params | proxy combination, other cities | 0.573 | 0.530 | 0.393 | 0.653 | 0.369 | 0.616 | 0.560 | 0.000 | 0.000 |
| ridge_zico_family_params | proxy combination, other cities | 0.433 | 0.504 | 0.364 | 0.611 | 0.373 | 0.532 | 0.572 | 0.000 | 0.000 |
| ridge_proxies | proxy combination, other cities | 0.479 | 0.468 | 0.327 | 0.590 | 0.354 | 0.391 | 0.628 | 0.000 | 0.000 |

### chengdu: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 2.287 | 6.040 | 3.000 | 0.357 | 1.695 | 0.755 | 2.489 | 3.000 |
| gbr_proxies_head | proxy combination, other cities | 4.685 | 22.148 | 10.000 | 1.454 | 6.904 | 0.755 | 8.812 | 8.000 |
| ridge_proxies_head | proxy combination, other cities | 2.941 | 9.396 |  |  |  | 0.740 | 9.672 | 10.000 |
| gbr_zico_family_params | proxy combination, other cities | 2.941 | 9.396 |  |  |  | 0.740 | 11.160 | 8.000 |
| ridge_proxies | proxy combination, other cities | 9.874 | 74.497 |  |  |  | 0.115 |  |  |
| gbr_proxies | proxy combination, other cities | 4.685 | 22.148 |  |  |  | 0.465 |  |  |
| ridge_zico_family_params | proxy combination, other cities | 4.657 | 21.477 |  |  |  | 0.115 |  |  |
| best_single_proxy (zico_t) | zero-cost proxy | 2.939 | 8.725 |  |  |  | 0.080 |  |  |

### chengdu: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.680 | 0.645 | 0.513 | 0.738 | 0.715 | 0.615 | 0.624 | 2.287 | 12.821 |
| gbr_proxies | proxy combination, other cities | 0.660 | 0.617 | 0.466 | 0.711 | 0.652 | 0.547 | 0.660 | 4.685 | 38.462 |
| gbr_proxies_head | proxy combination, other cities | 0.653 | 0.605 | 0.456 | 0.703 | 0.590 | 0.586 | 0.634 | 4.685 | 38.462 |
| gbr_zico_family_params | proxy combination, other cities | 0.636 | 0.590 | 0.456 | 0.685 | 0.648 | 0.592 | 0.546 | 2.941 | 17.949 |
| best_single_proxy (zico_t) | zero-cost proxy | 0.516 | 0.585 | 0.444 | 0.688 | 0.653 | 0.585 | 0.535 | 2.941 | 17.949 |
| ridge_zico_family_params | proxy combination, other cities | 0.491 | 0.582 | 0.430 | 0.672 | 0.710 | 0.555 | 0.516 | 2.941 | 17.949 |
| ridge_proxies_head | proxy combination, other cities | 0.584 | 0.557 | 0.410 | 0.656 | 0.695 | 0.541 | 0.472 | 2.941 | 17.949 |
| ridge_proxies | proxy combination, other cities | 0.508 | 0.494 | 0.357 | 0.602 | 0.646 | 0.515 | 0.363 | 4.361 | 30.769 |

### shenzhen: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.926 | 1.000 |
| gbr_proxies_head | proxy combination, other cities | 3.767 | 6.711 | 2.000 | 0.331 | 1.036 | 1.000 | 1.560 | 2.000 |
| gbr_proxies | proxy combination, other cities | 2.965 | 2.685 | 3.000 | 0.697 | 2.180 | 1.000 | 3.221 | 3.000 |
| ridge_proxies_head | proxy combination, other cities | 2.965 | 2.685 | 3.000 | 0.888 | 2.778 | 0.955 | 4.093 | 3.000 |
| gbr_zico_family_params | proxy combination, other cities | 5.402 | 18.121 |  |  |  | 0.685 | 9.796 | 10.000 |
| ridge_proxies | proxy combination, other cities | 4.826 | 15.436 | 10.000 | 2.554 | 7.987 | 0.740 | 9.829 | 8.000 |
| ridge_zico_family_params | proxy combination, other cities | 6.101 | 21.477 |  |  |  | 0.040 |  |  |
| best_single_proxy (zico_t) | zero-cost proxy | 5.123 | 16.779 |  |  |  | 0.060 |  |  |

### shenzhen: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.879 | 0.843 | 0.771 | 0.881 | 0.862 | 0.870 | 0.801 | 0.965 | 2.564 |
| gbr_proxies_head | proxy combination, other cities | 0.850 | 0.807 | 0.720 | 0.849 | 0.769 | 0.853 | 0.789 | 3.767 | 15.385 |
| gbr_proxies | proxy combination, other cities | 0.839 | 0.797 | 0.713 | 0.847 | 0.783 | 0.818 | 0.788 | 2.965 | 7.692 |
| gbr_zico_family_params | proxy combination, other cities | 0.771 | 0.751 | 0.659 | 0.810 | 0.760 | 0.784 | 0.711 | 2.965 | 7.692 |
| ridge_proxies_head | proxy combination, other cities | 0.756 | 0.657 | 0.535 | 0.734 | 0.813 | 0.541 | 0.658 | 2.965 | 7.692 |
| ridge_zico_family_params | proxy combination, other cities | 0.511 | 0.637 | 0.520 | 0.719 | 0.743 | 0.511 | 0.686 | 2.965 | 7.692 |
| best_single_proxy (zico_t) | zero-cost proxy | 0.502 | 0.628 | 0.504 | 0.718 | 0.677 | 0.544 | 0.676 | 2.965 | 7.692 |
| ridge_proxies | proxy combination, other cities | 0.672 | 0.602 | 0.479 | 0.692 | 0.783 | 0.499 | 0.573 | 3.148 | 12.821 |

### expytky: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| gbr_proxies_head | proxy combination, other cities | 0.635 | 0.671 | 1.000 | 0.123 | 0.218 | 1.000 | 0.337 | 1.000 |
| transfer_pooled | transfer | 1.455 | 2.013 | 5.000 | 1.276 | 2.257 | 1.000 | 1.754 | 3.000 |
| gbr_proxies | proxy combination, other cities | 4.487 | 5.369 | 2.000 | 0.689 | 1.219 | 0.995 | 1.829 | 2.000 |
| ridge_proxies_head | proxy combination, other cities | 4.487 | 5.369 | 5.000 | 1.237 | 2.188 | 0.980 | 2.238 | 3.000 |
| gbr_zico_family_params | proxy combination, other cities | 8.816 | 46.980 | 8.000 | 2.775 | 4.910 | 0.710 | 5.367 | 5.000 |
| ridge_proxies | proxy combination, other cities | 8.816 | 46.980 |  |  |  | 0.775 | 6.878 | 10.000 |
| ridge_zico_family_params | proxy combination, other cities | 6.305 | 18.121 |  |  |  | 0.735 | 8.276 | 8.000 |
| best_single_proxy (glass_t) | zero-cost proxy | 7.789 | 32.215 |  |  |  | 0.265 |  |  |

### expytky: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.789 | 0.641 | 0.522 | 0.730 | 0.681 | 0.579 | 0.672 | 1.455 | 7.692 |
| gbr_proxies | proxy combination, other cities | 0.713 | 0.537 | 0.402 | 0.630 | 0.581 | 0.387 | 0.655 | 4.487 | 17.949 |
| gbr_proxies_head | proxy combination, other cities | 0.729 | 0.526 | 0.403 | 0.640 | 0.652 | 0.353 | 0.608 | 0.635 | 2.564 |
| gbr_zico_family_params | proxy combination, other cities | 0.456 | 0.397 | 0.247 | 0.524 | 0.483 | 0.197 | 0.533 | 1.321 | 5.128 |
| ridge_proxies | proxy combination, other cities | 0.495 | 0.377 | 0.248 | 0.490 | 0.580 | 0.116 | 0.489 | 6.616 | 48.718 |
| ridge_zico_family_params | proxy combination, other cities | 0.344 | 0.355 | 0.204 | 0.477 | 0.464 | 0.008 | 0.622 | 4.487 | 17.949 |
| best_single_proxy (glass_t) | zero-cost proxy | 0.283 | 0.350 | 0.203 | 0.484 | 0.419 | 0.018 | 0.631 | 4.487 | 17.949 |
| ridge_proxies_head | proxy combination, other cities | 0.606 | 0.337 | 0.199 | 0.466 | 0.459 | 0.045 | 0.540 | 4.487 | 17.949 |
