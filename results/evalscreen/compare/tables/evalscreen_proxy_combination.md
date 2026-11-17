# evalscreen proxy_combination: a model on the proxy scores, fit on the other cities

Inputs: the 27 stored scores as ranks inside the city (set `proxies`), with the head one-hot (`proxies_head`), or the ZiCo family and the parameter count alone (`zico_family_params`). Models: ridge, gradient boosting (300 trees, depth 3, mean of 3 fit seeds). Target of the fit: within-city rank of -test MAE of the three training cities. Pass: inside the heads rho >= 0.5 and above the best single proxy at three of four cities, the paired CI of the difference excludes 0 at two cities or more, and the n-weighted Kendall on a held-out family at the held-out city is >= 0.5 at three of four cities. The best single proxy is chosen with the labels of the held-out city, which favours the baseline.

### Verdict per model

| model | cities_rho_ge_05_and_above | cities_ci_excludes_0 | cities_family_kendall_ge_05 | pass |
|---|---|---|---|---|
| gbr_proxies | 3 | 1 | 0 | False |
| gbr_proxies_head | 3 | 2 | 1 | False |
| gbr_zico_family_params | 3 | 2 | 0 | False |
| ridge_proxies | 0 | 0 | 0 | False |
| ridge_proxies_head | 1 | 0 | 1 | False |
| ridge_zico_family_params | 1 | 0 | 0 | False |

### Inside the heads: the model against the best single proxy

diff = within-head rho of the model minus that of the best single proxy; CI from 1000 paired stratified resamples.

| city | model | rho_within_head | best_single_proxy | best_single_within | diff | diff_ci_lo | diff_ci_hi |
|---|---|---|---|---|---|---|---|
| metrla | ridge_proxies_head | 0.411 | glass_t | 0.406 | 0.006 | -0.073 | 0.083 |
| pems04 | ridge_proxies_head | 0.550 | glass | 0.686 | -0.136 | -0.223 | -0.051 |
| chengdu | ridge_proxies_head | 0.549 | zico_t | 0.585 | -0.036 | -0.125 | 0.039 |
| shenzhen | ridge_proxies_head | 0.666 | zico_t | 0.628 | 0.037 | -0.026 | 0.104 |
| metrla | gbr_proxies_head | 0.521 | glass_t | 0.406 | 0.115 | 0.008 | 0.214 |
| pems04 | gbr_proxies_head | 0.596 | glass | 0.686 | -0.090 | -0.190 | 0.004 |
| chengdu | gbr_proxies_head | 0.608 | zico_t | 0.585 | 0.023 | -0.085 | 0.130 |
| shenzhen | gbr_proxies_head | 0.761 | zico_t | 0.628 | 0.132 | 0.049 | 0.220 |
| metrla | ridge_proxies | 0.419 | glass_t | 0.406 | 0.013 | -0.086 | 0.106 |
| pems04 | ridge_proxies | 0.485 | glass | 0.686 | -0.201 | -0.302 | -0.104 |
| chengdu | ridge_proxies | 0.498 | zico_t | 0.585 | -0.086 | -0.178 | -0.000 |
| shenzhen | ridge_proxies | 0.626 | zico_t | 0.628 | -0.002 | -0.080 | 0.078 |
| metrla | gbr_proxies | 0.502 | glass_t | 0.406 | 0.096 | -0.013 | 0.203 |
| pems04 | gbr_proxies | 0.539 | glass | 0.686 | -0.147 | -0.259 | -0.041 |
| chengdu | gbr_proxies | 0.600 | zico_t | 0.585 | 0.015 | -0.102 | 0.126 |
| shenzhen | gbr_proxies | 0.774 | zico_t | 0.628 | 0.145 | 0.059 | 0.234 |
| metrla | ridge_zico_family_params | 0.426 | glass_t | 0.406 | 0.020 | -0.048 | 0.089 |
| pems04 | ridge_zico_family_params | 0.507 | glass | 0.686 | -0.179 | -0.275 | -0.090 |
| chengdu | ridge_zico_family_params | 0.574 | zico_t | 0.585 | -0.011 | -0.082 | 0.056 |
| shenzhen | ridge_zico_family_params | 0.632 | zico_t | 0.628 | 0.004 | -0.058 | 0.064 |
| metrla | gbr_zico_family_params | 0.529 | glass_t | 0.406 | 0.124 | 0.026 | 0.218 |
| pems04 | gbr_zico_family_params | 0.531 | glass | 0.686 | -0.155 | -0.258 | -0.056 |
| chengdu | gbr_zico_family_params | 0.587 | zico_t | 0.585 | 0.002 | -0.095 | 0.089 |
| shenzhen | gbr_zico_family_params | 0.722 | zico_t | 0.628 | 0.094 | 0.013 | 0.187 |

### City and operator family held out together

Kendall with -test MAE on the held-out family at the held-out city; n-weighted over the families with 8 architectures or more.

| city | model | families | kendall_weighted | families_ge_0.5 |
|---|---|---|---|---|
| chengdu | gbr_operator_counts | 12.000 | 0.444 | 4.000 |
| chengdu | gbr_proxies | 12.000 | 0.298 | 1.000 |
| chengdu | gbr_proxies_head | 12.000 | 0.393 | 3.000 |
| chengdu | gbr_zico_family_params | 12.000 | 0.271 | 1.000 |
| chengdu | ridge_operator_counts | 12.000 | 0.430 | 3.000 |
| chengdu | ridge_proxies | 12.000 | 0.316 | 1.000 |
| chengdu | ridge_proxies_head | 12.000 | 0.393 | 3.000 |
| chengdu | ridge_zico_family_params | 12.000 | 0.331 | 0.000 |
| metrla | gbr_operator_counts | 12.000 | 0.473 | 6.000 |
| metrla | gbr_proxies | 12.000 | 0.340 | 1.000 |
| metrla | gbr_proxies_head | 12.000 | 0.450 | 4.000 |
| metrla | gbr_zico_family_params | 12.000 | 0.123 | 0.000 |
| metrla | ridge_operator_counts | 12.000 | 0.462 | 4.000 |
| metrla | ridge_proxies | 12.000 | 0.258 | 0.000 |
| metrla | ridge_proxies_head | 12.000 | 0.466 | 2.000 |
| metrla | ridge_zico_family_params | 12.000 | 0.138 | 0.000 |
| pems04 | gbr_operator_counts | 12.000 | 0.455 | 3.000 |
| pems04 | gbr_proxies | 12.000 | 0.283 | 1.000 |
| pems04 | gbr_proxies_head | 12.000 | 0.392 | 2.000 |
| pems04 | gbr_zico_family_params | 12.000 | 0.222 | 2.000 |
| pems04 | ridge_operator_counts | 12.000 | 0.457 | 4.000 |
| pems04 | ridge_proxies | 12.000 | 0.312 | 2.000 |
| pems04 | ridge_proxies_head | 12.000 | 0.439 | 3.000 |
| pems04 | ridge_zico_family_params | 12.000 | 0.323 | 1.000 |
| shenzhen | gbr_operator_counts | 12.000 | 0.569 | 10.000 |
| shenzhen | gbr_proxies | 12.000 | 0.412 | 3.000 |
| shenzhen | gbr_proxies_head | 12.000 | 0.513 | 8.000 |
| shenzhen | gbr_zico_family_params | 12.000 | 0.277 | 0.000 |
| shenzhen | ridge_operator_counts | 12.000 | 0.589 | 10.000 |
| shenzhen | ridge_proxies | 12.000 | 0.399 | 6.000 |
| shenzhen | ridge_proxies_head | 12.000 | 0.506 | 8.000 |
| shenzhen | ridge_zico_family_params | 12.000 | 0.354 | 2.000 |

### Kendall on the held-out gru family

| model | chengdu | metrla | pems04 | shenzhen |
|---|---|---|---|---|
| gbr_operator_counts | 0.462 | 0.026 | 0.359 | 0.128 |
| gbr_proxies | 0.179 | -0.026 | -0.154 | 0.103 |
| gbr_proxies_head | 0.359 | 0.282 | 0.051 | 0.231 |
| gbr_zico_family_params | 0.154 | -0.103 | 0.103 | 0.128 |
| ridge_operator_counts | 0.462 | 0.103 | 0.359 | 0.231 |
| ridge_proxies | 0.231 | 0.026 | -0.333 | -0.128 |
| ridge_proxies_head | 0.359 | 0.282 | 0.179 | 0.026 |
| ridge_zico_family_params | 0.128 | -0.256 | -0.154 | -0.154 |

### metrla: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 1.283 | 1.342 | 2.000 | 0.498 | 1.515 | 1.000 | 2.185 | 2.000 |
| gbr_proxies_head | proxy combination, other cities | 2.555 | 8.054 | 3.000 | 1.049 | 3.191 | 1.000 | 4.402 | 3.000 |
| gbr_proxies | proxy combination, other cities | 2.555 | 8.054 | 5.000 | 1.336 | 4.065 | 0.990 | 6.152 | 5.000 |
| ridge_proxies_head | proxy combination, other cities | 2.555 | 8.054 | 8.000 | 2.193 | 6.672 | 0.995 | 6.372 | 5.000 |
| gbr_zico_family_params | proxy combination, other cities | 2.555 | 8.054 |  |  |  | 0.565 | 11.394 | 10.000 |
| ridge_proxies | proxy combination, other cities | 4.132 | 22.819 |  |  |  | 0.625 | 12.171 | 10.000 |
| ridge_zico_family_params | proxy combination, other cities | 4.263 | 24.161 |  |  |  | 0.250 |  |  |
| best_single_proxy (glass_t) | zero-cost proxy | 5.816 | 39.597 |  |  |  | 0.345 |  |  |

### metrla: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.683 | 0.578 | 0.442 | 0.675 | 0.673 | 0.598 | 0.489 | 1.283 | 5.128 |
| gbr_zico_family_params | proxy combination, other cities | 0.507 | 0.529 | 0.400 | 0.637 | 0.547 | 0.477 | 0.569 | 2.555 | 28.205 |
| gbr_proxies_head | proxy combination, other cities | 0.701 | 0.521 | 0.384 | 0.640 | 0.593 | 0.501 | 0.488 | 2.555 | 28.205 |
| gbr_proxies | proxy combination, other cities | 0.637 | 0.502 | 0.352 | 0.629 | 0.580 | 0.470 | 0.477 | 2.555 | 28.205 |
| ridge_zico_family_params | proxy combination, other cities | 0.212 | 0.426 | 0.273 | 0.542 | 0.513 | 0.235 | 0.554 | 2.555 | 28.205 |
| ridge_proxies | proxy combination, other cities | 0.439 | 0.419 | 0.271 | 0.529 | 0.544 | 0.214 | 0.534 | 2.555 | 28.205 |
| ridge_proxies_head | proxy combination, other cities | 0.672 | 0.411 | 0.259 | 0.536 | 0.496 | 0.229 | 0.532 | 2.555 | 28.205 |
| best_single_proxy (glass_t) | zero-cost proxy | 0.194 | 0.406 | 0.249 | 0.520 | 0.433 | 0.251 | 0.542 | 2.555 | 28.205 |

### pems04: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| gbr_proxies_head | proxy combination, other cities | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.990 | 0.859 | 1.000 |
| gbr_proxies | proxy combination, other cities | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.980 | 0.864 | 1.000 |
| transfer_pooled | transfer | 2.635 | 6.711 | 3.000 | 0.426 | 1.485 | 0.995 | 2.192 | 3.000 |
| gbr_zico_family_params | proxy combination, other cities | 5.914 | 16.779 | 2.000 | 0.446 | 1.558 | 0.970 | 2.338 | 2.000 |
| ridge_proxies_head | proxy combination, other cities | 3.406 | 10.067 | 3.000 | 0.610 | 2.131 | 0.985 | 3.126 | 2.000 |
| best_single_proxy (glass) | zero-cost proxy | 1.157 | 2.013 | 8.000 | 1.971 | 6.878 | 0.960 | 7.086 | 5.000 |
| ridge_proxies | proxy combination, other cities | 8.601 | 36.913 | 10.000 | 1.975 | 6.894 | 0.915 | 7.873 | 8.000 |
| ridge_zico_family_params | proxy combination, other cities | 4.784 | 12.752 |  |  |  | 0.045 |  |  |

### pems04: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| best_single_proxy (glass) | zero-cost proxy | 0.588 | 0.686 | 0.575 | 0.759 | 0.618 | 0.622 | 0.799 | 0.000 | 0.000 |
| transfer_pooled | transfer | 0.667 | 0.634 | 0.520 | 0.725 | 0.632 | 0.715 | 0.553 | 2.635 | 17.949 |
| gbr_proxies_head | proxy combination, other cities | 0.633 | 0.596 | 0.483 | 0.684 | 0.587 | 0.675 | 0.523 | 0.846 | 2.564 |
| ridge_proxies_head | proxy combination, other cities | 0.602 | 0.550 | 0.409 | 0.644 | 0.492 | 0.530 | 0.613 | 3.406 | 28.205 |
| gbr_proxies | proxy combination, other cities | 0.592 | 0.539 | 0.405 | 0.639 | 0.491 | 0.612 | 0.502 | 0.846 | 2.564 |
| gbr_zico_family_params | proxy combination, other cities | 0.583 | 0.531 | 0.390 | 0.647 | 0.442 | 0.606 | 0.521 | 0.000 | 0.000 |
| ridge_zico_family_params | proxy combination, other cities | 0.439 | 0.507 | 0.359 | 0.614 | 0.366 | 0.533 | 0.583 | 0.000 | 0.000 |
| ridge_proxies | proxy combination, other cities | 0.491 | 0.485 | 0.339 | 0.609 | 0.383 | 0.409 | 0.634 | 0.000 | 0.000 |

### chengdu: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 2.287 | 6.040 | 2.000 | 0.257 | 1.218 | 0.755 | 1.828 | 2.000 |
| ridge_proxies_head | proxy combination, other cities | 2.941 | 9.396 | 8.000 | 1.246 | 5.918 | 0.755 | 8.964 | 8.000 |
| gbr_proxies_head | proxy combination, other cities | 4.685 | 22.148 |  |  |  | 0.720 | 9.339 | 10.000 |
| gbr_zico_family_params | proxy combination, other cities | 2.941 | 9.396 |  |  |  | 0.750 | 10.476 | 8.000 |
| ridge_proxies | proxy combination, other cities | 9.726 | 72.483 |  |  |  | 0.095 |  |  |
| gbr_proxies | proxy combination, other cities | 2.941 | 9.396 |  |  |  | 0.280 |  |  |
| ridge_zico_family_params | proxy combination, other cities | 4.657 | 21.477 |  |  |  | 0.115 |  |  |
| best_single_proxy (zico_t) | zero-cost proxy | 2.939 | 8.725 |  |  |  | 0.080 |  |  |

### chengdu: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.688 | 0.657 | 0.529 | 0.750 | 0.702 | 0.664 | 0.618 | 2.287 | 12.821 |
| gbr_proxies_head | proxy combination, other cities | 0.645 | 0.608 | 0.471 | 0.706 | 0.564 | 0.641 | 0.606 | 4.685 | 38.462 |
| gbr_proxies | proxy combination, other cities | 0.648 | 0.600 | 0.459 | 0.697 | 0.618 | 0.566 | 0.621 | 2.941 | 17.949 |
| gbr_zico_family_params | proxy combination, other cities | 0.630 | 0.587 | 0.457 | 0.694 | 0.635 | 0.617 | 0.523 | 2.941 | 17.949 |
| best_single_proxy (zico_t) | zero-cost proxy | 0.516 | 0.585 | 0.444 | 0.688 | 0.653 | 0.585 | 0.535 | 2.941 | 17.949 |
| ridge_zico_family_params | proxy combination, other cities | 0.484 | 0.574 | 0.422 | 0.668 | 0.692 | 0.545 | 0.516 | 2.941 | 17.949 |
| ridge_proxies_head | proxy combination, other cities | 0.592 | 0.549 | 0.402 | 0.653 | 0.639 | 0.551 | 0.481 | 2.941 | 17.949 |
| ridge_proxies | proxy combination, other cities | 0.524 | 0.498 | 0.364 | 0.610 | 0.623 | 0.548 | 0.358 | 4.361 | 30.769 |

### shenzhen: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.926 | 1.000 |
| gbr_proxies | proxy combination, other cities | 3.767 | 6.711 | 5.000 | 1.007 | 3.150 | 0.965 | 3.367 | 3.000 |
| ridge_proxies_head | proxy combination, other cities | 2.965 | 2.685 | 3.000 | 0.888 | 2.778 | 0.925 | 4.093 | 3.000 |
| gbr_proxies_head | proxy combination, other cities | 3.767 | 6.711 | 8.000 | 1.914 | 5.985 | 0.955 | 5.465 | 5.000 |
| ridge_proxies | proxy combination, other cities | 4.826 | 15.436 |  |  |  | 0.520 | 11.211 | 10.000 |
| ridge_zico_family_params | proxy combination, other cities | 6.101 | 21.477 |  |  |  | 0.040 |  |  |
| gbr_zico_family_params | proxy combination, other cities | 5.402 | 18.121 |  |  |  | 0.260 |  |  |
| best_single_proxy (zico_t) | zero-cost proxy | 5.123 | 16.779 |  |  |  | 0.060 |  |  |

### shenzhen: head control

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.869 | 0.845 | 0.771 | 0.886 | 0.824 | 0.872 | 0.834 | 0.965 | 2.564 |
| gbr_proxies | proxy combination, other cities | 0.824 | 0.774 | 0.680 | 0.828 | 0.748 | 0.767 | 0.798 | 3.767 | 15.385 |
| gbr_proxies_head | proxy combination, other cities | 0.831 | 0.761 | 0.675 | 0.816 | 0.717 | 0.773 | 0.779 | 3.767 | 15.385 |
| gbr_zico_family_params | proxy combination, other cities | 0.737 | 0.722 | 0.620 | 0.785 | 0.718 | 0.723 | 0.724 | 3.767 | 15.385 |
| ridge_proxies_head | proxy combination, other cities | 0.764 | 0.666 | 0.546 | 0.740 | 0.808 | 0.537 | 0.691 | 2.965 | 7.692 |
| ridge_zico_family_params | proxy combination, other cities | 0.506 | 0.632 | 0.510 | 0.715 | 0.738 | 0.501 | 0.686 | 2.965 | 7.692 |
| best_single_proxy (zico_t) | zero-cost proxy | 0.502 | 0.628 | 0.504 | 0.718 | 0.677 | 0.544 | 0.676 | 2.965 | 7.692 |
| ridge_proxies | proxy combination, other cities | 0.680 | 0.626 | 0.504 | 0.714 | 0.813 | 0.532 | 0.584 | 2.965 | 7.692 |
