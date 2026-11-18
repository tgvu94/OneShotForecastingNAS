# evalscreen curve_rank: a model on the first k epochs, fit on the other cities

Inputs: ranks inside the city of the val MAE and the train loss at each of the first k epochs, their change from epoch 1 to k, the rank of the last two inside the head, and the head one-hot. Models: ridge, gradient boosting, fit on three cities, scored on the fourth. inverse_epoch = a least-squares fit of val(e) = a + b / e per run, read at epoch 20, with no fit across cities. loss_sum = the sum of the train loss over the first k epochs, z-scored inside each head. Every score costs k epochs of the whole list. Pass: inside the heads rho >= 0.6 at k <= 3 at three of four cities, and above early validation at the same k at every late city (all four, see base).

### Verdict per model

| model | cities_rho_ge_06_at_k_le_3 | cities_ge_06_and_above_early_val | cities_above_early_val_at_k3 | cities_ci_excludes_0_at_k3 | pass |
|---|---|---|---|---|---|
| gbr_curve | 1 | 1 | 2 | 0 | False |
| inverse_epoch | 1 | 0 | 0 | 0 | False |
| loss_sum | 0 | 0 | 2 | 1 | False |
| ridge_curve | 2 | 1 | 2 | 0 | False |

### Spearman inside the heads, by k

| model | k | chengdu | expytky | metrla | pems04 | pemsbay | shenzhen |
|---|---|---|---|---|---|---|---|
| gbr_curve | 1 | 0.201 | 0.233 | 0.396 | 0.434 | 0.162 | 0.391 |
| gbr_curve | 2 | 0.414 | 0.453 | 0.525 | 0.279 | 0.341 | 0.529 |
| gbr_curve | 3 | 0.574 | 0.600 | 0.606 | 0.368 | 0.480 | 0.584 |
| gbr_curve | 5 | 0.713 | 0.681 | 0.727 | 0.635 | 0.586 | 0.730 |
| inverse_epoch | 2 | 0.370 | 0.432 | 0.381 | 0.152 | 0.347 | 0.098 |
| inverse_epoch | 3 | 0.476 | 0.604 | 0.505 | 0.256 | 0.528 | 0.286 |
| inverse_epoch | 5 | 0.690 | 0.709 | 0.666 | 0.475 | 0.628 | 0.525 |
| loss_sum | 1 | 0.226 | 0.274 | 0.452 | 0.513 | 0.128 | 0.501 |
| loss_sum | 2 | 0.276 | 0.189 | 0.414 | 0.532 | 0.106 | 0.559 |
| loss_sum | 3 | 0.318 | 0.129 | 0.389 | 0.553 | 0.070 | 0.580 |
| loss_sum | 5 | 0.374 | 0.075 | 0.346 | 0.608 | -0.017 | 0.592 |
| ridge_curve | 1 | 0.237 | 0.294 | 0.482 | 0.472 | 0.182 | 0.481 |
| ridge_curve | 2 | 0.376 | 0.439 | 0.587 | 0.304 | 0.375 | 0.466 |
| ridge_curve | 3 | 0.580 | 0.639 | 0.602 | 0.428 | 0.526 | 0.599 |
| ridge_curve | 5 | 0.772 | 0.735 | 0.702 | 0.705 | 0.600 | 0.743 |

### Early validation inside the heads, by k (the baseline)

| k | chengdu | expytky | metrla | pems04 | pemsbay | shenzhen |
|---|---|---|---|---|---|---|
| 1.000 | 0.158 | 0.173 | 0.446 | 0.312 | 0.344 | 0.367 |
| 2.000 | 0.398 | 0.504 | 0.557 | 0.309 | 0.430 | 0.411 |
| 3.000 | 0.583 | 0.666 | 0.591 | 0.428 | 0.578 | 0.579 |
| 5.000 | 0.727 | 0.718 | 0.697 | 0.676 | 0.663 | 0.700 |

### Against early validation at the same k

CI from 1000 paired stratified resamples.

| city | k | model | rho_within_head | early_val_within | diff | diff_ci_lo | diff_ci_hi |
|---|---|---|---|---|---|---|---|
| metrla | 1 | ridge_curve | 0.482 | 0.446 | 0.036 | -0.060 | 0.143 |
| metrla | 1 | gbr_curve | 0.396 | 0.446 | -0.050 | -0.177 | 0.082 |
| metrla | 1 | loss_sum | 0.452 | 0.446 | 0.007 | -0.128 | 0.155 |
| pems04 | 1 | ridge_curve | 0.472 | 0.312 | 0.160 | 0.042 | 0.274 |
| pems04 | 1 | gbr_curve | 0.434 | 0.312 | 0.122 | -0.051 | 0.284 |
| pems04 | 1 | loss_sum | 0.513 | 0.312 | 0.201 | 0.035 | 0.352 |
| chengdu | 1 | ridge_curve | 0.237 | 0.158 | 0.078 | -0.044 | 0.203 |
| chengdu | 1 | gbr_curve | 0.201 | 0.158 | 0.043 | -0.114 | 0.205 |
| chengdu | 1 | loss_sum | 0.226 | 0.158 | 0.068 | -0.076 | 0.219 |
| shenzhen | 1 | ridge_curve | 0.481 | 0.367 | 0.114 | -0.019 | 0.248 |
| shenzhen | 1 | gbr_curve | 0.391 | 0.367 | 0.024 | -0.140 | 0.197 |
| shenzhen | 1 | loss_sum | 0.501 | 0.367 | 0.134 | -0.005 | 0.276 |
| expytky | 1 | ridge_curve | 0.294 | 0.173 | 0.121 | -0.003 | 0.248 |
| expytky | 1 | gbr_curve | 0.233 | 0.173 | 0.060 | -0.097 | 0.224 |
| expytky | 1 | loss_sum | 0.274 | 0.173 | 0.100 | -0.031 | 0.235 |
| pemsbay | 1 | ridge_curve | 0.182 | 0.344 | -0.162 | -0.290 | -0.034 |
| pemsbay | 1 | gbr_curve | 0.162 | 0.344 | -0.182 | -0.318 | -0.040 |
| pemsbay | 1 | loss_sum | 0.128 | 0.344 | -0.216 | -0.371 | -0.066 |
| metrla | 2 | ridge_curve | 0.587 | 0.557 | 0.030 | -0.012 | 0.075 |
| metrla | 2 | gbr_curve | 0.525 | 0.557 | -0.032 | -0.125 | 0.066 |
| metrla | 2 | loss_sum | 0.414 | 0.557 | -0.143 | -0.274 | 0.001 |
| metrla | 2 | inverse_epoch | 0.381 | 0.557 | -0.176 | -0.305 | -0.055 |
| pems04 | 2 | ridge_curve | 0.304 | 0.309 | -0.006 | -0.057 | 0.043 |
| pems04 | 2 | gbr_curve | 0.279 | 0.309 | -0.031 | -0.138 | 0.078 |
| pems04 | 2 | loss_sum | 0.532 | 0.309 | 0.223 | 0.103 | 0.340 |
| pems04 | 2 | inverse_epoch | 0.152 | 0.309 | -0.157 | -0.304 | -0.003 |
| chengdu | 2 | ridge_curve | 0.376 | 0.398 | -0.023 | -0.087 | 0.040 |
| chengdu | 2 | gbr_curve | 0.414 | 0.398 | 0.016 | -0.089 | 0.129 |
| chengdu | 2 | loss_sum | 0.276 | 0.398 | -0.122 | -0.250 | 0.002 |
| chengdu | 2 | inverse_epoch | 0.370 | 0.398 | -0.028 | -0.157 | 0.103 |
| shenzhen | 2 | ridge_curve | 0.466 | 0.411 | 0.054 | -0.025 | 0.125 |
| shenzhen | 2 | gbr_curve | 0.529 | 0.411 | 0.118 | 0.004 | 0.220 |
| shenzhen | 2 | loss_sum | 0.559 | 0.411 | 0.148 | 0.013 | 0.291 |
| shenzhen | 2 | inverse_epoch | 0.098 | 0.411 | -0.313 | -0.458 | -0.136 |
| expytky | 2 | ridge_curve | 0.439 | 0.504 | -0.065 | -0.127 | -0.010 |
| expytky | 2 | gbr_curve | 0.453 | 0.504 | -0.051 | -0.162 | 0.050 |
| expytky | 2 | loss_sum | 0.189 | 0.504 | -0.315 | -0.445 | -0.189 |
| expytky | 2 | inverse_epoch | 0.432 | 0.504 | -0.072 | -0.185 | 0.039 |
| pemsbay | 2 | ridge_curve | 0.375 | 0.430 | -0.054 | -0.114 | 0.006 |
| pemsbay | 2 | gbr_curve | 0.341 | 0.430 | -0.088 | -0.185 | 0.015 |
| pemsbay | 2 | loss_sum | 0.106 | 0.430 | -0.324 | -0.457 | -0.171 |
| pemsbay | 2 | inverse_epoch | 0.347 | 0.430 | -0.083 | -0.190 | 0.021 |
| metrla | 3 | ridge_curve | 0.602 | 0.591 | 0.010 | -0.033 | 0.047 |
| metrla | 3 | gbr_curve | 0.606 | 0.591 | 0.015 | -0.046 | 0.077 |
| metrla | 3 | loss_sum | 0.389 | 0.591 | -0.203 | -0.331 | -0.073 |
| metrla | 3 | inverse_epoch | 0.505 | 0.591 | -0.086 | -0.199 | 0.021 |
| pems04 | 3 | ridge_curve | 0.428 | 0.428 | -0.000 | -0.086 | 0.078 |
| pems04 | 3 | gbr_curve | 0.368 | 0.428 | -0.061 | -0.130 | 0.013 |
| pems04 | 3 | loss_sum | 0.553 | 0.428 | 0.125 | 0.015 | 0.231 |
| pems04 | 3 | inverse_epoch | 0.256 | 0.428 | -0.172 | -0.311 | -0.038 |
| chengdu | 3 | ridge_curve | 0.580 | 0.583 | -0.003 | -0.032 | 0.027 |
| chengdu | 3 | gbr_curve | 0.574 | 0.583 | -0.009 | -0.075 | 0.054 |
| chengdu | 3 | loss_sum | 0.318 | 0.583 | -0.264 | -0.381 | -0.152 |
| chengdu | 3 | inverse_epoch | 0.476 | 0.583 | -0.107 | -0.226 | 0.018 |
| shenzhen | 3 | ridge_curve | 0.599 | 0.579 | 0.020 | -0.023 | 0.065 |
| shenzhen | 3 | gbr_curve | 0.584 | 0.579 | 0.005 | -0.090 | 0.084 |
| shenzhen | 3 | loss_sum | 0.580 | 0.579 | 0.001 | -0.135 | 0.123 |
| shenzhen | 3 | inverse_epoch | 0.286 | 0.579 | -0.293 | -0.438 | -0.132 |
| expytky | 3 | ridge_curve | 0.639 | 0.666 | -0.028 | -0.071 | 0.015 |
| expytky | 3 | gbr_curve | 0.600 | 0.666 | -0.067 | -0.143 | 0.002 |
| expytky | 3 | loss_sum | 0.129 | 0.666 | -0.537 | -0.673 | -0.395 |
| expytky | 3 | inverse_epoch | 0.604 | 0.666 | -0.063 | -0.138 | 0.010 |
| pemsbay | 3 | ridge_curve | 0.526 | 0.578 | -0.053 | -0.101 | -0.000 |
| pemsbay | 3 | gbr_curve | 0.480 | 0.578 | -0.099 | -0.195 | -0.007 |
| pemsbay | 3 | loss_sum | 0.070 | 0.578 | -0.509 | -0.639 | -0.379 |
| pemsbay | 3 | inverse_epoch | 0.528 | 0.578 | -0.050 | -0.131 | 0.041 |
| metrla | 5 | ridge_curve | 0.702 | 0.697 | 0.005 | -0.044 | 0.054 |
| metrla | 5 | gbr_curve | 0.727 | 0.697 | 0.030 | -0.023 | 0.092 |
| metrla | 5 | loss_sum | 0.346 | 0.697 | -0.351 | -0.484 | -0.218 |
| metrla | 5 | inverse_epoch | 0.666 | 0.697 | -0.031 | -0.114 | 0.042 |
| pems04 | 5 | ridge_curve | 0.705 | 0.676 | 0.029 | -0.020 | 0.078 |
| pems04 | 5 | gbr_curve | 0.635 | 0.676 | -0.041 | -0.101 | 0.016 |
| pems04 | 5 | loss_sum | 0.608 | 0.676 | -0.069 | -0.155 | 0.018 |
| pems04 | 5 | inverse_epoch | 0.475 | 0.676 | -0.201 | -0.304 | -0.097 |
| chengdu | 5 | ridge_curve | 0.772 | 0.727 | 0.044 | 0.008 | 0.084 |
| chengdu | 5 | gbr_curve | 0.713 | 0.727 | -0.014 | -0.076 | 0.036 |
| chengdu | 5 | loss_sum | 0.374 | 0.727 | -0.354 | -0.465 | -0.243 |
| chengdu | 5 | inverse_epoch | 0.690 | 0.727 | -0.037 | -0.141 | 0.072 |
| shenzhen | 5 | ridge_curve | 0.743 | 0.700 | 0.043 | 0.007 | 0.081 |
| shenzhen | 5 | gbr_curve | 0.730 | 0.700 | 0.030 | -0.017 | 0.079 |
| shenzhen | 5 | loss_sum | 0.592 | 0.700 | -0.108 | -0.229 | 0.010 |
| shenzhen | 5 | inverse_epoch | 0.525 | 0.700 | -0.175 | -0.298 | -0.065 |
| expytky | 5 | ridge_curve | 0.735 | 0.718 | 0.017 | -0.019 | 0.059 |
| expytky | 5 | gbr_curve | 0.681 | 0.718 | -0.037 | -0.082 | 0.003 |
| expytky | 5 | loss_sum | 0.075 | 0.718 | -0.643 | -0.806 | -0.452 |
| expytky | 5 | inverse_epoch | 0.709 | 0.718 | -0.009 | -0.064 | 0.051 |
| pemsbay | 5 | ridge_curve | 0.600 | 0.663 | -0.063 | -0.121 | -0.007 |
| pemsbay | 5 | gbr_curve | 0.586 | 0.663 | -0.077 | -0.161 | 0.006 |
| pemsbay | 5 | loss_sum | -0.017 | 0.663 | -0.680 | -0.827 | -0.522 |
| pemsbay | 5 | inverse_epoch | 0.628 | 0.663 | -0.035 | -0.107 | 0.035 |

### metrla: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.424 | 1.000 |
| gbr_curve_k1 | curve model, other cities | 5.663 | 38.926 | 2.000 | 2.669 | 8.121 | 1.000 | 8.659 | 2.000 |
| ridge_curve_k1 | curve model, other cities | 1.379 | 2.013 | 3.000 | 3.136 | 9.542 | 1.000 | 9.497 | 2.000 |
| early_val_k1 | brief training | 4.734 | 29.530 | 5.000 | 3.448 | 10.492 | 0.765 | 10.778 | 3.000 |
| loss_sum_k1 | train-loss sum | 1.379 | 2.013 | 8.000 | 4.161 | 12.660 | 0.960 | 12.682 | 5.000 |
| early_val_k2 | brief training | 0.000 | 0.000 | 1.000 | 4.498 | 13.687 | 1.000 | 14.022 | 1.000 |
| ridge_curve_k2 | curve model, other cities | 0.000 | 0.000 | 1.000 | 4.498 | 13.687 | 1.000 | 14.121 | 1.000 |
| gbr_curve_k2 | curve model, other cities | 1.588 | 3.356 | 3.000 | 5.011 | 15.248 | 1.000 | 15.125 | 2.000 |
| inverse_epoch_k2 | extrapolation, no fit | 8.240 | 57.047 | 5.000 | 5.285 | 16.082 | 1.000 | 15.905 | 3.000 |
| loss_sum_k2 | train-loss sum | 6.634 | 49.664 | 8.000 | 5.749 | 17.493 | 0.965 | 20.164 | 8.000 |
| early_val_k3 | brief training | 0.000 | 0.000 | 1.000 | 6.489 | 19.745 | 1.000 | 20.258 | 1.000 |
| ridge_curve_k3 | curve model, other cities | 0.000 | 0.000 | 1.000 | 6.489 | 19.745 | 1.000 | 20.258 | 1.000 |
| gbr_curve_k3 | curve model, other cities | 1.283 | 1.342 | 2.000 | 6.640 | 20.206 | 1.000 | 20.398 | 1.000 |
| inverse_epoch_k3 | extrapolation, no fit | 3.969 | 20.805 | 2.000 | 6.665 | 20.280 | 1.000 | 20.784 | 2.000 |
| loss_sum_k3 | train-loss sum | 6.634 | 49.664 | 8.000 | 7.646 | 23.265 | 0.805 | 25.101 | 8.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 10.486 | 31.907 | 1.000 | 32.241 | 1.000 |
| inverse_epoch_k5 | extrapolation, no fit | 0.000 | 0.000 | 1.000 | 10.486 | 31.907 | 1.000 | 32.321 | 1.000 |
| ridge_curve_k5 | curve model, other cities | 0.000 | 0.000 | 1.000 | 10.486 | 31.907 | 1.000 | 32.470 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 1.588 | 3.356 | 2.000 | 10.720 | 32.620 | 1.000 | 32.719 | 1.000 |
| loss_sum_k5 | train-loss sum | 6.634 | 49.664 |  |  |  | 0.680 | 37.655 | 8.000 |

### pems04: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 6.574 | 21.477 | 2.000 | 0.295 | 1.031 | 0.980 | 1.556 | 2.000 |
| ridge_curve_k1 | curve model, other cities | 7.691 | 29.530 | 5.000 | 2.569 | 8.965 | 0.870 | 10.753 | 5.000 |
| gbr_curve_k1 | curve model, other cities | 8.745 | 38.255 | 8.000 | 3.184 | 11.113 | 0.775 | 11.018 | 5.000 |
| loss_sum_k1 | train-loss sum | 6.593 | 22.148 |  |  |  | 0.720 | 16.668 | 10.000 |
| gbr_curve_k3 | curve model, other cities | 5.047 | 14.094 | 8.000 | 5.754 | 20.085 | 0.805 | 20.470 | 5.000 |
| ridge_curve_k3 | curve model, other cities | 5.047 | 14.094 | 10.000 | 6.087 | 21.245 | 0.945 | 22.542 | 8.000 |
| ridge_curve_k5 | curve model, other cities | 0.000 | 0.000 | 1.000 | 7.543 | 26.327 | 1.000 | 26.718 | 1.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 7.543 | 26.327 | 0.970 | 26.736 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 5.047 | 14.094 | 5.000 | 8.074 | 28.182 | 0.995 | 28.021 | 3.000 |
| inverse_epoch_k5 | extrapolation, no fit | 6.356 | 20.134 |  |  |  | 0.640 | 33.092 | 10.000 |
| early_val_k1 | brief training | 15.677 | 85.906 |  |  |  | 0.000 |  |  |
| early_val_k2 | brief training | 12.225 | 63.087 |  |  |  | 0.000 |  |  |
| ridge_curve_k2 | curve model, other cities | 7.543 | 28.859 |  |  |  | 0.155 |  |  |
| gbr_curve_k2 | curve model, other cities | 5.917 | 17.450 |  |  |  | 0.140 |  |  |
| loss_sum_k2 | train-loss sum | 6.593 | 22.148 |  |  |  | 0.150 |  |  |
| inverse_epoch_k2 | extrapolation, no fit | 6.356 | 20.134 |  |  |  | 0.030 |  |  |
| early_val_k3 | brief training | 2.982 | 8.725 |  |  |  | 0.310 |  |  |
| loss_sum_k3 | train-loss sum | 6.593 | 22.148 |  |  |  | 0.105 |  |  |
| inverse_epoch_k3 | extrapolation, no fit | 6.356 | 20.134 |  |  |  | 0.030 |  |  |
| loss_sum_k5 | train-loss sum | 2.057 | 5.369 |  |  |  | 0.265 |  |  |

### chengdu: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 2.287 | 6.040 | 8.000 | 1.041 | 4.942 | 0.755 | 4.197 | 5.000 |
| ridge_curve_k1 | curve model, other cities | 3.950 | 14.094 | 8.000 | 2.424 | 11.512 | 0.750 | 10.970 | 5.000 |
| gbr_curve_k2 | curve model, other cities | 3.950 | 14.094 | 2.000 | 2.794 | 13.266 | 0.755 | 13.869 | 2.000 |
| ridge_curve_k2 | curve model, other cities | 3.875 | 13.423 | 2.000 | 2.895 | 13.746 | 0.755 | 14.525 | 2.000 |
| gbr_curve_k1 | curve model, other cities | 2.287 | 6.040 | 8.000 | 2.640 | 12.536 | 0.750 | 14.886 | 8.000 |
| early_val_k1 | brief training | 6.321 | 33.557 |  |  |  | 0.655 | 14.950 | 10.000 |
| early_val_k2 | brief training | 2.958 | 10.067 | 8.000 | 3.480 | 16.526 | 0.750 | 16.652 | 5.000 |
| inverse_epoch_k2 | extrapolation, no fit | 9.014 | 69.128 | 8.000 | 3.598 | 17.087 | 0.710 | 17.623 | 5.000 |
| ridge_curve_k3 | curve model, other cities | 0.000 | 0.000 | 1.000 | 3.932 | 18.671 | 0.755 | 19.019 | 1.000 |
| gbr_curve_k3 | curve model, other cities | 2.287 | 6.040 | 2.000 | 4.064 | 19.300 | 0.755 | 19.748 | 2.000 |
| early_val_k3 | brief training | 2.288 | 6.711 | 3.000 | 4.139 | 19.654 | 0.755 | 20.149 | 3.000 |
| inverse_epoch_k3 | extrapolation, no fit | 7.547 | 51.678 | 5.000 | 4.353 | 20.672 | 0.755 | 22.089 | 5.000 |
| inverse_epoch_k5 | extrapolation, no fit | 0.429 | 0.671 | 1.000 | 6.445 | 30.605 | 0.995 | 31.060 | 1.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 6.452 | 30.637 | 0.890 | 31.080 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 2.287 | 6.040 | 5.000 | 6.946 | 32.982 | 0.755 | 32.560 | 3.000 |
| ridge_curve_k5 | curve model, other cities | 1.519 | 2.013 | 5.000 | 6.935 | 32.933 | 0.775 | 33.054 | 3.000 |
| loss_sum_k1 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.485 |  |  |
| loss_sum_k2 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.040 |  |  |
| loss_sum_k3 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.030 |  |  |
| loss_sum_k5 | train-loss sum | 9.209 | 70.470 |  |  |  | 0.090 |  |  |

### shenzhen: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.940 | 1.000 |
| gbr_curve_k1 | curve model, other cities | 4.223 | 10.067 | 5.000 | 2.554 | 7.990 | 1.000 | 7.595 | 3.000 |
| ridge_curve_k1 | curve model, other cities | 3.148 | 4.698 | 8.000 | 3.551 | 11.107 | 0.965 | 11.289 | 5.000 |
| gbr_curve_k2 | curve model, other cities | 0.965 | 0.671 | 1.000 | 3.697 | 11.564 | 1.000 | 11.952 | 1.000 |
| ridge_curve_k2 | curve model, other cities | 4.673 | 14.094 | 8.000 | 5.242 | 16.396 | 0.905 | 16.377 | 5.000 |
| gbr_curve_k3 | curve model, other cities | 0.965 | 0.671 | 1.000 | 5.404 | 16.902 | 1.000 | 17.223 | 1.000 |
| ridge_curve_k3 | curve model, other cities | 0.965 | 0.671 | 1.000 | 5.404 | 16.902 | 0.970 | 17.305 | 1.000 |
| early_val_k2 | brief training | 4.673 | 14.094 |  |  |  | 0.705 | 20.500 | 10.000 |
| early_val_k3 | brief training | 4.673 | 14.094 | 8.000 | 6.791 | 21.242 | 0.970 | 21.124 | 5.000 |
| ridge_curve_k5 | curve model, other cities | 0.000 | 0.000 | 1.000 | 8.785 | 27.478 | 1.000 | 27.854 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 0.965 | 0.671 | 1.000 | 8.838 | 27.645 | 1.000 | 27.884 | 1.000 |
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
| transfer_pooled | transfer | 1.455 | 2.013 | 3.000 | 0.587 | 1.039 | 1.000 | 0.925 | 2.000 |
| gbr_curve_k1 | curve model, other cities | 8.121 | 36.242 | 2.000 | 5.007 | 8.858 | 0.975 | 9.637 | 2.000 |
| ridge_curve_k1 | curve model, other cities | 8.121 | 36.242 | 8.000 | 7.051 | 12.473 | 0.970 | 12.172 | 5.000 |
| inverse_epoch_k2 | extrapolation, no fit | 0.635 | 0.671 | 1.000 | 8.298 | 14.679 | 0.735 | 15.007 | 1.000 |
| gbr_curve_k2 | curve model, other cities | 1.455 | 2.013 | 2.000 | 8.653 | 15.308 | 1.000 | 15.498 | 1.000 |
| early_val_k2 | brief training | 1.455 | 2.013 | 2.000 | 8.602 | 15.217 | 0.940 | 15.515 | 2.000 |
| early_val_k1 | brief training | 3.213 | 2.685 |  |  |  | 0.520 | 17.690 | 10.000 |
| ridge_curve_k2 | curve model, other cities | 1.455 | 2.013 |  |  |  | 0.915 | 21.351 | 8.000 |
| inverse_epoch_k3 | extrapolation, no fit | 0.635 | 0.671 | 1.000 | 12.358 | 21.862 | 1.000 | 22.273 | 1.000 |
| ridge_curve_k3 | curve model, other cities | 1.455 | 2.013 | 2.000 | 12.694 | 22.457 | 1.000 | 22.585 | 1.000 |
| early_val_k3 | brief training | 1.455 | 2.013 | 2.000 | 12.645 | 22.369 | 1.000 | 22.682 | 2.000 |
| gbr_curve_k3 | curve model, other cities | 7.428 | 27.517 | 5.000 | 14.404 | 25.482 | 1.000 | 24.979 | 3.000 |
| inverse_epoch_k5 | extrapolation, no fit | 0.635 | 0.671 | 1.000 | 20.480 | 36.230 | 1.000 | 36.536 | 1.000 |
| ridge_curve_k5 | curve model, other cities | 1.455 | 2.013 | 2.000 | 20.779 | 36.759 | 1.000 | 36.931 | 1.000 |
| early_val_k5 | brief training | 1.455 | 2.013 | 2.000 | 20.733 | 36.678 | 1.000 | 37.006 | 1.000 |
| gbr_curve_k5 | curve model, other cities | 3.213 | 2.685 | 8.000 | 22.174 | 39.228 | 1.000 | 38.677 | 5.000 |
| loss_sum_k1 | train-loss sum | 10.177 | 68.456 |  |  |  | 0.270 |  |  |
| loss_sum_k2 | train-loss sum | 10.177 | 68.456 |  |  |  | 0.000 |  |  |
| loss_sum_k3 | train-loss sum | 10.177 | 68.456 |  |  |  | 0.000 |  |  |
| loss_sum_k5 | train-loss sum | 10.177 | 68.456 |  |  |  | 0.000 |  |  |

### pemsbay: cost to one sigma

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pooled | transfer | 0.000 | 0.000 | 1.000 | 0.512 | 0.706 | 0.980 | 1.065 | 1.000 |
| ridge_curve_k1 | curve model, other cities | 3.421 | 12.081 | 5.000 | 6.964 | 9.606 | 0.960 | 10.531 | 5.000 |
| early_val_k1 | brief training | 5.348 | 29.530 | 5.000 | 6.945 | 9.581 | 0.915 | 11.300 | 5.000 |
| gbr_curve_k1 | curve model, other cities | 4.619 | 21.477 | 8.000 | 8.113 | 11.192 | 0.980 | 12.875 | 8.000 |
| early_val_k2 | brief training | 4.766 | 22.819 | 2.000 | 9.376 | 12.934 | 0.995 | 13.565 | 2.000 |
| ridge_curve_k2 | curve model, other cities | 4.619 | 21.477 | 3.000 | 9.974 | 13.759 | 0.990 | 14.471 | 3.000 |
| inverse_epoch_k2 | extrapolation, no fit | 2.259 | 4.698 | 8.000 | 12.532 | 17.287 | 0.990 | 17.009 | 5.000 |
| gbr_curve_k2 | curve model, other cities | 4.619 | 21.477 | 10.000 | 12.777 | 17.625 | 1.000 | 17.850 | 8.000 |
| early_val_k3 | brief training | 0.000 | 0.000 | 1.000 | 13.001 | 17.934 | 1.000 | 18.380 | 1.000 |
| inverse_epoch_k3 | extrapolation, no fit | 4.619 | 21.477 | 3.000 | 13.674 | 18.863 | 0.995 | 19.078 | 2.000 |
| ridge_curve_k3 | curve model, other cities | 4.619 | 21.477 | 2.000 | 13.559 | 18.705 | 0.995 | 19.179 | 2.000 |
| gbr_curve_k3 | curve model, other cities | 1.722 | 2.685 | 5.000 | 14.549 | 20.070 | 1.000 | 20.635 | 3.000 |
| ridge_curve_k5 | curve model, other cities | 0.000 | 0.000 | 1.000 | 21.273 | 29.345 | 1.000 | 29.810 | 1.000 |
| early_val_k5 | brief training | 1.722 | 2.685 | 2.000 | 21.533 | 29.705 | 1.000 | 29.917 | 2.000 |
| inverse_epoch_k5 | extrapolation, no fit | 4.619 | 21.477 | 3.000 | 21.852 | 30.144 | 0.990 | 30.275 | 2.000 |
| gbr_curve_k5 | curve model, other cities | 2.734 | 8.054 | 8.000 | 23.876 | 32.936 | 0.995 | 32.477 | 5.000 |
| loss_sum_k1 | train-loss sum | 14.159 | 74.497 |  |  |  | 0.180 |  |  |
| loss_sum_k2 | train-loss sum | 19.325 | 95.302 |  |  |  | 0.005 |  |  |
| loss_sum_k3 | train-loss sum | 19.325 | 95.302 |  |  |  | 0.000 |  |  |
| loss_sum_k5 | train-loss sum | 7.239 | 48.322 |  |  |  | 0.000 |  |  |
