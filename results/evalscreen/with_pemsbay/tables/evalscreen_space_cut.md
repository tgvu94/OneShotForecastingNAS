# evalscreen space_cut: a reduced search space learned from the labels of the other cities

Choices: ['seq_family', 'graph_family', 'flat_family', 'decoder'] (single) and their pairs. Greedy rule on three cities: remove the choice whose architectures rank lowest inside their heads, when it is below the mean of the remaining list at every training city that holds three or more of them; stop at the keep fraction. The rule never sees the head, and the rank is taken inside the head. Line: the reduced list of the held-out city holds at most half of the list and 13 or more of the top 15, and five random picks inside it have a lower expected regret than ten random picks in the full list, at three of four cities. ref_* = a list filter, not a rule on the space.

### Verdict

| cut | cities_ok | kept_share_mean | top15_kept_min | pass |
|---|---|---|---|---|
| learned_pairs_keep25 | 0 | 0.569 | 5 | False |
| learned_pairs_keep50 | 0 | 0.592 | 8 | False |
| learned_single_keep25 | 0 | 0.363 | 3 | False |
| learned_single_keep50 | 0 | 0.441 | 6 | False |
| ref_pooled_transfer_top_half | 3 | 0.500 | 14 | True |
| ref_zico_sizectrl_top_half | 1 | 0.500 | 9 | False |

### Every cut at every held-out city

| city | cut | kept_share | top15_kept | best_kept | mae_head_top4_kept | random5_inside_sigma | random10_full_sigma | rules_removed | ok |
|---|---|---|---|---|---|---|---|---|---|
| metrla | learned_single_keep50 | 0.440 | 9 | True | 2 | 2.760 | 2.267 | seq_family=gru; seq_family=sep_tcn; seq_family=skip_connection; seq_family=tcn | False |
| metrla | learned_single_keep25 | 0.440 | 9 | True | 2 | 2.774 | 2.267 | seq_family=gru; seq_family=sep_tcn; seq_family=skip_connection; seq_family=tcn | False |
| metrla | learned_pairs_keep50 | 0.700 | 14 | True | 4 | 2.868 | 2.267 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s | False |
| metrla | learned_pairs_keep25 | 0.700 | 14 | True | 4 | 2.833 | 2.267 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s | False |
| metrla | ref_zico_sizectrl_top_half | 0.500 | 13 | True | 4 | 2.426 | 2.267 |  | False |
| metrla | ref_pooled_transfer_top_half | 0.500 | 14 | True | 4 | 2.226 | 2.267 |  | True |
| pems04 | learned_single_keep50 | 0.440 | 10 | True | 3 | 3.457 | 2.968 | seq_family=gru; seq_family=skip_connection; seq_family=sep_tcn; seq_family=tcn | False |
| pems04 | learned_single_keep25 | 0.347 | 9 | True | 3 | 3.443 | 2.968 | seq_family=gru; seq_family=skip_connection; seq_family=sep_tcn; seq_family=tcn; seq_family=transformer | False |
| pems04 | learned_pairs_keep50 | 0.447 | 8 | False | 3 | 4.241 | 2.968 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; flat_family=skip_connection&decoder=linear; seq_family=tcn&flat_family=nbeats_s; seq_family=transformer&flat_family=nbeats_g; graph_family=mixed | False |
| pems04 | learned_pairs_keep25 | 0.447 | 8 | False | 3 | 4.213 | 2.968 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; flat_family=skip_connection&decoder=linear; seq_family=tcn&flat_family=nbeats_s; seq_family=transformer&flat_family=nbeats_g; graph_family=mixed | False |
| pems04 | ref_zico_sizectrl_top_half | 0.500 | 15 | True | 4 | 2.943 | 2.968 |  | True |
| pems04 | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 2.995 | 2.968 |  | False |
| chengdu | learned_single_keep50 | 0.473 | 8 | False | 1 | 3.650 | 2.569 | seq_family=gru; seq_family=sep_tcn; seq_family=skip_connection; flat_family=skip_connection; graph_family=adaptive-only | False |
| chengdu | learned_single_keep25 | 0.313 | 7 | False | 1 | 3.173 | 2.569 | seq_family=gru; seq_family=sep_tcn; seq_family=skip_connection; flat_family=skip_connection; graph_family=adaptive-only; seq_family=tcn | False |
| chengdu | learned_pairs_keep50 | 0.620 | 14 | True | 4 | 2.930 | 2.569 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s; seq_family=lstm&flat_family=skip_connection; seq_family=tcn&flat_family=mlp | False |
| chengdu | learned_pairs_keep25 | 0.620 | 14 | True | 4 | 2.899 | 2.569 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s; seq_family=lstm&flat_family=skip_connection; seq_family=tcn&flat_family=mlp | False |
| chengdu | ref_zico_sizectrl_top_half | 0.500 | 14 | True | 4 | 2.789 | 2.569 |  | False |
| chengdu | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 2.630 | 2.569 |  | False |
| shenzhen | learned_single_keep50 | 0.440 | 9 | False | 2 | 4.174 | 3.494 | seq_family=gru; seq_family=sep_tcn; seq_family=skip_connection; seq_family=tcn | False |
| shenzhen | learned_single_keep25 | 0.440 | 9 | False | 2 | 4.170 | 3.494 | seq_family=gru; seq_family=sep_tcn; seq_family=skip_connection; seq_family=tcn | False |
| shenzhen | learned_pairs_keep50 | 0.700 | 15 | True | 4 | 4.021 | 3.494 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s | False |
| shenzhen | learned_pairs_keep25 | 0.700 | 15 | True | 4 | 4.034 | 3.494 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s | False |
| shenzhen | ref_zico_sizectrl_top_half | 0.500 | 14 | True | 4 | 3.562 | 3.494 |  | False |
| shenzhen | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 3.418 | 3.494 |  | True |
| expytky | learned_single_keep50 | 0.440 | 8 | False | 2 | 4.924 | 3.969 | seq_family=gru; seq_family=skip_connection; seq_family=sep_tcn; seq_family=tcn | False |
| expytky | learned_single_keep25 | 0.440 | 8 | False | 2 | 4.938 | 3.969 | seq_family=gru; seq_family=skip_connection; seq_family=sep_tcn; seq_family=tcn | False |
| expytky | learned_pairs_keep50 | 0.593 | 10 | True | 3 | 4.760 | 3.969 | seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s; seq_family=lstm&flat_family=mlp; graph_family=mixed&flat_family=mlp | False |
| expytky | learned_pairs_keep25 | 0.593 | 10 | True | 3 | 4.791 | 3.969 | seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=skip_connection&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s; seq_family=lstm&flat_family=mlp; graph_family=mixed&flat_family=mlp | False |
| expytky | ref_zico_sizectrl_top_half | 0.500 | 10 | True | 4 | 4.476 | 3.969 |  | False |
| expytky | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 3.958 | 3.969 |  | True |
| pemsbay | learned_single_keep50 | 0.413 | 6 | True | 2 | 3.653 | 2.524 | decoder=linear; seq_family=gru; flat_family=nbeats_s | False |
| pemsbay | learned_single_keep25 | 0.200 | 3 | True | 2 | 3.185 | 2.524 | decoder=linear; seq_family=gru; flat_family=nbeats_s; seq_family=lstm; seq_family=tcn | False |
| pemsbay | learned_pairs_keep50 | 0.493 | 8 | True | 4 | 3.467 | 2.524 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; flat_family=mlp&decoder=linear; seq_family=tcn&flat_family=nbeats_s; seq_family=tcn&graph_family=none | False |
| pemsbay | learned_pairs_keep25 | 0.353 | 5 | True | 3 | 3.481 | 2.524 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; flat_family=mlp&decoder=linear; seq_family=tcn&flat_family=nbeats_s; seq_family=tcn&graph_family=none; seq_family=lstm&flat_family=skip_connection; flat_family=nbeats_s | False |
| pemsbay | ref_zico_sizectrl_top_half | 0.500 | 9 | True | 3 | 3.297 | 2.524 |  | False |
| pemsbay | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 2.527 | 2.524 |  | False |

### metrla: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 0.475 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 16.495 | 91.946 | 8.000 | 1.644 | 5.001 | 0.490 |  |  |
| random_inside_learned_single_keep50 | random in a reduced list | 15.077 | 83.221 |  |  |  | 0.350 |  |  |
| random_inside_learned_single_keep25 | random in a reduced list | 15.077 | 83.221 |  |  |  | 0.350 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 2.555 | 8.054 |  |  |  | 0.375 |  |  |
| random_inside_learned_pairs_keep25 | random in a reduced list | 2.555 | 8.054 |  |  |  | 0.375 |  |  |
| random_full_list | floor | 8.158 | 55.705 |  |  |  | 0.265 |  |  |

### pems04: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_single_keep25 | random in a reduced list | 13.485 | 76.510 |  |  |  | 0.585 | 8.696 | 10.000 |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 17.588 | 92.617 | 3.000 | 0.509 | 1.776 | 0.440 |  |  |
| random_inside_learned_single_keep50 | random in a reduced list | 6.991 | 24.161 | 8.000 | 1.644 | 5.739 | 0.470 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 10.423 | 51.007 | 8.000 | 1.689 | 5.896 | 0.500 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 5.914 | 16.779 |  |  |  | 0.335 |  |  |
| random_inside_learned_pairs_keep25 | random in a reduced list | 5.914 | 16.779 |  |  |  | 0.335 |  |  |
| random_full_list | floor | 14.325 | 80.537 |  |  |  | 0.285 |  |  |

### chengdu: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 0.429 | 0.671 | 1.000 | 0.093 | 0.441 | 0.380 |  |  |
| random_inside_learned_single_keep50 | random in a reduced list | 7.445 | 48.993 | 8.000 | 1.333 | 6.329 | 0.155 |  |  |
| random_inside_learned_single_keep25 | random in a reduced list | 13.713 | 93.289 |  |  |  | 0.245 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 2.287 | 6.040 |  |  |  | 0.300 |  |  |
| random_inside_learned_pairs_keep25 | random in a reduced list | 2.287 | 6.040 |  |  |  | 0.300 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 1.944 | 4.027 |  |  |  | 0.195 |  |  |
| random_full_list | floor | 16.013 | 98.658 |  |  |  | 0.175 |  |  |

### shenzhen: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 0.965 | 0.671 | 1.000 | 0.198 | 0.620 | 0.370 |  |  |
| random_inside_learned_single_keep50 | random in a reduced list | 9.860 | 61.745 |  |  |  | 0.180 |  |  |
| random_inside_learned_single_keep25 | random in a reduced list | 9.860 | 61.745 |  |  |  | 0.180 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 2.965 | 2.685 |  |  |  | 0.255 |  |  |
| random_inside_learned_pairs_keep25 | random in a reduced list | 2.965 | 2.685 |  |  |  | 0.255 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 5.455 | 18.792 |  |  |  | 0.310 |  |  |
| random_full_list | floor | 12.366 | 81.879 |  |  |  | 0.145 |  |  |

### expytky: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 6.621 | 21.477 | 8.000 | 3.030 | 5.361 | 0.335 |  |  |
| random_inside_learned_single_keep50 | random in a reduced list | 11.160 | 78.523 |  |  |  | 0.085 |  |  |
| random_inside_learned_single_keep25 | random in a reduced list | 11.160 | 78.523 |  |  |  | 0.085 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 10.584 | 70.470 |  |  |  | 0.260 |  |  |
| random_inside_learned_pairs_keep25 | random in a reduced list | 10.584 | 70.470 |  |  |  | 0.260 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 6.632 | 22.148 |  |  |  | 0.355 |  |  |
| random_full_list | floor | 12.387 | 87.919 |  |  |  | 0.150 |  |  |

### pemsbay: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 19.160 | 93.960 | 8.000 | 4.998 | 6.894 | 0.310 |  |  |
| random_inside_learned_single_keep50 | random in a reduced list | 9.957 | 59.732 |  |  |  | 0.225 |  |  |
| random_inside_learned_single_keep25 | random in a reduced list | 5.585 | 33.557 |  |  |  | 0.430 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 7.426 | 49.664 |  |  |  | 0.390 |  |  |
| random_inside_learned_pairs_keep25 | random in a reduced list | 15.612 | 84.564 |  |  |  | 0.435 |  |  |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 8.294 | 53.691 |  |  |  | 0.390 |  |  |
| random_full_list | floor | 8.101 | 53.020 |  |  |  | 0.245 |  |  |
