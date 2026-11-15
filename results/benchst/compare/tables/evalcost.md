# evalcost: cost against quality of every cheap evaluator, target = test_mae (seed 0)

Regret = the evaluator's pick minus the best architecture of the set, in MAE units of the normalised target and in units of sigma_seed. sigma_seed is provisional: the std over seeds 0 to 2 of the few architectures that have three seeds (count per city below). gpu_hours are the logged seconds on the cluster and GPU unit of the root (listed per city below); gpu_hours_ref = gpu_hours / cost_ratio is the same cost on the reference unit, one H100 3g.40gb slice of Nibi. A zero-cost proxy is recorded at 0 h (seconds per architecture). rho is Spearman with -MAE; partial = after rank regression on log params; within head = n-weighted mean of rho inside each loss head.

- metrla: N = 150, max epochs 20, sigma_seed = 0.0035 over 5 architectures; trained on nibi (H100 3g.40gb slice), cost_ratio 1.00 (no COST.json: reference unit assumed)
- pems04: N = 150, max epochs 20, sigma_seed = 0.0003 over 5 architectures; trained on nibi (H100 3g.40gb slice), cost_ratio 1.00 (no COST.json: reference unit assumed)
- chengdu: N = 150, max epochs 20, sigma_seed = 0.0018 over 5 architectures; trained on rorqual (H100 3g.40gb slice), cost_ratio 1.01
- shenzhen: N = 150, max epochs 20, sigma_seed = 0.0014 over 5 architectures; trained on fir (H100 3g.40gb slice), cost_ratio 0.94

### metrla: floors, proxies, brief training, ceiling

| evaluator | kind | gpu_hours | gpu_hours_ref | regret_top1 | regret_top1_sigma | regret_best_of_5 | regret_best_of_5_sigma | pick_rank_pct | rho | rho_partial | rho_within_head |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random | floor | 0.000 | 0.000 | 0.013 | 3.641 | 0.005 | 1.314 | 50.000 | 0.000 | 0.000 | 0.000 |
| params | floor | 0.000 | 0.000 | 0.006 | 1.626 | 0.006 | 1.626 | 21.477 | 0.035 | 0.049 | 0.161 |
| flops | floor | 0.000 | 0.000 | 0.010 | 2.799 | 0.009 | 2.445 | 51.007 | -0.120 | -0.132 | -0.130 |
| zico | zero-cost proxy | 0.000 | 0.000 | 0.006 | 1.795 | 0.006 | 1.795 | 26.174 | 0.224 | 0.279 | 0.395 |
| zico_sizectrl | zero-cost proxy | 0.000 | 0.000 | 0.021 | 5.884 | 0.006 | 1.795 | 79.195 | 0.258 | 0.259 | 0.376 |
| swap | zero-cost proxy | 0.000 | 0.000 | 0.002 | 0.666 | 0.002 | 0.638 | 4.698 | -0.088 | -0.144 | -0.020 |
| swap_reg | zero-cost proxy | 0.000 | 0.000 | 0.025 | 7.085 | 0.010 | 2.799 | 94.631 | 0.036 | 0.044 | -0.036 |
| nwot | zero-cost proxy | 0.000 | 0.000 | 0.002 | 0.666 | 0.002 | 0.666 | 4.698 | -0.090 | -0.124 | -0.056 |
| synflow_all | zero-cost proxy | 0.000 | 0.000 | 0.008 | 2.362 | 0.008 | 2.362 | 39.597 | -0.208 | -0.210 | -0.124 |
| snip_all | zero-cost proxy | 0.000 | 0.000 | 0.021 | 5.914 | 0.019 | 5.448 | 79.866 | -0.429 | -0.449 | -0.023 |
| grasp_all | zero-cost proxy | 0.000 | 0.000 | 0.010 | 2.862 | 0.007 | 2.072 | 52.349 | 0.484 | 0.488 | 0.024 |
| grad_norm_all | zero-cost proxy | 0.000 | 0.000 | 0.021 | 5.914 | 0.019 | 5.448 | 79.866 | -0.475 | -0.495 | -0.047 |
| fisher | zero-cost proxy | 0.000 | 0.000 | 0.030 | 8.502 | 0.021 | 5.914 | 98.658 | -0.542 | -0.558 | -0.074 |
| jacov | zero-cost proxy | 0.000 | 0.000 | 0.004 | 1.174 | 0.004 | 1.174 | 10.067 | 0.104 | 0.102 | 0.026 |
| zen | zero-cost proxy | 0.000 | 0.000 | 0.006 | 1.626 | 0.006 | 1.626 | 21.477 | -0.011 | -0.091 | 0.080 |
| l2_norm_all | zero-cost proxy | 0.000 | 0.000 | 0.006 | 1.795 | 0.004 | 1.033 | 26.174 | 0.136 | 0.194 | 0.295 |
| plain_all | zero-cost proxy | 0.000 | 0.000 | 0.030 | 8.502 | 0.005 | 1.293 | 98.658 | -0.424 | -0.437 | 0.008 |
| zico_t | zero-cost proxy | 0.000 | 0.000 | 0.008 | 2.362 | 0.006 | 1.795 | 39.597 | 0.239 | 0.289 | 0.404 |
| zico_s | zero-cost proxy | 0.000 | 0.000 | 0.015 | 4.324 | 0.009 | 2.535 | 61.745 | -0.048 | -0.037 | -0.107 |
| glass | zero-cost proxy | 0.000 | 0.000 | 0.006 | 1.795 | 0.006 | 1.795 | 26.174 | 0.182 | 0.223 | 0.390 |
| glass_t | zero-cost proxy | 0.000 | 0.000 | 0.008 | 2.362 | 0.006 | 1.795 | 39.597 | 0.194 | 0.230 | 0.406 |
| glass_s | zero-cost proxy | 0.000 | 0.000 | 0.015 | 4.324 | 0.009 | 2.535 | 61.745 | -0.059 | -0.047 | -0.108 |
| nwot_per_layer | zero-cost proxy | 0.000 | 0.000 | 0.016 | 4.661 | 0.006 | 1.582 | 63.087 | -0.188 | -0.207 | -0.278 |
| early_val_k1 | brief training | 2.213 | 2.213 | 0.007 | 1.922 | 0.001 | 0.335 | 29.530 | 0.581 | 0.581 | 0.446 |
| early_val_k2 | brief training | 4.214 | 4.214 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.843 | 0.845 | 0.557 |
| early_val_k3 | brief training | 6.221 | 6.221 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.878 | 0.880 | 0.591 |
| early_val_k4 | brief training | 8.235 | 8.235 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.925 | 0.927 | 0.680 |
| early_val_k5 | brief training | 10.249 | 10.249 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.926 | 0.926 | 0.697 |
| early_val_k6 | brief training | 12.256 | 12.256 | 0.002 | 0.656 | 0.000 | 0.000 | 4.027 | 0.924 | 0.923 | 0.727 |
| early_val_k8 | brief training | 16.251 | 16.251 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.951 | 0.951 | 0.805 |
| early_val_k10 | brief training | 20.014 | 20.014 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.961 | 0.962 | 0.844 |
| early_val_k15 | brief training | 27.489 | 27.489 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.974 | 0.974 | 0.907 |
| full_training | ceiling | 32.863 | 32.863 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |

### metrla: successive halving on the logged curves

| evaluator | gpu_hours | gpu_hours_ref | rounds | dropped_top10_round1 | regret_top1 | regret_top1_sigma | regret_best_of_5 | pick_rank_pct |
|---|---|---|---|---|---|---|---|---|
| sh_r1_eta2 | 6.446 | 6.446 | 6 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r1_eta3 | 5.777 | 5.777 | 4 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r2_eta2 | 10.676 | 10.676 | 5 | 1 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r2_eta3 | 9.848 | 9.848 | 4 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r3_eta2 | 14.053 | 14.053 | 4 | 0 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r3_eta3 | 12.702 | 12.702 | 3 | 1 | 0.000 | 0.000 | 0.000 | 0.000 |

### metrla: proxy as a filter, then brief training on the top half

| evaluator | gpu_hours | gpu_hours_ref | top10_in_bottom_half | top10_total | regret_top1 | regret_top1_sigma | regret_best_of_5 |
|---|---|---|---|---|---|---|---|
| zico_half_then_k1 | 1.251 | 1.251 | 5 | 15 | 0.007 | 1.922 | 0.001 |
| zico_half_then_k3 | 3.502 | 3.502 | 5 | 15 | 0.000 | 0.000 | 0.000 |
| zico_half_then_k5 | 5.775 | 5.775 | 5 | 15 | 0.000 | 0.000 | 0.000 |
| swap_half_then_k1 | 1.286 | 1.286 | 9 | 15 | 0.007 | 1.922 | 0.002 |
| swap_half_then_k3 | 3.661 | 3.661 | 9 | 15 | 0.004 | 1.038 | 0.002 |
| swap_half_then_k5 | 6.056 | 6.056 | 9 | 15 | 0.004 | 1.038 | 0.002 |
| zico_sizectrl_half_then_k1 | 1.222 | 1.222 | 2 | 15 | 0.007 | 1.922 | 0.001 |
| zico_sizectrl_half_then_k3 | 3.416 | 3.416 | 2 | 15 | 0.000 | 0.000 | 0.000 |
| zico_sizectrl_half_then_k5 | 5.630 | 5.630 | 2 | 15 | 0.000 | 0.000 | 0.000 |
| params_half_then_k1 | 1.235 | 1.235 | 6 | 15 | 0.002 | 0.560 | 0.001 |
| params_half_then_k3 | 3.485 | 3.485 | 6 | 15 | 0.000 | 0.000 | 0.000 |
| params_half_then_k5 | 5.752 | 5.752 | 6 | 15 | 0.000 | 0.000 | 0.000 |

### pems04: floors, proxies, brief training, ceiling

| evaluator | kind | gpu_hours | gpu_hours_ref | regret_top1 | regret_top1_sigma | regret_best_of_5 | regret_best_of_5_sigma | pick_rank_pct | rho | rho_partial | rho_within_head |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random | floor | 0.000 | 0.000 | 0.004 | 16.357 | 0.002 | 7.209 | 50.000 | 0.000 | 0.000 | 0.000 |
| params | floor | 0.000 | 0.000 | 0.001 | 4.569 | 0.000 | 1.795 | 8.054 | 0.244 | -0.018 | 0.324 |
| flops | floor | 0.000 | 0.000 | 0.005 | 18.122 | 0.003 | 11.650 | 59.732 | 0.182 | 0.133 | 0.204 |
| zico | zero-cost proxy | 0.000 | 0.000 | 0.000 | 1.795 | 0.000 | 1.795 | 2.013 | 0.594 | 0.602 | 0.685 |
| zico_sizectrl | zero-cost proxy | 0.000 | 0.000 | 0.001 | 3.918 | 0.000 | 1.795 | 6.040 | 0.569 | 0.581 | 0.606 |
| swap | zero-cost proxy | 0.000 | 0.000 | 0.003 | 10.003 | 0.001 | 4.703 | 20.805 | 0.111 | -0.053 | 0.193 |
| swap_reg | zero-cost proxy | 0.000 | 0.000 | 0.009 | 34.221 | 0.004 | 14.061 | 98.658 | 0.071 | 0.038 | 0.070 |
| nwot | zero-cost proxy | 0.000 | 0.000 | 0.004 | 14.433 | 0.001 | 4.703 | 42.282 | 0.203 | 0.113 | 0.254 |
| synflow_all | zero-cost proxy | 0.000 | 0.000 | 0.001 | 3.918 | 0.001 | 3.918 | 6.040 | 0.108 | 0.094 | 0.160 |
| snip_all | zero-cost proxy | 0.000 | 0.000 | 0.006 | 22.620 | 0.005 | 18.502 | 81.879 | -0.233 | -0.307 | -0.142 |
| grasp_all | zero-cost proxy | 0.000 | 0.000 | 0.007 | 26.668 | 0.004 | 12.957 | 91.275 | 0.268 | 0.304 | 0.194 |
| grad_norm_all | zero-cost proxy | 0.000 | 0.000 | 0.006 | 22.620 | 0.005 | 18.502 | 81.879 | -0.234 | -0.313 | -0.106 |
| fisher | zero-cost proxy | 0.000 | 0.000 | 0.005 | 18.502 | 0.005 | 18.502 | 61.745 | -0.222 | -0.282 | -0.081 |
| jacov | zero-cost proxy | 0.000 | 0.000 | 0.008 | 29.457 | 0.005 | 19.431 | 95.302 | -0.182 | -0.197 | -0.193 |
| zen | zero-cost proxy | 0.000 | 0.000 | 0.001 | 4.569 | 0.000 | 1.795 | 8.054 | 0.120 | -0.194 | 0.177 |
| l2_norm_all | zero-cost proxy | 0.000 | 0.000 | 0.000 | 1.795 | 0.000 | 1.795 | 2.013 | 0.547 | 0.584 | 0.627 |
| plain_all | zero-cost proxy | 0.000 | 0.000 | 0.005 | 18.502 | 0.005 | 17.139 | 61.745 | -0.186 | -0.239 | 0.065 |
| zico_t | zero-cost proxy | 0.000 | 0.000 | 0.001 | 3.918 | 0.000 | 1.795 | 6.040 | 0.565 | 0.552 | 0.654 |
| zico_s | zero-cost proxy | 0.000 | 0.000 | 0.005 | 17.242 | 0.003 | 11.650 | 55.705 | 0.231 | 0.244 | 0.221 |
| glass | zero-cost proxy | 0.000 | 0.000 | 0.000 | 1.795 | 0.000 | 1.795 | 2.013 | 0.588 | 0.595 | 0.686 |
| glass_t | zero-cost proxy | 0.000 | 0.000 | 0.001 | 3.918 | 0.000 | 1.795 | 6.040 | 0.560 | 0.547 | 0.657 |
| glass_s | zero-cost proxy | 0.000 | 0.000 | 0.005 | 17.242 | 0.003 | 11.650 | 55.705 | 0.231 | 0.244 | 0.219 |
| nwot_per_layer | zero-cost proxy | 0.000 | 0.000 | 0.008 | 28.955 | 0.004 | 13.564 | 93.960 | -0.422 | -0.348 | -0.463 |
| early_val_k1 | brief training | 1.677 | 1.677 | 0.007 | 24.317 | 0.003 | 12.722 | 85.906 | 0.130 | 0.119 | 0.312 |
| early_val_k2 | brief training | 3.088 | 3.088 | 0.005 | 18.963 | 0.002 | 7.652 | 63.087 | 0.156 | 0.155 | 0.309 |
| early_val_k3 | brief training | 4.499 | 4.499 | 0.001 | 4.625 | 0.001 | 4.625 | 8.725 | 0.304 | 0.310 | 0.428 |
| early_val_k4 | brief training | 5.915 | 5.915 | 0.002 | 7.828 | 0.000 | 0.000 | 14.094 | 0.468 | 0.471 | 0.591 |
| early_val_k5 | brief training | 7.329 | 7.329 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.582 | 0.586 | 0.676 |
| early_val_k6 | brief training | 8.746 | 8.746 | 0.001 | 4.625 | 0.000 | 0.000 | 8.725 | 0.657 | 0.649 | 0.753 |
| early_val_k8 | brief training | 11.584 | 11.584 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.799 | 0.793 | 0.833 |
| early_val_k10 | brief training | 14.427 | 14.427 | 0.000 | 1.359 | 0.000 | 0.000 | 1.342 | 0.869 | 0.867 | 0.888 |
| early_val_k15 | brief training | 21.522 | 21.522 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.945 | 0.941 | 0.943 |
| full_training | ceiling | 28.650 | 28.650 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |

### pems04: successive halving on the logged curves

| evaluator | gpu_hours | gpu_hours_ref | rounds | dropped_top10_round1 | regret_top1 | regret_top1_sigma | regret_best_of_5 | pick_rank_pct |
|---|---|---|---|---|---|---|---|---|
| sh_r1_eta2 | 4.863 | 4.863 | 6 | 3 | 0.001 | 2.291 | 0.001 | 2.685 |
| sh_r1_eta3 | 4.266 | 4.266 | 4 | 8 | 0.000 | 1.312 | 0.000 | 0.671 |
| sh_r2_eta2 | 8.099 | 8.099 | 5 | 4 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r2_eta3 | 7.343 | 7.343 | 4 | 9 | 0.000 | 1.359 | 0.000 | 1.342 |
| sh_r3_eta2 | 10.676 | 10.676 | 4 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r3_eta3 | 9.486 | 9.486 | 3 | 6 | 0.000 | 0.000 | 0.000 | 0.000 |

### pems04: proxy as a filter, then brief training on the top half

| evaluator | gpu_hours | gpu_hours_ref | top10_in_bottom_half | top10_total | regret_top1 | regret_top1_sigma | regret_best_of_5 |
|---|---|---|---|---|---|---|---|
| zico_half_then_k1 | 0.907 | 0.907 | 2 | 15 | 0.003 | 12.722 | 0.002 |
| zico_half_then_k3 | 2.424 | 2.424 | 2 | 15 | 0.001 | 4.625 | 0.001 |
| zico_half_then_k5 | 3.943 | 3.943 | 2 | 15 | 0.000 | 0.000 | 0.000 |
| swap_half_then_k1 | 0.956 | 0.956 | 6 | 15 | 0.003 | 12.722 | 0.003 |
| swap_half_then_k3 | 2.623 | 2.623 | 6 | 15 | 0.001 | 4.625 | 0.001 |
| swap_half_then_k5 | 4.304 | 4.304 | 6 | 15 | 0.000 | 0.000 | 0.000 |
| zico_sizectrl_half_then_k1 | 0.908 | 0.908 | 0 | 15 | 0.007 | 24.317 | 0.003 |
| zico_sizectrl_half_then_k3 | 2.387 | 2.387 | 0 | 15 | 0.001 | 4.625 | 0.001 |
| zico_sizectrl_half_then_k5 | 3.871 | 3.871 | 0 | 15 | 0.000 | 0.000 | 0.000 |
| params_half_then_k1 | 0.912 | 0.912 | 4 | 15 | 0.003 | 12.722 | 0.003 |
| params_half_then_k3 | 2.461 | 2.461 | 4 | 15 | 0.002 | 7.652 | 0.002 |
| params_half_then_k5 | 4.010 | 4.010 | 4 | 15 | 0.000 | 0.000 | 0.000 |

### chengdu: floors, proxies, brief training, ceiling

| evaluator | kind | gpu_hours | gpu_hours_ref | regret_top1 | regret_top1_sigma | regret_best_of_5 | regret_best_of_5_sigma | pick_rank_pct | rho | rho_partial | rho_within_head |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random | floor | 0.000 | 0.000 | 0.010 | 5.718 | 0.005 | 2.686 | 50.000 | 0.000 | 0.000 | 0.000 |
| params | floor | 0.000 | 0.000 | 0.013 | 7.202 | 0.004 | 2.144 | 74.497 | 0.227 | 0.066 | 0.259 |
| flops | floor | 0.000 | 0.000 | 0.011 | 6.364 | 0.010 | 5.308 | 65.101 | -0.306 | -0.355 | -0.302 |
| zico | zero-cost proxy | 0.000 | 0.000 | 0.013 | 7.094 | 0.004 | 2.144 | 72.483 | 0.467 | 0.434 | 0.532 |
| zico_sizectrl | zero-cost proxy | 0.000 | 0.000 | 0.014 | 7.826 | 0.004 | 2.144 | 79.195 | 0.382 | 0.392 | 0.435 |
| swap | zero-cost proxy | 0.000 | 0.000 | 0.011 | 6.364 | 0.005 | 2.949 | 65.101 | -0.134 | -0.364 | -0.093 |
| swap_reg | zero-cost proxy | 0.000 | 0.000 | 0.021 | 11.634 | 0.004 | 2.043 | 97.987 | -0.027 | -0.070 | -0.020 |
| nwot | zero-cost proxy | 0.000 | 0.000 | 0.013 | 7.306 | 0.009 | 4.839 | 76.510 | -0.298 | -0.406 | -0.280 |
| synflow_all | zero-cost proxy | 0.000 | 0.000 | 0.004 | 2.144 | 0.004 | 2.144 | 8.725 | 0.043 | 0.022 | 0.129 |
| snip_all | zero-cost proxy | 0.000 | 0.000 | 0.005 | 2.975 | 0.005 | 2.975 | 15.436 | -0.113 | -0.169 | 0.026 |
| grasp_all | zero-cost proxy | 0.000 | 0.000 | 0.011 | 6.144 | 0.004 | 2.026 | 61.745 | 0.199 | 0.230 | 0.023 |
| grad_norm_all | zero-cost proxy | 0.000 | 0.000 | 0.005 | 2.975 | 0.005 | 2.975 | 15.436 | -0.128 | -0.187 | 0.071 |
| fisher | zero-cost proxy | 0.000 | 0.000 | 0.010 | 5.783 | 0.005 | 2.975 | 55.705 | -0.101 | -0.147 | 0.184 |
| jacov | zero-cost proxy | 0.000 | 0.000 | 0.009 | 4.792 | 0.005 | 2.975 | 36.913 | 0.298 | 0.298 | 0.268 |
| zen | zero-cost proxy | 0.000 | 0.000 | 0.013 | 7.202 | 0.004 | 2.204 | 74.497 | 0.117 | -0.142 | 0.133 |
| l2_norm_all | zero-cost proxy | 0.000 | 0.000 | 0.013 | 7.094 | 0.007 | 3.788 | 72.483 | 0.139 | -0.034 | 0.175 |
| plain_all | zero-cost proxy | 0.000 | 0.000 | 0.010 | 5.783 | 0.008 | 4.585 | 55.705 | -0.062 | -0.112 | 0.237 |
| zico_t | zero-cost proxy | 0.000 | 0.000 | 0.004 | 2.144 | 0.004 | 2.144 | 8.725 | 0.516 | 0.509 | 0.585 |
| zico_s | zero-cost proxy | 0.000 | 0.000 | 0.018 | 9.970 | 0.010 | 5.430 | 92.617 | -0.348 | -0.357 | -0.356 |
| glass | zero-cost proxy | 0.000 | 0.000 | 0.013 | 7.094 | 0.004 | 2.144 | 72.483 | 0.465 | 0.435 | 0.524 |
| glass_t | zero-cost proxy | 0.000 | 0.000 | 0.004 | 2.144 | 0.004 | 2.144 | 8.725 | 0.512 | 0.502 | 0.578 |
| glass_s | zero-cost proxy | 0.000 | 0.000 | 0.018 | 9.970 | 0.010 | 5.430 | 92.617 | -0.344 | -0.353 | -0.355 |
| nwot_per_layer | zero-cost proxy | 0.000 | 0.000 | 0.015 | 8.232 | 0.008 | 4.728 | 81.879 | -0.314 | -0.219 | -0.335 |
| early_val_k1 | brief training | 1.328 | 1.315 | 0.008 | 4.610 | 0.004 | 2.158 | 33.557 | 0.088 | 0.058 | 0.158 |
| early_val_k2 | brief training | 2.607 | 2.581 | 0.004 | 2.158 | 0.003 | 1.669 | 10.067 | 0.296 | 0.262 | 0.398 |
| early_val_k3 | brief training | 3.885 | 3.847 | 0.003 | 1.669 | 0.000 | 0.000 | 6.711 | 0.486 | 0.458 | 0.583 |
| early_val_k4 | brief training | 5.165 | 5.114 | 0.003 | 1.668 | 0.000 | 0.000 | 6.040 | 0.666 | 0.648 | 0.751 |
| early_val_k5 | brief training | 6.441 | 6.377 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.681 | 0.660 | 0.727 |
| early_val_k6 | brief training | 7.719 | 7.642 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.777 | 0.755 | 0.802 |
| early_val_k8 | brief training | 10.274 | 10.172 | 0.002 | 1.071 | 0.000 | 0.000 | 1.342 | 0.863 | 0.852 | 0.858 |
| early_val_k10 | brief training | 12.806 | 12.680 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.896 | 0.890 | 0.882 |
| early_val_k15 | brief training | 18.151 | 17.972 | 0.002 | 1.108 | 0.000 | 0.000 | 2.013 | 0.929 | 0.923 | 0.918 |
| full_training | ceiling | 21.270 | 21.059 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |

### chengdu: successive halving on the logged curves

| evaluator | gpu_hours | gpu_hours_ref | rounds | dropped_top10_round1 | regret_top1 | regret_top1_sigma | regret_best_of_5 | pick_rank_pct |
|---|---|---|---|---|---|---|---|---|
| sh_r1_eta2 | 3.978 | 3.938 | 6 | 6 | 0.002 | 1.071 | 0.000 | 1.342 |
| sh_r1_eta3 | 3.384 | 3.351 | 4 | 9 | 0.003 | 1.668 | 0.000 | 6.040 |
| sh_r2_eta2 | 6.697 | 6.630 | 5 | 5 | 0.003 | 1.668 | 0.000 | 6.040 |
| sh_r2_eta3 | 5.972 | 5.913 | 4 | 7 | 0.003 | 1.668 | 0.000 | 6.040 |
| sh_r3_eta2 | 8.553 | 8.468 | 4 | 1 | 0.003 | 1.668 | 0.000 | 6.040 |
| sh_r3_eta3 | 7.691 | 7.615 | 3 | 5 | 0.003 | 1.668 | 0.000 | 6.040 |

### chengdu: proxy as a filter, then brief training on the top half

| evaluator | gpu_hours | gpu_hours_ref | top10_in_bottom_half | top10_total | regret_top1 | regret_top1_sigma | regret_best_of_5 |
|---|---|---|---|---|---|---|---|
| zico_half_then_k1 | 0.736 | 0.728 | 1 | 15 | 0.004 | 2.158 | 0.004 |
| zico_half_then_k3 | 2.146 | 2.125 | 1 | 15 | 0.003 | 1.669 | 0.003 |
| zico_half_then_k5 | 3.556 | 3.520 | 1 | 15 | 0.004 | 2.158 | 0.002 |
| swap_half_then_k1 | 0.822 | 0.814 | 9 | 15 | 0.004 | 2.158 | 0.004 |
| swap_half_then_k3 | 2.413 | 2.389 | 9 | 15 | 0.004 | 2.158 | 0.003 |
| swap_half_then_k5 | 4.004 | 3.964 | 9 | 15 | 0.004 | 2.158 | 0.003 |
| zico_sizectrl_half_then_k1 | 0.735 | 0.727 | 1 | 15 | 0.008 | 4.610 | 0.004 |
| zico_sizectrl_half_then_k3 | 2.142 | 2.121 | 1 | 15 | 0.003 | 1.669 | 0.000 |
| zico_sizectrl_half_then_k5 | 3.548 | 3.513 | 1 | 15 | 0.000 | 0.000 | 0.000 |
| params_half_then_k1 | 0.722 | 0.715 | 6 | 15 | 0.005 | 2.827 | 0.005 |
| params_half_then_k3 | 2.114 | 2.094 | 6 | 15 | 0.010 | 5.559 | 0.003 |
| params_half_then_k5 | 3.507 | 3.472 | 6 | 15 | 0.002 | 1.108 | 0.002 |

### shenzhen: floors, proxies, brief training, ceiling

| evaluator | kind | gpu_hours | gpu_hours_ref | regret_top1 | regret_top1_sigma | regret_best_of_5 | regret_best_of_5_sigma | pick_rank_pct | rho | rho_partial | rho_within_head |
|---|---|---|---|---|---|---|---|---|---|---|---|
| random | floor | 0.000 | 0.000 | 0.011 | 7.509 | 0.005 | 3.900 | 50.000 | 0.000 | 0.000 | 0.000 |
| params | floor | 0.000 | 0.000 | 0.008 | 5.983 | 0.005 | 3.756 | 33.557 | 0.246 | 0.002 | 0.316 |
| flops | floor | 0.000 | 0.000 | 0.013 | 9.514 | 0.010 | 7.285 | 75.839 | -0.186 | -0.231 | -0.164 |
| zico | zero-cost proxy | 0.000 | 0.000 | 0.005 | 3.756 | 0.004 | 3.103 | 12.081 | 0.465 | 0.392 | 0.596 |
| zico_sizectrl | zero-cost proxy | 0.000 | 0.000 | 0.012 | 8.528 | 0.004 | 3.103 | 66.443 | 0.375 | 0.376 | 0.495 |
| swap | zero-cost proxy | 0.000 | 0.000 | 0.010 | 7.304 | 0.005 | 3.756 | 51.678 | -0.056 | -0.355 | 0.015 |
| swap_reg | zero-cost proxy | 0.000 | 0.000 | 0.021 | 15.225 | 0.011 | 7.665 | 98.658 | 0.029 | -0.005 | 0.014 |
| nwot | zero-cost proxy | 0.000 | 0.000 | 0.010 | 7.304 | 0.008 | 5.476 | 51.678 | -0.155 | -0.264 | -0.117 |
| synflow_all | zero-cost proxy | 0.000 | 0.000 | 0.006 | 4.239 | 0.006 | 4.239 | 16.779 | -0.143 | -0.180 | -0.033 |
| snip_all | zero-cost proxy | 0.000 | 0.000 | 0.010 | 7.069 | 0.009 | 6.726 | 47.651 | -0.239 | -0.310 | 0.008 |
| grasp_all | zero-cost proxy | 0.000 | 0.000 | 0.018 | 12.609 | 0.005 | 3.480 | 93.960 | 0.374 | 0.418 | 0.102 |
| grad_norm_all | zero-cost proxy | 0.000 | 0.000 | 0.016 | 11.080 | 0.009 | 6.726 | 87.248 | -0.291 | -0.365 | 0.036 |
| fisher | zero-cost proxy | 0.000 | 0.000 | 0.016 | 11.080 | 0.010 | 7.069 | 87.248 | -0.276 | -0.347 | 0.104 |
| jacov | zero-cost proxy | 0.000 | 0.000 | 0.009 | 6.353 | 0.008 | 5.983 | 38.255 | 0.163 | 0.165 | 0.118 |
| zen | zero-cost proxy | 0.000 | 0.000 | 0.008 | 5.983 | 0.005 | 3.756 | 33.557 | 0.153 | -0.103 | 0.191 |
| l2_norm_all | zero-cost proxy | 0.000 | 0.000 | 0.005 | 3.756 | 0.005 | 3.756 | 12.081 | 0.249 | 0.099 | 0.331 |
| plain_all | zero-cost proxy | 0.000 | 0.000 | 0.016 | 11.080 | 0.012 | 8.651 | 87.248 | -0.234 | -0.310 | 0.167 |
| zico_t | zero-cost proxy | 0.000 | 0.000 | 0.006 | 4.239 | 0.005 | 3.756 | 16.779 | 0.502 | 0.441 | 0.628 |
| zico_s | zero-cost proxy | 0.000 | 0.000 | 0.013 | 9.553 | 0.010 | 7.285 | 76.510 | -0.190 | -0.189 | -0.194 |
| glass | zero-cost proxy | 0.000 | 0.000 | 0.005 | 3.756 | 0.004 | 3.103 | 12.081 | 0.465 | 0.393 | 0.594 |
| glass_t | zero-cost proxy | 0.000 | 0.000 | 0.006 | 4.239 | 0.005 | 3.756 | 16.779 | 0.497 | 0.434 | 0.628 |
| glass_s | zero-cost proxy | 0.000 | 0.000 | 0.013 | 9.553 | 0.010 | 7.285 | 76.510 | -0.189 | -0.188 | -0.196 |
| nwot_per_layer | zero-cost proxy | 0.000 | 0.000 | 0.016 | 11.694 | 0.010 | 7.411 | 89.262 | -0.334 | -0.233 | -0.378 |
| early_val_k1 | brief training | 1.693 | 1.801 | 0.006 | 4.417 | 0.003 | 2.453 | 17.450 | 0.072 | 0.061 | 0.367 |
| early_val_k2 | brief training | 3.309 | 3.520 | 0.005 | 3.866 | 0.003 | 2.453 | 14.094 | 0.226 | 0.211 | 0.411 |
| early_val_k3 | brief training | 4.922 | 5.236 | 0.005 | 3.866 | 0.003 | 2.453 | 14.094 | 0.419 | 0.399 | 0.579 |
| early_val_k4 | brief training | 6.551 | 6.969 | 0.005 | 3.866 | 0.004 | 2.605 | 14.094 | 0.623 | 0.618 | 0.656 |
| early_val_k5 | brief training | 8.169 | 8.691 | 0.004 | 2.605 | 0.000 | 0.000 | 4.698 | 0.725 | 0.716 | 0.700 |
| early_val_k6 | brief training | 9.789 | 10.414 | 0.004 | 2.605 | 0.000 | 0.000 | 4.698 | 0.817 | 0.805 | 0.785 |
| early_val_k8 | brief training | 13.023 | 13.854 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.897 | 0.889 | 0.859 |
| early_val_k10 | brief training | 16.265 | 17.303 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.909 | 0.904 | 0.866 |
| early_val_k15 | brief training | 23.912 | 25.439 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.934 | 0.930 | 0.912 |
| full_training | ceiling | 30.052 | 31.970 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |

### shenzhen: successive halving on the logged curves

| evaluator | gpu_hours | gpu_hours_ref | rounds | dropped_top10_round1 | regret_top1 | regret_top1_sigma | regret_best_of_5 | pick_rank_pct |
|---|---|---|---|---|---|---|---|---|
| sh_r1_eta2 | 4.984 | 5.302 | 6 | 6 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r1_eta3 | 4.598 | 4.891 | 4 | 7 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r2_eta2 | 8.330 | 8.862 | 5 | 6 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r2_eta3 | 7.358 | 7.827 | 4 | 7 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r3_eta2 | 11.219 | 11.935 | 4 | 5 | 0.000 | 0.000 | 0.000 | 0.000 |
| sh_r3_eta3 | 9.948 | 10.583 | 3 | 6 | 0.000 | 0.000 | 0.000 | 0.000 |

### shenzhen: proxy as a filter, then brief training on the top half

| evaluator | gpu_hours | gpu_hours_ref | top10_in_bottom_half | top10_total | regret_top1 | regret_top1_sigma | regret_best_of_5 |
|---|---|---|---|---|---|---|---|
| zico_half_then_k1 | 0.933 | 0.993 | 2 | 15 | 0.006 | 4.417 | 0.003 |
| zico_half_then_k3 | 2.697 | 2.869 | 2 | 15 | 0.005 | 3.866 | 0.003 |
| zico_half_then_k5 | 4.473 | 4.758 | 2 | 15 | 0.004 | 2.605 | 0.003 |
| swap_half_then_k1 | 1.009 | 1.074 | 7 | 15 | 0.009 | 6.202 | 0.003 |
| swap_half_then_k3 | 2.950 | 3.138 | 7 | 15 | 0.004 | 2.605 | 0.003 |
| swap_half_then_k5 | 4.897 | 5.209 | 7 | 15 | 0.004 | 2.605 | 0.001 |
| zico_sizectrl_half_then_k1 | 0.920 | 0.979 | 1 | 15 | 0.006 | 4.417 | 0.003 |
| zico_sizectrl_half_then_k3 | 2.668 | 2.838 | 1 | 15 | 0.005 | 3.866 | 0.003 |
| zico_sizectrl_half_then_k5 | 4.433 | 4.716 | 1 | 15 | 0.004 | 2.605 | 0.000 |
| params_half_then_k1 | 0.930 | 0.989 | 5 | 15 | 0.009 | 6.202 | 0.003 |
| params_half_then_k3 | 2.702 | 2.875 | 5 | 15 | 0.004 | 2.605 | 0.001 |
| params_half_then_k5 | 4.480 | 4.766 | 5 | 15 | 0.004 | 2.605 | 0.001 |

### Transfer: the top-5 of a source city, scored at the target city

rho_cities = Spearman of the labels of the shared architectures between the two cities.

| source | target_city | n_shared | regret_top1 | regret_best_of_5 | top1_rank_pct | top5_mean_rank_pct | rho_cities |
|---|---|---|---|---|---|---|---|
| metrla | pems04 | 150 | 0.000 | 0.000 | 0.671 | 7.383 | 0.576 |
| metrla | chengdu | 150 | 0.003 | 0.000 | 6.040 | 15.570 | 0.530 |
| metrla | shenzhen | 150 | 0.001 | 0.000 | 0.671 | 6.309 | 0.716 |
| pems04 | metrla | 150 | 0.004 | 0.000 | 8.054 | 12.215 | 0.576 |
| pems04 | chengdu | 150 | 0.004 | 0.003 | 9.396 | 23.893 | 0.517 |
| pems04 | shenzhen | 150 | 0.003 | 0.001 | 2.685 | 7.785 | 0.691 |
| chengdu | metrla | 150 | 0.002 | 0.001 | 1.342 | 10.067 | 0.530 |
| chengdu | pems04 | 150 | 0.001 | 0.001 | 6.711 | 26.443 | 0.517 |
| chengdu | shenzhen | 150 | 0.000 | 0.000 | 0.000 | 6.443 | 0.779 |
| shenzhen | metrla | 150 | 0.002 | 0.000 | 1.342 | 8.322 | 0.716 |
| shenzhen | pems04 | 150 | 0.001 | 0.000 | 6.711 | 9.664 | 0.691 |
| shenzhen | chengdu | 150 | 0.000 | 0.000 | 0.000 | 7.651 | 0.779 |
