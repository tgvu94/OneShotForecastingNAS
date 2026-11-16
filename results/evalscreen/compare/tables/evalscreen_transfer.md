# evalscreen transfer: cheap sources, the choice of the source, and the headroom of transfer

pooled_final_labels = mean label rank over the other three cities. pooled_source_k = the same rank from the validation MAE of the sources after k epochs; source_cost_share = the share of a source list's full cost that k epochs take. b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

### Cheap sources: Spearman inside the heads at the target against the epochs trained at the sources

| city | k | rho_within_head | full_label_within | loss | source_cost_share |
|---|---|---|---|---|---|
| metrla | 1 | 0.097 | 0.578 | 0.481 | 0.059 |
| metrla | 3 | 0.320 | 0.578 | 0.258 | 0.168 |
| metrla | 5 | 0.396 | 0.578 | 0.182 | 0.277 |
| metrla | 10 | 0.535 | 0.578 | 0.043 | 0.549 |
| pems04 | 1 | 0.635 | 0.634 | -0.002 | 0.062 |
| pems04 | 3 | 0.726 | 0.634 | -0.092 | 0.179 |
| pems04 | 5 | 0.738 | 0.634 | -0.104 | 0.296 |
| pems04 | 10 | 0.721 | 0.634 | -0.088 | 0.584 |
| chengdu | 1 | 0.195 | 0.657 | 0.463 | 0.061 |
| chengdu | 3 | 0.161 | 0.657 | 0.496 | 0.170 |
| chengdu | 5 | 0.322 | 0.657 | 0.336 | 0.280 |
| chengdu | 10 | 0.491 | 0.657 | 0.166 | 0.551 |
| shenzhen | 1 | 0.412 | 0.845 | 0.433 | 0.063 |
| shenzhen | 3 | 0.476 | 0.845 | 0.369 | 0.176 |
| shenzhen | 5 | 0.654 | 0.845 | 0.191 | 0.290 |
| shenzhen | 10 | 0.788 | 0.845 | 0.057 | 0.572 |

### Cheap sources at k = 5 against the pass line

ok = loss <= 0.1 and robust cost at most 1.5 times the full-label pooled rank with a subset share >= 0.9.

| city | k | rho_within_head | full_label_within | loss | source_cost_share | sub_share | sub_pct_median | full_sub_pct_median | ok |
|---|---|---|---|---|---|---|---|---|---|
| metrla | 5 | 0.396 | 0.578 | 0.182 | 0.277 | 1.000 | 4.364 | 0.840 | False |
| pems04 | 5 | 0.738 | 0.634 | -0.104 | 0.296 | 0.995 | 2.308 | 4.346 | True |
| chengdu | 5 | 0.322 | 0.657 | 0.336 | 0.280 | 0.680 | 10.291 | 1.828 | False |
| shenzhen | 5 | 0.654 | 0.845 | 0.191 | 0.290 | 0.915 | 4.298 | 0.926 | False |

### Headroom of transfer in sigma_seed, and the probe statistic

probe_spread = std of the test MAE of 5 architectures over sigma_seed (the first 5 of the list; 20 random sets).

| city | sigma_seed | list_std_over_sigma | list_range_over_sigma | share_of_list_within_1_sigma | headroom_pooled_top1_sigma | headroom_pooled_best_of_5_sigma | probe_spread_first5 | probe_spread_mean_random5 | probe_spread_p5 | probe_spread_p95 |
|---|---|---|---|---|---|---|---|---|---|---|
| metrla | 0.003 | 2.296 | 11.653 | 0.073 | 0.521 | 0.000 | 1.693 | 2.243 | 1.380 | 3.026 |
| pems04 | 0.000 | 8.429 | 62.712 | 0.007 | 4.087 | 0.000 | 5.979 | 7.552 | 2.802 | 10.671 |
| chengdu | 0.001 | 3.632 | 17.398 | 0.013 | 2.287 | 0.000 | 2.869 | 3.788 | 2.310 | 5.369 |
| shenzhen | 0.001 | 3.850 | 19.746 | 0.013 | 0.965 | 0.000 | 2.908 | 4.086 | 2.698 | 5.875 |

### Source pairs: label-free similarities against the transfer quality

| target | source | sim_proxy_profile | sim_probe_agreement | sim_task_stats | label_rho_within_head | sub_share | sub_pct_median | pct_sigma |
|---|---|---|---|---|---|---|---|---|
| metrla | pems04 | 0.951 | -0.600 |  | 0.501 | 1.000 | 3.182 | 2.219 |
| metrla | chengdu | 0.963 | -0.900 |  | 0.435 | 1.000 | 0.840 | 0.550 |
| metrla | shenzhen | 0.964 | 0.200 |  | 0.576 | 1.000 | 0.840 | 0.550 |
| pems04 | metrla | 0.951 | -0.600 |  | 0.501 | 0.830 | 8.620 |  |
| pems04 | chengdu | 0.956 | 0.700 |  | 0.468 | 0.645 | 9.933 |  |
| pems04 | shenzhen | 0.957 | 0.000 |  | 0.687 | 0.995 | 3.217 | 3.071 |
| chengdu | metrla | 0.963 | -0.900 |  | 0.435 | 0.755 | 2.525 | 1.767 |
| chengdu | pems04 | 0.956 | 0.700 |  | 0.468 | 0.740 | 10.359 |  |
| chengdu | shenzhen | 0.974 | 0.100 | -2.449 | 0.762 | 0.840 | 0.728 | 0.477 |
| shenzhen | metrla | 0.964 | 0.200 |  | 0.576 | 1.000 | 0.934 | 0.620 |
| shenzhen | pems04 | 0.957 | 0.000 |  | 0.687 | 0.920 | 2.646 | 1.765 |
| shenzhen | chengdu | 0.974 | 0.100 | -2.449 | 0.762 | 1.000 | 0.600 | 0.392 |

### The source that each similarity picks

| similarity | target | chosen_source | true_rank_of_choice | chosen_sub_pct_median | pooled_sub_pct_median | chosen_below_pooled | rho_sim_vs_label_rho |
|---|---|---|---|---|---|---|---|
| sim_proxy_profile | chengdu | shenzhen | 1 | 0.728 | 1.828 | True |  |
| sim_proxy_profile | metrla | shenzhen | 1 | 0.840 | 0.840 | False |  |
| sim_proxy_profile | pems04 | shenzhen | 1 | 3.217 | 4.346 | True |  |
| sim_proxy_profile | shenzhen | chengdu | 1 | 0.600 | 0.926 | True |  |
| sim_probe_agreement | chengdu | pems04 | 2 | 10.359 | 1.828 | False |  |
| sim_probe_agreement | metrla | shenzhen | 1 | 0.840 | 0.840 | False |  |
| sim_probe_agreement | pems04 | chengdu | 3 | 9.933 | 4.346 | False |  |
| sim_probe_agreement | shenzhen | metrla | 3 | 0.934 | 0.926 | False |  |

### metrla: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| pooled_final_labels | transfer | 0.521 | 1.342 | 1.000 | 0.181 | 0.550 | 1.000 | 0.840 | 1.000 |
| from_chengdu | transfer, one source | 0.521 | 1.342 | 1.000 | 0.181 | 0.550 | 1.000 | 0.840 | 1.000 |
| from_chengdu_k5 | transfer, one cheap source | 0.521 | 1.342 | 1.000 | 0.181 | 0.550 | 1.000 | 0.840 | 1.000 |
| from_shenzhen | transfer, one source | 0.521 | 1.342 | 1.000 | 0.181 | 0.550 | 1.000 | 0.840 | 1.000 |
| pooled_source_k10 | transfer, cheap sources | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 1.000 | 1.440 | 1.000 |
| from_shenzhen_k5 | transfer, one cheap source | 0.560 | 2.013 | 1.000 | 0.347 | 1.057 | 1.000 | 1.570 | 1.000 |
| pooled_source_k3 | transfer, cheap sources | 1.922 | 29.530 | 3.000 | 0.775 | 2.359 | 1.000 | 2.673 | 2.000 |
| from_pems04 | transfer, one source | 1.038 | 8.054 | 2.000 | 0.729 | 2.219 | 1.000 | 3.182 | 2.000 |
| pooled_source_k5 | transfer, cheap sources | 1.922 | 29.530 | 5.000 | 1.530 | 4.656 | 1.000 | 4.364 | 3.000 |
| pooled_source_k1 | transfer, cheap sources | 4.991 | 67.114 | 5.000 | 1.146 | 3.487 | 0.985 | 4.786 | 5.000 |
| from_pems04_k5 | transfer, one cheap source | 1.038 | 8.054 |  |  |  | 0.870 | 9.558 | 8.000 |

### pems04: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| pooled_source_k3 | transfer, cheap sources | 0.000 | 0.000 | 1.000 | 0.286 | 0.998 | 0.995 | 1.499 | 1.000 |
| from_metrla_k5 | transfer, one cheap source | 1.312 | 0.671 | 3.000 | 0.578 | 2.016 | 0.995 | 2.214 | 2.000 |
| pooled_source_k5 | transfer, cheap sources | 1.312 | 0.671 | 2.000 | 0.449 | 1.567 | 0.995 | 2.308 | 2.000 |
| from_shenzhen | transfer, one source | 4.087 | 6.711 | 5.000 | 0.880 | 3.071 | 0.995 | 3.217 | 3.000 |
| pooled_final_labels | transfer | 4.087 | 6.711 | 5.000 | 0.840 | 2.933 | 0.985 | 4.346 | 5.000 |
| pooled_source_k10 | transfer, cheap sources | 4.087 | 6.711 | 8.000 | 1.616 | 5.639 | 0.995 | 4.688 | 5.000 |
| from_shenzhen_k5 | transfer, one cheap source | 2.505 | 3.356 | 5.000 | 1.076 | 3.755 | 0.985 | 4.876 | 5.000 |
| from_chengdu_k5 | transfer, one cheap source | 4.087 | 6.711 | 8.000 | 1.380 | 4.818 | 0.965 | 4.957 | 5.000 |
| pooled_source_k1 | transfer, cheap sources | 4.625 | 8.725 | 5.000 | 1.139 | 3.977 | 0.975 | 5.012 | 5.000 |
| from_metrla | transfer, one source | 1.312 | 0.671 |  |  |  | 0.830 | 8.620 | 8.000 |
| from_chengdu | transfer, one source | 4.087 | 6.711 |  |  |  | 0.645 | 9.933 | 10.000 |

### chengdu: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_shenzhen | transfer, one source | 0.000 | 0.000 | 1.000 | 0.100 | 0.477 | 0.840 | 0.728 | 1.000 |
| from_shenzhen_k5 | transfer, one cheap source | 4.685 | 22.148 | 2.000 | 0.201 | 0.954 | 0.755 | 1.439 | 2.000 |
| pooled_final_labels | transfer | 2.287 | 6.040 | 2.000 | 0.257 | 1.218 | 0.755 | 1.828 | 2.000 |
| from_metrla | transfer, one source | 2.287 | 6.040 | 3.000 | 0.372 | 1.767 | 0.755 | 2.525 | 3.000 |
| pooled_source_k10 | transfer, cheap sources | 2.287 | 6.040 | 3.000 | 0.519 | 2.463 | 0.755 | 3.613 | 3.000 |
| pooled_source_k1 | transfer, cheap sources | 8.085 | 59.732 | 10.000 | 1.285 | 6.103 | 0.740 | 7.882 | 8.000 |
| pooled_source_k5 | transfer, cheap sources | 2.941 | 9.396 |  |  |  | 0.680 | 10.291 | 10.000 |
| from_pems04 | transfer, one source | 2.941 | 9.396 |  |  |  | 0.740 | 10.359 | 8.000 |
| pooled_source_k3 | transfer, cheap sources | 2.288 | 6.711 |  |  |  | 0.460 |  |  |
| from_metrla_k5 | transfer, one cheap source | 2.287 | 6.040 |  |  |  | 0.205 |  |  |
| from_pems04_k5 | transfer, one cheap source | 2.941 | 9.396 |  |  |  | 0.110 |  |  |

### shenzhen: cost to one sigma

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| from_chengdu | transfer, one source | 0.000 | 0.000 | 1.000 | 0.125 | 0.392 | 1.000 | 0.600 | 1.000 |
| from_chengdu_k5 | transfer, one cheap source | 0.000 | 0.000 | 1.000 | 0.125 | 0.392 | 1.000 | 0.600 | 1.000 |
| pooled_final_labels | transfer | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.926 | 1.000 |
| pooled_source_k10 | transfer, cheap sources | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 0.945 | 0.926 | 1.000 |
| from_metrla | transfer, one source | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 1.000 | 0.934 | 1.000 |
| from_metrla_k5 | transfer, one cheap source | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 0.790 | 0.943 | 1.000 |
| pooled_source_k1 | transfer, cheap sources | 7.052 | 31.544 | 3.000 | 0.439 | 1.373 | 0.730 | 2.053 | 3.000 |
| from_pems04 | transfer, one source | 2.965 | 2.685 | 2.000 | 0.564 | 1.765 | 0.920 | 2.646 | 2.000 |
| pooled_source_k3 | transfer, cheap sources | 5.339 | 17.450 | 5.000 | 0.945 | 2.955 | 0.915 | 4.028 | 5.000 |
| pooled_source_k5 | transfer, cheap sources | 2.965 | 2.685 | 5.000 | 1.197 | 3.743 | 0.915 | 4.298 | 3.000 |
| from_pems04_k5 | transfer, one cheap source | 2.965 | 2.685 |  |  |  | 0.045 |  |  |
