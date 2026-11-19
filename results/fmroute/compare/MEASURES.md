# fmroute: the measures of the frozen and the trained side, per regime

Test split, h = 12, MAE in the raw unit of the city, zero mask, targets whose window has a regime label. A value of the trained side, of the selector and of the mean is the mean over 3 seeds. The main pair of a city is the frozen setting and the trained model with the lowest validation MAE.

**Line of the plan (main pair, rule of the city):** fail. Cities that pass: 1. Cities where the selector is within 2 sigma_seed in every regime: 4. Cities where one model wins every regime: 5.

## The rule that the line reads

### metrla, absolute rule

Share of the targets: free 0.603, transition 0.378, congested 0.018.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | 1.4985 | 6.0825 | 4.3959 | 3.2857 |
| `chronos2_joint` | frozen | 1.4498 | 5.8643 | 4.3574 | 3.1731 |
| `261470bcc0` | trained | 1.6672 ± 0.0051 | 6.2518 ± 0.0044 | 7.4012 ± 0.0857 | 3.5063 ± 0.0012 |
| `stid_trueclock` | trained | 1.6105 ± 0.0059 | 6.3378 ± 0.0077 | 6.1203 ± 0.1117 | 3.4813 ± 0.0042 |

**Pair `chronos2_alone` and `261470bcc0`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.745 of the cells (0.788 of the targets). The selector gives 0.725 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.4985 | 1.4985 | 1.5177 | 1.5316 | 1.4972 | -0.0193 | -3.8 | 0.84 / 0.91 / 0.98 | 0.950 of 201 |
| transition | 6.0825 | 6.0825 | 6.0969 | 5.9516 | 6.0224 | -0.0144 | -3.3 | 0.91 / 0.97 / 1.04 | 0.739 of 207 |
| congested | 4.3959 | 4.3959 | 4.4187 | 5.5095 | 4.3729 | -0.0228 | -0.3 | 0.43 / 0.70 / 1.00 | 0.901 of 101 |
| labelled | 3.2857 | 3.2857 | 3.3032 | 3.2765 | 3.2618 | -0.0175 | -14.7 | 0.87 / 0.94 / 0.99 | 0.942 of 207 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.662 of the cells (0.675 of the targets). The selector gives 0.590 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.4985 | 1.4985 | 1.5190 | 1.5115 | 1.4916 | -0.0206 | -3.5 | 0.88 / 0.93 / 1.02 | 0.851 of 201 |
| transition | 6.0825 | 6.0825 | 6.2019 | 5.9934 | 6.0498 | -0.1193 | -15.5 | 0.89 / 0.96 / 1.02 | 0.821 of 207 |
| congested | 4.3959 | 4.3959 | 4.7038 | 5.0493 | 4.3432 | -0.3079 | -2.8 | 0.56 / 0.86 / 1.10 | 0.762 of 101 |
| labelled | 3.2857 | 3.2857 | 3.3489 | 3.2718 | 3.2683 | -0.0632 | -15.2 | 0.89 / 0.94 / 0.99 | 0.942 of 207 |

**Pair `chronos2_joint` and `261470bcc0`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.889 of the cells (0.947 of the targets). The selector gives 0.956 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.4498 | 1.4498 | 1.4515 | 1.5145 | 1.4498 | -0.0017 | -0.3 | 0.82 / 0.88 / 0.93 | 0.990 of 201 |
| transition | 5.8643 | 5.8643 | 5.8849 | 5.8691 | 5.8567 | -0.0205 | -4.6 | 0.89 / 0.94 / 0.99 | 0.918 of 207 |
| congested | 4.3574 | 4.3574 | 4.4063 | 5.5180 | 4.3461 | -0.0489 | -0.6 | 0.45 / 0.68 / 0.92 | 0.950 of 101 |
| labelled | 3.1731 | 3.1731 | 3.1828 | 3.2351 | 3.1700 | -0.0097 | -8.1 | 0.85 / 0.91 / 0.95 | 1.000 of 207 |

**Pair `chronos2_joint` and `stid_trueclock` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.853 of the cells (0.922 of the targets). The selector gives 0.929 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.4498 | 1.4498 | 1.4525 | 1.4947 | 1.4490 | -0.0027 | -0.5 | 0.86 / 0.90 / 0.96 | 0.955 of 201 |
| transition | 5.8643 | 5.8643 | 5.9143 | 5.9124 | 5.8611 | -0.0500 | -6.5 | 0.87 / 0.94 / 0.99 | 0.947 of 207 |
| congested | 4.3574 | 4.3574 | 4.4770 | 5.0501 | 4.3202 | -0.1196 | -1.1 | 0.55 / 0.84 / 1.06 | 0.842 of 101 |
| labelled | 3.1731 | 3.1731 | 3.1959 | 3.2310 | 3.1707 | -0.0227 | -5.5 | 0.86 / 0.92 / 0.95 | 1.000 of 207 |

### pemsbay, absolute rule

Share of the targets: free 0.846, transition 0.146, congested 0.008.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | 0.9030 | 5.7226 | 3.1712 | 1.6259 |
| `chronos2_joint` | frozen | 0.8751 | 5.4889 | 3.4464 | 1.5704 |
| `261470bcc0` | trained | 0.9953 ± 0.0020 | 5.9735 ± 0.0140 | 5.6436 ± 0.0966 | 1.7615 ± 0.0044 |
| `stid_trueclock` | trained | 0.9917 ± 0.0021 | 6.2264 ± 0.0200 | 4.1976 ± 0.0223 | 1.7831 ± 0.0025 |

**Pair `chronos2_alone` and `261470bcc0`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.821 of the cells (0.891 of the targets). The selector gives 0.886 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 0.9030 | 0.9030 | 0.9051 | 0.9087 | 0.9024 | -0.0021 | -1.1 | 0.83 / 0.92 / 0.98 | 0.954 of 325 |
| transition | 5.7226 | 5.7226 | 5.7043 | 5.5967 | 5.6308 | 0.0182 | 1.3 | 0.87 / 0.97 / 1.09 | 0.617 of 321 |
| congested | 3.1712 | 3.1712 | 3.1953 | 4.0411 | 3.1370 | -0.0241 | -0.2 | 0.36 / 0.62 / 1.13 | 0.850 of 140 |
| labelled | 1.6259 | 1.6259 | 1.6252 | 1.6197 | 1.6116 | 0.0007 | 0.2 | 0.86 / 0.94 / 0.99 | 0.957 of 325 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.851 of the cells (0.938 of the targets). The selector gives 0.937 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 0.9030 | 0.9030 | 0.9040 | 0.9090 | 0.9022 | -0.0010 | -0.5 | 0.86 / 0.92 / 0.97 | 0.966 of 325 |
| transition | 5.7226 | 5.7226 | 5.7175 | 5.7489 | 5.6932 | 0.0051 | 0.3 | 0.82 / 0.94 / 1.03 | 0.826 of 321 |
| congested | 3.1712 | 3.1712 | 3.1373 | 3.4165 | 2.9959 | 0.0339 | 1.5 | 0.47 / 0.90 / 1.53 | 0.607 of 140 |
| labelled | 1.6259 | 1.6259 | 1.6257 | 1.6368 | 1.6194 | 0.0002 | 0.1 | 0.85 / 0.92 / 0.96 | 0.966 of 325 |

**Pair `chronos2_joint` and `261470bcc0` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.898 of the cells (0.978 of the targets). The selector gives 0.983 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 0.8751 | 0.8751 | 0.8752 | 0.9004 | 0.8750 | -0.0002 | -0.1 | 0.81 / 0.89 / 0.94 | 1.000 of 325 |
| transition | 5.4889 | 5.4889 | 5.4958 | 5.5216 | 5.4655 | -0.0069 | -0.5 | 0.83 / 0.93 / 1.03 | 0.804 of 321 |
| congested | 3.4464 | 3.4464 | 3.4583 | 4.2016 | 3.4048 | -0.0119 | -0.1 | 0.42 / 0.69 / 1.08 | 0.843 of 140 |
| labelled | 1.5704 | 1.5704 | 1.5717 | 1.6031 | 1.5667 | -0.0013 | -0.3 | 0.83 / 0.90 / 0.95 | 1.000 of 325 |

**Pair `chronos2_joint` and `stid_trueclock`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.893 of the cells (0.982 of the targets). The selector gives 0.988 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: False; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 0.8751 | 0.8751 | 0.8750 | 0.8985 | 0.8748 | 0.0000 | 0.0 | 0.83 / 0.89 / 0.94 | 0.985 of 325 |
| transition | 5.4889 | 5.4889 | 5.4950 | 5.6397 | 5.4793 | -0.0061 | -0.3 | 0.80 / 0.90 / 1.00 | 0.903 of 321 |
| congested | 3.4464 | 3.4464 | 3.3338 | 3.5510 | 3.1589 | 0.1125 | 5.0 | 0.48 / 0.98 / 1.63 | 0.514 of 140 |
| labelled | 1.5704 | 1.5704 | 1.5703 | 1.6132 | 1.5664 | 0.0001 | 0.0 | 0.83 / 0.89 / 0.94 | 0.994 of 325 |

### pems08, absolute rule

Share of the targets: free 0.901, transition 0.097, congested 0.002.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | 14.0950 | 24.3685 | 27.1845 | 15.1200 |
| `chronos2_joint` | frozen | 13.5771 | 23.7645 | 27.0276 | 14.5944 |
| `43d20fa260` | trained | 14.1691 ± 0.0208 | 25.8523 ± 0.0350 | 28.9562 ± 0.0850 | 15.3347 ± 0.0154 |
| `stid_trueclock` | trained | 13.6453 ± 0.0207 | 25.4965 ± 0.0197 | 31.2153 ± 0.0594 | 14.8324 ± 0.0172 |

**Pair `chronos2_alone` and `43d20fa260`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.804 of the cells (0.816 of the targets). The selector gives 0.658 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: False; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 14.0950 | 14.0950 | 13.6425 | 13.4525 | 13.5919 | 0.4524 | 21.8 | 0.91 / 1.00 / 1.35 | 0.512 of 170 |
| transition | 24.3685 | 24.3685 | 24.4074 | 24.4428 | 24.2321 | -0.0389 | -1.1 | 0.86 / 0.98 / 1.47 | 0.586 of 152 |
| congested | 27.1845 | 27.1845 | 27.1864 | 27.4440 | 26.8398 | -0.0019 | -0.0 | 0.80 / 0.96 / 1.13 | 0.688 of 16 |
| labelled | 15.1200 | 15.1200 | 14.7163 | 14.5490 | 14.6529 | 0.4037 | 26.2 | 0.90 / 0.99 / 1.35 | 0.565 of 170 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `stid_trueclock`. Validation and test winner agree in 0.776 of the cells (0.799 of the targets). The selector gives 0.497 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: False; one model wins every regime: False.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 13.6453 | 13.6453 | 13.2970 | 13.2087 | 13.2322 | 0.3483 | 16.8 | 0.93 / 1.01 / 1.73 | 0.424 of 170 |
| transition | 25.4965 | 24.3685 | 24.4408 | 24.2130 | 24.1125 | 1.0557 | 53.5 | 0.80 / 0.99 / 1.97 | 0.566 of 152 |
| congested | 31.2153 | 27.1845 | 28.3555 | 28.2126 | 26.9327 | 2.8598 | 48.1 | 0.63 / 0.84 / 1.02 | 0.750 of 16 |
| labelled | 14.8324 | 14.8324 | 14.4105 | 14.3085 | 14.3175 | 0.4219 | 24.6 | 0.93 / 1.00 / 1.73 | 0.488 of 170 |

**Pair `chronos2_joint` and `43d20fa260`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.906 of the cells (0.965 of the targets). The selector gives 0.816 of the targets to the frozen model. City pass: True; within 2 sigma_seed in every regime: False; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 13.5771 | 13.5771 | 13.2177 | 13.2508 | 13.2041 | 0.3594 | 17.3 | 0.87 / 0.96 / 1.32 | 0.806 of 170 |
| transition | 23.7645 | 23.7645 | 23.8307 | 24.1214 | 23.7134 | -0.0662 | -1.9 | 0.83 / 0.96 / 1.25 | 0.678 of 152 |
| congested | 27.0276 | 27.0276 | 27.3629 | 27.3116 | 26.5606 | -0.3353 | -3.9 | 0.84 / 0.96 / 1.16 | 0.688 of 16 |
| labelled | 14.5944 | 14.5944 | 14.2778 | 14.3359 | 14.2526 | 0.3167 | 20.5 | 0.88 / 0.95 / 1.32 | 0.829 of 170 |

**Pair `chronos2_joint` and `stid_trueclock` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.865 of the cells (0.914 of the targets). The selector gives 0.746 of the targets to the frozen model. City pass: True; within 2 sigma_seed in every regime: False; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 13.5771 | 13.5771 | 12.9373 | 13.0186 | 12.9064 | 0.6398 | 30.9 | 0.89 / 0.97 / 1.69 | 0.712 of 170 |
| transition | 23.7645 | 23.7645 | 23.8435 | 23.8858 | 23.6593 | -0.0790 | -4.0 | 0.79 / 0.96 / 1.67 | 0.678 of 152 |
| congested | 27.0276 | 27.0276 | 27.4312 | 28.1311 | 26.7465 | -0.4036 | -6.8 | 0.69 / 0.86 / 1.06 | 0.750 of 16 |
| labelled | 14.5944 | 14.5944 | 14.0266 | 14.1053 | 13.9796 | 0.5678 | 33.0 | 0.89 / 0.96 / 1.69 | 0.782 of 170 |

### chengdu, relative rule

Share of the targets: free 0.207, transition 0.788, congested 0.005.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | 1.9354 | 2.3596 | 2.7576 | 2.2740 |
| `chronos2_joint` | frozen | 1.9181 | 2.2905 | 2.6197 | 2.2153 |
| `59d2d9e09e` | trained | 2.0096 ± 0.0036 | 2.4312 ± 0.0051 | 3.9240 ± 0.0167 | 2.3518 ± 0.0044 |
| `stid_trueclock` | trained | 2.0526 ± 0.0032 | 2.4674 ± 0.0019 | 3.7085 ± 0.0274 | 2.3881 ± 0.0020 |

**Pair `chronos2_alone` and `59d2d9e09e`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.743 of the cells (0.762 of the targets). The selector gives 0.597 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: False; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.9354 | 1.9354 | 1.9307 | 1.9183 | 1.9214 | 0.0047 | 1.3 | 0.90 / 0.98 / 1.03 | 0.717 of 523 |
| transition | 2.3596 | 2.3596 | 2.3576 | 2.3100 | 2.3442 | 0.0020 | 0.4 | 0.91 / 0.99 / 1.02 | 0.666 of 524 |
| congested | 2.7576 | 2.7576 | 2.7149 | 3.0814 | 2.6447 | 0.0427 | 2.6 | 0.53 / 0.95 / 1.31 | 0.602 of 88 |
| labelled | 2.2740 | 2.2740 | 2.2712 | 2.2330 | 2.2584 | 0.0028 | 0.6 | 0.91 / 0.98 / 1.02 | 0.706 of 524 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.794 of the cells (0.795 of the targets). The selector gives 0.744 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.9354 | 1.9354 | 1.9359 | 1.9434 | 1.9289 | -0.0005 | -0.2 | 0.88 / 0.95 / 1.01 | 0.862 of 523 |
| transition | 2.3596 | 2.3596 | 2.3674 | 2.3289 | 2.3541 | -0.0078 | -4.1 | 0.90 / 0.97 / 1.01 | 0.844 of 524 |
| congested | 2.7576 | 2.7576 | 2.7205 | 2.9986 | 2.6248 | 0.0370 | 1.4 | 0.57 / 0.95 / 1.29 | 0.557 of 88 |
| labelled | 2.2740 | 2.2740 | 2.2800 | 2.2527 | 2.2676 | -0.0061 | -3.1 | 0.90 / 0.97 / 1.00 | 0.903 of 524 |

**Pair `chronos2_joint` and `59d2d9e09e` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.815 of the cells (0.864 of the targets). The selector gives 0.867 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.9181 | 1.9181 | 1.9184 | 1.9122 | 1.9095 | -0.0004 | -0.1 | 0.90 / 0.97 / 1.02 | 0.797 of 523 |
| transition | 2.2905 | 2.2905 | 2.2952 | 2.2807 | 2.2895 | -0.0047 | -0.9 | 0.88 / 0.96 / 0.99 | 0.954 of 524 |
| congested | 2.6197 | 2.6197 | 2.6116 | 3.0363 | 2.5716 | 0.0081 | 0.5 | 0.51 / 0.83 / 1.15 | 0.807 of 88 |
| labelled | 2.2153 | 2.2153 | 2.2190 | 2.2085 | 2.2125 | -0.0037 | -0.9 | 0.89 / 0.96 / 0.99 | 0.979 of 524 |

**Pair `chronos2_joint` and `stid_trueclock`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.898 of the cells (0.941 of the targets). The selector gives 0.946 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.9181 | 1.9181 | 1.9195 | 1.9378 | 1.9149 | -0.0014 | -0.4 | 0.87 / 0.95 / 1.00 | 0.908 of 523 |
| transition | 2.2905 | 2.2905 | 2.2929 | 2.2969 | 2.2903 | -0.0024 | -1.2 | 0.87 / 0.94 / 0.98 | 0.989 of 524 |
| congested | 2.6197 | 2.6197 | 2.6332 | 2.9433 | 2.5640 | -0.0136 | -0.5 | 0.53 / 0.81 / 1.16 | 0.739 of 88 |
| labelled | 2.2153 | 2.2153 | 2.2175 | 2.2260 | 2.2141 | -0.0022 | -1.1 | 0.87 / 0.94 / 0.98 | 0.996 of 524 |

### expytky, relative rule

Share of the targets: free 0.270, transition 0.709, congested 0.022.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | 4.2972 | 6.5156 | 5.4497 | 5.8942 |
| `chronos2_joint` | frozen | 3.9665 | 6.1704 | 5.9435 | 5.5711 |
| `261470bcc0` | trained | 4.9527 ± 0.0198 | 7.9244 ± 0.0258 | 12.6204 ± 0.2065 | 7.2249 ± 0.0221 |
| `stid_trueclock` | trained | 5.0181 ± 0.0095 | 7.9348 ± 0.0074 | 11.0597 ± 0.0312 | 7.2161 ± 0.0084 |

**Pair `chronos2_alone` and `261470bcc0`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.772 of the cells (0.762 of the targets). The selector gives 0.662 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 4.2972 | 4.2972 | 4.2971 | 4.4735 | 4.2573 | 0.0001 | 0.0 | 0.43 / 0.93 / 1.02 | 0.826 of 1728 |
| transition | 6.5156 | 6.5156 | 6.5980 | 6.9585 | 6.4881 | -0.0824 | -3.2 | 0.52 / 0.92 / 1.01 | 0.854 of 1837 |
| congested | 5.4497 | 5.4497 | 5.6443 | 8.3789 | 5.4216 | -0.1946 | -0.9 | 0.30 / 0.48 / 0.81 | 0.967 of 642 |
| labelled | 5.8942 | 5.8942 | 5.9569 | 6.3192 | 5.8634 | -0.0626 | -2.8 | 0.51 / 0.89 / 1.00 | 0.921 of 1842 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.631 of the cells (0.647 of the targets). The selector gives 0.577 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 4.2972 | 4.2972 | 4.4232 | 4.5092 | 4.2866 | -0.1260 | -13.3 | 0.45 / 0.91 / 0.99 | 0.934 of 1728 |
| transition | 6.5156 | 6.5156 | 6.7049 | 6.9518 | 6.4916 | -0.1893 | -25.5 | 0.52 / 0.91 / 1.01 | 0.868 of 1837 |
| congested | 5.4497 | 5.4497 | 6.8564 | 7.7623 | 5.4160 | -1.4067 | -45.1 | 0.32 / 0.60 / 0.90 | 0.953 of 642 |
| labelled | 5.8942 | 5.8942 | 6.0929 | 6.3107 | 5.8736 | -0.1987 | -23.6 | 0.51 / 0.88 / 0.99 | 0.932 of 1842 |

**Pair `chronos2_joint` and `261470bcc0`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.886 of the cells (0.901 of the targets). The selector gives 0.904 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 3.9665 | 3.9665 | 3.9857 | 4.3086 | 3.9660 | -0.0191 | -1.0 | 0.36 / 0.86 / 0.96 | 0.992 of 1728 |
| transition | 6.1704 | 6.1704 | 6.2425 | 6.8313 | 6.1696 | -0.0722 | -2.8 | 0.49 / 0.87 / 0.96 | 0.989 of 1837 |
| congested | 5.9435 | 5.9435 | 6.1998 | 8.7715 | 5.9149 | -0.2563 | -1.2 | 0.32 / 0.53 / 0.81 | 0.966 of 642 |
| labelled | 5.5711 | 5.5711 | 5.6330 | 6.1931 | 5.5699 | -0.0619 | -2.8 | 0.48 / 0.84 / 0.95 | 0.999 of 1842 |

**Pair `chronos2_joint` and `stid_trueclock` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.749 of the cells (0.788 of the targets). The selector gives 0.788 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 3.9665 | 3.9665 | 4.0402 | 4.3456 | 3.9661 | -0.0736 | -7.8 | 0.36 / 0.82 / 0.94 | 0.995 of 1728 |
| transition | 6.1704 | 6.1704 | 6.4334 | 6.8174 | 6.1691 | -0.2630 | -35.5 | 0.50 / 0.86 / 0.96 | 0.990 of 1837 |
| congested | 5.9435 | 5.9435 | 8.1897 | 8.0750 | 5.9023 | -2.2462 | -72.0 | 0.35 / 0.65 / 0.95 | 0.936 of 642 |
| labelled | 5.5711 | 5.5711 | 5.8261 | 6.1781 | 5.5692 | -0.2550 | -30.3 | 0.48 / 0.83 / 0.95 | 0.998 of 1842 |

## The other rule

### metrla, relative rule

Share of the targets: free 0.703, transition 0.277, congested 0.020.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | 1.6125 | 7.4427 | 4.5868 | 3.2857 |
| `chronos2_joint` | frozen | 1.5649 | 7.1574 | 4.5768 | 3.1731 |
| `261470bcc0` | trained | 1.7834 ± 0.0049 | 7.5782 ± 0.0073 | 7.7026 ± 0.0723 | 3.5063 ± 0.0012 |
| `stid_trueclock` | trained | 1.7282 ± 0.0061 | 7.7193 ± 0.0080 | 6.4525 ± 0.0942 | 3.4813 ± 0.0042 |

**Pair `chronos2_alone` and `261470bcc0`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.766 of the cells (0.810 of the targets). The selector gives 0.751 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: False; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.6125 | 1.6125 | 1.6314 | 1.6443 | 1.6115 | -0.0189 | -3.9 | 0.84 / 0.91 / 0.97 | 0.961 of 207 |
| transition | 7.4427 | 7.4427 | 7.4213 | 7.2448 | 7.3370 | 0.0214 | 2.9 | 0.91 / 0.98 / 1.05 | 0.686 of 207 |
| congested | 4.5868 | 4.5868 | 4.6028 | 5.7336 | 4.5681 | -0.0160 | -0.2 | 0.45 / 0.68 / 0.97 | 0.915 of 106 |
| labelled | 3.2857 | 3.2857 | 3.2934 | 3.2765 | 3.2554 | -0.0077 | -6.4 | 0.87 / 0.94 / 0.99 | 0.942 of 207 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.680 of the cells (0.703 of the targets). The selector gives 0.613 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.6125 | 1.6125 | 1.6319 | 1.6250 | 1.6067 | -0.0194 | -3.2 | 0.88 / 0.93 / 1.01 | 0.884 of 207 |
| transition | 7.4427 | 7.4427 | 7.5864 | 7.3089 | 7.3862 | -0.1438 | -17.9 | 0.89 / 0.97 / 1.03 | 0.754 of 207 |
| congested | 4.5868 | 4.5868 | 4.9809 | 5.2957 | 4.5497 | -0.3940 | -4.2 | 0.56 / 0.83 / 1.07 | 0.811 of 106 |
| labelled | 3.2857 | 3.2857 | 3.3471 | 3.2718 | 3.2653 | -0.0614 | -14.8 | 0.89 / 0.94 / 0.99 | 0.942 of 207 |

**Pair `chronos2_joint` and `261470bcc0`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.888 of the cells (0.950 of the targets). The selector gives 0.957 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.5649 | 1.5649 | 1.5659 | 1.6276 | 1.5648 | -0.0010 | -0.2 | 0.82 / 0.88 / 0.93 | 0.995 of 207 |
| transition | 7.1574 | 7.1574 | 7.1836 | 7.1356 | 7.1405 | -0.0261 | -3.6 | 0.89 / 0.95 / 1.00 | 0.879 of 207 |
| congested | 4.5768 | 4.5768 | 4.6261 | 5.7608 | 4.5678 | -0.0494 | -0.7 | 0.48 / 0.68 / 0.91 | 0.953 of 106 |
| labelled | 3.1731 | 3.1731 | 3.1820 | 3.2351 | 3.1682 | -0.0089 | -7.5 | 0.85 / 0.91 / 0.95 | 1.000 of 207 |

**Pair `chronos2_joint` and `stid_trueclock` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.848 of the cells (0.925 of the targets). The selector gives 0.930 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.5649 | 1.5649 | 1.5673 | 1.6089 | 1.5643 | -0.0024 | -0.4 | 0.87 / 0.90 / 0.96 | 0.976 of 207 |
| transition | 7.1574 | 7.1574 | 7.2319 | 7.2010 | 7.1503 | -0.0744 | -9.3 | 0.87 / 0.94 / 1.00 | 0.908 of 207 |
| congested | 4.5768 | 4.5768 | 4.7546 | 5.3135 | 4.5500 | -0.1778 | -1.9 | 0.57 / 0.81 / 1.02 | 0.877 of 106 |
| labelled | 3.1731 | 3.1731 | 3.1990 | 3.2310 | 3.1701 | -0.0259 | -6.2 | 0.86 / 0.92 / 0.95 | 1.000 of 207 |

### pemsbay, relative rule

Share of the targets: free 0.860, transition 0.129, congested 0.011.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | 0.9246 | 6.1701 | 3.1629 | 1.6259 |
| `chronos2_joint` | frozen | 0.8968 | 5.9005 | 3.4590 | 1.5704 |
| `261470bcc0` | trained | 1.0185 ± 0.0019 | 6.3916 ± 0.0141 | 5.5407 ± 0.0965 | 1.7615 ± 0.0044 |
| `stid_trueclock` | trained | 1.0152 ± 0.0021 | 6.6971 ± 0.0229 | 4.1958 ± 0.0125 | 1.7831 ± 0.0025 |

**Pair `chronos2_alone` and `261470bcc0`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.828 of the cells (0.896 of the targets). The selector gives 0.892 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: False; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 0.9246 | 0.9246 | 0.9267 | 0.9303 | 0.9239 | -0.0020 | -1.1 | 0.83 / 0.93 / 0.98 | 0.948 of 325 |
| transition | 6.1701 | 6.1701 | 6.1376 | 6.0146 | 6.0498 | 0.0326 | 2.3 | 0.87 / 0.98 / 1.10 | 0.583 of 321 |
| congested | 3.1629 | 3.1629 | 3.1912 | 3.9822 | 3.1340 | -0.0283 | -0.3 | 0.38 / 0.62 / 1.04 | 0.885 of 157 |
| labelled | 1.6259 | 1.6259 | 1.6237 | 1.6197 | 1.6094 | 0.0021 | 0.5 | 0.86 / 0.94 / 0.99 | 0.957 of 325 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.860 of the cells (0.946 of the targets). The selector gives 0.945 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 0.9246 | 0.9246 | 0.9253 | 0.9308 | 0.9239 | -0.0007 | -0.3 | 0.86 / 0.92 / 0.97 | 0.966 of 325 |
| transition | 6.1701 | 6.1701 | 6.1625 | 6.1927 | 6.1329 | 0.0076 | 0.3 | 0.82 / 0.94 / 1.04 | 0.807 of 321 |
| congested | 3.1629 | 3.1629 | 3.1418 | 3.4109 | 3.0226 | 0.0211 | 1.7 | 0.49 / 0.86 / 1.52 | 0.669 of 157 |
| labelled | 1.6259 | 1.6259 | 1.6252 | 1.6368 | 1.6188 | 0.0006 | 0.2 | 0.85 / 0.92 / 0.96 | 0.966 of 325 |

**Pair `chronos2_joint` and `261470bcc0` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.884 of the cells (0.974 of the targets). The selector gives 0.981 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 0.8968 | 0.8968 | 0.8970 | 0.9220 | 0.8968 | -0.0002 | -0.1 | 0.81 / 0.89 / 0.94 | 1.000 of 325 |
| transition | 5.9005 | 5.9005 | 5.9126 | 5.9253 | 5.8697 | -0.0121 | -0.9 | 0.84 / 0.94 / 1.04 | 0.788 of 321 |
| congested | 3.4590 | 3.4590 | 3.4771 | 4.1558 | 3.4218 | -0.0181 | -0.2 | 0.44 / 0.70 / 1.11 | 0.860 of 157 |
| labelled | 1.5704 | 1.5704 | 1.5724 | 1.6031 | 1.5660 | -0.0019 | -0.4 | 0.83 / 0.90 / 0.95 | 1.000 of 325 |

**Pair `chronos2_joint` and `stid_trueclock`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.898 of the cells (0.985 of the targets). The selector gives 0.989 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: False; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 0.8968 | 0.8968 | 0.8968 | 0.9204 | 0.8965 | 0.0000 | 0.0 | 0.83 / 0.89 / 0.94 | 0.988 of 325 |
| transition | 5.9005 | 5.9005 | 5.9037 | 6.0664 | 5.8881 | -0.0031 | -0.1 | 0.80 / 0.90 / 1.00 | 0.897 of 321 |
| congested | 3.4590 | 3.4590 | 3.3753 | 3.5526 | 3.2165 | 0.0837 | 6.7 | 0.50 / 0.94 / 1.62 | 0.567 of 157 |
| labelled | 1.5704 | 1.5704 | 1.5699 | 1.6132 | 1.5659 | 0.0006 | 0.2 | 0.83 / 0.89 / 0.94 | 0.994 of 325 |

### pems08, relative rule

Share of the targets: free 0.916, transition 0.081, congested 0.003.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | 14.0920 | 26.2909 | 26.4840 | 15.1200 |
| `chronos2_joint` | frozen | 13.5770 | 25.6223 | 26.5914 | 14.5944 |
| `43d20fa260` | trained | 14.1844 ± 0.0204 | 27.8294 ± 0.0411 | 28.1594 ± 0.0542 | 15.3347 ± 0.0154 |
| `stid_trueclock` | trained | 13.6690 ± 0.0212 | 27.3928 ± 0.0340 | 29.8660 ± 0.0932 | 14.8324 ± 0.0172 |

**Pair `chronos2_alone` and `43d20fa260`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.792 of the cells (0.822 of the targets). The selector gives 0.662 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: False; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 14.0920 | 14.0920 | 13.6461 | 13.4633 | 13.5998 | 0.4458 | 21.9 | 0.91 / 1.00 / 1.35 | 0.535 of 170 |
| transition | 26.2909 | 26.2909 | 26.3468 | 26.3401 | 26.1336 | -0.0559 | -1.4 | 0.84 / 0.99 / 1.77 | 0.579 of 152 |
| congested | 26.4840 | 26.4840 | 26.5584 | 26.7145 | 26.1331 | -0.0744 | -1.4 | 0.86 / 0.94 / 1.12 | 0.737 of 19 |
| labelled | 15.1200 | 15.1200 | 14.7165 | 14.5490 | 14.6554 | 0.4035 | 26.2 | 0.90 / 0.99 / 1.35 | 0.565 of 170 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `stid_trueclock`. Validation and test winner agree in 0.775 of the cells (0.804 of the targets). The selector gives 0.497 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: False; one model wins every regime: False.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 13.6690 | 13.6690 | 13.3113 | 13.2223 | 13.2464 | 0.3578 | 16.9 | 0.93 / 1.01 / 1.73 | 0.441 of 170 |
| transition | 27.3928 | 26.2909 | 26.3628 | 26.0721 | 25.9773 | 1.0300 | 30.3 | 0.81 / 0.99 / 2.89 | 0.546 of 152 |
| congested | 29.8660 | 26.4840 | 27.4460 | 27.3606 | 26.3710 | 2.4200 | 26.0 | 0.71 / 0.87 / 0.99 | 0.947 of 19 |
| labelled | 14.8324 | 14.8324 | 14.4138 | 14.3085 | 14.3199 | 0.4186 | 24.4 | 0.93 / 1.00 / 1.73 | 0.488 of 170 |

**Pair `chronos2_joint` and `43d20fa260`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.887 of the cells (0.963 of the targets). The selector gives 0.813 of the targets to the frozen model. City pass: True; within 2 sigma_seed in every regime: False; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 13.5770 | 13.5770 | 13.2237 | 13.2616 | 13.2107 | 0.3533 | 17.3 | 0.87 / 0.96 / 1.32 | 0.806 of 170 |
| transition | 25.6223 | 25.6223 | 25.7193 | 25.9896 | 25.5556 | -0.0970 | -2.4 | 0.82 / 0.96 / 1.48 | 0.658 of 152 |
| congested | 26.5914 | 26.5914 | 26.8640 | 26.7150 | 26.1502 | -0.2726 | -5.0 | 0.90 / 0.97 / 1.13 | 0.684 of 19 |
| labelled | 14.5944 | 14.5944 | 14.2796 | 14.3359 | 14.2523 | 0.3148 | 20.4 | 0.88 / 0.95 / 1.32 | 0.829 of 170 |

**Pair `chronos2_joint` and `stid_trueclock` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.855 of the cells (0.915 of the targets). The selector gives 0.748 of the targets to the frozen model. City pass: True; within 2 sigma_seed in every regime: False; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 13.5770 | 13.5770 | 12.9478 | 13.0322 | 12.9188 | 0.6292 | 29.7 | 0.89 / 0.97 / 1.69 | 0.724 of 170 |
| transition | 25.6223 | 25.6223 | 25.7233 | 25.7143 | 25.4952 | -0.1009 | -3.0 | 0.79 / 0.97 / 2.40 | 0.632 of 152 |
| congested | 26.5914 | 26.5914 | 27.2562 | 27.3486 | 26.2491 | -0.6649 | -7.1 | 0.69 / 0.93 / 1.05 | 0.737 of 19 |
| labelled | 14.5944 | 14.5944 | 14.0284 | 14.1053 | 13.9803 | 0.5660 | 32.9 | 0.89 / 0.96 / 1.69 | 0.782 of 170 |

### chengdu, absolute rule

Share of the targets: free 0.000, transition 0.190, congested 0.810.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | n/a | 2.8640 | 2.1359 | 2.2740 |
| `chronos2_joint` | frozen | n/a | 2.7998 | 2.0785 | 2.2153 |
| `59d2d9e09e` | trained | n/a ± nan | 2.9938 ± 0.0076 | 2.2016 ± 0.0047 | 2.3518 ± 0.0044 |
| `stid_trueclock` | trained | n/a ± nan | 3.0253 ± 0.0037 | 2.2390 ± 0.0016 | 2.3881 ± 0.0020 |

**Pair `chronos2_alone` and `59d2d9e09e`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.695 of the cells (0.747 of the targets). The selector gives 0.608 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| transition | 2.8640 | 2.8640 | 2.8694 | 2.8326 | 2.8543 | -0.0054 | -0.7 | 0.91 / 0.98 / 1.03 | 0.701 of 478 |
| congested | 2.1359 | 2.1359 | 2.1315 | 2.0927 | 2.1209 | 0.0043 | 0.9 | 0.90 / 0.98 / 1.02 | 0.661 of 513 |
| labelled | 2.2740 | 2.2740 | 2.2715 | 2.2330 | 2.2600 | 0.0025 | 0.6 | 0.91 / 0.98 / 1.02 | 0.706 of 524 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.754 of the cells (0.805 of the targets). The selector gives 0.772 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| transition | 2.8640 | 2.8640 | 2.8716 | 2.8535 | 2.8580 | -0.0076 | -2.1 | 0.90 / 0.97 / 1.02 | 0.803 of 478 |
| congested | 2.1359 | 2.1359 | 2.1395 | 2.1121 | 2.1315 | -0.0036 | -2.2 | 0.89 / 0.96 / 1.00 | 0.877 of 513 |
| labelled | 2.2740 | 2.2740 | 2.2783 | 2.2527 | 2.2693 | -0.0043 | -2.2 | 0.90 / 0.97 / 1.00 | 0.903 of 524 |

**Pair `chronos2_joint` and `59d2d9e09e` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.794 of the cells (0.877 of the targets). The selector gives 0.882 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| transition | 2.7998 | 2.7998 | 2.8104 | 2.8090 | 2.7957 | -0.0106 | -1.4 | 0.89 / 0.98 / 1.01 | 0.778 of 478 |
| congested | 2.0785 | 2.0785 | 2.0821 | 2.0679 | 2.0775 | -0.0036 | -0.8 | 0.88 / 0.96 / 0.99 | 0.963 of 513 |
| labelled | 2.2153 | 2.2153 | 2.2202 | 2.2085 | 2.2137 | -0.0050 | -1.1 | 0.89 / 0.96 / 0.99 | 0.979 of 524 |

**Pair `chronos2_joint` and `stid_trueclock`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.868 of the cells (0.950 of the targets). The selector gives 0.948 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| transition | 2.7998 | 2.7998 | 2.8076 | 2.8285 | 2.7974 | -0.0078 | -2.1 | 0.88 / 0.96 / 1.01 | 0.864 of 478 |
| congested | 2.0785 | 2.0785 | 2.0804 | 2.0850 | 2.0782 | -0.0020 | -1.2 | 0.86 / 0.94 / 0.98 | 0.986 of 513 |
| labelled | 2.2153 | 2.2153 | 2.2183 | 2.2260 | 2.2146 | -0.0031 | -1.6 | 0.87 / 0.94 / 0.98 | 0.996 of 524 |

### expytky, absolute rule

Share of the targets: free 0.003, transition 0.880, congested 0.117.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | 3.4852 | 6.1901 | 3.7346 | 5.8942 |
| `chronos2_joint` | frozen | 3.2299 | 5.8217 | 3.7499 | 5.5711 |
| `261470bcc0` | trained | 5.8274 ± 0.0500 | 7.2973 ± 0.0190 | 6.7166 ± 0.0490 | 7.2249 ± 0.0221 |
| `stid_trueclock` | trained | 4.8695 ± 0.0145 | 7.3421 ± 0.0085 | 6.3296 ± 0.0079 | 7.2161 ± 0.0084 |

**Pair `chronos2_alone` and `261470bcc0`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.769 of the cells (0.741 of the targets). The selector gives 0.633 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 3.4852 | 3.4852 | 3.5597 | 4.5126 | 3.4168 | -0.0745 | -1.5 | 0.33 / 0.93 / 1.15 | 0.738 of 130 |
| transition | 6.1901 | 6.1901 | 6.2416 | 6.5114 | 6.1634 | -0.0514 | -2.7 | 0.52 / 0.93 / 1.01 | 0.854 of 1815 |
| congested | 3.7346 | 3.7346 | 3.8063 | 4.9226 | 3.7292 | -0.0717 | -1.5 | 0.35 / 0.60 / 0.92 | 0.960 of 1057 |
| labelled | 5.8942 | 5.8942 | 5.9481 | 6.3192 | 5.8698 | -0.0539 | -2.4 | 0.51 / 0.89 / 1.00 | 0.921 of 1842 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.642 of the cells (0.638 of the targets). The selector gives 0.564 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 3.4852 | 3.4852 | 3.5859 | 4.0523 | 3.3935 | -0.1006 | -7.0 | 0.49 / 0.89 / 1.15 | 0.785 of 130 |
| transition | 6.1901 | 6.1901 | 6.3497 | 6.5239 | 6.1746 | -0.1595 | -18.8 | 0.52 / 0.92 / 1.00 | 0.906 of 1815 |
| congested | 3.7346 | 3.7346 | 4.1176 | 4.7676 | 3.7269 | -0.3830 | -48.8 | 0.35 / 0.68 / 0.94 | 0.949 of 1057 |
| labelled | 5.8942 | 5.8942 | 6.0798 | 6.3107 | 5.8794 | -0.1856 | -22.0 | 0.51 / 0.88 / 0.99 | 0.932 of 1842 |

**Pair `chronos2_joint` and `261470bcc0`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.875 of the cells (0.909 of the targets). The selector gives 0.911 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 3.2299 | 3.2299 | 3.2644 | 4.3853 | 3.1924 | -0.0345 | -0.7 | 0.22 / 0.85 / 1.07 | 0.815 of 130 |
| transition | 5.8217 | 5.8217 | 5.8689 | 6.3591 | 5.8216 | -0.0472 | -2.5 | 0.49 / 0.87 / 0.96 | 0.997 of 1815 |
| congested | 3.7499 | 3.7499 | 3.8394 | 4.9928 | 3.7452 | -0.0895 | -1.8 | 0.35 / 0.62 / 0.90 | 0.964 of 1057 |
| labelled | 5.5711 | 5.5711 | 5.6233 | 6.1931 | 5.5704 | -0.0521 | -2.4 | 0.48 / 0.84 / 0.95 | 0.999 of 1842 |

**Pair `chronos2_joint` and `stid_trueclock` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.716 of the cells (0.770 of the targets). The selector gives 0.771 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 3.2299 | 3.2299 | 3.2972 | 3.9296 | 3.1822 | -0.0673 | -4.7 | 0.38 / 0.83 / 1.06 | 0.838 of 130 |
| transition | 5.8217 | 5.8217 | 6.0367 | 6.3673 | 5.8211 | -0.2150 | -25.3 | 0.50 / 0.86 / 0.95 | 0.996 of 1815 |
| congested | 3.7499 | 3.7499 | 4.3368 | 4.8150 | 3.7421 | -0.5870 | -74.7 | 0.37 / 0.70 / 0.94 | 0.941 of 1057 |
| labelled | 5.5711 | 5.5711 | 5.8293 | 6.1781 | 5.5695 | -0.2582 | -30.7 | 0.48 / 0.83 / 0.95 | 0.998 of 1842 |
