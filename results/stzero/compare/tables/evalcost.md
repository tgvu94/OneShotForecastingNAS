# evalcost: cost against quality of every cheap evaluator, target = test_mae (seed 0)

Regret = the evaluator's pick minus the best architecture of the set, in MAE units of the normalised target and in units of sigma_seed. sigma_seed is provisional: the std over seeds 0 to 2 of the few architectures that have three seeds (count per city below). GPU-hours are the logged seconds on one H100 3g.40gb slice. A zero-cost proxy is recorded at 0 h (seconds per architecture). rho is Spearman with -MAE; partial = after rank regression on log params; within head = n-weighted mean of rho inside each loss head.

- pems04: N = 300, max epochs 20, sigma_seed = 0.0004 over 5 architectures
- pems08: N = 150, max epochs 20, sigma_seed = 0.0009 over 5 architectures
- metrla: N = 150, max epochs 20, sigma_seed = 0.0059 over 5 architectures

### pems04: floors, proxies, brief training, ceiling

| evaluator | kind | gpu_hours | regret_top1 | regret_top1_sigma | regret_best_of_5 | regret_best_of_5_sigma | pick_rank_pct | rho | rho_partial | rho_within_head |
|---|---|---|---|---|---|---|---|---|---|---|
| random | floor | 0.000 | 0.005 | 12.727 | 0.002 | 5.905 | 50.000 | 0.000 | 0.000 | 0.000 |
| params | floor | 0.000 | 0.005 | 13.346 | 0.001 | 2.848 | 55.518 | 0.189 | 0.001 | 0.266 |
| flops | floor | 0.000 | 0.007 | 18.841 | 0.004 | 11.121 | 88.294 | 0.266 | 0.243 | 0.273 |
| zico | zero-cost proxy | 0.000 | 0.002 | 3.880 | 0.001 | 2.848 | 8.361 | 0.534 | 0.567 | 0.597 |
| zico_sizectrl | zero-cost proxy | 0.000 | 0.001 | 3.443 | 0.001 | 1.402 | 5.686 | 0.534 | 0.533 | 0.576 |
| swap | zero-cost proxy | 0.000 | 0.004 | 9.805 | 0.001 | 2.608 | 31.438 | 0.206 | 0.114 | 0.213 |
| swap_reg | zero-cost proxy | 0.000 | 0.005 | 13.481 | 0.005 | 12.894 | 57.191 | 0.093 | 0.068 | 0.059 |
| nwot | zero-cost proxy | 0.000 | 0.006 | 15.365 | 0.004 | 9.805 | 71.237 | 0.296 | 0.240 | 0.313 |
| synflow_all | zero-cost proxy | 0.000 | 0.004 | 8.972 | 0.001 | 3.512 | 25.418 | 0.138 | 0.138 | 0.202 |
| snip_all | zero-cost proxy | 0.000 | 0.004 | 9.648 | 0.004 | 9.648 | 30.100 | -0.220 | -0.283 | -0.135 |
| grasp_all | zero-cost proxy | 0.000 | 0.007 | 18.769 | 0.002 | 5.600 | 87.960 | 0.287 | 0.315 | 0.163 |
| grad_norm_all | zero-cost proxy | 0.000 | 0.004 | 9.648 | 0.004 | 9.648 | 30.100 | -0.231 | -0.288 | -0.100 |
| fisher | zero-cost proxy | 0.000 | 0.004 | 9.648 | 0.004 | 9.648 | 30.100 | -0.226 | -0.257 | -0.058 |
| jacov | zero-cost proxy | 0.000 | 0.006 | 15.678 | 0.005 | 13.346 | 73.244 | -0.249 | -0.282 | -0.283 |
| zen | zero-cost proxy | 0.000 | 0.006 | 15.678 | 0.002 | 4.042 | 73.244 | 0.120 | -0.137 | 0.170 |
| l2_norm_all | zero-cost proxy | 0.000 | 0.001 | 2.848 | 0.001 | 2.848 | 5.351 | 0.460 | 0.475 | 0.543 |
| plain_all | zero-cost proxy | 0.000 | 0.004 | 9.648 | 0.004 | 9.648 | 30.100 | -0.237 | -0.264 | 0.019 |
| early_val_k1 | brief training | 2.297 | 0.007 | 16.495 | 0.005 | 13.011 | 77.926 | 0.111 | 0.141 | 0.340 |
| early_val_k2 | brief training | 4.394 | 0.005 | 12.090 | 0.004 | 8.854 | 48.161 | 0.137 | 0.162 | 0.382 |
| early_val_k3 | brief training | 6.490 | 0.005 | 12.716 | 0.000 | 1.180 | 50.167 | 0.259 | 0.283 | 0.493 |
| early_val_k4 | brief training | 8.590 | 0.005 | 12.716 | 0.000 | 1.136 | 50.167 | 0.422 | 0.440 | 0.613 |
| early_val_k5 | brief training | 10.690 | 0.001 | 1.969 | 0.000 | 1.136 | 3.344 | 0.519 | 0.527 | 0.662 |
| early_val_k6 | brief training | 12.795 | 0.000 | 1.136 | 0.000 | 0.000 | 1.338 | 0.643 | 0.648 | 0.765 |
| early_val_k8 | brief training | 16.983 | 0.000 | 1.136 | 0.000 | 0.000 | 1.338 | 0.768 | 0.770 | 0.846 |
| early_val_k10 | brief training | 21.176 | 0.001 | 1.337 | 0.000 | 0.000 | 2.676 | 0.853 | 0.852 | 0.897 |
| early_val_k15 | brief training | 31.663 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.935 | 0.933 | 0.944 |
| full_training | ceiling | 42.141 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |

### pems04: successive halving on the logged curves

| evaluator | gpu_hours | rounds | dropped_top10_round1 | regret_top1 | regret_top1_sigma | regret_best_of_5 | pick_rank_pct |
|---|---|---|---|---|---|---|---|
| sh_r1_eta2 | 7.082 | 6 | 8 | 0.000 | 1.136 | 0.000 | 1.338 |
| sh_r1_eta3 | 6.329 | 4 | 19 | 0.001 | 1.969 | 0.000 | 3.344 |
| sh_r2_eta2 | 12.148 | 5 | 11 | 0.000 | 1.136 | 0.000 | 1.338 |
| sh_r2_eta3 | 10.792 | 4 | 19 | 0.000 | 1.136 | 0.000 | 1.338 |
| sh_r3_eta2 | 16.002 | 4 | 7 | 0.000 | 1.136 | 0.000 | 1.338 |
| sh_r3_eta3 | 14.050 | 3 | 14 | 0.000 | 1.136 | 0.000 | 1.338 |

### pems04: proxy as a filter, then brief training on the top half

| evaluator | gpu_hours | top10_in_bottom_half | top10_total | regret_top1 | regret_top1_sigma | regret_best_of_5 |
|---|---|---|---|---|---|---|
| zico_half_then_k1 | 1.288 | 0 | 30 | 0.005 | 12.716 | 0.003 |
| zico_half_then_k3 | 3.619 | 0 | 30 | 0.005 | 12.716 | 0.000 |
| zico_half_then_k5 | 5.955 | 0 | 30 | 0.001 | 1.969 | 0.000 |
| swap_half_then_k1 | 1.326 | 10 | 30 | 0.008 | 20.612 | 0.003 |
| swap_half_then_k3 | 3.788 | 10 | 30 | 0.008 | 20.612 | 0.001 |
| swap_half_then_k5 | 6.258 | 10 | 30 | 0.001 | 1.969 | 0.000 |
| zico_sizectrl_half_then_k1 | 1.288 | 2 | 30 | 0.007 | 16.495 | 0.006 |
| zico_sizectrl_half_then_k3 | 3.614 | 2 | 30 | 0.005 | 12.716 | 0.000 |
| zico_sizectrl_half_then_k5 | 5.939 | 2 | 30 | 0.001 | 1.969 | 0.000 |
| params_half_then_k1 | 1.223 | 11 | 30 | 0.005 | 13.011 | 0.003 |
| params_half_then_k3 | 3.461 | 11 | 30 | 0.005 | 12.716 | 0.004 |
| params_half_then_k5 | 5.706 | 11 | 30 | 0.001 | 1.969 | 0.000 |

### pems08: floors, proxies, brief training, ceiling

| evaluator | kind | gpu_hours | regret_top1 | regret_top1_sigma | regret_best_of_5 | regret_best_of_5_sigma | pick_rank_pct | rho | rho_partial | rho_within_head |
|---|---|---|---|---|---|---|---|---|---|---|
| random | floor | 0.000 | 0.006 | 7.467 | 0.003 | 2.969 | 50.000 | 0.000 | 0.000 | 0.000 |
| params | floor | 0.000 | 0.006 | 6.932 | 0.000 | 0.355 | 51.007 | 0.063 | -0.030 | 0.160 |
| flops | floor | 0.000 | 0.008 | 9.696 | 0.006 | 6.988 | 69.799 | 0.077 | 0.055 | 0.256 |
| zico | zero-cost proxy | 0.000 | 0.000 | 0.355 | 0.000 | 0.355 | 0.671 | 0.296 | 0.354 | 0.470 |
| zico_sizectrl | zero-cost proxy | 0.000 | 0.000 | 0.355 | 0.000 | 0.355 | 0.671 | 0.309 | 0.307 | 0.455 |
| swap | zero-cost proxy | 0.000 | 0.006 | 6.988 | 0.003 | 3.355 | 52.349 | 0.091 | 0.078 | 0.217 |
| swap_reg | zero-cost proxy | 0.000 | 0.004 | 4.280 | 0.002 | 2.090 | 26.174 | 0.037 | 0.026 | 0.069 |
| nwot | zero-cost proxy | 0.000 | 0.005 | 5.496 | 0.002 | 2.557 | 36.242 | 0.132 | 0.118 | 0.267 |
| synflow_all | zero-cost proxy | 0.000 | 0.005 | 5.930 | 0.005 | 5.930 | 40.940 | 0.010 | 0.008 | 0.084 |
| snip_all | zero-cost proxy | 0.000 | 0.012 | 14.133 | 0.009 | 9.877 | 96.644 | -0.343 | -0.402 | -0.096 |
| grasp_all | zero-cost proxy | 0.000 | 0.045 | 51.936 | 0.004 | 4.590 | 100.000 | 0.425 | 0.452 | 0.167 |
| grad_norm_all | zero-cost proxy | 0.000 | 0.012 | 14.133 | 0.009 | 9.877 | 96.644 | -0.371 | -0.427 | -0.090 |
| fisher | zero-cost proxy | 0.000 | 0.012 | 14.133 | 0.004 | 4.735 | 96.644 | -0.419 | -0.442 | -0.147 |
| jacov | zero-cost proxy | 0.000 | 0.010 | 11.724 | 0.006 | 7.019 | 87.919 | -0.180 | -0.194 | -0.297 |
| zen | zero-cost proxy | 0.000 | 0.006 | 6.932 | 0.000 | 0.355 | 51.007 | -0.016 | -0.097 | 0.040 |
| l2_norm_all | zero-cost proxy | 0.000 | 0.000 | 0.355 | 0.000 | 0.355 | 0.671 | 0.260 | 0.349 | 0.396 |
| plain_all | zero-cost proxy | 0.000 | 0.012 | 14.133 | 0.010 | 11.682 | 96.644 | -0.445 | -0.461 | -0.095 |
| early_val_k1 | brief training | 1.553 | 0.010 | 11.682 | 0.008 | 9.793 | 87.248 | 0.064 | 0.065 | 0.359 |
| early_val_k2 | brief training | 2.455 | 0.006 | 6.697 | 0.005 | 6.300 | 46.309 | 0.245 | 0.250 | 0.490 |
| early_val_k3 | brief training | 3.357 | 0.003 | 3.001 | 0.003 | 3.001 | 14.765 | 0.356 | 0.356 | 0.528 |
| early_val_k4 | brief training | 4.259 | 0.002 | 2.323 | 0.000 | 0.000 | 7.383 | 0.650 | 0.659 | 0.696 |
| early_val_k5 | brief training | 5.164 | 0.003 | 3.474 | 0.002 | 1.795 | 20.805 | 0.684 | 0.685 | 0.725 |
| early_val_k6 | brief training | 6.076 | 0.002 | 1.795 | 0.000 | 0.000 | 4.698 | 0.799 | 0.801 | 0.774 |
| early_val_k8 | brief training | 7.889 | 0.003 | 3.474 | 0.000 | 0.501 | 20.805 | 0.881 | 0.882 | 0.819 |
| early_val_k10 | brief training | 9.708 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.914 | 0.914 | 0.870 |
| early_val_k15 | brief training | 14.181 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.948 | 0.947 | 0.910 |
| full_training | ceiling | 18.525 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |

### pems08: successive halving on the logged curves

| evaluator | gpu_hours | rounds | dropped_top10_round1 | regret_top1 | regret_top1_sigma | regret_best_of_5 | pick_rank_pct |
|---|---|---|---|---|---|---|---|
| sh_r1_eta2 | 3.612 | 6 | 6 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r1_eta3 | 3.140 | 4 | 9 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r2_eta2 | 5.575 | 5 | 5 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r2_eta3 | 5.135 | 4 | 7 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r3_eta2 | 7.349 | 4 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r3_eta3 | 6.490 | 3 | 4 | 0.000 | 0.000 | 0.000 | 0.000 |

### pems08: proxy as a filter, then brief training on the top half

| evaluator | gpu_hours | top10_in_bottom_half | top10_total | regret_top1 | regret_top1_sigma | regret_best_of_5 |
|---|---|---|---|---|---|---|
| zico_half_then_k1 | 0.968 | 4 | 15 | 0.010 | 11.682 | 0.006 |
| zico_half_then_k3 | 2.005 | 4 | 15 | 0.003 | 3.001 | 0.002 |
| zico_half_then_k5 | 3.044 | 4 | 15 | 0.003 | 3.474 | 0.002 |
| swap_half_then_k1 | 0.758 | 8 | 15 | 0.010 | 11.682 | 0.008 |
| swap_half_then_k3 | 1.789 | 8 | 15 | 0.003 | 3.001 | 0.003 |
| swap_half_then_k5 | 2.819 | 8 | 15 | 0.002 | 1.795 | 0.001 |
| zico_sizectrl_half_then_k1 | 0.905 | 4 | 15 | 0.010 | 11.682 | 0.005 |
| zico_sizectrl_half_then_k3 | 1.919 | 4 | 15 | 0.005 | 5.930 | 0.002 |
| zico_sizectrl_half_then_k5 | 2.935 | 4 | 15 | 0.003 | 3.474 | 0.002 |
| params_half_then_k1 | 0.770 | 4 | 15 | 0.010 | 11.682 | 0.008 |
| params_half_then_k3 | 1.759 | 4 | 15 | 0.003 | 3.001 | 0.002 |
| params_half_then_k5 | 2.749 | 4 | 15 | 0.002 | 1.795 | 0.000 |

### metrla: floors, proxies, brief training, ceiling

| evaluator | kind | gpu_hours | regret_top1 | regret_top1_sigma | regret_best_of_5 | regret_best_of_5_sigma | pick_rank_pct | rho | rho_partial | rho_within_head |
|---|---|---|---|---|---|---|---|---|---|---|
| random | floor | 0.000 | 0.030 | 5.089 | 0.010 | 1.658 | 50.000 | 0.000 | 0.000 | 0.000 |
| params | floor | 0.000 | 0.020 | 3.349 | 0.011 | 1.768 | 40.940 | -0.112 | 0.008 | -0.116 |
| flops | floor | 0.000 | 0.010 | 1.643 | 0.010 | 1.643 | 10.067 | -0.025 | -0.005 | 0.074 |
| zico | zero-cost proxy | 0.000 | 0.019 | 3.280 | 0.011 | 1.768 | 39.597 | -0.087 | -0.008 | -0.181 |
| zico_sizectrl | zero-cost proxy | 0.000 | 0.011 | 1.768 | 0.011 | 1.768 | 13.423 | -0.013 | -0.005 | -0.145 |
| swap | zero-cost proxy | 0.000 | 0.015 | 2.475 | 0.013 | 2.110 | 26.174 | -0.103 | -0.040 | -0.033 |
| swap_reg | zero-cost proxy | 0.000 | 0.049 | 8.282 | 0.010 | 1.643 | 76.510 | 0.023 | 0.046 | 0.021 |
| nwot | zero-cost proxy | 0.000 | 0.015 | 2.475 | 0.005 | 0.797 | 26.174 | -0.057 | -0.037 | 0.007 |
| synflow_all | zero-cost proxy | 0.000 | 0.011 | 1.768 | 0.010 | 1.643 | 13.423 | -0.145 | -0.134 | 0.032 |
| snip_all | zero-cost proxy | 0.000 | 0.067 | 11.259 | 0.049 | 8.282 | 99.329 | -0.487 | -0.483 | -0.233 |
| grasp_all | zero-cost proxy | 0.000 | 0.025 | 4.191 | 0.011 | 1.768 | 57.047 | 0.532 | 0.525 | 0.168 |
| grad_norm_all | zero-cost proxy | 0.000 | 0.067 | 11.259 | 0.049 | 8.282 | 99.329 | -0.540 | -0.526 | -0.240 |
| fisher | zero-cost proxy | 0.000 | 0.054 | 9.139 | 0.049 | 8.282 | 85.235 | -0.590 | -0.586 | -0.238 |
| jacov | zero-cost proxy | 0.000 | 0.018 | 2.972 | 0.014 | 2.424 | 36.242 | -0.012 | -0.005 | -0.229 |
| zen | zero-cost proxy | 0.000 | 0.020 | 3.349 | 0.019 | 3.280 | 40.940 | -0.120 | -0.060 | -0.119 |
| l2_norm_all | zero-cost proxy | 0.000 | 0.019 | 3.280 | 0.011 | 1.768 | 39.597 | -0.092 | 0.019 | -0.154 |
| plain_all | zero-cost proxy | 0.000 | 0.054 | 9.139 | 0.014 | 2.296 | 85.235 | -0.538 | -0.526 | -0.179 |
| early_val_k1 | brief training | 1.582 | 0.004 | 0.593 | 0.004 | 0.593 | 4.698 | 0.811 | 0.814 | 0.077 |
| early_val_k2 | brief training | 2.982 | 0.004 | 0.593 | 0.003 | 0.526 | 4.698 | 0.868 | 0.870 | 0.333 |
| early_val_k3 | brief training | 4.385 | 0.001 | 0.208 | 0.001 | 0.181 | 2.013 | 0.882 | 0.884 | 0.430 |
| early_val_k4 | brief training | 5.782 | 0.013 | 2.259 | 0.003 | 0.540 | 20.805 | 0.859 | 0.862 | 0.344 |
| early_val_k5 | brief training | 7.184 | 0.004 | 0.746 | 0.003 | 0.540 | 6.711 | 0.833 | 0.835 | 0.222 |
| early_val_k6 | brief training | 8.586 | 0.004 | 0.593 | 0.002 | 0.260 | 4.698 | 0.829 | 0.833 | 0.284 |
| early_val_k8 | brief training | 11.385 | 0.002 | 0.260 | 0.002 | 0.260 | 2.685 | 0.821 | 0.820 | 0.280 |
| early_val_k10 | brief training | 13.251 | 0.013 | 2.259 | 0.004 | 0.593 | 20.805 | 0.825 | 0.827 | 0.325 |
| early_val_k15 | brief training | 16.068 | 0.004 | 0.593 | 0.004 | 0.593 | 4.698 | 0.818 | 0.818 | 0.323 |
| full_training | ceiling | 17.615 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |

### metrla: successive halving on the logged curves

| evaluator | gpu_hours | rounds | dropped_top10_round1 | regret_top1 | regret_top1_sigma | regret_best_of_5 | pick_rank_pct |
|---|---|---|---|---|---|---|---|
| sh_r1_eta2 | 4.140 | 6 | 0 | 0.004 | 0.593 | 0.004 | 4.698 |
| sh_r1_eta3 | 3.724 | 4 | 1 | 0.004 | 0.593 | 0.004 | 4.698 |
| sh_r2_eta2 | 6.709 | 5 | 0 | 0.004 | 0.593 | 0.004 | 4.698 |
| sh_r2_eta3 | 6.027 | 4 | 1 | 0.004 | 0.593 | 0.004 | 4.698 |
| sh_r3_eta2 | 8.683 | 4 | 0 | 0.004 | 0.593 | 0.004 | 4.698 |
| sh_r3_eta3 | 8.019 | 3 | 0 | 0.004 | 0.593 | 0.004 | 4.698 |

### metrla: proxy as a filter, then brief training on the top half

| evaluator | gpu_hours | top10_in_bottom_half | top10_total | regret_top1 | regret_top1_sigma | regret_best_of_5 |
|---|---|---|---|---|---|---|
| zico_half_then_k1 | 0.905 | 9 | 15 | 0.025 | 4.192 | 0.001 |
| zico_half_then_k3 | 2.484 | 9 | 15 | 0.001 | 0.181 | 0.001 |
| zico_half_then_k5 | 4.068 | 9 | 15 | 0.004 | 0.746 | 0.004 |
| swap_half_then_k1 | 0.905 | 7 | 15 | 0.013 | 2.110 | 0.001 |
| swap_half_then_k3 | 2.519 | 7 | 15 | 0.001 | 0.181 | 0.001 |
| swap_half_then_k5 | 4.128 | 7 | 15 | 0.004 | 0.746 | 0.003 |
| zico_sizectrl_half_then_k1 | 0.900 | 7 | 15 | 0.004 | 0.593 | 0.004 |
| zico_sizectrl_half_then_k3 | 2.464 | 7 | 15 | 0.001 | 0.208 | 0.001 |
| zico_sizectrl_half_then_k5 | 4.030 | 7 | 15 | 0.004 | 0.746 | 0.004 |
| params_half_then_k1 | 0.875 | 8 | 15 | 0.025 | 4.192 | 0.013 |
| params_half_then_k3 | 2.421 | 8 | 15 | 0.001 | 0.181 | 0.001 |
| params_half_then_k5 | 3.964 | 8 | 15 | 0.004 | 0.746 | 0.003 |

### Transfer: the top-5 of a source city, scored at the target city

rho_cities = Spearman of the labels of the shared architectures between the two cities.

| source | target_city | n_shared | regret_top1 | regret_best_of_5 | top1_rank_pct | top5_mean_rank_pct | rho_cities |
|---|---|---|---|---|---|---|---|
| pems04 | metrla | 50 | 0.011 | 0.000 | 22.449 | 19.184 | 0.468 |
| metrla | pems04 | 50 | 0.000 | 0.000 | 2.041 | 35.102 | 0.468 |
