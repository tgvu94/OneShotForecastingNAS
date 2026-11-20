# fmroute: the measures of the frozen and the trained side, per regime

Test split, h = 12, MAE in the raw unit of the city, zero mask, targets whose window has a regime label. A value of the trained side, of the selector and of the mean is the mean over 3 seeds. The main pair of a city is the frozen setting and the trained model with the lowest validation MAE.

**Line of the plan (main pair, rule of the city):** not read: the line needs five cities. Cities that pass: 0. Cities where the selector is within 2 sigma_seed in every regime: 1. Cities where one model wins every regime: 1.

## The rule that the line reads

### metrla, absolute rule

Share of the targets: free 0.603, transition 0.378, congested 0.018.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | 1.4985 | 6.0825 | 4.3959 | 3.2857 |
| `chronos2_joint` | frozen | 1.4498 | 5.8643 | 4.3574 | 3.1731 |
| `261470bcc0` | trained | 1.6648 ± 0.0068 | 6.2579 ± 0.0068 | 7.5721 ± 0.2919 | 3.5102 ± 0.0037 |
| `stid_trueclock` | trained | 1.5859 ± 0.0047 | 6.2794 ± 0.0270 | 6.1996 ± 0.0652 | 3.4458 ± 0.0086 |

**Pair `chronos2_alone` and `261470bcc0`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.753 of the cells (0.792 of the targets). The selector gives 0.735 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.4985 | 1.4985 | 1.5164 | 1.5302 | 1.4974 | -0.0180 | -2.7 | 0.83 / 0.91 / 0.98 | 0.955 of 201 |
| transition | 6.0825 | 6.0825 | 6.1050 | 5.9467 | 6.0237 | -0.0224 | -3.3 | 0.91 / 0.97 / 1.04 | 0.749 of 207 |
| congested | 4.3959 | 4.3959 | 4.4197 | 5.5832 | 4.3782 | -0.0239 | -0.1 | 0.41 / 0.68 / 0.98 | 0.921 of 101 |
| labelled | 3.2857 | 3.2857 | 3.3055 | 3.2751 | 3.2625 | -0.0198 | -5.3 | 0.87 / 0.94 / 0.99 | 0.937 of 207 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.632 of the cells (0.624 of the targets). The selector gives 0.517 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.4985 | 1.4985 | 1.5165 | 1.5003 | 1.4890 | -0.0181 | -3.9 | 0.90 / 0.94 / 1.03 | 0.816 of 201 |
| transition | 6.0825 | 6.0825 | 6.1954 | 5.9516 | 6.0406 | -0.1129 | -4.2 | 0.92 / 0.97 / 1.03 | 0.763 of 207 |
| congested | 4.3959 | 4.3959 | 4.4726 | 5.0607 | 4.3349 | -0.0768 | -1.2 | 0.54 / 0.82 / 1.15 | 0.782 of 101 |
| labelled | 3.2857 | 3.2857 | 3.3408 | 3.2494 | 3.2630 | -0.0550 | -6.4 | 0.91 / 0.95 / 1.00 | 0.903 of 207 |

**Pair `chronos2_joint` and `261470bcc0`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.896 of the cells (0.956 of the targets). The selector gives 0.966 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.4498 | 1.4498 | 1.4514 | 1.5134 | 1.4497 | -0.0016 | -0.2 | 0.81 / 0.88 / 0.93 | 0.990 of 201 |
| transition | 5.8643 | 5.8643 | 5.8793 | 5.8638 | 5.8556 | -0.0150 | -2.2 | 0.89 / 0.94 / 1.00 | 0.928 of 207 |
| congested | 4.3574 | 4.3574 | 4.4099 | 5.5878 | 4.3444 | -0.0524 | -0.2 | 0.42 / 0.66 / 0.93 | 0.960 of 101 |
| labelled | 3.1731 | 3.1731 | 3.1807 | 3.2337 | 3.1695 | -0.0076 | -2.0 | 0.85 / 0.91 / 0.95 | 1.000 of 207 |

**Pair `chronos2_joint` and `stid_trueclock` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.793 of the cells (0.861 of the targets). The selector gives 0.880 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.4498 | 1.4498 | 1.4523 | 1.4837 | 1.4483 | -0.0025 | -0.5 | 0.88 / 0.91 / 0.98 | 0.940 of 201 |
| transition | 5.8643 | 5.8643 | 5.9467 | 5.8736 | 5.8581 | -0.0823 | -3.1 | 0.88 / 0.94 / 1.00 | 0.903 of 207 |
| congested | 4.3574 | 4.3574 | 4.3750 | 5.0618 | 4.3122 | -0.0176 | -0.3 | 0.54 / 0.81 / 1.15 | 0.802 of 101 |
| labelled | 3.1731 | 3.1731 | 3.2061 | 3.2099 | 3.1690 | -0.0330 | -3.8 | 0.87 / 0.93 / 0.96 | 0.990 of 207 |

## The other rule

### metrla, relative rule

Share of the targets: free 0.703, transition 0.277, congested 0.020.

| Model | Side | free | transition | congested | labelled |
|---|---|---|---|---|---|
| `chronos2_alone` | frozen | 1.6125 | 7.4427 | 4.5868 | 3.2857 |
| `chronos2_joint` | frozen | 1.5649 | 7.1574 | 4.5768 | 3.1731 |
| `261470bcc0` | trained | 1.7801 ± 0.0080 | 7.5882 ± 0.0107 | 7.8773 ± 0.3060 | 3.5102 ± 0.0037 |
| `stid_trueclock` | trained | 1.7032 ± 0.0050 | 7.6505 ± 0.0395 | 6.5082 ± 0.0591 | 3.4458 ± 0.0086 |

**Pair `chronos2_alone` and `261470bcc0`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.773 of the cells (0.819 of the targets). The selector gives 0.765 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.6125 | 1.6125 | 1.6287 | 1.6424 | 1.6116 | -0.0161 | -2.0 | 0.85 / 0.91 / 0.98 | 0.966 of 207 |
| transition | 7.4427 | 7.4427 | 7.4291 | 7.2390 | 7.3396 | 0.0136 | 1.3 | 0.91 / 0.98 / 1.05 | 0.686 of 207 |
| congested | 4.5868 | 4.5868 | 4.6053 | 5.8094 | 4.5698 | -0.0184 | -0.1 | 0.44 / 0.68 / 0.97 | 0.925 of 106 |
| labelled | 3.2857 | 3.2857 | 3.2937 | 3.2751 | 3.2562 | -0.0080 | -2.1 | 0.87 / 0.94 / 0.99 | 0.937 of 207 |

**Pair `chronos2_alone` and `stid_trueclock`.** Better single model: `chronos2_alone`. Validation and test winner agree in 0.641 of the cells (0.650 of the targets). The selector gives 0.546 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.6125 | 1.6125 | 1.6304 | 1.6134 | 1.6041 | -0.0179 | -3.6 | 0.90 / 0.95 / 1.02 | 0.836 of 207 |
| transition | 7.4427 | 7.4427 | 7.5716 | 7.2573 | 7.3723 | -0.1289 | -3.3 | 0.91 / 0.98 / 1.04 | 0.696 of 207 |
| congested | 4.5868 | 4.5868 | 4.6486 | 5.2952 | 4.5437 | -0.0618 | -1.0 | 0.53 / 0.81 / 1.13 | 0.792 of 106 |
| labelled | 3.2857 | 3.2857 | 3.3352 | 3.2494 | 3.2595 | -0.0495 | -5.8 | 0.91 / 0.95 / 1.00 | 0.903 of 207 |

**Pair `chronos2_joint` and `261470bcc0`.** Better single model: `chronos2_joint`. Validation and test winner agree in 0.888 of the cells (0.950 of the targets). The selector gives 0.957 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.5649 | 1.5649 | 1.5657 | 1.6260 | 1.5648 | -0.0008 | -0.1 | 0.82 / 0.88 / 0.94 | 0.990 of 207 |
| transition | 7.1574 | 7.1574 | 7.1869 | 7.1293 | 7.1395 | -0.0295 | -2.7 | 0.89 / 0.95 / 1.01 | 0.884 of 207 |
| congested | 4.5768 | 4.5768 | 4.6141 | 5.8328 | 4.5655 | -0.0373 | -0.1 | 0.46 / 0.66 / 0.90 | 0.962 of 106 |
| labelled | 3.1731 | 3.1731 | 3.1826 | 3.2337 | 3.1679 | -0.0095 | -2.6 | 0.85 / 0.91 / 0.95 | 1.000 of 207 |

**Pair `chronos2_joint` and `stid_trueclock` (main pair).** Better single model: `chronos2_joint`. Validation and test winner agree in 0.779 of the cells (0.874 of the targets). The selector gives 0.896 of the targets to the frozen model. City pass: False; within 2 sigma_seed in every regime: True; one model wins every regime: True.

| Scope | Better single | Lower of the two | Selector | Mean of forecasts | Oracle | Gain | Gain in sigma_seed | Ratio per sensor, p10 / p50 / p90 | Sensors with ratio below 1 |
|---|---|---|---|---|---|---|---|---|---|
| free | 1.5649 | 1.5649 | 1.5666 | 1.5976 | 1.5636 | -0.0017 | -0.3 | 0.88 / 0.92 / 0.97 | 0.961 of 207 |
| transition | 7.1574 | 7.1574 | 7.2737 | 7.1537 | 7.1455 | -0.1162 | -2.9 | 0.88 / 0.95 / 1.01 | 0.860 of 207 |
| congested | 4.5768 | 4.5768 | 4.5944 | 5.3129 | 4.5410 | -0.0176 | -0.3 | 0.55 / 0.80 / 1.03 | 0.849 of 106 |
| labelled | 3.1731 | 3.1731 | 3.2069 | 3.2099 | 3.1682 | -0.0337 | -3.9 | 0.87 / 0.93 / 0.96 | 0.990 of 207 |
