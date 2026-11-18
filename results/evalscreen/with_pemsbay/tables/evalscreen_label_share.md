# evalscreen label_share: a sparse label matrix shared by the cities

n architectures are trained at each city (design: independent, disjoint, or anchor = half common and half disjoint); a model predicts every missing entry; each city trains its b best predictions and keeps the best architecture it trained. share = the share of 50 random designs where that architecture lies within one sigma_seed of the best of the list. fleet_cost_pct = the GPU-hours of all pairs and picks over the GPU-hours of the whole matrix. own = a ridge on the labels of the city alone; pooled = one ridge on all trained pairs; pooled_own = own with the pooled prediction as an input; observed_mean = the mean rank at the cities that trained the architecture. Pass: a sharing model with a share of 0.9 or more at three of four cities at a fleet cost of 10 % or less, and a mean share above own at every setting.

### Verdict

| model | settings_at_10pct_with_3_cities | share_of_settings_above_own | cheapest_setting_with_3_cities_pct | pass |
|---|---|---|---|---|
| pooled | 0 | 0.970 | 23.353 | False |
| pooled_own | 0 | 0.909 |  | False |
| observed_mean | 0 | 1.000 | 23.353 | False |

### Reference: one city trained in full

| reference | fleet_cost_pct | other_cities_within_sigma |
|---|---|---|
| metrla in full, transfer of its best 5 | 16.520 | 5 |
| pems04 in full, transfer of its best 5 | 15.713 | 3 |
| chengdu in full, transfer of its best 5 | 10.565 | 3 |
| shenzhen in full, transfer of its best 5 | 15.872 | 5 |
| expytky in full, transfer of its best 5 | 25.882 | 4 |
| pemsbay in full, transfer of its best 5 | 31.730 | 4 |

### Every setting

| design | n | b | model | fleet_cost_pct | mean_share | min_share | cities_ge_09 | above_own |
|---|---|---|---|---|---|---|---|---|
| anchor | 5 | 1 | observed_mean | 3.937 | 0.110 | 0.060 | 0 | True |
| anchor | 5 | 1 | own | 3.937 | 0.107 | 0.020 | 0 | False |
| anchor | 5 | 1 | pooled | 3.937 | 0.130 | 0.040 | 0 | True |
| anchor | 5 | 1 | pooled_own | 3.937 | 0.110 | 0.020 | 0 | True |
| anchor | 5 | 1 | random | 3.937 | 0.077 | 0.020 | 0 | False |
| anchor | 5 | 3 | observed_mean | 5.270 | 0.217 | 0.120 | 0 | True |
| anchor | 5 | 3 | own | 5.270 | 0.193 | 0.080 | 0 | False |
| anchor | 5 | 3 | pooled | 5.270 | 0.237 | 0.120 | 0 | True |
| anchor | 5 | 3 | pooled_own | 5.270 | 0.207 | 0.080 | 0 | True |
| anchor | 5 | 3 | random | 5.270 | 0.100 | 0.040 | 0 | False |
| anchor | 5 | 5 | observed_mean | 6.604 | 0.313 | 0.180 | 0 | True |
| anchor | 5 | 5 | own | 6.604 | 0.260 | 0.120 | 0 | False |
| anchor | 5 | 5 | pooled | 6.604 | 0.340 | 0.180 | 0 | True |
| anchor | 5 | 5 | pooled_own | 6.604 | 0.267 | 0.120 | 0 | True |
| anchor | 5 | 5 | random | 6.604 | 0.127 | 0.060 | 0 | False |
| anchor | 10 | 1 | observed_mean | 7.240 | 0.247 | 0.140 | 0 | True |
| anchor | 10 | 1 | own | 7.240 | 0.213 | 0.120 | 0 | False |
| anchor | 10 | 1 | pooled | 7.240 | 0.227 | 0.140 | 0 | True |
| anchor | 10 | 1 | pooled_own | 7.240 | 0.227 | 0.140 | 0 | True |
| anchor | 10 | 1 | random | 7.240 | 0.167 | 0.140 | 0 | False |
| anchor | 10 | 3 | observed_mean | 8.573 | 0.383 | 0.240 | 0 | True |
| anchor | 10 | 3 | own | 8.573 | 0.330 | 0.120 | 0 | False |
| anchor | 10 | 3 | pooled | 8.573 | 0.363 | 0.220 | 0 | True |
| anchor | 10 | 3 | pooled_own | 8.573 | 0.367 | 0.160 | 0 | True |
| anchor | 10 | 3 | random | 8.573 | 0.170 | 0.140 | 0 | False |
| anchor | 10 | 5 | observed_mean | 9.907 | 0.453 | 0.280 | 0 | True |
| anchor | 10 | 5 | own | 9.907 | 0.400 | 0.160 | 0 | False |
| anchor | 10 | 5 | pooled | 9.907 | 0.440 | 0.260 | 0 | True |
| anchor | 10 | 5 | pooled_own | 9.907 | 0.413 | 0.160 | 0 | True |
| anchor | 10 | 5 | random | 9.907 | 0.197 | 0.140 | 0 | False |
| anchor | 15 | 1 | observed_mean | 10.431 | 0.303 | 0.100 | 0 | True |
| anchor | 15 | 1 | own | 10.431 | 0.277 | 0.120 | 0 | False |
| anchor | 15 | 1 | pooled | 10.431 | 0.340 | 0.120 | 0 | True |
| anchor | 15 | 1 | pooled_own | 10.431 | 0.297 | 0.120 | 0 | True |
| anchor | 15 | 1 | random | 10.431 | 0.213 | 0.120 | 0 | False |
| anchor | 15 | 3 | observed_mean | 11.765 | 0.443 | 0.220 | 0 | True |
| anchor | 15 | 3 | own | 11.765 | 0.393 | 0.200 | 0 | False |
| anchor | 15 | 3 | pooled | 11.765 | 0.463 | 0.160 | 0 | True |
| anchor | 15 | 3 | pooled_own | 11.765 | 0.427 | 0.220 | 0 | True |
| anchor | 15 | 3 | random | 11.765 | 0.237 | 0.120 | 0 | False |
| anchor | 15 | 5 | observed_mean | 13.098 | 0.537 | 0.340 | 0 | True |
| anchor | 15 | 5 | own | 13.098 | 0.490 | 0.300 | 0 | False |
| anchor | 15 | 5 | pooled | 13.098 | 0.577 | 0.260 | 1 | True |
| anchor | 15 | 5 | pooled_own | 13.098 | 0.497 | 0.280 | 0 | True |
| anchor | 15 | 5 | random | 13.098 | 0.270 | 0.160 | 0 | False |
| anchor | 30 | 1 | observed_mean | 20.600 | 0.583 | 0.380 | 0 | True |
| anchor | 30 | 1 | own | 20.600 | 0.500 | 0.340 | 0 | False |
| anchor | 30 | 1 | pooled | 20.600 | 0.510 | 0.340 | 0 | True |
| anchor | 30 | 1 | pooled_own | 20.600 | 0.500 | 0.360 | 0 | False |
| anchor | 30 | 1 | random | 20.600 | 0.377 | 0.340 | 0 | False |
| anchor | 30 | 3 | observed_mean | 21.933 | 0.713 | 0.560 | 0 | True |
| anchor | 30 | 3 | own | 21.933 | 0.633 | 0.400 | 1 | False |
| anchor | 30 | 3 | pooled | 21.933 | 0.677 | 0.420 | 1 | True |
| anchor | 30 | 3 | pooled_own | 21.933 | 0.677 | 0.500 | 1 | True |
| anchor | 30 | 3 | random | 21.933 | 0.400 | 0.360 | 0 | False |
| anchor | 30 | 5 | observed_mean | 23.267 | 0.773 | 0.640 | 0 | True |
| anchor | 30 | 5 | own | 23.267 | 0.713 | 0.540 | 1 | False |
| anchor | 30 | 5 | pooled | 23.267 | 0.750 | 0.460 | 1 | True |
| anchor | 30 | 5 | pooled_own | 23.267 | 0.743 | 0.560 | 1 | True |
| anchor | 30 | 5 | random | 23.267 | 0.417 | 0.380 | 0 | False |
| disjoint | 5 | 1 | observed_mean | 4.032 | 0.160 | 0.100 | 0 | True |
| disjoint | 5 | 1 | own | 4.032 | 0.113 | 0.080 | 0 | False |
| disjoint | 5 | 1 | pooled | 4.032 | 0.137 | 0.060 | 0 | True |
| disjoint | 5 | 1 | pooled_own | 4.032 | 0.117 | 0.060 | 0 | True |
| disjoint | 5 | 1 | random | 4.032 | 0.093 | 0.060 | 0 | False |
| disjoint | 5 | 3 | observed_mean | 5.365 | 0.253 | 0.120 | 0 | True |
| disjoint | 5 | 3 | own | 5.365 | 0.160 | 0.080 | 0 | False |
| disjoint | 5 | 3 | pooled | 5.365 | 0.293 | 0.140 | 0 | True |
| disjoint | 5 | 3 | pooled_own | 5.365 | 0.177 | 0.080 | 0 | True |
| disjoint | 5 | 3 | random | 5.365 | 0.127 | 0.080 | 0 | False |
| disjoint | 5 | 5 | observed_mean | 6.698 | 0.367 | 0.200 | 0 | True |
| disjoint | 5 | 5 | own | 6.698 | 0.250 | 0.120 | 0 | False |
| disjoint | 5 | 5 | pooled | 6.698 | 0.387 | 0.240 | 0 | True |
| disjoint | 5 | 5 | pooled_own | 6.698 | 0.303 | 0.160 | 0 | True |
| disjoint | 5 | 5 | random | 6.698 | 0.150 | 0.100 | 0 | False |
| disjoint | 10 | 1 | observed_mean | 7.347 | 0.253 | 0.120 | 0 | True |
| disjoint | 10 | 1 | own | 7.347 | 0.230 | 0.060 | 0 | False |
| disjoint | 10 | 1 | pooled | 7.347 | 0.293 | 0.060 | 0 | True |
| disjoint | 10 | 1 | pooled_own | 7.347 | 0.237 | 0.080 | 0 | True |
| disjoint | 10 | 1 | random | 7.347 | 0.183 | 0.080 | 0 | False |
| disjoint | 10 | 3 | observed_mean | 8.681 | 0.390 | 0.180 | 0 | True |
| disjoint | 10 | 3 | own | 8.681 | 0.350 | 0.180 | 0 | False |
| disjoint | 10 | 3 | pooled | 8.681 | 0.407 | 0.100 | 0 | True |
| disjoint | 10 | 3 | pooled_own | 8.681 | 0.387 | 0.200 | 0 | True |
| disjoint | 10 | 3 | random | 8.681 | 0.210 | 0.100 | 0 | False |
| disjoint | 10 | 5 | observed_mean | 10.014 | 0.473 | 0.220 | 0 | True |
| disjoint | 10 | 5 | own | 10.014 | 0.417 | 0.220 | 0 | False |
| disjoint | 10 | 5 | pooled | 10.014 | 0.537 | 0.180 | 0 | True |
| disjoint | 10 | 5 | pooled_own | 10.014 | 0.457 | 0.240 | 0 | True |
| disjoint | 10 | 5 | random | 10.014 | 0.223 | 0.100 | 0 | False |
| disjoint | 15 | 1 | observed_mean | 10.826 | 0.377 | 0.240 | 0 | True |
| disjoint | 15 | 1 | own | 10.826 | 0.313 | 0.240 | 0 | False |
| disjoint | 15 | 1 | pooled | 10.826 | 0.383 | 0.200 | 0 | True |
| disjoint | 15 | 1 | pooled_own | 10.826 | 0.303 | 0.240 | 0 | False |
| disjoint | 15 | 1 | random | 10.826 | 0.243 | 0.180 | 0 | False |
| disjoint | 15 | 3 | observed_mean | 12.159 | 0.577 | 0.360 | 0 | True |
| disjoint | 15 | 3 | own | 12.159 | 0.430 | 0.260 | 0 | False |
| disjoint | 15 | 3 | pooled | 12.159 | 0.503 | 0.240 | 0 | True |
| disjoint | 15 | 3 | pooled_own | 12.159 | 0.470 | 0.280 | 0 | True |
| disjoint | 15 | 3 | random | 12.159 | 0.283 | 0.180 | 0 | False |
| disjoint | 15 | 5 | observed_mean | 13.492 | 0.677 | 0.400 | 0 | True |
| disjoint | 15 | 5 | own | 13.492 | 0.517 | 0.340 | 0 | False |
| disjoint | 15 | 5 | pooled | 13.492 | 0.663 | 0.280 | 1 | True |
| disjoint | 15 | 5 | pooled_own | 13.492 | 0.583 | 0.400 | 0 | True |
| disjoint | 15 | 5 | random | 13.492 | 0.310 | 0.220 | 0 | False |
| independent | 5 | 1 | observed_mean | 4.003 | 0.140 | 0.100 | 0 | True |
| independent | 5 | 1 | own | 4.003 | 0.107 | 0.020 | 0 | False |
| independent | 5 | 1 | pooled | 4.003 | 0.103 | 0.020 | 0 | False |
| independent | 5 | 1 | pooled_own | 4.003 | 0.107 | 0.020 | 0 | False |
| independent | 5 | 1 | random | 4.003 | 0.077 | 0.040 | 0 | False |
| independent | 5 | 3 | observed_mean | 5.336 | 0.240 | 0.140 | 0 | True |
| independent | 5 | 3 | own | 5.336 | 0.150 | 0.060 | 0 | False |
| independent | 5 | 3 | pooled | 5.336 | 0.207 | 0.120 | 0 | True |
| independent | 5 | 3 | pooled_own | 5.336 | 0.163 | 0.100 | 0 | True |
| independent | 5 | 3 | random | 5.336 | 0.110 | 0.040 | 0 | False |
| independent | 5 | 5 | observed_mean | 6.670 | 0.320 | 0.200 | 0 | True |
| independent | 5 | 5 | own | 6.670 | 0.217 | 0.120 | 0 | False |
| independent | 5 | 5 | pooled | 6.670 | 0.303 | 0.200 | 0 | True |
| independent | 5 | 5 | pooled_own | 6.670 | 0.253 | 0.180 | 0 | True |
| independent | 5 | 5 | random | 6.670 | 0.127 | 0.040 | 0 | False |
| independent | 10 | 1 | observed_mean | 7.323 | 0.313 | 0.160 | 0 | True |
| independent | 10 | 1 | own | 7.323 | 0.207 | 0.100 | 0 | False |
| independent | 10 | 1 | pooled | 7.323 | 0.247 | 0.120 | 0 | True |
| independent | 10 | 1 | pooled_own | 7.323 | 0.210 | 0.100 | 0 | True |
| independent | 10 | 1 | random | 7.323 | 0.183 | 0.120 | 0 | False |
| independent | 10 | 3 | observed_mean | 8.656 | 0.460 | 0.220 | 0 | True |
| independent | 10 | 3 | own | 8.656 | 0.310 | 0.120 | 0 | False |
| independent | 10 | 3 | pooled | 8.656 | 0.407 | 0.160 | 0 | True |
| independent | 10 | 3 | pooled_own | 8.656 | 0.343 | 0.140 | 0 | True |
| independent | 10 | 3 | random | 8.656 | 0.213 | 0.140 | 0 | False |
| independent | 10 | 5 | observed_mean | 9.989 | 0.543 | 0.260 | 0 | True |
| independent | 10 | 5 | own | 9.989 | 0.383 | 0.200 | 0 | False |
| independent | 10 | 5 | pooled | 9.989 | 0.557 | 0.260 | 0 | True |
| independent | 10 | 5 | pooled_own | 9.989 | 0.430 | 0.220 | 0 | True |
| independent | 10 | 5 | random | 9.989 | 0.227 | 0.140 | 0 | False |
| independent | 15 | 1 | observed_mean | 10.684 | 0.333 | 0.260 | 0 | True |
| independent | 15 | 1 | own | 10.684 | 0.260 | 0.180 | 0 | False |
| independent | 15 | 1 | pooled | 10.684 | 0.297 | 0.200 | 0 | True |
| independent | 15 | 1 | pooled_own | 10.684 | 0.280 | 0.180 | 0 | True |
| independent | 15 | 1 | random | 10.684 | 0.213 | 0.160 | 0 | False |
| independent | 15 | 3 | observed_mean | 12.018 | 0.493 | 0.380 | 0 | True |
| independent | 15 | 3 | own | 12.018 | 0.383 | 0.220 | 0 | False |
| independent | 15 | 3 | pooled | 12.018 | 0.470 | 0.260 | 0 | True |
| independent | 15 | 3 | pooled_own | 12.018 | 0.413 | 0.240 | 0 | True |
| independent | 15 | 3 | random | 12.018 | 0.230 | 0.160 | 0 | False |
| independent | 15 | 5 | observed_mean | 13.351 | 0.603 | 0.400 | 0 | True |
| independent | 15 | 5 | own | 13.351 | 0.457 | 0.300 | 0 | False |
| independent | 15 | 5 | pooled | 13.351 | 0.627 | 0.400 | 0 | True |
| independent | 15 | 5 | pooled_own | 13.351 | 0.500 | 0.320 | 0 | True |
| independent | 15 | 5 | random | 13.351 | 0.253 | 0.200 | 0 | False |
| independent | 30 | 1 | observed_mean | 20.686 | 0.623 | 0.400 | 0 | True |
| independent | 30 | 1 | own | 20.686 | 0.510 | 0.380 | 0 | False |
| independent | 30 | 1 | pooled | 20.686 | 0.550 | 0.340 | 0 | True |
| independent | 30 | 1 | pooled_own | 20.686 | 0.520 | 0.380 | 0 | True |
| independent | 30 | 1 | random | 20.686 | 0.410 | 0.320 | 0 | False |
| independent | 30 | 3 | observed_mean | 22.019 | 0.757 | 0.500 | 0 | True |
| independent | 30 | 3 | own | 22.019 | 0.617 | 0.460 | 1 | False |
| independent | 30 | 3 | pooled | 22.019 | 0.733 | 0.340 | 2 | True |
| independent | 30 | 3 | pooled_own | 22.019 | 0.633 | 0.460 | 1 | True |
| independent | 30 | 3 | random | 22.019 | 0.443 | 0.340 | 0 | False |
| independent | 30 | 5 | observed_mean | 23.353 | 0.827 | 0.560 | 3 | True |
| independent | 30 | 5 | own | 23.353 | 0.693 | 0.540 | 1 | False |
| independent | 30 | 5 | pooled | 23.353 | 0.803 | 0.400 | 4 | True |
| independent | 30 | 5 | pooled_own | 23.353 | 0.757 | 0.580 | 1 | True |
| independent | 30 | 5 | random | 23.353 | 0.463 | 0.340 | 0 | False |

### Every city

| design | n | b | model | city | share | fleet_cost_pct |
|---|---|---|---|---|---|---|
| independent | 5 | 1 | own | metrla | 0.100 | 4.003 |
| independent | 5 | 1 | own | pems04 | 0.180 | 4.003 |
| independent | 5 | 1 | own | chengdu | 0.080 | 4.003 |
| independent | 5 | 1 | own | shenzhen | 0.020 | 4.003 |
| independent | 5 | 1 | own | expytky | 0.160 | 4.003 |
| independent | 5 | 1 | own | pemsbay | 0.100 | 4.003 |
| independent | 5 | 3 | own | metrla | 0.120 | 5.336 |
| independent | 5 | 3 | own | pems04 | 0.260 | 5.336 |
| independent | 5 | 3 | own | chengdu | 0.120 | 5.336 |
| independent | 5 | 3 | own | shenzhen | 0.060 | 5.336 |
| independent | 5 | 3 | own | expytky | 0.220 | 5.336 |
| independent | 5 | 3 | own | pemsbay | 0.120 | 5.336 |
| independent | 5 | 5 | own | metrla | 0.240 | 6.670 |
| independent | 5 | 5 | own | pems04 | 0.400 | 6.670 |
| independent | 5 | 5 | own | chengdu | 0.120 | 6.670 |
| independent | 5 | 5 | own | shenzhen | 0.140 | 6.670 |
| independent | 5 | 5 | own | expytky | 0.240 | 6.670 |
| independent | 5 | 5 | own | pemsbay | 0.160 | 6.670 |
| independent | 5 | 1 | pooled | metrla | 0.160 | 4.003 |
| independent | 5 | 1 | pooled | pems04 | 0.120 | 4.003 |
| independent | 5 | 1 | pooled | chengdu | 0.060 | 4.003 |
| independent | 5 | 1 | pooled | shenzhen | 0.020 | 4.003 |
| independent | 5 | 1 | pooled | expytky | 0.160 | 4.003 |
| independent | 5 | 1 | pooled | pemsbay | 0.100 | 4.003 |
| independent | 5 | 3 | pooled | metrla | 0.280 | 5.336 |
| independent | 5 | 3 | pooled | pems04 | 0.240 | 5.336 |
| independent | 5 | 3 | pooled | chengdu | 0.140 | 5.336 |
| independent | 5 | 3 | pooled | shenzhen | 0.120 | 5.336 |
| independent | 5 | 3 | pooled | expytky | 0.300 | 5.336 |
| independent | 5 | 3 | pooled | pemsbay | 0.160 | 5.336 |
| independent | 5 | 5 | pooled | metrla | 0.360 | 6.670 |
| independent | 5 | 5 | pooled | pems04 | 0.360 | 6.670 |
| independent | 5 | 5 | pooled | chengdu | 0.240 | 6.670 |
| independent | 5 | 5 | pooled | shenzhen | 0.260 | 6.670 |
| independent | 5 | 5 | pooled | expytky | 0.400 | 6.670 |
| independent | 5 | 5 | pooled | pemsbay | 0.200 | 6.670 |
| independent | 5 | 1 | pooled_own | metrla | 0.080 | 4.003 |
| independent | 5 | 1 | pooled_own | pems04 | 0.200 | 4.003 |
| independent | 5 | 1 | pooled_own | chengdu | 0.100 | 4.003 |
| independent | 5 | 1 | pooled_own | shenzhen | 0.020 | 4.003 |
| independent | 5 | 1 | pooled_own | expytky | 0.140 | 4.003 |
| independent | 5 | 1 | pooled_own | pemsbay | 0.100 | 4.003 |
| independent | 5 | 3 | pooled_own | metrla | 0.160 | 5.336 |
| independent | 5 | 3 | pooled_own | pems04 | 0.300 | 5.336 |
| independent | 5 | 3 | pooled_own | chengdu | 0.100 | 5.336 |
| independent | 5 | 3 | pooled_own | shenzhen | 0.120 | 5.336 |
| independent | 5 | 3 | pooled_own | expytky | 0.200 | 5.336 |
| independent | 5 | 3 | pooled_own | pemsbay | 0.100 | 5.336 |
| independent | 5 | 5 | pooled_own | metrla | 0.260 | 6.670 |
| independent | 5 | 5 | pooled_own | pems04 | 0.460 | 6.670 |
| independent | 5 | 5 | pooled_own | chengdu | 0.200 | 6.670 |
| independent | 5 | 5 | pooled_own | shenzhen | 0.180 | 6.670 |
| independent | 5 | 5 | pooled_own | expytky | 0.240 | 6.670 |
| independent | 5 | 5 | pooled_own | pemsbay | 0.180 | 6.670 |
| independent | 5 | 1 | observed_mean | metrla | 0.140 | 4.003 |
| independent | 5 | 1 | observed_mean | pems04 | 0.140 | 4.003 |
| independent | 5 | 1 | observed_mean | chengdu | 0.100 | 4.003 |
| independent | 5 | 1 | observed_mean | shenzhen | 0.100 | 4.003 |
| independent | 5 | 1 | observed_mean | expytky | 0.180 | 4.003 |
| independent | 5 | 1 | observed_mean | pemsbay | 0.180 | 4.003 |
| independent | 5 | 3 | observed_mean | metrla | 0.280 | 5.336 |
| independent | 5 | 3 | observed_mean | pems04 | 0.240 | 5.336 |
| independent | 5 | 3 | observed_mean | chengdu | 0.140 | 5.336 |
| independent | 5 | 3 | observed_mean | shenzhen | 0.220 | 5.336 |
| independent | 5 | 3 | observed_mean | expytky | 0.300 | 5.336 |
| independent | 5 | 3 | observed_mean | pemsbay | 0.260 | 5.336 |
| independent | 5 | 5 | observed_mean | metrla | 0.380 | 6.670 |
| independent | 5 | 5 | observed_mean | pems04 | 0.360 | 6.670 |
| independent | 5 | 5 | observed_mean | chengdu | 0.200 | 6.670 |
| independent | 5 | 5 | observed_mean | shenzhen | 0.280 | 6.670 |
| independent | 5 | 5 | observed_mean | expytky | 0.420 | 6.670 |
| independent | 5 | 5 | observed_mean | pemsbay | 0.280 | 6.670 |
| independent | 5 | 1 | random | metrla | 0.080 | 4.003 |
| independent | 5 | 1 | random | pems04 | 0.060 | 4.003 |
| independent | 5 | 1 | random | chengdu | 0.060 | 4.003 |
| independent | 5 | 1 | random | shenzhen | 0.040 | 4.003 |
| independent | 5 | 1 | random | expytky | 0.100 | 4.003 |
| independent | 5 | 1 | random | pemsbay | 0.120 | 4.003 |
| independent | 5 | 3 | random | metrla | 0.080 | 5.336 |
| independent | 5 | 3 | random | pems04 | 0.120 | 5.336 |
| independent | 5 | 3 | random | chengdu | 0.100 | 5.336 |
| independent | 5 | 3 | random | shenzhen | 0.040 | 5.336 |
| independent | 5 | 3 | random | expytky | 0.160 | 5.336 |
| independent | 5 | 3 | random | pemsbay | 0.160 | 5.336 |
| independent | 5 | 5 | random | metrla | 0.120 | 6.670 |
| independent | 5 | 5 | random | pems04 | 0.140 | 6.670 |
| independent | 5 | 5 | random | chengdu | 0.100 | 6.670 |
| independent | 5 | 5 | random | shenzhen | 0.040 | 6.670 |
| independent | 5 | 5 | random | expytky | 0.180 | 6.670 |
| independent | 5 | 5 | random | pemsbay | 0.180 | 6.670 |
| independent | 10 | 1 | own | metrla | 0.200 | 7.323 |
| independent | 10 | 1 | own | pems04 | 0.380 | 7.323 |
| independent | 10 | 1 | own | chengdu | 0.120 | 7.323 |
| independent | 10 | 1 | own | shenzhen | 0.100 | 7.323 |
| independent | 10 | 1 | own | expytky | 0.320 | 7.323 |
| independent | 10 | 1 | own | pemsbay | 0.120 | 7.323 |
| independent | 10 | 3 | own | metrla | 0.300 | 8.656 |
| independent | 10 | 3 | own | pems04 | 0.660 | 8.656 |
| independent | 10 | 3 | own | chengdu | 0.220 | 8.656 |
| independent | 10 | 3 | own | shenzhen | 0.160 | 8.656 |
| independent | 10 | 3 | own | expytky | 0.400 | 8.656 |
| independent | 10 | 3 | own | pemsbay | 0.120 | 8.656 |
| independent | 10 | 5 | own | metrla | 0.380 | 9.989 |
| independent | 10 | 5 | own | pems04 | 0.760 | 9.989 |
| independent | 10 | 5 | own | chengdu | 0.260 | 9.989 |
| independent | 10 | 5 | own | shenzhen | 0.300 | 9.989 |
| independent | 10 | 5 | own | expytky | 0.400 | 9.989 |
| independent | 10 | 5 | own | pemsbay | 0.200 | 9.989 |
| independent | 10 | 1 | pooled | metrla | 0.320 | 7.323 |
| independent | 10 | 1 | pooled | pems04 | 0.400 | 7.323 |
| independent | 10 | 1 | pooled | chengdu | 0.120 | 7.323 |
| independent | 10 | 1 | pooled | shenzhen | 0.180 | 7.323 |
| independent | 10 | 1 | pooled | expytky | 0.320 | 7.323 |
| independent | 10 | 1 | pooled | pemsbay | 0.140 | 7.323 |
| independent | 10 | 3 | pooled | metrla | 0.560 | 8.656 |
| independent | 10 | 3 | pooled | pems04 | 0.640 | 8.656 |
| independent | 10 | 3 | pooled | chengdu | 0.160 | 8.656 |
| independent | 10 | 3 | pooled | shenzhen | 0.340 | 8.656 |
| independent | 10 | 3 | pooled | expytky | 0.460 | 8.656 |
| independent | 10 | 3 | pooled | pemsbay | 0.280 | 8.656 |
| independent | 10 | 5 | pooled | metrla | 0.780 | 9.989 |
| independent | 10 | 5 | pooled | pems04 | 0.740 | 9.989 |
| independent | 10 | 5 | pooled | chengdu | 0.260 | 9.989 |
| independent | 10 | 5 | pooled | shenzhen | 0.500 | 9.989 |
| independent | 10 | 5 | pooled | expytky | 0.600 | 9.989 |
| independent | 10 | 5 | pooled | pemsbay | 0.460 | 9.989 |
| independent | 10 | 1 | pooled_own | metrla | 0.220 | 7.323 |
| independent | 10 | 1 | pooled_own | pems04 | 0.400 | 7.323 |
| independent | 10 | 1 | pooled_own | chengdu | 0.100 | 7.323 |
| independent | 10 | 1 | pooled_own | shenzhen | 0.100 | 7.323 |
| independent | 10 | 1 | pooled_own | expytky | 0.320 | 7.323 |
| independent | 10 | 1 | pooled_own | pemsbay | 0.120 | 7.323 |
| independent | 10 | 3 | pooled_own | metrla | 0.340 | 8.656 |
| independent | 10 | 3 | pooled_own | pems04 | 0.700 | 8.656 |
| independent | 10 | 3 | pooled_own | chengdu | 0.220 | 8.656 |
| independent | 10 | 3 | pooled_own | shenzhen | 0.240 | 8.656 |
| independent | 10 | 3 | pooled_own | expytky | 0.420 | 8.656 |
| independent | 10 | 3 | pooled_own | pemsbay | 0.140 | 8.656 |
| independent | 10 | 5 | pooled_own | metrla | 0.460 | 9.989 |
| independent | 10 | 5 | pooled_own | pems04 | 0.820 | 9.989 |
| independent | 10 | 5 | pooled_own | chengdu | 0.320 | 9.989 |
| independent | 10 | 5 | pooled_own | shenzhen | 0.300 | 9.989 |
| independent | 10 | 5 | pooled_own | expytky | 0.460 | 9.989 |
| independent | 10 | 5 | pooled_own | pemsbay | 0.220 | 9.989 |
| independent | 10 | 1 | observed_mean | metrla | 0.420 | 7.323 |
| independent | 10 | 1 | observed_mean | pems04 | 0.380 | 7.323 |
| independent | 10 | 1 | observed_mean | chengdu | 0.160 | 7.323 |
| independent | 10 | 1 | observed_mean | shenzhen | 0.280 | 7.323 |
| independent | 10 | 1 | observed_mean | expytky | 0.380 | 7.323 |
| independent | 10 | 1 | observed_mean | pemsbay | 0.260 | 7.323 |
| independent | 10 | 3 | observed_mean | metrla | 0.640 | 8.656 |
| independent | 10 | 3 | observed_mean | pems04 | 0.520 | 8.656 |
| independent | 10 | 3 | observed_mean | chengdu | 0.220 | 8.656 |
| independent | 10 | 3 | observed_mean | shenzhen | 0.420 | 8.656 |
| independent | 10 | 3 | observed_mean | expytky | 0.580 | 8.656 |
| independent | 10 | 3 | observed_mean | pemsbay | 0.380 | 8.656 |
| independent | 10 | 5 | observed_mean | metrla | 0.740 | 9.989 |
| independent | 10 | 5 | observed_mean | pems04 | 0.580 | 9.989 |
| independent | 10 | 5 | observed_mean | chengdu | 0.260 | 9.989 |
| independent | 10 | 5 | observed_mean | shenzhen | 0.520 | 9.989 |
| independent | 10 | 5 | observed_mean | expytky | 0.720 | 9.989 |
| independent | 10 | 5 | observed_mean | pemsbay | 0.440 | 9.989 |
| independent | 10 | 1 | random | metrla | 0.180 | 7.323 |
| independent | 10 | 1 | random | pems04 | 0.280 | 7.323 |
| independent | 10 | 1 | random | chengdu | 0.160 | 7.323 |
| independent | 10 | 1 | random | shenzhen | 0.120 | 7.323 |
| independent | 10 | 1 | random | expytky | 0.240 | 7.323 |
| independent | 10 | 1 | random | pemsbay | 0.120 | 7.323 |
| independent | 10 | 3 | random | metrla | 0.240 | 8.656 |
| independent | 10 | 3 | random | pems04 | 0.340 | 8.656 |
| independent | 10 | 3 | random | chengdu | 0.160 | 8.656 |
| independent | 10 | 3 | random | shenzhen | 0.140 | 8.656 |
| independent | 10 | 3 | random | expytky | 0.260 | 8.656 |
| independent | 10 | 3 | random | pemsbay | 0.140 | 8.656 |
| independent | 10 | 5 | random | metrla | 0.240 | 9.989 |
| independent | 10 | 5 | random | pems04 | 0.360 | 9.989 |
| independent | 10 | 5 | random | chengdu | 0.160 | 9.989 |
| independent | 10 | 5 | random | shenzhen | 0.140 | 9.989 |
| independent | 10 | 5 | random | expytky | 0.280 | 9.989 |
| independent | 10 | 5 | random | pemsbay | 0.180 | 9.989 |
| independent | 15 | 1 | own | metrla | 0.320 | 10.684 |
| independent | 15 | 1 | own | pems04 | 0.440 | 10.684 |
| independent | 15 | 1 | own | chengdu | 0.180 | 10.684 |
| independent | 15 | 1 | own | shenzhen | 0.240 | 10.684 |
| independent | 15 | 1 | own | expytky | 0.200 | 10.684 |
| independent | 15 | 1 | own | pemsbay | 0.180 | 10.684 |
| independent | 15 | 3 | own | metrla | 0.460 | 12.018 |
| independent | 15 | 3 | own | pems04 | 0.760 | 12.018 |
| independent | 15 | 3 | own | chengdu | 0.280 | 12.018 |
| independent | 15 | 3 | own | shenzhen | 0.300 | 12.018 |
| independent | 15 | 3 | own | expytky | 0.280 | 12.018 |
| independent | 15 | 3 | own | pemsbay | 0.220 | 12.018 |
| independent | 15 | 5 | own | metrla | 0.480 | 13.351 |
| independent | 15 | 5 | own | pems04 | 0.780 | 13.351 |
| independent | 15 | 5 | own | chengdu | 0.340 | 13.351 |
| independent | 15 | 5 | own | shenzhen | 0.420 | 13.351 |
| independent | 15 | 5 | own | expytky | 0.420 | 13.351 |
| independent | 15 | 5 | own | pemsbay | 0.300 | 13.351 |
| independent | 15 | 1 | pooled | metrla | 0.400 | 10.684 |
| independent | 15 | 1 | pooled | pems04 | 0.380 | 10.684 |
| independent | 15 | 1 | pooled | chengdu | 0.200 | 10.684 |
| independent | 15 | 1 | pooled | shenzhen | 0.320 | 10.684 |
| independent | 15 | 1 | pooled | expytky | 0.220 | 10.684 |
| independent | 15 | 1 | pooled | pemsbay | 0.260 | 10.684 |
| independent | 15 | 3 | pooled | metrla | 0.580 | 12.018 |
| independent | 15 | 3 | pooled | pems04 | 0.680 | 12.018 |
| independent | 15 | 3 | pooled | chengdu | 0.260 | 12.018 |
| independent | 15 | 3 | pooled | shenzhen | 0.520 | 12.018 |
| independent | 15 | 3 | pooled | expytky | 0.380 | 12.018 |
| independent | 15 | 3 | pooled | pemsbay | 0.400 | 12.018 |
| independent | 15 | 5 | pooled | metrla | 0.740 | 13.351 |
| independent | 15 | 5 | pooled | pems04 | 0.880 | 13.351 |
| independent | 15 | 5 | pooled | chengdu | 0.400 | 13.351 |
| independent | 15 | 5 | pooled | shenzhen | 0.640 | 13.351 |
| independent | 15 | 5 | pooled | expytky | 0.540 | 13.351 |
| independent | 15 | 5 | pooled | pemsbay | 0.560 | 13.351 |
| independent | 15 | 1 | pooled_own | metrla | 0.340 | 10.684 |
| independent | 15 | 1 | pooled_own | pems04 | 0.500 | 10.684 |
| independent | 15 | 1 | pooled_own | chengdu | 0.180 | 10.684 |
| independent | 15 | 1 | pooled_own | shenzhen | 0.260 | 10.684 |
| independent | 15 | 1 | pooled_own | expytky | 0.220 | 10.684 |
| independent | 15 | 1 | pooled_own | pemsbay | 0.180 | 10.684 |
| independent | 15 | 3 | pooled_own | metrla | 0.440 | 12.018 |
| independent | 15 | 3 | pooled_own | pems04 | 0.820 | 12.018 |
| independent | 15 | 3 | pooled_own | chengdu | 0.320 | 12.018 |
| independent | 15 | 3 | pooled_own | shenzhen | 0.380 | 12.018 |
| independent | 15 | 3 | pooled_own | expytky | 0.280 | 12.018 |
| independent | 15 | 3 | pooled_own | pemsbay | 0.240 | 12.018 |
| independent | 15 | 5 | pooled_own | metrla | 0.560 | 13.351 |
| independent | 15 | 5 | pooled_own | pems04 | 0.840 | 13.351 |
| independent | 15 | 5 | pooled_own | chengdu | 0.420 | 13.351 |
| independent | 15 | 5 | pooled_own | shenzhen | 0.460 | 13.351 |
| independent | 15 | 5 | pooled_own | expytky | 0.400 | 13.351 |
| independent | 15 | 5 | pooled_own | pemsbay | 0.320 | 13.351 |
| independent | 15 | 1 | observed_mean | metrla | 0.400 | 10.684 |
| independent | 15 | 1 | observed_mean | pems04 | 0.400 | 10.684 |
| independent | 15 | 1 | observed_mean | chengdu | 0.260 | 10.684 |
| independent | 15 | 1 | observed_mean | shenzhen | 0.380 | 10.684 |
| independent | 15 | 1 | observed_mean | expytky | 0.260 | 10.684 |
| independent | 15 | 1 | observed_mean | pemsbay | 0.300 | 10.684 |
| independent | 15 | 3 | observed_mean | metrla | 0.520 | 12.018 |
| independent | 15 | 3 | observed_mean | pems04 | 0.540 | 12.018 |
| independent | 15 | 3 | observed_mean | chengdu | 0.380 | 12.018 |
| independent | 15 | 3 | observed_mean | shenzhen | 0.580 | 12.018 |
| independent | 15 | 3 | observed_mean | expytky | 0.460 | 12.018 |
| independent | 15 | 3 | observed_mean | pemsbay | 0.480 | 12.018 |
| independent | 15 | 5 | observed_mean | metrla | 0.660 | 13.351 |
| independent | 15 | 5 | observed_mean | pems04 | 0.700 | 13.351 |
| independent | 15 | 5 | observed_mean | chengdu | 0.400 | 13.351 |
| independent | 15 | 5 | observed_mean | shenzhen | 0.680 | 13.351 |
| independent | 15 | 5 | observed_mean | expytky | 0.600 | 13.351 |
| independent | 15 | 5 | observed_mean | pemsbay | 0.580 | 13.351 |
| independent | 15 | 1 | random | metrla | 0.240 | 10.684 |
| independent | 15 | 1 | random | pems04 | 0.280 | 10.684 |
| independent | 15 | 1 | random | chengdu | 0.160 | 10.684 |
| independent | 15 | 1 | random | shenzhen | 0.240 | 10.684 |
| independent | 15 | 1 | random | expytky | 0.160 | 10.684 |
| independent | 15 | 1 | random | pemsbay | 0.200 | 10.684 |
| independent | 15 | 3 | random | metrla | 0.260 | 12.018 |
| independent | 15 | 3 | random | pems04 | 0.280 | 12.018 |
| independent | 15 | 3 | random | chengdu | 0.160 | 12.018 |
| independent | 15 | 3 | random | shenzhen | 0.280 | 12.018 |
| independent | 15 | 3 | random | expytky | 0.200 | 12.018 |
| independent | 15 | 3 | random | pemsbay | 0.200 | 12.018 |
| independent | 15 | 5 | random | metrla | 0.300 | 13.351 |
| independent | 15 | 5 | random | pems04 | 0.300 | 13.351 |
| independent | 15 | 5 | random | chengdu | 0.200 | 13.351 |
| independent | 15 | 5 | random | shenzhen | 0.280 | 13.351 |
| independent | 15 | 5 | random | expytky | 0.240 | 13.351 |
| independent | 15 | 5 | random | pemsbay | 0.200 | 13.351 |
| independent | 30 | 1 | own | metrla | 0.580 | 20.686 |
| independent | 30 | 1 | own | pems04 | 0.760 | 20.686 |
| independent | 30 | 1 | own | chengdu | 0.380 | 20.686 |
| independent | 30 | 1 | own | shenzhen | 0.400 | 20.686 |
| independent | 30 | 1 | own | expytky | 0.420 | 20.686 |
| independent | 30 | 1 | own | pemsbay | 0.520 | 20.686 |
| independent | 30 | 3 | own | metrla | 0.760 | 22.019 |
| independent | 30 | 3 | own | pems04 | 0.920 | 22.019 |
| independent | 30 | 3 | own | chengdu | 0.460 | 22.019 |
| independent | 30 | 3 | own | shenzhen | 0.560 | 22.019 |
| independent | 30 | 3 | own | expytky | 0.480 | 22.019 |
| independent | 30 | 3 | own | pemsbay | 0.520 | 22.019 |
| independent | 30 | 5 | own | metrla | 0.780 | 23.353 |
| independent | 30 | 5 | own | pems04 | 1.000 | 23.353 |
| independent | 30 | 5 | own | chengdu | 0.560 | 23.353 |
| independent | 30 | 5 | own | shenzhen | 0.660 | 23.353 |
| independent | 30 | 5 | own | expytky | 0.540 | 23.353 |
| independent | 30 | 5 | own | pemsbay | 0.620 | 23.353 |
| independent | 30 | 1 | pooled | metrla | 0.600 | 20.686 |
| independent | 30 | 1 | pooled | pems04 | 0.820 | 20.686 |
| independent | 30 | 1 | pooled | chengdu | 0.340 | 20.686 |
| independent | 30 | 1 | pooled | shenzhen | 0.520 | 20.686 |
| independent | 30 | 1 | pooled | expytky | 0.420 | 20.686 |
| independent | 30 | 1 | pooled | pemsbay | 0.600 | 20.686 |
| independent | 30 | 3 | pooled | metrla | 0.900 | 22.019 |
| independent | 30 | 3 | pooled | pems04 | 0.920 | 22.019 |
| independent | 30 | 3 | pooled | chengdu | 0.340 | 22.019 |
| independent | 30 | 3 | pooled | shenzhen | 0.880 | 22.019 |
| independent | 30 | 3 | pooled | expytky | 0.520 | 22.019 |
| independent | 30 | 3 | pooled | pemsbay | 0.840 | 22.019 |
| independent | 30 | 5 | pooled | metrla | 0.980 | 23.353 |
| independent | 30 | 5 | pooled | pems04 | 0.980 | 23.353 |
| independent | 30 | 5 | pooled | chengdu | 0.400 | 23.353 |
| independent | 30 | 5 | pooled | shenzhen | 0.920 | 23.353 |
| independent | 30 | 5 | pooled | expytky | 0.600 | 23.353 |
| independent | 30 | 5 | pooled | pemsbay | 0.940 | 23.353 |
| independent | 30 | 1 | pooled_own | metrla | 0.560 | 20.686 |
| independent | 30 | 1 | pooled_own | pems04 | 0.800 | 20.686 |
| independent | 30 | 1 | pooled_own | chengdu | 0.380 | 20.686 |
| independent | 30 | 1 | pooled_own | shenzhen | 0.440 | 20.686 |
| independent | 30 | 1 | pooled_own | expytky | 0.420 | 20.686 |
| independent | 30 | 1 | pooled_own | pemsbay | 0.520 | 20.686 |
| independent | 30 | 3 | pooled_own | metrla | 0.760 | 22.019 |
| independent | 30 | 3 | pooled_own | pems04 | 0.920 | 22.019 |
| independent | 30 | 3 | pooled_own | chengdu | 0.460 | 22.019 |
| independent | 30 | 3 | pooled_own | shenzhen | 0.620 | 22.019 |
| independent | 30 | 3 | pooled_own | expytky | 0.480 | 22.019 |
| independent | 30 | 3 | pooled_own | pemsbay | 0.560 | 22.019 |
| independent | 30 | 5 | pooled_own | metrla | 0.880 | 23.353 |
| independent | 30 | 5 | pooled_own | pems04 | 1.000 | 23.353 |
| independent | 30 | 5 | pooled_own | chengdu | 0.640 | 23.353 |
| independent | 30 | 5 | pooled_own | shenzhen | 0.760 | 23.353 |
| independent | 30 | 5 | pooled_own | expytky | 0.580 | 23.353 |
| independent | 30 | 5 | pooled_own | pemsbay | 0.680 | 23.353 |
| independent | 30 | 1 | observed_mean | metrla | 0.700 | 20.686 |
| independent | 30 | 1 | observed_mean | pems04 | 0.780 | 20.686 |
| independent | 30 | 1 | observed_mean | chengdu | 0.400 | 20.686 |
| independent | 30 | 1 | observed_mean | shenzhen | 0.600 | 20.686 |
| independent | 30 | 1 | observed_mean | expytky | 0.520 | 20.686 |
| independent | 30 | 1 | observed_mean | pemsbay | 0.740 | 20.686 |
| independent | 30 | 3 | observed_mean | metrla | 0.860 | 22.019 |
| independent | 30 | 3 | observed_mean | pems04 | 0.860 | 22.019 |
| independent | 30 | 3 | observed_mean | chengdu | 0.500 | 22.019 |
| independent | 30 | 3 | observed_mean | shenzhen | 0.820 | 22.019 |
| independent | 30 | 3 | observed_mean | expytky | 0.720 | 22.019 |
| independent | 30 | 3 | observed_mean | pemsbay | 0.780 | 22.019 |
| independent | 30 | 5 | observed_mean | metrla | 0.900 | 23.353 |
| independent | 30 | 5 | observed_mean | pems04 | 0.940 | 23.353 |
| independent | 30 | 5 | observed_mean | chengdu | 0.560 | 23.353 |
| independent | 30 | 5 | observed_mean | shenzhen | 0.900 | 23.353 |
| independent | 30 | 5 | observed_mean | expytky | 0.800 | 23.353 |
| independent | 30 | 5 | observed_mean | pemsbay | 0.860 | 23.353 |
| independent | 30 | 1 | random | metrla | 0.400 | 20.686 |
| independent | 30 | 1 | random | pems04 | 0.480 | 20.686 |
| independent | 30 | 1 | random | chengdu | 0.340 | 20.686 |
| independent | 30 | 1 | random | shenzhen | 0.320 | 20.686 |
| independent | 30 | 1 | random | expytky | 0.400 | 20.686 |
| independent | 30 | 1 | random | pemsbay | 0.520 | 20.686 |
| independent | 30 | 3 | random | metrla | 0.400 | 22.019 |
| independent | 30 | 3 | random | pems04 | 0.500 | 22.019 |
| independent | 30 | 3 | random | chengdu | 0.340 | 22.019 |
| independent | 30 | 3 | random | shenzhen | 0.460 | 22.019 |
| independent | 30 | 3 | random | expytky | 0.420 | 22.019 |
| independent | 30 | 3 | random | pemsbay | 0.540 | 22.019 |
| independent | 30 | 5 | random | metrla | 0.420 | 23.353 |
| independent | 30 | 5 | random | pems04 | 0.540 | 23.353 |
| independent | 30 | 5 | random | chengdu | 0.340 | 23.353 |
| independent | 30 | 5 | random | shenzhen | 0.500 | 23.353 |
| independent | 30 | 5 | random | expytky | 0.420 | 23.353 |
| independent | 30 | 5 | random | pemsbay | 0.560 | 23.353 |
| disjoint | 5 | 1 | own | metrla | 0.160 | 4.032 |
| disjoint | 5 | 1 | own | pems04 | 0.120 | 4.032 |
| disjoint | 5 | 1 | own | chengdu | 0.100 | 4.032 |
| disjoint | 5 | 1 | own | shenzhen | 0.080 | 4.032 |
| disjoint | 5 | 1 | own | expytky | 0.140 | 4.032 |
| disjoint | 5 | 1 | own | pemsbay | 0.080 | 4.032 |
| disjoint | 5 | 3 | own | metrla | 0.200 | 5.365 |
| disjoint | 5 | 3 | own | pems04 | 0.180 | 5.365 |
| disjoint | 5 | 3 | own | chengdu | 0.200 | 5.365 |
| disjoint | 5 | 3 | own | shenzhen | 0.100 | 5.365 |
| disjoint | 5 | 3 | own | expytky | 0.200 | 5.365 |
| disjoint | 5 | 3 | own | pemsbay | 0.080 | 5.365 |
| disjoint | 5 | 5 | own | metrla | 0.280 | 6.698 |
| disjoint | 5 | 5 | own | pems04 | 0.360 | 6.698 |
| disjoint | 5 | 5 | own | chengdu | 0.280 | 6.698 |
| disjoint | 5 | 5 | own | shenzhen | 0.140 | 6.698 |
| disjoint | 5 | 5 | own | expytky | 0.320 | 6.698 |
| disjoint | 5 | 5 | own | pemsbay | 0.120 | 6.698 |
| disjoint | 5 | 1 | pooled | metrla | 0.180 | 4.032 |
| disjoint | 5 | 1 | pooled | pems04 | 0.220 | 4.032 |
| disjoint | 5 | 1 | pooled | chengdu | 0.060 | 4.032 |
| disjoint | 5 | 1 | pooled | shenzhen | 0.100 | 4.032 |
| disjoint | 5 | 1 | pooled | expytky | 0.160 | 4.032 |
| disjoint | 5 | 1 | pooled | pemsbay | 0.100 | 4.032 |
| disjoint | 5 | 3 | pooled | metrla | 0.360 | 5.365 |
| disjoint | 5 | 3 | pooled | pems04 | 0.500 | 5.365 |
| disjoint | 5 | 3 | pooled | chengdu | 0.140 | 5.365 |
| disjoint | 5 | 3 | pooled | shenzhen | 0.240 | 5.365 |
| disjoint | 5 | 3 | pooled | expytky | 0.360 | 5.365 |
| disjoint | 5 | 3 | pooled | pemsbay | 0.160 | 5.365 |
| disjoint | 5 | 5 | pooled | metrla | 0.420 | 6.698 |
| disjoint | 5 | 5 | pooled | pems04 | 0.600 | 6.698 |
| disjoint | 5 | 5 | pooled | chengdu | 0.240 | 6.698 |
| disjoint | 5 | 5 | pooled | shenzhen | 0.360 | 6.698 |
| disjoint | 5 | 5 | pooled | expytky | 0.440 | 6.698 |
| disjoint | 5 | 5 | pooled | pemsbay | 0.260 | 6.698 |
| disjoint | 5 | 1 | pooled_own | metrla | 0.160 | 4.032 |
| disjoint | 5 | 1 | pooled_own | pems04 | 0.160 | 4.032 |
| disjoint | 5 | 1 | pooled_own | chengdu | 0.100 | 4.032 |
| disjoint | 5 | 1 | pooled_own | shenzhen | 0.080 | 4.032 |
| disjoint | 5 | 1 | pooled_own | expytky | 0.140 | 4.032 |
| disjoint | 5 | 1 | pooled_own | pemsbay | 0.060 | 4.032 |
| disjoint | 5 | 3 | pooled_own | metrla | 0.200 | 5.365 |
| disjoint | 5 | 3 | pooled_own | pems04 | 0.300 | 5.365 |
| disjoint | 5 | 3 | pooled_own | chengdu | 0.180 | 5.365 |
| disjoint | 5 | 3 | pooled_own | shenzhen | 0.080 | 5.365 |
| disjoint | 5 | 3 | pooled_own | expytky | 0.200 | 5.365 |
| disjoint | 5 | 3 | pooled_own | pemsbay | 0.100 | 5.365 |
| disjoint | 5 | 5 | pooled_own | metrla | 0.320 | 6.698 |
| disjoint | 5 | 5 | pooled_own | pems04 | 0.480 | 6.698 |
| disjoint | 5 | 5 | pooled_own | chengdu | 0.240 | 6.698 |
| disjoint | 5 | 5 | pooled_own | shenzhen | 0.240 | 6.698 |
| disjoint | 5 | 5 | pooled_own | expytky | 0.380 | 6.698 |
| disjoint | 5 | 5 | pooled_own | pemsbay | 0.160 | 6.698 |
| disjoint | 5 | 1 | observed_mean | metrla | 0.220 | 4.032 |
| disjoint | 5 | 1 | observed_mean | pems04 | 0.200 | 4.032 |
| disjoint | 5 | 1 | observed_mean | chengdu | 0.100 | 4.032 |
| disjoint | 5 | 1 | observed_mean | shenzhen | 0.180 | 4.032 |
| disjoint | 5 | 1 | observed_mean | expytky | 0.120 | 4.032 |
| disjoint | 5 | 1 | observed_mean | pemsbay | 0.140 | 4.032 |
| disjoint | 5 | 3 | observed_mean | metrla | 0.260 | 5.365 |
| disjoint | 5 | 3 | observed_mean | pems04 | 0.360 | 5.365 |
| disjoint | 5 | 3 | observed_mean | chengdu | 0.120 | 5.365 |
| disjoint | 5 | 3 | observed_mean | shenzhen | 0.240 | 5.365 |
| disjoint | 5 | 3 | observed_mean | expytky | 0.240 | 5.365 |
| disjoint | 5 | 3 | observed_mean | pemsbay | 0.300 | 5.365 |
| disjoint | 5 | 5 | observed_mean | metrla | 0.360 | 6.698 |
| disjoint | 5 | 5 | observed_mean | pems04 | 0.500 | 6.698 |
| disjoint | 5 | 5 | observed_mean | chengdu | 0.200 | 6.698 |
| disjoint | 5 | 5 | observed_mean | shenzhen | 0.340 | 6.698 |
| disjoint | 5 | 5 | observed_mean | expytky | 0.440 | 6.698 |
| disjoint | 5 | 5 | observed_mean | pemsbay | 0.360 | 6.698 |
| disjoint | 5 | 1 | random | metrla | 0.160 | 4.032 |
| disjoint | 5 | 1 | random | pems04 | 0.080 | 4.032 |
| disjoint | 5 | 1 | random | chengdu | 0.060 | 4.032 |
| disjoint | 5 | 1 | random | shenzhen | 0.080 | 4.032 |
| disjoint | 5 | 1 | random | expytky | 0.100 | 4.032 |
| disjoint | 5 | 1 | random | pemsbay | 0.080 | 4.032 |
| disjoint | 5 | 3 | random | metrla | 0.160 | 5.365 |
| disjoint | 5 | 3 | random | pems04 | 0.160 | 5.365 |
| disjoint | 5 | 3 | random | chengdu | 0.080 | 5.365 |
| disjoint | 5 | 3 | random | shenzhen | 0.120 | 5.365 |
| disjoint | 5 | 3 | random | expytky | 0.160 | 5.365 |
| disjoint | 5 | 3 | random | pemsbay | 0.080 | 5.365 |
| disjoint | 5 | 5 | random | metrla | 0.200 | 6.698 |
| disjoint | 5 | 5 | random | pems04 | 0.180 | 6.698 |
| disjoint | 5 | 5 | random | chengdu | 0.120 | 6.698 |
| disjoint | 5 | 5 | random | shenzhen | 0.120 | 6.698 |
| disjoint | 5 | 5 | random | expytky | 0.180 | 6.698 |
| disjoint | 5 | 5 | random | pemsbay | 0.100 | 6.698 |
| disjoint | 10 | 1 | own | metrla | 0.220 | 7.347 |
| disjoint | 10 | 1 | own | pems04 | 0.460 | 7.347 |
| disjoint | 10 | 1 | own | chengdu | 0.060 | 7.347 |
| disjoint | 10 | 1 | own | shenzhen | 0.280 | 7.347 |
| disjoint | 10 | 1 | own | expytky | 0.220 | 7.347 |
| disjoint | 10 | 1 | own | pemsbay | 0.140 | 7.347 |
| disjoint | 10 | 3 | own | metrla | 0.320 | 8.681 |
| disjoint | 10 | 3 | own | pems04 | 0.640 | 8.681 |
| disjoint | 10 | 3 | own | chengdu | 0.220 | 8.681 |
| disjoint | 10 | 3 | own | shenzhen | 0.380 | 8.681 |
| disjoint | 10 | 3 | own | expytky | 0.360 | 8.681 |
| disjoint | 10 | 3 | own | pemsbay | 0.180 | 8.681 |
| disjoint | 10 | 5 | own | metrla | 0.420 | 10.014 |
| disjoint | 10 | 5 | own | pems04 | 0.780 | 10.014 |
| disjoint | 10 | 5 | own | chengdu | 0.280 | 10.014 |
| disjoint | 10 | 5 | own | shenzhen | 0.400 | 10.014 |
| disjoint | 10 | 5 | own | expytky | 0.400 | 10.014 |
| disjoint | 10 | 5 | own | pemsbay | 0.220 | 10.014 |
| disjoint | 10 | 1 | pooled | metrla | 0.380 | 7.347 |
| disjoint | 10 | 1 | pooled | pems04 | 0.460 | 7.347 |
| disjoint | 10 | 1 | pooled | chengdu | 0.060 | 7.347 |
| disjoint | 10 | 1 | pooled | shenzhen | 0.340 | 7.347 |
| disjoint | 10 | 1 | pooled | expytky | 0.240 | 7.347 |
| disjoint | 10 | 1 | pooled | pemsbay | 0.280 | 7.347 |
| disjoint | 10 | 3 | pooled | metrla | 0.580 | 8.681 |
| disjoint | 10 | 3 | pooled | pems04 | 0.600 | 8.681 |
| disjoint | 10 | 3 | pooled | chengdu | 0.100 | 8.681 |
| disjoint | 10 | 3 | pooled | shenzhen | 0.460 | 8.681 |
| disjoint | 10 | 3 | pooled | expytky | 0.360 | 8.681 |
| disjoint | 10 | 3 | pooled | pemsbay | 0.340 | 8.681 |
| disjoint | 10 | 5 | pooled | metrla | 0.720 | 10.014 |
| disjoint | 10 | 5 | pooled | pems04 | 0.800 | 10.014 |
| disjoint | 10 | 5 | pooled | chengdu | 0.180 | 10.014 |
| disjoint | 10 | 5 | pooled | shenzhen | 0.600 | 10.014 |
| disjoint | 10 | 5 | pooled | expytky | 0.420 | 10.014 |
| disjoint | 10 | 5 | pooled | pemsbay | 0.500 | 10.014 |
| disjoint | 10 | 1 | pooled_own | metrla | 0.160 | 7.347 |
| disjoint | 10 | 1 | pooled_own | pems04 | 0.460 | 7.347 |
| disjoint | 10 | 1 | pooled_own | chengdu | 0.080 | 7.347 |
| disjoint | 10 | 1 | pooled_own | shenzhen | 0.300 | 7.347 |
| disjoint | 10 | 1 | pooled_own | expytky | 0.260 | 7.347 |
| disjoint | 10 | 1 | pooled_own | pemsbay | 0.160 | 7.347 |
| disjoint | 10 | 3 | pooled_own | metrla | 0.440 | 8.681 |
| disjoint | 10 | 3 | pooled_own | pems04 | 0.740 | 8.681 |
| disjoint | 10 | 3 | pooled_own | chengdu | 0.220 | 8.681 |
| disjoint | 10 | 3 | pooled_own | shenzhen | 0.380 | 8.681 |
| disjoint | 10 | 3 | pooled_own | expytky | 0.340 | 8.681 |
| disjoint | 10 | 3 | pooled_own | pemsbay | 0.200 | 8.681 |
| disjoint | 10 | 5 | pooled_own | metrla | 0.500 | 10.014 |
| disjoint | 10 | 5 | pooled_own | pems04 | 0.820 | 10.014 |
| disjoint | 10 | 5 | pooled_own | chengdu | 0.340 | 10.014 |
| disjoint | 10 | 5 | pooled_own | shenzhen | 0.420 | 10.014 |
| disjoint | 10 | 5 | pooled_own | expytky | 0.420 | 10.014 |
| disjoint | 10 | 5 | pooled_own | pemsbay | 0.240 | 10.014 |
| disjoint | 10 | 1 | observed_mean | metrla | 0.320 | 7.347 |
| disjoint | 10 | 1 | observed_mean | pems04 | 0.360 | 7.347 |
| disjoint | 10 | 1 | observed_mean | chengdu | 0.120 | 7.347 |
| disjoint | 10 | 1 | observed_mean | shenzhen | 0.300 | 7.347 |
| disjoint | 10 | 1 | observed_mean | expytky | 0.220 | 7.347 |
| disjoint | 10 | 1 | observed_mean | pemsbay | 0.200 | 7.347 |
| disjoint | 10 | 3 | observed_mean | metrla | 0.500 | 8.681 |
| disjoint | 10 | 3 | observed_mean | pems04 | 0.520 | 8.681 |
| disjoint | 10 | 3 | observed_mean | chengdu | 0.180 | 8.681 |
| disjoint | 10 | 3 | observed_mean | shenzhen | 0.420 | 8.681 |
| disjoint | 10 | 3 | observed_mean | expytky | 0.360 | 8.681 |
| disjoint | 10 | 3 | observed_mean | pemsbay | 0.360 | 8.681 |
| disjoint | 10 | 5 | observed_mean | metrla | 0.600 | 10.014 |
| disjoint | 10 | 5 | observed_mean | pems04 | 0.580 | 10.014 |
| disjoint | 10 | 5 | observed_mean | chengdu | 0.220 | 10.014 |
| disjoint | 10 | 5 | observed_mean | shenzhen | 0.440 | 10.014 |
| disjoint | 10 | 5 | observed_mean | expytky | 0.540 | 10.014 |
| disjoint | 10 | 5 | observed_mean | pemsbay | 0.460 | 10.014 |
| disjoint | 10 | 1 | random | metrla | 0.140 | 7.347 |
| disjoint | 10 | 1 | random | pems04 | 0.360 | 7.347 |
| disjoint | 10 | 1 | random | chengdu | 0.080 | 7.347 |
| disjoint | 10 | 1 | random | shenzhen | 0.240 | 7.347 |
| disjoint | 10 | 1 | random | expytky | 0.140 | 7.347 |
| disjoint | 10 | 1 | random | pemsbay | 0.140 | 7.347 |
| disjoint | 10 | 3 | random | metrla | 0.160 | 8.681 |
| disjoint | 10 | 3 | random | pems04 | 0.360 | 8.681 |
| disjoint | 10 | 3 | random | chengdu | 0.100 | 8.681 |
| disjoint | 10 | 3 | random | shenzhen | 0.340 | 8.681 |
| disjoint | 10 | 3 | random | expytky | 0.160 | 8.681 |
| disjoint | 10 | 3 | random | pemsbay | 0.140 | 8.681 |
| disjoint | 10 | 5 | random | metrla | 0.200 | 10.014 |
| disjoint | 10 | 5 | random | pems04 | 0.380 | 10.014 |
| disjoint | 10 | 5 | random | chengdu | 0.100 | 10.014 |
| disjoint | 10 | 5 | random | shenzhen | 0.340 | 10.014 |
| disjoint | 10 | 5 | random | expytky | 0.180 | 10.014 |
| disjoint | 10 | 5 | random | pemsbay | 0.140 | 10.014 |
| disjoint | 15 | 1 | own | metrla | 0.340 | 10.826 |
| disjoint | 15 | 1 | own | pems04 | 0.500 | 10.826 |
| disjoint | 15 | 1 | own | chengdu | 0.240 | 10.826 |
| disjoint | 15 | 1 | own | shenzhen | 0.280 | 10.826 |
| disjoint | 15 | 1 | own | expytky | 0.260 | 10.826 |
| disjoint | 15 | 1 | own | pemsbay | 0.260 | 10.826 |
| disjoint | 15 | 3 | own | metrla | 0.420 | 12.159 |
| disjoint | 15 | 3 | own | pems04 | 0.740 | 12.159 |
| disjoint | 15 | 3 | own | chengdu | 0.320 | 12.159 |
| disjoint | 15 | 3 | own | shenzhen | 0.520 | 12.159 |
| disjoint | 15 | 3 | own | expytky | 0.320 | 12.159 |
| disjoint | 15 | 3 | own | pemsbay | 0.260 | 12.159 |
| disjoint | 15 | 5 | own | metrla | 0.540 | 13.492 |
| disjoint | 15 | 5 | own | pems04 | 0.820 | 13.492 |
| disjoint | 15 | 5 | own | chengdu | 0.400 | 13.492 |
| disjoint | 15 | 5 | own | shenzhen | 0.600 | 13.492 |
| disjoint | 15 | 5 | own | expytky | 0.400 | 13.492 |
| disjoint | 15 | 5 | own | pemsbay | 0.340 | 13.492 |
| disjoint | 15 | 1 | pooled | metrla | 0.420 | 10.826 |
| disjoint | 15 | 1 | pooled | pems04 | 0.600 | 10.826 |
| disjoint | 15 | 1 | pooled | chengdu | 0.200 | 10.826 |
| disjoint | 15 | 1 | pooled | shenzhen | 0.420 | 10.826 |
| disjoint | 15 | 1 | pooled | expytky | 0.280 | 10.826 |
| disjoint | 15 | 1 | pooled | pemsbay | 0.380 | 10.826 |
| disjoint | 15 | 3 | pooled | metrla | 0.520 | 12.159 |
| disjoint | 15 | 3 | pooled | pems04 | 0.780 | 12.159 |
| disjoint | 15 | 3 | pooled | chengdu | 0.240 | 12.159 |
| disjoint | 15 | 3 | pooled | shenzhen | 0.560 | 12.159 |
| disjoint | 15 | 3 | pooled | expytky | 0.460 | 12.159 |
| disjoint | 15 | 3 | pooled | pemsbay | 0.460 | 12.159 |
| disjoint | 15 | 5 | pooled | metrla | 0.760 | 13.492 |
| disjoint | 15 | 5 | pooled | pems04 | 0.900 | 13.492 |
| disjoint | 15 | 5 | pooled | chengdu | 0.280 | 13.492 |
| disjoint | 15 | 5 | pooled | shenzhen | 0.720 | 13.492 |
| disjoint | 15 | 5 | pooled | expytky | 0.640 | 13.492 |
| disjoint | 15 | 5 | pooled | pemsbay | 0.680 | 13.492 |
| disjoint | 15 | 1 | pooled_own | metrla | 0.300 | 10.826 |
| disjoint | 15 | 1 | pooled_own | pems04 | 0.500 | 10.826 |
| disjoint | 15 | 1 | pooled_own | chengdu | 0.240 | 10.826 |
| disjoint | 15 | 1 | pooled_own | shenzhen | 0.260 | 10.826 |
| disjoint | 15 | 1 | pooled_own | expytky | 0.260 | 10.826 |
| disjoint | 15 | 1 | pooled_own | pemsbay | 0.260 | 10.826 |
| disjoint | 15 | 3 | pooled_own | metrla | 0.540 | 12.159 |
| disjoint | 15 | 3 | pooled_own | pems04 | 0.800 | 12.159 |
| disjoint | 15 | 3 | pooled_own | chengdu | 0.340 | 12.159 |
| disjoint | 15 | 3 | pooled_own | shenzhen | 0.480 | 12.159 |
| disjoint | 15 | 3 | pooled_own | expytky | 0.380 | 12.159 |
| disjoint | 15 | 3 | pooled_own | pemsbay | 0.280 | 12.159 |
| disjoint | 15 | 5 | pooled_own | metrla | 0.660 | 13.492 |
| disjoint | 15 | 5 | pooled_own | pems04 | 0.880 | 13.492 |
| disjoint | 15 | 5 | pooled_own | chengdu | 0.460 | 13.492 |
| disjoint | 15 | 5 | pooled_own | shenzhen | 0.620 | 13.492 |
| disjoint | 15 | 5 | pooled_own | expytky | 0.480 | 13.492 |
| disjoint | 15 | 5 | pooled_own | pemsbay | 0.400 | 13.492 |
| disjoint | 15 | 1 | observed_mean | metrla | 0.480 | 10.826 |
| disjoint | 15 | 1 | observed_mean | pems04 | 0.420 | 10.826 |
| disjoint | 15 | 1 | observed_mean | chengdu | 0.240 | 10.826 |
| disjoint | 15 | 1 | observed_mean | shenzhen | 0.400 | 10.826 |
| disjoint | 15 | 1 | observed_mean | expytky | 0.300 | 10.826 |
| disjoint | 15 | 1 | observed_mean | pemsbay | 0.420 | 10.826 |
| disjoint | 15 | 3 | observed_mean | metrla | 0.680 | 12.159 |
| disjoint | 15 | 3 | observed_mean | pems04 | 0.660 | 12.159 |
| disjoint | 15 | 3 | observed_mean | chengdu | 0.360 | 12.159 |
| disjoint | 15 | 3 | observed_mean | shenzhen | 0.680 | 12.159 |
| disjoint | 15 | 3 | observed_mean | expytky | 0.480 | 12.159 |
| disjoint | 15 | 3 | observed_mean | pemsbay | 0.600 | 12.159 |
| disjoint | 15 | 5 | observed_mean | metrla | 0.820 | 13.492 |
| disjoint | 15 | 5 | observed_mean | pems04 | 0.740 | 13.492 |
| disjoint | 15 | 5 | observed_mean | chengdu | 0.400 | 13.492 |
| disjoint | 15 | 5 | observed_mean | shenzhen | 0.780 | 13.492 |
| disjoint | 15 | 5 | observed_mean | expytky | 0.600 | 13.492 |
| disjoint | 15 | 5 | observed_mean | pemsbay | 0.720 | 13.492 |
| disjoint | 15 | 1 | random | metrla | 0.220 | 10.826 |
| disjoint | 15 | 1 | random | pems04 | 0.340 | 10.826 |
| disjoint | 15 | 1 | random | chengdu | 0.200 | 10.826 |
| disjoint | 15 | 1 | random | shenzhen | 0.260 | 10.826 |
| disjoint | 15 | 1 | random | expytky | 0.180 | 10.826 |
| disjoint | 15 | 1 | random | pemsbay | 0.260 | 10.826 |
| disjoint | 15 | 3 | random | metrla | 0.280 | 12.159 |
| disjoint | 15 | 3 | random | pems04 | 0.400 | 12.159 |
| disjoint | 15 | 3 | random | chengdu | 0.260 | 12.159 |
| disjoint | 15 | 3 | random | shenzhen | 0.300 | 12.159 |
| disjoint | 15 | 3 | random | expytky | 0.180 | 12.159 |
| disjoint | 15 | 3 | random | pemsbay | 0.280 | 12.159 |
| disjoint | 15 | 5 | random | metrla | 0.320 | 13.492 |
| disjoint | 15 | 5 | random | pems04 | 0.420 | 13.492 |
| disjoint | 15 | 5 | random | chengdu | 0.300 | 13.492 |
| disjoint | 15 | 5 | random | shenzhen | 0.300 | 13.492 |
| disjoint | 15 | 5 | random | expytky | 0.220 | 13.492 |
| disjoint | 15 | 5 | random | pemsbay | 0.300 | 13.492 |
| anchor | 5 | 1 | own | metrla | 0.100 | 3.937 |
| anchor | 5 | 1 | own | pems04 | 0.340 | 3.937 |
| anchor | 5 | 1 | own | chengdu | 0.060 | 3.937 |
| anchor | 5 | 1 | own | shenzhen | 0.080 | 3.937 |
| anchor | 5 | 1 | own | expytky | 0.020 | 3.937 |
| anchor | 5 | 1 | own | pemsbay | 0.040 | 3.937 |
| anchor | 5 | 3 | own | metrla | 0.140 | 5.270 |
| anchor | 5 | 3 | own | pems04 | 0.500 | 5.270 |
| anchor | 5 | 3 | own | chengdu | 0.100 | 5.270 |
| anchor | 5 | 3 | own | shenzhen | 0.140 | 5.270 |
| anchor | 5 | 3 | own | expytky | 0.200 | 5.270 |
| anchor | 5 | 3 | own | pemsbay | 0.080 | 5.270 |
| anchor | 5 | 5 | own | metrla | 0.200 | 6.604 |
| anchor | 5 | 5 | own | pems04 | 0.540 | 6.604 |
| anchor | 5 | 5 | own | chengdu | 0.220 | 6.604 |
| anchor | 5 | 5 | own | shenzhen | 0.180 | 6.604 |
| anchor | 5 | 5 | own | expytky | 0.300 | 6.604 |
| anchor | 5 | 5 | own | pemsbay | 0.120 | 6.604 |
| anchor | 5 | 1 | pooled | metrla | 0.200 | 3.937 |
| anchor | 5 | 1 | pooled | pems04 | 0.280 | 3.937 |
| anchor | 5 | 1 | pooled | chengdu | 0.040 | 3.937 |
| anchor | 5 | 1 | pooled | shenzhen | 0.080 | 3.937 |
| anchor | 5 | 1 | pooled | expytky | 0.120 | 3.937 |
| anchor | 5 | 1 | pooled | pemsbay | 0.060 | 3.937 |
| anchor | 5 | 3 | pooled | metrla | 0.280 | 5.270 |
| anchor | 5 | 3 | pooled | pems04 | 0.460 | 5.270 |
| anchor | 5 | 3 | pooled | chengdu | 0.140 | 5.270 |
| anchor | 5 | 3 | pooled | shenzhen | 0.220 | 5.270 |
| anchor | 5 | 3 | pooled | expytky | 0.200 | 5.270 |
| anchor | 5 | 3 | pooled | pemsbay | 0.120 | 5.270 |
| anchor | 5 | 5 | pooled | metrla | 0.340 | 6.604 |
| anchor | 5 | 5 | pooled | pems04 | 0.660 | 6.604 |
| anchor | 5 | 5 | pooled | chengdu | 0.220 | 6.604 |
| anchor | 5 | 5 | pooled | shenzhen | 0.360 | 6.604 |
| anchor | 5 | 5 | pooled | expytky | 0.280 | 6.604 |
| anchor | 5 | 5 | pooled | pemsbay | 0.180 | 6.604 |
| anchor | 5 | 1 | pooled_own | metrla | 0.100 | 3.937 |
| anchor | 5 | 1 | pooled_own | pems04 | 0.360 | 3.937 |
| anchor | 5 | 1 | pooled_own | chengdu | 0.040 | 3.937 |
| anchor | 5 | 1 | pooled_own | shenzhen | 0.080 | 3.937 |
| anchor | 5 | 1 | pooled_own | expytky | 0.020 | 3.937 |
| anchor | 5 | 1 | pooled_own | pemsbay | 0.060 | 3.937 |
| anchor | 5 | 3 | pooled_own | metrla | 0.160 | 5.270 |
| anchor | 5 | 3 | pooled_own | pems04 | 0.480 | 5.270 |
| anchor | 5 | 3 | pooled_own | chengdu | 0.160 | 5.270 |
| anchor | 5 | 3 | pooled_own | shenzhen | 0.100 | 5.270 |
| anchor | 5 | 3 | pooled_own | expytky | 0.260 | 5.270 |
| anchor | 5 | 3 | pooled_own | pemsbay | 0.080 | 5.270 |
| anchor | 5 | 5 | pooled_own | metrla | 0.180 | 6.604 |
| anchor | 5 | 5 | pooled_own | pems04 | 0.580 | 6.604 |
| anchor | 5 | 5 | pooled_own | chengdu | 0.220 | 6.604 |
| anchor | 5 | 5 | pooled_own | shenzhen | 0.200 | 6.604 |
| anchor | 5 | 5 | pooled_own | expytky | 0.300 | 6.604 |
| anchor | 5 | 5 | pooled_own | pemsbay | 0.120 | 6.604 |
| anchor | 5 | 1 | observed_mean | metrla | 0.140 | 3.937 |
| anchor | 5 | 1 | observed_mean | pems04 | 0.200 | 3.937 |
| anchor | 5 | 1 | observed_mean | chengdu | 0.080 | 3.937 |
| anchor | 5 | 1 | observed_mean | shenzhen | 0.120 | 3.937 |
| anchor | 5 | 1 | observed_mean | expytky | 0.060 | 3.937 |
| anchor | 5 | 1 | observed_mean | pemsbay | 0.060 | 3.937 |
| anchor | 5 | 3 | observed_mean | metrla | 0.240 | 5.270 |
| anchor | 5 | 3 | observed_mean | pems04 | 0.320 | 5.270 |
| anchor | 5 | 3 | observed_mean | chengdu | 0.120 | 5.270 |
| anchor | 5 | 3 | observed_mean | shenzhen | 0.260 | 5.270 |
| anchor | 5 | 3 | observed_mean | expytky | 0.200 | 5.270 |
| anchor | 5 | 3 | observed_mean | pemsbay | 0.160 | 5.270 |
| anchor | 5 | 5 | observed_mean | metrla | 0.320 | 6.604 |
| anchor | 5 | 5 | observed_mean | pems04 | 0.560 | 6.604 |
| anchor | 5 | 5 | observed_mean | chengdu | 0.180 | 6.604 |
| anchor | 5 | 5 | observed_mean | shenzhen | 0.340 | 6.604 |
| anchor | 5 | 5 | observed_mean | expytky | 0.260 | 6.604 |
| anchor | 5 | 5 | observed_mean | pemsbay | 0.220 | 6.604 |
| anchor | 5 | 1 | random | metrla | 0.100 | 3.937 |
| anchor | 5 | 1 | random | pems04 | 0.200 | 3.937 |
| anchor | 5 | 1 | random | chengdu | 0.040 | 3.937 |
| anchor | 5 | 1 | random | shenzhen | 0.060 | 3.937 |
| anchor | 5 | 1 | random | expytky | 0.040 | 3.937 |
| anchor | 5 | 1 | random | pemsbay | 0.020 | 3.937 |
| anchor | 5 | 3 | random | metrla | 0.120 | 5.270 |
| anchor | 5 | 3 | random | pems04 | 0.220 | 5.270 |
| anchor | 5 | 3 | random | chengdu | 0.040 | 5.270 |
| anchor | 5 | 3 | random | shenzhen | 0.080 | 5.270 |
| anchor | 5 | 3 | random | expytky | 0.080 | 5.270 |
| anchor | 5 | 3 | random | pemsbay | 0.060 | 5.270 |
| anchor | 5 | 5 | random | metrla | 0.160 | 6.604 |
| anchor | 5 | 5 | random | pems04 | 0.220 | 6.604 |
| anchor | 5 | 5 | random | chengdu | 0.060 | 6.604 |
| anchor | 5 | 5 | random | shenzhen | 0.080 | 6.604 |
| anchor | 5 | 5 | random | expytky | 0.140 | 6.604 |
| anchor | 5 | 5 | random | pemsbay | 0.100 | 6.604 |
| anchor | 10 | 1 | own | metrla | 0.240 | 7.240 |
| anchor | 10 | 1 | own | pems04 | 0.400 | 7.240 |
| anchor | 10 | 1 | own | chengdu | 0.200 | 7.240 |
| anchor | 10 | 1 | own | shenzhen | 0.120 | 7.240 |
| anchor | 10 | 1 | own | expytky | 0.200 | 7.240 |
| anchor | 10 | 1 | own | pemsbay | 0.120 | 7.240 |
| anchor | 10 | 3 | own | metrla | 0.340 | 8.573 |
| anchor | 10 | 3 | own | pems04 | 0.620 | 8.573 |
| anchor | 10 | 3 | own | chengdu | 0.340 | 8.573 |
| anchor | 10 | 3 | own | shenzhen | 0.240 | 8.573 |
| anchor | 10 | 3 | own | expytky | 0.320 | 8.573 |
| anchor | 10 | 3 | own | pemsbay | 0.120 | 8.573 |
| anchor | 10 | 5 | own | metrla | 0.380 | 9.907 |
| anchor | 10 | 5 | own | pems04 | 0.760 | 9.907 |
| anchor | 10 | 5 | own | chengdu | 0.400 | 9.907 |
| anchor | 10 | 5 | own | shenzhen | 0.300 | 9.907 |
| anchor | 10 | 5 | own | expytky | 0.400 | 9.907 |
| anchor | 10 | 5 | own | pemsbay | 0.160 | 9.907 |
| anchor | 10 | 1 | pooled | metrla | 0.320 | 7.240 |
| anchor | 10 | 1 | pooled | pems04 | 0.320 | 7.240 |
| anchor | 10 | 1 | pooled | chengdu | 0.140 | 7.240 |
| anchor | 10 | 1 | pooled | shenzhen | 0.160 | 7.240 |
| anchor | 10 | 1 | pooled | expytky | 0.260 | 7.240 |
| anchor | 10 | 1 | pooled | pemsbay | 0.160 | 7.240 |
| anchor | 10 | 3 | pooled | metrla | 0.480 | 8.573 |
| anchor | 10 | 3 | pooled | pems04 | 0.560 | 8.573 |
| anchor | 10 | 3 | pooled | chengdu | 0.280 | 8.573 |
| anchor | 10 | 3 | pooled | shenzhen | 0.300 | 8.573 |
| anchor | 10 | 3 | pooled | expytky | 0.340 | 8.573 |
| anchor | 10 | 3 | pooled | pemsbay | 0.220 | 8.573 |
| anchor | 10 | 5 | pooled | metrla | 0.580 | 9.907 |
| anchor | 10 | 5 | pooled | pems04 | 0.700 | 9.907 |
| anchor | 10 | 5 | pooled | chengdu | 0.360 | 9.907 |
| anchor | 10 | 5 | pooled | shenzhen | 0.360 | 9.907 |
| anchor | 10 | 5 | pooled | expytky | 0.380 | 9.907 |
| anchor | 10 | 5 | pooled | pemsbay | 0.260 | 9.907 |
| anchor | 10 | 1 | pooled_own | metrla | 0.240 | 7.240 |
| anchor | 10 | 1 | pooled_own | pems04 | 0.440 | 7.240 |
| anchor | 10 | 1 | pooled_own | chengdu | 0.200 | 7.240 |
| anchor | 10 | 1 | pooled_own | shenzhen | 0.140 | 7.240 |
| anchor | 10 | 1 | pooled_own | expytky | 0.200 | 7.240 |
| anchor | 10 | 1 | pooled_own | pemsbay | 0.140 | 7.240 |
| anchor | 10 | 3 | pooled_own | metrla | 0.360 | 8.573 |
| anchor | 10 | 3 | pooled_own | pems04 | 0.740 | 8.573 |
| anchor | 10 | 3 | pooled_own | chengdu | 0.400 | 8.573 |
| anchor | 10 | 3 | pooled_own | shenzhen | 0.220 | 8.573 |
| anchor | 10 | 3 | pooled_own | expytky | 0.320 | 8.573 |
| anchor | 10 | 3 | pooled_own | pemsbay | 0.160 | 8.573 |
| anchor | 10 | 5 | pooled_own | metrla | 0.420 | 9.907 |
| anchor | 10 | 5 | pooled_own | pems04 | 0.800 | 9.907 |
| anchor | 10 | 5 | pooled_own | chengdu | 0.420 | 9.907 |
| anchor | 10 | 5 | pooled_own | shenzhen | 0.300 | 9.907 |
| anchor | 10 | 5 | pooled_own | expytky | 0.380 | 9.907 |
| anchor | 10 | 5 | pooled_own | pemsbay | 0.160 | 9.907 |
| anchor | 10 | 1 | observed_mean | metrla | 0.360 | 7.240 |
| anchor | 10 | 1 | observed_mean | pems04 | 0.360 | 7.240 |
| anchor | 10 | 1 | observed_mean | chengdu | 0.140 | 7.240 |
| anchor | 10 | 1 | observed_mean | shenzhen | 0.180 | 7.240 |
| anchor | 10 | 1 | observed_mean | expytky | 0.240 | 7.240 |
| anchor | 10 | 1 | observed_mean | pemsbay | 0.200 | 7.240 |
| anchor | 10 | 3 | observed_mean | metrla | 0.480 | 8.573 |
| anchor | 10 | 3 | observed_mean | pems04 | 0.560 | 8.573 |
| anchor | 10 | 3 | observed_mean | chengdu | 0.240 | 8.573 |
| anchor | 10 | 3 | observed_mean | shenzhen | 0.360 | 8.573 |
| anchor | 10 | 3 | observed_mean | expytky | 0.340 | 8.573 |
| anchor | 10 | 3 | observed_mean | pemsbay | 0.320 | 8.573 |
| anchor | 10 | 5 | observed_mean | metrla | 0.560 | 9.907 |
| anchor | 10 | 5 | observed_mean | pems04 | 0.640 | 9.907 |
| anchor | 10 | 5 | observed_mean | chengdu | 0.280 | 9.907 |
| anchor | 10 | 5 | observed_mean | shenzhen | 0.380 | 9.907 |
| anchor | 10 | 5 | observed_mean | expytky | 0.480 | 9.907 |
| anchor | 10 | 5 | observed_mean | pemsbay | 0.380 | 9.907 |
| anchor | 10 | 1 | random | metrla | 0.200 | 7.240 |
| anchor | 10 | 1 | random | pems04 | 0.220 | 7.240 |
| anchor | 10 | 1 | random | chengdu | 0.140 | 7.240 |
| anchor | 10 | 1 | random | shenzhen | 0.140 | 7.240 |
| anchor | 10 | 1 | random | expytky | 0.160 | 7.240 |
| anchor | 10 | 1 | random | pemsbay | 0.140 | 7.240 |
| anchor | 10 | 3 | random | metrla | 0.200 | 8.573 |
| anchor | 10 | 3 | random | pems04 | 0.240 | 8.573 |
| anchor | 10 | 3 | random | chengdu | 0.140 | 8.573 |
| anchor | 10 | 3 | random | shenzhen | 0.140 | 8.573 |
| anchor | 10 | 3 | random | expytky | 0.160 | 8.573 |
| anchor | 10 | 3 | random | pemsbay | 0.140 | 8.573 |
| anchor | 10 | 5 | random | metrla | 0.240 | 9.907 |
| anchor | 10 | 5 | random | pems04 | 0.260 | 9.907 |
| anchor | 10 | 5 | random | chengdu | 0.200 | 9.907 |
| anchor | 10 | 5 | random | shenzhen | 0.160 | 9.907 |
| anchor | 10 | 5 | random | expytky | 0.180 | 9.907 |
| anchor | 10 | 5 | random | pemsbay | 0.140 | 9.907 |
| anchor | 15 | 1 | own | metrla | 0.300 | 10.431 |
| anchor | 15 | 1 | own | pems04 | 0.560 | 10.431 |
| anchor | 15 | 1 | own | chengdu | 0.120 | 10.431 |
| anchor | 15 | 1 | own | shenzhen | 0.180 | 10.431 |
| anchor | 15 | 1 | own | expytky | 0.240 | 10.431 |
| anchor | 15 | 1 | own | pemsbay | 0.260 | 10.431 |
| anchor | 15 | 3 | own | metrla | 0.420 | 11.765 |
| anchor | 15 | 3 | own | pems04 | 0.720 | 11.765 |
| anchor | 15 | 3 | own | chengdu | 0.200 | 11.765 |
| anchor | 15 | 3 | own | shenzhen | 0.260 | 11.765 |
| anchor | 15 | 3 | own | expytky | 0.420 | 11.765 |
| anchor | 15 | 3 | own | pemsbay | 0.340 | 11.765 |
| anchor | 15 | 5 | own | metrla | 0.460 | 13.098 |
| anchor | 15 | 5 | own | pems04 | 0.800 | 13.098 |
| anchor | 15 | 5 | own | chengdu | 0.300 | 13.098 |
| anchor | 15 | 5 | own | shenzhen | 0.420 | 13.098 |
| anchor | 15 | 5 | own | expytky | 0.540 | 13.098 |
| anchor | 15 | 5 | own | pemsbay | 0.420 | 13.098 |
| anchor | 15 | 1 | pooled | metrla | 0.400 | 10.431 |
| anchor | 15 | 1 | pooled | pems04 | 0.580 | 10.431 |
| anchor | 15 | 1 | pooled | chengdu | 0.120 | 10.431 |
| anchor | 15 | 1 | pooled | shenzhen | 0.320 | 10.431 |
| anchor | 15 | 1 | pooled | expytky | 0.240 | 10.431 |
| anchor | 15 | 1 | pooled | pemsbay | 0.380 | 10.431 |
| anchor | 15 | 3 | pooled | metrla | 0.560 | 11.765 |
| anchor | 15 | 3 | pooled | pems04 | 0.820 | 11.765 |
| anchor | 15 | 3 | pooled | chengdu | 0.160 | 11.765 |
| anchor | 15 | 3 | pooled | shenzhen | 0.460 | 11.765 |
| anchor | 15 | 3 | pooled | expytky | 0.320 | 11.765 |
| anchor | 15 | 3 | pooled | pemsbay | 0.460 | 11.765 |
| anchor | 15 | 5 | pooled | metrla | 0.720 | 13.098 |
| anchor | 15 | 5 | pooled | pems04 | 0.900 | 13.098 |
| anchor | 15 | 5 | pooled | chengdu | 0.260 | 13.098 |
| anchor | 15 | 5 | pooled | shenzhen | 0.600 | 13.098 |
| anchor | 15 | 5 | pooled | expytky | 0.400 | 13.098 |
| anchor | 15 | 5 | pooled | pemsbay | 0.580 | 13.098 |
| anchor | 15 | 1 | pooled_own | metrla | 0.320 | 10.431 |
| anchor | 15 | 1 | pooled_own | pems04 | 0.600 | 10.431 |
| anchor | 15 | 1 | pooled_own | chengdu | 0.120 | 10.431 |
| anchor | 15 | 1 | pooled_own | shenzhen | 0.180 | 10.431 |
| anchor | 15 | 1 | pooled_own | expytky | 0.280 | 10.431 |
| anchor | 15 | 1 | pooled_own | pemsbay | 0.280 | 10.431 |
| anchor | 15 | 3 | pooled_own | metrla | 0.440 | 11.765 |
| anchor | 15 | 3 | pooled_own | pems04 | 0.740 | 11.765 |
| anchor | 15 | 3 | pooled_own | chengdu | 0.220 | 11.765 |
| anchor | 15 | 3 | pooled_own | shenzhen | 0.360 | 11.765 |
| anchor | 15 | 3 | pooled_own | expytky | 0.380 | 11.765 |
| anchor | 15 | 3 | pooled_own | pemsbay | 0.420 | 11.765 |
| anchor | 15 | 5 | pooled_own | metrla | 0.500 | 13.098 |
| anchor | 15 | 5 | pooled_own | pems04 | 0.820 | 13.098 |
| anchor | 15 | 5 | pooled_own | chengdu | 0.280 | 13.098 |
| anchor | 15 | 5 | pooled_own | shenzhen | 0.440 | 13.098 |
| anchor | 15 | 5 | pooled_own | expytky | 0.480 | 13.098 |
| anchor | 15 | 5 | pooled_own | pemsbay | 0.460 | 13.098 |
| anchor | 15 | 1 | observed_mean | metrla | 0.400 | 10.431 |
| anchor | 15 | 1 | observed_mean | pems04 | 0.420 | 10.431 |
| anchor | 15 | 1 | observed_mean | chengdu | 0.100 | 10.431 |
| anchor | 15 | 1 | observed_mean | shenzhen | 0.280 | 10.431 |
| anchor | 15 | 1 | observed_mean | expytky | 0.280 | 10.431 |
| anchor | 15 | 1 | observed_mean | pemsbay | 0.340 | 10.431 |
| anchor | 15 | 3 | observed_mean | metrla | 0.540 | 11.765 |
| anchor | 15 | 3 | observed_mean | pems04 | 0.540 | 11.765 |
| anchor | 15 | 3 | observed_mean | chengdu | 0.220 | 11.765 |
| anchor | 15 | 3 | observed_mean | shenzhen | 0.440 | 11.765 |
| anchor | 15 | 3 | observed_mean | expytky | 0.380 | 11.765 |
| anchor | 15 | 3 | observed_mean | pemsbay | 0.540 | 11.765 |
| anchor | 15 | 5 | observed_mean | metrla | 0.640 | 13.098 |
| anchor | 15 | 5 | observed_mean | pems04 | 0.640 | 13.098 |
| anchor | 15 | 5 | observed_mean | chengdu | 0.340 | 13.098 |
| anchor | 15 | 5 | observed_mean | shenzhen | 0.560 | 13.098 |
| anchor | 15 | 5 | observed_mean | expytky | 0.440 | 13.098 |
| anchor | 15 | 5 | observed_mean | pemsbay | 0.600 | 13.098 |
| anchor | 15 | 1 | random | metrla | 0.220 | 10.431 |
| anchor | 15 | 1 | random | pems04 | 0.300 | 10.431 |
| anchor | 15 | 1 | random | chengdu | 0.120 | 10.431 |
| anchor | 15 | 1 | random | shenzhen | 0.160 | 10.431 |
| anchor | 15 | 1 | random | expytky | 0.260 | 10.431 |
| anchor | 15 | 1 | random | pemsbay | 0.220 | 10.431 |
| anchor | 15 | 3 | random | metrla | 0.240 | 11.765 |
| anchor | 15 | 3 | random | pems04 | 0.380 | 11.765 |
| anchor | 15 | 3 | random | chengdu | 0.120 | 11.765 |
| anchor | 15 | 3 | random | shenzhen | 0.160 | 11.765 |
| anchor | 15 | 3 | random | expytky | 0.260 | 11.765 |
| anchor | 15 | 3 | random | pemsbay | 0.260 | 11.765 |
| anchor | 15 | 5 | random | metrla | 0.260 | 13.098 |
| anchor | 15 | 5 | random | pems04 | 0.440 | 13.098 |
| anchor | 15 | 5 | random | chengdu | 0.160 | 13.098 |
| anchor | 15 | 5 | random | shenzhen | 0.200 | 13.098 |
| anchor | 15 | 5 | random | expytky | 0.260 | 13.098 |
| anchor | 15 | 5 | random | pemsbay | 0.300 | 13.098 |
| anchor | 30 | 1 | own | metrla | 0.540 | 20.600 |
| anchor | 30 | 1 | own | pems04 | 0.740 | 20.600 |
| anchor | 30 | 1 | own | chengdu | 0.440 | 20.600 |
| anchor | 30 | 1 | own | shenzhen | 0.460 | 20.600 |
| anchor | 30 | 1 | own | expytky | 0.480 | 20.600 |
| anchor | 30 | 1 | own | pemsbay | 0.340 | 20.600 |
| anchor | 30 | 3 | own | metrla | 0.720 | 21.933 |
| anchor | 30 | 3 | own | pems04 | 0.960 | 21.933 |
| anchor | 30 | 3 | own | chengdu | 0.560 | 21.933 |
| anchor | 30 | 3 | own | shenzhen | 0.600 | 21.933 |
| anchor | 30 | 3 | own | expytky | 0.560 | 21.933 |
| anchor | 30 | 3 | own | pemsbay | 0.400 | 21.933 |
| anchor | 30 | 5 | own | metrla | 0.820 | 23.267 |
| anchor | 30 | 5 | own | pems04 | 1.000 | 23.267 |
| anchor | 30 | 5 | own | chengdu | 0.600 | 23.267 |
| anchor | 30 | 5 | own | shenzhen | 0.660 | 23.267 |
| anchor | 30 | 5 | own | expytky | 0.660 | 23.267 |
| anchor | 30 | 5 | own | pemsbay | 0.540 | 23.267 |
| anchor | 30 | 1 | pooled | metrla | 0.580 | 20.600 |
| anchor | 30 | 1 | pooled | pems04 | 0.700 | 20.600 |
| anchor | 30 | 1 | pooled | chengdu | 0.380 | 20.600 |
| anchor | 30 | 1 | pooled | shenzhen | 0.600 | 20.600 |
| anchor | 30 | 1 | pooled | expytky | 0.340 | 20.600 |
| anchor | 30 | 1 | pooled | pemsbay | 0.460 | 20.600 |
| anchor | 30 | 3 | pooled | metrla | 0.840 | 21.933 |
| anchor | 30 | 3 | pooled | pems04 | 0.900 | 21.933 |
| anchor | 30 | 3 | pooled | chengdu | 0.420 | 21.933 |
| anchor | 30 | 3 | pooled | shenzhen | 0.740 | 21.933 |
| anchor | 30 | 3 | pooled | expytky | 0.500 | 21.933 |
| anchor | 30 | 3 | pooled | pemsbay | 0.660 | 21.933 |
| anchor | 30 | 5 | pooled | metrla | 0.880 | 23.267 |
| anchor | 30 | 5 | pooled | pems04 | 0.960 | 23.267 |
| anchor | 30 | 5 | pooled | chengdu | 0.460 | 23.267 |
| anchor | 30 | 5 | pooled | shenzhen | 0.840 | 23.267 |
| anchor | 30 | 5 | pooled | expytky | 0.560 | 23.267 |
| anchor | 30 | 5 | pooled | pemsbay | 0.800 | 23.267 |
| anchor | 30 | 1 | pooled_own | metrla | 0.540 | 20.600 |
| anchor | 30 | 1 | pooled_own | pems04 | 0.740 | 20.600 |
| anchor | 30 | 1 | pooled_own | chengdu | 0.420 | 20.600 |
| anchor | 30 | 1 | pooled_own | shenzhen | 0.480 | 20.600 |
| anchor | 30 | 1 | pooled_own | expytky | 0.460 | 20.600 |
| anchor | 30 | 1 | pooled_own | pemsbay | 0.360 | 20.600 |
| anchor | 30 | 3 | pooled_own | metrla | 0.840 | 21.933 |
| anchor | 30 | 3 | pooled_own | pems04 | 0.980 | 21.933 |
| anchor | 30 | 3 | pooled_own | chengdu | 0.560 | 21.933 |
| anchor | 30 | 3 | pooled_own | shenzhen | 0.640 | 21.933 |
| anchor | 30 | 3 | pooled_own | expytky | 0.540 | 21.933 |
| anchor | 30 | 3 | pooled_own | pemsbay | 0.500 | 21.933 |
| anchor | 30 | 5 | pooled_own | metrla | 0.880 | 23.267 |
| anchor | 30 | 5 | pooled_own | pems04 | 1.000 | 23.267 |
| anchor | 30 | 5 | pooled_own | chengdu | 0.600 | 23.267 |
| anchor | 30 | 5 | pooled_own | shenzhen | 0.740 | 23.267 |
| anchor | 30 | 5 | pooled_own | expytky | 0.680 | 23.267 |
| anchor | 30 | 5 | pooled_own | pemsbay | 0.560 | 23.267 |
| anchor | 30 | 1 | observed_mean | metrla | 0.760 | 20.600 |
| anchor | 30 | 1 | observed_mean | pems04 | 0.620 | 20.600 |
| anchor | 30 | 1 | observed_mean | chengdu | 0.440 | 20.600 |
| anchor | 30 | 1 | observed_mean | shenzhen | 0.660 | 20.600 |
| anchor | 30 | 1 | observed_mean | expytky | 0.380 | 20.600 |
| anchor | 30 | 1 | observed_mean | pemsbay | 0.640 | 20.600 |
| anchor | 30 | 3 | observed_mean | metrla | 0.880 | 21.933 |
| anchor | 30 | 3 | observed_mean | pems04 | 0.740 | 21.933 |
| anchor | 30 | 3 | observed_mean | chengdu | 0.560 | 21.933 |
| anchor | 30 | 3 | observed_mean | shenzhen | 0.760 | 21.933 |
| anchor | 30 | 3 | observed_mean | expytky | 0.620 | 21.933 |
| anchor | 30 | 3 | observed_mean | pemsbay | 0.720 | 21.933 |
| anchor | 30 | 5 | observed_mean | metrla | 0.880 | 23.267 |
| anchor | 30 | 5 | observed_mean | pems04 | 0.800 | 23.267 |
| anchor | 30 | 5 | observed_mean | chengdu | 0.640 | 23.267 |
| anchor | 30 | 5 | observed_mean | shenzhen | 0.800 | 23.267 |
| anchor | 30 | 5 | observed_mean | expytky | 0.760 | 23.267 |
| anchor | 30 | 5 | observed_mean | pemsbay | 0.760 | 23.267 |
| anchor | 30 | 1 | random | metrla | 0.380 | 20.600 |
| anchor | 30 | 1 | random | pems04 | 0.400 | 20.600 |
| anchor | 30 | 1 | random | chengdu | 0.380 | 20.600 |
| anchor | 30 | 1 | random | shenzhen | 0.420 | 20.600 |
| anchor | 30 | 1 | random | expytky | 0.340 | 20.600 |
| anchor | 30 | 1 | random | pemsbay | 0.340 | 20.600 |
| anchor | 30 | 3 | random | metrla | 0.380 | 21.933 |
| anchor | 30 | 3 | random | pems04 | 0.400 | 21.933 |
| anchor | 30 | 3 | random | chengdu | 0.380 | 21.933 |
| anchor | 30 | 3 | random | shenzhen | 0.480 | 21.933 |
| anchor | 30 | 3 | random | expytky | 0.360 | 21.933 |
| anchor | 30 | 3 | random | pemsbay | 0.400 | 21.933 |
| anchor | 30 | 5 | random | metrla | 0.380 | 23.267 |
| anchor | 30 | 5 | random | pems04 | 0.440 | 23.267 |
| anchor | 30 | 5 | random | chengdu | 0.400 | 23.267 |
| anchor | 30 | 5 | random | shenzhen | 0.480 | 23.267 |
| anchor | 30 | 5 | random | expytky | 0.380 | 23.267 |
| anchor | 30 | 5 | random | pemsbay | 0.420 | 23.267 |
