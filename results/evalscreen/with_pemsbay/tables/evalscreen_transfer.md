# evalscreen transfer: cheap sources, the choice of the source, and the headroom of transfer

pooled_final_labels = mean label rank over the other three cities. pooled_source_k = the same rank from the validation MAE of the sources after k epochs; source_cost_share = the share of a source list's full cost that k epochs take. b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

### Cheap sources: Spearman inside the heads at the target against the epochs trained at the sources

| city | k | rho_within_head | full_label_within | loss | source_cost_share |
|---|---|---|---|---|---|
| metrla | 1 | 0.167 | 0.656 | 0.489 | 0.062 |
| metrla | 3 | 0.406 | 0.656 | 0.250 | 0.179 |
| metrla | 5 | 0.483 | 0.656 | 0.173 | 0.296 |
| metrla | 10 | 0.630 | 0.656 | 0.026 | 0.585 |
| pems04 | 1 | 0.599 | 0.618 | 0.019 | 0.064 |
| pems04 | 3 | 0.753 | 0.618 | -0.134 | 0.185 |
| pems04 | 5 | 0.754 | 0.618 | -0.136 | 0.307 |
| pems04 | 10 | 0.695 | 0.618 | -0.077 | 0.606 |
| chengdu | 1 | 0.201 | 0.594 | 0.393 | 0.063 |
| chengdu | 3 | 0.232 | 0.594 | 0.363 | 0.180 |
| chengdu | 5 | 0.379 | 0.594 | 0.215 | 0.298 |
| chengdu | 10 | 0.491 | 0.594 | 0.103 | 0.586 |
| shenzhen | 1 | 0.411 | 0.816 | 0.406 | 0.064 |
| shenzhen | 3 | 0.561 | 0.816 | 0.256 | 0.184 |
| shenzhen | 5 | 0.679 | 0.816 | 0.138 | 0.304 |
| shenzhen | 10 | 0.756 | 0.816 | 0.061 | 0.598 |
| expytky | 1 | 0.296 | 0.690 | 0.394 | 0.061 |
| expytky | 3 | 0.460 | 0.690 | 0.230 | 0.173 |
| expytky | 5 | 0.534 | 0.690 | 0.156 | 0.286 |
| expytky | 10 | 0.653 | 0.690 | 0.037 | 0.566 |
| pemsbay | 1 | 0.085 | 0.268 | 0.183 | 0.064 |
| pemsbay | 3 | 0.260 | 0.268 | 0.008 | 0.182 |
| pemsbay | 5 | 0.260 | 0.268 | 0.008 | 0.301 |
| pemsbay | 10 | 0.346 | 0.268 | -0.078 | 0.592 |

### Cheap sources at k = 5 against the pass line

ok = loss <= 0.1 and robust cost at most 1.5 times the full-label pooled rank with a subset share >= 0.9.

| city | k | rho_within_head | full_label_within | loss | source_cost_share | sub_share | sub_pct_median | full_sub_pct_median | ok |
|---|---|---|---|---|---|---|---|---|---|
| metrla | 5 | 0.483 | 0.656 | 0.173 | 0.296 | 1.000 | 3.277 | 1.424 | False |
| pems04 | 5 | 0.754 | 0.618 | -0.136 | 0.307 | 0.995 | 0.864 | 1.556 | True |
| chengdu | 5 | 0.379 | 0.594 | 0.215 | 0.298 | 0.725 | 9.717 | 4.197 | False |
| shenzhen | 5 | 0.679 | 0.816 | 0.138 | 0.304 | 0.925 | 2.647 | 0.940 | False |
| expytky | 5 | 0.534 | 0.690 | 0.156 | 0.286 | 0.745 | 4.978 | 0.925 | False |
| pemsbay | 5 | 0.260 | 0.268 | 0.008 | 0.301 | 0.995 | 2.783 | 1.065 | False |

### Headroom of transfer in sigma_seed, and the probe statistic

probe_spread = std of the test MAE of 5 architectures over sigma_seed (the first 5 of the list; 20 random sets).

| city | sigma_seed | list_std_over_sigma | list_range_over_sigma | share_of_list_within_1_sigma | headroom_pooled_top1_sigma | headroom_pooled_best_of_5_sigma | probe_spread_first5 | probe_spread_mean_random5 | probe_spread_p5 | probe_spread_p95 |
|---|---|---|---|---|---|---|---|---|---|---|
| metrla | 0.001 | 5.654 | 28.697 | 0.013 | 0.000 | 0.000 | 4.169 | 5.523 | 3.398 | 7.452 |
| pems04 | 0.000 | 5.434 | 40.429 | 0.020 | 6.574 | 0.846 | 3.855 | 4.869 | 1.807 | 6.880 |
| chengdu | 0.001 | 3.632 | 17.398 | 0.013 | 2.287 | 1.468 | 2.869 | 3.788 | 2.310 | 5.369 |
| shenzhen | 0.001 | 3.850 | 19.746 | 0.013 | 0.965 | 0.000 | 2.908 | 4.086 | 2.698 | 5.875 |
| expytky | 0.002 | 3.220 | 21.120 | 0.013 | 1.455 | 0.000 | 1.670 | 2.809 | 1.515 | 4.949 |
| pemsbay | 0.001 | 5.677 | 24.569 | 0.013 | 0.000 | 0.000 | 5.183 | 4.931 | 3.562 | 7.310 |

### Source pairs: label-free similarities against the transfer quality

| target | source | sim_proxy_profile | sim_probe_agreement | sim_task_stats | label_rho_within_head | sub_share | sub_pct_median | pct_sigma |
|---|---|---|---|---|---|---|---|---|
| metrla | pems04 | 0.951 | -0.600 |  | 0.501 | 1.000 | 3.326 | 2.219 |
| metrla | chengdu | 0.963 | -0.900 |  | 0.435 | 0.990 | 2.786 | 3.175 |
| metrla | shenzhen | 0.964 | 0.200 |  | 0.576 | 1.000 | 1.482 | 1.515 |
| metrla | expytky | 0.951 | 0.300 |  | 0.626 | 1.000 | 1.067 | 0.704 |
| metrla | pemsbay | 0.971 | 0.100 |  | 0.474 | 1.000 | 1.459 | 0.965 |
| pems04 | metrla | 0.951 | -0.600 |  | 0.501 | 0.965 | 0.864 | 0.568 |
| pems04 | chengdu | 0.956 | 0.700 |  | 0.468 | 0.830 | 7.395 | 5.758 |
| pems04 | shenzhen | 0.957 | 0.000 |  | 0.687 | 1.000 | 1.540 | 1.023 |
| pems04 | expytky | 0.938 | 0.100 |  | 0.479 | 0.975 | 2.834 | 3.133 |
| pems04 | pemsbay | 0.957 | 0.300 |  | 0.186 | 0.715 | 0.864 | 0.568 |
| chengdu | metrla | 0.963 | -0.900 |  | 0.435 | 0.755 | 2.525 | 1.767 |
| chengdu | pems04 | 0.956 | 0.700 |  | 0.468 | 0.740 | 10.359 |  |
| chengdu | shenzhen | 0.974 | 0.100 | -0.429 | 0.762 | 0.840 | 0.728 | 0.477 |
| chengdu | expytky | 0.968 | 0.100 | -2.672 | 0.481 | 0.720 | 8.370 |  |
| chengdu | pemsbay | 0.973 | 0.200 | -1.552 | 0.019 | 0.120 |  |  |
| shenzhen | metrla | 0.964 | 0.200 |  | 0.576 | 1.000 | 0.934 | 0.620 |
| shenzhen | pems04 | 0.957 | 0.000 |  | 0.687 | 0.920 | 2.646 | 1.765 |
| shenzhen | chengdu | 0.974 | 0.100 | -0.429 | 0.762 | 1.000 | 0.600 | 0.392 |
| shenzhen | expytky | 0.968 | 0.300 | -2.310 | 0.617 | 1.000 | 2.457 | 3.178 |
| shenzhen | pemsbay | 0.975 | -0.100 | -1.977 | 0.195 | 0.760 | 0.940 | 0.620 |
| expytky | metrla | 0.951 | 0.300 |  | 0.626 | 1.000 | 1.290 | 0.912 |
| expytky | pems04 | 0.938 | 0.100 |  | 0.479 | 0.440 |  |  |
| expytky | chengdu | 0.968 | 0.100 | -2.672 | 0.481 | 0.970 | 0.702 | 0.524 |
| expytky | shenzhen | 0.968 | 0.300 | -2.310 | 0.617 | 1.000 | 1.308 | 1.039 |
| expytky | pemsbay | 0.961 | 0.900 | -4.126 | 0.464 | 0.980 | 0.957 | 1.077 |
| pemsbay | metrla | 0.971 | 0.100 |  | 0.474 | 1.000 | 1.051 | 0.706 |
| pemsbay | pems04 | 0.957 | 0.300 |  | 0.186 | 0.940 | 2.787 | 1.857 |
| pemsbay | chengdu | 0.973 | 0.200 | -1.552 | 0.019 | 0.970 | 6.970 | 6.242 |
| pemsbay | shenzhen | 0.975 | -0.100 | -1.977 | 0.195 | 0.980 | 1.612 | 1.138 |
| pemsbay | expytky | 0.961 | 0.900 | -4.126 | 0.464 | 1.000 | 2.576 | 3.525 |

### The source that each similarity picks

| similarity | target | chosen_source | true_rank_of_choice | chosen_sub_pct_median | pooled_sub_pct_median | chosen_below_pooled | rho_sim_vs_label_rho |
|---|---|---|---|---|---|---|---|
| sim_proxy_profile | chengdu | shenzhen | 1 | 0.728 | 4.197 | True | 0.300 |
| sim_proxy_profile | expytky | chengdu | 3 | 0.702 | 0.925 | True | 0.100 |
| sim_proxy_profile | metrla | pemsbay | 4 | 1.459 | 1.424 | False | -0.500 |
| sim_proxy_profile | pems04 | pemsbay | 5 | 0.864 | 1.556 | True | -0.300 |
| sim_proxy_profile | pemsbay | shenzhen | 3 | 1.612 | 1.065 | False | -0.100 |
| sim_proxy_profile | shenzhen | pemsbay | 5 | 0.940 | 0.940 | False | -0.300 |
| sim_probe_agreement | chengdu | pems04 | 3 | 10.359 | 4.197 | False | -0.154 |
| sim_probe_agreement | expytky | pemsbay | 5 | 0.957 | 0.925 | False | -0.105 |
| sim_probe_agreement | metrla | expytky | 1 | 1.067 | 1.424 | True | 0.900 |
| sim_probe_agreement | pems04 | chengdu | 4 | 7.395 | 1.556 | False | -0.800 |
| sim_probe_agreement | pemsbay | expytky | 2 | 2.576 | 1.065 | False | -0.100 |
| sim_probe_agreement | shenzhen | expytky | 3 | 2.457 | 0.940 | False | 0.200 |
| sim_task_stats | chengdu | shenzhen | 1 | 0.728 | 4.197 | True |  |
| sim_task_stats | expytky | shenzhen | 2 | 1.308 | 0.925 | False |  |
| sim_task_stats | pemsbay | chengdu | 5 | 6.970 | 1.065 | False |  |
| sim_task_stats | shenzhen | chengdu | 1 | 0.600 | 0.940 | True |  |

### metrla: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_expytky | transfer, one source | 0.826 | 0.671 | 1.000 | 0.231 | 0.704 | 1.000 | 1.067 | 1.000 |
| pooled_final_labels | transfer | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.424 | 1.000 |
| pooled_source_k10 | transfer, cheap sources | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.433 | 1.000 |
| from_expytky_k5 | transfer, one cheap source | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.436 | 1.000 |
| from_pemsbay | transfer, one source | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.459 | 1.000 |
| from_shenzhen | transfer, one source | 1.283 | 1.342 | 2.000 | 0.498 | 1.515 | 1.000 | 1.482 | 1.000 |
| from_pemsbay_k5 | transfer, one cheap source | 1.684 | 5.369 | 2.000 | 0.532 | 1.620 | 1.000 | 2.331 | 2.000 |
| from_chengdu_k5 | transfer, one cheap source | 1.283 | 1.342 | 3.000 | 0.781 | 2.378 | 1.000 | 2.710 | 2.000 |
| from_chengdu | transfer, one source | 1.283 | 1.342 | 5.000 | 1.043 | 3.175 | 0.990 | 2.786 | 3.000 |
| pooled_source_k3 | transfer, cheap sources | 3.270 | 13.423 | 3.000 | 0.870 | 2.649 | 1.000 | 3.208 | 2.000 |
| pooled_source_k5 | transfer, cheap sources | 2.555 | 8.054 | 2.000 | 0.729 | 2.219 | 1.000 | 3.277 | 2.000 |
| from_pems04 | transfer, one source | 2.555 | 8.054 | 2.000 | 0.729 | 2.219 | 1.000 | 3.326 | 2.000 |
| from_shenzhen_k5 | transfer, one cheap source | 1.379 | 2.013 | 8.000 | 2.273 | 6.917 | 1.000 | 6.717 | 5.000 |
| pooled_source_k1 | transfer, cheap sources | 1.616 | 4.027 |  |  |  | 0.970 | 9.922 | 8.000 |
| from_pems04_k5 | transfer, one cheap source | 2.555 | 8.054 |  |  |  | 0.275 |  |  |

### pems04: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_metrla_k5 | transfer, one cheap source | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.995 | 0.858 | 1.000 |
| pooled_source_k3 | transfer, cheap sources | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.995 | 0.864 | 1.000 |
| pooled_source_k5 | transfer, cheap sources | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.995 | 0.864 | 1.000 |
| pooled_source_k10 | transfer, cheap sources | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.995 | 0.864 | 1.000 |
| from_metrla | transfer, one source | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.965 | 0.864 | 1.000 |
| from_expytky_k5 | transfer, one cheap source | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.990 | 0.864 | 1.000 |
| from_pemsbay | transfer, one source | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.715 | 0.864 | 1.000 |
| from_pemsbay_k5 | transfer, one cheap source | 3.413 | 10.738 | 2.000 | 0.292 | 1.018 | 1.000 | 1.525 | 2.000 |
| from_shenzhen | transfer, one source | 2.635 | 6.711 | 2.000 | 0.293 | 1.023 | 1.000 | 1.540 | 2.000 |
| pooled_final_labels | transfer | 6.574 | 21.477 | 2.000 | 0.295 | 1.031 | 0.980 | 1.556 | 2.000 |
| from_expytky | transfer, one source | 6.574 | 21.477 | 5.000 | 0.898 | 3.133 | 0.975 | 2.834 | 3.000 |
| from_chengdu_k5 | transfer, one cheap source | 2.635 | 6.711 | 5.000 | 0.818 | 2.855 | 0.990 | 2.945 | 3.000 |
| from_shenzhen_k5 | transfer, one cheap source | 1.615 | 3.356 | 5.000 | 1.076 | 3.755 | 0.990 | 3.660 | 3.000 |
| pooled_source_k1 | transfer, cheap sources | 2.982 | 8.725 | 5.000 | 1.139 | 3.977 | 0.995 | 4.273 | 3.000 |
| from_chengdu | transfer, one source | 2.635 | 6.711 | 10.000 | 1.650 | 5.758 | 0.830 | 7.395 | 8.000 |

### chengdu: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_shenzhen | transfer, one source | 0.000 | 0.000 | 1.000 | 0.100 | 0.477 | 0.840 | 0.728 | 1.000 |
| from_shenzhen_k5 | transfer, one cheap source | 4.685 | 22.148 | 2.000 | 0.201 | 0.954 | 0.755 | 1.439 | 2.000 |
| from_metrla | transfer, one source | 2.287 | 6.040 | 3.000 | 0.372 | 1.767 | 0.755 | 2.525 | 3.000 |
| pooled_final_labels | transfer | 2.287 | 6.040 | 8.000 | 1.041 | 4.942 | 0.755 | 4.197 | 5.000 |
| from_expytky_k5 | transfer, one cheap source | 2.287 | 6.040 | 8.000 | 1.067 | 5.065 | 0.755 | 5.321 | 5.000 |
| pooled_source_k10 | transfer, cheap sources | 2.287 | 6.040 | 8.000 | 1.200 | 5.697 | 0.755 | 6.022 | 5.000 |
| pooled_source_k1 | transfer, cheap sources | 8.085 | 59.732 | 10.000 | 1.425 | 6.766 | 0.750 | 8.243 | 8.000 |
| from_expytky | transfer, one source | 1.519 | 2.013 |  |  |  | 0.720 | 8.370 | 9.000 |
| pooled_source_k5 | transfer, cheap sources | 2.941 | 9.396 |  |  |  | 0.725 | 9.717 | 10.000 |
| from_pems04 | transfer, one source | 2.941 | 9.396 |  |  |  | 0.740 | 10.359 | 8.000 |
| pooled_source_k3 | transfer, cheap sources | 2.287 | 6.040 |  |  |  | 0.670 | 10.514 | 10.000 |
| from_metrla_k5 | transfer, one cheap source | 2.287 | 6.040 |  |  |  | 0.205 |  |  |
| from_pems04_k5 | transfer, one cheap source | 2.941 | 9.396 |  |  |  | 0.110 |  |  |
| from_pemsbay | transfer, one source | 2.287 | 6.040 |  |  |  | 0.120 |  |  |
| from_pemsbay_k5 | transfer, one cheap source | 1.468 | 1.342 |  |  |  | 0.120 |  |  |

### shenzhen: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_chengdu | transfer, one source | 0.000 | 0.000 | 1.000 | 0.125 | 0.392 | 1.000 | 0.600 | 1.000 |
| from_chengdu_k5 | transfer, one cheap source | 0.000 | 0.000 | 1.000 | 0.125 | 0.392 | 1.000 | 0.600 | 1.000 |
| from_metrla | transfer, one source | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.934 | 1.000 |
| pooled_final_labels | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.940 | 1.000 |
| from_pemsbay | transfer, one source | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 0.760 | 0.940 | 1.000 |
| from_expytky_k5 | transfer, one cheap source | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.941 | 1.000 |
| pooled_source_k10 | transfer, cheap sources | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.943 | 1.000 |
| from_metrla_k5 | transfer, one cheap source | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 0.790 | 0.943 | 1.000 |
| pooled_source_k3 | transfer, cheap sources | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 0.930 | 0.944 | 1.000 |
| from_pemsbay_k5 | transfer, one cheap source | 3.767 | 6.711 | 2.000 | 0.331 | 1.036 | 0.710 | 1.562 | 2.000 |
| from_expytky | transfer, one source | 1.260 | 1.342 | 5.000 | 1.016 | 3.178 | 1.000 | 2.457 | 3.000 |
| from_pems04 | transfer, one source | 2.965 | 2.685 | 2.000 | 0.564 | 1.765 | 0.920 | 2.646 | 2.000 |
| pooled_source_k5 | transfer, cheap sources | 2.965 | 2.685 | 2.000 | 0.564 | 1.765 | 0.925 | 2.647 | 2.000 |
| pooled_source_k1 | transfer, cheap sources | 10.078 | 64.430 | 8.000 | 1.724 | 5.394 | 0.940 | 5.133 | 5.000 |
| from_pems04_k5 | transfer, one cheap source | 2.965 | 2.685 |  |  |  | 0.045 |  |  |

### expytky: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_pemsbay_k5 | transfer, one cheap source | 0.635 | 0.671 | 1.000 | 0.123 | 0.218 | 0.705 | 0.337 | 1.000 |
| from_chengdu | transfer, one source | 4.692 | 7.383 | 3.000 | 0.296 | 0.524 | 0.970 | 0.702 | 2.000 |
| pooled_final_labels | transfer | 1.455 | 2.013 | 3.000 | 0.587 | 1.039 | 1.000 | 0.925 | 2.000 |
| from_pemsbay | transfer, one source | 1.455 | 2.013 | 3.000 | 0.609 | 1.077 | 0.980 | 0.957 | 2.000 |
| pooled_source_k10 | transfer, cheap sources | 1.455 | 2.013 | 2.000 | 0.461 | 0.816 | 0.985 | 1.197 | 2.000 |
| from_metrla_k5 | transfer, one cheap source | 1.455 | 2.013 | 2.000 | 0.461 | 0.816 | 0.925 | 1.197 | 2.000 |
| from_metrla | transfer, one source | 1.455 | 2.013 | 2.000 | 0.516 | 0.912 | 1.000 | 1.290 | 1.000 |
| from_shenzhen | transfer, one source | 4.692 | 7.383 | 3.000 | 0.587 | 1.039 | 1.000 | 1.308 | 2.000 |
| from_chengdu_k5 | transfer, one cheap source | 4.692 | 7.383 | 3.000 | 0.779 | 1.377 | 0.970 | 1.999 | 2.000 |
| from_shenzhen_k5 | transfer, one cheap source | 1.321 | 1.342 | 5.000 | 2.101 | 3.717 | 1.000 | 2.666 | 3.000 |
| pooled_source_k5 | transfer, cheap sources | 4.487 | 5.369 | 8.000 | 2.570 | 4.546 | 0.745 | 4.978 | 5.000 |
| pooled_source_k1 | transfer, cheap sources | 8.671 | 42.953 |  |  |  | 0.530 | 11.925 | 10.000 |
| pooled_source_k3 | transfer, cheap sources | 4.649 | 6.711 |  |  |  | 0.430 |  |  |
| from_pems04 | transfer, one source | 4.487 | 5.369 |  |  |  | 0.440 |  |  |
| from_pems04_k5 | transfer, one cheap source | 4.487 | 5.369 |  |  |  | 0.100 |  |  |

### pemsbay: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_metrla | transfer, one source | 0.000 | 0.000 | 1.000 | 0.512 | 0.706 | 1.000 | 1.051 | 1.000 |
| from_expytky_k5 | transfer, one cheap source | 0.000 | 0.000 | 1.000 | 0.512 | 0.706 | 1.000 | 1.051 | 1.000 |
| pooled_source_k10 | transfer, cheap sources | 0.000 | 0.000 | 1.000 | 0.512 | 0.706 | 0.990 | 1.055 | 1.000 |
| from_metrla_k5 | transfer, one cheap source | 0.000 | 0.000 | 1.000 | 0.512 | 0.706 | 1.000 | 1.055 | 1.000 |
| pooled_final_labels | transfer | 0.000 | 0.000 | 1.000 | 0.512 | 0.706 | 0.980 | 1.065 | 1.000 |
| pooled_source_k3 | transfer, cheap sources | 5.767 | 38.255 | 2.000 | 0.716 | 0.987 | 0.930 | 1.495 | 2.000 |
| from_shenzhen | transfer, one source | 4.150 | 17.450 | 2.000 | 0.825 | 1.138 | 0.980 | 1.612 | 2.000 |
| from_expytky | transfer, one source | 1.124 | 1.342 | 5.000 | 2.556 | 3.525 | 1.000 | 2.576 | 3.000 |
| pooled_source_k5 | transfer, cheap sources | 5.348 | 29.530 | 2.000 | 1.346 | 1.857 | 0.995 | 2.783 | 2.000 |
| from_pems04 | transfer, one source | 5.348 | 29.530 | 2.000 | 1.346 | 1.857 | 0.940 | 2.787 | 2.000 |
| from_chengdu_k5 | transfer, one cheap source | 4.150 | 17.450 | 5.000 | 2.001 | 2.761 | 0.990 | 2.805 | 3.000 |
| from_shenzhen_k5 | transfer, one cheap source | 3.421 | 12.081 | 8.000 | 3.843 | 5.301 | 1.000 | 6.096 | 5.000 |
| from_chengdu | transfer, one source | 4.150 | 17.450 | 10.000 | 4.525 | 6.242 | 0.970 | 6.970 | 8.000 |
| pooled_source_k1 | transfer, cheap sources | 2.527 | 6.040 |  |  |  | 0.445 |  |  |
| from_pems04_k5 | transfer, one cheap source | 5.348 | 29.530 |  |  |  | 0.010 |  |  |
