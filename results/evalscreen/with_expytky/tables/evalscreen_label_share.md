# evalscreen label_share: a sparse label matrix shared by the cities

n architectures are trained at each city (design: independent, disjoint, or anchor = half common and half disjoint); a model predicts every missing entry; each city trains its b best predictions and keeps the best architecture it trained. share = the share of 50 random designs where that architecture lies within one sigma_seed of the best of the list. fleet_cost_pct = the GPU-hours of all pairs and picks over the GPU-hours of the whole matrix. own = a ridge on the labels of the city alone; pooled = one ridge on all trained pairs; pooled_own = own with the pooled prediction as an input; observed_mean = the mean rank at the cities that trained the architecture. Pass: a sharing model with a share of 0.9 or more at three of four cities at a fleet cost of 10 % or less, and a mean share above own at every setting.

### Verdict

| model | settings_at_10pct_with_3_cities | share_of_settings_above_own | cheapest_setting_with_3_cities_pct | pass |
|---|---|---|---|---|
| pooled | 0 | 0.861 | 23.341 | False |
| pooled_own | 0 | 0.861 |  | False |
| observed_mean | 0 | 0.944 |  | False |

### Reference: one city trained in full

| reference | fleet_cost_pct | other_cities_within_sigma |
|---|---|---|
| metrla in full, transfer of its best 5 | 21.921 | 4 |
| pems04 in full, transfer of its best 5 | 20.441 | 2 |
| chengdu in full, transfer of its best 5 | 14.023 | 3 |
| shenzhen in full, transfer of its best 5 | 21.181 | 4 |
| expytky in full, transfer of its best 5 | 35.355 | 3 |

### Every setting

| design | n | b | model | fleet_cost_pct | mean_share | min_share | cities_ge_09 | above_own |
|---|---|---|---|---|---|---|---|---|
| anchor | 5 | 1 | observed_mean | 3.915 | 0.128 | 0.060 | 0 | True |
| anchor | 5 | 1 | own | 3.915 | 0.120 | 0.020 | 0 | False |
| anchor | 5 | 1 | pooled | 3.915 | 0.148 | 0.060 | 0 | True |
| anchor | 5 | 1 | pooled_own | 3.915 | 0.116 | 0.040 | 0 | False |
| anchor | 5 | 1 | random | 3.915 | 0.088 | 0.040 | 0 | False |
| anchor | 5 | 3 | observed_mean | 5.249 | 0.248 | 0.100 | 0 | True |
| anchor | 5 | 3 | own | 5.249 | 0.216 | 0.100 | 0 | False |
| anchor | 5 | 3 | pooled | 5.249 | 0.264 | 0.140 | 0 | True |
| anchor | 5 | 3 | pooled_own | 5.249 | 0.236 | 0.120 | 0 | True |
| anchor | 5 | 3 | random | 5.249 | 0.108 | 0.040 | 0 | False |
| anchor | 5 | 5 | observed_mean | 6.582 | 0.344 | 0.200 | 0 | True |
| anchor | 5 | 5 | own | 6.582 | 0.288 | 0.180 | 0 | False |
| anchor | 5 | 5 | pooled | 6.582 | 0.384 | 0.240 | 0 | True |
| anchor | 5 | 5 | pooled_own | 6.582 | 0.312 | 0.180 | 0 | True |
| anchor | 5 | 5 | random | 6.582 | 0.132 | 0.060 | 0 | False |
| anchor | 10 | 1 | observed_mean | 7.224 | 0.260 | 0.160 | 0 | True |
| anchor | 10 | 1 | own | 7.224 | 0.232 | 0.120 | 0 | False |
| anchor | 10 | 1 | pooled | 7.224 | 0.228 | 0.140 | 0 | False |
| anchor | 10 | 1 | pooled_own | 7.224 | 0.232 | 0.120 | 0 | False |
| anchor | 10 | 1 | random | 7.224 | 0.172 | 0.140 | 0 | False |
| anchor | 10 | 3 | observed_mean | 8.557 | 0.376 | 0.260 | 0 | True |
| anchor | 10 | 3 | own | 8.557 | 0.372 | 0.240 | 0 | False |
| anchor | 10 | 3 | pooled | 8.557 | 0.380 | 0.240 | 0 | True |
| anchor | 10 | 3 | pooled_own | 8.557 | 0.396 | 0.220 | 0 | True |
| anchor | 10 | 3 | random | 8.557 | 0.176 | 0.140 | 0 | False |
| anchor | 10 | 5 | observed_mean | 9.890 | 0.468 | 0.280 | 0 | True |
| anchor | 10 | 5 | own | 9.890 | 0.448 | 0.300 | 0 | False |
| anchor | 10 | 5 | pooled | 9.890 | 0.492 | 0.320 | 0 | True |
| anchor | 10 | 5 | pooled_own | 9.890 | 0.476 | 0.320 | 0 | True |
| anchor | 10 | 5 | random | 9.890 | 0.208 | 0.160 | 0 | False |
| anchor | 15 | 1 | observed_mean | 10.381 | 0.284 | 0.100 | 0 | True |
| anchor | 15 | 1 | own | 10.381 | 0.280 | 0.120 | 0 | False |
| anchor | 15 | 1 | pooled | 10.381 | 0.300 | 0.100 | 0 | True |
| anchor | 15 | 1 | pooled_own | 10.381 | 0.300 | 0.120 | 0 | True |
| anchor | 15 | 1 | random | 10.381 | 0.212 | 0.120 | 0 | False |
| anchor | 15 | 3 | observed_mean | 11.715 | 0.416 | 0.220 | 0 | True |
| anchor | 15 | 3 | own | 11.715 | 0.404 | 0.200 | 0 | False |
| anchor | 15 | 3 | pooled | 11.715 | 0.456 | 0.180 | 0 | True |
| anchor | 15 | 3 | pooled_own | 11.715 | 0.420 | 0.200 | 0 | True |
| anchor | 15 | 3 | random | 11.715 | 0.232 | 0.120 | 0 | False |
| anchor | 15 | 5 | observed_mean | 13.048 | 0.504 | 0.360 | 0 | False |
| anchor | 15 | 5 | own | 13.048 | 0.504 | 0.300 | 0 | False |
| anchor | 15 | 5 | pooled | 13.048 | 0.576 | 0.260 | 1 | True |
| anchor | 15 | 5 | pooled_own | 13.048 | 0.520 | 0.280 | 0 | True |
| anchor | 15 | 5 | random | 13.048 | 0.264 | 0.160 | 0 | False |
| anchor | 30 | 1 | observed_mean | 20.532 | 0.564 | 0.400 | 0 | True |
| anchor | 30 | 1 | own | 20.532 | 0.532 | 0.440 | 0 | False |
| anchor | 30 | 1 | pooled | 20.532 | 0.512 | 0.360 | 0 | False |
| anchor | 30 | 1 | pooled_own | 20.532 | 0.544 | 0.460 | 0 | True |
| anchor | 30 | 1 | random | 20.532 | 0.384 | 0.340 | 0 | False |
| anchor | 30 | 3 | observed_mean | 21.866 | 0.700 | 0.580 | 0 | True |
| anchor | 30 | 3 | own | 21.866 | 0.680 | 0.560 | 1 | False |
| anchor | 30 | 3 | pooled | 21.866 | 0.648 | 0.420 | 0 | False |
| anchor | 30 | 3 | pooled_own | 21.866 | 0.696 | 0.540 | 1 | True |
| anchor | 30 | 3 | random | 21.866 | 0.400 | 0.360 | 0 | False |
| anchor | 30 | 5 | observed_mean | 23.199 | 0.764 | 0.660 | 0 | True |
| anchor | 30 | 5 | own | 23.199 | 0.748 | 0.600 | 1 | False |
| anchor | 30 | 5 | pooled | 23.199 | 0.736 | 0.480 | 2 | False |
| anchor | 30 | 5 | pooled_own | 23.199 | 0.768 | 0.620 | 1 | True |
| anchor | 30 | 5 | random | 23.199 | 0.416 | 0.380 | 0 | False |
| disjoint | 5 | 1 | observed_mean | 4.026 | 0.176 | 0.100 | 0 | True |
| disjoint | 5 | 1 | own | 4.026 | 0.120 | 0.080 | 0 | False |
| disjoint | 5 | 1 | pooled | 4.026 | 0.200 | 0.080 | 0 | True |
| disjoint | 5 | 1 | pooled_own | 4.026 | 0.128 | 0.080 | 0 | True |
| disjoint | 5 | 1 | random | 4.026 | 0.096 | 0.060 | 0 | False |
| disjoint | 5 | 3 | observed_mean | 5.359 | 0.284 | 0.160 | 0 | True |
| disjoint | 5 | 3 | own | 5.359 | 0.176 | 0.100 | 0 | False |
| disjoint | 5 | 3 | pooled | 5.359 | 0.300 | 0.140 | 0 | True |
| disjoint | 5 | 3 | pooled_own | 5.359 | 0.204 | 0.080 | 0 | True |
| disjoint | 5 | 3 | random | 5.359 | 0.136 | 0.080 | 0 | False |
| disjoint | 5 | 5 | observed_mean | 6.692 | 0.384 | 0.200 | 0 | True |
| disjoint | 5 | 5 | own | 6.692 | 0.276 | 0.140 | 0 | False |
| disjoint | 5 | 5 | pooled | 6.692 | 0.408 | 0.240 | 0 | True |
| disjoint | 5 | 5 | pooled_own | 6.692 | 0.324 | 0.220 | 0 | True |
| disjoint | 5 | 5 | random | 6.692 | 0.160 | 0.120 | 0 | False |
| disjoint | 10 | 1 | observed_mean | 7.387 | 0.268 | 0.120 | 0 | True |
| disjoint | 10 | 1 | own | 7.387 | 0.248 | 0.060 | 0 | False |
| disjoint | 10 | 1 | pooled | 7.387 | 0.332 | 0.060 | 0 | True |
| disjoint | 10 | 1 | pooled_own | 7.387 | 0.260 | 0.080 | 0 | True |
| disjoint | 10 | 1 | random | 7.387 | 0.192 | 0.080 | 0 | False |
| disjoint | 10 | 3 | observed_mean | 8.720 | 0.396 | 0.180 | 0 | True |
| disjoint | 10 | 3 | own | 8.720 | 0.384 | 0.220 | 0 | False |
| disjoint | 10 | 3 | pooled | 8.720 | 0.476 | 0.160 | 0 | True |
| disjoint | 10 | 3 | pooled_own | 8.720 | 0.424 | 0.220 | 0 | True |
| disjoint | 10 | 3 | random | 8.720 | 0.224 | 0.100 | 0 | False |
| disjoint | 10 | 5 | observed_mean | 10.053 | 0.500 | 0.280 | 0 | True |
| disjoint | 10 | 5 | own | 10.053 | 0.456 | 0.280 | 0 | False |
| disjoint | 10 | 5 | pooled | 10.053 | 0.576 | 0.160 | 0 | True |
| disjoint | 10 | 5 | pooled_own | 10.053 | 0.500 | 0.320 | 0 | True |
| disjoint | 10 | 5 | random | 10.053 | 0.240 | 0.100 | 0 | False |
| disjoint | 15 | 1 | observed_mean | 10.813 | 0.364 | 0.220 | 0 | True |
| disjoint | 15 | 1 | own | 10.813 | 0.324 | 0.240 | 0 | False |
| disjoint | 15 | 1 | pooled | 10.813 | 0.356 | 0.180 | 0 | True |
| disjoint | 15 | 1 | pooled_own | 10.813 | 0.324 | 0.240 | 0 | False |
| disjoint | 15 | 1 | random | 10.813 | 0.240 | 0.180 | 0 | False |
| disjoint | 15 | 3 | observed_mean | 12.147 | 0.552 | 0.380 | 0 | True |
| disjoint | 15 | 3 | own | 12.147 | 0.464 | 0.320 | 0 | False |
| disjoint | 15 | 3 | pooled | 12.147 | 0.556 | 0.220 | 0 | True |
| disjoint | 15 | 3 | pooled_own | 12.147 | 0.516 | 0.340 | 0 | True |
| disjoint | 15 | 3 | random | 12.147 | 0.284 | 0.180 | 0 | False |
| disjoint | 15 | 5 | observed_mean | 13.480 | 0.636 | 0.460 | 0 | True |
| disjoint | 15 | 5 | own | 13.480 | 0.552 | 0.400 | 0 | False |
| disjoint | 15 | 5 | pooled | 13.480 | 0.676 | 0.380 | 1 | True |
| disjoint | 15 | 5 | pooled_own | 13.480 | 0.624 | 0.460 | 0 | True |
| disjoint | 15 | 5 | random | 13.480 | 0.312 | 0.220 | 0 | False |
| disjoint | 30 | 1 | observed_mean | 20.690 | 0.500 | 0.400 | 0 | False |
| disjoint | 30 | 1 | own | 20.690 | 0.500 | 0.420 | 0 | False |
| disjoint | 30 | 1 | pooled | 20.690 | 0.500 | 0.320 | 0 | False |
| disjoint | 30 | 1 | pooled_own | 20.690 | 0.500 | 0.420 | 0 | False |
| disjoint | 30 | 1 | random | 20.690 | 0.348 | 0.300 | 0 | False |
| disjoint | 30 | 3 | observed_mean | 22.023 | 0.664 | 0.540 | 0 | True |
| disjoint | 30 | 3 | own | 22.023 | 0.620 | 0.480 | 0 | False |
| disjoint | 30 | 3 | pooled | 22.023 | 0.680 | 0.440 | 1 | True |
| disjoint | 30 | 3 | pooled_own | 22.023 | 0.668 | 0.500 | 1 | True |
| disjoint | 30 | 3 | random | 22.023 | 0.372 | 0.320 | 0 | False |
| disjoint | 30 | 5 | observed_mean | 23.357 | 0.780 | 0.660 | 1 | True |
| disjoint | 30 | 5 | own | 23.357 | 0.700 | 0.520 | 1 | False |
| disjoint | 30 | 5 | pooled | 23.357 | 0.808 | 0.580 | 3 | True |
| disjoint | 30 | 5 | pooled_own | 23.357 | 0.724 | 0.540 | 1 | True |
| disjoint | 30 | 5 | random | 23.357 | 0.404 | 0.340 | 0 | False |
| independent | 5 | 1 | observed_mean | 3.995 | 0.116 | 0.080 | 0 | True |
| independent | 5 | 1 | own | 3.995 | 0.108 | 0.020 | 0 | False |
| independent | 5 | 1 | pooled | 3.995 | 0.112 | 0.040 | 0 | True |
| independent | 5 | 1 | pooled_own | 3.995 | 0.104 | 0.020 | 0 | False |
| independent | 5 | 1 | random | 3.995 | 0.076 | 0.020 | 0 | False |
| independent | 5 | 3 | observed_mean | 5.328 | 0.216 | 0.140 | 0 | True |
| independent | 5 | 3 | own | 5.328 | 0.156 | 0.060 | 0 | False |
| independent | 5 | 3 | pooled | 5.328 | 0.204 | 0.100 | 0 | True |
| independent | 5 | 3 | pooled_own | 5.328 | 0.168 | 0.100 | 0 | True |
| independent | 5 | 3 | random | 5.328 | 0.100 | 0.020 | 0 | False |
| independent | 5 | 5 | observed_mean | 6.662 | 0.312 | 0.220 | 0 | True |
| independent | 5 | 5 | own | 6.662 | 0.228 | 0.120 | 0 | False |
| independent | 5 | 5 | pooled | 6.662 | 0.324 | 0.140 | 0 | True |
| independent | 5 | 5 | pooled_own | 6.662 | 0.252 | 0.160 | 0 | True |
| independent | 5 | 5 | random | 6.662 | 0.124 | 0.040 | 0 | False |
| independent | 10 | 1 | observed_mean | 7.330 | 0.316 | 0.160 | 0 | True |
| independent | 10 | 1 | own | 7.330 | 0.224 | 0.100 | 0 | False |
| independent | 10 | 1 | pooled | 7.330 | 0.268 | 0.140 | 0 | True |
| independent | 10 | 1 | pooled_own | 7.330 | 0.236 | 0.100 | 0 | True |
| independent | 10 | 1 | random | 7.330 | 0.184 | 0.100 | 0 | False |
| independent | 10 | 3 | observed_mean | 8.663 | 0.464 | 0.240 | 0 | True |
| independent | 10 | 3 | own | 8.663 | 0.348 | 0.160 | 0 | False |
| independent | 10 | 3 | pooled | 8.663 | 0.472 | 0.180 | 0 | True |
| independent | 10 | 3 | pooled_own | 8.663 | 0.380 | 0.220 | 0 | True |
| independent | 10 | 3 | random | 8.663 | 0.200 | 0.120 | 0 | False |
| independent | 10 | 5 | observed_mean | 9.997 | 0.572 | 0.280 | 0 | True |
| independent | 10 | 5 | own | 9.997 | 0.420 | 0.260 | 0 | False |
| independent | 10 | 5 | pooled | 9.997 | 0.580 | 0.280 | 0 | True |
| independent | 10 | 5 | pooled_own | 9.997 | 0.472 | 0.280 | 0 | True |
| independent | 10 | 5 | random | 9.997 | 0.224 | 0.140 | 0 | False |
| independent | 15 | 1 | observed_mean | 10.637 | 0.336 | 0.260 | 0 | True |
| independent | 15 | 1 | own | 10.637 | 0.276 | 0.180 | 0 | False |
| independent | 15 | 1 | pooled | 10.637 | 0.296 | 0.160 | 0 | True |
| independent | 15 | 1 | pooled_own | 10.637 | 0.300 | 0.200 | 0 | True |
| independent | 15 | 1 | random | 10.637 | 0.220 | 0.160 | 0 | False |
| independent | 15 | 3 | observed_mean | 11.970 | 0.472 | 0.380 | 0 | True |
| independent | 15 | 3 | own | 11.970 | 0.416 | 0.280 | 0 | False |
| independent | 15 | 3 | pooled | 11.970 | 0.504 | 0.280 | 0 | True |
| independent | 15 | 3 | pooled_own | 11.970 | 0.444 | 0.300 | 0 | True |
| independent | 15 | 3 | random | 11.970 | 0.232 | 0.160 | 0 | False |
| independent | 15 | 5 | observed_mean | 13.303 | 0.580 | 0.400 | 0 | True |
| independent | 15 | 5 | own | 13.303 | 0.488 | 0.340 | 0 | False |
| independent | 15 | 5 | pooled | 13.303 | 0.612 | 0.340 | 0 | True |
| independent | 15 | 5 | pooled_own | 13.303 | 0.540 | 0.380 | 0 | True |
| independent | 15 | 5 | random | 13.303 | 0.252 | 0.160 | 0 | False |
| independent | 30 | 1 | observed_mean | 20.674 | 0.560 | 0.400 | 0 | True |
| independent | 30 | 1 | own | 20.674 | 0.508 | 0.380 | 0 | False |
| independent | 30 | 1 | pooled | 20.674 | 0.540 | 0.340 | 0 | True |
| independent | 30 | 1 | pooled_own | 20.674 | 0.516 | 0.380 | 0 | True |
| independent | 30 | 1 | random | 20.674 | 0.404 | 0.320 | 0 | False |
| independent | 30 | 3 | observed_mean | 22.008 | 0.708 | 0.460 | 0 | True |
| independent | 30 | 3 | own | 22.008 | 0.636 | 0.460 | 1 | False |
| independent | 30 | 3 | pooled | 22.008 | 0.688 | 0.400 | 1 | True |
| independent | 30 | 3 | pooled_own | 22.008 | 0.652 | 0.460 | 1 | True |
| independent | 30 | 3 | random | 22.008 | 0.428 | 0.360 | 0 | False |
| independent | 30 | 5 | observed_mean | 23.341 | 0.804 | 0.580 | 2 | True |
| independent | 30 | 5 | own | 23.341 | 0.708 | 0.540 | 1 | False |
| independent | 30 | 5 | pooled | 23.341 | 0.812 | 0.500 | 3 | True |
| independent | 30 | 5 | pooled_own | 23.341 | 0.768 | 0.560 | 1 | True |
| independent | 30 | 5 | random | 23.341 | 0.452 | 0.380 | 0 | False |

### Every city

| design | n | b | model | city | share | fleet_cost_pct |
|---|---|---|---|---|---|---|
| independent | 5 | 1 | own | metrla | 0.100 | 3.995 |
| independent | 5 | 1 | own | pems04 | 0.180 | 3.995 |
| independent | 5 | 1 | own | chengdu | 0.080 | 3.995 |
| independent | 5 | 1 | own | shenzhen | 0.020 | 3.995 |
| independent | 5 | 1 | own | expytky | 0.160 | 3.995 |
| independent | 5 | 3 | own | metrla | 0.120 | 5.328 |
| independent | 5 | 3 | own | pems04 | 0.260 | 5.328 |
| independent | 5 | 3 | own | chengdu | 0.120 | 5.328 |
| independent | 5 | 3 | own | shenzhen | 0.060 | 5.328 |
| independent | 5 | 3 | own | expytky | 0.220 | 5.328 |
| independent | 5 | 5 | own | metrla | 0.240 | 6.662 |
| independent | 5 | 5 | own | pems04 | 0.400 | 6.662 |
| independent | 5 | 5 | own | chengdu | 0.120 | 6.662 |
| independent | 5 | 5 | own | shenzhen | 0.140 | 6.662 |
| independent | 5 | 5 | own | expytky | 0.240 | 6.662 |
| independent | 5 | 1 | pooled | metrla | 0.140 | 3.995 |
| independent | 5 | 1 | pooled | pems04 | 0.160 | 3.995 |
| independent | 5 | 1 | pooled | chengdu | 0.060 | 3.995 |
| independent | 5 | 1 | pooled | shenzhen | 0.040 | 3.995 |
| independent | 5 | 1 | pooled | expytky | 0.160 | 3.995 |
| independent | 5 | 3 | pooled | metrla | 0.200 | 5.328 |
| independent | 5 | 3 | pooled | pems04 | 0.320 | 5.328 |
| independent | 5 | 3 | pooled | chengdu | 0.100 | 5.328 |
| independent | 5 | 3 | pooled | shenzhen | 0.140 | 5.328 |
| independent | 5 | 3 | pooled | expytky | 0.260 | 5.328 |
| independent | 5 | 5 | pooled | metrla | 0.400 | 6.662 |
| independent | 5 | 5 | pooled | pems04 | 0.500 | 6.662 |
| independent | 5 | 5 | pooled | chengdu | 0.140 | 6.662 |
| independent | 5 | 5 | pooled | shenzhen | 0.200 | 6.662 |
| independent | 5 | 5 | pooled | expytky | 0.380 | 6.662 |
| independent | 5 | 1 | pooled_own | metrla | 0.080 | 3.995 |
| independent | 5 | 1 | pooled_own | pems04 | 0.160 | 3.995 |
| independent | 5 | 1 | pooled_own | chengdu | 0.100 | 3.995 |
| independent | 5 | 1 | pooled_own | shenzhen | 0.020 | 3.995 |
| independent | 5 | 1 | pooled_own | expytky | 0.160 | 3.995 |
| independent | 5 | 3 | pooled_own | metrla | 0.140 | 5.328 |
| independent | 5 | 3 | pooled_own | pems04 | 0.300 | 5.328 |
| independent | 5 | 3 | pooled_own | chengdu | 0.120 | 5.328 |
| independent | 5 | 3 | pooled_own | shenzhen | 0.100 | 5.328 |
| independent | 5 | 3 | pooled_own | expytky | 0.180 | 5.328 |
| independent | 5 | 5 | pooled_own | metrla | 0.240 | 6.662 |
| independent | 5 | 5 | pooled_own | pems04 | 0.460 | 6.662 |
| independent | 5 | 5 | pooled_own | chengdu | 0.160 | 6.662 |
| independent | 5 | 5 | pooled_own | shenzhen | 0.160 | 6.662 |
| independent | 5 | 5 | pooled_own | expytky | 0.240 | 6.662 |
| independent | 5 | 1 | observed_mean | metrla | 0.120 | 3.995 |
| independent | 5 | 1 | observed_mean | pems04 | 0.120 | 3.995 |
| independent | 5 | 1 | observed_mean | chengdu | 0.080 | 3.995 |
| independent | 5 | 1 | observed_mean | shenzhen | 0.080 | 3.995 |
| independent | 5 | 1 | observed_mean | expytky | 0.180 | 3.995 |
| independent | 5 | 3 | observed_mean | metrla | 0.200 | 5.328 |
| independent | 5 | 3 | observed_mean | pems04 | 0.280 | 5.328 |
| independent | 5 | 3 | observed_mean | chengdu | 0.140 | 5.328 |
| independent | 5 | 3 | observed_mean | shenzhen | 0.200 | 5.328 |
| independent | 5 | 3 | observed_mean | expytky | 0.260 | 5.328 |
| independent | 5 | 5 | observed_mean | metrla | 0.280 | 6.662 |
| independent | 5 | 5 | observed_mean | pems04 | 0.380 | 6.662 |
| independent | 5 | 5 | observed_mean | chengdu | 0.220 | 6.662 |
| independent | 5 | 5 | observed_mean | shenzhen | 0.280 | 6.662 |
| independent | 5 | 5 | observed_mean | expytky | 0.400 | 6.662 |
| independent | 5 | 1 | random | metrla | 0.100 | 3.995 |
| independent | 5 | 1 | random | pems04 | 0.080 | 3.995 |
| independent | 5 | 1 | random | chengdu | 0.080 | 3.995 |
| independent | 5 | 1 | random | shenzhen | 0.020 | 3.995 |
| independent | 5 | 1 | random | expytky | 0.100 | 3.995 |
| independent | 5 | 3 | random | metrla | 0.120 | 5.328 |
| independent | 5 | 3 | random | pems04 | 0.140 | 5.328 |
| independent | 5 | 3 | random | chengdu | 0.120 | 5.328 |
| independent | 5 | 3 | random | shenzhen | 0.020 | 5.328 |
| independent | 5 | 3 | random | expytky | 0.100 | 5.328 |
| independent | 5 | 5 | random | metrla | 0.160 | 6.662 |
| independent | 5 | 5 | random | pems04 | 0.160 | 6.662 |
| independent | 5 | 5 | random | chengdu | 0.120 | 6.662 |
| independent | 5 | 5 | random | shenzhen | 0.040 | 6.662 |
| independent | 5 | 5 | random | expytky | 0.140 | 6.662 |
| independent | 10 | 1 | own | metrla | 0.200 | 7.330 |
| independent | 10 | 1 | own | pems04 | 0.380 | 7.330 |
| independent | 10 | 1 | own | chengdu | 0.120 | 7.330 |
| independent | 10 | 1 | own | shenzhen | 0.100 | 7.330 |
| independent | 10 | 1 | own | expytky | 0.320 | 7.330 |
| independent | 10 | 3 | own | metrla | 0.300 | 8.663 |
| independent | 10 | 3 | own | pems04 | 0.660 | 8.663 |
| independent | 10 | 3 | own | chengdu | 0.220 | 8.663 |
| independent | 10 | 3 | own | shenzhen | 0.160 | 8.663 |
| independent | 10 | 3 | own | expytky | 0.400 | 8.663 |
| independent | 10 | 5 | own | metrla | 0.380 | 9.997 |
| independent | 10 | 5 | own | pems04 | 0.760 | 9.997 |
| independent | 10 | 5 | own | chengdu | 0.260 | 9.997 |
| independent | 10 | 5 | own | shenzhen | 0.300 | 9.997 |
| independent | 10 | 5 | own | expytky | 0.400 | 9.997 |
| independent | 10 | 1 | pooled | metrla | 0.340 | 7.330 |
| independent | 10 | 1 | pooled | pems04 | 0.340 | 7.330 |
| independent | 10 | 1 | pooled | chengdu | 0.140 | 7.330 |
| independent | 10 | 1 | pooled | shenzhen | 0.180 | 7.330 |
| independent | 10 | 1 | pooled | expytky | 0.340 | 7.330 |
| independent | 10 | 3 | pooled | metrla | 0.660 | 8.663 |
| independent | 10 | 3 | pooled | pems04 | 0.660 | 8.663 |
| independent | 10 | 3 | pooled | chengdu | 0.180 | 8.663 |
| independent | 10 | 3 | pooled | shenzhen | 0.280 | 8.663 |
| independent | 10 | 3 | pooled | expytky | 0.580 | 8.663 |
| independent | 10 | 5 | pooled | metrla | 0.840 | 9.997 |
| independent | 10 | 5 | pooled | pems04 | 0.740 | 9.997 |
| independent | 10 | 5 | pooled | chengdu | 0.280 | 9.997 |
| independent | 10 | 5 | pooled | shenzhen | 0.400 | 9.997 |
| independent | 10 | 5 | pooled | expytky | 0.640 | 9.997 |
| independent | 10 | 1 | pooled_own | metrla | 0.220 | 7.330 |
| independent | 10 | 1 | pooled_own | pems04 | 0.420 | 7.330 |
| independent | 10 | 1 | pooled_own | chengdu | 0.100 | 7.330 |
| independent | 10 | 1 | pooled_own | shenzhen | 0.100 | 7.330 |
| independent | 10 | 1 | pooled_own | expytky | 0.340 | 7.330 |
| independent | 10 | 3 | pooled_own | metrla | 0.320 | 8.663 |
| independent | 10 | 3 | pooled_own | pems04 | 0.720 | 8.663 |
| independent | 10 | 3 | pooled_own | chengdu | 0.240 | 8.663 |
| independent | 10 | 3 | pooled_own | shenzhen | 0.220 | 8.663 |
| independent | 10 | 3 | pooled_own | expytky | 0.400 | 8.663 |
| independent | 10 | 5 | pooled_own | metrla | 0.480 | 9.997 |
| independent | 10 | 5 | pooled_own | pems04 | 0.820 | 9.997 |
| independent | 10 | 5 | pooled_own | chengdu | 0.340 | 9.997 |
| independent | 10 | 5 | pooled_own | shenzhen | 0.280 | 9.997 |
| independent | 10 | 5 | pooled_own | expytky | 0.440 | 9.997 |
| independent | 10 | 1 | observed_mean | metrla | 0.400 | 7.330 |
| independent | 10 | 1 | observed_mean | pems04 | 0.360 | 7.330 |
| independent | 10 | 1 | observed_mean | chengdu | 0.160 | 7.330 |
| independent | 10 | 1 | observed_mean | shenzhen | 0.260 | 7.330 |
| independent | 10 | 1 | observed_mean | expytky | 0.400 | 7.330 |
| independent | 10 | 3 | observed_mean | metrla | 0.600 | 8.663 |
| independent | 10 | 3 | observed_mean | pems04 | 0.480 | 8.663 |
| independent | 10 | 3 | observed_mean | chengdu | 0.240 | 8.663 |
| independent | 10 | 3 | observed_mean | shenzhen | 0.440 | 8.663 |
| independent | 10 | 3 | observed_mean | expytky | 0.560 | 8.663 |
| independent | 10 | 5 | observed_mean | metrla | 0.720 | 9.997 |
| independent | 10 | 5 | observed_mean | pems04 | 0.660 | 9.997 |
| independent | 10 | 5 | observed_mean | chengdu | 0.280 | 9.997 |
| independent | 10 | 5 | observed_mean | shenzhen | 0.540 | 9.997 |
| independent | 10 | 5 | observed_mean | expytky | 0.660 | 9.997 |
| independent | 10 | 1 | random | metrla | 0.200 | 7.330 |
| independent | 10 | 1 | random | pems04 | 0.260 | 7.330 |
| independent | 10 | 1 | random | chengdu | 0.120 | 7.330 |
| independent | 10 | 1 | random | shenzhen | 0.100 | 7.330 |
| independent | 10 | 1 | random | expytky | 0.240 | 7.330 |
| independent | 10 | 3 | random | metrla | 0.220 | 8.663 |
| independent | 10 | 3 | random | pems04 | 0.280 | 8.663 |
| independent | 10 | 3 | random | chengdu | 0.120 | 8.663 |
| independent | 10 | 3 | random | shenzhen | 0.120 | 8.663 |
| independent | 10 | 3 | random | expytky | 0.260 | 8.663 |
| independent | 10 | 5 | random | metrla | 0.240 | 9.997 |
| independent | 10 | 5 | random | pems04 | 0.280 | 9.997 |
| independent | 10 | 5 | random | chengdu | 0.140 | 9.997 |
| independent | 10 | 5 | random | shenzhen | 0.140 | 9.997 |
| independent | 10 | 5 | random | expytky | 0.320 | 9.997 |
| independent | 15 | 1 | own | metrla | 0.320 | 10.637 |
| independent | 15 | 1 | own | pems04 | 0.440 | 10.637 |
| independent | 15 | 1 | own | chengdu | 0.180 | 10.637 |
| independent | 15 | 1 | own | shenzhen | 0.240 | 10.637 |
| independent | 15 | 1 | own | expytky | 0.200 | 10.637 |
| independent | 15 | 3 | own | metrla | 0.460 | 11.970 |
| independent | 15 | 3 | own | pems04 | 0.760 | 11.970 |
| independent | 15 | 3 | own | chengdu | 0.280 | 11.970 |
| independent | 15 | 3 | own | shenzhen | 0.300 | 11.970 |
| independent | 15 | 3 | own | expytky | 0.280 | 11.970 |
| independent | 15 | 5 | own | metrla | 0.480 | 13.303 |
| independent | 15 | 5 | own | pems04 | 0.780 | 13.303 |
| independent | 15 | 5 | own | chengdu | 0.340 | 13.303 |
| independent | 15 | 5 | own | shenzhen | 0.420 | 13.303 |
| independent | 15 | 5 | own | expytky | 0.420 | 13.303 |
| independent | 15 | 1 | pooled | metrla | 0.340 | 10.637 |
| independent | 15 | 1 | pooled | pems04 | 0.440 | 10.637 |
| independent | 15 | 1 | pooled | chengdu | 0.160 | 10.637 |
| independent | 15 | 1 | pooled | shenzhen | 0.320 | 10.637 |
| independent | 15 | 1 | pooled | expytky | 0.220 | 10.637 |
| independent | 15 | 3 | pooled | metrla | 0.580 | 11.970 |
| independent | 15 | 3 | pooled | pems04 | 0.780 | 11.970 |
| independent | 15 | 3 | pooled | chengdu | 0.280 | 11.970 |
| independent | 15 | 3 | pooled | shenzhen | 0.500 | 11.970 |
| independent | 15 | 3 | pooled | expytky | 0.380 | 11.970 |
| independent | 15 | 5 | pooled | metrla | 0.700 | 13.303 |
| independent | 15 | 5 | pooled | pems04 | 0.880 | 13.303 |
| independent | 15 | 5 | pooled | chengdu | 0.340 | 13.303 |
| independent | 15 | 5 | pooled | shenzhen | 0.620 | 13.303 |
| independent | 15 | 5 | pooled | expytky | 0.520 | 13.303 |
| independent | 15 | 1 | pooled_own | metrla | 0.320 | 10.637 |
| independent | 15 | 1 | pooled_own | pems04 | 0.520 | 10.637 |
| independent | 15 | 1 | pooled_own | chengdu | 0.200 | 10.637 |
| independent | 15 | 1 | pooled_own | shenzhen | 0.260 | 10.637 |
| independent | 15 | 1 | pooled_own | expytky | 0.200 | 10.637 |
| independent | 15 | 3 | pooled_own | metrla | 0.460 | 11.970 |
| independent | 15 | 3 | pooled_own | pems04 | 0.800 | 11.970 |
| independent | 15 | 3 | pooled_own | chengdu | 0.300 | 11.970 |
| independent | 15 | 3 | pooled_own | shenzhen | 0.360 | 11.970 |
| independent | 15 | 3 | pooled_own | expytky | 0.300 | 11.970 |
| independent | 15 | 5 | pooled_own | metrla | 0.560 | 13.303 |
| independent | 15 | 5 | pooled_own | pems04 | 0.880 | 13.303 |
| independent | 15 | 5 | pooled_own | chengdu | 0.380 | 13.303 |
| independent | 15 | 5 | pooled_own | shenzhen | 0.460 | 13.303 |
| independent | 15 | 5 | pooled_own | expytky | 0.420 | 13.303 |
| independent | 15 | 1 | observed_mean | metrla | 0.380 | 10.637 |
| independent | 15 | 1 | observed_mean | pems04 | 0.400 | 10.637 |
| independent | 15 | 1 | observed_mean | chengdu | 0.260 | 10.637 |
| independent | 15 | 1 | observed_mean | shenzhen | 0.380 | 10.637 |
| independent | 15 | 1 | observed_mean | expytky | 0.260 | 10.637 |
| independent | 15 | 3 | observed_mean | metrla | 0.520 | 11.970 |
| independent | 15 | 3 | observed_mean | pems04 | 0.520 | 11.970 |
| independent | 15 | 3 | observed_mean | chengdu | 0.380 | 11.970 |
| independent | 15 | 3 | observed_mean | shenzhen | 0.560 | 11.970 |
| independent | 15 | 3 | observed_mean | expytky | 0.380 | 11.970 |
| independent | 15 | 5 | observed_mean | metrla | 0.580 | 13.303 |
| independent | 15 | 5 | observed_mean | pems04 | 0.780 | 13.303 |
| independent | 15 | 5 | observed_mean | chengdu | 0.400 | 13.303 |
| independent | 15 | 5 | observed_mean | shenzhen | 0.640 | 13.303 |
| independent | 15 | 5 | observed_mean | expytky | 0.500 | 13.303 |
| independent | 15 | 1 | random | metrla | 0.260 | 10.637 |
| independent | 15 | 1 | random | pems04 | 0.280 | 10.637 |
| independent | 15 | 1 | random | chengdu | 0.160 | 10.637 |
| independent | 15 | 1 | random | shenzhen | 0.240 | 10.637 |
| independent | 15 | 1 | random | expytky | 0.160 | 10.637 |
| independent | 15 | 3 | random | metrla | 0.260 | 11.970 |
| independent | 15 | 3 | random | pems04 | 0.320 | 11.970 |
| independent | 15 | 3 | random | chengdu | 0.160 | 11.970 |
| independent | 15 | 3 | random | shenzhen | 0.260 | 11.970 |
| independent | 15 | 3 | random | expytky | 0.160 | 11.970 |
| independent | 15 | 5 | random | metrla | 0.280 | 13.303 |
| independent | 15 | 5 | random | pems04 | 0.320 | 13.303 |
| independent | 15 | 5 | random | chengdu | 0.160 | 13.303 |
| independent | 15 | 5 | random | shenzhen | 0.300 | 13.303 |
| independent | 15 | 5 | random | expytky | 0.200 | 13.303 |
| independent | 30 | 1 | own | metrla | 0.580 | 20.674 |
| independent | 30 | 1 | own | pems04 | 0.760 | 20.674 |
| independent | 30 | 1 | own | chengdu | 0.380 | 20.674 |
| independent | 30 | 1 | own | shenzhen | 0.400 | 20.674 |
| independent | 30 | 1 | own | expytky | 0.420 | 20.674 |
| independent | 30 | 3 | own | metrla | 0.760 | 22.008 |
| independent | 30 | 3 | own | pems04 | 0.920 | 22.008 |
| independent | 30 | 3 | own | chengdu | 0.460 | 22.008 |
| independent | 30 | 3 | own | shenzhen | 0.560 | 22.008 |
| independent | 30 | 3 | own | expytky | 0.480 | 22.008 |
| independent | 30 | 5 | own | metrla | 0.780 | 23.341 |
| independent | 30 | 5 | own | pems04 | 1.000 | 23.341 |
| independent | 30 | 5 | own | chengdu | 0.560 | 23.341 |
| independent | 30 | 5 | own | shenzhen | 0.660 | 23.341 |
| independent | 30 | 5 | own | expytky | 0.540 | 23.341 |
| independent | 30 | 1 | pooled | metrla | 0.600 | 20.674 |
| independent | 30 | 1 | pooled | pems04 | 0.820 | 20.674 |
| independent | 30 | 1 | pooled | chengdu | 0.340 | 20.674 |
| independent | 30 | 1 | pooled | shenzhen | 0.540 | 20.674 |
| independent | 30 | 1 | pooled | expytky | 0.400 | 20.674 |
| independent | 30 | 3 | pooled | metrla | 0.840 | 22.008 |
| independent | 30 | 3 | pooled | pems04 | 0.940 | 22.008 |
| independent | 30 | 3 | pooled | chengdu | 0.400 | 22.008 |
| independent | 30 | 3 | pooled | shenzhen | 0.740 | 22.008 |
| independent | 30 | 3 | pooled | expytky | 0.520 | 22.008 |
| independent | 30 | 5 | pooled | metrla | 0.960 | 23.341 |
| independent | 30 | 5 | pooled | pems04 | 1.000 | 23.341 |
| independent | 30 | 5 | pooled | chengdu | 0.500 | 23.341 |
| independent | 30 | 5 | pooled | shenzhen | 0.920 | 23.341 |
| independent | 30 | 5 | pooled | expytky | 0.680 | 23.341 |
| independent | 30 | 1 | pooled_own | metrla | 0.580 | 20.674 |
| independent | 30 | 1 | pooled_own | pems04 | 0.780 | 20.674 |
| independent | 30 | 1 | pooled_own | chengdu | 0.380 | 20.674 |
| independent | 30 | 1 | pooled_own | shenzhen | 0.420 | 20.674 |
| independent | 30 | 1 | pooled_own | expytky | 0.420 | 20.674 |
| independent | 30 | 3 | pooled_own | metrla | 0.760 | 22.008 |
| independent | 30 | 3 | pooled_own | pems04 | 0.940 | 22.008 |
| independent | 30 | 3 | pooled_own | chengdu | 0.460 | 22.008 |
| independent | 30 | 3 | pooled_own | shenzhen | 0.620 | 22.008 |
| independent | 30 | 3 | pooled_own | expytky | 0.480 | 22.008 |
| independent | 30 | 5 | pooled_own | metrla | 0.860 | 23.341 |
| independent | 30 | 5 | pooled_own | pems04 | 1.000 | 23.341 |
| independent | 30 | 5 | pooled_own | chengdu | 0.680 | 23.341 |
| independent | 30 | 5 | pooled_own | shenzhen | 0.740 | 23.341 |
| independent | 30 | 5 | pooled_own | expytky | 0.560 | 23.341 |
| independent | 30 | 1 | observed_mean | metrla | 0.680 | 20.674 |
| independent | 30 | 1 | observed_mean | pems04 | 0.680 | 20.674 |
| independent | 30 | 1 | observed_mean | chengdu | 0.400 | 20.674 |
| independent | 30 | 1 | observed_mean | shenzhen | 0.560 | 20.674 |
| independent | 30 | 1 | observed_mean | expytky | 0.480 | 20.674 |
| independent | 30 | 3 | observed_mean | metrla | 0.800 | 22.008 |
| independent | 30 | 3 | observed_mean | pems04 | 0.820 | 22.008 |
| independent | 30 | 3 | observed_mean | chengdu | 0.460 | 22.008 |
| independent | 30 | 3 | observed_mean | shenzhen | 0.740 | 22.008 |
| independent | 30 | 3 | observed_mean | expytky | 0.720 | 22.008 |
| independent | 30 | 5 | observed_mean | metrla | 0.900 | 23.341 |
| independent | 30 | 5 | observed_mean | pems04 | 0.900 | 23.341 |
| independent | 30 | 5 | observed_mean | chengdu | 0.580 | 23.341 |
| independent | 30 | 5 | observed_mean | shenzhen | 0.840 | 23.341 |
| independent | 30 | 5 | observed_mean | expytky | 0.800 | 23.341 |
| independent | 30 | 1 | random | metrla | 0.420 | 20.674 |
| independent | 30 | 1 | random | pems04 | 0.500 | 20.674 |
| independent | 30 | 1 | random | chengdu | 0.360 | 20.674 |
| independent | 30 | 1 | random | shenzhen | 0.320 | 20.674 |
| independent | 30 | 1 | random | expytky | 0.420 | 20.674 |
| independent | 30 | 3 | random | metrla | 0.440 | 22.008 |
| independent | 30 | 3 | random | pems04 | 0.500 | 22.008 |
| independent | 30 | 3 | random | chengdu | 0.360 | 22.008 |
| independent | 30 | 3 | random | shenzhen | 0.380 | 22.008 |
| independent | 30 | 3 | random | expytky | 0.460 | 22.008 |
| independent | 30 | 5 | random | metrla | 0.460 | 23.341 |
| independent | 30 | 5 | random | pems04 | 0.520 | 23.341 |
| independent | 30 | 5 | random | chengdu | 0.380 | 23.341 |
| independent | 30 | 5 | random | shenzhen | 0.420 | 23.341 |
| independent | 30 | 5 | random | expytky | 0.480 | 23.341 |
| disjoint | 5 | 1 | own | metrla | 0.160 | 4.026 |
| disjoint | 5 | 1 | own | pems04 | 0.120 | 4.026 |
| disjoint | 5 | 1 | own | chengdu | 0.100 | 4.026 |
| disjoint | 5 | 1 | own | shenzhen | 0.080 | 4.026 |
| disjoint | 5 | 1 | own | expytky | 0.140 | 4.026 |
| disjoint | 5 | 3 | own | metrla | 0.200 | 5.359 |
| disjoint | 5 | 3 | own | pems04 | 0.180 | 5.359 |
| disjoint | 5 | 3 | own | chengdu | 0.200 | 5.359 |
| disjoint | 5 | 3 | own | shenzhen | 0.100 | 5.359 |
| disjoint | 5 | 3 | own | expytky | 0.200 | 5.359 |
| disjoint | 5 | 5 | own | metrla | 0.280 | 6.692 |
| disjoint | 5 | 5 | own | pems04 | 0.360 | 6.692 |
| disjoint | 5 | 5 | own | chengdu | 0.280 | 6.692 |
| disjoint | 5 | 5 | own | shenzhen | 0.140 | 6.692 |
| disjoint | 5 | 5 | own | expytky | 0.320 | 6.692 |
| disjoint | 5 | 1 | pooled | metrla | 0.260 | 4.026 |
| disjoint | 5 | 1 | pooled | pems04 | 0.300 | 4.026 |
| disjoint | 5 | 1 | pooled | chengdu | 0.080 | 4.026 |
| disjoint | 5 | 1 | pooled | shenzhen | 0.140 | 4.026 |
| disjoint | 5 | 1 | pooled | expytky | 0.220 | 4.026 |
| disjoint | 5 | 3 | pooled | metrla | 0.400 | 5.359 |
| disjoint | 5 | 3 | pooled | pems04 | 0.460 | 5.359 |
| disjoint | 5 | 3 | pooled | chengdu | 0.140 | 5.359 |
| disjoint | 5 | 3 | pooled | shenzhen | 0.220 | 5.359 |
| disjoint | 5 | 3 | pooled | expytky | 0.280 | 5.359 |
| disjoint | 5 | 5 | pooled | metrla | 0.500 | 6.692 |
| disjoint | 5 | 5 | pooled | pems04 | 0.560 | 6.692 |
| disjoint | 5 | 5 | pooled | chengdu | 0.240 | 6.692 |
| disjoint | 5 | 5 | pooled | shenzhen | 0.340 | 6.692 |
| disjoint | 5 | 5 | pooled | expytky | 0.400 | 6.692 |
| disjoint | 5 | 1 | pooled_own | metrla | 0.160 | 4.026 |
| disjoint | 5 | 1 | pooled_own | pems04 | 0.180 | 4.026 |
| disjoint | 5 | 1 | pooled_own | chengdu | 0.080 | 4.026 |
| disjoint | 5 | 1 | pooled_own | shenzhen | 0.080 | 4.026 |
| disjoint | 5 | 1 | pooled_own | expytky | 0.140 | 4.026 |
| disjoint | 5 | 3 | pooled_own | metrla | 0.220 | 5.359 |
| disjoint | 5 | 3 | pooled_own | pems04 | 0.320 | 5.359 |
| disjoint | 5 | 3 | pooled_own | chengdu | 0.200 | 5.359 |
| disjoint | 5 | 3 | pooled_own | shenzhen | 0.080 | 5.359 |
| disjoint | 5 | 3 | pooled_own | expytky | 0.200 | 5.359 |
| disjoint | 5 | 5 | pooled_own | metrla | 0.340 | 6.692 |
| disjoint | 5 | 5 | pooled_own | pems04 | 0.420 | 6.692 |
| disjoint | 5 | 5 | pooled_own | chengdu | 0.300 | 6.692 |
| disjoint | 5 | 5 | pooled_own | shenzhen | 0.220 | 6.692 |
| disjoint | 5 | 5 | pooled_own | expytky | 0.340 | 6.692 |
| disjoint | 5 | 1 | observed_mean | metrla | 0.260 | 4.026 |
| disjoint | 5 | 1 | observed_mean | pems04 | 0.200 | 4.026 |
| disjoint | 5 | 1 | observed_mean | chengdu | 0.100 | 4.026 |
| disjoint | 5 | 1 | observed_mean | shenzhen | 0.180 | 4.026 |
| disjoint | 5 | 1 | observed_mean | expytky | 0.140 | 4.026 |
| disjoint | 5 | 3 | observed_mean | metrla | 0.320 | 5.359 |
| disjoint | 5 | 3 | observed_mean | pems04 | 0.440 | 5.359 |
| disjoint | 5 | 3 | observed_mean | chengdu | 0.160 | 5.359 |
| disjoint | 5 | 3 | observed_mean | shenzhen | 0.260 | 5.359 |
| disjoint | 5 | 3 | observed_mean | expytky | 0.240 | 5.359 |
| disjoint | 5 | 5 | observed_mean | metrla | 0.420 | 6.692 |
| disjoint | 5 | 5 | observed_mean | pems04 | 0.580 | 6.692 |
| disjoint | 5 | 5 | observed_mean | chengdu | 0.200 | 6.692 |
| disjoint | 5 | 5 | observed_mean | shenzhen | 0.360 | 6.692 |
| disjoint | 5 | 5 | observed_mean | expytky | 0.360 | 6.692 |
| disjoint | 5 | 1 | random | metrla | 0.160 | 4.026 |
| disjoint | 5 | 1 | random | pems04 | 0.080 | 4.026 |
| disjoint | 5 | 1 | random | chengdu | 0.060 | 4.026 |
| disjoint | 5 | 1 | random | shenzhen | 0.080 | 4.026 |
| disjoint | 5 | 1 | random | expytky | 0.100 | 4.026 |
| disjoint | 5 | 3 | random | metrla | 0.160 | 5.359 |
| disjoint | 5 | 3 | random | pems04 | 0.160 | 5.359 |
| disjoint | 5 | 3 | random | chengdu | 0.080 | 5.359 |
| disjoint | 5 | 3 | random | shenzhen | 0.120 | 5.359 |
| disjoint | 5 | 3 | random | expytky | 0.160 | 5.359 |
| disjoint | 5 | 5 | random | metrla | 0.200 | 6.692 |
| disjoint | 5 | 5 | random | pems04 | 0.180 | 6.692 |
| disjoint | 5 | 5 | random | chengdu | 0.120 | 6.692 |
| disjoint | 5 | 5 | random | shenzhen | 0.120 | 6.692 |
| disjoint | 5 | 5 | random | expytky | 0.180 | 6.692 |
| disjoint | 10 | 1 | own | metrla | 0.220 | 7.387 |
| disjoint | 10 | 1 | own | pems04 | 0.460 | 7.387 |
| disjoint | 10 | 1 | own | chengdu | 0.060 | 7.387 |
| disjoint | 10 | 1 | own | shenzhen | 0.280 | 7.387 |
| disjoint | 10 | 1 | own | expytky | 0.220 | 7.387 |
| disjoint | 10 | 3 | own | metrla | 0.320 | 8.720 |
| disjoint | 10 | 3 | own | pems04 | 0.640 | 8.720 |
| disjoint | 10 | 3 | own | chengdu | 0.220 | 8.720 |
| disjoint | 10 | 3 | own | shenzhen | 0.380 | 8.720 |
| disjoint | 10 | 3 | own | expytky | 0.360 | 8.720 |
| disjoint | 10 | 5 | own | metrla | 0.420 | 10.053 |
| disjoint | 10 | 5 | own | pems04 | 0.780 | 10.053 |
| disjoint | 10 | 5 | own | chengdu | 0.280 | 10.053 |
| disjoint | 10 | 5 | own | shenzhen | 0.400 | 10.053 |
| disjoint | 10 | 5 | own | expytky | 0.400 | 10.053 |
| disjoint | 10 | 1 | pooled | metrla | 0.420 | 7.387 |
| disjoint | 10 | 1 | pooled | pems04 | 0.480 | 7.387 |
| disjoint | 10 | 1 | pooled | chengdu | 0.060 | 7.387 |
| disjoint | 10 | 1 | pooled | shenzhen | 0.340 | 7.387 |
| disjoint | 10 | 1 | pooled | expytky | 0.360 | 7.387 |
| disjoint | 10 | 3 | pooled | metrla | 0.680 | 8.720 |
| disjoint | 10 | 3 | pooled | pems04 | 0.640 | 8.720 |
| disjoint | 10 | 3 | pooled | chengdu | 0.160 | 8.720 |
| disjoint | 10 | 3 | pooled | shenzhen | 0.500 | 8.720 |
| disjoint | 10 | 3 | pooled | expytky | 0.400 | 8.720 |
| disjoint | 10 | 5 | pooled | metrla | 0.800 | 10.053 |
| disjoint | 10 | 5 | pooled | pems04 | 0.780 | 10.053 |
| disjoint | 10 | 5 | pooled | chengdu | 0.160 | 10.053 |
| disjoint | 10 | 5 | pooled | shenzhen | 0.580 | 10.053 |
| disjoint | 10 | 5 | pooled | expytky | 0.560 | 10.053 |
| disjoint | 10 | 1 | pooled_own | metrla | 0.180 | 7.387 |
| disjoint | 10 | 1 | pooled_own | pems04 | 0.480 | 7.387 |
| disjoint | 10 | 1 | pooled_own | chengdu | 0.080 | 7.387 |
| disjoint | 10 | 1 | pooled_own | shenzhen | 0.300 | 7.387 |
| disjoint | 10 | 1 | pooled_own | expytky | 0.260 | 7.387 |
| disjoint | 10 | 3 | pooled_own | metrla | 0.440 | 8.720 |
| disjoint | 10 | 3 | pooled_own | pems04 | 0.720 | 8.720 |
| disjoint | 10 | 3 | pooled_own | chengdu | 0.220 | 8.720 |
| disjoint | 10 | 3 | pooled_own | shenzhen | 0.400 | 8.720 |
| disjoint | 10 | 3 | pooled_own | expytky | 0.340 | 8.720 |
| disjoint | 10 | 5 | pooled_own | metrla | 0.520 | 10.053 |
| disjoint | 10 | 5 | pooled_own | pems04 | 0.800 | 10.053 |
| disjoint | 10 | 5 | pooled_own | chengdu | 0.320 | 10.053 |
| disjoint | 10 | 5 | pooled_own | shenzhen | 0.440 | 10.053 |
| disjoint | 10 | 5 | pooled_own | expytky | 0.420 | 10.053 |
| disjoint | 10 | 1 | observed_mean | metrla | 0.320 | 7.387 |
| disjoint | 10 | 1 | observed_mean | pems04 | 0.360 | 7.387 |
| disjoint | 10 | 1 | observed_mean | chengdu | 0.120 | 7.387 |
| disjoint | 10 | 1 | observed_mean | shenzhen | 0.320 | 7.387 |
| disjoint | 10 | 1 | observed_mean | expytky | 0.220 | 7.387 |
| disjoint | 10 | 3 | observed_mean | metrla | 0.520 | 8.720 |
| disjoint | 10 | 3 | observed_mean | pems04 | 0.480 | 8.720 |
| disjoint | 10 | 3 | observed_mean | chengdu | 0.180 | 8.720 |
| disjoint | 10 | 3 | observed_mean | shenzhen | 0.420 | 8.720 |
| disjoint | 10 | 3 | observed_mean | expytky | 0.380 | 8.720 |
| disjoint | 10 | 5 | observed_mean | metrla | 0.620 | 10.053 |
| disjoint | 10 | 5 | observed_mean | pems04 | 0.640 | 10.053 |
| disjoint | 10 | 5 | observed_mean | chengdu | 0.280 | 10.053 |
| disjoint | 10 | 5 | observed_mean | shenzhen | 0.440 | 10.053 |
| disjoint | 10 | 5 | observed_mean | expytky | 0.520 | 10.053 |
| disjoint | 10 | 1 | random | metrla | 0.140 | 7.387 |
| disjoint | 10 | 1 | random | pems04 | 0.360 | 7.387 |
| disjoint | 10 | 1 | random | chengdu | 0.080 | 7.387 |
| disjoint | 10 | 1 | random | shenzhen | 0.240 | 7.387 |
| disjoint | 10 | 1 | random | expytky | 0.140 | 7.387 |
| disjoint | 10 | 3 | random | metrla | 0.160 | 8.720 |
| disjoint | 10 | 3 | random | pems04 | 0.360 | 8.720 |
| disjoint | 10 | 3 | random | chengdu | 0.100 | 8.720 |
| disjoint | 10 | 3 | random | shenzhen | 0.340 | 8.720 |
| disjoint | 10 | 3 | random | expytky | 0.160 | 8.720 |
| disjoint | 10 | 5 | random | metrla | 0.200 | 10.053 |
| disjoint | 10 | 5 | random | pems04 | 0.380 | 10.053 |
| disjoint | 10 | 5 | random | chengdu | 0.100 | 10.053 |
| disjoint | 10 | 5 | random | shenzhen | 0.340 | 10.053 |
| disjoint | 10 | 5 | random | expytky | 0.180 | 10.053 |
| disjoint | 15 | 1 | own | metrla | 0.340 | 10.813 |
| disjoint | 15 | 1 | own | pems04 | 0.500 | 10.813 |
| disjoint | 15 | 1 | own | chengdu | 0.240 | 10.813 |
| disjoint | 15 | 1 | own | shenzhen | 0.280 | 10.813 |
| disjoint | 15 | 1 | own | expytky | 0.260 | 10.813 |
| disjoint | 15 | 3 | own | metrla | 0.420 | 12.147 |
| disjoint | 15 | 3 | own | pems04 | 0.740 | 12.147 |
| disjoint | 15 | 3 | own | chengdu | 0.320 | 12.147 |
| disjoint | 15 | 3 | own | shenzhen | 0.520 | 12.147 |
| disjoint | 15 | 3 | own | expytky | 0.320 | 12.147 |
| disjoint | 15 | 5 | own | metrla | 0.540 | 13.480 |
| disjoint | 15 | 5 | own | pems04 | 0.820 | 13.480 |
| disjoint | 15 | 5 | own | chengdu | 0.400 | 13.480 |
| disjoint | 15 | 5 | own | shenzhen | 0.600 | 13.480 |
| disjoint | 15 | 5 | own | expytky | 0.400 | 13.480 |
| disjoint | 15 | 1 | pooled | metrla | 0.380 | 10.813 |
| disjoint | 15 | 1 | pooled | pems04 | 0.560 | 10.813 |
| disjoint | 15 | 1 | pooled | chengdu | 0.180 | 10.813 |
| disjoint | 15 | 1 | pooled | shenzhen | 0.380 | 10.813 |
| disjoint | 15 | 1 | pooled | expytky | 0.280 | 10.813 |
| disjoint | 15 | 3 | pooled | metrla | 0.640 | 12.147 |
| disjoint | 15 | 3 | pooled | pems04 | 0.840 | 12.147 |
| disjoint | 15 | 3 | pooled | chengdu | 0.220 | 12.147 |
| disjoint | 15 | 3 | pooled | shenzhen | 0.640 | 12.147 |
| disjoint | 15 | 3 | pooled | expytky | 0.440 | 12.147 |
| disjoint | 15 | 5 | pooled | metrla | 0.780 | 13.480 |
| disjoint | 15 | 5 | pooled | pems04 | 0.900 | 13.480 |
| disjoint | 15 | 5 | pooled | chengdu | 0.380 | 13.480 |
| disjoint | 15 | 5 | pooled | shenzhen | 0.700 | 13.480 |
| disjoint | 15 | 5 | pooled | expytky | 0.620 | 13.480 |
| disjoint | 15 | 1 | pooled_own | metrla | 0.340 | 10.813 |
| disjoint | 15 | 1 | pooled_own | pems04 | 0.520 | 10.813 |
| disjoint | 15 | 1 | pooled_own | chengdu | 0.240 | 10.813 |
| disjoint | 15 | 1 | pooled_own | shenzhen | 0.260 | 10.813 |
| disjoint | 15 | 1 | pooled_own | expytky | 0.260 | 10.813 |
| disjoint | 15 | 3 | pooled_own | metrla | 0.560 | 12.147 |
| disjoint | 15 | 3 | pooled_own | pems04 | 0.820 | 12.147 |
| disjoint | 15 | 3 | pooled_own | chengdu | 0.340 | 12.147 |
| disjoint | 15 | 3 | pooled_own | shenzhen | 0.480 | 12.147 |
| disjoint | 15 | 3 | pooled_own | expytky | 0.380 | 12.147 |
| disjoint | 15 | 5 | pooled_own | metrla | 0.620 | 13.480 |
| disjoint | 15 | 5 | pooled_own | pems04 | 0.880 | 13.480 |
| disjoint | 15 | 5 | pooled_own | chengdu | 0.460 | 13.480 |
| disjoint | 15 | 5 | pooled_own | shenzhen | 0.660 | 13.480 |
| disjoint | 15 | 5 | pooled_own | expytky | 0.500 | 13.480 |
| disjoint | 15 | 1 | observed_mean | metrla | 0.480 | 10.813 |
| disjoint | 15 | 1 | observed_mean | pems04 | 0.420 | 10.813 |
| disjoint | 15 | 1 | observed_mean | chengdu | 0.220 | 10.813 |
| disjoint | 15 | 1 | observed_mean | shenzhen | 0.400 | 10.813 |
| disjoint | 15 | 1 | observed_mean | expytky | 0.300 | 10.813 |
| disjoint | 15 | 3 | observed_mean | metrla | 0.640 | 12.147 |
| disjoint | 15 | 3 | observed_mean | pems04 | 0.600 | 12.147 |
| disjoint | 15 | 3 | observed_mean | chengdu | 0.380 | 12.147 |
| disjoint | 15 | 3 | observed_mean | shenzhen | 0.640 | 12.147 |
| disjoint | 15 | 3 | observed_mean | expytky | 0.500 | 12.147 |
| disjoint | 15 | 5 | observed_mean | metrla | 0.720 | 13.480 |
| disjoint | 15 | 5 | observed_mean | pems04 | 0.700 | 13.480 |
| disjoint | 15 | 5 | observed_mean | chengdu | 0.460 | 13.480 |
| disjoint | 15 | 5 | observed_mean | shenzhen | 0.720 | 13.480 |
| disjoint | 15 | 5 | observed_mean | expytky | 0.580 | 13.480 |
| disjoint | 15 | 1 | random | metrla | 0.220 | 10.813 |
| disjoint | 15 | 1 | random | pems04 | 0.340 | 10.813 |
| disjoint | 15 | 1 | random | chengdu | 0.200 | 10.813 |
| disjoint | 15 | 1 | random | shenzhen | 0.260 | 10.813 |
| disjoint | 15 | 1 | random | expytky | 0.180 | 10.813 |
| disjoint | 15 | 3 | random | metrla | 0.280 | 12.147 |
| disjoint | 15 | 3 | random | pems04 | 0.400 | 12.147 |
| disjoint | 15 | 3 | random | chengdu | 0.260 | 12.147 |
| disjoint | 15 | 3 | random | shenzhen | 0.300 | 12.147 |
| disjoint | 15 | 3 | random | expytky | 0.180 | 12.147 |
| disjoint | 15 | 5 | random | metrla | 0.320 | 13.480 |
| disjoint | 15 | 5 | random | pems04 | 0.420 | 13.480 |
| disjoint | 15 | 5 | random | chengdu | 0.300 | 13.480 |
| disjoint | 15 | 5 | random | shenzhen | 0.300 | 13.480 |
| disjoint | 15 | 5 | random | expytky | 0.220 | 13.480 |
| disjoint | 30 | 1 | own | metrla | 0.480 | 20.690 |
| disjoint | 30 | 1 | own | pems04 | 0.740 | 20.690 |
| disjoint | 30 | 1 | own | chengdu | 0.420 | 20.690 |
| disjoint | 30 | 1 | own | shenzhen | 0.440 | 20.690 |
| disjoint | 30 | 1 | own | expytky | 0.420 | 20.690 |
| disjoint | 30 | 3 | own | metrla | 0.620 | 22.023 |
| disjoint | 30 | 3 | own | pems04 | 0.880 | 22.023 |
| disjoint | 30 | 3 | own | chengdu | 0.600 | 22.023 |
| disjoint | 30 | 3 | own | shenzhen | 0.520 | 22.023 |
| disjoint | 30 | 3 | own | expytky | 0.480 | 22.023 |
| disjoint | 30 | 5 | own | metrla | 0.780 | 23.357 |
| disjoint | 30 | 5 | own | pems04 | 0.940 | 23.357 |
| disjoint | 30 | 5 | own | chengdu | 0.640 | 23.357 |
| disjoint | 30 | 5 | own | shenzhen | 0.620 | 23.357 |
| disjoint | 30 | 5 | own | expytky | 0.520 | 23.357 |
| disjoint | 30 | 1 | pooled | metrla | 0.560 | 20.690 |
| disjoint | 30 | 1 | pooled | pems04 | 0.720 | 20.690 |
| disjoint | 30 | 1 | pooled | chengdu | 0.400 | 20.690 |
| disjoint | 30 | 1 | pooled | shenzhen | 0.500 | 20.690 |
| disjoint | 30 | 1 | pooled | expytky | 0.320 | 20.690 |
| disjoint | 30 | 3 | pooled | metrla | 0.760 | 22.023 |
| disjoint | 30 | 3 | pooled | pems04 | 0.980 | 22.023 |
| disjoint | 30 | 3 | pooled | chengdu | 0.460 | 22.023 |
| disjoint | 30 | 3 | pooled | shenzhen | 0.760 | 22.023 |
| disjoint | 30 | 3 | pooled | expytky | 0.440 | 22.023 |
| disjoint | 30 | 5 | pooled | metrla | 0.940 | 23.357 |
| disjoint | 30 | 5 | pooled | pems04 | 1.000 | 23.357 |
| disjoint | 30 | 5 | pooled | chengdu | 0.600 | 23.357 |
| disjoint | 30 | 5 | pooled | shenzhen | 0.920 | 23.357 |
| disjoint | 30 | 5 | pooled | expytky | 0.580 | 23.357 |
| disjoint | 30 | 1 | pooled_own | metrla | 0.460 | 20.690 |
| disjoint | 30 | 1 | pooled_own | pems04 | 0.740 | 20.690 |
| disjoint | 30 | 1 | pooled_own | chengdu | 0.420 | 20.690 |
| disjoint | 30 | 1 | pooled_own | shenzhen | 0.440 | 20.690 |
| disjoint | 30 | 1 | pooled_own | expytky | 0.440 | 20.690 |
| disjoint | 30 | 3 | pooled_own | metrla | 0.760 | 22.023 |
| disjoint | 30 | 3 | pooled_own | pems04 | 0.920 | 22.023 |
| disjoint | 30 | 3 | pooled_own | chengdu | 0.580 | 22.023 |
| disjoint | 30 | 3 | pooled_own | shenzhen | 0.580 | 22.023 |
| disjoint | 30 | 3 | pooled_own | expytky | 0.500 | 22.023 |
| disjoint | 30 | 5 | pooled_own | metrla | 0.840 | 23.357 |
| disjoint | 30 | 5 | pooled_own | pems04 | 0.940 | 23.357 |
| disjoint | 30 | 5 | pooled_own | chengdu | 0.660 | 23.357 |
| disjoint | 30 | 5 | pooled_own | shenzhen | 0.640 | 23.357 |
| disjoint | 30 | 5 | pooled_own | expytky | 0.540 | 23.357 |
| disjoint | 30 | 1 | observed_mean | metrla | 0.580 | 20.690 |
| disjoint | 30 | 1 | observed_mean | pems04 | 0.520 | 20.690 |
| disjoint | 30 | 1 | observed_mean | chengdu | 0.460 | 20.690 |
| disjoint | 30 | 1 | observed_mean | shenzhen | 0.540 | 20.690 |
| disjoint | 30 | 1 | observed_mean | expytky | 0.400 | 20.690 |
| disjoint | 30 | 3 | observed_mean | metrla | 0.780 | 22.023 |
| disjoint | 30 | 3 | observed_mean | pems04 | 0.680 | 22.023 |
| disjoint | 30 | 3 | observed_mean | chengdu | 0.580 | 22.023 |
| disjoint | 30 | 3 | observed_mean | shenzhen | 0.740 | 22.023 |
| disjoint | 30 | 3 | observed_mean | expytky | 0.540 | 22.023 |
| disjoint | 30 | 5 | observed_mean | metrla | 0.900 | 23.357 |
| disjoint | 30 | 5 | observed_mean | pems04 | 0.800 | 23.357 |
| disjoint | 30 | 5 | observed_mean | chengdu | 0.660 | 23.357 |
| disjoint | 30 | 5 | observed_mean | shenzhen | 0.840 | 23.357 |
| disjoint | 30 | 5 | observed_mean | expytky | 0.700 | 23.357 |
| disjoint | 30 | 1 | random | metrla | 0.320 | 20.690 |
| disjoint | 30 | 1 | random | pems04 | 0.420 | 20.690 |
| disjoint | 30 | 1 | random | chengdu | 0.380 | 20.690 |
| disjoint | 30 | 1 | random | shenzhen | 0.320 | 20.690 |
| disjoint | 30 | 1 | random | expytky | 0.300 | 20.690 |
| disjoint | 30 | 3 | random | metrla | 0.400 | 22.023 |
| disjoint | 30 | 3 | random | pems04 | 0.440 | 22.023 |
| disjoint | 30 | 3 | random | chengdu | 0.380 | 22.023 |
| disjoint | 30 | 3 | random | shenzhen | 0.320 | 22.023 |
| disjoint | 30 | 3 | random | expytky | 0.320 | 22.023 |
| disjoint | 30 | 5 | random | metrla | 0.440 | 23.357 |
| disjoint | 30 | 5 | random | pems04 | 0.460 | 23.357 |
| disjoint | 30 | 5 | random | chengdu | 0.400 | 23.357 |
| disjoint | 30 | 5 | random | shenzhen | 0.380 | 23.357 |
| disjoint | 30 | 5 | random | expytky | 0.340 | 23.357 |
| anchor | 5 | 1 | own | metrla | 0.100 | 3.915 |
| anchor | 5 | 1 | own | pems04 | 0.340 | 3.915 |
| anchor | 5 | 1 | own | chengdu | 0.060 | 3.915 |
| anchor | 5 | 1 | own | shenzhen | 0.080 | 3.915 |
| anchor | 5 | 1 | own | expytky | 0.020 | 3.915 |
| anchor | 5 | 3 | own | metrla | 0.140 | 5.249 |
| anchor | 5 | 3 | own | pems04 | 0.500 | 5.249 |
| anchor | 5 | 3 | own | chengdu | 0.100 | 5.249 |
| anchor | 5 | 3 | own | shenzhen | 0.140 | 5.249 |
| anchor | 5 | 3 | own | expytky | 0.200 | 5.249 |
| anchor | 5 | 5 | own | metrla | 0.200 | 6.582 |
| anchor | 5 | 5 | own | pems04 | 0.540 | 6.582 |
| anchor | 5 | 5 | own | chengdu | 0.220 | 6.582 |
| anchor | 5 | 5 | own | shenzhen | 0.180 | 6.582 |
| anchor | 5 | 5 | own | expytky | 0.300 | 6.582 |
| anchor | 5 | 1 | pooled | metrla | 0.180 | 3.915 |
| anchor | 5 | 1 | pooled | pems04 | 0.280 | 3.915 |
| anchor | 5 | 1 | pooled | chengdu | 0.060 | 3.915 |
| anchor | 5 | 1 | pooled | shenzhen | 0.080 | 3.915 |
| anchor | 5 | 1 | pooled | expytky | 0.140 | 3.915 |
| anchor | 5 | 3 | pooled | metrla | 0.300 | 5.249 |
| anchor | 5 | 3 | pooled | pems04 | 0.460 | 5.249 |
| anchor | 5 | 3 | pooled | chengdu | 0.140 | 5.249 |
| anchor | 5 | 3 | pooled | shenzhen | 0.200 | 5.249 |
| anchor | 5 | 3 | pooled | expytky | 0.220 | 5.249 |
| anchor | 5 | 5 | pooled | metrla | 0.420 | 6.582 |
| anchor | 5 | 5 | pooled | pems04 | 0.560 | 6.582 |
| anchor | 5 | 5 | pooled | chengdu | 0.240 | 6.582 |
| anchor | 5 | 5 | pooled | shenzhen | 0.280 | 6.582 |
| anchor | 5 | 5 | pooled | expytky | 0.420 | 6.582 |
| anchor | 5 | 1 | pooled_own | metrla | 0.100 | 3.915 |
| anchor | 5 | 1 | pooled_own | pems04 | 0.320 | 3.915 |
| anchor | 5 | 1 | pooled_own | chengdu | 0.040 | 3.915 |
| anchor | 5 | 1 | pooled_own | shenzhen | 0.080 | 3.915 |
| anchor | 5 | 1 | pooled_own | expytky | 0.040 | 3.915 |
| anchor | 5 | 3 | pooled_own | metrla | 0.160 | 5.249 |
| anchor | 5 | 3 | pooled_own | pems04 | 0.500 | 5.249 |
| anchor | 5 | 3 | pooled_own | chengdu | 0.140 | 5.249 |
| anchor | 5 | 3 | pooled_own | shenzhen | 0.120 | 5.249 |
| anchor | 5 | 3 | pooled_own | expytky | 0.260 | 5.249 |
| anchor | 5 | 5 | pooled_own | metrla | 0.200 | 6.582 |
| anchor | 5 | 5 | pooled_own | pems04 | 0.580 | 6.582 |
| anchor | 5 | 5 | pooled_own | chengdu | 0.240 | 6.582 |
| anchor | 5 | 5 | pooled_own | shenzhen | 0.180 | 6.582 |
| anchor | 5 | 5 | pooled_own | expytky | 0.360 | 6.582 |
| anchor | 5 | 1 | observed_mean | metrla | 0.160 | 3.915 |
| anchor | 5 | 1 | observed_mean | pems04 | 0.220 | 3.915 |
| anchor | 5 | 1 | observed_mean | chengdu | 0.060 | 3.915 |
| anchor | 5 | 1 | observed_mean | shenzhen | 0.100 | 3.915 |
| anchor | 5 | 1 | observed_mean | expytky | 0.100 | 3.915 |
| anchor | 5 | 3 | observed_mean | metrla | 0.280 | 5.249 |
| anchor | 5 | 3 | observed_mean | pems04 | 0.380 | 5.249 |
| anchor | 5 | 3 | observed_mean | chengdu | 0.100 | 5.249 |
| anchor | 5 | 3 | observed_mean | shenzhen | 0.240 | 5.249 |
| anchor | 5 | 3 | observed_mean | expytky | 0.240 | 5.249 |
| anchor | 5 | 5 | observed_mean | metrla | 0.380 | 6.582 |
| anchor | 5 | 5 | observed_mean | pems04 | 0.520 | 6.582 |
| anchor | 5 | 5 | observed_mean | chengdu | 0.200 | 6.582 |
| anchor | 5 | 5 | observed_mean | shenzhen | 0.280 | 6.582 |
| anchor | 5 | 5 | observed_mean | expytky | 0.340 | 6.582 |
| anchor | 5 | 1 | random | metrla | 0.100 | 3.915 |
| anchor | 5 | 1 | random | pems04 | 0.200 | 3.915 |
| anchor | 5 | 1 | random | chengdu | 0.040 | 3.915 |
| anchor | 5 | 1 | random | shenzhen | 0.060 | 3.915 |
| anchor | 5 | 1 | random | expytky | 0.040 | 3.915 |
| anchor | 5 | 3 | random | metrla | 0.120 | 5.249 |
| anchor | 5 | 3 | random | pems04 | 0.220 | 5.249 |
| anchor | 5 | 3 | random | chengdu | 0.040 | 5.249 |
| anchor | 5 | 3 | random | shenzhen | 0.080 | 5.249 |
| anchor | 5 | 3 | random | expytky | 0.080 | 5.249 |
| anchor | 5 | 5 | random | metrla | 0.160 | 6.582 |
| anchor | 5 | 5 | random | pems04 | 0.220 | 6.582 |
| anchor | 5 | 5 | random | chengdu | 0.060 | 6.582 |
| anchor | 5 | 5 | random | shenzhen | 0.080 | 6.582 |
| anchor | 5 | 5 | random | expytky | 0.140 | 6.582 |
| anchor | 10 | 1 | own | metrla | 0.240 | 7.224 |
| anchor | 10 | 1 | own | pems04 | 0.400 | 7.224 |
| anchor | 10 | 1 | own | chengdu | 0.200 | 7.224 |
| anchor | 10 | 1 | own | shenzhen | 0.120 | 7.224 |
| anchor | 10 | 1 | own | expytky | 0.200 | 7.224 |
| anchor | 10 | 3 | own | metrla | 0.340 | 8.557 |
| anchor | 10 | 3 | own | pems04 | 0.620 | 8.557 |
| anchor | 10 | 3 | own | chengdu | 0.340 | 8.557 |
| anchor | 10 | 3 | own | shenzhen | 0.240 | 8.557 |
| anchor | 10 | 3 | own | expytky | 0.320 | 8.557 |
| anchor | 10 | 5 | own | metrla | 0.380 | 9.890 |
| anchor | 10 | 5 | own | pems04 | 0.760 | 9.890 |
| anchor | 10 | 5 | own | chengdu | 0.400 | 9.890 |
| anchor | 10 | 5 | own | shenzhen | 0.300 | 9.890 |
| anchor | 10 | 5 | own | expytky | 0.400 | 9.890 |
| anchor | 10 | 1 | pooled | metrla | 0.280 | 7.224 |
| anchor | 10 | 1 | pooled | pems04 | 0.360 | 7.224 |
| anchor | 10 | 1 | pooled | chengdu | 0.140 | 7.224 |
| anchor | 10 | 1 | pooled | shenzhen | 0.140 | 7.224 |
| anchor | 10 | 1 | pooled | expytky | 0.220 | 7.224 |
| anchor | 10 | 3 | pooled | metrla | 0.480 | 8.557 |
| anchor | 10 | 3 | pooled | pems04 | 0.580 | 8.557 |
| anchor | 10 | 3 | pooled | chengdu | 0.240 | 8.557 |
| anchor | 10 | 3 | pooled | shenzhen | 0.260 | 8.557 |
| anchor | 10 | 3 | pooled | expytky | 0.340 | 8.557 |
| anchor | 10 | 5 | pooled | metrla | 0.600 | 9.890 |
| anchor | 10 | 5 | pooled | pems04 | 0.740 | 9.890 |
| anchor | 10 | 5 | pooled | chengdu | 0.320 | 9.890 |
| anchor | 10 | 5 | pooled | shenzhen | 0.320 | 9.890 |
| anchor | 10 | 5 | pooled | expytky | 0.480 | 9.890 |
| anchor | 10 | 1 | pooled_own | metrla | 0.240 | 7.224 |
| anchor | 10 | 1 | pooled_own | pems04 | 0.440 | 7.224 |
| anchor | 10 | 1 | pooled_own | chengdu | 0.180 | 7.224 |
| anchor | 10 | 1 | pooled_own | shenzhen | 0.120 | 7.224 |
| anchor | 10 | 1 | pooled_own | expytky | 0.180 | 7.224 |
| anchor | 10 | 3 | pooled_own | metrla | 0.340 | 8.557 |
| anchor | 10 | 3 | pooled_own | pems04 | 0.700 | 8.557 |
| anchor | 10 | 3 | pooled_own | chengdu | 0.400 | 8.557 |
| anchor | 10 | 3 | pooled_own | shenzhen | 0.220 | 8.557 |
| anchor | 10 | 3 | pooled_own | expytky | 0.320 | 8.557 |
| anchor | 10 | 5 | pooled_own | metrla | 0.420 | 9.890 |
| anchor | 10 | 5 | pooled_own | pems04 | 0.820 | 9.890 |
| anchor | 10 | 5 | pooled_own | chengdu | 0.440 | 9.890 |
| anchor | 10 | 5 | pooled_own | shenzhen | 0.320 | 9.890 |
| anchor | 10 | 5 | pooled_own | expytky | 0.380 | 9.890 |
| anchor | 10 | 1 | observed_mean | metrla | 0.360 | 7.224 |
| anchor | 10 | 1 | observed_mean | pems04 | 0.340 | 7.224 |
| anchor | 10 | 1 | observed_mean | chengdu | 0.160 | 7.224 |
| anchor | 10 | 1 | observed_mean | shenzhen | 0.180 | 7.224 |
| anchor | 10 | 1 | observed_mean | expytky | 0.260 | 7.224 |
| anchor | 10 | 3 | observed_mean | metrla | 0.440 | 8.557 |
| anchor | 10 | 3 | observed_mean | pems04 | 0.500 | 8.557 |
| anchor | 10 | 3 | observed_mean | chengdu | 0.260 | 8.557 |
| anchor | 10 | 3 | observed_mean | shenzhen | 0.320 | 8.557 |
| anchor | 10 | 3 | observed_mean | expytky | 0.360 | 8.557 |
| anchor | 10 | 5 | observed_mean | metrla | 0.560 | 9.890 |
| anchor | 10 | 5 | observed_mean | pems04 | 0.660 | 9.890 |
| anchor | 10 | 5 | observed_mean | chengdu | 0.280 | 9.890 |
| anchor | 10 | 5 | observed_mean | shenzhen | 0.360 | 9.890 |
| anchor | 10 | 5 | observed_mean | expytky | 0.480 | 9.890 |
| anchor | 10 | 1 | random | metrla | 0.200 | 7.224 |
| anchor | 10 | 1 | random | pems04 | 0.220 | 7.224 |
| anchor | 10 | 1 | random | chengdu | 0.140 | 7.224 |
| anchor | 10 | 1 | random | shenzhen | 0.140 | 7.224 |
| anchor | 10 | 1 | random | expytky | 0.160 | 7.224 |
| anchor | 10 | 3 | random | metrla | 0.200 | 8.557 |
| anchor | 10 | 3 | random | pems04 | 0.240 | 8.557 |
| anchor | 10 | 3 | random | chengdu | 0.140 | 8.557 |
| anchor | 10 | 3 | random | shenzhen | 0.140 | 8.557 |
| anchor | 10 | 3 | random | expytky | 0.160 | 8.557 |
| anchor | 10 | 5 | random | metrla | 0.240 | 9.890 |
| anchor | 10 | 5 | random | pems04 | 0.260 | 9.890 |
| anchor | 10 | 5 | random | chengdu | 0.200 | 9.890 |
| anchor | 10 | 5 | random | shenzhen | 0.160 | 9.890 |
| anchor | 10 | 5 | random | expytky | 0.180 | 9.890 |
| anchor | 15 | 1 | own | metrla | 0.300 | 10.381 |
| anchor | 15 | 1 | own | pems04 | 0.560 | 10.381 |
| anchor | 15 | 1 | own | chengdu | 0.120 | 10.381 |
| anchor | 15 | 1 | own | shenzhen | 0.180 | 10.381 |
| anchor | 15 | 1 | own | expytky | 0.240 | 10.381 |
| anchor | 15 | 3 | own | metrla | 0.420 | 11.715 |
| anchor | 15 | 3 | own | pems04 | 0.720 | 11.715 |
| anchor | 15 | 3 | own | chengdu | 0.200 | 11.715 |
| anchor | 15 | 3 | own | shenzhen | 0.260 | 11.715 |
| anchor | 15 | 3 | own | expytky | 0.420 | 11.715 |
| anchor | 15 | 5 | own | metrla | 0.460 | 13.048 |
| anchor | 15 | 5 | own | pems04 | 0.800 | 13.048 |
| anchor | 15 | 5 | own | chengdu | 0.300 | 13.048 |
| anchor | 15 | 5 | own | shenzhen | 0.420 | 13.048 |
| anchor | 15 | 5 | own | expytky | 0.540 | 13.048 |
| anchor | 15 | 1 | pooled | metrla | 0.380 | 10.381 |
| anchor | 15 | 1 | pooled | pems04 | 0.520 | 10.381 |
| anchor | 15 | 1 | pooled | chengdu | 0.100 | 10.381 |
| anchor | 15 | 1 | pooled | shenzhen | 0.260 | 10.381 |
| anchor | 15 | 1 | pooled | expytky | 0.240 | 10.381 |
| anchor | 15 | 3 | pooled | metrla | 0.540 | 11.715 |
| anchor | 15 | 3 | pooled | pems04 | 0.780 | 11.715 |
| anchor | 15 | 3 | pooled | chengdu | 0.180 | 11.715 |
| anchor | 15 | 3 | pooled | shenzhen | 0.380 | 11.715 |
| anchor | 15 | 3 | pooled | expytky | 0.400 | 11.715 |
| anchor | 15 | 5 | pooled | metrla | 0.740 | 13.048 |
| anchor | 15 | 5 | pooled | pems04 | 0.900 | 13.048 |
| anchor | 15 | 5 | pooled | chengdu | 0.260 | 13.048 |
| anchor | 15 | 5 | pooled | shenzhen | 0.520 | 13.048 |
| anchor | 15 | 5 | pooled | expytky | 0.460 | 13.048 |
| anchor | 15 | 1 | pooled_own | metrla | 0.320 | 10.381 |
| anchor | 15 | 1 | pooled_own | pems04 | 0.580 | 10.381 |
| anchor | 15 | 1 | pooled_own | chengdu | 0.120 | 10.381 |
| anchor | 15 | 1 | pooled_own | shenzhen | 0.200 | 10.381 |
| anchor | 15 | 1 | pooled_own | expytky | 0.280 | 10.381 |
| anchor | 15 | 3 | pooled_own | metrla | 0.440 | 11.715 |
| anchor | 15 | 3 | pooled_own | pems04 | 0.740 | 11.715 |
| anchor | 15 | 3 | pooled_own | chengdu | 0.200 | 11.715 |
| anchor | 15 | 3 | pooled_own | shenzhen | 0.320 | 11.715 |
| anchor | 15 | 3 | pooled_own | expytky | 0.400 | 11.715 |
| anchor | 15 | 5 | pooled_own | metrla | 0.500 | 13.048 |
| anchor | 15 | 5 | pooled_own | pems04 | 0.820 | 13.048 |
| anchor | 15 | 5 | pooled_own | chengdu | 0.280 | 13.048 |
| anchor | 15 | 5 | pooled_own | shenzhen | 0.480 | 13.048 |
| anchor | 15 | 5 | pooled_own | expytky | 0.520 | 13.048 |
| anchor | 15 | 1 | observed_mean | metrla | 0.380 | 10.381 |
| anchor | 15 | 1 | observed_mean | pems04 | 0.400 | 10.381 |
| anchor | 15 | 1 | observed_mean | chengdu | 0.100 | 10.381 |
| anchor | 15 | 1 | observed_mean | shenzhen | 0.260 | 10.381 |
| anchor | 15 | 1 | observed_mean | expytky | 0.280 | 10.381 |
| anchor | 15 | 3 | observed_mean | metrla | 0.500 | 11.715 |
| anchor | 15 | 3 | observed_mean | pems04 | 0.560 | 11.715 |
| anchor | 15 | 3 | observed_mean | chengdu | 0.220 | 11.715 |
| anchor | 15 | 3 | observed_mean | shenzhen | 0.400 | 11.715 |
| anchor | 15 | 3 | observed_mean | expytky | 0.400 | 11.715 |
| anchor | 15 | 5 | observed_mean | metrla | 0.600 | 13.048 |
| anchor | 15 | 5 | observed_mean | pems04 | 0.600 | 13.048 |
| anchor | 15 | 5 | observed_mean | chengdu | 0.360 | 13.048 |
| anchor | 15 | 5 | observed_mean | shenzhen | 0.500 | 13.048 |
| anchor | 15 | 5 | observed_mean | expytky | 0.460 | 13.048 |
| anchor | 15 | 1 | random | metrla | 0.220 | 10.381 |
| anchor | 15 | 1 | random | pems04 | 0.300 | 10.381 |
| anchor | 15 | 1 | random | chengdu | 0.120 | 10.381 |
| anchor | 15 | 1 | random | shenzhen | 0.160 | 10.381 |
| anchor | 15 | 1 | random | expytky | 0.260 | 10.381 |
| anchor | 15 | 3 | random | metrla | 0.240 | 11.715 |
| anchor | 15 | 3 | random | pems04 | 0.380 | 11.715 |
| anchor | 15 | 3 | random | chengdu | 0.120 | 11.715 |
| anchor | 15 | 3 | random | shenzhen | 0.160 | 11.715 |
| anchor | 15 | 3 | random | expytky | 0.260 | 11.715 |
| anchor | 15 | 5 | random | metrla | 0.260 | 13.048 |
| anchor | 15 | 5 | random | pems04 | 0.440 | 13.048 |
| anchor | 15 | 5 | random | chengdu | 0.160 | 13.048 |
| anchor | 15 | 5 | random | shenzhen | 0.200 | 13.048 |
| anchor | 15 | 5 | random | expytky | 0.260 | 13.048 |
| anchor | 30 | 1 | own | metrla | 0.540 | 20.532 |
| anchor | 30 | 1 | own | pems04 | 0.740 | 20.532 |
| anchor | 30 | 1 | own | chengdu | 0.440 | 20.532 |
| anchor | 30 | 1 | own | shenzhen | 0.460 | 20.532 |
| anchor | 30 | 1 | own | expytky | 0.480 | 20.532 |
| anchor | 30 | 3 | own | metrla | 0.720 | 21.866 |
| anchor | 30 | 3 | own | pems04 | 0.960 | 21.866 |
| anchor | 30 | 3 | own | chengdu | 0.560 | 21.866 |
| anchor | 30 | 3 | own | shenzhen | 0.600 | 21.866 |
| anchor | 30 | 3 | own | expytky | 0.560 | 21.866 |
| anchor | 30 | 5 | own | metrla | 0.820 | 23.199 |
| anchor | 30 | 5 | own | pems04 | 1.000 | 23.199 |
| anchor | 30 | 5 | own | chengdu | 0.600 | 23.199 |
| anchor | 30 | 5 | own | shenzhen | 0.660 | 23.199 |
| anchor | 30 | 5 | own | expytky | 0.660 | 23.199 |
| anchor | 30 | 1 | pooled | metrla | 0.580 | 20.532 |
| anchor | 30 | 1 | pooled | pems04 | 0.700 | 20.532 |
| anchor | 30 | 1 | pooled | chengdu | 0.380 | 20.532 |
| anchor | 30 | 1 | pooled | shenzhen | 0.540 | 20.532 |
| anchor | 30 | 1 | pooled | expytky | 0.360 | 20.532 |
| anchor | 30 | 3 | pooled | metrla | 0.780 | 21.866 |
| anchor | 30 | 3 | pooled | pems04 | 0.880 | 21.866 |
| anchor | 30 | 3 | pooled | chengdu | 0.420 | 21.866 |
| anchor | 30 | 3 | pooled | shenzhen | 0.660 | 21.866 |
| anchor | 30 | 3 | pooled | expytky | 0.500 | 21.866 |
| anchor | 30 | 5 | pooled | metrla | 0.940 | 23.199 |
| anchor | 30 | 5 | pooled | pems04 | 0.940 | 23.199 |
| anchor | 30 | 5 | pooled | chengdu | 0.480 | 23.199 |
| anchor | 30 | 5 | pooled | shenzhen | 0.760 | 23.199 |
| anchor | 30 | 5 | pooled | expytky | 0.560 | 23.199 |
| anchor | 30 | 1 | pooled_own | metrla | 0.560 | 20.532 |
| anchor | 30 | 1 | pooled_own | pems04 | 0.740 | 20.532 |
| anchor | 30 | 1 | pooled_own | chengdu | 0.460 | 20.532 |
| anchor | 30 | 1 | pooled_own | shenzhen | 0.500 | 20.532 |
| anchor | 30 | 1 | pooled_own | expytky | 0.460 | 20.532 |
| anchor | 30 | 3 | pooled_own | metrla | 0.780 | 21.866 |
| anchor | 30 | 3 | pooled_own | pems04 | 0.980 | 21.866 |
| anchor | 30 | 3 | pooled_own | chengdu | 0.560 | 21.866 |
| anchor | 30 | 3 | pooled_own | shenzhen | 0.620 | 21.866 |
| anchor | 30 | 3 | pooled_own | expytky | 0.540 | 21.866 |
| anchor | 30 | 5 | pooled_own | metrla | 0.840 | 23.199 |
| anchor | 30 | 5 | pooled_own | pems04 | 1.000 | 23.199 |
| anchor | 30 | 5 | pooled_own | chengdu | 0.620 | 23.199 |
| anchor | 30 | 5 | pooled_own | shenzhen | 0.720 | 23.199 |
| anchor | 30 | 5 | pooled_own | expytky | 0.660 | 23.199 |
| anchor | 30 | 1 | observed_mean | metrla | 0.740 | 20.532 |
| anchor | 30 | 1 | observed_mean | pems04 | 0.600 | 20.532 |
| anchor | 30 | 1 | observed_mean | chengdu | 0.440 | 20.532 |
| anchor | 30 | 1 | observed_mean | shenzhen | 0.640 | 20.532 |
| anchor | 30 | 1 | observed_mean | expytky | 0.400 | 20.532 |
| anchor | 30 | 3 | observed_mean | metrla | 0.840 | 21.866 |
| anchor | 30 | 3 | observed_mean | pems04 | 0.700 | 21.866 |
| anchor | 30 | 3 | observed_mean | chengdu | 0.580 | 21.866 |
| anchor | 30 | 3 | observed_mean | shenzhen | 0.720 | 21.866 |
| anchor | 30 | 3 | observed_mean | expytky | 0.660 | 21.866 |
| anchor | 30 | 5 | observed_mean | metrla | 0.840 | 23.199 |
| anchor | 30 | 5 | observed_mean | pems04 | 0.780 | 23.199 |
| anchor | 30 | 5 | observed_mean | chengdu | 0.660 | 23.199 |
| anchor | 30 | 5 | observed_mean | shenzhen | 0.780 | 23.199 |
| anchor | 30 | 5 | observed_mean | expytky | 0.760 | 23.199 |
| anchor | 30 | 1 | random | metrla | 0.380 | 20.532 |
| anchor | 30 | 1 | random | pems04 | 0.400 | 20.532 |
| anchor | 30 | 1 | random | chengdu | 0.380 | 20.532 |
| anchor | 30 | 1 | random | shenzhen | 0.420 | 20.532 |
| anchor | 30 | 1 | random | expytky | 0.340 | 20.532 |
| anchor | 30 | 3 | random | metrla | 0.380 | 21.866 |
| anchor | 30 | 3 | random | pems04 | 0.400 | 21.866 |
| anchor | 30 | 3 | random | chengdu | 0.380 | 21.866 |
| anchor | 30 | 3 | random | shenzhen | 0.480 | 21.866 |
| anchor | 30 | 3 | random | expytky | 0.360 | 21.866 |
| anchor | 30 | 5 | random | metrla | 0.380 | 23.199 |
| anchor | 30 | 5 | random | pems04 | 0.440 | 23.199 |
| anchor | 30 | 5 | random | chengdu | 0.400 | 23.199 |
| anchor | 30 | 5 | random | shenzhen | 0.480 | 23.199 |
| anchor | 30 | 5 | random | expytky | 0.380 | 23.199 |
