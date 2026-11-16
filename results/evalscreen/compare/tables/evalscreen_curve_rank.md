# evalscreen curve_rank: a model on the first k epochs, fit on the other cities

Inputs: ranks inside the city of the val MAE and the train loss at each of the first k epochs, their change from epoch 1 to k, the rank of the last two inside the head, and the head one-hot. Models: ridge, gradient boosting, fit on three cities, scored on the fourth. inverse_epoch = a least-squares fit of val(e) = a + b / e per run, read at epoch 20, with no fit across cities. loss_sum = the sum of the train loss over the first k epochs, z-scored inside each head. Every score costs k epochs of the whole list. Pass: inside the heads rho >= 0.6 at k <= 3 at three of four cities, and above early validation at the same k at every late city (all four, see base).

### Verdict per model

| model | cities_rho_ge_06_at_k_le_3 | cities_ge_06_and_above_early_val | cities_above_early_val_at_k3 | cities_ci_excludes_0_at_k3 | pass |
|---|---|---|---|---|---|
| gbr_curve | 1 | 1 | 1 | 0 | False |
| inverse_epoch | 0 | 0 | 0 | 0 | False |
| loss_sum | 0 | 0 | 2 | 1 | False |
| ridge_curve | 1 | 1 | 2 | 0 | False |

### Spearman inside the heads, by k

| model | k | chengdu | metrla | pems04 | shenzhen |
|---|---|---|---|---|---|
| gbr_curve | 1 | 0.250 | 0.322 | 0.341 | 0.282 |
| gbr_curve | 2 | 0.429 | 0.459 | 0.362 | 0.522 |
| gbr_curve | 3 | 0.552 | 0.511 | 0.406 | 0.605 |
| gbr_curve | 5 | 0.721 | 0.644 | 0.674 | 0.728 |
| inverse_epoch | 2 | 0.370 | 0.381 | 0.152 | 0.098 |
| inverse_epoch | 3 | 0.476 | 0.505 | 0.256 | 0.286 |
| inverse_epoch | 5 | 0.690 | 0.666 | 0.475 | 0.525 |
| loss_sum | 1 | 0.226 | 0.452 | 0.513 | 0.501 |
| loss_sum | 2 | 0.276 | 0.414 | 0.532 | 0.559 |
| loss_sum | 3 | 0.318 | 0.389 | 0.553 | 0.580 |
| loss_sum | 5 | 0.374 | 0.346 | 0.608 | 0.592 |
| ridge_curve | 1 | 0.238 | 0.470 | 0.489 | 0.365 |
| ridge_curve | 2 | 0.347 | 0.508 | 0.341 | 0.580 |
| ridge_curve | 3 | 0.551 | 0.493 | 0.487 | 0.641 |
| ridge_curve | 5 | 0.763 | 0.689 | 0.740 | 0.753 |

### Early validation inside the heads, by k (the baseline)

| k | chengdu | metrla | pems04 | shenzhen |
|---|---|---|---|---|
| 1.000 | 0.158 | 0.446 | 0.312 | 0.367 |
| 2.000 | 0.398 | 0.557 | 0.309 | 0.411 |
| 3.000 | 0.583 | 0.591 | 0.428 | 0.579 |
| 5.000 | 0.727 | 0.697 | 0.676 | 0.700 |

### Against early validation at the same k

CI from 1000 paired stratified resamples.

| city | k | model | rho_within_head | early_val_within | diff | diff_ci_lo | diff_ci_hi |
|---|---|---|---|---|---|---|---|
| metrla | 1 | ridge_curve | 0.470 | 0.446 | 0.024 | -0.086 | 0.143 |
| metrla | 1 | gbr_curve | 0.322 | 0.446 | -0.123 | -0.251 | 0.007 |
| metrla | 1 | loss_sum | 0.452 | 0.446 | 0.007 | -0.128 | 0.155 |
| pems04 | 1 | ridge_curve | 0.489 | 0.312 | 0.177 | 0.050 | 0.301 |
| pems04 | 1 | gbr_curve | 0.341 | 0.312 | 0.029 | -0.136 | 0.208 |
| pems04 | 1 | loss_sum | 0.513 | 0.312 | 0.201 | 0.035 | 0.352 |
| chengdu | 1 | ridge_curve | 0.238 | 0.158 | 0.080 | -0.053 | 0.214 |
| chengdu | 1 | gbr_curve | 0.250 | 0.158 | 0.092 | -0.074 | 0.248 |
| chengdu | 1 | loss_sum | 0.226 | 0.158 | 0.068 | -0.076 | 0.219 |
| shenzhen | 1 | ridge_curve | 0.365 | 0.367 | -0.002 | -0.165 | 0.173 |
| shenzhen | 1 | gbr_curve | 0.282 | 0.367 | -0.085 | -0.265 | 0.092 |
| shenzhen | 1 | loss_sum | 0.501 | 0.367 | 0.134 | -0.005 | 0.276 |
| metrla | 2 | ridge_curve | 0.508 | 0.557 | -0.049 | -0.134 | 0.043 |
| metrla | 2 | gbr_curve | 0.459 | 0.557 | -0.098 | -0.217 | 0.023 |
| metrla | 2 | loss_sum | 0.414 | 0.557 | -0.143 | -0.274 | 0.001 |
| metrla | 2 | inverse_epoch | 0.381 | 0.557 | -0.176 | -0.305 | -0.055 |
| pems04 | 2 | ridge_curve | 0.341 | 0.309 | 0.032 | -0.022 | 0.084 |
| pems04 | 2 | gbr_curve | 0.362 | 0.309 | 0.052 | -0.049 | 0.144 |
| pems04 | 2 | loss_sum | 0.532 | 0.309 | 0.223 | 0.103 | 0.340 |
| pems04 | 2 | inverse_epoch | 0.152 | 0.309 | -0.157 | -0.304 | -0.003 |
| chengdu | 2 | ridge_curve | 0.347 | 0.398 | -0.051 | -0.132 | 0.026 |
| chengdu | 2 | gbr_curve | 0.429 | 0.398 | 0.031 | -0.101 | 0.154 |
| chengdu | 2 | loss_sum | 0.276 | 0.398 | -0.122 | -0.250 | 0.002 |
| chengdu | 2 | inverse_epoch | 0.370 | 0.398 | -0.028 | -0.157 | 0.103 |
| shenzhen | 2 | ridge_curve | 0.580 | 0.411 | 0.168 | 0.062 | 0.279 |
| shenzhen | 2 | gbr_curve | 0.522 | 0.411 | 0.111 | -0.042 | 0.248 |
| shenzhen | 2 | loss_sum | 0.559 | 0.411 | 0.148 | 0.013 | 0.291 |
| shenzhen | 2 | inverse_epoch | 0.098 | 0.411 | -0.313 | -0.458 | -0.136 |
| metrla | 3 | ridge_curve | 0.493 | 0.591 | -0.098 | -0.159 | -0.035 |
| metrla | 3 | gbr_curve | 0.511 | 0.591 | -0.080 | -0.164 | 0.003 |
| metrla | 3 | loss_sum | 0.389 | 0.591 | -0.203 | -0.331 | -0.073 |
| metrla | 3 | inverse_epoch | 0.505 | 0.591 | -0.086 | -0.199 | 0.021 |
| pems04 | 3 | ridge_curve | 0.487 | 0.428 | 0.058 | -0.025 | 0.140 |
| pems04 | 3 | gbr_curve | 0.406 | 0.428 | -0.023 | -0.102 | 0.056 |
| pems04 | 3 | loss_sum | 0.553 | 0.428 | 0.125 | 0.015 | 0.231 |
| pems04 | 3 | inverse_epoch | 0.256 | 0.428 | -0.172 | -0.311 | -0.038 |
| chengdu | 3 | ridge_curve | 0.551 | 0.583 | -0.032 | -0.095 | 0.026 |
| chengdu | 3 | gbr_curve | 0.552 | 0.583 | -0.031 | -0.112 | 0.047 |
| chengdu | 3 | loss_sum | 0.318 | 0.583 | -0.264 | -0.381 | -0.152 |
| chengdu | 3 | inverse_epoch | 0.476 | 0.583 | -0.107 | -0.226 | 0.018 |
| shenzhen | 3 | ridge_curve | 0.641 | 0.579 | 0.062 | -0.015 | 0.133 |
| shenzhen | 3 | gbr_curve | 0.605 | 0.579 | 0.026 | -0.067 | 0.110 |
| shenzhen | 3 | loss_sum | 0.580 | 0.579 | 0.001 | -0.135 | 0.123 |
| shenzhen | 3 | inverse_epoch | 0.286 | 0.579 | -0.293 | -0.438 | -0.132 |
| metrla | 5 | ridge_curve | 0.689 | 0.697 | -0.008 | -0.062 | 0.041 |
| metrla | 5 | gbr_curve | 0.644 | 0.697 | -0.053 | -0.127 | 0.031 |
| metrla | 5 | loss_sum | 0.346 | 0.697 | -0.351 | -0.484 | -0.218 |
| metrla | 5 | inverse_epoch | 0.666 | 0.697 | -0.031 | -0.114 | 0.042 |
| pems04 | 5 | ridge_curve | 0.740 | 0.676 | 0.063 | -0.004 | 0.130 |
| pems04 | 5 | gbr_curve | 0.674 | 0.676 | -0.002 | -0.063 | 0.060 |
| pems04 | 5 | loss_sum | 0.608 | 0.676 | -0.069 | -0.155 | 0.018 |
| pems04 | 5 | inverse_epoch | 0.475 | 0.676 | -0.201 | -0.304 | -0.097 |
| chengdu | 5 | ridge_curve | 0.763 | 0.727 | 0.035 | -0.011 | 0.088 |
| chengdu | 5 | gbr_curve | 0.721 | 0.727 | -0.006 | -0.068 | 0.048 |
| chengdu | 5 | loss_sum | 0.374 | 0.727 | -0.354 | -0.465 | -0.243 |
| chengdu | 5 | inverse_epoch | 0.690 | 0.727 | -0.037 | -0.141 | 0.072 |
| shenzhen | 5 | ridge_curve | 0.753 | 0.700 | 0.053 | 0.013 | 0.099 |
| shenzhen | 5 | gbr_curve | 0.728 | 0.700 | 0.028 | -0.023 | 0.081 |
| shenzhen | 5 | loss_sum | 0.592 | 0.700 | -0.108 | -0.229 | 0.010 |
| shenzhen | 5 | inverse_epoch | 0.525 | 0.700 | -0.175 | -0.298 | -0.065 |

### metrla: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.521 | 1.342 | 1.000 | 0.181 | 0.550 | 1.000 | 0.840 | 1.000 |
| ridge_curve_k1 | curve model, other cities | 0.560 | 2.013 | 1.000 | 2.542 | 7.734 | 1.000 | 8.220 | 1.000 |
| loss_sum_k1 | train-loss sum | 0.560 | 2.013 | 1.000 | 2.542 | 7.734 | 0.980 | 8.305 | 1.000 |
| gbr_curve_k1 | curve model, other cities | 1.403 | 14.765 | 3.000 | 2.961 | 9.011 | 1.000 | 9.390 | 2.000 |
| early_val_k1 | brief training | 1.922 | 29.530 | 3.000 | 3.127 | 9.514 | 1.000 | 9.566 | 2.000 |
| early_val_k2 | brief training | 0.000 | 0.000 | 1.000 | 4.498 | 13.687 | 1.000 | 14.022 | 1.000 |
| ridge_curve_k2 | curve model, other cities | 0.000 | 0.000 | 1.000 | 4.498 | 13.687 | 1.000 | 14.063 | 1.000 |
| gbr_curve_k2 | curve model, other cities | 0.645 | 3.356 | 1.000 | 4.493 | 13.673 | 1.000 | 14.172 | 1.000 |
| inverse_epoch_k2 | extrapolation, no fit | 3.346 | 57.047 | 5.000 | 5.285 | 16.082 | 1.000 | 15.790 | 3.000 |
| loss_sum_k2 | train-loss sum | 2.694 | 49.664 | 8.000 | 5.749 | 17.493 | 0.990 | 20.040 | 8.000 |
| early_val_k3 | brief training | 0.000 | 0.000 | 1.000 | 6.489 | 19.745 | 1.000 | 20.232 | 1.000 |
| gbr_curve_k3 | curve model, other cities | 1.248 | 12.081 | 2.000 | 6.699 | 20.385 | 1.000 | 20.589 | 1.000 |
| inverse_epoch_k3 | extrapolation, no fit | 1.612 | 20.805 | 2.000 | 6.665 | 20.280 | 1.000 | 20.776 | 2.000 |
| ridge_curve_k3 | curve model, other cities | 1.038 | 8.054 | 2.000 | 6.831 | 20.787 | 1.000 | 20.855 | 1.000 |
| loss_sum_k3 | train-loss sum | 2.694 | 49.664 | 8.000 | 7.646 | 23.265 | 0.945 | 23.613 | 5.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 10.486 | 31.907 | 1.000 | 32.199 | 1.000 |
| inverse_epoch_k5 | extrapolation, no fit | 0.000 | 0.000 | 1.000 | 10.486 | 31.907 | 1.000 | 32.319 | 1.000 |
| ridge_curve_k5 | curve model, other cities | 0.000 | 0.000 | 1.000 | 10.486 | 31.907 | 1.000 | 32.329 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 0.645 | 3.356 | 1.000 | 10.484 | 31.900 | 1.000 | 32.453 | 1.000 |
| loss_sum_k5 | train-loss sum | 2.694 | 49.664 |  |  |  | 0.980 | 36.805 | 8.000 |

### pems04: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 4.087 | 6.711 | 5.000 | 0.840 | 2.933 | 0.985 | 4.346 | 5.000 |
| ridge_curve_k3 | curve model, other cities | 7.828 | 14.094 |  |  |  | 0.790 | 24.647 | 10.000 |
| ridge_curve_k5 | curve model, other cities | 0.000 | 0.000 | 1.000 | 7.543 | 26.327 | 1.000 | 26.724 | 1.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 7.543 | 26.327 | 0.955 | 26.736 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 7.828 | 14.094 | 5.000 | 8.074 | 28.182 | 0.995 | 28.243 | 3.000 |
| inverse_epoch_k5 | extrapolation, no fit | 9.859 | 20.134 |  |  |  | 0.615 | 33.219 | 10.000 |
| early_val_k1 | brief training | 24.317 | 85.906 |  |  |  | 0.000 |  |  |
| ridge_curve_k1 | curve model, other cities | 11.931 | 29.530 |  |  |  | 0.360 |  |  |
| gbr_curve_k1 | curve model, other cities | 13.564 | 38.255 |  |  |  | 0.250 |  |  |
| loss_sum_k1 | train-loss sum | 10.227 | 22.148 |  |  |  | 0.220 |  |  |
| early_val_k2 | brief training | 18.963 | 63.087 |  |  |  | 0.000 |  |  |
| ridge_curve_k2 | curve model, other cities | 11.693 | 28.188 |  |  |  | 0.260 |  |  |
| gbr_curve_k2 | curve model, other cities | 11.700 | 28.859 |  |  |  | 0.005 |  |  |
| loss_sum_k2 | train-loss sum | 10.227 | 22.148 |  |  |  | 0.010 |  |  |
| inverse_epoch_k2 | extrapolation, no fit | 9.859 | 20.134 |  |  |  | 0.005 |  |  |
| early_val_k3 | brief training | 4.625 | 8.725 |  |  |  | 0.235 |  |  |
| gbr_curve_k3 | curve model, other cities | 7.828 | 14.094 |  |  |  | 0.300 |  |  |
| loss_sum_k3 | train-loss sum | 10.227 | 22.148 |  |  |  | 0.005 |  |  |
| inverse_epoch_k3 | extrapolation, no fit | 9.859 | 20.134 |  |  |  | 0.005 |  |  |
| loss_sum_k5 | train-loss sum | 3.191 | 5.369 |  |  |  | 0.255 |  |  |

### chengdu: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 2.287 | 6.040 | 2.000 | 0.257 | 1.218 | 0.755 | 1.828 | 2.000 |
| ridge_curve_k1 | curve model, other cities | 3.950 | 14.094 | 8.000 | 2.424 | 11.512 | 0.750 | 11.129 | 5.000 |
| gbr_curve_k2 | curve model, other cities | 2.287 | 6.040 | 2.000 | 2.811 | 13.350 | 0.755 | 13.852 | 2.000 |
| early_val_k1 | brief training | 6.321 | 33.557 |  |  |  | 0.655 | 14.950 | 10.000 |
| early_val_k2 | brief training | 2.958 | 10.067 | 8.000 | 3.480 | 16.526 | 0.750 | 16.652 | 5.000 |
| inverse_epoch_k2 | extrapolation, no fit | 9.014 | 69.128 | 8.000 | 3.598 | 17.087 | 0.710 | 17.623 | 5.000 |
| ridge_curve_k2 | curve model, other cities | 2.958 | 10.067 | 8.000 | 3.481 | 16.529 | 0.755 | 19.232 | 8.000 |
| early_val_k3 | brief training | 2.288 | 6.711 | 3.000 | 4.139 | 19.654 | 0.755 | 20.149 | 3.000 |
| gbr_curve_k3 | curve model, other cities | 2.287 | 6.040 | 5.000 | 4.493 | 21.333 | 0.755 | 21.341 | 3.000 |
| ridge_curve_k3 | curve model, other cities | 2.958 | 10.067 | 5.000 | 4.428 | 21.025 | 0.755 | 21.354 | 3.000 |
| inverse_epoch_k3 | extrapolation, no fit | 7.547 | 51.678 | 5.000 | 4.353 | 20.672 | 0.755 | 22.089 | 5.000 |
| inverse_epoch_k5 | extrapolation, no fit | 0.429 | 0.671 | 1.000 | 6.445 | 30.605 | 0.995 | 31.060 | 1.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 6.452 | 30.637 | 0.890 | 31.080 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 2.287 | 6.040 | 5.000 | 6.946 | 32.982 | 0.755 | 33.007 | 3.000 |
| ridge_curve_k5 | curve model, other cities | 2.941 | 9.396 | 8.000 | 7.312 | 34.722 | 0.775 | 36.416 | 8.000 |
| gbr_curve_k1 | curve model, other cities | 2.287 | 6.040 |  |  |  | 0.285 |  |  |
| loss_sum_k1 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.485 |  |  |
| loss_sum_k2 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.040 |  |  |
| loss_sum_k3 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.030 |  |  |
| loss_sum_k5 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.090 |  |  |

### shenzhen: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.926 | 1.000 |
| gbr_curve_k1 | curve model, other cities | 10.078 | 64.430 | 10.000 | 3.847 | 12.034 | 0.965 | 11.530 | 6.500 |
| ridge_curve_k1 | curve model, other cities | 3.796 | 7.383 | 8.000 | 3.788 | 11.848 | 0.725 | 14.279 | 8.000 |
| ridge_curve_k2 | curve model, other cities | 3.148 | 4.698 | 5.000 | 4.530 | 14.168 | 0.930 | 15.676 | 5.000 |
| gbr_curve_k2 | curve model, other cities | 3.097 | 4.027 | 8.000 | 5.447 | 17.037 | 1.000 | 16.066 | 5.000 |
| ridge_curve_k3 | curve model, other cities | 0.965 | 0.671 | 1.000 | 5.404 | 16.902 | 1.000 | 17.310 | 1.000 |
| gbr_curve_k3 | curve model, other cities | 3.148 | 4.698 | 2.000 | 5.617 | 17.569 | 1.000 | 18.041 | 2.000 |
| early_val_k2 | brief training | 4.673 | 14.094 |  |  |  | 0.705 | 20.500 | 10.000 |
| early_val_k3 | brief training | 4.673 | 14.094 | 8.000 | 6.791 | 21.242 | 0.970 | 21.124 | 5.000 |
| ridge_curve_k5 | curve model, other cities | 0.000 | 0.000 | 1.000 | 8.785 | 27.478 | 1.000 | 27.854 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 0.965 | 0.671 | 1.000 | 8.838 | 27.645 | 1.000 | 27.893 | 1.000 |
| early_val_k5 | brief training | 3.148 | 4.698 | 2.000 | 9.027 | 28.235 | 1.000 | 28.775 | 2.000 |
| early_val_k1 | brief training | 5.339 | 17.450 |  |  |  | 0.040 |  |  |
| loss_sum_k1 | train-loss sum | 3.751 | 6.040 |  |  |  | 0.075 |  |  |
| loss_sum_k2 | train-loss sum | 8.394 | 45.638 |  |  |  | 0.025 |  |  |
| inverse_epoch_k2 | extrapolation, no fit | 11.499 | 75.839 |  |  |  | 0.000 |  |  |
| loss_sum_k3 | train-loss sum | 8.394 | 45.638 |  |  |  | 0.005 |  |  |
| inverse_epoch_k3 | extrapolation, no fit | 14.814 | 91.946 |  |  |  | 0.010 |  |  |
| loss_sum_k5 | train-loss sum | 8.394 | 45.638 |  |  |  | 0.010 |  |  |
| inverse_epoch_k5 | extrapolation, no fit | 6.193 | 24.161 |  |  |  | 0.240 |  |  |
