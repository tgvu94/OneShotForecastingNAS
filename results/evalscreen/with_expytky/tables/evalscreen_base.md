# evalscreen base: the stored evaluators on the common measure

Target = test_mae, seed 0, zero-masked pipeline, shared list. b in [1, 2, 3, 5, 8, 10]. b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line. random is an expectation over draws on the full list.

- metrla: N = 150, sigma_seed = 0.0014 over 50 architectures, whole list 32.9 GPU-hours (reference unit; cost_ratio 1.00, nibi)
- pems04: N = 150, sigma_seed = 0.0004 over 50 architectures, whole list 28.7 GPU-hours (reference unit; cost_ratio 1.00, nibi)
- chengdu: N = 150, sigma_seed = 0.0013 over 50 architectures, whole list 21.1 GPU-hours (reference unit; cost_ratio 1.01, rorqual)
- shenzhen: N = 150, sigma_seed = 0.0012 over 50 architectures, whole list 32.0 GPU-hours (reference unit; cost_ratio 0.94, fir)
- expytky: N = 150, sigma_seed = 0.0019 over 50 architectures, whole list 56.5 GPU-hours (reference unit; cost_ratio 1.01, rorqual)

### metrla: cost to one sigma, cheapest robust form first

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_from_expytky | transfer | 0.826 | 0.671 | 1.000 | 0.231 | 0.704 | 1.000 | 1.067 | 1.000 |
| transfer_pooled | transfer | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.436 | 1.000 |
| transfer_from_shenzhen | transfer | 1.283 | 1.342 | 2.000 | 0.498 | 1.515 | 1.000 | 1.482 | 1.000 |
| transfer_from_chengdu | transfer | 1.283 | 1.342 | 5.000 | 1.043 | 3.175 | 0.990 | 2.786 | 3.000 |
| loco_gbr_arch_proxies | predictor, other cities | 1.379 | 2.013 | 3.000 | 1.077 | 3.276 | 1.000 | 3.255 | 2.000 |
| loco_ridge_arch | predictor, other cities | 2.555 | 8.054 | 2.000 | 0.729 | 2.219 | 1.000 | 3.271 | 2.000 |
| transfer_from_pems04 | transfer | 2.555 | 8.054 | 2.000 | 0.729 | 2.219 | 1.000 | 3.326 | 2.000 |
| loco_gbr_proxies | predictor, other cities | 2.555 | 8.054 | 3.000 | 0.919 | 2.796 | 1.000 | 3.382 | 2.000 |
| loco_gbr_arch | predictor, other cities | 1.379 | 2.013 | 5.000 | 1.708 | 5.198 | 1.000 | 4.413 | 3.000 |
| zico_sizectrl_half_then_k1 | proxy filter | 4.734 | 29.530 | 5.000 | 2.458 | 7.478 | 0.770 | 7.783 | 3.000 |
| zico_half_then_k1 | proxy filter | 4.734 | 29.530 | 5.000 | 2.617 | 7.963 | 0.825 | 7.845 | 3.000 |
| early_val_k1 | brief training | 4.734 | 29.530 | 5.000 | 3.448 | 10.492 | 0.765 | 10.778 | 3.000 |
| zico_sizectrl_half_then_k3 | proxy filter | 0.000 | 0.000 | 1.000 | 3.684 | 11.211 | 1.000 | 11.809 | 1.000 |
| zico_half_then_k3 | proxy filter | 0.000 | 0.000 | 1.000 | 3.770 | 11.472 | 1.000 | 11.977 | 1.000 |
| early_val_k2 | brief training | 0.000 | 0.000 | 1.000 | 4.498 | 13.687 | 1.000 | 14.022 | 1.000 |
| sh_r1_eta3 | successive halving | 0.000 | 0.000 | 1.000 | 5.777 | 17.579 | 1.000 | 17.418 | 1.000 |
| zico_sizectrl_half_then_k5 | proxy filter | 0.000 | 0.000 | 1.000 | 5.867 | 17.851 | 1.000 | 18.341 | 1.000 |
| zico_half_then_k5 | proxy filter | 0.000 | 0.000 | 1.000 | 6.011 | 18.291 | 1.000 | 18.583 | 1.000 |
| sh_r1_eta2 | successive halving | 0.000 | 0.000 | 1.000 | 6.446 | 19.615 | 1.000 | 19.812 | 1.000 |
| early_val_k3 | brief training | 0.000 | 0.000 | 1.000 | 6.489 | 19.745 | 1.000 | 20.258 | 1.000 |
| early_val_k4 | brief training | 0.000 | 0.000 | 1.000 | 8.487 | 25.826 | 1.000 | 26.182 | 1.000 |
| sh_r2_eta3 | successive halving | 0.000 | 0.000 | 1.000 | 9.848 | 29.965 | 1.000 | 30.010 | 1.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 10.486 | 31.907 | 1.000 | 32.241 | 1.000 |
| sh_r2_eta2 | successive halving | 0.000 | 0.000 | 1.000 | 10.676 | 32.487 | 1.000 | 32.582 | 1.000 |
| early_val_k6 | brief training | 1.616 | 4.027 | 2.000 | 12.628 | 38.426 | 1.000 | 38.583 | 1.000 |
| sh_r3_eta3 | successive halving | 0.000 | 0.000 | 1.000 | 12.702 | 38.650 | 1.000 | 38.717 | 1.000 |
| sh_r3_eta2 | successive halving | 0.000 | 0.000 | 1.000 | 14.053 | 42.762 | 1.000 | 43.041 | 1.000 |
| early_val_k8 | brief training | 0.000 | 0.000 | 1.000 | 16.440 | 50.025 | 1.000 | 50.237 | 1.000 |
| early_val_k10 | brief training | 0.000 | 0.000 | 1.000 | 20.171 | 61.377 | 1.000 | 61.538 | 1.000 |
| full_training | ceiling | 0.000 | 0.000 | 1.000 | 32.863 | 100.000 | 1.000 | 100.000 | 1.000 |
| random | floor | 8.965 |  |  |  |  | 0.265 |  |  |
| params | floor | 4.004 | 21.477 |  |  |  | 0.060 |  |  |
| flops | floor | 6.893 | 51.007 |  |  |  | 0.000 |  |  |
| zico | zero-cost proxy | 4.420 | 26.174 |  |  |  | 0.320 |  |  |
| zico_sizectrl | zero-cost proxy | 14.490 | 79.195 |  |  |  | 0.220 |  |  |
| swap | zero-cost proxy | 1.640 | 4.698 |  |  |  | 0.265 |  |  |
| swap_reg | zero-cost proxy | 17.447 | 94.631 |  |  |  | 0.215 |  |  |
| nwot | zero-cost proxy | 1.640 | 4.698 |  |  |  | 0.265 |  |  |
| synflow_all | zero-cost proxy | 5.816 | 39.597 |  |  |  | 0.000 |  |  |
| snip_all | zero-cost proxy | 14.565 | 79.866 |  |  |  | 0.000 |  |  |
| grasp_all | zero-cost proxy | 7.048 | 52.349 |  |  |  | 0.000 |  |  |
| grad_norm_all | zero-cost proxy | 14.565 | 79.866 |  |  |  | 0.000 |  |  |
| fisher | zero-cost proxy | 20.936 | 98.658 |  |  |  | 0.000 |  |  |
| jacov | zero-cost proxy | 2.891 | 10.067 |  |  |  | 0.070 |  |  |
| zen | zero-cost proxy | 4.004 | 21.477 |  |  |  | 0.260 |  |  |
| l2_norm_all | zero-cost proxy | 4.420 | 26.174 |  |  |  | 0.285 |  |  |
| plain_all | zero-cost proxy | 20.936 | 98.658 |  |  |  | 0.000 |  |  |
| zico_t | zero-cost proxy | 5.816 | 39.597 |  |  |  | 0.425 |  |  |
| zico_s | zero-cost proxy | 10.647 | 61.745 |  |  |  | 0.215 |  |  |
| glass | zero-cost proxy | 4.420 | 26.174 |  |  |  | 0.325 |  |  |
| glass_t | zero-cost proxy | 5.816 | 39.597 |  |  |  | 0.345 |  |  |
| glass_s | zero-cost proxy | 10.647 | 61.745 |  |  |  | 0.215 |  |  |
| nwot_per_layer | zero-cost proxy | 11.477 | 63.087 |  |  |  | 0.000 |  |  |

### metrla: head control, Spearman with -test_mae

rho_within_head = n-weighted mean of the three heads, with a stratified bootstrap CI; mae_head_* = the pick among the MAE-head architectures alone.

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| full_training | ceiling | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| early_val_k10 | brief training | 0.961 | 0.844 | 0.761 | 0.890 | 0.889 | 0.820 | 0.834 | 0.000 | 0.000 |
| early_val_k8 | brief training | 0.951 | 0.805 | 0.710 | 0.859 | 0.866 | 0.853 | 0.713 | 0.000 | 0.000 |
| early_val_k6 | brief training | 0.924 | 0.727 | 0.617 | 0.803 | 0.810 | 0.753 | 0.640 | 1.616 | 15.385 |
| early_val_k5 | brief training | 0.926 | 0.697 | 0.573 | 0.781 | 0.762 | 0.746 | 0.601 | 0.000 | 0.000 |
| early_val_k4 | brief training | 0.925 | 0.680 | 0.561 | 0.772 | 0.777 | 0.717 | 0.572 | 0.000 | 0.000 |
| transfer_from_expytky | transfer | 0.756 | 0.626 | 0.517 | 0.705 | 0.597 | 0.595 | 0.676 | 0.826 | 2.564 |
| transfer_pooled | transfer | 0.745 | 0.620 | 0.494 | 0.713 | 0.667 | 0.625 | 0.581 | 0.000 | 0.000 |
| early_val_k3 | brief training | 0.878 | 0.591 | 0.449 | 0.701 | 0.790 | 0.556 | 0.483 | 0.000 | 0.000 |
| transfer_from_shenzhen | transfer | 0.716 | 0.576 | 0.438 | 0.668 | 0.629 | 0.606 | 0.507 | 1.283 | 5.128 |
| early_val_k2 | brief training | 0.843 | 0.557 | 0.406 | 0.682 | 0.641 | 0.594 | 0.459 | 0.000 | 0.000 |
| loco_gbr_arch | predictor, other cities | 0.707 | 0.553 | 0.424 | 0.668 | 0.571 | 0.557 | 0.535 | 1.379 | 7.692 |
| loco_ridge_arch | predictor, other cities | 0.758 | 0.553 | 0.421 | 0.653 | 0.656 | 0.415 | 0.615 | 2.555 | 28.205 |
| loco_gbr_arch_proxies | predictor, other cities | 0.700 | 0.535 | 0.392 | 0.662 | 0.587 | 0.509 | 0.523 | 1.379 | 7.692 |
| loco_gbr_proxies | predictor, other cities | 0.695 | 0.523 | 0.379 | 0.630 | 0.569 | 0.476 | 0.535 | 2.555 | 28.205 |
| transfer_from_pems04 | transfer | 0.576 | 0.501 | 0.368 | 0.643 | 0.548 | 0.594 | 0.372 | 2.555 | 28.205 |
| early_val_k1 | brief training | 0.581 | 0.446 | 0.303 | 0.585 | 0.638 | 0.500 | 0.252 | 4.734 | 71.795 |
| transfer_from_chengdu | transfer | 0.530 | 0.435 | 0.285 | 0.550 | 0.537 | 0.420 | 0.377 | 1.283 | 5.128 |
| glass_t | zero-cost proxy | 0.194 | 0.406 | 0.249 | 0.520 | 0.433 | 0.251 | 0.542 | 2.555 | 28.205 |
| zico_t | zero-cost proxy | 0.239 | 0.404 | 0.247 | 0.519 | 0.433 | 0.242 | 0.544 | 2.555 | 28.205 |
| zico | zero-cost proxy | 0.224 | 0.395 | 0.232 | 0.524 | 0.404 | 0.249 | 0.534 | 2.555 | 28.205 |
| glass | zero-cost proxy | 0.182 | 0.390 | 0.228 | 0.520 | 0.405 | 0.236 | 0.535 | 2.555 | 28.205 |
| zico_sizectrl | zero-cost proxy | 0.258 | 0.376 | 0.192 | 0.521 | 0.498 | 0.274 | 0.389 | 2.555 | 28.205 |
| l2_norm_all | zero-cost proxy | 0.136 | 0.295 | 0.140 | 0.448 | 0.309 | 0.231 | 0.350 | 1.640 | 17.949 |
| params | floor | 0.035 | 0.161 | -0.014 | 0.333 | 0.061 | 0.031 | 0.365 | 9.732 | 100.000 |
| zen | zero-cost proxy | -0.011 | 0.080 | -0.075 | 0.249 | -0.106 | -0.018 | 0.313 | 1.640 | 17.949 |
| jacov | zero-cost proxy | 0.104 | 0.026 | -0.134 | 0.175 | -0.028 | -0.007 | 0.099 | 2.891 | 35.897 |
| grasp_all | zero-cost proxy | 0.484 | 0.024 | -0.135 | 0.180 | 0.170 | -0.006 | -0.053 | 2.665 | 33.333 |
| plain_all | zero-cost proxy | -0.424 | 0.008 | -0.169 | 0.149 | 0.198 | -0.109 | -0.014 | 3.183 | 46.154 |
| swap | zero-cost proxy | -0.088 | -0.020 | -0.186 | 0.150 | -0.116 | -0.058 | 0.086 | 1.640 | 17.949 |
| snip_all | zero-cost proxy | -0.429 | -0.023 | -0.168 | 0.140 | -0.206 | -0.078 | 0.165 | 3.451 | 51.282 |
| swap_reg | zero-cost proxy | 0.036 | -0.036 | -0.201 | 0.124 | 0.092 | -0.089 | -0.074 | 6.893 | 89.744 |
| grad_norm_all | zero-cost proxy | -0.475 | -0.047 | -0.203 | 0.121 | -0.212 | -0.093 | 0.118 | 3.451 | 51.282 |
| nwot | zero-cost proxy | -0.090 | -0.056 | -0.209 | 0.110 | -0.110 | -0.077 | 0.004 | 1.640 | 17.949 |
| fisher | zero-cost proxy | -0.542 | -0.074 | -0.225 | 0.090 | -0.131 | -0.118 | 0.013 | 3.183 | 46.154 |
| zico_s | zero-cost proxy | -0.048 | -0.107 | -0.285 | 0.055 | -0.088 | -0.078 | -0.150 | 6.893 | 89.744 |
| glass_s | zero-cost proxy | -0.059 | -0.108 | -0.286 | 0.053 | -0.088 | -0.082 | -0.150 | 6.893 | 89.744 |
| synflow_all | zero-cost proxy | -0.208 | -0.124 | -0.298 | 0.047 | 0.020 | -0.238 | -0.113 | 6.893 | 89.744 |
| flops | floor | -0.120 | -0.130 | -0.298 | 0.037 | -0.204 | -0.144 | -0.062 | 6.893 | 89.744 |
| nwot_per_layer | zero-cost proxy | -0.188 | -0.278 | -0.432 | -0.113 | -0.310 | -0.008 | -0.524 | 3.896 | 61.538 |

### pems04: cost to one sigma, cheapest robust form first

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_from_metrla | transfer | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.965 | 0.864 | 1.000 |
| loco_gbr_arch | predictor, other cities | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.995 | 0.864 | 1.000 |
| loco_gbr_proxies | predictor, other cities | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.980 | 0.864 | 1.000 |
| transfer_from_shenzhen | transfer | 2.635 | 6.711 | 2.000 | 0.293 | 1.023 | 1.000 | 1.540 | 2.000 |
| loco_ridge_arch | predictor, other cities | 6.574 | 21.477 | 2.000 | 0.295 | 1.031 | 0.990 | 1.548 | 2.000 |
| transfer_pooled | transfer | 6.574 | 21.477 | 2.000 | 0.295 | 1.031 | 0.990 | 1.556 | 2.000 |
| loco_gbr_arch_proxies | predictor, other cities | 6.574 | 21.477 | 2.000 | 0.295 | 1.031 | 0.990 | 1.556 | 2.000 |
| transfer_from_expytky | transfer | 6.574 | 21.477 | 5.000 | 0.898 | 3.133 | 0.975 | 2.834 | 3.000 |
| zico_sizectrl | zero-cost proxy | 2.526 | 6.040 | 8.000 | 1.825 | 6.369 | 0.970 | 6.444 | 5.000 |
| glass_t | zero-cost proxy | 2.526 | 6.040 | 8.000 | 1.971 | 6.878 | 0.965 | 6.978 | 5.000 |
| glass | zero-cost proxy | 1.157 | 2.013 | 8.000 | 1.971 | 6.878 | 0.960 | 7.086 | 5.000 |
| transfer_from_chengdu | transfer | 2.635 | 6.711 | 10.000 | 1.650 | 5.758 | 0.830 | 7.395 | 8.000 |
| zico_t | zero-cost proxy | 2.526 | 6.040 | 10.000 | 2.437 | 8.505 | 0.960 | 9.822 | 8.000 |
| zico | zero-cost proxy | 1.157 | 2.013 | 10.000 | 2.563 | 8.946 | 0.960 | 10.009 | 8.000 |
| swap_reg | zero-cost proxy | 22.062 | 98.658 | 8.000 | 2.057 | 7.181 | 0.680 | 10.382 | 8.000 |
| l2_norm_all | zero-cost proxy | 1.157 | 2.013 |  |  |  | 0.625 | 13.365 | 10.000 |
| zico_sizectrl_half_then_k5 | proxy filter | 0.000 | 0.000 | 1.000 | 4.085 | 14.258 | 0.990 | 14.809 | 1.000 |
| sh_r1_eta3 | successive halving | 0.846 | 0.671 | 1.000 | 4.266 | 14.891 | 0.690 | 14.928 | 1.000 |
| zico_half_then_k5 | proxy filter | 0.000 | 0.000 | 1.000 | 4.156 | 14.507 | 0.990 | 14.981 | 1.000 |
| zico_sizectrl_half_then_k3 | proxy filter | 2.982 | 8.725 |  |  |  | 0.895 | 16.248 | 8.000 |
| zico_half_then_k3 | proxy filter | 2.982 | 8.725 |  |  |  | 0.885 | 16.642 | 8.000 |
| early_val_k4 | brief training | 5.047 | 14.094 | 2.000 | 6.249 | 21.810 | 0.990 | 22.388 | 2.000 |
| sh_r2_eta3 | successive halving | 0.876 | 1.342 | 1.000 | 7.343 | 25.629 | 0.700 | 25.870 | 1.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 7.543 | 26.327 | 0.970 | 26.736 | 1.000 |
| sh_r2_eta2 | successive halving | 0.000 | 0.000 | 1.000 | 8.099 | 28.268 | 0.995 | 28.477 | 1.000 |
| early_val_k6 | brief training | 2.982 | 8.725 | 2.000 | 9.124 | 31.847 | 0.995 | 32.423 | 2.000 |
| sh_r3_eta3 | successive halving | 0.000 | 0.000 | 1.000 | 9.486 | 33.108 | 0.995 | 33.314 | 1.000 |
| sh_r3_eta2 | successive halving | 0.000 | 0.000 | 1.000 | 10.676 | 37.263 | 1.000 | 37.470 | 1.000 |
| early_val_k8 | brief training | 0.000 | 0.000 | 1.000 | 11.754 | 41.027 | 1.000 | 41.315 | 1.000 |
| early_val_k10 | brief training | 0.876 | 1.342 | 1.000 | 14.558 | 50.811 | 1.000 | 51.036 | 1.000 |
| full_training | ceiling | 0.000 | 0.000 | 1.000 | 28.650 | 100.000 | 1.000 | 100.000 | 1.000 |
| random | floor | 10.545 |  |  |  |  | 0.285 |  |  |
| params | floor | 2.945 | 8.054 |  |  |  | 0.230 |  |  |
| flops | floor | 11.682 | 59.732 |  |  |  | 0.205 |  |  |
| swap | zero-cost proxy | 6.448 | 20.805 |  |  |  | 0.230 |  |  |
| nwot | zero-cost proxy | 9.305 | 42.282 |  |  |  | 0.110 |  |  |
| synflow_all | zero-cost proxy | 2.526 | 6.040 |  |  |  | 0.000 |  |  |
| snip_all | zero-cost proxy | 14.582 | 81.879 |  |  |  | 0.000 |  |  |
| grasp_all | zero-cost proxy | 17.192 | 91.275 |  |  |  | 0.000 |  |  |
| grad_norm_all | zero-cost proxy | 14.582 | 81.879 |  |  |  | 0.000 |  |  |
| fisher | zero-cost proxy | 11.928 | 61.745 |  |  |  | 0.000 |  |  |
| jacov | zero-cost proxy | 18.990 | 95.302 |  |  |  | 0.000 |  |  |
| zen | zero-cost proxy | 2.945 | 8.054 |  |  |  | 0.230 |  |  |
| plain_all | zero-cost proxy | 11.928 | 61.745 |  |  |  | 0.000 |  |  |
| zico_s | zero-cost proxy | 11.115 | 55.705 |  |  |  | 0.020 |  |  |
| glass_s | zero-cost proxy | 11.115 | 55.705 |  |  |  | 0.020 |  |  |
| nwot_per_layer | zero-cost proxy | 18.666 | 93.960 |  |  |  | 0.000 |  |  |
| early_val_k1 | brief training | 15.677 | 85.906 |  |  |  | 0.000 |  |  |
| early_val_k2 | brief training | 12.225 | 63.087 |  |  |  | 0.000 |  |  |
| early_val_k3 | brief training | 2.982 | 8.725 |  |  |  | 0.310 |  |  |
| sh_r1_eta2 | successive halving | 1.477 | 2.685 |  |  |  | 0.230 |  |  |
| zico_half_then_k1 | proxy filter | 8.201 | 31.544 |  |  |  | 0.050 |  |  |
| zico_sizectrl_half_then_k1 | proxy filter | 15.677 | 85.906 |  |  |  | 0.110 |  |  |

### pems04: head control, Spearman with -test_mae

rho_within_head = n-weighted mean of the three heads, with a stratified bootstrap CI; mae_head_* = the pick among the MAE-head architectures alone.

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| full_training | ceiling | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| early_val_k10 | brief training | 0.869 | 0.888 | 0.807 | 0.929 | 0.953 | 0.804 | 0.924 | 0.876 | 5.128 |
| early_val_k8 | brief training | 0.799 | 0.833 | 0.745 | 0.884 | 0.892 | 0.773 | 0.849 | 0.000 | 0.000 |
| early_val_k6 | brief training | 0.657 | 0.753 | 0.647 | 0.824 | 0.824 | 0.731 | 0.724 | 2.982 | 23.077 |
| transfer_from_shenzhen | transfer | 0.691 | 0.687 | 0.576 | 0.766 | 0.655 | 0.770 | 0.627 | 2.635 | 17.949 |
| glass | zero-cost proxy | 0.588 | 0.686 | 0.575 | 0.759 | 0.618 | 0.622 | 0.799 | 0.000 | 0.000 |
| zico | zero-cost proxy | 0.594 | 0.685 | 0.574 | 0.754 | 0.622 | 0.616 | 0.800 | 0.000 | 0.000 |
| early_val_k5 | brief training | 0.582 | 0.676 | 0.548 | 0.774 | 0.754 | 0.619 | 0.676 | 0.000 | 0.000 |
| glass_t | zero-cost proxy | 0.560 | 0.657 | 0.540 | 0.730 | 0.565 | 0.614 | 0.767 | 0.000 | 0.000 |
| zico_t | zero-cost proxy | 0.565 | 0.654 | 0.538 | 0.729 | 0.565 | 0.612 | 0.761 | 0.000 | 0.000 |
| transfer_pooled | transfer | 0.676 | 0.640 | 0.528 | 0.725 | 0.623 | 0.720 | 0.574 | 6.574 | 46.154 |
| loco_gbr_arch | predictor, other cities | 0.650 | 0.638 | 0.523 | 0.729 | 0.650 | 0.731 | 0.537 | 0.846 | 2.564 |
| l2_norm_all | zero-cost proxy | 0.547 | 0.627 | 0.507 | 0.716 | 0.584 | 0.601 | 0.684 | 3.032 | 25.641 |
| loco_gbr_arch_proxies | predictor, other cities | 0.656 | 0.624 | 0.520 | 0.713 | 0.622 | 0.728 | 0.523 | 6.574 | 46.154 |
| loco_gbr_proxies | predictor, other cities | 0.647 | 0.622 | 0.514 | 0.706 | 0.599 | 0.703 | 0.557 | 0.846 | 2.564 |
| zico_sizectrl | zero-cost proxy | 0.569 | 0.606 | 0.442 | 0.714 | 0.651 | 0.560 | 0.619 | 0.000 | 0.000 |
| early_val_k4 | brief training | 0.468 | 0.591 | 0.451 | 0.695 | 0.707 | 0.473 | 0.624 | 5.047 | 35.897 |
| loco_ridge_arch | predictor, other cities | 0.623 | 0.587 | 0.457 | 0.680 | 0.605 | 0.624 | 0.538 | 6.574 | 46.154 |
| transfer_from_metrla | transfer | 0.576 | 0.501 | 0.368 | 0.643 | 0.548 | 0.594 | 0.372 | 0.846 | 2.564 |
| transfer_from_expytky | transfer | 0.594 | 0.479 | 0.360 | 0.594 | 0.450 | 0.541 | 0.438 | 6.574 | 46.154 |
| transfer_from_chengdu | transfer | 0.517 | 0.468 | 0.311 | 0.584 | 0.490 | 0.543 | 0.379 | 2.635 | 17.949 |
| early_val_k3 | brief training | 0.304 | 0.428 | 0.272 | 0.564 | 0.642 | 0.247 | 0.454 | 2.982 | 23.077 |
| params | floor | 0.244 | 0.324 | 0.170 | 0.476 | 0.129 | 0.280 | 0.511 | 18.990 | 97.436 |
| early_val_k1 | brief training | 0.130 | 0.312 | 0.137 | 0.468 | 0.498 | 0.274 | 0.214 | 8.745 | 58.974 |
| early_val_k2 | brief training | 0.156 | 0.309 | 0.133 | 0.453 | 0.361 | 0.211 | 0.369 | 7.691 | 53.846 |
| nwot | zero-cost proxy | 0.203 | 0.254 | 0.078 | 0.397 | 0.349 | 0.124 | 0.314 | 9.305 | 66.667 |
| zico_s | zero-cost proxy | 0.231 | 0.221 | 0.049 | 0.375 | 0.406 | 0.074 | 0.235 | 11.682 | 79.487 |
| glass_s | zero-cost proxy | 0.231 | 0.219 | 0.048 | 0.369 | 0.406 | 0.067 | 0.235 | 11.682 | 79.487 |
| flops | floor | 0.182 | 0.204 | 0.036 | 0.363 | 0.359 | 0.056 | 0.238 | 11.682 | 79.487 |
| grasp_all | zero-cost proxy | 0.268 | 0.194 | 0.045 | 0.335 | 0.502 | 0.067 | 0.097 | 9.515 | 71.795 |
| swap | zero-cost proxy | 0.111 | 0.193 | 0.010 | 0.357 | 0.065 | 0.111 | 0.367 | 3.032 | 25.641 |
| zen | zero-cost proxy | 0.120 | 0.177 | 0.037 | 0.322 | -0.081 | 0.105 | 0.437 | 3.032 | 25.641 |
| synflow_all | zero-cost proxy | 0.108 | 0.160 | -0.017 | 0.276 | 0.217 | -0.088 | 0.366 | 11.682 | 79.487 |
| swap_reg | zero-cost proxy | 0.071 | 0.070 | -0.103 | 0.249 | 0.213 | -0.069 | 0.106 | 11.682 | 79.487 |
| plain_all | zero-cost proxy | -0.186 | 0.065 | -0.101 | 0.217 | -0.056 | -0.167 | 0.386 | 5.303 | 38.462 |
| fisher | zero-cost proxy | -0.222 | -0.081 | -0.219 | 0.080 | -0.362 | -0.118 | 0.161 | 5.303 | 38.462 |
| grad_norm_all | zero-cost proxy | -0.234 | -0.106 | -0.261 | 0.047 | -0.390 | -0.026 | 0.020 | 18.673 | 94.872 |
| snip_all | zero-cost proxy | -0.233 | -0.142 | -0.296 | 0.012 | -0.423 | -0.049 | -0.030 | 18.673 | 94.872 |
| jacov | zero-cost proxy | -0.182 | -0.193 | -0.344 | -0.020 | -0.481 | -0.108 | -0.069 | 18.990 | 97.436 |
| nwot_per_layer | zero-cost proxy | -0.422 | -0.463 | -0.579 | -0.322 | -0.368 | -0.343 | -0.652 | 8.745 | 58.974 |

### chengdu: cost to one sigma, cheapest robust form first

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_from_shenzhen | transfer | 0.000 | 0.000 | 1.000 | 0.100 | 0.477 | 0.840 | 0.728 | 1.000 |
| transfer_pooled | transfer | 2.287 | 6.040 | 3.000 | 0.357 | 1.695 | 0.755 | 2.489 | 3.000 |
| transfer_from_metrla | transfer | 2.287 | 6.040 | 3.000 | 0.372 | 1.767 | 0.755 | 2.525 | 3.000 |
| jacov | zero-cost proxy | 6.571 | 36.913 |  |  |  | 0.655 | 6.137 | 10.000 |
| transfer_from_expytky | transfer | 1.519 | 2.013 |  |  |  | 0.720 | 8.370 | 9.000 |
| loco_gbr_arch_proxies | predictor, other cities | 2.287 | 6.040 |  |  |  | 0.750 | 8.623 | 8.000 |
| transfer_from_pems04 | transfer | 2.941 | 9.396 |  |  |  | 0.740 | 10.359 | 8.000 |
| loco_gbr_arch | predictor, other cities | 3.950 | 14.094 |  |  |  | 0.735 | 10.478 | 10.000 |
| zico_sizectrl_half_then_k1 | proxy filter | 6.321 | 33.557 | 8.000 | 1.788 | 8.489 | 0.730 | 10.735 | 8.000 |
| zen | zero-cost proxy | 9.874 | 74.497 |  |  |  | 0.510 | 11.208 | 10.000 |
| loco_gbr_proxies | predictor, other cities | 4.685 | 22.148 |  |  |  | 0.575 | 11.724 | 10.000 |
| zico_sizectrl_half_then_k3 | proxy filter | 2.288 | 6.711 | 3.000 | 2.413 | 11.459 | 0.755 | 11.815 | 3.000 |
| early_val_k1 | brief training | 6.321 | 33.557 |  |  |  | 0.655 | 14.950 | 10.000 |
| sh_r1_eta3 | successive halving | 2.287 | 6.040 | 2.000 | 3.351 | 15.910 | 0.750 | 15.967 | 2.000 |
| early_val_k2 | brief training | 2.958 | 10.067 | 8.000 | 3.480 | 16.526 | 0.750 | 16.652 | 5.000 |
| zico_sizectrl_half_then_k5 | proxy filter | 0.000 | 0.000 | 1.000 | 3.588 | 17.036 | 0.755 | 17.331 | 1.000 |
| sh_r1_eta2 | successive halving | 1.468 | 1.342 | 2.000 | 3.938 | 18.701 | 0.755 | 18.954 | 2.000 |
| early_val_k3 | brief training | 2.288 | 6.711 | 3.000 | 4.139 | 19.654 | 0.755 | 20.149 | 3.000 |
| zico_half_then_k5 | proxy filter | 2.958 | 10.067 |  |  |  | 0.675 | 24.430 | 10.000 |
| early_val_k4 | brief training | 2.287 | 6.040 | 5.000 | 5.716 | 27.145 | 0.755 | 28.188 | 5.000 |
| sh_r2_eta3 | successive halving | 2.287 | 6.040 | 3.000 | 5.913 | 28.078 | 0.755 | 28.306 | 3.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 6.452 | 30.637 | 0.890 | 31.080 | 1.000 |
| sh_r2_eta2 | successive halving | 2.287 | 6.040 | 5.000 | 6.630 | 31.485 | 0.755 | 31.375 | 3.000 |
| sh_r3_eta3 | successive halving | 2.287 | 6.040 | 3.000 | 7.615 | 36.159 | 0.755 | 36.258 | 3.000 |
| early_val_k6 | brief training | 0.000 | 0.000 | 1.000 | 7.712 | 36.621 | 0.760 | 37.028 | 1.000 |
| sh_r3_eta2 | successive halving | 2.287 | 6.040 | 5.000 | 8.468 | 40.211 | 1.000 | 40.612 | 3.000 |
| early_val_k8 | brief training | 1.468 | 1.342 | 2.000 | 10.295 | 48.888 | 1.000 | 49.301 | 2.000 |
| early_val_k10 | brief training | 0.000 | 0.000 | 1.000 | 12.729 | 60.446 | 1.000 | 60.921 | 1.000 |
| full_training | ceiling | 0.000 | 0.000 | 1.000 | 21.059 | 100.000 | 1.000 | 100.000 | 1.000 |
| random | floor | 7.839 |  |  |  |  | 0.175 |  |  |
| params | floor | 9.874 | 74.497 |  |  |  | 0.000 |  |  |
| flops | floor | 8.726 | 65.101 |  |  |  | 0.060 |  |  |
| zico | zero-cost proxy | 9.726 | 72.483 |  |  |  | 0.080 |  |  |
| zico_sizectrl | zero-cost proxy | 10.730 | 79.195 |  |  |  | 0.100 |  |  |
| swap | zero-cost proxy | 8.726 | 65.101 |  |  |  | 0.000 |  |  |
| swap_reg | zero-cost proxy | 15.952 | 97.987 |  |  |  | 0.040 |  |  |
| nwot | zero-cost proxy | 10.018 | 76.510 |  |  |  | 0.000 |  |  |
| synflow_all | zero-cost proxy | 2.939 | 8.725 |  |  |  | 0.110 |  |  |
| snip_all | zero-cost proxy | 4.080 | 15.436 |  |  |  | 0.000 |  |  |
| grasp_all | zero-cost proxy | 8.424 | 61.745 |  |  |  | 0.095 |  |  |
| grad_norm_all | zero-cost proxy | 4.080 | 15.436 |  |  |  | 0.000 |  |  |
| fisher | zero-cost proxy | 7.929 | 55.705 |  |  |  | 0.035 |  |  |
| l2_norm_all | zero-cost proxy | 9.726 | 72.483 |  |  |  | 0.000 |  |  |
| plain_all | zero-cost proxy | 7.929 | 55.705 |  |  |  | 0.080 |  |  |
| zico_t | zero-cost proxy | 2.939 | 8.725 |  |  |  | 0.080 |  |  |
| zico_s | zero-cost proxy | 13.670 | 92.617 |  |  |  | 0.060 |  |  |
| glass | zero-cost proxy | 9.726 | 72.483 |  |  |  | 0.080 |  |  |
| glass_t | zero-cost proxy | 2.939 | 8.725 |  |  |  | 0.080 |  |  |
| glass_s | zero-cost proxy | 13.670 | 92.617 |  |  |  | 0.060 |  |  |
| nwot_per_layer | zero-cost proxy | 11.287 | 81.879 |  |  |  | 0.000 |  |  |
| zico_half_then_k1 | proxy filter | 2.958 | 10.067 |  |  |  | 0.175 |  |  |
| zico_half_then_k3 | proxy filter | 2.288 | 6.711 |  |  |  | 0.210 |  |  |
| loco_ridge_arch | predictor, other cities | 2.941 | 9.396 |  |  |  | 0.475 |  |  |

### chengdu: head control, Spearman with -test_mae

rho_within_head = n-weighted mean of the three heads, with a stratified bootstrap CI; mae_head_* = the pick among the MAE-head architectures alone.

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| full_training | ceiling | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| early_val_k10 | brief training | 0.896 | 0.882 | 0.811 | 0.919 | 0.842 | 0.889 | 0.904 | 0.000 | 0.000 |
| early_val_k8 | brief training | 0.863 | 0.858 | 0.786 | 0.893 | 0.864 | 0.886 | 0.825 | 1.468 | 2.564 |
| early_val_k6 | brief training | 0.777 | 0.802 | 0.711 | 0.859 | 0.791 | 0.859 | 0.753 | 0.000 | 0.000 |
| transfer_from_shenzhen | transfer | 0.779 | 0.762 | 0.667 | 0.822 | 0.820 | 0.751 | 0.731 | 0.000 | 0.000 |
| early_val_k4 | brief training | 0.666 | 0.751 | 0.637 | 0.814 | 0.787 | 0.790 | 0.686 | 2.287 | 12.821 |
| early_val_k5 | brief training | 0.681 | 0.727 | 0.616 | 0.807 | 0.780 | 0.717 | 0.700 | 0.000 | 0.000 |
| loco_gbr_proxies | predictor, other cities | 0.676 | 0.647 | 0.519 | 0.736 | 0.745 | 0.570 | 0.651 | 4.685 | 38.462 |
| transfer_pooled | transfer | 0.680 | 0.645 | 0.513 | 0.738 | 0.715 | 0.615 | 0.624 | 2.287 | 12.821 |
| loco_gbr_arch | predictor, other cities | 0.680 | 0.636 | 0.507 | 0.746 | 0.712 | 0.635 | 0.582 | 3.950 | 25.641 |
| loco_gbr_arch_proxies | predictor, other cities | 0.667 | 0.625 | 0.499 | 0.727 | 0.694 | 0.636 | 0.565 | 2.287 | 12.821 |
| loco_ridge_arch | predictor, other cities | 0.635 | 0.607 | 0.469 | 0.707 | 0.623 | 0.617 | 0.585 | 2.941 | 17.949 |
| zico_t | zero-cost proxy | 0.516 | 0.585 | 0.444 | 0.688 | 0.653 | 0.585 | 0.535 | 2.941 | 17.949 |
| early_val_k3 | brief training | 0.486 | 0.583 | 0.438 | 0.680 | 0.502 | 0.665 | 0.559 | 2.288 | 15.385 |
| glass_t | zero-cost proxy | 0.512 | 0.578 | 0.433 | 0.686 | 0.653 | 0.574 | 0.526 | 2.941 | 17.949 |
| zico | zero-cost proxy | 0.467 | 0.532 | 0.382 | 0.643 | 0.568 | 0.553 | 0.485 | 2.941 | 17.949 |
| glass | zero-cost proxy | 0.465 | 0.524 | 0.377 | 0.633 | 0.564 | 0.546 | 0.474 | 2.941 | 17.949 |
| transfer_from_expytky | transfer | 0.584 | 0.481 | 0.327 | 0.597 | 0.581 | 0.373 | 0.516 | 1.519 | 5.128 |
| transfer_from_pems04 | transfer | 0.517 | 0.468 | 0.311 | 0.584 | 0.490 | 0.543 | 0.379 | 2.941 | 17.949 |
| transfer_from_metrla | transfer | 0.530 | 0.435 | 0.285 | 0.550 | 0.537 | 0.420 | 0.377 | 2.287 | 12.821 |
| zico_sizectrl | zero-cost proxy | 0.382 | 0.435 | 0.260 | 0.539 | 0.645 | 0.450 | 0.267 | 2.941 | 17.949 |
| early_val_k2 | brief training | 0.296 | 0.398 | 0.248 | 0.541 | 0.481 | 0.503 | 0.233 | 2.958 | 20.513 |
| jacov | zero-cost proxy | 0.298 | 0.268 | 0.086 | 0.419 | 0.192 | 0.309 | 0.283 | 6.571 | 53.846 |
| params | floor | 0.227 | 0.259 | 0.085 | 0.432 | 0.083 | 0.307 | 0.339 | 6.571 | 53.846 |
| plain_all | zero-cost proxy | -0.062 | 0.237 | 0.077 | 0.414 | 0.194 | 0.133 | 0.372 | 1.944 | 10.256 |
| fisher | zero-cost proxy | -0.101 | 0.184 | 0.013 | 0.374 | 0.013 | 0.170 | 0.322 | 1.944 | 10.256 |
| l2_norm_all | zero-cost proxy | 0.139 | 0.175 | 0.024 | 0.345 | 0.165 | 0.273 | 0.085 | 6.635 | 56.410 |
| early_val_k1 | brief training | 0.088 | 0.158 | -0.013 | 0.327 | 0.365 | 0.089 | 0.077 | 6.321 | 48.718 |
| zen | zero-cost proxy | 0.117 | 0.133 | -0.055 | 0.306 | -0.121 | 0.211 | 0.240 | 6.635 | 56.410 |
| synflow_all | zero-cost proxy | 0.043 | 0.129 | -0.057 | 0.293 | 0.107 | 0.174 | 0.099 | 8.726 | 87.179 |
| grad_norm_all | zero-cost proxy | -0.128 | 0.071 | -0.101 | 0.250 | -0.067 | 0.088 | 0.153 | 11.246 | 100.000 |
| snip_all | zero-cost proxy | -0.113 | 0.026 | -0.144 | 0.198 | -0.111 | 0.064 | 0.086 | 11.246 | 100.000 |
| grasp_all | zero-cost proxy | 0.199 | 0.023 | -0.154 | 0.177 | 0.068 | 0.033 | -0.018 | 4.461 | 35.897 |
| swap_reg | zero-cost proxy | -0.027 | -0.020 | -0.192 | 0.163 | 0.045 | -0.266 | 0.179 | 8.726 | 87.179 |
| swap | zero-cost proxy | -0.134 | -0.093 | -0.251 | 0.106 | -0.157 | 0.040 | -0.177 | 8.726 | 87.179 |
| nwot | zero-cost proxy | -0.298 | -0.280 | -0.440 | -0.102 | -0.289 | -0.245 | -0.310 | 10.018 | 94.872 |
| flops | floor | -0.306 | -0.302 | -0.471 | -0.124 | -0.260 | -0.292 | -0.343 | 8.726 | 87.179 |
| nwot_per_layer | zero-cost proxy | -0.314 | -0.335 | -0.460 | -0.176 | -0.289 | -0.325 | -0.378 | 8.085 | 79.487 |
| glass_s | zero-cost proxy | -0.344 | -0.355 | -0.507 | -0.190 | -0.284 | -0.344 | -0.417 | 8.726 | 87.179 |
| zico_s | zero-cost proxy | -0.348 | -0.356 | -0.509 | -0.190 | -0.284 | -0.348 | -0.417 | 8.726 | 87.179 |

### shenzhen: cost to one sigma, cheapest robust form first

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| transfer_from_chengdu | transfer | 0.000 | 0.000 | 1.000 | 0.125 | 0.392 | 1.000 | 0.600 | 1.000 |
| transfer_pooled | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.926 | 1.000 |
| transfer_from_metrla | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.934 | 1.000 |
| loco_gbr_arch_proxies | predictor, other cities | 1.260 | 1.342 | 2.000 | 0.347 | 1.084 | 1.000 | 1.227 | 2.000 |
| loco_gbr_arch | predictor, other cities | 1.260 | 1.342 | 2.000 | 0.347 | 1.084 | 1.000 | 1.323 | 1.000 |
| transfer_from_expytky | transfer | 1.260 | 1.342 | 5.000 | 1.016 | 3.178 | 1.000 | 2.457 | 3.000 |
| loco_ridge_arch | predictor, other cities | 2.965 | 2.685 | 2.000 | 0.564 | 1.765 | 1.000 | 2.633 | 2.000 |
| transfer_from_pems04 | transfer | 2.965 | 2.685 | 2.000 | 0.564 | 1.765 | 0.920 | 2.646 | 2.000 |
| loco_gbr_proxies | predictor, other cities | 2.965 | 2.685 | 3.000 | 0.697 | 2.180 | 0.940 | 3.225 | 3.000 |
| zico_sizectrl_half_then_k3 | proxy filter | 4.673 | 14.094 | 8.000 | 4.321 | 13.517 | 1.000 | 13.356 | 5.000 |
| zico_half_then_k3 | proxy filter | 4.673 | 14.094 | 8.000 | 4.362 | 13.643 | 0.830 | 13.860 | 5.000 |
| sh_r1_eta3 | successive halving | 0.000 | 0.000 | 1.000 | 4.891 | 15.299 | 1.000 | 15.131 | 1.000 |
| zico_sizectrl_half_then_k5 | proxy filter | 3.148 | 4.698 | 2.000 | 5.052 | 15.801 | 1.000 | 16.308 | 2.000 |
| sh_r1_eta2 | successive halving | 0.000 | 0.000 | 1.000 | 5.302 | 16.586 | 0.920 | 16.769 | 1.000 |
| zico_half_then_k5 | proxy filter | 3.148 | 4.698 | 8.000 | 6.085 | 19.034 | 0.830 | 19.242 | 5.000 |
| early_val_k2 | brief training | 4.673 | 14.094 |  |  |  | 0.705 | 20.500 | 10.000 |
| early_val_k3 | brief training | 4.673 | 14.094 | 8.000 | 6.791 | 21.242 | 0.970 | 21.124 | 5.000 |
| sh_r2_eta3 | successive halving | 0.000 | 0.000 | 1.000 | 7.827 | 24.483 | 0.940 | 24.581 | 1.000 |
| early_val_k4 | brief training | 4.673 | 14.094 | 8.000 | 8.259 | 25.833 | 0.940 | 25.705 | 5.000 |
| sh_r2_eta2 | successive halving | 0.000 | 0.000 | 1.000 | 8.862 | 27.720 | 0.980 | 27.639 | 1.000 |
| early_val_k5 | brief training | 3.148 | 4.698 | 2.000 | 9.027 | 28.235 | 1.000 | 28.775 | 2.000 |
| sh_r3_eta3 | successive halving | 0.000 | 0.000 | 1.000 | 10.583 | 33.104 | 1.000 | 33.233 | 1.000 |
| early_val_k6 | brief training | 3.148 | 4.698 | 5.000 | 11.311 | 35.381 | 1.000 | 36.094 | 5.000 |
| sh_r3_eta2 | successive halving | 0.000 | 0.000 | 1.000 | 11.935 | 37.331 | 1.000 | 37.638 | 1.000 |
| early_val_k8 | brief training | 0.000 | 0.000 | 1.000 | 13.929 | 43.570 | 0.920 | 44.088 | 1.000 |
| early_val_k10 | brief training | 0.000 | 0.000 | 1.000 | 17.366 | 54.319 | 1.000 | 54.824 | 1.000 |
| full_training | ceiling | 0.000 | 0.000 | 1.000 | 31.970 | 100.000 | 1.000 | 100.000 | 1.000 |
| random | floor | 9.075 |  |  |  |  | 0.145 |  |  |
| params | floor | 7.231 | 33.557 |  |  |  | 0.000 |  |  |
| flops | floor | 11.499 | 75.839 |  |  |  | 0.035 |  |  |
| zico | zero-cost proxy | 4.540 | 12.081 |  |  |  | 0.050 |  |  |
| zico_sizectrl | zero-cost proxy | 10.307 | 66.443 |  |  |  | 0.040 |  |  |
| swap | zero-cost proxy | 8.827 | 51.678 |  |  |  | 0.000 |  |  |
| swap_reg | zero-cost proxy | 18.401 | 98.658 |  |  |  | 0.040 |  |  |
| nwot | zero-cost proxy | 8.827 | 51.678 |  |  |  | 0.000 |  |  |
| synflow_all | zero-cost proxy | 5.123 | 16.779 |  |  |  | 0.030 |  |  |
| snip_all | zero-cost proxy | 8.543 | 47.651 |  |  |  | 0.000 |  |  |
| grasp_all | zero-cost proxy | 15.239 | 93.960 |  |  |  | 0.000 |  |  |
| grad_norm_all | zero-cost proxy | 13.391 | 87.248 |  |  |  | 0.000 |  |  |
| fisher | zero-cost proxy | 13.391 | 87.248 |  |  |  | 0.000 |  |  |
| jacov | zero-cost proxy | 7.678 | 38.255 |  |  |  | 0.000 |  |  |
| zen | zero-cost proxy | 7.231 | 33.557 |  |  |  | 0.015 |  |  |
| l2_norm_all | zero-cost proxy | 4.540 | 12.081 |  |  |  | 0.010 |  |  |
| plain_all | zero-cost proxy | 13.391 | 87.248 |  |  |  | 0.000 |  |  |
| zico_t | zero-cost proxy | 5.123 | 16.779 |  |  |  | 0.060 |  |  |
| zico_s | zero-cost proxy | 11.546 | 76.510 |  |  |  | 0.030 |  |  |
| glass | zero-cost proxy | 4.540 | 12.081 |  |  |  | 0.080 |  |  |
| glass_t | zero-cost proxy | 5.123 | 16.779 |  |  |  | 0.100 |  |  |
| glass_s | zero-cost proxy | 11.546 | 76.510 |  |  |  | 0.030 |  |  |
| nwot_per_layer | zero-cost proxy | 14.133 | 89.262 |  |  |  | 0.000 |  |  |
| early_val_k1 | brief training | 5.339 | 17.450 |  |  |  | 0.040 |  |  |
| zico_half_then_k1 | proxy filter | 5.339 | 17.450 |  |  |  | 0.055 |  |  |
| zico_sizectrl_half_then_k1 | proxy filter | 5.339 | 17.450 |  |  |  | 0.375 |  |  |

### shenzhen: head control, Spearman with -test_mae

rho_within_head = n-weighted mean of the three heads, with a stratified bootstrap CI; mae_head_* = the pick among the MAE-head architectures alone.

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| full_training | ceiling | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| early_val_k10 | brief training | 0.909 | 0.866 | 0.788 | 0.904 | 0.870 | 0.848 | 0.881 | 0.000 | 0.000 |
| early_val_k8 | brief training | 0.897 | 0.859 | 0.800 | 0.889 | 0.860 | 0.844 | 0.872 | 0.000 | 0.000 |
| loco_gbr_arch | predictor, other cities | 0.887 | 0.844 | 0.772 | 0.886 | 0.907 | 0.821 | 0.821 | 1.260 | 5.128 |
| transfer_pooled | transfer | 0.879 | 0.843 | 0.771 | 0.881 | 0.862 | 0.870 | 0.801 | 0.965 | 2.564 |
| loco_gbr_arch_proxies | predictor, other cities | 0.876 | 0.840 | 0.774 | 0.878 | 0.837 | 0.875 | 0.806 | 1.260 | 5.128 |
| loco_gbr_proxies | predictor, other cities | 0.844 | 0.791 | 0.710 | 0.842 | 0.754 | 0.821 | 0.789 | 2.965 | 7.692 |
| early_val_k6 | brief training | 0.817 | 0.785 | 0.681 | 0.843 | 0.795 | 0.800 | 0.763 | 3.148 | 12.821 |
| loco_ridge_arch | predictor, other cities | 0.835 | 0.770 | 0.688 | 0.824 | 0.874 | 0.689 | 0.775 | 2.965 | 7.692 |
| transfer_from_chengdu | transfer | 0.779 | 0.762 | 0.667 | 0.822 | 0.820 | 0.751 | 0.731 | 0.000 | 0.000 |
| early_val_k5 | brief training | 0.725 | 0.700 | 0.588 | 0.775 | 0.749 | 0.702 | 0.663 | 3.148 | 12.821 |
| transfer_from_pems04 | transfer | 0.691 | 0.687 | 0.576 | 0.766 | 0.655 | 0.770 | 0.627 | 2.965 | 7.692 |
| early_val_k4 | brief training | 0.623 | 0.656 | 0.535 | 0.737 | 0.659 | 0.653 | 0.657 | 4.673 | 25.641 |
| zico_t | zero-cost proxy | 0.502 | 0.628 | 0.504 | 0.718 | 0.677 | 0.544 | 0.676 | 2.965 | 7.692 |
| glass_t | zero-cost proxy | 0.497 | 0.628 | 0.501 | 0.720 | 0.677 | 0.552 | 0.667 | 2.965 | 7.692 |
| transfer_from_expytky | transfer | 0.753 | 0.617 | 0.503 | 0.706 | 0.691 | 0.605 | 0.575 | 1.260 | 5.128 |
| zico | zero-cost proxy | 0.465 | 0.596 | 0.462 | 0.683 | 0.609 | 0.515 | 0.666 | 2.965 | 7.692 |
| glass | zero-cost proxy | 0.465 | 0.594 | 0.459 | 0.682 | 0.611 | 0.525 | 0.652 | 2.965 | 7.692 |
| early_val_k3 | brief training | 0.419 | 0.579 | 0.458 | 0.680 | 0.627 | 0.635 | 0.489 | 4.673 | 25.641 |
| transfer_from_metrla | transfer | 0.716 | 0.576 | 0.438 | 0.668 | 0.629 | 0.606 | 0.507 | 0.965 | 2.564 |
| zico_sizectrl | zero-cost proxy | 0.375 | 0.495 | 0.336 | 0.613 | 0.651 | 0.415 | 0.462 | 2.965 | 7.692 |
| early_val_k2 | brief training | 0.226 | 0.411 | 0.269 | 0.536 | 0.434 | 0.315 | 0.491 | 4.673 | 25.641 |
| early_val_k1 | brief training | 0.072 | 0.367 | 0.213 | 0.502 | 0.404 | 0.313 | 0.393 | 5.339 | 33.333 |
| l2_norm_all | zero-cost proxy | 0.249 | 0.331 | 0.193 | 0.470 | 0.281 | 0.393 | 0.305 | 6.618 | 48.718 |
| params | floor | 0.246 | 0.316 | 0.164 | 0.459 | 0.134 | 0.317 | 0.447 | 7.678 | 76.923 |
| zen | zero-cost proxy | 0.153 | 0.191 | 0.036 | 0.338 | -0.059 | 0.175 | 0.390 | 6.618 | 48.718 |
| plain_all | zero-cost proxy | -0.234 | 0.167 | 0.016 | 0.319 | -0.090 | 0.086 | 0.435 | 5.455 | 35.897 |
| jacov | zero-cost proxy | 0.163 | 0.118 | -0.051 | 0.266 | -0.121 | 0.216 | 0.193 | 7.678 | 76.923 |
| fisher | zero-cost proxy | -0.276 | 0.104 | -0.039 | 0.260 | -0.171 | 0.047 | 0.360 | 5.455 | 35.897 |
| grasp_all | zero-cost proxy | 0.374 | 0.102 | -0.073 | 0.231 | 0.414 | -0.000 | -0.022 | 4.789 | 28.205 |
| grad_norm_all | zero-cost proxy | -0.291 | 0.036 | -0.104 | 0.207 | -0.299 | 0.122 | 0.193 | 11.616 | 94.872 |
| swap | zero-cost proxy | -0.056 | 0.015 | -0.161 | 0.193 | -0.257 | 0.087 | 0.142 | 8.827 | 82.051 |
| swap_reg | zero-cost proxy | 0.029 | 0.014 | -0.177 | 0.204 | 0.075 | -0.094 | 0.078 | 11.499 | 92.308 |
| snip_all | zero-cost proxy | -0.239 | 0.008 | -0.131 | 0.177 | -0.312 | 0.120 | 0.129 | 11.616 | 94.872 |
| synflow_all | zero-cost proxy | -0.143 | -0.033 | -0.193 | 0.129 | -0.016 | -0.201 | 0.124 | 11.499 | 92.308 |
| nwot | zero-cost proxy | -0.155 | -0.117 | -0.279 | 0.051 | -0.226 | -0.134 | -0.020 | 8.827 | 82.051 |
| flops | floor | -0.186 | -0.164 | -0.330 | -0.002 | -0.182 | -0.222 | -0.093 | 11.499 | 92.308 |
| zico_s | zero-cost proxy | -0.190 | -0.194 | -0.365 | -0.041 | -0.151 | -0.230 | -0.189 | 11.499 | 92.308 |
| glass_s | zero-cost proxy | -0.189 | -0.196 | -0.369 | -0.047 | -0.151 | -0.235 | -0.189 | 11.499 | 92.308 |
| nwot_per_layer | zero-cost proxy | -0.334 | -0.378 | -0.507 | -0.232 | -0.321 | -0.233 | -0.565 | 10.078 | 89.744 |

### expytky: cost to one sigma, cheapest robust form first

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| loco_gbr_arch_proxies | predictor, other cities | 0.635 | 0.671 | 1.000 | 0.123 | 0.218 | 0.995 | 0.337 | 1.000 |
| loco_gbr_arch | predictor, other cities | 4.692 | 7.383 | 2.000 | 0.195 | 0.345 | 1.000 | 0.527 | 2.000 |
| transfer_from_chengdu | transfer | 4.692 | 7.383 | 3.000 | 0.296 | 0.524 | 0.970 | 0.702 | 2.000 |
| transfer_from_metrla | transfer | 1.455 | 2.013 | 2.000 | 0.516 | 0.912 | 1.000 | 1.290 | 1.000 |
| transfer_from_shenzhen | transfer | 4.692 | 7.383 | 3.000 | 0.587 | 1.039 | 1.000 | 1.308 | 2.000 |
| transfer_pooled | transfer | 1.455 | 2.013 | 5.000 | 1.276 | 2.257 | 1.000 | 1.754 | 3.000 |
| loco_gbr_proxies | predictor, other cities | 1.455 | 2.013 | 8.000 | 1.679 | 2.971 | 0.990 | 2.634 | 5.000 |
| loco_ridge_arch | predictor, other cities | 4.487 | 5.369 | 5.000 | 2.029 | 3.589 | 1.000 | 2.973 | 3.000 |
| zico_sizectrl | zero-cost proxy | 10.394 | 69.799 |  |  |  | 0.610 | 9.547 | 10.000 |
| zico_half_then_k1 | proxy filter | 3.213 | 2.685 |  |  |  | 0.895 | 11.545 | 8.000 |
| zico_sizectrl_half_then_k1 | proxy filter | 3.213 | 2.685 |  |  |  | 0.800 | 12.189 | 10.000 |
| zico_half_then_k3 | proxy filter | 1.455 | 2.013 | 2.000 | 6.899 | 12.204 | 1.000 | 12.418 | 2.000 |
| zico_sizectrl_half_then_k3 | proxy filter | 1.455 | 2.013 | 2.000 | 7.160 | 12.667 | 1.000 | 12.840 | 2.000 |
| early_val_k2 | brief training | 1.455 | 2.013 | 2.000 | 8.602 | 15.217 | 0.940 | 15.515 | 2.000 |
| early_val_k1 | brief training | 3.213 | 2.685 |  |  |  | 0.520 | 17.690 | 10.000 |
| sh_r1_eta3 | successive halving | 1.455 | 2.013 | 2.000 | 10.321 | 18.259 | 1.000 | 18.214 | 1.000 |
| zico_half_then_k5 | proxy filter | 1.455 | 2.013 | 2.000 | 11.169 | 19.758 | 1.000 | 20.007 | 1.000 |
| sh_r1_eta2 | successive halving | 1.455 | 2.013 | 2.000 | 11.455 | 20.264 | 1.000 | 20.472 | 1.000 |
| zico_sizectrl_half_then_k5 | proxy filter | 1.455 | 2.013 | 2.000 | 11.605 | 20.530 | 1.000 | 20.647 | 1.000 |
| early_val_k3 | brief training | 1.455 | 2.013 | 2.000 | 12.645 | 22.369 | 1.000 | 22.682 | 2.000 |
| early_val_k4 | brief training | 0.635 | 0.671 | 1.000 | 16.419 | 29.045 | 1.000 | 29.271 | 1.000 |
| sh_r2_eta3 | successive halving | 1.455 | 2.013 | 2.000 | 16.895 | 29.888 | 1.000 | 30.413 | 1.000 |
| sh_r2_eta2 | successive halving | 1.455 | 2.013 | 2.000 | 19.261 | 34.074 | 1.000 | 33.634 | 1.000 |
| early_val_k5 | brief training | 1.455 | 2.013 | 2.000 | 20.733 | 36.678 | 1.000 | 37.006 | 1.000 |
| sh_r3_eta3 | successive halving | 1.455 | 2.013 | 2.000 | 22.757 | 40.258 | 1.000 | 40.065 | 1.000 |
| early_val_k6 | brief training | 1.455 | 2.013 | 2.000 | 24.778 | 43.834 | 1.000 | 44.024 | 1.000 |
| sh_r3_eta2 | successive halving | 1.455 | 2.013 | 2.000 | 25.655 | 45.386 | 1.000 | 45.888 | 1.000 |
| early_val_k8 | brief training | 1.455 | 2.013 | 2.000 | 32.858 | 58.128 | 1.000 | 58.280 | 1.000 |
| early_val_k10 | brief training | 1.455 | 2.013 | 2.000 | 39.990 | 70.744 | 1.000 | 70.932 | 1.000 |
| full_training | ceiling | 0.000 | 0.000 | 1.000 | 56.527 | 100.000 | 1.000 | 100.000 | 1.000 |
| random | floor | 9.006 |  |  |  |  | 0.150 |  |  |
| params | floor | 4.288 | 4.698 |  |  |  | 0.000 |  |  |
| flops | floor | 11.608 | 81.879 |  |  |  | 0.000 |  |  |
| zico | zero-cost proxy | 8.816 | 46.980 |  |  |  | 0.220 |  |  |
| swap | zero-cost proxy | 12.620 | 90.604 |  |  |  | 0.000 |  |  |
| swap_reg | zero-cost proxy | 11.608 | 81.879 |  |  |  | 0.000 |  |  |
| nwot | zero-cost proxy | 9.584 | 59.732 |  |  |  | 0.000 |  |  |
| synflow_all | zero-cost proxy | 7.789 | 32.215 |  |  |  | 0.000 |  |  |
| snip_all | zero-cost proxy | 9.931 | 64.430 |  |  |  | 0.000 |  |  |
| grasp_all | zero-cost proxy | 9.024 | 49.664 |  |  |  | 0.000 |  |  |
| grad_norm_all | zero-cost proxy | 14.913 | 97.315 |  |  |  | 0.000 |  |  |
| fisher | zero-cost proxy | 14.913 | 97.315 |  |  |  | 0.000 |  |  |
| jacov | zero-cost proxy | 7.500 | 28.188 |  |  |  | 0.040 |  |  |
| zen | zero-cost proxy | 4.288 | 4.698 |  |  |  | 0.050 |  |  |
| l2_norm_all | zero-cost proxy | 8.816 | 46.980 |  |  |  | 0.035 |  |  |
| plain_all | zero-cost proxy | 8.569 | 41.611 |  |  |  | 0.000 |  |  |
| zico_t | zero-cost proxy | 7.789 | 32.215 |  |  |  | 0.215 |  |  |
| zico_s | zero-cost proxy | 12.420 | 88.591 |  |  |  | 0.000 |  |  |
| glass | zero-cost proxy | 8.816 | 46.980 |  |  |  | 0.200 |  |  |
| glass_t | zero-cost proxy | 7.789 | 32.215 |  |  |  | 0.190 |  |  |
| glass_s | zero-cost proxy | 12.420 | 88.591 |  |  |  | 0.000 |  |  |
| nwot_per_layer | zero-cost proxy | 13.344 | 95.302 |  |  |  | 0.000 |  |  |
| transfer_from_pems04 | transfer | 4.487 | 5.369 |  |  |  | 0.440 |  |  |

### expytky: head control, Spearman with -test_mae

rho_within_head = n-weighted mean of the three heads, with a stratified bootstrap CI; mae_head_* = the pick among the MAE-head architectures alone.

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| full_training | ceiling | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| early_val_k6 | brief training | 0.839 | 0.748 | 0.644 | 0.810 | 0.806 | 0.675 | 0.779 | 1.455 | 7.692 |
| early_val_k8 | brief training | 0.847 | 0.738 | 0.638 | 0.802 | 0.778 | 0.622 | 0.825 | 1.455 | 7.692 |
| early_val_k10 | brief training | 0.857 | 0.735 | 0.641 | 0.804 | 0.775 | 0.619 | 0.821 | 1.455 | 7.692 |
| early_val_k5 | brief training | 0.812 | 0.718 | 0.591 | 0.799 | 0.745 | 0.695 | 0.721 | 1.455 | 7.692 |
| early_val_k4 | brief training | 0.749 | 0.687 | 0.565 | 0.785 | 0.811 | 0.730 | 0.555 | 0.635 | 2.564 |
| early_val_k3 | brief training | 0.604 | 0.666 | 0.554 | 0.762 | 0.779 | 0.792 | 0.459 | 1.455 | 7.692 |
| transfer_pooled | transfer | 0.789 | 0.641 | 0.522 | 0.730 | 0.681 | 0.579 | 0.672 | 1.455 | 7.692 |
| transfer_from_metrla | transfer | 0.756 | 0.626 | 0.517 | 0.705 | 0.597 | 0.595 | 0.676 | 1.455 | 7.692 |
| transfer_from_shenzhen | transfer | 0.753 | 0.617 | 0.503 | 0.706 | 0.691 | 0.605 | 0.575 | 4.692 | 25.641 |
| loco_gbr_proxies | predictor, other cities | 0.721 | 0.552 | 0.428 | 0.645 | 0.563 | 0.429 | 0.668 | 1.455 | 7.692 |
| loco_gbr_arch_proxies | predictor, other cities | 0.705 | 0.547 | 0.428 | 0.656 | 0.629 | 0.350 | 0.684 | 0.635 | 2.564 |
| loco_gbr_arch | predictor, other cities | 0.693 | 0.541 | 0.409 | 0.664 | 0.645 | 0.382 | 0.624 | 4.692 | 25.641 |
| loco_ridge_arch | predictor, other cities | 0.727 | 0.512 | 0.402 | 0.627 | 0.641 | 0.260 | 0.671 | 4.487 | 17.949 |
| early_val_k2 | brief training | 0.344 | 0.504 | 0.367 | 0.628 | 0.669 | 0.706 | 0.182 | 1.455 | 7.692 |
| transfer_from_chengdu | transfer | 0.584 | 0.481 | 0.327 | 0.597 | 0.581 | 0.373 | 0.516 | 4.692 | 25.641 |
| transfer_from_pems04 | transfer | 0.594 | 0.479 | 0.360 | 0.594 | 0.450 | 0.541 | 0.438 | 4.487 | 17.949 |
| glass_t | zero-cost proxy | 0.293 | 0.345 | 0.204 | 0.472 | 0.404 | 0.009 | 0.639 | 4.487 | 17.949 |
| zico_t | zero-cost proxy | 0.304 | 0.344 | 0.201 | 0.469 | 0.404 | -0.002 | 0.647 | 4.487 | 17.949 |
| glass | zero-cost proxy | 0.266 | 0.311 | 0.162 | 0.447 | 0.334 | 0.011 | 0.593 | 4.487 | 17.949 |
| zico | zero-cost proxy | 0.271 | 0.310 | 0.164 | 0.441 | 0.334 | 0.002 | 0.600 | 4.487 | 17.949 |
| zico_sizectrl | zero-cost proxy | 0.225 | 0.243 | 0.088 | 0.397 | 0.236 | 0.071 | 0.420 | 4.487 | 17.949 |
| params | floor | 0.144 | 0.190 | 0.031 | 0.334 | 0.170 | -0.061 | 0.456 | 4.966 | 30.769 |
| early_val_k1 | brief training | 0.099 | 0.173 | -0.004 | 0.318 | 0.465 | 0.309 | -0.174 | 3.213 | 10.256 |
| grasp_all | zero-cost proxy | 0.328 | 0.115 | -0.055 | 0.287 | 0.492 | 0.059 | -0.105 | 4.081 | 15.385 |
| l2_norm_all | zero-cost proxy | 0.108 | 0.098 | -0.073 | 0.271 | 0.118 | 0.012 | 0.170 | 5.057 | 33.333 |
| zen | zero-cost proxy | 0.058 | 0.084 | -0.073 | 0.244 | 0.012 | -0.106 | 0.325 | 5.057 | 33.333 |
| jacov | zero-cost proxy | 0.124 | 0.083 | -0.096 | 0.227 | 0.047 | 0.081 | 0.110 | 7.500 | 64.103 |
| snip_all | zero-cost proxy | -0.227 | 0.011 | -0.152 | 0.178 | -0.335 | 0.044 | 0.229 | 7.792 | 66.667 |
| grad_norm_all | zero-cost proxy | -0.274 | -0.016 | -0.176 | 0.147 | -0.370 | -0.001 | 0.226 | 11.608 | 97.436 |
| swap | zero-cost proxy | -0.150 | -0.086 | -0.256 | 0.103 | -0.203 | -0.149 | 0.062 | 11.608 | 97.436 |
| plain_all | zero-cost proxy | -0.323 | -0.094 | -0.264 | 0.083 | -0.312 | -0.194 | 0.164 | 8.098 | 69.231 |
| fisher | zero-cost proxy | -0.329 | -0.099 | -0.254 | 0.072 | -0.303 | -0.209 | 0.160 | 8.098 | 69.231 |
| swap_reg | zero-cost proxy | -0.083 | -0.101 | -0.279 | 0.088 | 0.000 | -0.183 | -0.094 | 11.608 | 97.436 |
| nwot | zero-cost proxy | -0.139 | -0.124 | -0.277 | 0.054 | -0.221 | -0.154 | -0.024 | 9.584 | 92.308 |
| glass_s | zero-cost proxy | -0.134 | -0.166 | -0.314 | -0.009 | -0.207 | -0.086 | -0.217 | 11.608 | 97.436 |
| flops | floor | -0.161 | -0.167 | -0.334 | -0.007 | -0.210 | -0.183 | -0.119 | 11.608 | 97.436 |
| zico_s | zero-cost proxy | -0.133 | -0.167 | -0.314 | -0.011 | -0.207 | -0.088 | -0.217 | 11.608 | 97.436 |
| synflow_all | zero-cost proxy | -0.239 | -0.178 | -0.339 | -0.014 | -0.053 | -0.346 | -0.102 | 11.608 | 97.436 |
| nwot_per_layer | zero-cost proxy | -0.205 | -0.200 | -0.343 | -0.060 | -0.172 | 0.048 | -0.469 | 8.671 | 79.487 |

### Convergence

k_rho06_* = the smallest k at which early validation reaches rho >= 0.6; late = the within-head k is above 3.

| city | head | n | median_best_epoch | share_stopped_early | k_rho06_all_heads | k_rho06_within_head | late | rho_within_k1 | rho_within_k2 | rho_within_k3 | rho_within_k5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| metrla | all | 150 | 14.000 | 0.527 | 2 | 4 | True | 0.446 | 0.557 | 0.591 | 0.697 |
| metrla | mae | 40 | 18.000 | 0.125 | 2 | 4 | True | 0.446 | 0.557 | 0.591 | 0.697 |
| metrla | mse | 55 | 7.000 | 0.945 | 2 | 4 | True | 0.446 | 0.557 | 0.591 | 0.697 |
| metrla | quantile | 55 | 15.000 | 0.400 | 2 | 4 | True | 0.446 | 0.557 | 0.591 | 0.697 |
| pems04 | all | 150 | 20.000 | 0.000 | 6 | 5 | True | 0.312 | 0.309 | 0.428 | 0.676 |
| pems04 | mae | 40 | 20.000 | 0.000 | 6 | 5 | True | 0.312 | 0.309 | 0.428 | 0.676 |
| pems04 | mse | 55 | 20.000 | 0.000 | 6 | 5 | True | 0.312 | 0.309 | 0.428 | 0.676 |
| pems04 | quantile | 55 | 19.000 | 0.000 | 6 | 5 | True | 0.312 | 0.309 | 0.428 | 0.676 |
| chengdu | all | 150 | 13.000 | 0.653 | 4 | 4 | True | 0.158 | 0.398 | 0.583 | 0.727 |
| chengdu | mae | 40 | 14.000 | 0.550 | 4 | 4 | True | 0.158 | 0.398 | 0.583 | 0.727 |
| chengdu | mse | 55 | 11.000 | 0.782 | 4 | 4 | True | 0.158 | 0.398 | 0.583 | 0.727 |
| chengdu | quantile | 55 | 13.000 | 0.600 | 4 | 4 | True | 0.158 | 0.398 | 0.583 | 0.727 |
| shenzhen | all | 150 | 17.000 | 0.313 | 4 | 4 | True | 0.367 | 0.411 | 0.579 | 0.700 |
| shenzhen | mae | 40 | 18.000 | 0.250 | 4 | 4 | True | 0.367 | 0.411 | 0.579 | 0.700 |
| shenzhen | mse | 55 | 13.000 | 0.600 | 4 | 4 | True | 0.367 | 0.411 | 0.579 | 0.700 |
| shenzhen | quantile | 55 | 19.000 | 0.073 | 4 | 4 | True | 0.367 | 0.411 | 0.579 | 0.700 |
| expytky | all | 150 | 9.000 | 0.827 | 3 | 3 | False | 0.173 | 0.504 | 0.666 | 0.718 |
| expytky | mae | 40 | 9.500 | 0.800 | 3 | 3 | False | 0.173 | 0.504 | 0.666 | 0.718 |
| expytky | mse | 55 | 5.000 | 0.964 | 3 | 3 | False | 0.173 | 0.504 | 0.666 | 0.718 |
| expytky | quantile | 55 | 12.000 | 0.709 | 3 | 3 | False | 0.173 | 0.504 | 0.666 | 0.718 |
