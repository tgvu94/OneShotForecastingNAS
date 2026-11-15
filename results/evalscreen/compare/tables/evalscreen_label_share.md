# evalscreen label_share: a sparse label matrix shared by the cities

n architectures are trained at each city (design: independent, disjoint, or anchor = half common and half disjoint); a model predicts every missing entry; each city trains its b best predictions and keeps the best architecture it trained. share = the share of 50 random designs where that architecture lies within one sigma_seed of the best of the list. fleet_cost_pct = the GPU-hours of all pairs and picks over the GPU-hours of the whole matrix. own = a ridge on the labels of the city alone; pooled = one ridge on all trained pairs; pooled_own = own with the pooled prediction as an input; observed_mean = the mean rank at the cities that trained the architecture. Pass: a sharing model with a share of 0.9 or more at three of four cities at a fleet cost of 10 % or less, and a mean share above own at every setting.

### Verdict

| model | settings_at_10pct_with_3_cities | share_of_settings_above_own | cheapest_setting_with_3_cities_pct | pass |
|---|---|---|---|---|
| pooled | 0 | 0.556 | 23.310 | False |
| pooled_own | 0 | 0.889 |  | False |
| observed_mean | 0 | 0.333 |  | False |

### Reference: one city trained in full

| reference | fleet_cost_pct | other_cities_within_sigma |
|---|---|---|
| metrla in full, transfer of its best 5 | 31.108 | 2 |
| pems04 in full, transfer of its best 5 | 28.483 | 2 |
| chengdu in full, transfer of its best 5 | 20.451 | 2 |
| shenzhen in full, transfer of its best 5 | 30.503 | 3 |

### Every setting

| design | n | b | model | fleet_cost_pct | mean_share | min_share | cities_ge_09 | above_own |
|---|---|---|---|---|---|---|---|---|
| anchor | 5 | 1 | observed_mean | 3.997 | 0.155 | 0.040 | 0 | False |
| anchor | 5 | 1 | own | 3.997 | 0.200 | 0.060 | 0 | False |
| anchor | 5 | 1 | pooled | 3.997 | 0.160 | 0.040 | 0 | False |
| anchor | 5 | 1 | pooled_own | 3.997 | 0.185 | 0.040 | 0 | False |
| anchor | 5 | 1 | random | 3.997 | 0.140 | 0.040 | 0 | False |
| anchor | 5 | 3 | observed_mean | 5.330 | 0.295 | 0.120 | 0 | True |
| anchor | 5 | 3 | own | 5.330 | 0.285 | 0.100 | 0 | False |
| anchor | 5 | 3 | pooled | 5.330 | 0.310 | 0.080 | 0 | True |
| anchor | 5 | 3 | pooled_own | 5.330 | 0.300 | 0.120 | 0 | True |
| anchor | 5 | 3 | random | 5.330 | 0.155 | 0.040 | 0 | False |
| anchor | 5 | 5 | observed_mean | 6.663 | 0.385 | 0.140 | 0 | True |
| anchor | 5 | 5 | own | 6.663 | 0.370 | 0.180 | 0 | False |
| anchor | 5 | 5 | pooled | 6.663 | 0.390 | 0.160 | 0 | True |
| anchor | 5 | 5 | pooled_own | 6.663 | 0.385 | 0.200 | 0 | True |
| anchor | 5 | 5 | random | 6.663 | 0.180 | 0.060 | 0 | False |
| anchor | 10 | 1 | observed_mean | 7.299 | 0.310 | 0.140 | 0 | False |
| anchor | 10 | 1 | own | 7.299 | 0.315 | 0.120 | 0 | False |
| anchor | 10 | 1 | pooled | 7.299 | 0.275 | 0.120 | 0 | False |
| anchor | 10 | 1 | pooled_own | 7.299 | 0.335 | 0.120 | 0 | True |
| anchor | 10 | 1 | random | 7.299 | 0.230 | 0.120 | 0 | False |
| anchor | 10 | 3 | observed_mean | 8.633 | 0.405 | 0.220 | 0 | False |
| anchor | 10 | 3 | own | 8.633 | 0.455 | 0.240 | 0 | False |
| anchor | 10 | 3 | pooled | 8.633 | 0.410 | 0.180 | 0 | False |
| anchor | 10 | 3 | pooled_own | 8.633 | 0.470 | 0.240 | 0 | True |
| anchor | 10 | 3 | random | 8.633 | 0.255 | 0.140 | 0 | False |
| anchor | 10 | 5 | observed_mean | 9.966 | 0.495 | 0.260 | 1 | False |
| anchor | 10 | 5 | own | 9.966 | 0.535 | 0.300 | 0 | False |
| anchor | 10 | 5 | pooled | 9.966 | 0.520 | 0.260 | 1 | False |
| anchor | 10 | 5 | pooled_own | 9.966 | 0.555 | 0.300 | 0 | True |
| anchor | 10 | 5 | random | 9.966 | 0.290 | 0.140 | 0 | False |
| anchor | 15 | 1 | observed_mean | 10.478 | 0.340 | 0.140 | 0 | False |
| anchor | 15 | 1 | own | 10.478 | 0.385 | 0.120 | 0 | False |
| anchor | 15 | 1 | pooled | 10.478 | 0.365 | 0.120 | 0 | False |
| anchor | 15 | 1 | pooled_own | 10.478 | 0.400 | 0.120 | 0 | True |
| anchor | 15 | 1 | random | 10.478 | 0.280 | 0.120 | 0 | False |
| anchor | 15 | 3 | observed_mean | 11.811 | 0.455 | 0.220 | 1 | False |
| anchor | 15 | 3 | own | 11.811 | 0.485 | 0.200 | 0 | False |
| anchor | 15 | 3 | pooled | 11.811 | 0.510 | 0.160 | 1 | True |
| anchor | 15 | 3 | pooled_own | 11.811 | 0.520 | 0.200 | 1 | True |
| anchor | 15 | 3 | random | 11.811 | 0.305 | 0.120 | 0 | False |
| anchor | 15 | 5 | observed_mean | 13.145 | 0.550 | 0.320 | 1 | False |
| anchor | 15 | 5 | own | 13.145 | 0.575 | 0.300 | 1 | False |
| anchor | 15 | 5 | pooled | 13.145 | 0.590 | 0.220 | 1 | True |
| anchor | 15 | 5 | pooled_own | 13.145 | 0.605 | 0.340 | 1 | True |
| anchor | 15 | 5 | random | 13.145 | 0.340 | 0.140 | 0 | False |
| anchor | 30 | 1 | observed_mean | 20.624 | 0.555 | 0.140 | 1 | False |
| anchor | 30 | 1 | own | 20.624 | 0.625 | 0.440 | 1 | False |
| anchor | 30 | 1 | pooled | 20.624 | 0.560 | 0.360 | 1 | False |
| anchor | 30 | 1 | pooled_own | 20.624 | 0.640 | 0.460 | 1 | True |
| anchor | 30 | 1 | random | 20.624 | 0.480 | 0.140 | 1 | False |
| anchor | 30 | 3 | observed_mean | 21.958 | 0.625 | 0.260 | 1 | False |
| anchor | 30 | 3 | own | 21.958 | 0.765 | 0.560 | 2 | False |
| anchor | 30 | 3 | pooled | 21.958 | 0.710 | 0.480 | 1 | False |
| anchor | 30 | 3 | pooled_own | 21.958 | 0.765 | 0.540 | 2 | False |
| anchor | 30 | 3 | random | 21.958 | 0.495 | 0.140 | 1 | False |
| anchor | 30 | 5 | observed_mean | 23.291 | 0.685 | 0.360 | 1 | False |
| anchor | 30 | 5 | own | 23.291 | 0.805 | 0.600 | 2 | False |
| anchor | 30 | 5 | pooled | 23.291 | 0.790 | 0.540 | 1 | False |
| anchor | 30 | 5 | pooled_own | 23.291 | 0.825 | 0.600 | 2 | True |
| anchor | 30 | 5 | random | 23.291 | 0.500 | 0.140 | 1 | False |
| disjoint | 5 | 1 | observed_mean | 3.974 | 0.255 | 0.060 | 0 | True |
| disjoint | 5 | 1 | own | 3.974 | 0.195 | 0.080 | 0 | False |
| disjoint | 5 | 1 | pooled | 3.974 | 0.240 | 0.080 | 0 | True |
| disjoint | 5 | 1 | pooled_own | 3.974 | 0.205 | 0.080 | 0 | True |
| disjoint | 5 | 1 | random | 3.974 | 0.155 | 0.040 | 0 | False |
| disjoint | 5 | 3 | observed_mean | 5.307 | 0.345 | 0.140 | 0 | True |
| disjoint | 5 | 3 | own | 5.307 | 0.260 | 0.100 | 0 | False |
| disjoint | 5 | 3 | pooled | 5.307 | 0.320 | 0.120 | 0 | True |
| disjoint | 5 | 3 | pooled_own | 5.307 | 0.290 | 0.120 | 0 | True |
| disjoint | 5 | 3 | random | 5.307 | 0.195 | 0.080 | 0 | False |
| disjoint | 5 | 5 | observed_mean | 6.640 | 0.400 | 0.200 | 0 | True |
| disjoint | 5 | 5 | own | 6.640 | 0.350 | 0.140 | 0 | False |
| disjoint | 5 | 5 | pooled | 6.640 | 0.440 | 0.220 | 1 | True |
| disjoint | 5 | 5 | pooled_own | 6.640 | 0.395 | 0.160 | 0 | True |
| disjoint | 5 | 5 | random | 6.640 | 0.220 | 0.120 | 0 | False |
| disjoint | 10 | 1 | observed_mean | 7.317 | 0.310 | 0.100 | 0 | False |
| disjoint | 10 | 1 | own | 7.317 | 0.330 | 0.060 | 0 | False |
| disjoint | 10 | 1 | pooled | 7.317 | 0.325 | 0.040 | 0 | False |
| disjoint | 10 | 1 | pooled_own | 7.317 | 0.360 | 0.080 | 0 | True |
| disjoint | 10 | 1 | random | 7.317 | 0.255 | 0.080 | 0 | False |
| disjoint | 10 | 3 | observed_mean | 8.650 | 0.385 | 0.160 | 0 | False |
| disjoint | 10 | 3 | own | 8.650 | 0.465 | 0.220 | 0 | False |
| disjoint | 10 | 3 | pooled | 8.650 | 0.465 | 0.160 | 1 | False |
| disjoint | 10 | 3 | pooled_own | 8.650 | 0.510 | 0.220 | 1 | True |
| disjoint | 10 | 3 | random | 8.650 | 0.305 | 0.100 | 0 | False |
| disjoint | 10 | 5 | observed_mean | 9.984 | 0.485 | 0.260 | 1 | False |
| disjoint | 10 | 5 | own | 9.984 | 0.545 | 0.280 | 0 | False |
| disjoint | 10 | 5 | pooled | 9.984 | 0.565 | 0.240 | 1 | True |
| disjoint | 10 | 5 | pooled_own | 9.984 | 0.590 | 0.320 | 1 | True |
| disjoint | 10 | 5 | random | 9.984 | 0.315 | 0.100 | 0 | False |
| disjoint | 15 | 1 | observed_mean | 10.596 | 0.400 | 0.180 | 0 | False |
| disjoint | 15 | 1 | own | 10.596 | 0.415 | 0.240 | 0 | False |
| disjoint | 15 | 1 | pooled | 10.596 | 0.410 | 0.220 | 0 | False |
| disjoint | 15 | 1 | pooled_own | 10.596 | 0.425 | 0.240 | 0 | True |
| disjoint | 15 | 1 | random | 10.596 | 0.335 | 0.180 | 0 | False |
| disjoint | 15 | 3 | observed_mean | 11.930 | 0.545 | 0.300 | 1 | False |
| disjoint | 15 | 3 | own | 11.930 | 0.585 | 0.320 | 0 | False |
| disjoint | 15 | 3 | pooled | 11.930 | 0.595 | 0.300 | 1 | True |
| disjoint | 15 | 3 | pooled_own | 11.930 | 0.620 | 0.360 | 1 | True |
| disjoint | 15 | 3 | random | 11.930 | 0.380 | 0.180 | 0 | False |
| disjoint | 15 | 5 | observed_mean | 13.263 | 0.605 | 0.420 | 1 | False |
| disjoint | 15 | 5 | own | 13.263 | 0.660 | 0.400 | 1 | False |
| disjoint | 15 | 5 | pooled | 13.263 | 0.690 | 0.400 | 1 | True |
| disjoint | 15 | 5 | pooled_own | 13.263 | 0.730 | 0.460 | 1 | True |
| disjoint | 15 | 5 | random | 13.263 | 0.405 | 0.220 | 0 | False |
| disjoint | 30 | 1 | observed_mean | 20.782 | 0.570 | 0.200 | 1 | False |
| disjoint | 30 | 1 | own | 20.782 | 0.605 | 0.420 | 1 | False |
| disjoint | 30 | 1 | pooled | 20.782 | 0.575 | 0.400 | 1 | False |
| disjoint | 30 | 1 | pooled_own | 20.782 | 0.615 | 0.420 | 1 | True |
| disjoint | 30 | 1 | random | 20.782 | 0.455 | 0.200 | 1 | False |
| disjoint | 30 | 3 | observed_mean | 22.116 | 0.650 | 0.280 | 1 | False |
| disjoint | 30 | 3 | own | 22.116 | 0.735 | 0.520 | 1 | False |
| disjoint | 30 | 3 | pooled | 22.116 | 0.765 | 0.520 | 2 | True |
| disjoint | 30 | 3 | pooled_own | 22.116 | 0.740 | 0.540 | 1 | True |
| disjoint | 30 | 3 | random | 22.116 | 0.455 | 0.200 | 1 | False |
| disjoint | 30 | 5 | observed_mean | 23.449 | 0.740 | 0.420 | 1 | False |
| disjoint | 30 | 5 | own | 23.449 | 0.780 | 0.620 | 1 | False |
| disjoint | 30 | 5 | pooled | 23.449 | 0.855 | 0.680 | 2 | True |
| disjoint | 30 | 5 | pooled_own | 23.449 | 0.795 | 0.640 | 1 | True |
| disjoint | 30 | 5 | random | 23.449 | 0.480 | 0.200 | 1 | False |
| independent | 5 | 1 | observed_mean | 4.019 | 0.185 | 0.040 | 0 | True |
| independent | 5 | 1 | own | 4.019 | 0.180 | 0.020 | 0 | False |
| independent | 5 | 1 | pooled | 4.019 | 0.170 | 0.040 | 0 | False |
| independent | 5 | 1 | pooled_own | 4.019 | 0.160 | 0.020 | 0 | False |
| independent | 5 | 1 | random | 4.019 | 0.120 | 0.020 | 0 | False |
| independent | 5 | 3 | observed_mean | 5.352 | 0.300 | 0.120 | 0 | True |
| independent | 5 | 3 | own | 5.352 | 0.270 | 0.060 | 0 | False |
| independent | 5 | 3 | pooled | 5.352 | 0.310 | 0.140 | 0 | True |
| independent | 5 | 3 | pooled_own | 5.352 | 0.290 | 0.080 | 0 | True |
| independent | 5 | 3 | random | 5.352 | 0.170 | 0.020 | 0 | False |
| independent | 5 | 5 | observed_mean | 6.686 | 0.395 | 0.180 | 0 | True |
| independent | 5 | 5 | own | 6.686 | 0.340 | 0.120 | 0 | False |
| independent | 5 | 5 | pooled | 6.686 | 0.395 | 0.160 | 0 | True |
| independent | 5 | 5 | pooled_own | 6.686 | 0.370 | 0.160 | 0 | True |
| independent | 5 | 5 | random | 6.686 | 0.205 | 0.020 | 0 | False |
| independent | 10 | 1 | observed_mean | 7.318 | 0.340 | 0.060 | 0 | True |
| independent | 10 | 1 | own | 7.318 | 0.255 | 0.100 | 0 | False |
| independent | 10 | 1 | pooled | 7.318 | 0.275 | 0.140 | 0 | True |
| independent | 10 | 1 | pooled_own | 7.318 | 0.255 | 0.100 | 0 | False |
| independent | 10 | 1 | random | 7.318 | 0.220 | 0.040 | 0 | False |
| independent | 10 | 3 | observed_mean | 8.651 | 0.450 | 0.180 | 1 | True |
| independent | 10 | 3 | own | 8.651 | 0.410 | 0.160 | 0 | False |
| independent | 10 | 3 | pooled | 8.651 | 0.435 | 0.220 | 1 | True |
| independent | 10 | 3 | pooled_own | 8.651 | 0.435 | 0.200 | 0 | True |
| independent | 10 | 3 | random | 8.651 | 0.250 | 0.060 | 0 | False |
| independent | 10 | 5 | observed_mean | 9.985 | 0.515 | 0.300 | 1 | True |
| independent | 10 | 5 | own | 9.985 | 0.490 | 0.260 | 0 | False |
| independent | 10 | 5 | pooled | 9.985 | 0.540 | 0.260 | 1 | True |
| independent | 10 | 5 | pooled_own | 9.985 | 0.535 | 0.320 | 0 | True |
| independent | 10 | 5 | random | 9.985 | 0.260 | 0.060 | 0 | False |
| independent | 15 | 1 | observed_mean | 10.586 | 0.400 | 0.140 | 0 | True |
| independent | 15 | 1 | own | 10.586 | 0.385 | 0.180 | 0 | False |
| independent | 15 | 1 | pooled | 10.586 | 0.360 | 0.180 | 0 | False |
| independent | 15 | 1 | pooled_own | 10.586 | 0.405 | 0.200 | 0 | True |
| independent | 15 | 1 | random | 10.586 | 0.305 | 0.080 | 0 | False |
| independent | 15 | 3 | observed_mean | 11.919 | 0.500 | 0.180 | 1 | False |
| independent | 15 | 3 | own | 11.919 | 0.545 | 0.280 | 1 | False |
| independent | 15 | 3 | pooled | 11.919 | 0.545 | 0.300 | 1 | False |
| independent | 15 | 3 | pooled_own | 11.919 | 0.580 | 0.320 | 1 | True |
| independent | 15 | 3 | random | 11.919 | 0.330 | 0.120 | 0 | False |
| independent | 15 | 5 | observed_mean | 13.253 | 0.595 | 0.380 | 1 | False |
| independent | 15 | 5 | own | 13.253 | 0.600 | 0.340 | 1 | False |
| independent | 15 | 5 | pooled | 13.253 | 0.650 | 0.380 | 1 | True |
| independent | 15 | 5 | pooled_own | 13.253 | 0.670 | 0.460 | 1 | True |
| independent | 15 | 5 | random | 13.253 | 0.355 | 0.120 | 0 | False |
| independent | 30 | 1 | observed_mean | 20.643 | 0.530 | 0.120 | 1 | False |
| independent | 30 | 1 | own | 20.643 | 0.590 | 0.380 | 1 | False |
| independent | 30 | 1 | pooled | 20.643 | 0.555 | 0.340 | 1 | False |
| independent | 30 | 1 | pooled_own | 20.643 | 0.610 | 0.380 | 1 | True |
| independent | 30 | 1 | random | 20.643 | 0.425 | 0.080 | 1 | False |
| independent | 30 | 3 | observed_mean | 21.976 | 0.625 | 0.260 | 1 | False |
| independent | 30 | 3 | own | 21.976 | 0.700 | 0.460 | 1 | False |
| independent | 30 | 3 | pooled | 21.976 | 0.730 | 0.440 | 1 | True |
| independent | 30 | 3 | pooled_own | 21.976 | 0.750 | 0.460 | 2 | True |
| independent | 30 | 3 | random | 21.976 | 0.440 | 0.080 | 1 | False |
| independent | 30 | 5 | observed_mean | 23.310 | 0.700 | 0.380 | 1 | False |
| independent | 30 | 5 | own | 23.310 | 0.790 | 0.560 | 2 | False |
| independent | 30 | 5 | pooled | 23.310 | 0.840 | 0.520 | 3 | True |
| independent | 30 | 5 | pooled_own | 23.310 | 0.835 | 0.660 | 2 | True |
| independent | 30 | 5 | random | 23.310 | 0.455 | 0.080 | 1 | False |

### Every city

| design | n | b | model | city | share | fleet_cost_pct |
|---|---|---|---|---|---|---|
| independent | 5 | 1 | own | metrla | 0.480 | 4.019 |
| independent | 5 | 1 | own | pems04 | 0.140 | 4.019 |
| independent | 5 | 1 | own | chengdu | 0.080 | 4.019 |
| independent | 5 | 1 | own | shenzhen | 0.020 | 4.019 |
| independent | 5 | 3 | own | metrla | 0.660 | 5.352 |
| independent | 5 | 3 | own | pems04 | 0.240 | 5.352 |
| independent | 5 | 3 | own | chengdu | 0.120 | 5.352 |
| independent | 5 | 3 | own | shenzhen | 0.060 | 5.352 |
| independent | 5 | 5 | own | metrla | 0.700 | 6.686 |
| independent | 5 | 5 | own | pems04 | 0.400 | 6.686 |
| independent | 5 | 5 | own | chengdu | 0.120 | 6.686 |
| independent | 5 | 5 | own | shenzhen | 0.140 | 6.686 |
| independent | 5 | 1 | pooled | metrla | 0.540 | 4.019 |
| independent | 5 | 1 | pooled | pems04 | 0.040 | 4.019 |
| independent | 5 | 1 | pooled | chengdu | 0.060 | 4.019 |
| independent | 5 | 1 | pooled | shenzhen | 0.040 | 4.019 |
| independent | 5 | 3 | pooled | metrla | 0.700 | 5.352 |
| independent | 5 | 3 | pooled | pems04 | 0.240 | 5.352 |
| independent | 5 | 3 | pooled | chengdu | 0.140 | 5.352 |
| independent | 5 | 3 | pooled | shenzhen | 0.160 | 5.352 |
| independent | 5 | 5 | pooled | metrla | 0.820 | 6.686 |
| independent | 5 | 5 | pooled | pems04 | 0.340 | 6.686 |
| independent | 5 | 5 | pooled | chengdu | 0.160 | 6.686 |
| independent | 5 | 5 | pooled | shenzhen | 0.260 | 6.686 |
| independent | 5 | 1 | pooled_own | metrla | 0.460 | 4.019 |
| independent | 5 | 1 | pooled_own | pems04 | 0.100 | 4.019 |
| independent | 5 | 1 | pooled_own | chengdu | 0.060 | 4.019 |
| independent | 5 | 1 | pooled_own | shenzhen | 0.020 | 4.019 |
| independent | 5 | 3 | pooled_own | metrla | 0.640 | 5.352 |
| independent | 5 | 3 | pooled_own | pems04 | 0.320 | 5.352 |
| independent | 5 | 3 | pooled_own | chengdu | 0.120 | 5.352 |
| independent | 5 | 3 | pooled_own | shenzhen | 0.080 | 5.352 |
| independent | 5 | 5 | pooled_own | metrla | 0.720 | 6.686 |
| independent | 5 | 5 | pooled_own | pems04 | 0.420 | 6.686 |
| independent | 5 | 5 | pooled_own | chengdu | 0.180 | 6.686 |
| independent | 5 | 5 | pooled_own | shenzhen | 0.160 | 6.686 |
| independent | 5 | 1 | observed_mean | metrla | 0.520 | 4.019 |
| independent | 5 | 1 | observed_mean | pems04 | 0.040 | 4.019 |
| independent | 5 | 1 | observed_mean | chengdu | 0.080 | 4.019 |
| independent | 5 | 1 | observed_mean | shenzhen | 0.100 | 4.019 |
| independent | 5 | 3 | observed_mean | metrla | 0.760 | 5.352 |
| independent | 5 | 3 | observed_mean | pems04 | 0.160 | 5.352 |
| independent | 5 | 3 | observed_mean | chengdu | 0.120 | 5.352 |
| independent | 5 | 3 | observed_mean | shenzhen | 0.160 | 5.352 |
| independent | 5 | 5 | observed_mean | metrla | 0.860 | 6.686 |
| independent | 5 | 5 | observed_mean | pems04 | 0.280 | 6.686 |
| independent | 5 | 5 | observed_mean | chengdu | 0.180 | 6.686 |
| independent | 5 | 5 | observed_mean | shenzhen | 0.260 | 6.686 |
| independent | 5 | 1 | random | metrla | 0.360 | 4.019 |
| independent | 5 | 1 | random | pems04 | 0.020 | 4.019 |
| independent | 5 | 1 | random | chengdu | 0.080 | 4.019 |
| independent | 5 | 1 | random | shenzhen | 0.020 | 4.019 |
| independent | 5 | 3 | random | metrla | 0.520 | 5.352 |
| independent | 5 | 3 | random | pems04 | 0.040 | 5.352 |
| independent | 5 | 3 | random | chengdu | 0.100 | 5.352 |
| independent | 5 | 3 | random | shenzhen | 0.020 | 5.352 |
| independent | 5 | 5 | random | metrla | 0.600 | 6.686 |
| independent | 5 | 5 | random | pems04 | 0.060 | 6.686 |
| independent | 5 | 5 | random | chengdu | 0.140 | 6.686 |
| independent | 5 | 5 | random | shenzhen | 0.020 | 6.686 |
| independent | 10 | 1 | own | metrla | 0.620 | 7.318 |
| independent | 10 | 1 | own | pems04 | 0.180 | 7.318 |
| independent | 10 | 1 | own | chengdu | 0.120 | 7.318 |
| independent | 10 | 1 | own | shenzhen | 0.100 | 7.318 |
| independent | 10 | 3 | own | metrla | 0.800 | 8.651 |
| independent | 10 | 3 | own | pems04 | 0.460 | 8.651 |
| independent | 10 | 3 | own | chengdu | 0.220 | 8.651 |
| independent | 10 | 3 | own | shenzhen | 0.160 | 8.651 |
| independent | 10 | 5 | own | metrla | 0.840 | 9.985 |
| independent | 10 | 5 | own | pems04 | 0.560 | 9.985 |
| independent | 10 | 5 | own | chengdu | 0.260 | 9.985 |
| independent | 10 | 5 | own | shenzhen | 0.300 | 9.985 |
| independent | 10 | 1 | pooled | metrla | 0.680 | 7.318 |
| independent | 10 | 1 | pooled | pems04 | 0.140 | 7.318 |
| independent | 10 | 1 | pooled | chengdu | 0.140 | 7.318 |
| independent | 10 | 1 | pooled | shenzhen | 0.140 | 7.318 |
| independent | 10 | 3 | pooled | metrla | 0.920 | 8.651 |
| independent | 10 | 3 | pooled | pems04 | 0.320 | 8.651 |
| independent | 10 | 3 | pooled | chengdu | 0.220 | 8.651 |
| independent | 10 | 3 | pooled | shenzhen | 0.280 | 8.651 |
| independent | 10 | 5 | pooled | metrla | 1.000 | 9.985 |
| independent | 10 | 5 | pooled | pems04 | 0.480 | 9.985 |
| independent | 10 | 5 | pooled | chengdu | 0.260 | 9.985 |
| independent | 10 | 5 | pooled | shenzhen | 0.420 | 9.985 |
| independent | 10 | 1 | pooled_own | metrla | 0.640 | 7.318 |
| independent | 10 | 1 | pooled_own | pems04 | 0.180 | 7.318 |
| independent | 10 | 1 | pooled_own | chengdu | 0.100 | 7.318 |
| independent | 10 | 1 | pooled_own | shenzhen | 0.100 | 7.318 |
| independent | 10 | 3 | pooled_own | metrla | 0.800 | 8.651 |
| independent | 10 | 3 | pooled_own | pems04 | 0.520 | 8.651 |
| independent | 10 | 3 | pooled_own | chengdu | 0.220 | 8.651 |
| independent | 10 | 3 | pooled_own | shenzhen | 0.200 | 8.651 |
| independent | 10 | 5 | pooled_own | metrla | 0.840 | 9.985 |
| independent | 10 | 5 | pooled_own | pems04 | 0.640 | 9.985 |
| independent | 10 | 5 | pooled_own | chengdu | 0.340 | 9.985 |
| independent | 10 | 5 | pooled_own | shenzhen | 0.320 | 9.985 |
| independent | 10 | 1 | observed_mean | metrla | 0.840 | 7.318 |
| independent | 10 | 1 | observed_mean | pems04 | 0.060 | 7.318 |
| independent | 10 | 1 | observed_mean | chengdu | 0.180 | 7.318 |
| independent | 10 | 1 | observed_mean | shenzhen | 0.280 | 7.318 |
| independent | 10 | 3 | observed_mean | metrla | 0.920 | 8.651 |
| independent | 10 | 3 | observed_mean | pems04 | 0.180 | 8.651 |
| independent | 10 | 3 | observed_mean | chengdu | 0.260 | 8.651 |
| independent | 10 | 3 | observed_mean | shenzhen | 0.440 | 8.651 |
| independent | 10 | 5 | observed_mean | metrla | 0.960 | 9.985 |
| independent | 10 | 5 | observed_mean | pems04 | 0.300 | 9.985 |
| independent | 10 | 5 | observed_mean | chengdu | 0.300 | 9.985 |
| independent | 10 | 5 | observed_mean | shenzhen | 0.500 | 9.985 |
| independent | 10 | 1 | random | metrla | 0.580 | 7.318 |
| independent | 10 | 1 | random | pems04 | 0.040 | 7.318 |
| independent | 10 | 1 | random | chengdu | 0.140 | 7.318 |
| independent | 10 | 1 | random | shenzhen | 0.120 | 7.318 |
| independent | 10 | 3 | random | metrla | 0.640 | 8.651 |
| independent | 10 | 3 | random | pems04 | 0.060 | 8.651 |
| independent | 10 | 3 | random | chengdu | 0.160 | 8.651 |
| independent | 10 | 3 | random | shenzhen | 0.140 | 8.651 |
| independent | 10 | 5 | random | metrla | 0.660 | 9.985 |
| independent | 10 | 5 | random | pems04 | 0.060 | 9.985 |
| independent | 10 | 5 | random | chengdu | 0.160 | 9.985 |
| independent | 10 | 5 | random | shenzhen | 0.160 | 9.985 |
| independent | 15 | 1 | own | metrla | 0.820 | 10.586 |
| independent | 15 | 1 | own | pems04 | 0.300 | 10.586 |
| independent | 15 | 1 | own | chengdu | 0.180 | 10.586 |
| independent | 15 | 1 | own | shenzhen | 0.240 | 10.586 |
| independent | 15 | 3 | own | metrla | 0.940 | 11.919 |
| independent | 15 | 3 | own | pems04 | 0.660 | 11.919 |
| independent | 15 | 3 | own | chengdu | 0.280 | 11.919 |
| independent | 15 | 3 | own | shenzhen | 0.300 | 11.919 |
| independent | 15 | 5 | own | metrla | 0.940 | 13.253 |
| independent | 15 | 5 | own | pems04 | 0.700 | 13.253 |
| independent | 15 | 5 | own | chengdu | 0.340 | 13.253 |
| independent | 15 | 5 | own | shenzhen | 0.420 | 13.253 |
| independent | 15 | 1 | pooled | metrla | 0.760 | 10.586 |
| independent | 15 | 1 | pooled | pems04 | 0.200 | 10.586 |
| independent | 15 | 1 | pooled | chengdu | 0.180 | 10.586 |
| independent | 15 | 1 | pooled | shenzhen | 0.300 | 10.586 |
| independent | 15 | 3 | pooled | metrla | 0.900 | 11.919 |
| independent | 15 | 3 | pooled | pems04 | 0.500 | 11.919 |
| independent | 15 | 3 | pooled | chengdu | 0.300 | 11.919 |
| independent | 15 | 3 | pooled | shenzhen | 0.480 | 11.919 |
| independent | 15 | 5 | pooled | metrla | 0.980 | 13.253 |
| independent | 15 | 5 | pooled | pems04 | 0.600 | 13.253 |
| independent | 15 | 5 | pooled | chengdu | 0.380 | 13.253 |
| independent | 15 | 5 | pooled | shenzhen | 0.640 | 13.253 |
| independent | 15 | 1 | pooled_own | metrla | 0.800 | 10.586 |
| independent | 15 | 1 | pooled_own | pems04 | 0.360 | 10.586 |
| independent | 15 | 1 | pooled_own | chengdu | 0.200 | 10.586 |
| independent | 15 | 1 | pooled_own | shenzhen | 0.260 | 10.586 |
| independent | 15 | 3 | pooled_own | metrla | 0.940 | 11.919 |
| independent | 15 | 3 | pooled_own | pems04 | 0.700 | 11.919 |
| independent | 15 | 3 | pooled_own | chengdu | 0.320 | 11.919 |
| independent | 15 | 3 | pooled_own | shenzhen | 0.360 | 11.919 |
| independent | 15 | 5 | pooled_own | metrla | 0.960 | 13.253 |
| independent | 15 | 5 | pooled_own | pems04 | 0.800 | 13.253 |
| independent | 15 | 5 | pooled_own | chengdu | 0.460 | 13.253 |
| independent | 15 | 5 | pooled_own | shenzhen | 0.460 | 13.253 |
| independent | 15 | 1 | observed_mean | metrla | 0.820 | 10.586 |
| independent | 15 | 1 | observed_mean | pems04 | 0.140 | 10.586 |
| independent | 15 | 1 | observed_mean | chengdu | 0.240 | 10.586 |
| independent | 15 | 1 | observed_mean | shenzhen | 0.400 | 10.586 |
| independent | 15 | 3 | observed_mean | metrla | 0.940 | 11.919 |
| independent | 15 | 3 | observed_mean | pems04 | 0.180 | 11.919 |
| independent | 15 | 3 | observed_mean | chengdu | 0.340 | 11.919 |
| independent | 15 | 3 | observed_mean | shenzhen | 0.540 | 11.919 |
| independent | 15 | 5 | observed_mean | metrla | 0.960 | 13.253 |
| independent | 15 | 5 | observed_mean | pems04 | 0.440 | 13.253 |
| independent | 15 | 5 | observed_mean | chengdu | 0.380 | 13.253 |
| independent | 15 | 5 | observed_mean | shenzhen | 0.600 | 13.253 |
| independent | 15 | 1 | random | metrla | 0.720 | 10.586 |
| independent | 15 | 1 | random | pems04 | 0.080 | 10.586 |
| independent | 15 | 1 | random | chengdu | 0.180 | 10.586 |
| independent | 15 | 1 | random | shenzhen | 0.240 | 10.586 |
| independent | 15 | 3 | random | metrla | 0.740 | 11.919 |
| independent | 15 | 3 | random | pems04 | 0.120 | 11.919 |
| independent | 15 | 3 | random | chengdu | 0.180 | 11.919 |
| independent | 15 | 3 | random | shenzhen | 0.280 | 11.919 |
| independent | 15 | 5 | random | metrla | 0.780 | 13.253 |
| independent | 15 | 5 | random | pems04 | 0.120 | 13.253 |
| independent | 15 | 5 | random | chengdu | 0.220 | 13.253 |
| independent | 15 | 5 | random | shenzhen | 0.300 | 13.253 |
| independent | 30 | 1 | own | metrla | 0.960 | 20.643 |
| independent | 30 | 1 | own | pems04 | 0.620 | 20.643 |
| independent | 30 | 1 | own | chengdu | 0.380 | 20.643 |
| independent | 30 | 1 | own | shenzhen | 0.400 | 20.643 |
| independent | 30 | 3 | own | metrla | 0.980 | 21.976 |
| independent | 30 | 3 | own | pems04 | 0.800 | 21.976 |
| independent | 30 | 3 | own | chengdu | 0.460 | 21.976 |
| independent | 30 | 3 | own | shenzhen | 0.560 | 21.976 |
| independent | 30 | 5 | own | metrla | 0.980 | 23.310 |
| independent | 30 | 5 | own | pems04 | 0.960 | 23.310 |
| independent | 30 | 5 | own | chengdu | 0.560 | 23.310 |
| independent | 30 | 5 | own | shenzhen | 0.660 | 23.310 |
| independent | 30 | 1 | pooled | metrla | 0.960 | 20.643 |
| independent | 30 | 1 | pooled | pems04 | 0.440 | 20.643 |
| independent | 30 | 1 | pooled | chengdu | 0.340 | 20.643 |
| independent | 30 | 1 | pooled | shenzhen | 0.480 | 20.643 |
| independent | 30 | 3 | pooled | metrla | 0.980 | 21.976 |
| independent | 30 | 3 | pooled | pems04 | 0.740 | 21.976 |
| independent | 30 | 3 | pooled | chengdu | 0.440 | 21.976 |
| independent | 30 | 3 | pooled | shenzhen | 0.760 | 21.976 |
| independent | 30 | 5 | pooled | metrla | 1.000 | 23.310 |
| independent | 30 | 5 | pooled | pems04 | 0.940 | 23.310 |
| independent | 30 | 5 | pooled | chengdu | 0.520 | 23.310 |
| independent | 30 | 5 | pooled | shenzhen | 0.900 | 23.310 |
| independent | 30 | 1 | pooled_own | metrla | 0.980 | 20.643 |
| independent | 30 | 1 | pooled_own | pems04 | 0.660 | 20.643 |
| independent | 30 | 1 | pooled_own | chengdu | 0.380 | 20.643 |
| independent | 30 | 1 | pooled_own | shenzhen | 0.420 | 20.643 |
| independent | 30 | 3 | pooled_own | metrla | 1.000 | 21.976 |
| independent | 30 | 3 | pooled_own | pems04 | 0.900 | 21.976 |
| independent | 30 | 3 | pooled_own | chengdu | 0.460 | 21.976 |
| independent | 30 | 3 | pooled_own | shenzhen | 0.640 | 21.976 |
| independent | 30 | 5 | pooled_own | metrla | 1.000 | 23.310 |
| independent | 30 | 5 | pooled_own | pems04 | 0.980 | 23.310 |
| independent | 30 | 5 | pooled_own | chengdu | 0.660 | 23.310 |
| independent | 30 | 5 | pooled_own | shenzhen | 0.700 | 23.310 |
| independent | 30 | 1 | observed_mean | metrla | 1.000 | 20.643 |
| independent | 30 | 1 | observed_mean | pems04 | 0.120 | 20.643 |
| independent | 30 | 1 | observed_mean | chengdu | 0.440 | 20.643 |
| independent | 30 | 1 | observed_mean | shenzhen | 0.560 | 20.643 |
| independent | 30 | 3 | observed_mean | metrla | 1.000 | 21.976 |
| independent | 30 | 3 | observed_mean | pems04 | 0.260 | 21.976 |
| independent | 30 | 3 | observed_mean | chengdu | 0.500 | 21.976 |
| independent | 30 | 3 | observed_mean | shenzhen | 0.740 | 21.976 |
| independent | 30 | 5 | observed_mean | metrla | 1.000 | 23.310 |
| independent | 30 | 5 | observed_mean | pems04 | 0.380 | 23.310 |
| independent | 30 | 5 | observed_mean | chengdu | 0.600 | 23.310 |
| independent | 30 | 5 | observed_mean | shenzhen | 0.820 | 23.310 |
| independent | 30 | 1 | random | metrla | 0.920 | 20.643 |
| independent | 30 | 1 | random | pems04 | 0.080 | 20.643 |
| independent | 30 | 1 | random | chengdu | 0.360 | 20.643 |
| independent | 30 | 1 | random | shenzhen | 0.340 | 20.643 |
| independent | 30 | 3 | random | metrla | 0.980 | 21.976 |
| independent | 30 | 3 | random | pems04 | 0.080 | 21.976 |
| independent | 30 | 3 | random | chengdu | 0.360 | 21.976 |
| independent | 30 | 3 | random | shenzhen | 0.340 | 21.976 |
| independent | 30 | 5 | random | metrla | 0.980 | 23.310 |
| independent | 30 | 5 | random | pems04 | 0.080 | 23.310 |
| independent | 30 | 5 | random | chengdu | 0.400 | 23.310 |
| independent | 30 | 5 | random | shenzhen | 0.360 | 23.310 |
| disjoint | 5 | 1 | own | metrla | 0.520 | 3.974 |
| disjoint | 5 | 1 | own | pems04 | 0.080 | 3.974 |
| disjoint | 5 | 1 | own | chengdu | 0.100 | 3.974 |
| disjoint | 5 | 1 | own | shenzhen | 0.080 | 3.974 |
| disjoint | 5 | 3 | own | metrla | 0.600 | 5.307 |
| disjoint | 5 | 3 | own | pems04 | 0.140 | 5.307 |
| disjoint | 5 | 3 | own | chengdu | 0.200 | 5.307 |
| disjoint | 5 | 3 | own | shenzhen | 0.100 | 5.307 |
| disjoint | 5 | 5 | own | metrla | 0.740 | 6.640 |
| disjoint | 5 | 5 | own | pems04 | 0.240 | 6.640 |
| disjoint | 5 | 5 | own | chengdu | 0.280 | 6.640 |
| disjoint | 5 | 5 | own | shenzhen | 0.140 | 6.640 |
| disjoint | 5 | 1 | pooled | metrla | 0.640 | 3.974 |
| disjoint | 5 | 1 | pooled | pems04 | 0.120 | 3.974 |
| disjoint | 5 | 1 | pooled | chengdu | 0.080 | 3.974 |
| disjoint | 5 | 1 | pooled | shenzhen | 0.120 | 3.974 |
| disjoint | 5 | 3 | pooled | metrla | 0.800 | 5.307 |
| disjoint | 5 | 3 | pooled | pems04 | 0.220 | 5.307 |
| disjoint | 5 | 3 | pooled | chengdu | 0.120 | 5.307 |
| disjoint | 5 | 3 | pooled | shenzhen | 0.140 | 5.307 |
| disjoint | 5 | 5 | pooled | metrla | 0.900 | 6.640 |
| disjoint | 5 | 5 | pooled | pems04 | 0.360 | 6.640 |
| disjoint | 5 | 5 | pooled | chengdu | 0.220 | 6.640 |
| disjoint | 5 | 5 | pooled | shenzhen | 0.280 | 6.640 |
| disjoint | 5 | 1 | pooled_own | metrla | 0.520 | 3.974 |
| disjoint | 5 | 1 | pooled_own | pems04 | 0.120 | 3.974 |
| disjoint | 5 | 1 | pooled_own | chengdu | 0.100 | 3.974 |
| disjoint | 5 | 1 | pooled_own | shenzhen | 0.080 | 3.974 |
| disjoint | 5 | 3 | pooled_own | metrla | 0.660 | 5.307 |
| disjoint | 5 | 3 | pooled_own | pems04 | 0.180 | 5.307 |
| disjoint | 5 | 3 | pooled_own | chengdu | 0.200 | 5.307 |
| disjoint | 5 | 3 | pooled_own | shenzhen | 0.120 | 5.307 |
| disjoint | 5 | 5 | pooled_own | metrla | 0.780 | 6.640 |
| disjoint | 5 | 5 | pooled_own | pems04 | 0.320 | 6.640 |
| disjoint | 5 | 5 | pooled_own | chengdu | 0.320 | 6.640 |
| disjoint | 5 | 5 | pooled_own | shenzhen | 0.160 | 6.640 |
| disjoint | 5 | 1 | observed_mean | metrla | 0.660 | 3.974 |
| disjoint | 5 | 1 | observed_mean | pems04 | 0.060 | 3.974 |
| disjoint | 5 | 1 | observed_mean | chengdu | 0.120 | 3.974 |
| disjoint | 5 | 1 | observed_mean | shenzhen | 0.180 | 3.974 |
| disjoint | 5 | 3 | observed_mean | metrla | 0.800 | 5.307 |
| disjoint | 5 | 3 | observed_mean | pems04 | 0.180 | 5.307 |
| disjoint | 5 | 3 | observed_mean | chengdu | 0.140 | 5.307 |
| disjoint | 5 | 3 | observed_mean | shenzhen | 0.260 | 5.307 |
| disjoint | 5 | 5 | observed_mean | metrla | 0.860 | 6.640 |
| disjoint | 5 | 5 | observed_mean | pems04 | 0.240 | 6.640 |
| disjoint | 5 | 5 | observed_mean | chengdu | 0.200 | 6.640 |
| disjoint | 5 | 5 | observed_mean | shenzhen | 0.300 | 6.640 |
| disjoint | 5 | 1 | random | metrla | 0.440 | 3.974 |
| disjoint | 5 | 1 | random | pems04 | 0.040 | 3.974 |
| disjoint | 5 | 1 | random | chengdu | 0.060 | 3.974 |
| disjoint | 5 | 1 | random | shenzhen | 0.080 | 3.974 |
| disjoint | 5 | 3 | random | metrla | 0.480 | 5.307 |
| disjoint | 5 | 3 | random | pems04 | 0.100 | 5.307 |
| disjoint | 5 | 3 | random | chengdu | 0.080 | 5.307 |
| disjoint | 5 | 3 | random | shenzhen | 0.120 | 5.307 |
| disjoint | 5 | 5 | random | metrla | 0.520 | 6.640 |
| disjoint | 5 | 5 | random | pems04 | 0.120 | 6.640 |
| disjoint | 5 | 5 | random | chengdu | 0.120 | 6.640 |
| disjoint | 5 | 5 | random | shenzhen | 0.120 | 6.640 |
| disjoint | 10 | 1 | own | metrla | 0.680 | 7.317 |
| disjoint | 10 | 1 | own | pems04 | 0.300 | 7.317 |
| disjoint | 10 | 1 | own | chengdu | 0.060 | 7.317 |
| disjoint | 10 | 1 | own | shenzhen | 0.280 | 7.317 |
| disjoint | 10 | 3 | own | metrla | 0.820 | 8.650 |
| disjoint | 10 | 3 | own | pems04 | 0.440 | 8.650 |
| disjoint | 10 | 3 | own | chengdu | 0.220 | 8.650 |
| disjoint | 10 | 3 | own | shenzhen | 0.380 | 8.650 |
| disjoint | 10 | 5 | own | metrla | 0.880 | 9.984 |
| disjoint | 10 | 5 | own | pems04 | 0.620 | 9.984 |
| disjoint | 10 | 5 | own | chengdu | 0.280 | 9.984 |
| disjoint | 10 | 5 | own | shenzhen | 0.400 | 9.984 |
| disjoint | 10 | 1 | pooled | metrla | 0.700 | 7.317 |
| disjoint | 10 | 1 | pooled | pems04 | 0.240 | 7.317 |
| disjoint | 10 | 1 | pooled | chengdu | 0.040 | 7.317 |
| disjoint | 10 | 1 | pooled | shenzhen | 0.320 | 7.317 |
| disjoint | 10 | 3 | pooled | metrla | 0.900 | 8.650 |
| disjoint | 10 | 3 | pooled | pems04 | 0.380 | 8.650 |
| disjoint | 10 | 3 | pooled | chengdu | 0.160 | 8.650 |
| disjoint | 10 | 3 | pooled | shenzhen | 0.420 | 8.650 |
| disjoint | 10 | 5 | pooled | metrla | 0.960 | 9.984 |
| disjoint | 10 | 5 | pooled | pems04 | 0.520 | 9.984 |
| disjoint | 10 | 5 | pooled | chengdu | 0.240 | 9.984 |
| disjoint | 10 | 5 | pooled | shenzhen | 0.540 | 9.984 |
| disjoint | 10 | 1 | pooled_own | metrla | 0.740 | 7.317 |
| disjoint | 10 | 1 | pooled_own | pems04 | 0.320 | 7.317 |
| disjoint | 10 | 1 | pooled_own | chengdu | 0.080 | 7.317 |
| disjoint | 10 | 1 | pooled_own | shenzhen | 0.300 | 7.317 |
| disjoint | 10 | 3 | pooled_own | metrla | 0.920 | 8.650 |
| disjoint | 10 | 3 | pooled_own | pems04 | 0.480 | 8.650 |
| disjoint | 10 | 3 | pooled_own | chengdu | 0.220 | 8.650 |
| disjoint | 10 | 3 | pooled_own | shenzhen | 0.420 | 8.650 |
| disjoint | 10 | 5 | pooled_own | metrla | 0.940 | 9.984 |
| disjoint | 10 | 5 | pooled_own | pems04 | 0.660 | 9.984 |
| disjoint | 10 | 5 | pooled_own | chengdu | 0.320 | 9.984 |
| disjoint | 10 | 5 | pooled_own | shenzhen | 0.440 | 9.984 |
| disjoint | 10 | 1 | observed_mean | metrla | 0.700 | 7.317 |
| disjoint | 10 | 1 | observed_mean | pems04 | 0.140 | 7.317 |
| disjoint | 10 | 1 | observed_mean | chengdu | 0.100 | 7.317 |
| disjoint | 10 | 1 | observed_mean | shenzhen | 0.300 | 7.317 |
| disjoint | 10 | 3 | observed_mean | metrla | 0.840 | 8.650 |
| disjoint | 10 | 3 | observed_mean | pems04 | 0.180 | 8.650 |
| disjoint | 10 | 3 | observed_mean | chengdu | 0.160 | 8.650 |
| disjoint | 10 | 3 | observed_mean | shenzhen | 0.360 | 8.650 |
| disjoint | 10 | 5 | observed_mean | metrla | 0.960 | 9.984 |
| disjoint | 10 | 5 | observed_mean | pems04 | 0.320 | 9.984 |
| disjoint | 10 | 5 | observed_mean | chengdu | 0.260 | 9.984 |
| disjoint | 10 | 5 | observed_mean | shenzhen | 0.400 | 9.984 |
| disjoint | 10 | 1 | random | metrla | 0.580 | 7.317 |
| disjoint | 10 | 1 | random | pems04 | 0.120 | 7.317 |
| disjoint | 10 | 1 | random | chengdu | 0.080 | 7.317 |
| disjoint | 10 | 1 | random | shenzhen | 0.240 | 7.317 |
| disjoint | 10 | 3 | random | metrla | 0.640 | 8.650 |
| disjoint | 10 | 3 | random | pems04 | 0.140 | 8.650 |
| disjoint | 10 | 3 | random | chengdu | 0.100 | 8.650 |
| disjoint | 10 | 3 | random | shenzhen | 0.340 | 8.650 |
| disjoint | 10 | 5 | random | metrla | 0.660 | 9.984 |
| disjoint | 10 | 5 | random | pems04 | 0.160 | 9.984 |
| disjoint | 10 | 5 | random | chengdu | 0.100 | 9.984 |
| disjoint | 10 | 5 | random | shenzhen | 0.340 | 9.984 |
| disjoint | 15 | 1 | own | metrla | 0.740 | 10.596 |
| disjoint | 15 | 1 | own | pems04 | 0.400 | 10.596 |
| disjoint | 15 | 1 | own | chengdu | 0.240 | 10.596 |
| disjoint | 15 | 1 | own | shenzhen | 0.280 | 10.596 |
| disjoint | 15 | 3 | own | metrla | 0.860 | 11.930 |
| disjoint | 15 | 3 | own | pems04 | 0.640 | 11.930 |
| disjoint | 15 | 3 | own | chengdu | 0.320 | 11.930 |
| disjoint | 15 | 3 | own | shenzhen | 0.520 | 11.930 |
| disjoint | 15 | 5 | own | metrla | 0.900 | 13.263 |
| disjoint | 15 | 5 | own | pems04 | 0.740 | 13.263 |
| disjoint | 15 | 5 | own | chengdu | 0.400 | 13.263 |
| disjoint | 15 | 5 | own | shenzhen | 0.600 | 13.263 |
| disjoint | 15 | 1 | pooled | metrla | 0.760 | 10.596 |
| disjoint | 15 | 1 | pooled | pems04 | 0.300 | 10.596 |
| disjoint | 15 | 1 | pooled | chengdu | 0.220 | 10.596 |
| disjoint | 15 | 1 | pooled | shenzhen | 0.360 | 10.596 |
| disjoint | 15 | 3 | pooled | metrla | 0.900 | 11.930 |
| disjoint | 15 | 3 | pooled | pems04 | 0.640 | 11.930 |
| disjoint | 15 | 3 | pooled | chengdu | 0.300 | 11.930 |
| disjoint | 15 | 3 | pooled | shenzhen | 0.540 | 11.930 |
| disjoint | 15 | 5 | pooled | metrla | 1.000 | 13.263 |
| disjoint | 15 | 5 | pooled | pems04 | 0.680 | 13.263 |
| disjoint | 15 | 5 | pooled | chengdu | 0.400 | 13.263 |
| disjoint | 15 | 5 | pooled | shenzhen | 0.680 | 13.263 |
| disjoint | 15 | 1 | pooled_own | metrla | 0.780 | 10.596 |
| disjoint | 15 | 1 | pooled_own | pems04 | 0.420 | 10.596 |
| disjoint | 15 | 1 | pooled_own | chengdu | 0.240 | 10.596 |
| disjoint | 15 | 1 | pooled_own | shenzhen | 0.260 | 10.596 |
| disjoint | 15 | 3 | pooled_own | metrla | 0.900 | 11.930 |
| disjoint | 15 | 3 | pooled_own | pems04 | 0.760 | 11.930 |
| disjoint | 15 | 3 | pooled_own | chengdu | 0.360 | 11.930 |
| disjoint | 15 | 3 | pooled_own | shenzhen | 0.460 | 11.930 |
| disjoint | 15 | 5 | pooled_own | metrla | 0.960 | 13.263 |
| disjoint | 15 | 5 | pooled_own | pems04 | 0.840 | 13.263 |
| disjoint | 15 | 5 | pooled_own | chengdu | 0.460 | 13.263 |
| disjoint | 15 | 5 | pooled_own | shenzhen | 0.660 | 13.263 |
| disjoint | 15 | 1 | observed_mean | metrla | 0.780 | 10.596 |
| disjoint | 15 | 1 | observed_mean | pems04 | 0.180 | 10.596 |
| disjoint | 15 | 1 | observed_mean | chengdu | 0.260 | 10.596 |
| disjoint | 15 | 1 | observed_mean | shenzhen | 0.380 | 10.596 |
| disjoint | 15 | 3 | observed_mean | metrla | 0.920 | 11.930 |
| disjoint | 15 | 3 | observed_mean | pems04 | 0.300 | 11.930 |
| disjoint | 15 | 3 | observed_mean | chengdu | 0.380 | 11.930 |
| disjoint | 15 | 3 | observed_mean | shenzhen | 0.580 | 11.930 |
| disjoint | 15 | 5 | observed_mean | metrla | 0.920 | 13.263 |
| disjoint | 15 | 5 | observed_mean | pems04 | 0.460 | 13.263 |
| disjoint | 15 | 5 | observed_mean | chengdu | 0.420 | 13.263 |
| disjoint | 15 | 5 | observed_mean | shenzhen | 0.620 | 13.263 |
| disjoint | 15 | 1 | random | metrla | 0.700 | 10.596 |
| disjoint | 15 | 1 | random | pems04 | 0.180 | 10.596 |
| disjoint | 15 | 1 | random | chengdu | 0.200 | 10.596 |
| disjoint | 15 | 1 | random | shenzhen | 0.260 | 10.596 |
| disjoint | 15 | 3 | random | metrla | 0.780 | 11.930 |
| disjoint | 15 | 3 | random | pems04 | 0.180 | 11.930 |
| disjoint | 15 | 3 | random | chengdu | 0.260 | 11.930 |
| disjoint | 15 | 3 | random | shenzhen | 0.300 | 11.930 |
| disjoint | 15 | 5 | random | metrla | 0.800 | 13.263 |
| disjoint | 15 | 5 | random | pems04 | 0.220 | 13.263 |
| disjoint | 15 | 5 | random | chengdu | 0.300 | 13.263 |
| disjoint | 15 | 5 | random | shenzhen | 0.300 | 13.263 |
| disjoint | 30 | 1 | own | metrla | 0.960 | 20.782 |
| disjoint | 30 | 1 | own | pems04 | 0.600 | 20.782 |
| disjoint | 30 | 1 | own | chengdu | 0.420 | 20.782 |
| disjoint | 30 | 1 | own | shenzhen | 0.440 | 20.782 |
| disjoint | 30 | 3 | own | metrla | 1.000 | 22.116 |
| disjoint | 30 | 3 | own | pems04 | 0.820 | 22.116 |
| disjoint | 30 | 3 | own | chengdu | 0.600 | 22.116 |
| disjoint | 30 | 3 | own | shenzhen | 0.520 | 22.116 |
| disjoint | 30 | 5 | own | metrla | 1.000 | 23.449 |
| disjoint | 30 | 5 | own | pems04 | 0.860 | 23.449 |
| disjoint | 30 | 5 | own | chengdu | 0.640 | 23.449 |
| disjoint | 30 | 5 | own | shenzhen | 0.620 | 23.449 |
| disjoint | 30 | 1 | pooled | metrla | 0.960 | 20.782 |
| disjoint | 30 | 1 | pooled | pems04 | 0.460 | 20.782 |
| disjoint | 30 | 1 | pooled | chengdu | 0.400 | 20.782 |
| disjoint | 30 | 1 | pooled | shenzhen | 0.480 | 20.782 |
| disjoint | 30 | 3 | pooled | metrla | 1.000 | 22.116 |
| disjoint | 30 | 3 | pooled | pems04 | 0.920 | 22.116 |
| disjoint | 30 | 3 | pooled | chengdu | 0.520 | 22.116 |
| disjoint | 30 | 3 | pooled | shenzhen | 0.620 | 22.116 |
| disjoint | 30 | 5 | pooled | metrla | 1.000 | 23.449 |
| disjoint | 30 | 5 | pooled | pems04 | 0.960 | 23.449 |
| disjoint | 30 | 5 | pooled | chengdu | 0.680 | 23.449 |
| disjoint | 30 | 5 | pooled | shenzhen | 0.780 | 23.449 |
| disjoint | 30 | 1 | pooled_own | metrla | 0.980 | 20.782 |
| disjoint | 30 | 1 | pooled_own | pems04 | 0.620 | 20.782 |
| disjoint | 30 | 1 | pooled_own | chengdu | 0.420 | 20.782 |
| disjoint | 30 | 1 | pooled_own | shenzhen | 0.440 | 20.782 |
| disjoint | 30 | 3 | pooled_own | metrla | 1.000 | 22.116 |
| disjoint | 30 | 3 | pooled_own | pems04 | 0.860 | 22.116 |
| disjoint | 30 | 3 | pooled_own | chengdu | 0.560 | 22.116 |
| disjoint | 30 | 3 | pooled_own | shenzhen | 0.540 | 22.116 |
| disjoint | 30 | 5 | pooled_own | metrla | 1.000 | 23.449 |
| disjoint | 30 | 5 | pooled_own | pems04 | 0.860 | 23.449 |
| disjoint | 30 | 5 | pooled_own | chengdu | 0.680 | 23.449 |
| disjoint | 30 | 5 | pooled_own | shenzhen | 0.640 | 23.449 |
| disjoint | 30 | 1 | observed_mean | metrla | 1.000 | 20.782 |
| disjoint | 30 | 1 | observed_mean | pems04 | 0.200 | 20.782 |
| disjoint | 30 | 1 | observed_mean | chengdu | 0.520 | 20.782 |
| disjoint | 30 | 1 | observed_mean | shenzhen | 0.560 | 20.782 |
| disjoint | 30 | 3 | observed_mean | metrla | 1.000 | 22.116 |
| disjoint | 30 | 3 | observed_mean | pems04 | 0.280 | 22.116 |
| disjoint | 30 | 3 | observed_mean | chengdu | 0.580 | 22.116 |
| disjoint | 30 | 3 | observed_mean | shenzhen | 0.740 | 22.116 |
| disjoint | 30 | 5 | observed_mean | metrla | 1.000 | 23.449 |
| disjoint | 30 | 5 | observed_mean | pems04 | 0.420 | 23.449 |
| disjoint | 30 | 5 | observed_mean | chengdu | 0.680 | 23.449 |
| disjoint | 30 | 5 | observed_mean | shenzhen | 0.860 | 23.449 |
| disjoint | 30 | 1 | random | metrla | 0.920 | 20.782 |
| disjoint | 30 | 1 | random | pems04 | 0.200 | 20.782 |
| disjoint | 30 | 1 | random | chengdu | 0.380 | 20.782 |
| disjoint | 30 | 1 | random | shenzhen | 0.320 | 20.782 |
| disjoint | 30 | 3 | random | metrla | 0.920 | 22.116 |
| disjoint | 30 | 3 | random | pems04 | 0.200 | 22.116 |
| disjoint | 30 | 3 | random | chengdu | 0.380 | 22.116 |
| disjoint | 30 | 3 | random | shenzhen | 0.320 | 22.116 |
| disjoint | 30 | 5 | random | metrla | 0.940 | 23.449 |
| disjoint | 30 | 5 | random | pems04 | 0.200 | 23.449 |
| disjoint | 30 | 5 | random | chengdu | 0.400 | 23.449 |
| disjoint | 30 | 5 | random | shenzhen | 0.380 | 23.449 |
| anchor | 5 | 1 | own | metrla | 0.440 | 3.997 |
| anchor | 5 | 1 | own | pems04 | 0.220 | 3.997 |
| anchor | 5 | 1 | own | chengdu | 0.060 | 3.997 |
| anchor | 5 | 1 | own | shenzhen | 0.080 | 3.997 |
| anchor | 5 | 3 | own | metrla | 0.520 | 5.330 |
| anchor | 5 | 3 | own | pems04 | 0.380 | 5.330 |
| anchor | 5 | 3 | own | chengdu | 0.100 | 5.330 |
| anchor | 5 | 3 | own | shenzhen | 0.140 | 5.330 |
| anchor | 5 | 5 | own | metrla | 0.600 | 6.663 |
| anchor | 5 | 5 | own | pems04 | 0.480 | 6.663 |
| anchor | 5 | 5 | own | chengdu | 0.220 | 6.663 |
| anchor | 5 | 5 | own | shenzhen | 0.180 | 6.663 |
| anchor | 5 | 1 | pooled | metrla | 0.380 | 3.997 |
| anchor | 5 | 1 | pooled | pems04 | 0.180 | 3.997 |
| anchor | 5 | 1 | pooled | chengdu | 0.040 | 3.997 |
| anchor | 5 | 1 | pooled | shenzhen | 0.040 | 3.997 |
| anchor | 5 | 3 | pooled | metrla | 0.720 | 5.330 |
| anchor | 5 | 3 | pooled | pems04 | 0.320 | 5.330 |
| anchor | 5 | 3 | pooled | chengdu | 0.120 | 5.330 |
| anchor | 5 | 3 | pooled | shenzhen | 0.080 | 5.330 |
| anchor | 5 | 5 | pooled | metrla | 0.820 | 6.663 |
| anchor | 5 | 5 | pooled | pems04 | 0.400 | 6.663 |
| anchor | 5 | 5 | pooled | chengdu | 0.160 | 6.663 |
| anchor | 5 | 5 | pooled | shenzhen | 0.180 | 6.663 |
| anchor | 5 | 1 | pooled_own | metrla | 0.420 | 3.997 |
| anchor | 5 | 1 | pooled_own | pems04 | 0.200 | 3.997 |
| anchor | 5 | 1 | pooled_own | chengdu | 0.040 | 3.997 |
| anchor | 5 | 1 | pooled_own | shenzhen | 0.080 | 3.997 |
| anchor | 5 | 3 | pooled_own | metrla | 0.560 | 5.330 |
| anchor | 5 | 3 | pooled_own | pems04 | 0.400 | 5.330 |
| anchor | 5 | 3 | pooled_own | chengdu | 0.120 | 5.330 |
| anchor | 5 | 3 | pooled_own | shenzhen | 0.120 | 5.330 |
| anchor | 5 | 5 | pooled_own | metrla | 0.620 | 6.663 |
| anchor | 5 | 5 | pooled_own | pems04 | 0.500 | 6.663 |
| anchor | 5 | 5 | pooled_own | chengdu | 0.220 | 6.663 |
| anchor | 5 | 5 | pooled_own | shenzhen | 0.200 | 6.663 |
| anchor | 5 | 1 | observed_mean | metrla | 0.400 | 3.997 |
| anchor | 5 | 1 | observed_mean | pems04 | 0.100 | 3.997 |
| anchor | 5 | 1 | observed_mean | chengdu | 0.040 | 3.997 |
| anchor | 5 | 1 | observed_mean | shenzhen | 0.080 | 3.997 |
| anchor | 5 | 3 | observed_mean | metrla | 0.640 | 5.330 |
| anchor | 5 | 3 | observed_mean | pems04 | 0.280 | 5.330 |
| anchor | 5 | 3 | observed_mean | chengdu | 0.120 | 5.330 |
| anchor | 5 | 3 | observed_mean | shenzhen | 0.140 | 5.330 |
| anchor | 5 | 5 | observed_mean | metrla | 0.800 | 6.663 |
| anchor | 5 | 5 | observed_mean | pems04 | 0.380 | 6.663 |
| anchor | 5 | 5 | observed_mean | chengdu | 0.140 | 6.663 |
| anchor | 5 | 5 | observed_mean | shenzhen | 0.220 | 6.663 |
| anchor | 5 | 1 | random | metrla | 0.380 | 3.997 |
| anchor | 5 | 1 | random | pems04 | 0.080 | 3.997 |
| anchor | 5 | 1 | random | chengdu | 0.040 | 3.997 |
| anchor | 5 | 1 | random | shenzhen | 0.060 | 3.997 |
| anchor | 5 | 3 | random | metrla | 0.420 | 5.330 |
| anchor | 5 | 3 | random | pems04 | 0.080 | 5.330 |
| anchor | 5 | 3 | random | chengdu | 0.040 | 5.330 |
| anchor | 5 | 3 | random | shenzhen | 0.080 | 5.330 |
| anchor | 5 | 5 | random | metrla | 0.500 | 6.663 |
| anchor | 5 | 5 | random | pems04 | 0.080 | 6.663 |
| anchor | 5 | 5 | random | chengdu | 0.060 | 6.663 |
| anchor | 5 | 5 | random | shenzhen | 0.080 | 6.663 |
| anchor | 10 | 1 | own | metrla | 0.620 | 7.299 |
| anchor | 10 | 1 | own | pems04 | 0.320 | 7.299 |
| anchor | 10 | 1 | own | chengdu | 0.200 | 7.299 |
| anchor | 10 | 1 | own | shenzhen | 0.120 | 7.299 |
| anchor | 10 | 3 | own | metrla | 0.740 | 8.633 |
| anchor | 10 | 3 | own | pems04 | 0.500 | 8.633 |
| anchor | 10 | 3 | own | chengdu | 0.340 | 8.633 |
| anchor | 10 | 3 | own | shenzhen | 0.240 | 8.633 |
| anchor | 10 | 5 | own | metrla | 0.800 | 9.966 |
| anchor | 10 | 5 | own | pems04 | 0.640 | 9.966 |
| anchor | 10 | 5 | own | chengdu | 0.400 | 9.966 |
| anchor | 10 | 5 | own | shenzhen | 0.300 | 9.966 |
| anchor | 10 | 1 | pooled | metrla | 0.660 | 7.299 |
| anchor | 10 | 1 | pooled | pems04 | 0.180 | 7.299 |
| anchor | 10 | 1 | pooled | chengdu | 0.140 | 7.299 |
| anchor | 10 | 1 | pooled | shenzhen | 0.120 | 7.299 |
| anchor | 10 | 3 | pooled | metrla | 0.840 | 8.633 |
| anchor | 10 | 3 | pooled | pems04 | 0.440 | 8.633 |
| anchor | 10 | 3 | pooled | chengdu | 0.180 | 8.633 |
| anchor | 10 | 3 | pooled | shenzhen | 0.180 | 8.633 |
| anchor | 10 | 5 | pooled | metrla | 0.920 | 9.966 |
| anchor | 10 | 5 | pooled | pems04 | 0.540 | 9.966 |
| anchor | 10 | 5 | pooled | chengdu | 0.260 | 9.966 |
| anchor | 10 | 5 | pooled | shenzhen | 0.360 | 9.966 |
| anchor | 10 | 1 | pooled_own | metrla | 0.720 | 7.299 |
| anchor | 10 | 1 | pooled_own | pems04 | 0.340 | 7.299 |
| anchor | 10 | 1 | pooled_own | chengdu | 0.160 | 7.299 |
| anchor | 10 | 1 | pooled_own | shenzhen | 0.120 | 7.299 |
| anchor | 10 | 3 | pooled_own | metrla | 0.740 | 8.633 |
| anchor | 10 | 3 | pooled_own | pems04 | 0.560 | 8.633 |
| anchor | 10 | 3 | pooled_own | chengdu | 0.340 | 8.633 |
| anchor | 10 | 3 | pooled_own | shenzhen | 0.240 | 8.633 |
| anchor | 10 | 5 | pooled_own | metrla | 0.800 | 9.966 |
| anchor | 10 | 5 | pooled_own | pems04 | 0.700 | 9.966 |
| anchor | 10 | 5 | pooled_own | chengdu | 0.420 | 9.966 |
| anchor | 10 | 5 | pooled_own | shenzhen | 0.300 | 9.966 |
| anchor | 10 | 1 | observed_mean | metrla | 0.720 | 7.299 |
| anchor | 10 | 1 | observed_mean | pems04 | 0.140 | 7.299 |
| anchor | 10 | 1 | observed_mean | chengdu | 0.180 | 7.299 |
| anchor | 10 | 1 | observed_mean | shenzhen | 0.200 | 7.299 |
| anchor | 10 | 3 | observed_mean | metrla | 0.840 | 8.633 |
| anchor | 10 | 3 | observed_mean | pems04 | 0.260 | 8.633 |
| anchor | 10 | 3 | observed_mean | chengdu | 0.220 | 8.633 |
| anchor | 10 | 3 | observed_mean | shenzhen | 0.300 | 8.633 |
| anchor | 10 | 5 | observed_mean | metrla | 0.900 | 9.966 |
| anchor | 10 | 5 | observed_mean | pems04 | 0.420 | 9.966 |
| anchor | 10 | 5 | observed_mean | chengdu | 0.260 | 9.966 |
| anchor | 10 | 5 | observed_mean | shenzhen | 0.400 | 9.966 |
| anchor | 10 | 1 | random | metrla | 0.520 | 7.299 |
| anchor | 10 | 1 | random | pems04 | 0.120 | 7.299 |
| anchor | 10 | 1 | random | chengdu | 0.140 | 7.299 |
| anchor | 10 | 1 | random | shenzhen | 0.140 | 7.299 |
| anchor | 10 | 3 | random | metrla | 0.600 | 8.633 |
| anchor | 10 | 3 | random | pems04 | 0.140 | 8.633 |
| anchor | 10 | 3 | random | chengdu | 0.140 | 8.633 |
| anchor | 10 | 3 | random | shenzhen | 0.140 | 8.633 |
| anchor | 10 | 5 | random | metrla | 0.660 | 9.966 |
| anchor | 10 | 5 | random | pems04 | 0.140 | 9.966 |
| anchor | 10 | 5 | random | chengdu | 0.200 | 9.966 |
| anchor | 10 | 5 | random | shenzhen | 0.160 | 9.966 |
| anchor | 15 | 1 | own | metrla | 0.780 | 10.478 |
| anchor | 15 | 1 | own | pems04 | 0.460 | 10.478 |
| anchor | 15 | 1 | own | chengdu | 0.120 | 10.478 |
| anchor | 15 | 1 | own | shenzhen | 0.180 | 10.478 |
| anchor | 15 | 3 | own | metrla | 0.880 | 11.811 |
| anchor | 15 | 3 | own | pems04 | 0.600 | 11.811 |
| anchor | 15 | 3 | own | chengdu | 0.200 | 11.811 |
| anchor | 15 | 3 | own | shenzhen | 0.260 | 11.811 |
| anchor | 15 | 5 | own | metrla | 0.940 | 13.145 |
| anchor | 15 | 5 | own | pems04 | 0.640 | 13.145 |
| anchor | 15 | 5 | own | chengdu | 0.300 | 13.145 |
| anchor | 15 | 5 | own | shenzhen | 0.420 | 13.145 |
| anchor | 15 | 1 | pooled | metrla | 0.820 | 10.478 |
| anchor | 15 | 1 | pooled | pems04 | 0.240 | 10.478 |
| anchor | 15 | 1 | pooled | chengdu | 0.120 | 10.478 |
| anchor | 15 | 1 | pooled | shenzhen | 0.280 | 10.478 |
| anchor | 15 | 3 | pooled | metrla | 0.980 | 11.811 |
| anchor | 15 | 3 | pooled | pems04 | 0.500 | 11.811 |
| anchor | 15 | 3 | pooled | chengdu | 0.160 | 11.811 |
| anchor | 15 | 3 | pooled | shenzhen | 0.400 | 11.811 |
| anchor | 15 | 5 | pooled | metrla | 1.000 | 13.145 |
| anchor | 15 | 5 | pooled | pems04 | 0.640 | 13.145 |
| anchor | 15 | 5 | pooled | chengdu | 0.220 | 13.145 |
| anchor | 15 | 5 | pooled | shenzhen | 0.500 | 13.145 |
| anchor | 15 | 1 | pooled_own | metrla | 0.800 | 10.478 |
| anchor | 15 | 1 | pooled_own | pems04 | 0.480 | 10.478 |
| anchor | 15 | 1 | pooled_own | chengdu | 0.120 | 10.478 |
| anchor | 15 | 1 | pooled_own | shenzhen | 0.200 | 10.478 |
| anchor | 15 | 3 | pooled_own | metrla | 0.920 | 11.811 |
| anchor | 15 | 3 | pooled_own | pems04 | 0.620 | 11.811 |
| anchor | 15 | 3 | pooled_own | chengdu | 0.200 | 11.811 |
| anchor | 15 | 3 | pooled_own | shenzhen | 0.340 | 11.811 |
| anchor | 15 | 5 | pooled_own | metrla | 0.940 | 13.145 |
| anchor | 15 | 5 | pooled_own | pems04 | 0.700 | 13.145 |
| anchor | 15 | 5 | pooled_own | chengdu | 0.340 | 13.145 |
| anchor | 15 | 5 | pooled_own | shenzhen | 0.440 | 13.145 |
| anchor | 15 | 1 | observed_mean | metrla | 0.820 | 10.478 |
| anchor | 15 | 1 | observed_mean | pems04 | 0.140 | 10.478 |
| anchor | 15 | 1 | observed_mean | chengdu | 0.140 | 10.478 |
| anchor | 15 | 1 | observed_mean | shenzhen | 0.260 | 10.478 |
| anchor | 15 | 3 | observed_mean | metrla | 0.940 | 11.811 |
| anchor | 15 | 3 | observed_mean | pems04 | 0.220 | 11.811 |
| anchor | 15 | 3 | observed_mean | chengdu | 0.240 | 11.811 |
| anchor | 15 | 3 | observed_mean | shenzhen | 0.420 | 11.811 |
| anchor | 15 | 5 | observed_mean | metrla | 0.960 | 13.145 |
| anchor | 15 | 5 | observed_mean | pems04 | 0.360 | 13.145 |
| anchor | 15 | 5 | observed_mean | chengdu | 0.320 | 13.145 |
| anchor | 15 | 5 | observed_mean | shenzhen | 0.560 | 13.145 |
| anchor | 15 | 1 | random | metrla | 0.720 | 10.478 |
| anchor | 15 | 1 | random | pems04 | 0.120 | 10.478 |
| anchor | 15 | 1 | random | chengdu | 0.120 | 10.478 |
| anchor | 15 | 1 | random | shenzhen | 0.160 | 10.478 |
| anchor | 15 | 3 | random | metrla | 0.820 | 11.811 |
| anchor | 15 | 3 | random | pems04 | 0.120 | 11.811 |
| anchor | 15 | 3 | random | chengdu | 0.120 | 11.811 |
| anchor | 15 | 3 | random | shenzhen | 0.160 | 11.811 |
| anchor | 15 | 5 | random | metrla | 0.860 | 13.145 |
| anchor | 15 | 5 | random | pems04 | 0.140 | 13.145 |
| anchor | 15 | 5 | random | chengdu | 0.160 | 13.145 |
| anchor | 15 | 5 | random | shenzhen | 0.200 | 13.145 |
| anchor | 30 | 1 | own | metrla | 0.960 | 20.624 |
| anchor | 30 | 1 | own | pems04 | 0.640 | 20.624 |
| anchor | 30 | 1 | own | chengdu | 0.440 | 20.624 |
| anchor | 30 | 1 | own | shenzhen | 0.460 | 20.624 |
| anchor | 30 | 3 | own | metrla | 1.000 | 21.958 |
| anchor | 30 | 3 | own | pems04 | 0.900 | 21.958 |
| anchor | 30 | 3 | own | chengdu | 0.560 | 21.958 |
| anchor | 30 | 3 | own | shenzhen | 0.600 | 21.958 |
| anchor | 30 | 5 | own | metrla | 1.000 | 23.291 |
| anchor | 30 | 5 | own | pems04 | 0.960 | 23.291 |
| anchor | 30 | 5 | own | chengdu | 0.600 | 23.291 |
| anchor | 30 | 5 | own | shenzhen | 0.660 | 23.291 |
| anchor | 30 | 1 | pooled | metrla | 0.960 | 20.624 |
| anchor | 30 | 1 | pooled | pems04 | 0.360 | 20.624 |
| anchor | 30 | 1 | pooled | chengdu | 0.400 | 20.624 |
| anchor | 30 | 1 | pooled | shenzhen | 0.520 | 20.624 |
| anchor | 30 | 3 | pooled | metrla | 1.000 | 21.958 |
| anchor | 30 | 3 | pooled | pems04 | 0.720 | 21.958 |
| anchor | 30 | 3 | pooled | chengdu | 0.480 | 21.958 |
| anchor | 30 | 3 | pooled | shenzhen | 0.640 | 21.958 |
| anchor | 30 | 5 | pooled | metrla | 1.000 | 23.291 |
| anchor | 30 | 5 | pooled | pems04 | 0.880 | 23.291 |
| anchor | 30 | 5 | pooled | chengdu | 0.540 | 23.291 |
| anchor | 30 | 5 | pooled | shenzhen | 0.740 | 23.291 |
| anchor | 30 | 1 | pooled_own | metrla | 0.960 | 20.624 |
| anchor | 30 | 1 | pooled_own | pems04 | 0.620 | 20.624 |
| anchor | 30 | 1 | pooled_own | chengdu | 0.460 | 20.624 |
| anchor | 30 | 1 | pooled_own | shenzhen | 0.520 | 20.624 |
| anchor | 30 | 3 | pooled_own | metrla | 0.980 | 21.958 |
| anchor | 30 | 3 | pooled_own | pems04 | 0.920 | 21.958 |
| anchor | 30 | 3 | pooled_own | chengdu | 0.540 | 21.958 |
| anchor | 30 | 3 | pooled_own | shenzhen | 0.620 | 21.958 |
| anchor | 30 | 5 | pooled_own | metrla | 1.000 | 23.291 |
| anchor | 30 | 5 | pooled_own | pems04 | 0.980 | 23.291 |
| anchor | 30 | 5 | pooled_own | chengdu | 0.600 | 23.291 |
| anchor | 30 | 5 | pooled_own | shenzhen | 0.720 | 23.291 |
| anchor | 30 | 1 | observed_mean | metrla | 1.000 | 20.624 |
| anchor | 30 | 1 | observed_mean | pems04 | 0.140 | 20.624 |
| anchor | 30 | 1 | observed_mean | chengdu | 0.500 | 20.624 |
| anchor | 30 | 1 | observed_mean | shenzhen | 0.580 | 20.624 |
| anchor | 30 | 3 | observed_mean | metrla | 1.000 | 21.958 |
| anchor | 30 | 3 | observed_mean | pems04 | 0.260 | 21.958 |
| anchor | 30 | 3 | observed_mean | chengdu | 0.580 | 21.958 |
| anchor | 30 | 3 | observed_mean | shenzhen | 0.660 | 21.958 |
| anchor | 30 | 5 | observed_mean | metrla | 1.000 | 23.291 |
| anchor | 30 | 5 | observed_mean | pems04 | 0.360 | 23.291 |
| anchor | 30 | 5 | observed_mean | chengdu | 0.620 | 23.291 |
| anchor | 30 | 5 | observed_mean | shenzhen | 0.760 | 23.291 |
| anchor | 30 | 1 | random | metrla | 0.980 | 20.624 |
| anchor | 30 | 1 | random | pems04 | 0.140 | 20.624 |
| anchor | 30 | 1 | random | chengdu | 0.380 | 20.624 |
| anchor | 30 | 1 | random | shenzhen | 0.420 | 20.624 |
| anchor | 30 | 3 | random | metrla | 0.980 | 21.958 |
| anchor | 30 | 3 | random | pems04 | 0.140 | 21.958 |
| anchor | 30 | 3 | random | chengdu | 0.380 | 21.958 |
| anchor | 30 | 3 | random | shenzhen | 0.480 | 21.958 |
| anchor | 30 | 5 | random | metrla | 0.980 | 23.291 |
| anchor | 30 | 5 | random | pems04 | 0.140 | 23.291 |
| anchor | 30 | 5 | random | chengdu | 0.400 | 23.291 |
| anchor | 30 | 5 | random | shenzhen | 0.480 | 23.291 |
