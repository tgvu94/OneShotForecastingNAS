# evalscreen space_cut: a reduced search space learned from the labels of the other cities

Choices: ['seq_family', 'graph_family', 'flat_family', 'decoder'] (single) and their pairs. Greedy rule on three cities: remove the choice whose architectures rank lowest inside their heads, when it is below the mean of the remaining list at every training city that holds three or more of them; stop at the keep fraction. The rule never sees the head, and the rank is taken inside the head. Line: the reduced list of the held-out city holds at most half of the list and 13 or more of the top 15, and five random picks inside it have a lower expected regret than ten random picks in the full list, at three of four cities. ref_* = a list filter, not a rule on the space.

### Verdict

| cut | cities_ok | kept_share_mean | top15_kept_min | pass |
|---|---|---|---|---|
| learned_pairs_keep25 | 2 | 0.321 | 8 | False |
| learned_pairs_keep50 | 2 | 0.493 | 12 | False |
| learned_single_keep25 | 0 | 0.219 | 6 | False |
| learned_single_keep50 | 2 | 0.405 | 9 | False |
| ref_pooled_transfer_top_half | 3 | 0.500 | 15 | True |
| ref_zico_sizectrl_top_half | 1 | 0.500 | 10 | False |

### Every cut at every held-out city

| city | cut | kept_share | top15_kept | best_kept | mae_head_top4_kept | random5_inside_sigma | random10_full_sigma | rules_removed | ok |
|---|---|---|---|---|---|---|---|---|---|
| metrla | learned_single_keep50 | 0.413 | 9 | True | 4 | 2.555 | 2.267 | decoder=linear; seq_family=gru; flat_family=nbeats_s | False |
| metrla | learned_single_keep25 | 0.200 | 7 | True | 4 | 1.806 | 2.267 | decoder=linear; seq_family=gru; flat_family=nbeats_s; seq_family=lstm; seq_family=tcn | False |
| metrla | learned_pairs_keep50 | 0.493 | 12 | True | 4 | 2.521 | 2.267 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; graph_family=mixed&decoder=linear; flat_family=mlp&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s; seq_family=tcn&graph_family=none | False |
| metrla | learned_pairs_keep25 | 0.353 | 9 | True | 4 | 2.376 | 2.267 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; graph_family=mixed&decoder=linear; flat_family=mlp&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s; seq_family=tcn&graph_family=none; seq_family=lstm&flat_family=skip_connection; flat_family=nbeats_s | False |
| metrla | ref_zico_sizectrl_top_half | 0.500 | 13 | True | 4 | 2.426 | 2.267 |  | False |
| metrla | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 2.222 | 2.267 |  | True |
| pems04 | learned_single_keep50 | 0.393 | 12 | True | 3 | 2.728 | 2.968 | decoder=linear; seq_family=gru; seq_family=tcn | False |
| pems04 | learned_single_keep25 | 0.247 | 7 | True | 2 | 2.708 | 2.968 | decoder=linear; seq_family=gru; seq_family=tcn; graph_family=diffusion; seq_family=lstm | False |
| pems04 | learned_pairs_keep50 | 0.500 | 15 | True | 4 | 3.021 | 2.968 | seq_family=sep_tcn&decoder=linear; graph_family=adaptive-only&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=skip_connection&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; graph_family=diffusion&decoder=linear; seq_family=tcn&flat_family=nbeats_s; decoder=linear | False |
| pems04 | learned_pairs_keep25 | 0.227 | 8 | True | 2 | 2.327 | 2.968 | seq_family=sep_tcn&decoder=linear; graph_family=adaptive-only&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=skip_connection&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; graph_family=diffusion&decoder=linear; seq_family=tcn&flat_family=nbeats_s; decoder=linear; seq_family=lstm&graph_family=mixed; seq_family=tcn&graph_family=none; seq_family=lstm; flat_family=nbeats_s; graph_family=adaptive-only | False |
| pems04 | ref_zico_sizectrl_top_half | 0.500 | 15 | True | 4 | 2.943 | 2.968 |  | True |
| pems04 | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 2.963 | 2.968 |  | True |
| chengdu | learned_single_keep50 | 0.413 | 13 | True | 3 | 2.560 | 2.569 | decoder=linear; seq_family=gru; flat_family=nbeats_s | True |
| chengdu | learned_single_keep25 | 0.247 | 6 | False | 1 | 3.137 | 2.569 | decoder=linear; seq_family=gru; flat_family=nbeats_s; graph_family=none | False |
| chengdu | learned_pairs_keep50 | 0.487 | 15 | True | 4 | 2.510 | 2.569 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; graph_family=mixed&decoder=linear; seq_family=tcn&decoder=linear; flat_family=mlp&decoder=linear; seq_family=tcn&graph_family=none; seq_family=lstm&flat_family=skip_connection | True |
| chengdu | learned_pairs_keep25 | 0.353 | 13 | True | 3 | 2.351 | 2.569 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; graph_family=mixed&decoder=linear; seq_family=tcn&decoder=linear; flat_family=mlp&decoder=linear; seq_family=tcn&graph_family=none; seq_family=lstm&flat_family=skip_connection; flat_family=nbeats_s | True |
| chengdu | ref_zico_sizectrl_top_half | 0.500 | 14 | True | 4 | 2.789 | 2.569 |  | False |
| chengdu | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 2.611 | 2.569 |  | False |
| shenzhen | learned_single_keep50 | 0.413 | 13 | True | 4 | 3.313 | 3.494 | decoder=linear; seq_family=gru; flat_family=nbeats_s | True |
| shenzhen | learned_single_keep25 | 0.200 | 8 | True | 4 | 2.461 | 3.494 | decoder=linear; seq_family=gru; flat_family=nbeats_s; seq_family=lstm; seq_family=tcn | False |
| shenzhen | learned_pairs_keep50 | 0.493 | 15 | True | 4 | 3.448 | 3.494 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; graph_family=mixed&decoder=linear; flat_family=mlp&decoder=linear; seq_family=tcn&flat_family=nbeats_s; seq_family=tcn&graph_family=none | True |
| shenzhen | learned_pairs_keep25 | 0.353 | 13 | True | 4 | 3.057 | 3.494 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; graph_family=mixed&decoder=linear; flat_family=mlp&decoder=linear; seq_family=tcn&flat_family=nbeats_s; seq_family=tcn&graph_family=none; seq_family=lstm&flat_family=skip_connection; flat_family=nbeats_s | True |
| shenzhen | ref_zico_sizectrl_top_half | 0.500 | 14 | True | 4 | 3.562 | 3.494 |  | False |
| shenzhen | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 3.387 | 3.494 |  | True |
| expytky | learned_single_keep50 | 0.393 | 9 | True | 4 | 4.008 | 3.969 | decoder=linear; seq_family=gru; seq_family=tcn | False |
| expytky | learned_single_keep25 | 0.200 | 6 | True | 3 | 3.447 | 3.969 | decoder=linear; seq_family=gru; seq_family=tcn; seq_family=lstm; flat_family=nbeats_s | False |
| expytky | learned_pairs_keep50 | 0.493 | 13 | True | 4 | 4.152 | 3.969 | seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; flat_family=mlp&decoder=linear; seq_family=tcn&flat_family=nbeats_s; seq_family=tcn&graph_family=none | False |
| expytky | learned_pairs_keep25 | 0.320 | 10 | True | 3 | 3.891 | 3.969 | seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; flat_family=mlp&decoder=linear; seq_family=tcn&flat_family=nbeats_s; seq_family=tcn&graph_family=none; seq_family=lstm&flat_family=skip_connection; seq_family=lstm&flat_family=mlp; flat_family=nbeats_s | False |
| expytky | ref_zico_sizectrl_top_half | 0.500 | 10 | True | 4 | 4.476 | 3.969 |  | False |
| expytky | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 3.995 | 3.969 |  | False |

### metrla: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_single_keep25 | random in a reduced list | 4.383 | 25.503 |  |  |  | 0.675 | 8.639 | 8.000 |
| random_inside_learned_pairs_keep25 | random in a reduced list | 16.212 | 89.262 |  |  |  | 0.565 | 10.573 | 8.000 |
| random_inside_learned_pairs_keep50 | random in a reduced list | 4.019 | 22.148 |  |  |  | 0.505 | 12.978 | 10.000 |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 16.495 | 91.946 | 8.000 | 1.644 | 5.001 | 0.490 |  |  |
| random_inside_learned_single_keep50 | random in a reduced list | 11.513 | 63.758 | 10.000 | 2.236 | 6.804 | 0.490 |  |  |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 11.705 | 65.101 |  |  |  | 0.490 |  |  |
| random_full_list | floor | 8.158 | 55.705 |  |  |  | 0.265 |  |  |

### pems04: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_pairs_keep25 | random in a reduced list | 4.303 | 12.081 |  |  |  | 0.705 | 8.145 | 8.000 |
| random_inside_learned_pairs_keep50 | random in a reduced list | 17.588 | 92.617 |  |  |  | 0.550 | 9.137 | 8.000 |
| random_inside_learned_single_keep50 | random in a reduced list | 9.933 | 48.322 | 5.000 | 0.921 | 3.214 | 0.545 | 9.897 | 10.000 |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 0.846 | 0.671 | 1.000 | 0.163 | 0.568 | 0.510 | 10.512 | 10.000 |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 10.423 | 51.007 | 8.000 | 1.689 | 5.896 | 0.500 |  |  |
| random_inside_learned_single_keep25 | random in a reduced list | 8.601 | 36.913 | 10.000 | 1.742 | 6.079 | 0.495 |  |  |
| random_full_list | floor | 14.325 | 80.537 |  |  |  | 0.285 |  |  |

### chengdu: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 0.429 | 0.671 | 1.000 | 0.093 | 0.441 | 0.365 |  |  |
| random_inside_learned_single_keep50 | random in a reduced list | 6.312 | 32.886 | 2.000 | 0.179 | 0.848 | 0.260 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 6.400 | 34.899 | 8.000 | 1.411 | 6.699 | 0.365 |  |  |
| random_inside_learned_single_keep25 | random in a reduced list | 1.917 | 3.356 |  |  |  | 0.070 |  |  |
| random_inside_learned_pairs_keep25 | random in a reduced list | 7.490 | 51.007 |  |  |  | 0.250 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 1.944 | 4.027 |  |  |  | 0.195 |  |  |
| random_full_list | floor | 16.013 | 98.658 |  |  |  | 0.175 |  |  |

### shenzhen: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_single_keep25 | random in a reduced list | 9.862 | 62.416 |  |  |  | 0.625 | 8.115 | 8.000 |
| random_inside_learned_single_keep50 | random in a reduced list | 11.321 | 73.826 | 2.000 | 0.199 | 0.623 | 0.385 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 4.379 | 10.738 |  |  |  | 0.375 |  |  |
| random_inside_learned_pairs_keep25 | random in a reduced list | 8.537 | 46.980 |  |  |  | 0.460 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 5.455 | 18.792 |  |  |  | 0.310 |  |  |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 7.763 | 38.926 |  |  |  | 0.320 |  |  |
| random_full_list | floor | 12.366 | 81.879 |  |  |  | 0.145 |  |  |

### expytky: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_single_keep25 | random in a reduced list | 5.370 | 14.765 |  |  |  | 0.515 | 9.344 | 10.000 |
| random_inside_learned_single_keep50 | random in a reduced list | 9.950 | 65.101 |  |  |  | 0.430 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 5.471 | 15.436 |  |  |  | 0.400 |  |  |
| random_inside_learned_pairs_keep25 | random in a reduced list | 7.780 | 31.544 |  |  |  | 0.350 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 6.632 | 22.148 |  |  |  | 0.355 |  |  |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 1.455 | 2.013 |  |  |  | 0.370 |  |  |
| random_full_list | floor | 12.387 | 87.919 |  |  |  | 0.150 |  |  |
