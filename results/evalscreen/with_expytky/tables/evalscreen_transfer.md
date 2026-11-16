# evalscreen transfer: cheap sources, the choice of the source, and the headroom of transfer

pooled_final_labels = mean label rank over the other three cities. pooled_source_k = the same rank from the validation MAE of the sources after k epochs; source_cost_share = the share of a source list's full cost that k epochs take. b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

### Cheap sources: Spearman inside the heads at the target against the epochs trained at the sources

| city | k | rho_within_head | full_label_within | loss | source_cost_share |
|---|---|---|---|---|---|
| metrla | 1 | 0.131 | 0.620 | 0.489 | 0.063 |
| metrla | 3 | 0.401 | 0.620 | 0.220 | 0.180 |
| metrla | 5 | 0.473 | 0.620 | 0.147 | 0.298 |
| metrla | 10 | 0.602 | 0.620 | 0.018 | 0.587 |
| pems04 | 1 | 0.648 | 0.640 | -0.007 | 0.065 |
| pems04 | 3 | 0.746 | 0.640 | -0.105 | 0.188 |
| pems04 | 5 | 0.745 | 0.640 | -0.105 | 0.312 |
| pems04 | 10 | 0.696 | 0.640 | -0.056 | 0.614 |
| chengdu | 1 | 0.235 | 0.645 | 0.410 | 0.064 |
| chengdu | 3 | 0.237 | 0.645 | 0.408 | 0.182 |
| chengdu | 5 | 0.389 | 0.645 | 0.256 | 0.300 |
| chengdu | 10 | 0.538 | 0.645 | 0.107 | 0.589 |
| shenzhen | 1 | 0.456 | 0.843 | 0.387 | 0.065 |
| shenzhen | 3 | 0.552 | 0.843 | 0.291 | 0.186 |
| shenzhen | 5 | 0.679 | 0.843 | 0.164 | 0.308 |
| shenzhen | 10 | 0.799 | 0.843 | 0.044 | 0.604 |
| expytky | 1 | 0.270 | 0.641 | 0.370 | 0.061 |
| expytky | 3 | 0.433 | 0.641 | 0.208 | 0.173 |
| expytky | 5 | 0.511 | 0.641 | 0.129 | 0.286 |
| expytky | 10 | 0.600 | 0.641 | 0.041 | 0.564 |

### Cheap sources at k = 5 against the pass line

ok = loss <= 0.1 and robust cost at most 1.5 times the full-label pooled rank with a subset share >= 0.9.

| city | k | rho_within_head | full_label_within | loss | source_cost_share | sub_share | sub_pct_median | full_sub_pct_median | ok |
|---|---|---|---|---|---|---|---|---|---|
| metrla | 5 | 0.473 | 0.620 | 0.147 | 0.298 | 1.000 | 3.231 | 1.436 | False |
| pems04 | 5 | 0.745 | 0.640 | -0.105 | 0.312 | 0.995 | 2.337 | 4.199 | True |
| chengdu | 5 | 0.389 | 0.645 | 0.256 | 0.300 | 0.750 | 9.171 | 2.489 | False |
| shenzhen | 5 | 0.679 | 0.843 | 0.164 | 0.308 | 0.925 | 2.647 | 0.926 | False |
| expytky | 5 | 0.511 | 0.641 | 0.129 | 0.286 | 0.735 | 7.347 | 1.754 | False |

### Headroom of transfer in sigma_seed, and the probe statistic

probe_spread = std of the test MAE of 5 architectures over sigma_seed (the first 5 of the list; 20 random sets).

| city | sigma_seed | list_std_over_sigma | list_range_over_sigma | share_of_list_within_1_sigma | headroom_pooled_top1_sigma | headroom_pooled_best_of_5_sigma | probe_spread_first5 | probe_spread_mean_random5 | probe_spread_p5 | probe_spread_p95 |
|---|---|---|---|---|---|---|---|---|---|---|
| metrla | 0.003 | 2.296 | 11.653 | 0.073 | 0.000 | 0.000 | 1.693 | 2.243 | 1.380 | 3.026 |
| pems04 | 0.000 | 8.429 | 62.712 | 0.007 | 10.197 | 0.000 | 5.979 | 7.552 | 2.802 | 10.671 |
| chengdu | 0.001 | 3.632 | 17.398 | 0.013 | 2.287 | 0.000 | 2.869 | 3.788 | 2.310 | 5.369 |
| shenzhen | 0.001 | 3.850 | 19.746 | 0.013 | 0.965 | 0.000 | 2.908 | 4.086 | 2.698 | 5.875 |
| expytky | 0.002 | 3.144 | 20.626 | 0.013 | 1.421 | 0.000 | 1.631 | 2.743 | 1.479 | 4.833 |

### Source pairs: label-free similarities against the transfer quality

| target | source | sim_proxy_profile | sim_probe_agreement | sim_task_stats | label_rho_within_head | sub_share | sub_pct_median | pct_sigma |
|---|---|---|---|---|---|---|---|---|
| metrla | pems04 | 0.951 | -0.600 |  | 0.501 | 1.000 | 3.182 | 2.219 |
| metrla | chengdu | 0.963 | -0.900 |  | 0.435 | 1.000 | 0.840 | 0.550 |
| metrla | shenzhen | 0.964 | 0.200 |  | 0.576 | 1.000 | 0.840 | 0.550 |
| metrla | expytky | 0.950 | 0.300 |  | 0.626 | 1.000 | 1.052 | 0.704 |
| pems04 | metrla | 0.951 | -0.600 |  | 0.501 | 0.830 | 8.620 |  |
| pems04 | chengdu | 0.956 | 0.700 |  | 0.468 | 0.645 | 9.933 |  |
| pems04 | shenzhen | 0.957 | 0.000 |  | 0.687 | 0.995 | 3.217 | 3.071 |
| pems04 | expytky | 0.936 | 0.100 |  | 0.479 | 0.915 | 7.106 | 6.236 |
| chengdu | metrla | 0.963 | -0.900 |  | 0.435 | 0.755 | 2.525 | 1.767 |
| chengdu | pems04 | 0.956 | 0.700 |  | 0.468 | 0.740 | 10.359 |  |
| chengdu | shenzhen | 0.974 | 0.100 | -0.622 | 0.762 | 0.840 | 0.728 | 0.477 |
| chengdu | expytky | 0.967 | 0.100 | -3.221 | 0.481 | 0.720 | 8.370 |  |
| shenzhen | metrla | 0.964 | 0.200 |  | 0.576 | 1.000 | 0.934 | 0.620 |
| shenzhen | pems04 | 0.957 | 0.000 |  | 0.687 | 0.920 | 2.646 | 1.765 |
| shenzhen | chengdu | 0.974 | 0.100 | -0.622 | 0.762 | 1.000 | 0.600 | 0.392 |
| shenzhen | expytky | 0.967 | 0.300 | -2.691 | 0.617 | 1.000 | 2.457 | 3.178 |
| expytky | metrla | 0.950 | 0.300 |  | 0.626 | 1.000 | 1.290 | 0.912 |
| expytky | pems04 | 0.936 | 0.100 |  | 0.479 | 0.440 |  |  |
| expytky | chengdu | 0.967 | 0.100 | -3.221 | 0.481 | 0.970 | 0.702 | 0.524 |
| expytky | shenzhen | 0.967 | 0.300 | -2.691 | 0.617 | 1.000 | 1.308 | 1.039 |

### The source that each similarity picks

| similarity | target | chosen_source | true_rank_of_choice | chosen_sub_pct_median | pooled_sub_pct_median | chosen_below_pooled | rho_sim_vs_label_rho |
|---|---|---|---|---|---|---|---|
| sim_proxy_profile | chengdu | shenzhen | 1 | 0.728 | 2.489 | True | 0.800 |
| sim_proxy_profile | expytky | chengdu | 3 | 0.702 | 1.754 | True | 0.200 |
| sim_proxy_profile | metrla | shenzhen | 2 | 0.840 | 1.436 | True | -0.400 |
| sim_proxy_profile | pems04 | shenzhen | 1 | 3.217 | 4.199 | True | 0.400 |
| sim_proxy_profile | shenzhen | chengdu | 1 | 0.600 | 0.926 | True | 0.400 |
| sim_probe_agreement | chengdu | pems04 | 3 | 10.359 | 2.489 | False | 0.316 |
| sim_probe_agreement | expytky | metrla | 1 | 1.290 | 1.754 | True | 0.894 |
| sim_probe_agreement | metrla | expytky | 1 | 1.052 | 1.436 | True | 1.000 |
| sim_probe_agreement | pems04 | chengdu | 4 | 9.933 | 4.199 | False | -0.800 |
| sim_probe_agreement | shenzhen | expytky | 3 | 2.457 | 0.926 | False | -0.600 |
| sim_task_stats | chengdu | shenzhen | 1 | 0.728 | 2.489 | True |  |
| sim_task_stats | expytky | shenzhen | 2 | 1.308 | 1.754 | True |  |
| sim_task_stats | shenzhen | chengdu | 1 | 0.600 | 0.926 | True |  |

### metrla: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_chengdu | transfer, one source | 0.521 | 1.342 | 1.000 | 0.181 | 0.550 | 1.000 | 0.840 | 1.000 |
| from_chengdu_k5 | transfer, one cheap source | 0.521 | 1.342 | 1.000 | 0.181 | 0.550 | 1.000 | 0.840 | 1.000 |
| from_shenzhen | transfer, one source | 0.521 | 1.342 | 1.000 | 0.181 | 0.550 | 1.000 | 0.840 | 1.000 |
| from_expytky | transfer, one source | 0.335 | 0.671 | 1.000 | 0.231 | 0.704 | 1.000 | 1.052 | 1.000 |
| pooled_final_labels | transfer | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.436 | 1.000 |
| pooled_source_k10 | transfer, cheap sources | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.436 | 1.000 |
| from_expytky_k5 | transfer, one cheap source | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.436 | 1.000 |
| from_shenzhen_k5 | transfer, one cheap source | 0.560 | 2.013 | 1.000 | 0.347 | 1.057 | 1.000 | 1.570 | 1.000 |
| pooled_source_k3 | transfer, cheap sources | 1.328 | 13.423 | 3.000 | 0.870 | 2.649 | 1.000 | 2.720 | 2.000 |
| pooled_source_k1 | transfer, cheap sources | 4.991 | 67.114 | 5.000 | 1.050 | 3.194 | 0.990 | 2.926 | 3.000 |
| from_pems04 | transfer, one source | 1.038 | 8.054 | 2.000 | 0.729 | 2.219 | 1.000 | 3.182 | 2.000 |
| pooled_source_k5 | transfer, cheap sources | 1.038 | 8.054 | 3.000 | 1.099 | 3.343 | 1.000 | 3.231 | 2.000 |
| from_pems04_k5 | transfer, one cheap source | 1.038 | 8.054 |  |  |  | 0.870 | 9.558 | 8.000 |

### pems04: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_metrla_k5 | transfer, one cheap source | 1.312 | 0.671 | 3.000 | 0.578 | 2.016 | 0.995 | 2.214 | 2.000 |
| pooled_source_k3 | transfer, cheap sources | 1.312 | 0.671 | 2.000 | 0.449 | 1.567 | 0.995 | 2.291 | 2.000 |
| pooled_source_k5 | transfer, cheap sources | 1.312 | 0.671 | 3.000 | 0.578 | 2.016 | 0.995 | 2.337 | 2.000 |
| from_shenzhen | transfer, one source | 4.087 | 6.711 | 5.000 | 0.880 | 3.071 | 0.995 | 3.217 | 3.000 |
| from_expytky_k5 | transfer, one cheap source | 1.312 | 0.671 | 5.000 | 0.983 | 3.432 | 0.990 | 3.592 | 3.000 |
| pooled_final_labels | transfer | 10.197 | 21.477 | 5.000 | 0.840 | 2.933 | 0.985 | 4.199 | 5.000 |
| pooled_source_k10 | transfer, cheap sources | 1.312 | 0.671 | 8.000 | 1.418 | 4.948 | 0.990 | 4.578 | 5.000 |
| from_shenzhen_k5 | transfer, one cheap source | 2.505 | 3.356 | 5.000 | 1.076 | 3.755 | 0.985 | 4.876 | 5.000 |
| from_chengdu_k5 | transfer, one cheap source | 4.087 | 6.711 | 8.000 | 1.380 | 4.818 | 0.965 | 4.957 | 5.000 |
| from_expytky | transfer, one source | 10.197 | 21.477 | 10.000 | 1.787 | 6.236 | 0.915 | 7.106 | 8.000 |
| pooled_source_k1 | transfer, cheap sources | 4.625 | 8.725 | 10.000 | 1.919 | 6.698 | 0.995 | 7.921 | 8.000 |
| from_metrla | transfer, one source | 1.312 | 0.671 |  |  |  | 0.830 | 8.620 | 8.000 |
| from_chengdu | transfer, one source | 4.087 | 6.711 |  |  |  | 0.645 | 9.933 | 10.000 |

### chengdu: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_shenzhen | transfer, one source | 0.000 | 0.000 | 1.000 | 0.100 | 0.477 | 0.840 | 0.728 | 1.000 |
| from_shenzhen_k5 | transfer, one cheap source | 4.685 | 22.148 | 2.000 | 0.201 | 0.954 | 0.755 | 1.439 | 2.000 |
| pooled_final_labels | transfer | 2.287 | 6.040 | 3.000 | 0.357 | 1.695 | 0.755 | 2.489 | 3.000 |
| from_metrla | transfer, one source | 2.287 | 6.040 | 3.000 | 0.372 | 1.767 | 0.755 | 2.525 | 3.000 |
| pooled_source_k1 | transfer, cheap sources | 8.085 | 59.732 | 8.000 | 1.017 | 4.831 | 0.740 | 4.640 | 5.000 |
| pooled_source_k10 | transfer, cheap sources | 2.287 | 6.040 | 5.000 | 0.711 | 3.378 | 0.755 | 5.020 | 5.000 |
| from_expytky_k5 | transfer, one cheap source | 2.287 | 6.040 | 8.000 | 1.067 | 5.065 | 0.755 | 5.321 | 5.000 |
| from_expytky | transfer, one source | 1.519 | 2.013 |  |  |  | 0.720 | 8.370 | 9.000 |
| pooled_source_k5 | transfer, cheap sources | 2.941 | 9.396 |  |  |  | 0.750 | 9.171 | 8.000 |
| from_pems04 | transfer, one source | 2.941 | 9.396 |  |  |  | 0.740 | 10.359 | 8.000 |
| pooled_source_k3 | transfer, cheap sources | 2.287 | 6.040 |  |  |  | 0.660 | 10.590 | 10.000 |
| from_metrla_k5 | transfer, one cheap source | 2.287 | 6.040 |  |  |  | 0.205 |  |  |
| from_pems04_k5 | transfer, one cheap source | 2.941 | 9.396 |  |  |  | 0.110 |  |  |

### shenzhen: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_chengdu | transfer, one source | 0.000 | 0.000 | 1.000 | 0.125 | 0.392 | 1.000 | 0.600 | 1.000 |
| from_chengdu_k5 | transfer, one cheap source | 0.000 | 0.000 | 1.000 | 0.125 | 0.392 | 1.000 | 0.600 | 1.000 |
| pooled_final_labels | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.926 | 1.000 |
| from_metrla | transfer, one source | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.934 | 1.000 |
| pooled_source_k10 | transfer, cheap sources | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 0.985 | 0.937 | 1.000 |
| from_expytky_k5 | transfer, one cheap source | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.941 | 1.000 |
| from_metrla_k5 | transfer, one cheap source | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 0.790 | 0.943 | 1.000 |
| pooled_source_k3 | transfer, cheap sources | 5.339 | 17.450 | 2.000 | 0.334 | 1.044 | 0.925 | 1.575 | 2.000 |
| pooled_source_k1 | transfer, cheap sources | 3.796 | 7.383 | 3.000 | 0.500 | 1.564 | 0.880 | 2.342 | 3.000 |
| from_expytky | transfer, one source | 1.260 | 1.342 | 5.000 | 1.016 | 3.178 | 1.000 | 2.457 | 3.000 |
| from_pems04 | transfer, one source | 2.965 | 2.685 | 2.000 | 0.564 | 1.765 | 0.920 | 2.646 | 2.000 |
| pooled_source_k5 | transfer, cheap sources | 2.965 | 2.685 | 2.000 | 0.564 | 1.765 | 0.925 | 2.647 | 2.000 |
| from_pems04_k5 | transfer, one cheap source | 2.965 | 2.685 |  |  |  | 0.045 |  |  |

### expytky: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_chengdu | transfer, one source | 4.582 | 7.383 | 3.000 | 0.296 | 0.524 | 0.970 | 0.702 | 2.000 |
| from_metrla_k5 | transfer, one cheap source | 1.421 | 2.013 | 2.000 | 0.461 | 0.816 | 0.925 | 1.197 | 2.000 |
| pooled_source_k10 | transfer, cheap sources | 1.421 | 2.013 | 3.000 | 0.533 | 0.942 | 0.955 | 1.221 | 2.000 |
| from_metrla | transfer, one source | 1.421 | 2.013 | 2.000 | 0.516 | 0.912 | 1.000 | 1.290 | 1.000 |
| from_shenzhen | transfer, one source | 4.582 | 7.383 | 3.000 | 0.587 | 1.039 | 1.000 | 1.308 | 2.000 |
| pooled_final_labels | transfer | 1.421 | 2.013 | 5.000 | 1.276 | 2.257 | 1.000 | 1.754 | 3.000 |
| from_chengdu_k5 | transfer, one cheap source | 4.582 | 7.383 | 3.000 | 0.779 | 1.377 | 0.970 | 1.999 | 2.000 |
| from_shenzhen_k5 | transfer, one cheap source | 1.290 | 1.342 | 5.000 | 2.101 | 3.717 | 1.000 | 2.666 | 3.000 |
| pooled_source_k5 | transfer, cheap sources | 4.382 | 5.369 | 10.000 | 3.659 | 6.474 | 0.735 | 7.347 | 8.000 |
| pooled_source_k1 | transfer, cheap sources | 8.468 | 42.953 |  |  |  | 0.210 |  |  |
| pooled_source_k3 | transfer, cheap sources | 4.540 | 6.711 |  |  |  | 0.300 |  |  |
| from_pems04 | transfer, one source | 4.382 | 5.369 |  |  |  | 0.440 |  |  |
| from_pems04_k5 | transfer, one cheap source | 4.382 | 5.369 |  |  |  | 0.100 |  |  |
