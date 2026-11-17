# evalscreen space_cut: a reduced search space learned from the labels of the other cities

Choices: ['seq_family', 'graph_family', 'flat_family', 'decoder'] (single) and their pairs. Greedy rule on three cities: remove the choice whose architectures rank lowest inside their heads, when it is below the mean of the remaining list at every training city that holds three or more of them; stop at the keep fraction. The rule never sees the head, and the rank is taken inside the head. Line: the reduced list of the held-out city holds at most half of the list and 13 or more of the top 15, and five random picks inside it have a lower expected regret than ten random picks in the full list, at three of four cities. ref_* = a list filter, not a rule on the space.

### Verdict

| cut | cities_ok | kept_share_mean | top15_kept_min | pass |
|---|---|---|---|---|
| learned_pairs_keep25 | 0 | 0.260 | 6 | False |
| learned_pairs_keep50 | 3 | 0.437 | 8 | True |
| learned_single_keep25 | 0 | 0.212 | 7 | False |
| learned_single_keep50 | 2 | 0.393 | 11 | False |
| ref_pooled_transfer_top_half | 4 | 0.500 | 15 | True |
| ref_zico_sizectrl_top_half | 1 | 0.500 | 13 | False |

### Every cut at every held-out city

| city | cut | kept_share | top15_kept | best_kept | mae_head_top4_kept | random5_inside_sigma | random10_full_sigma | rules_removed | ok |
|---|---|---|---|---|---|---|---|---|---|
| metrla | learned_single_keep50 | 0.393 | 11 | True | 4 | 2.344 | 2.267 | decoder=linear; seq_family=gru; seq_family=tcn | False |
| metrla | learned_single_keep25 | 0.200 | 7 | True | 4 | 1.806 | 2.267 | decoder=linear; seq_family=gru; seq_family=tcn; seq_family=lstm; flat_family=nbeats_s | False |
| metrla | learned_pairs_keep50 | 0.400 | 8 | True | 4 | 2.638 | 2.267 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; seq_family=gru&flat_family=skip_connection; graph_family=mixed&decoder=linear; seq_family=lstm&decoder=linear; seq_family=tcn&decoder=linear; seq_family=mlp_mix&decoder=linear; decoder=linear; seq_family=tcn&graph_family=none; flat_family=nbeats_s | False |
| metrla | learned_pairs_keep25 | 0.293 | 8 | True | 4 | 2.192 | 2.267 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; seq_family=gru&flat_family=skip_connection; graph_family=mixed&decoder=linear; seq_family=lstm&decoder=linear; seq_family=tcn&decoder=linear; seq_family=mlp_mix&decoder=linear; decoder=linear; seq_family=tcn&graph_family=none; flat_family=nbeats_s; seq_family=lstm&flat_family=skip_connection; seq_family=lstm&flat_family=mlp; graph_family=mixed&flat_family=nbeats_t | False |
| metrla | ref_zico_sizectrl_top_half | 0.500 | 13 | True | 4 | 2.426 | 2.267 |  | False |
| metrla | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 2.232 | 2.267 |  | True |
| pems04 | learned_single_keep50 | 0.393 | 12 | True | 3 | 2.728 | 2.968 | decoder=linear; seq_family=gru; seq_family=tcn | False |
| pems04 | learned_single_keep25 | 0.247 | 7 | True | 2 | 2.708 | 2.968 | decoder=linear; seq_family=gru; seq_family=tcn; graph_family=diffusion; seq_family=lstm | False |
| pems04 | learned_pairs_keep50 | 0.487 | 15 | True | 4 | 2.875 | 2.968 | graph_family=adaptive-only&decoder=linear; seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s; flat_family=mlp&decoder=linear; seq_family=tcn&graph_family=none | True |
| pems04 | learned_pairs_keep25 | 0.213 | 6 | True | 2 | 2.542 | 2.968 | graph_family=adaptive-only&decoder=linear; seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s; flat_family=mlp&decoder=linear; seq_family=tcn&graph_family=none; graph_family=diffusion; seq_family=lstm&graph_family=mixed; graph_family=adaptive-only; seq_family=lstm; seq_family=tcn | False |
| pems04 | ref_zico_sizectrl_top_half | 0.500 | 15 | True | 4 | 2.943 | 2.968 |  | True |
| pems04 | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 2.918 | 2.968 |  | True |
| chengdu | learned_single_keep50 | 0.393 | 13 | True | 4 | 2.332 | 2.569 | decoder=linear; seq_family=gru; seq_family=tcn | True |
| chengdu | learned_single_keep25 | 0.200 | 11 | True | 3 | 1.855 | 2.569 | decoder=linear; seq_family=gru; seq_family=tcn; seq_family=lstm; flat_family=nbeats_s | False |
| chengdu | learned_pairs_keep50 | 0.473 | 15 | True | 4 | 2.454 | 2.569 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; seq_family=gru&flat_family=skip_connection; seq_family=tcn&decoder=linear; seq_family=lstm&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru; seq_family=tcn&graph_family=none; seq_family=mlp_mix&decoder=linear; seq_family=lstm&flat_family=skip_connection | True |
| chengdu | learned_pairs_keep25 | 0.213 | 9 | True | 3 | 2.023 | 2.569 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; seq_family=gru&flat_family=skip_connection; seq_family=tcn&decoder=linear; seq_family=lstm&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru; seq_family=tcn&graph_family=none; seq_family=mlp_mix&decoder=linear; seq_family=lstm&flat_family=skip_connection; flat_family=nbeats_s; seq_family=lstm&flat_family=mlp; seq_family=mlp_mix&graph_family=none; seq_family=tcn | False |
| chengdu | ref_zico_sizectrl_top_half | 0.500 | 14 | True | 4 | 2.789 | 2.569 |  | False |
| chengdu | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 2.538 | 2.569 |  | True |
| shenzhen | learned_single_keep50 | 0.393 | 13 | True | 4 | 3.226 | 3.494 | decoder=linear; seq_family=gru; seq_family=tcn | True |
| shenzhen | learned_single_keep25 | 0.200 | 8 | True | 4 | 2.461 | 3.494 | decoder=linear; seq_family=gru; seq_family=tcn; seq_family=lstm; flat_family=nbeats_s | False |
| shenzhen | learned_pairs_keep50 | 0.387 | 13 | True | 4 | 3.219 | 3.494 | seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&decoder=linear; flat_family=mlp&decoder=linear; seq_family=tcn&graph_family=none; flat_family=nbeats_s | True |
| shenzhen | learned_pairs_keep25 | 0.320 | 11 | True | 4 | 3.090 | 3.494 | seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&decoder=linear; flat_family=mlp&decoder=linear; seq_family=tcn&graph_family=none; flat_family=nbeats_s; seq_family=lstm&flat_family=mlp; seq_family=lstm&flat_family=skip_connection | False |
| shenzhen | ref_zico_sizectrl_top_half | 0.500 | 14 | True | 4 | 3.562 | 3.494 |  | False |
| shenzhen | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 3.384 | 3.494 |  | True |

### metrla: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_single_keep25 | random in a reduced list | 4.383 | 25.503 |  |  |  | 0.675 | 8.639 | 8.000 |
| random_inside_learned_single_keep50 | random in a reduced list | 11.513 | 63.758 |  |  |  | 0.530 | 9.967 | 10.000 |
| random_inside_learned_pairs_keep25 | random in a reduced list | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 0.590 | 10.576 | 10.000 |
| random_inside_learned_pairs_keep50 | random in a reduced list | 4.871 | 31.544 |  |  |  | 0.510 | 12.029 | 10.000 |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 16.495 | 91.946 | 8.000 | 1.644 | 5.001 | 0.490 |  |  |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 5.482 | 36.242 | 8.000 | 1.928 | 5.865 | 0.495 |  |  |
| random_full_list | floor | 8.158 | 55.705 |  |  |  | 0.265 |  |  |

### pems04: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_pairs_keep25 | random in a reduced list | 12.891 | 71.812 | 8.000 | 1.408 | 4.914 | 0.585 | 8.420 | 8.000 |
| random_inside_learned_single_keep50 | random in a reduced list | 9.933 | 48.322 | 5.000 | 0.921 | 3.214 | 0.545 | 9.897 | 10.000 |
| random_inside_learned_pairs_keep50 | random in a reduced list | 15.700 | 86.577 |  |  |  | 0.540 | 9.982 | 10.000 |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.455 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 10.423 | 51.007 | 8.000 | 1.689 | 5.896 | 0.500 |  |  |
| random_inside_learned_single_keep25 | random in a reduced list | 8.601 | 36.913 | 10.000 | 1.742 | 6.079 | 0.495 |  |  |
| random_full_list | floor | 14.325 | 80.537 |  |  |  | 0.285 |  |  |

### chengdu: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_single_keep50 | random in a reduced list | 6.312 | 32.886 |  |  |  | 0.370 |  |  |
| random_inside_learned_single_keep25 | random in a reduced list | 8.051 | 57.718 |  |  |  | 0.425 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 1.917 | 3.356 |  |  |  | 0.395 |  |  |
| random_inside_learned_pairs_keep25 | random in a reduced list | 7.597 | 53.020 |  |  |  | 0.415 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 1.944 | 4.027 |  |  |  | 0.195 |  |  |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 6.653 | 38.255 |  |  |  | 0.340 |  |  |
| random_full_list | floor | 16.013 | 98.658 |  |  |  | 0.175 |  |  |

### shenzhen: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_single_keep25 | random in a reduced list | 9.862 | 62.416 |  |  |  | 0.625 | 8.115 | 8.000 |
| random_inside_learned_pairs_keep25 | random in a reduced list | 5.402 | 18.121 |  |  |  | 0.505 | 11.794 | 10.000 |
| random_inside_learned_single_keep50 | random in a reduced list | 11.321 | 73.826 |  |  |  | 0.385 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 2.318 | 2.013 |  |  |  | 0.395 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 5.455 | 18.792 |  |  |  | 0.310 |  |  |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 6.111 | 22.148 |  |  |  | 0.395 |  |  |
| random_full_list | floor | 12.366 | 81.879 |  |  |  | 0.145 |  |  |
