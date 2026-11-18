# evalscreen fresh_list: freshlist/pemsbay, a second list at a city of the benchmark

Fresh list: N = 150, 0 architectures in common with the source lists. Sources: ['metrla', 'pems04', 'chengdu', 'shenzhen', 'expytky', 'pemsbay']; the same city among them: ['pemsbay']. sigma_seed = 0.0011 (of the shared list of the city; the fresh list's own value from its seed runs is 0.0009). Nothing is fit on the fresh labels. F1: pass = rho inside the heads >= 0.5 for boosting on operator counts fit on the other cities and its best of five picks within one sigma_seed; fail = rho below 0.3. F2: pass = the frozen single rule keeps at most half of the list and 13 or more of the top 15; fail = it removes 4 or more of the top 15. F3: pass = head and decoder are the two axes with the highest unique share on both lists and the best level is equal on four axes or more. F4 is a measurement.

### Verdict

| question | value | verdict |
|---|---|---|
| F1 predictor on new architectures | rho inside the heads 0.16; best of 5 picks 0.57 sigma | fail |
| F2 search-space rule on new architectures | keeps 0.33 of the list and 4 of the top 15 | fail |
| F3 the same design axes | first two axes fresh ['head', 'log_params'], shared ['head', 'log_params']; best level equal on 3 of 5 axes | fail |

### F1: predictors fit on the sources, read on the fresh list

| model | fit | n_train | rho_all | rho_within_head | ci_lo | ci_hi | regret_top1_sigma | regret_best_of_5_sigma |
|---|---|---|---|---|---|---|---|---|
| gbr_operator_counts | other cities | 750 | 0.643 | 0.160 | 0.002 | 0.305 | 4.054 | 0.575 |
| ridge_operator_counts | other cities | 750 | 0.655 | 0.237 | 0.092 | 0.386 | 4.163 | 3.478 |
| gbr_proxies_head | other cities | 750 | 0.695 | 0.200 | 0.043 | 0.362 | 4.054 | 0.575 |
| gbr_operator_counts | all sources | 900 | 0.711 | 0.188 | 0.019 | 0.341 | 2.164 | 0.575 |
| ridge_operator_counts | all sources | 900 | 0.721 | 0.272 | 0.124 | 0.421 | 3.478 | 0.575 |
| gbr_proxies_head | all sources | 900 | 0.726 | 0.188 | 0.039 | 0.351 | 2.060 | 0.575 |

### F2: the search-space rules on the fresh list

| rule | kept_share | top15_kept | best_kept | random5_inside_sigma | random10_full_sigma | choices_removed |
|---|---|---|---|---|---|---|
| single rule, frozen | 0.333 | 4 | True | 2.037 | 1.461 | decoder=linear; seq_family=gru; seq_family=tcn |
| single rule, learned on the other cities, keep half | 0.327 | 4 | True | 2.026 | 1.461 | decoder=linear; seq_family=gru; flat_family=nbeats_s |
| pair rule, learned on the other cities, keep half | 0.453 | 8 | True | 1.787 | 1.461 | seq_family=sep_tcn&decoder=linear; seq_family=skip_connection&decoder=linear; flat_family=nbeats_t&decoder=linear; flat_family=skip_connection&decoder=linear; graph_family=mixed&decoder=linear; seq_family=gru&decoder=seq; flat_family=mlp&decoder=linear; seq_family=tcn&flat_family=nbeats_s; seq_family=tcn&graph_family=none |

### F4: the top of the two lists

| quantity | shared_list | fresh_list | fresh_minus_shared_sigma |
|---|---|---|---|
| best | 0.239 | 0.241 | 1.160 |
| mean of the best 5 | 0.241 | 0.241 | 0.602 |
| mean of the best 15 | 0.242 | 0.242 | 0.238 |
| median | 0.248 | 0.246 | -1.342 |
| list spread, std over sigma_seed | 5.677 | 5.447 |  |

### F3: design axes, freshlist/pemsbay, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma |
|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.745 |  |  |  | 22.112 |  |  |
| (seed) | 150 | 0.034 |  |  |  | 1.000 |  |  |
| head | 150 | 0.722 | 0.633 | 0.812 | 0.701 | 21.414 | mae | 4.099 |
| decoder | 150 | -0.006 | -0.007 | 0.026 | -0.002 | -0.181 | seq | 0.145 |
| seq_family | 150 | 0.017 | -0.022 | 0.169 | 0.001 | 0.513 | gru | 1.724 |
| graph_family | 150 | -0.007 | -0.019 | 0.112 | -0.001 | -0.212 | gcn | 1.812 |
| flat_family | 150 | 0.010 | -0.012 | 0.117 | 0.009 | 0.283 | nbeats_g | 1.723 |
| log_params | 150 | 0.026 | -0.005 | 0.106 | 0.011 | 0.777 |  |  |

### F3: design axes, pemsbay, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma |
|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.737 |  |  |  | 23.737 |  |  |
| (seed) | 150 | 0.031 |  |  |  | 1.000 |  |  |
| head | 150 | 0.709 | 0.594 | 0.804 | 0.712 | 22.858 | mae | 4.648 |
| decoder | 150 | 0.013 | -0.007 | 0.081 | 0.003 | 0.405 | linear | 0.884 |
| seq_family | 150 | -0.003 | -0.017 | 0.129 | -0.005 | -0.100 | mlp_mix | 2.078 |
| graph_family | 150 | 0.023 | -0.018 | 0.153 | 0.008 | 0.729 | gcn | 1.396 |
| flat_family | 150 | -0.013 | -0.021 | 0.094 | -0.004 | -0.414 | nbeats_g | 1.229 |
| log_params | 150 | 0.003 | -0.007 | 0.065 | 0.021 | 0.098 |  |  |

### Cost to one sigma on the fresh list

b_sigma = the smallest b whose best pick lies within one sigma_seed of the best of the list; hours_sigma_ref = the evaluator's epochs plus the remaining epochs of those b picks on the reference unit; pct_sigma = its share of training the whole list; an empty cell means no b up to 10 meets the line. sub_share = the share of 200 random subsets of 100 architectures where some b meets the line; sub_pct_median = the median cost share over the subsets, empty when fewer than half meet the line.

| evaluator | kind | regret_b1_sigma | rank_pct_b1 | b_sigma | hours_sigma_ref | pct_sigma | sub_share | sub_pct_median | sub_b_median |
|---|---|---|---|---|---|---|---|---|---|
| gbr_operator_counts, fit on other cities | predictor on the sources | 4.054 | 34.899 | 2.000 | 1.226 | 1.645 | 0.825 | 2.484 | 2.000 |
| gbr_operator_counts, fit on all sources | predictor on the sources | 2.164 | 12.752 | 2.000 | 1.255 | 1.684 | 0.785 | 2.557 | 2.000 |
| gbr_proxies_head, fit on all sources | predictor on the sources | 2.060 | 10.738 | 5.000 | 2.770 | 3.716 | 0.950 | 5.550 | 5.000 |
| gbr_proxies_head, fit on other cities | predictor on the sources | 4.054 | 34.899 | 5.000 | 3.087 | 4.141 | 0.730 | 6.082 | 5.000 |
| ridge_operator_counts, fit on all sources | predictor on the sources | 3.478 | 29.530 | 5.000 | 3.119 | 4.184 | 0.985 | 6.133 | 5.000 |
| early_val_k1 | brief training | 2.813 | 22.819 | 3.000 | 6.040 | 8.103 | 0.755 | 9.290 | 3.000 |
| params | floor | 4.691 | 46.309 | 10.000 | 5.689 | 7.631 | 0.685 | 9.607 | 8.000 |
| ridge_operator_counts, fit on other cities | predictor on the sources | 4.163 | 36.913 | 8.000 | 5.136 | 6.889 | 0.985 | 10.260 | 8.000 |
| sh_r1_eta3 | successive halving | 0.000 | 0.000 | 1.000 | 12.075 | 16.198 | 0.995 | 15.987 | 1.000 |
| zico_sizectrl_half_then_k5 | proxy filter | 0.000 | 0.000 | 1.000 | 12.001 | 16.099 | 0.990 | 16.583 | 1.000 |
| early_val_k3 | brief training | 0.000 | 0.000 | 1.000 | 13.032 | 17.482 | 0.995 | 18.040 | 1.000 |
| early_val_k2 | brief training | 2.205 | 14.094 | 10.000 | 13.788 | 18.496 | 1.000 | 19.563 | 8.000 |
| early_val_k5 | brief training | 0.000 | 0.000 | 1.000 | 21.082 | 28.280 | 0.995 | 28.764 | 1.000 |
| zico | zero-cost proxy | 4.163 | 36.913 |  |  |  | 0.115 |  |  |
| zico_t | zero-cost proxy | 4.691 | 46.309 |  |  |  | 0.160 |  |  |
| glass | zero-cost proxy | 4.163 | 36.913 |  |  |  | 0.115 |  |  |
| zico_sizectrl | zero-cost proxy | 4.163 | 36.913 |  |  |  | 0.200 |  |  |
| random | floor | 7.374 |  |  |  |  | 0.395 |  |  |

### Head control on the fresh list

| evaluator | kind | rho_all | rho_within_head | within_ci_lo | within_ci_hi | rho_mae | rho_mse | rho_quantile | mae_head_regret_sigma | mae_head_rank_pct |
|---|---|---|---|---|---|---|---|---|---|---|
| early_val_k5 | brief training | 0.879 | 0.664 | 0.560 | 0.747 | 0.568 | 0.877 | 0.576 | 0.000 | 0.000 |
| early_val_k3 | brief training | 0.835 | 0.564 | 0.449 | 0.660 | 0.496 | 0.713 | 0.504 | 0.000 | 0.000 |
| early_val_k2 | brief training | 0.775 | 0.394 | 0.235 | 0.513 | 0.399 | 0.416 | 0.371 | 2.205 | 40.000 |
| ridge_operator_counts, fit on all sources | predictor on the sources | 0.721 | 0.272 | 0.124 | 0.421 | 0.119 | 0.270 | 0.418 | 3.478 | 70.000 |
| ridge_operator_counts, fit on other cities | predictor on the sources | 0.655 | 0.237 | 0.092 | 0.386 | 0.097 | 0.235 | 0.372 | 3.478 | 70.000 |
| early_val_k1 | brief training | 0.507 | 0.221 | 0.069 | 0.358 | 0.258 | 0.418 | 0.021 | 2.813 | 58.000 |
| gbr_proxies_head, fit on other cities | predictor on the sources | 0.695 | 0.200 | 0.043 | 0.362 | 0.023 | 0.334 | 0.254 | 4.054 | 76.000 |
| gbr_proxies_head, fit on all sources | predictor on the sources | 0.726 | 0.188 | 0.039 | 0.351 | 0.026 | 0.278 | 0.266 | 2.060 | 30.000 |
| gbr_operator_counts, fit on all sources | predictor on the sources | 0.711 | 0.188 | 0.019 | 0.341 | 0.062 | 0.230 | 0.271 | 2.164 | 36.000 |
| params | floor | 0.077 | 0.161 | 0.014 | 0.332 | -0.065 | 0.208 | 0.336 | 4.127 | 78.000 |
| glass | zero-cost proxy | 0.091 | 0.161 | 0.024 | 0.304 | -0.070 | 0.288 | 0.274 | 4.127 | 78.000 |
| gbr_operator_counts, fit on other cities | predictor on the sources | 0.643 | 0.160 | 0.002 | 0.305 | 0.045 | 0.212 | 0.226 | 4.054 | 76.000 |
| zico | zero-cost proxy | 0.111 | 0.157 | 0.021 | 0.299 | -0.068 | 0.281 | 0.266 | 4.127 | 78.000 |
| zico_t | zero-cost proxy | 0.103 | 0.156 | 0.018 | 0.297 | -0.089 | 0.304 | 0.264 | 4.127 | 78.000 |
| zico_sizectrl | zero-cost proxy | -0.004 | -0.002 | -0.162 | 0.152 | -0.038 | 0.051 | -0.012 | 5.878 | 94.000 |
