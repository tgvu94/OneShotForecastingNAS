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
| metrla | learned_single_keep50 | 0.393 | 11 | True | 4 | 0.952 | 0.921 | decoder=linear; seq_family=gru; seq_family=tcn | False |
| metrla | learned_single_keep25 | 0.200 | 7 | True | 4 | 0.733 | 0.921 | decoder=linear; seq_family=gru; seq_family=tcn; seq_family=lstm; flat_family=nbeats_s | False |
| metrla | learned_pairs_keep50 | 0.400 | 8 | True | 4 | 1.071 | 0.921 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; seq_family=gru&flat_family=skip_connection; graph_family=mixed&decoder=linear; seq_family=lstm&decoder=linear; seq_family=tcn&decoder=linear; seq_family=mlp_mix&decoder=linear; decoder=linear; seq_family=tcn&graph_family=none; flat_family=nbeats_s | False |
| metrla | learned_pairs_keep25 | 0.293 | 8 | True | 4 | 0.890 | 0.921 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; seq_family=gru&flat_family=skip_connection; graph_family=mixed&decoder=linear; seq_family=lstm&decoder=linear; seq_family=tcn&decoder=linear; seq_family=mlp_mix&decoder=linear; decoder=linear; seq_family=tcn&graph_family=none; flat_family=nbeats_s; seq_family=lstm&flat_family=skip_connection; seq_family=lstm&flat_family=mlp; graph_family=mixed&flat_family=nbeats_t | False |
| metrla | ref_zico_sizectrl_top_half | 0.500 | 13 | True | 4 | 0.985 | 0.921 |  | False |
| metrla | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 0.906 | 0.921 |  | True |
| pems04 | learned_single_keep50 | 0.393 | 12 | True | 3 | 4.231 | 4.604 | decoder=linear; seq_family=gru; seq_family=tcn | False |
| pems04 | learned_single_keep25 | 0.247 | 7 | True | 2 | 4.200 | 4.604 | decoder=linear; seq_family=gru; seq_family=tcn; graph_family=diffusion; seq_family=lstm | False |
| pems04 | learned_pairs_keep50 | 0.487 | 15 | True | 4 | 4.460 | 4.604 | graph_family=adaptive-only&decoder=linear; seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s; flat_family=mlp&decoder=linear; seq_family=tcn&graph_family=none | True |
| pems04 | learned_pairs_keep25 | 0.213 | 6 | True | 2 | 3.943 | 4.604 | graph_family=adaptive-only&decoder=linear; seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&flat_family=nbeats_s; flat_family=mlp&decoder=linear; seq_family=tcn&graph_family=none; graph_family=diffusion; seq_family=lstm&graph_family=mixed; graph_family=adaptive-only; seq_family=lstm; seq_family=tcn | False |
| pems04 | ref_zico_sizectrl_top_half | 0.500 | 15 | True | 4 | 4.566 | 4.604 |  | True |
| pems04 | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 4.526 | 4.604 |  | True |
| chengdu | learned_single_keep50 | 0.393 | 13 | True | 4 | 1.701 | 1.874 | decoder=linear; seq_family=gru; seq_family=tcn | True |
| chengdu | learned_single_keep25 | 0.200 | 11 | True | 3 | 1.353 | 1.874 | decoder=linear; seq_family=gru; seq_family=tcn; seq_family=lstm; flat_family=nbeats_s | False |
| chengdu | learned_pairs_keep50 | 0.473 | 15 | True | 4 | 1.790 | 1.874 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; seq_family=gru&flat_family=skip_connection; seq_family=tcn&decoder=linear; seq_family=lstm&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru; seq_family=tcn&graph_family=none; seq_family=mlp_mix&decoder=linear; seq_family=lstm&flat_family=skip_connection | True |
| chengdu | learned_pairs_keep25 | 0.213 | 9 | True | 3 | 1.475 | 1.874 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; seq_family=gru&flat_family=skip_connection; seq_family=tcn&decoder=linear; seq_family=lstm&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru; seq_family=tcn&graph_family=none; seq_family=mlp_mix&decoder=linear; seq_family=lstm&flat_family=skip_connection; flat_family=nbeats_s; seq_family=lstm&flat_family=mlp; seq_family=mlp_mix&graph_family=none; seq_family=tcn | False |
| chengdu | ref_zico_sizectrl_top_half | 0.500 | 14 | True | 4 | 2.034 | 1.874 |  | False |
| chengdu | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 1.851 | 1.874 |  | True |
| shenzhen | learned_single_keep50 | 0.393 | 13 | True | 4 | 2.670 | 2.891 | decoder=linear; seq_family=gru; seq_family=tcn | True |
| shenzhen | learned_single_keep25 | 0.200 | 8 | True | 4 | 2.036 | 2.891 | decoder=linear; seq_family=gru; seq_family=tcn; seq_family=lstm; flat_family=nbeats_s | False |
| shenzhen | learned_pairs_keep50 | 0.387 | 13 | True | 4 | 2.663 | 2.891 | seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&decoder=linear; flat_family=mlp&decoder=linear; seq_family=tcn&graph_family=none; flat_family=nbeats_s | True |
| shenzhen | learned_pairs_keep25 | 0.320 | 11 | True | 4 | 2.556 | 2.891 | seq_family=skip_connection&decoder=linear; seq_family=sep_tcn&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; seq_family=tcn&decoder=linear; flat_family=mlp&decoder=linear; seq_family=tcn&graph_family=none; flat_family=nbeats_s; seq_family=lstm&flat_family=mlp; seq_family=lstm&flat_family=skip_connection | False |
| shenzhen | ref_zico_sizectrl_top_half | 0.500 | 14 | True | 4 | 2.947 | 2.891 |  | False |
| shenzhen | ref_pooled_transfer_top_half | 0.500 | 15 | True | 4 | 2.800 | 2.891 |  | True |

### metrla: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_single_keep25 | random in a reduced list | 1.780 | 25.503 | 2.000 | 0.399 | 1.215 | 0.945 | 4.201 | 4.000 |
| random_inside_learned_single_keep50 | random in a reduced list | 4.675 | 63.758 |  |  |  | 0.890 | 4.306 | 5.000 |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 2.226 | 36.242 | 5.000 | 1.344 | 4.091 | 0.860 | 5.072 | 5.000 |
| random_inside_learned_pairs_keep25 | random in a reduced list | 0.000 | 0.000 | 1.000 | 0.317 | 0.965 | 0.880 | 5.159 | 5.000 |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 6.698 | 91.946 | 8.000 | 1.644 | 5.001 | 0.890 | 6.082 | 5.000 |
| random_inside_learned_pairs_keep50 | random in a reduced list | 1.978 | 31.544 | 8.000 | 1.648 | 5.015 | 0.780 | 6.292 | 5.000 |
| random_full_list | floor | 3.313 | 55.705 | 2.000 | 0.491 | 1.495 | 0.625 | 8.566 | 8.000 |

### pems04: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_pairs_keep25 | random in a reduced list | 19.996 | 71.812 | 8.000 | 1.408 | 4.914 | 0.415 |  |  |
| random_inside_learned_single_keep25 | random in a reduced list | 13.341 | 36.913 | 10.000 | 1.742 | 6.079 | 0.340 |  |  |
| random_inside_learned_single_keep50 | random in a reduced list | 15.407 | 48.322 |  |  |  | 0.350 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 24.354 | 86.577 |  |  |  | 0.305 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 16.168 | 51.007 |  |  |  | 0.300 |  |  |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 1.312 | 0.671 |  |  |  | 0.275 |  |  |
| random_full_list | floor | 22.220 | 80.537 |  |  |  | 0.195 |  |  |

### chengdu: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_single_keep25 | random in a reduced list | 5.872 | 57.718 |  |  |  | 0.530 | 9.256 | 10.000 |
| random_inside_learned_pairs_keep25 | random in a reduced list | 5.541 | 53.020 |  |  |  | 0.565 | 9.637 | 10.000 |
| random_inside_learned_single_keep50 | random in a reduced list | 4.603 | 32.886 |  |  |  | 0.425 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 1.398 | 3.356 |  |  |  | 0.470 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 1.418 | 4.027 |  |  |  | 0.270 |  |  |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 4.853 | 38.255 |  |  |  | 0.405 |  |  |
| random_full_list | floor | 11.679 | 98.658 |  |  |  | 0.235 |  |  |

### shenzhen: cost to one sigma of random picks inside each reduced list

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| random_inside_learned_single_keep25 | random in a reduced list | 8.160 | 62.416 |  |  |  | 0.625 | 8.115 | 8.000 |
| random_inside_learned_pairs_keep25 | random in a reduced list | 4.469 | 18.121 |  |  |  | 0.505 | 11.794 | 10.000 |
| random_inside_learned_single_keep50 | random in a reduced list | 9.367 | 73.826 |  |  |  | 0.385 |  |  |
| random_inside_learned_pairs_keep50 | random in a reduced list | 1.918 | 2.013 |  |  |  | 0.395 |  |  |
| random_inside_ref_zico_sizectrl_top_half | random in a reduced list | 4.513 | 18.792 |  |  |  | 0.320 |  |  |
| random_inside_ref_pooled_transfer_top_half | random in a reduced list | 5.056 | 22.148 |  |  |  | 0.400 |  |  |
| random_full_list | floor | 10.232 | 81.879 |  |  |  | 0.145 |  |  |
