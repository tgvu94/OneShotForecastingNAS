# evalscreen curve_rank: a model on the first k epochs, fit on the other cities

Inputs: ranks inside the city of the val MAE and the train loss at each of the first k epochs, their change from epoch 1 to k, the rank of the last two inside the head, and the head one-hot. Models: ridge, gradient boosting, fit on three cities, scored on the fourth. inverse_epoch = a least-squares fit of val(e) = a + b / e per run, read at epoch 20, with no fit across cities. loss_sum = the sum of the train loss over the first k epochs, z-scored inside each head. Every score costs k epochs of the whole list. Pass: inside the heads rho >= 0.6 at k <= 3 at three of four cities, and above early validation at the same k at every late city (all four, see base).

### Verdict per model

| model | cities_rho_ge_06_at_k_le_3 | cities_ge_06_and_above_early_val | cities_above_early_val_at_k3 | cities_ci_excludes_0_at_k3 | pass |
|---|---|---|---|---|---|
| gbr_curve | 1 | 1 | 1 | 0 | False |
| inverse_epoch | 1 | 0 | 0 | 0 | False |
| loss_sum | 0 | 0 | 2 | 1 | False |
| ridge_curve | 1 | 1 | 2 | 0 | False |

### Spearman inside the heads, by k

| model | k | chengdu | expytky | metrla | pems04 | shenzhen |
|---|---|---|---|---|---|---|
| gbr_curve | 1 | 0.211 | 0.240 | 0.352 | 0.415 | 0.390 |
| gbr_curve | 2 | 0.429 | 0.393 | 0.520 | 0.318 | 0.548 |
| gbr_curve | 3 | 0.578 | 0.566 | 0.564 | 0.364 | 0.631 |
| gbr_curve | 5 | 0.717 | 0.654 | 0.656 | 0.645 | 0.728 |
| inverse_epoch | 2 | 0.370 | 0.432 | 0.381 | 0.152 | 0.098 |
| inverse_epoch | 3 | 0.476 | 0.604 | 0.505 | 0.256 | 0.286 |
| inverse_epoch | 5 | 0.690 | 0.709 | 0.666 | 0.475 | 0.525 |
| loss_sum | 1 | 0.226 | 0.274 | 0.452 | 0.513 | 0.501 |
| loss_sum | 2 | 0.276 | 0.189 | 0.414 | 0.532 | 0.559 |
| loss_sum | 3 | 0.318 | 0.129 | 0.389 | 0.553 | 0.580 |
| loss_sum | 5 | 0.374 | 0.075 | 0.346 | 0.608 | 0.592 |
| ridge_curve | 1 | 0.237 | 0.294 | 0.467 | 0.493 | 0.474 |
| ridge_curve | 2 | 0.372 | 0.333 | 0.581 | 0.307 | 0.507 |
| ridge_curve | 3 | 0.562 | 0.567 | 0.580 | 0.445 | 0.618 |
| ridge_curve | 5 | 0.777 | 0.720 | 0.680 | 0.735 | 0.751 |

### Early validation inside the heads, by k (the baseline)

| k | chengdu | expytky | metrla | pems04 | shenzhen |
|---|---|---|---|---|---|
| 1.000 | 0.158 | 0.173 | 0.446 | 0.312 | 0.367 |
| 2.000 | 0.398 | 0.504 | 0.557 | 0.309 | 0.411 |
| 3.000 | 0.583 | 0.666 | 0.591 | 0.428 | 0.579 |
| 5.000 | 0.727 | 0.718 | 0.697 | 0.676 | 0.700 |

### Against early validation at the same k

CI from 1000 paired stratified resamples.

| city | k | model | rho_within_head | early_val_within | diff | diff_ci_lo | diff_ci_hi |
|---|---|---|---|---|---|---|---|
| metrla | 1 | ridge_curve | 0.467 | 0.446 | 0.021 | -0.090 | 0.140 |
| metrla | 1 | gbr_curve | 0.352 | 0.446 | -0.094 | -0.224 | 0.047 |
| metrla | 1 | loss_sum | 0.452 | 0.446 | 0.007 | -0.128 | 0.155 |
| pems04 | 1 | ridge_curve | 0.493 | 0.312 | 0.181 | 0.042 | 0.312 |
| pems04 | 1 | gbr_curve | 0.415 | 0.312 | 0.103 | -0.064 | 0.264 |
| pems04 | 1 | loss_sum | 0.513 | 0.312 | 0.201 | 0.035 | 0.352 |
| chengdu | 1 | ridge_curve | 0.237 | 0.158 | 0.079 | -0.060 | 0.217 |
| chengdu | 1 | gbr_curve | 0.211 | 0.158 | 0.053 | -0.112 | 0.225 |
| chengdu | 1 | loss_sum | 0.226 | 0.158 | 0.068 | -0.076 | 0.219 |
| shenzhen | 1 | ridge_curve | 0.474 | 0.367 | 0.107 | -0.036 | 0.252 |
| shenzhen | 1 | gbr_curve | 0.390 | 0.367 | 0.024 | -0.137 | 0.192 |
| shenzhen | 1 | loss_sum | 0.501 | 0.367 | 0.134 | -0.005 | 0.276 |
| expytky | 1 | ridge_curve | 0.294 | 0.173 | 0.121 | -0.016 | 0.259 |
| expytky | 1 | gbr_curve | 0.240 | 0.173 | 0.066 | -0.096 | 0.220 |
| expytky | 1 | loss_sum | 0.274 | 0.173 | 0.100 | -0.031 | 0.235 |
| metrla | 2 | ridge_curve | 0.581 | 0.557 | 0.024 | -0.026 | 0.078 |
| metrla | 2 | gbr_curve | 0.520 | 0.557 | -0.037 | -0.146 | 0.069 |
| metrla | 2 | loss_sum | 0.414 | 0.557 | -0.143 | -0.274 | 0.001 |
| metrla | 2 | inverse_epoch | 0.381 | 0.557 | -0.176 | -0.305 | -0.055 |
| pems04 | 2 | ridge_curve | 0.307 | 0.309 | -0.003 | -0.058 | 0.047 |
| pems04 | 2 | gbr_curve | 0.318 | 0.309 | 0.008 | -0.094 | 0.100 |
| pems04 | 2 | loss_sum | 0.532 | 0.309 | 0.223 | 0.103 | 0.340 |
| pems04 | 2 | inverse_epoch | 0.152 | 0.309 | -0.157 | -0.304 | -0.003 |
| chengdu | 2 | ridge_curve | 0.372 | 0.398 | -0.026 | -0.091 | 0.039 |
| chengdu | 2 | gbr_curve | 0.429 | 0.398 | 0.031 | -0.077 | 0.148 |
| chengdu | 2 | loss_sum | 0.276 | 0.398 | -0.122 | -0.250 | 0.002 |
| chengdu | 2 | inverse_epoch | 0.370 | 0.398 | -0.028 | -0.157 | 0.103 |
| shenzhen | 2 | ridge_curve | 0.507 | 0.411 | 0.096 | -0.001 | 0.187 |
| shenzhen | 2 | gbr_curve | 0.548 | 0.411 | 0.137 | 0.010 | 0.249 |
| shenzhen | 2 | loss_sum | 0.559 | 0.411 | 0.148 | 0.013 | 0.291 |
| shenzhen | 2 | inverse_epoch | 0.098 | 0.411 | -0.313 | -0.458 | -0.136 |
| expytky | 2 | ridge_curve | 0.333 | 0.504 | -0.171 | -0.256 | -0.089 |
| expytky | 2 | gbr_curve | 0.393 | 0.504 | -0.111 | -0.234 | -0.005 |
| expytky | 2 | loss_sum | 0.189 | 0.504 | -0.315 | -0.445 | -0.189 |
| expytky | 2 | inverse_epoch | 0.432 | 0.504 | -0.072 | -0.185 | 0.039 |
| metrla | 3 | ridge_curve | 0.580 | 0.591 | -0.012 | -0.049 | 0.026 |
| metrla | 3 | gbr_curve | 0.564 | 0.591 | -0.028 | -0.095 | 0.039 |
| metrla | 3 | loss_sum | 0.389 | 0.591 | -0.203 | -0.331 | -0.073 |
| metrla | 3 | inverse_epoch | 0.505 | 0.591 | -0.086 | -0.199 | 0.021 |
| pems04 | 3 | ridge_curve | 0.445 | 0.428 | 0.017 | -0.068 | 0.095 |
| pems04 | 3 | gbr_curve | 0.364 | 0.428 | -0.064 | -0.134 | 0.008 |
| pems04 | 3 | loss_sum | 0.553 | 0.428 | 0.125 | 0.015 | 0.231 |
| pems04 | 3 | inverse_epoch | 0.256 | 0.428 | -0.172 | -0.311 | -0.038 |
| chengdu | 3 | ridge_curve | 0.562 | 0.583 | -0.021 | -0.058 | 0.016 |
| chengdu | 3 | gbr_curve | 0.578 | 0.583 | -0.005 | -0.074 | 0.055 |
| chengdu | 3 | loss_sum | 0.318 | 0.583 | -0.264 | -0.381 | -0.152 |
| chengdu | 3 | inverse_epoch | 0.476 | 0.583 | -0.107 | -0.226 | 0.018 |
| shenzhen | 3 | ridge_curve | 0.618 | 0.579 | 0.039 | -0.015 | 0.092 |
| shenzhen | 3 | gbr_curve | 0.631 | 0.579 | 0.051 | -0.035 | 0.132 |
| shenzhen | 3 | loss_sum | 0.580 | 0.579 | 0.001 | -0.135 | 0.123 |
| shenzhen | 3 | inverse_epoch | 0.286 | 0.579 | -0.293 | -0.438 | -0.132 |
| expytky | 3 | ridge_curve | 0.567 | 0.666 | -0.100 | -0.158 | -0.042 |
| expytky | 3 | gbr_curve | 0.566 | 0.666 | -0.101 | -0.189 | -0.027 |
| expytky | 3 | loss_sum | 0.129 | 0.666 | -0.537 | -0.673 | -0.395 |
| expytky | 3 | inverse_epoch | 0.604 | 0.666 | -0.063 | -0.138 | 0.010 |
| metrla | 5 | ridge_curve | 0.680 | 0.697 | -0.017 | -0.069 | 0.028 |
| metrla | 5 | gbr_curve | 0.656 | 0.697 | -0.041 | -0.117 | 0.036 |
| metrla | 5 | loss_sum | 0.346 | 0.697 | -0.351 | -0.484 | -0.218 |
| metrla | 5 | inverse_epoch | 0.666 | 0.697 | -0.031 | -0.114 | 0.042 |
| pems04 | 5 | ridge_curve | 0.735 | 0.676 | 0.059 | 0.001 | 0.118 |
| pems04 | 5 | gbr_curve | 0.645 | 0.676 | -0.031 | -0.089 | 0.027 |
| pems04 | 5 | loss_sum | 0.608 | 0.676 | -0.069 | -0.155 | 0.018 |
| pems04 | 5 | inverse_epoch | 0.475 | 0.676 | -0.201 | -0.304 | -0.097 |
| chengdu | 5 | ridge_curve | 0.777 | 0.727 | 0.050 | 0.014 | 0.095 |
| chengdu | 5 | gbr_curve | 0.717 | 0.727 | -0.010 | -0.068 | 0.038 |
| chengdu | 5 | loss_sum | 0.374 | 0.727 | -0.354 | -0.465 | -0.243 |
| chengdu | 5 | inverse_epoch | 0.690 | 0.727 | -0.037 | -0.141 | 0.072 |
| shenzhen | 5 | ridge_curve | 0.751 | 0.700 | 0.050 | 0.013 | 0.094 |
| shenzhen | 5 | gbr_curve | 0.728 | 0.700 | 0.027 | -0.022 | 0.081 |
| shenzhen | 5 | loss_sum | 0.592 | 0.700 | -0.108 | -0.229 | 0.010 |
| shenzhen | 5 | inverse_epoch | 0.525 | 0.700 | -0.175 | -0.298 | -0.065 |
| expytky | 5 | ridge_curve | 0.720 | 0.718 | 0.002 | -0.044 | 0.049 |
| expytky | 5 | gbr_curve | 0.654 | 0.718 | -0.064 | -0.116 | -0.017 |
| expytky | 5 | loss_sum | 0.075 | 0.718 | -0.643 | -0.806 | -0.452 |
| expytky | 5 | inverse_epoch | 0.709 | 0.718 | -0.009 | -0.064 | 0.051 |

### metrla: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.436 | 1.000 |
| gbr_curve_k1 | curve model, other cities | 5.663 | 38.926 | 3.000 | 2.964 | 9.019 | 1.000 | 9.082 | 2.000 |
| ridge_curve_k1 | curve model, other cities | 1.588 | 3.356 | 3.000 | 3.136 | 9.542 | 1.000 | 9.497 | 2.000 |
| early_val_k1 | brief training | 4.734 | 29.530 | 5.000 | 3.448 | 10.492 | 0.765 | 10.778 | 3.000 |
| loss_sum_k1 | train-loss sum | 1.379 | 2.013 | 8.000 | 4.161 | 12.660 | 0.960 | 12.682 | 5.000 |
| early_val_k2 | brief training | 0.000 | 0.000 | 1.000 | 4.498 | 13.687 | 1.000 | 14.022 | 1.000 |
| ridge_curve_k2 | curve model, other cities | 0.000 | 0.000 | 1.000 | 4.498 | 13.687 | 1.000 | 14.121 | 1.000 |
| gbr_curve_k2 | curve model, other cities | 1.588 | 3.356 | 3.000 | 5.088 | 15.481 | 1.000 | 15.363 | 2.000 |
| inverse_epoch_k2 | extrapolation, no fit | 8.240 | 57.047 | 5.000 | 5.285 | 16.082 | 1.000 | 15.905 | 3.000 |
| loss_sum_k2 | train-loss sum | 6.634 | 49.664 | 8.000 | 5.749 | 17.493 | 0.965 | 20.164 | 8.000 |
| gbr_curve_k3 | curve model, other cities | 0.000 | 0.000 | 1.000 | 6.489 | 19.745 | 1.000 | 20.230 | 1.000 |
| early_val_k3 | brief training | 0.000 | 0.000 | 1.000 | 6.489 | 19.745 | 1.000 | 20.258 | 1.000 |
| ridge_curve_k3 | curve model, other cities | 0.000 | 0.000 | 1.000 | 6.489 | 19.745 | 1.000 | 20.276 | 1.000 |
| inverse_epoch_k3 | extrapolation, no fit | 3.969 | 20.805 | 2.000 | 6.665 | 20.280 | 1.000 | 20.784 | 2.000 |
| loss_sum_k3 | train-loss sum | 6.634 | 49.664 | 8.000 | 7.646 | 23.265 | 0.805 | 25.101 | 8.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 10.486 | 31.907 | 1.000 | 32.241 | 1.000 |
| inverse_epoch_k5 | extrapolation, no fit | 0.000 | 0.000 | 1.000 | 10.486 | 31.907 | 1.000 | 32.321 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 0.000 | 0.000 | 1.000 | 10.486 | 31.907 | 1.000 | 32.470 | 1.000 |
| ridge_curve_k5 | curve model, other cities | 0.000 | 0.000 | 1.000 | 10.486 | 31.907 | 1.000 | 32.485 | 1.000 |
| loss_sum_k5 | train-loss sum | 6.634 | 49.664 |  |  |  | 0.680 | 37.655 | 8.000 |

### pems04: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 6.574 | 21.477 | 2.000 | 0.295 | 1.031 | 0.990 | 1.556 | 2.000 |
| ridge_curve_k1 | curve model, other cities | 7.691 | 29.530 | 5.000 | 2.569 | 8.965 | 0.880 | 10.784 | 5.000 |
| gbr_curve_k1 | curve model, other cities | 8.745 | 38.255 |  |  |  | 0.735 | 14.475 | 8.000 |
| loss_sum_k1 | train-loss sum | 6.593 | 22.148 |  |  |  | 0.720 | 16.668 | 10.000 |
| ridge_curve_k3 | curve model, other cities | 5.047 | 14.094 | 10.000 | 6.087 | 21.245 | 0.955 | 22.527 | 8.000 |
| ridge_curve_k5 | curve model, other cities | 0.000 | 0.000 | 1.000 | 7.543 | 26.327 | 1.000 | 26.724 | 1.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 7.543 | 26.327 | 0.970 | 26.736 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 5.047 | 14.094 | 5.000 | 8.074 | 28.182 | 0.995 | 27.986 | 3.000 |
| inverse_epoch_k5 | extrapolation, no fit | 6.356 | 20.134 |  |  |  | 0.640 | 33.092 | 10.000 |
| early_val_k1 | brief training | 15.677 | 85.906 |  |  |  | 0.000 |  |  |
| early_val_k2 | brief training | 12.225 | 63.087 |  |  |  | 0.000 |  |  |
| ridge_curve_k2 | curve model, other cities | 7.543 | 28.859 |  |  |  | 0.045 |  |  |
| gbr_curve_k2 | curve model, other cities | 7.543 | 28.859 |  |  |  | 0.125 |  |  |
| loss_sum_k2 | train-loss sum | 6.593 | 22.148 |  |  |  | 0.150 |  |  |
| inverse_epoch_k2 | extrapolation, no fit | 6.356 | 20.134 |  |  |  | 0.030 |  |  |
| early_val_k3 | brief training | 2.982 | 8.725 |  |  |  | 0.310 |  |  |
| gbr_curve_k3 | curve model, other cities | 5.047 | 14.094 |  |  |  | 0.375 |  |  |
| loss_sum_k3 | train-loss sum | 6.593 | 22.148 |  |  |  | 0.105 |  |  |
| inverse_epoch_k3 | extrapolation, no fit | 6.356 | 20.134 |  |  |  | 0.030 |  |  |
| loss_sum_k5 | train-loss sum | 2.057 | 5.369 |  |  |  | 0.265 |  |  |

### chengdu: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 2.287 | 6.040 | 3.000 | 0.357 | 1.695 | 0.755 | 2.489 | 3.000 |
| ridge_curve_k1 | curve model, other cities | 3.950 | 14.094 | 8.000 | 2.424 | 11.512 | 0.750 | 11.112 | 5.000 |
| gbr_curve_k2 | curve model, other cities | 3.950 | 14.094 | 2.000 | 2.794 | 13.266 | 0.755 | 13.869 | 2.000 |
| early_val_k1 | brief training | 6.321 | 33.557 |  |  |  | 0.655 | 14.950 | 10.000 |
| ridge_curve_k2 | curve model, other cities | 2.958 | 10.067 | 3.000 | 3.015 | 14.316 | 0.755 | 15.337 | 3.000 |
| early_val_k2 | brief training | 2.958 | 10.067 | 8.000 | 3.480 | 16.526 | 0.750 | 16.652 | 5.000 |
| gbr_curve_k1 | curve model, other cities | 2.287 | 6.040 |  |  |  | 0.675 | 16.980 | 10.000 |
| inverse_epoch_k2 | extrapolation, no fit | 9.014 | 69.128 | 8.000 | 3.598 | 17.087 | 0.710 | 17.623 | 5.000 |
| gbr_curve_k3 | curve model, other cities | 2.287 | 6.040 | 2.000 | 4.064 | 19.300 | 0.755 | 19.758 | 2.000 |
| early_val_k3 | brief training | 2.288 | 6.711 | 3.000 | 4.139 | 19.654 | 0.755 | 20.149 | 3.000 |
| ridge_curve_k3 | curve model, other cities | 2.958 | 10.067 | 3.000 | 4.139 | 19.654 | 0.755 | 20.190 | 3.000 |
| inverse_epoch_k3 | extrapolation, no fit | 7.547 | 51.678 | 5.000 | 4.353 | 20.672 | 0.755 | 22.089 | 5.000 |
| inverse_epoch_k5 | extrapolation, no fit | 0.429 | 0.671 | 1.000 | 6.445 | 30.605 | 0.995 | 31.060 | 1.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 6.452 | 30.637 | 0.890 | 31.080 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 2.287 | 6.040 | 5.000 | 6.946 | 32.982 | 0.755 | 32.560 | 3.000 |
| ridge_curve_k5 | curve model, other cities | 1.519 | 2.013 | 5.000 | 6.935 | 32.933 | 0.775 | 34.119 | 5.000 |
| loss_sum_k1 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.485 |  |  |
| loss_sum_k2 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.040 |  |  |
| loss_sum_k3 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.030 |  |  |
| loss_sum_k5 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.090 |  |  |

### shenzhen: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.926 | 1.000 |
| gbr_curve_k1 | curve model, other cities | 4.223 | 10.067 | 5.000 | 2.909 | 9.099 | 1.000 | 8.324 | 3.000 |
| ridge_curve_k1 | curve model, other cities | 3.148 | 4.698 | 5.000 | 3.122 | 9.764 | 1.000 | 10.974 | 5.000 |
| gbr_curve_k2 | curve model, other cities | 0.965 | 0.671 | 1.000 | 3.697 | 11.564 | 1.000 | 11.952 | 1.000 |
| ridge_curve_k2 | curve model, other cities | 4.223 | 10.067 | 3.000 | 4.096 | 12.813 | 0.920 | 13.700 | 3.000 |
| ridge_curve_k3 | curve model, other cities | 0.965 | 0.671 | 1.000 | 5.404 | 16.902 | 1.000 | 17.306 | 1.000 |
| gbr_curve_k3 | curve model, other cities | 3.148 | 4.698 | 2.000 | 5.678 | 17.761 | 1.000 | 18.242 | 2.000 |
| early_val_k2 | brief training | 4.673 | 14.094 |  |  |  | 0.705 | 20.500 | 10.000 |
| early_val_k3 | brief training | 4.673 | 14.094 | 8.000 | 6.791 | 21.242 | 0.970 | 21.124 | 5.000 |
| ridge_curve_k5 | curve model, other cities | 0.000 | 0.000 | 1.000 | 8.785 | 27.478 | 1.000 | 27.854 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 0.965 | 0.671 | 1.000 | 8.838 | 27.645 | 1.000 | 27.895 | 1.000 |
| early_val_k5 | brief training | 3.148 | 4.698 | 2.000 | 9.027 | 28.235 | 1.000 | 28.775 | 2.000 |
| early_val_k1 | brief training | 5.339 | 17.450 |  |  |  | 0.040 |  |  |
| loss_sum_k1 | train-loss sum | 3.751 | 6.040 |  |  |  | 0.075 |  |  |
| loss_sum_k2 | train-loss sum | 8.394 | 45.638 |  |  |  | 0.025 |  |  |
| inverse_epoch_k2 | extrapolation, no fit | 11.499 | 75.839 |  |  |  | 0.000 |  |  |
| loss_sum_k3 | train-loss sum | 8.394 | 45.638 |  |  |  | 0.005 |  |  |
| inverse_epoch_k3 | extrapolation, no fit | 14.814 | 91.946 |  |  |  | 0.010 |  |  |
| loss_sum_k5 | train-loss sum | 8.394 | 45.638 |  |  |  | 0.010 |  |  |
| inverse_epoch_k5 | extrapolation, no fit | 6.193 | 24.161 |  |  |  | 0.240 |  |  |

### expytky: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 1.455 | 2.013 | 5.000 | 1.276 | 2.257 | 1.000 | 1.754 | 3.000 |
| gbr_curve_k1 | curve model, other cities | 8.121 | 36.242 | 2.000 | 5.007 | 8.858 | 0.970 | 9.647 | 2.000 |
| ridge_curve_k1 | curve model, other cities | 8.121 | 36.242 | 8.000 | 7.051 | 12.473 | 0.970 | 12.166 | 5.000 |
| inverse_epoch_k2 | extrapolation, no fit | 0.635 | 0.671 | 1.000 | 8.298 | 14.679 | 0.735 | 15.007 | 1.000 |
| early_val_k2 | brief training | 1.455 | 2.013 | 2.000 | 8.602 | 15.217 | 0.940 | 15.515 | 2.000 |
| gbr_curve_k2 | curve model, other cities | 1.321 | 1.342 | 2.000 | 9.077 | 16.058 | 0.990 | 16.543 | 2.000 |
| early_val_k1 | brief training | 3.213 | 2.685 |  |  |  | 0.520 | 17.690 | 10.000 |
| inverse_epoch_k3 | extrapolation, no fit | 0.635 | 0.671 | 1.000 | 12.358 | 21.862 | 1.000 | 22.273 | 1.000 |
| early_val_k3 | brief training | 1.455 | 2.013 | 2.000 | 12.645 | 22.369 | 1.000 | 22.682 | 2.000 |
| ridge_curve_k2 | curve model, other cities | 4.487 | 5.369 |  |  |  | 0.555 | 23.657 | 10.000 |
| ridge_curve_k3 | curve model, other cities | 4.487 | 5.369 | 8.000 | 14.945 | 26.439 | 1.000 | 24.944 | 5.000 |
| gbr_curve_k3 | curve model, other cities | 4.649 | 6.711 | 5.000 | 13.900 | 24.590 | 0.995 | 26.005 | 5.000 |
| inverse_epoch_k5 | extrapolation, no fit | 0.635 | 0.671 | 1.000 | 20.480 | 36.230 | 1.000 | 36.536 | 1.000 |
| early_val_k5 | brief training | 1.455 | 2.013 | 2.000 | 20.733 | 36.678 | 1.000 | 37.006 | 1.000 |
| ridge_curve_k5 | curve model, other cities | 1.455 | 2.013 | 5.000 | 21.586 | 38.186 | 1.000 | 37.674 | 2.000 |
| gbr_curve_k5 | curve model, other cities | 4.692 | 7.383 |  |  |  | 0.595 | 43.358 | 10.000 |
| loss_sum_k1 | train-loss sum | 10.177 | 68.456 |  |  |  | 0.270 |  |  |
| loss_sum_k2 | train-loss sum | 10.177 | 68.456 |  |  |  | 0.000 |  |  |
| loss_sum_k3 | train-loss sum | 10.177 | 68.456 |  |  |  | 0.000 |  |  |
| loss_sum_k5 | train-loss sum | 10.177 | 68.456 |  |  |  | 0.000 |  |  |
