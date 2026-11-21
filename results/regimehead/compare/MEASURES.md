# regimehead: the head per regime, the composites and the lines of stage 0

Test split, h = 12, mean of 12 steps, raw unit, zero mask, targets with a regime label.  A value is the mean of 3 seeds.
sigma_seed of a scope is the standard deviation (ddof = 1) of the MAE head over its 3 seeds in that scope.  The choice of a
head uses the validation split (mean of the seeds); the ceiling of a seed uses the test split of the two other seeds.
A gain is the MAE head minus the composite, in sigma_seed.

## metrla (rule absolute, mph); share of the targets: free 0.603, transition 0.378, congested 0.018

### `261470bcc0`, MAE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 1.6672 ± 0.0051 | 6.2518 ± 0.0044 | 7.4012 ± 0.0857 | 3.5063 ± 0.0012 |
| head mse | 2.0290 ± 0.0078 | 6.3787 ± 0.0425 | 8.0508 ± 0.1369 | 3.7844 ± 0.0184 |
| head huber | 1.9663 ± 0.0286 | 6.3188 ± 0.0096 | 7.8141 ± 0.0543 | 3.7196 ± 0.0208 |
| head focal | 1.7797 ± 0.0082 | 6.2523 ± 0.0154 | 7.4728 ± 0.0260 | 3.5756 ± 0.0016 |
| head wmae2 | 1.7478 ± 0.0059 | 6.2196 ± 0.0168 | 7.0608 ± 0.0274 | 3.5365 ± 0.0034 |
| head wmae4 | 1.8527 ± 0.0086 | 6.2089 ± 0.0194 | 6.8493 ± 0.1158 | 3.5919 ± 0.0066 |
| composite per regime, validation choice | 1.6672 (+0.0 σ) | 6.2089 (+9.7 σ) | 6.8493 (+6.4 σ) | 3.4800 (+22.1 σ) |
| composite per sensor and regime, validation choice | 1.6676 (-0.1 σ) | 6.1977 (+12.2 σ) | 6.8533 (+6.4 σ) | 3.4760 (+25.4 σ) |
| ceiling per regime | 1.6672 (+0.0 σ) | 6.2089 (+9.7 σ) | 6.8493 (+6.4 σ) | 3.4800 (+22.1 σ) |
| ceiling per sensor and regime | 1.6675 (-0.1 σ) | 6.2001 (+11.7 σ) | 6.9130 (+5.7 σ) | 3.4780 (+23.7 σ) |
| chronos2_joint | 1.4498 | 5.8643 | 4.3574 | 3.1731 |
| share of the gap to the frozen model that the composite per regime closes | 0.000 | 0.111 | 0.181 | 0.079 |

Head chosen per regime on the validation split: free mae, transition wmae4, congested wmae4.  Share of the sensor-regime cells per head: mae 0.57, mse 0.02, huber 0.03, focal 0.05, wmae2 0.07, wmae4 0.25.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

### `261470bcc0`, RMSE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 2.8750 ± 0.0104 | 10.1456 ± 0.0099 | 11.6656 ± 0.2416 | 6.8126 ± 0.0095 |
| head mse | 3.2860 ± 0.0161 | 9.9398 ± 0.0470 | 11.8539 ± 0.1928 | 6.8159 ± 0.0224 |
| head huber | 3.2239 ± 0.0594 | 9.9195 ± 0.0086 | 11.6583 ± 0.0284 | 6.7806 ± 0.0157 |
| head focal | 2.9803 ± 0.0152 | 10.0421 ± 0.0339 | 11.5553 ± 0.0770 | 6.7784 ± 0.0180 |
| head wmae2 | 3.0169 ± 0.0198 | 10.0566 ± 0.0417 | 11.1111 ± 0.2060 | 6.7828 ± 0.0284 |
| head wmae4 | 3.1759 ± 0.0249 | 9.9933 ± 0.0331 | 10.8269 ± 0.2308 | 6.7829 ± 0.0178 |
| composite per regime, validation choice | 2.8750 (+0.0 σ) | 9.9195 (+22.9 σ) | 10.8269 (+3.5 σ) | 6.6597 (+16.2 σ) |
| composite per sensor and regime, validation choice | 2.8805 (-0.5 σ) | 9.9154 (+23.3 σ) | 10.7949 (+3.6 σ) | 6.6580 (+16.3 σ) |
| ceiling per regime | 2.8750 (+0.0 σ) | 9.9195 (+22.9 σ) | 10.8269 (+3.5 σ) | 6.6597 (+16.2 σ) |
| ceiling per sensor and regime | 2.8820 (-0.7 σ) | 9.9112 (+23.8 σ) | 10.9897 (+2.8 σ) | 6.6617 (+15.9 σ) |

Head chosen per regime on the validation split: free mae, transition huber, congested wmae4.  Share of the sensor-regime cells per head: mae 0.48, mse 0.14, huber 0.11, focal 0.05, wmae2 0.04, wmae4 0.18.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

### `stid_trueclock`, MAE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 1.6105 ± 0.0059 | 6.3378 ± 0.0077 | 6.1203 ± 0.1117 | 3.4813 ± 0.0042 |
| head mse | 1.8136 ± 0.0108 | 6.3678 ± 0.0178 | 7.4342 ± 0.2074 | 3.6391 ± 0.0053 |
| head huber | 1.7621 ± 0.0095 | 6.3468 ± 0.0088 | 7.0304 ± 0.1325 | 3.5927 ± 0.0068 |
| head focal | 1.6704 ± 0.0087 | 6.3267 ± 0.0079 | 6.3008 ± 0.0921 | 3.5165 ± 0.0059 |
| head wmae2 | 1.6577 ± 0.0021 | 6.2980 ± 0.0042 | 5.8807 ± 0.0782 | 3.4904 ± 0.0034 |
| head wmae4 | 1.7189 ± 0.0086 | 6.2962 ± 0.0196 | 5.7995 ± 0.1014 | 3.5251 ± 0.0115 |
| composite per regime, validation choice | 1.6105 (+0.0 σ) | 6.2962 (+5.4 σ) | 5.7995 (+2.9 σ) | 3.4597 (+5.2 σ) |
| composite per sensor and regime, validation choice | 1.6105 (-0.0 σ) | 6.2882 (+6.4 σ) | 5.7595 (+3.2 σ) | 3.4560 (+6.1 σ) |
| ceiling per regime | 1.6105 (+0.0 σ) | 6.3044 (+4.3 σ) | 5.7995 (+2.9 σ) | 3.4628 (+4.4 σ) |
| ceiling per sensor and regime | 1.6107 (-0.0 σ) | 6.2735 (+8.3 σ) | 5.7195 (+3.6 σ) | 3.4498 (+7.6 σ) |
| chronos2_joint | 1.4498 | 5.8643 | 4.3574 | 3.1731 |
| share of the gap to the frozen model that the composite per regime closes | 0.000 | 0.088 | 0.182 | 0.070 |

Head chosen per regime on the validation split: free mae, transition wmae4, congested wmae4.  Share of the sensor-regime cells per head: mae 0.52, mse 0.06, huber 0.03, focal 0.04, wmae2 0.07, wmae4 0.28.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

### `stid_trueclock`, RMSE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 3.1957 ± 0.0141 | 11.0699 ± 0.0814 | 11.4476 ± 0.4601 | 7.4106 ± 0.0486 |
| head mse | 3.4403 ± 0.0321 | 10.6302 ± 0.0604 | 12.5335 ± 0.5455 | 7.2636 ± 0.0577 |
| head huber | 3.3310 ± 0.0301 | 10.7189 ± 0.0791 | 12.1118 ± 0.3327 | 7.2691 ± 0.0536 |
| head focal | 3.2042 ± 0.0246 | 10.9286 ± 0.0998 | 11.5695 ± 0.3210 | 7.3365 ± 0.0611 |
| head wmae2 | 3.3746 ± 0.0177 | 11.0488 ± 0.0459 | 10.8399 ± 0.2626 | 7.4298 ± 0.0205 |
| head wmae4 | 3.6246 ± 0.0525 | 11.1073 ± 0.0959 | 10.9290 ± 0.3420 | 7.5356 ± 0.0697 |
| composite per regime, validation choice | 3.1957 (+0.0 σ) | 10.6302 (+5.4 σ) | 10.9290 (+1.1 σ) | 7.1481 (+5.4 σ) |
| composite per sensor and regime, validation choice | 3.1898 (+0.4 σ) | 10.6485 (+5.2 σ) | 10.7891 (+1.4 σ) | 7.1528 (+5.3 σ) |
| ceiling per regime | 3.1957 (+0.0 σ) | 10.6302 (+5.4 σ) | 11.0042 (+1.0 σ) | 7.1502 (+5.4 σ) |
| ceiling per sensor and regime | 3.1645 (+2.2 σ) | 10.6002 (+5.8 σ) | 10.5054 (+2.0 σ) | 7.1112 (+6.2 σ) |

Head chosen per regime on the validation split: free mae, transition mse, congested wmae4.  Share of the sensor-regime cells per head: mae 0.40, mse 0.32, huber 0.08, focal 0.07, wmae2 0.03, wmae4 0.11.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

## pemsbay (rule absolute, mph); share of the targets: free 0.846, transition 0.146, congested 0.008

### `261470bcc0`, MAE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 0.9953 ± 0.0020 | 5.9735 ± 0.0140 | 5.6436 ± 0.0966 | 1.7615 ± 0.0044 |
| head mse | 1.0878 ± 0.0035 | 6.0490 ± 0.0209 | 6.7217 ± 0.0554 | 1.8598 ± 0.0024 |
| head huber | 1.0507 ± 0.0028 | 5.9362 ± 0.0199 | 6.1662 ± 0.0731 | 1.8073 ± 0.0050 |
| head focal | 1.0395 ± 0.0020 | 5.9034 ± 0.0046 | 5.9494 ± 0.0556 | 1.7912 ± 0.0016 |
| head wmae2 | 1.0232 ± 0.0019 | 5.8941 ± 0.0033 | 5.5660 ± 0.1749 | 1.7728 ± 0.0034 |
| head wmae4 | 1.0594 ± 0.0034 | 5.8678 ± 0.0075 | 5.5838 ± 0.1021 | 1.7998 ± 0.0033 |
| composite per regime, validation choice | 0.9953 (+0.0 σ) | 5.8678 (+7.5 σ) | 5.5660 (+0.8 σ) | 1.7454 (+3.7 σ) |
| composite per sensor and regime, validation choice | 0.9923 (+1.5 σ) | 5.8662 (+7.7 σ) | 5.4966 (+1.5 σ) | 1.7420 (+4.5 σ) |
| ceiling per regime | 0.9953 (+0.0 σ) | 5.8678 (+7.5 σ) | 5.6051 (+0.4 σ) | 1.7457 (+3.6 σ) |
| ceiling per sensor and regime | 0.9922 (+1.5 σ) | 5.8581 (+8.2 σ) | 5.5533 (+0.9 σ) | 1.7413 (+4.6 σ) |
| chronos2_joint | 0.8751 | 5.4889 | 3.4464 | 1.5704 |
| share of the gap to the frozen model that the composite per regime closes | 0.000 | 0.218 | 0.035 | 0.084 |

Head chosen per regime on the validation split: free mae, transition wmae4, congested wmae2.  Share of the sensor-regime cells per head: mae 0.57, mse 0.06, huber 0.03, focal 0.05, wmae2 0.07, wmae4 0.22.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

### `261470bcc0`, RMSE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 1.6228 ± 0.0082 | 9.3304 ± 0.0134 | 9.1494 ± 0.1653 | 3.9555 ± 0.0044 |
| head mse | 1.8059 ± 0.0172 | 9.2236 ± 0.0203 | 10.3192 ± 0.1193 | 4.0101 ± 0.0025 |
| head huber | 1.7108 ± 0.0196 | 9.1751 ± 0.0308 | 9.7408 ± 0.1254 | 3.9458 ± 0.0173 |
| head focal | 1.6931 ± 0.0148 | 9.1719 ± 0.0135 | 9.5647 ± 0.1007 | 3.9346 ± 0.0107 |
| head wmae2 | 1.6950 ± 0.0073 | 9.2306 ± 0.0151 | 9.2391 ± 0.3226 | 3.9487 ± 0.0133 |
| head wmae4 | 1.8018 ± 0.0150 | 9.2021 ± 0.0031 | 9.3534 ± 0.2475 | 3.9812 ± 0.0014 |
| composite per regime, validation choice | 1.6228 (+0.0 σ) | 9.2236 (+8.0 σ) | 9.1494 (+0.0 σ) | 3.9188 (+8.3 σ) |
| composite per sensor and regime, validation choice | 1.6063 (+2.0 σ) | 9.1787 (+11.3 σ) | 9.1340 (+0.1 σ) | 3.8973 (+13.1 σ) |
| ceiling per regime | 1.6228 (+0.0 σ) | 9.1859 (+10.8 σ) | 9.1494 (+0.0 σ) | 3.9058 (+11.2 σ) |
| ceiling per sensor and regime | 1.6060 (+2.0 σ) | 9.1096 (+16.5 σ) | 9.1297 (+0.1 σ) | 3.8733 (+18.5 σ) |

Head chosen per regime on the validation split: free mae, transition mse, congested mae.  Share of the sensor-regime cells per head: mae 0.55, mse 0.15, huber 0.04, focal 0.07, wmae2 0.04, wmae4 0.15.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

### `stid_trueclock`, MAE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 0.9917 ± 0.0021 | 6.2264 ± 0.0200 | 4.1976 ± 0.0223 | 1.7831 ± 0.0025 |
| head mse | 1.0470 ± 0.0044 | 6.2179 ± 0.0147 | 5.8778 ± 0.0726 | 1.8429 ± 0.0053 |
| head huber | 1.0209 ± 0.0014 | 6.1622 ± 0.0372 | 4.9924 ± 0.1641 | 1.8051 ± 0.0055 |
| head focal | 1.0118 ± 0.0017 | 6.1573 ± 0.0341 | 4.5648 ± 0.1126 | 1.7931 ± 0.0048 |
| head wmae2 | 1.0035 ± 0.0042 | 6.1580 ± 0.0262 | 4.4066 ± 0.0568 | 1.7848 ± 0.0072 |
| head wmae4 | 1.0277 ± 0.0022 | 6.1105 ± 0.0410 | 4.3260 ± 0.1314 | 1.7977 ± 0.0072 |
| composite per regime, validation choice | 0.9917 (+0.0 σ) | 6.1105 (+5.8 σ) | 4.1976 (+0.0 σ) | 1.7662 (+6.7 σ) |
| composite per sensor and regime, validation choice | 0.9902 (+0.7 σ) | 6.0959 (+6.5 σ) | 4.2377 (-1.8 σ) | 1.7631 (+8.0 σ) |
| ceiling per regime | 0.9917 (+0.0 σ) | 6.1105 (+5.8 σ) | 4.1976 (+0.0 σ) | 1.7662 (+6.7 σ) |
| ceiling per sensor and regime | 0.9908 (+0.4 σ) | 6.0909 (+6.8 σ) | 4.2306 (-1.5 σ) | 1.7628 (+8.1 σ) |
| chronos2_joint | 0.8751 | 5.4889 | 3.4464 | 1.5704 |
| share of the gap to the frozen model that the composite per regime closes | 0.000 | 0.157 | 0.000 | 0.080 |

Head chosen per regime on the validation split: free mae, transition wmae4, congested mae.  Share of the sensor-regime cells per head: mae 0.55, mse 0.07, huber 0.04, focal 0.05, wmae2 0.08, wmae4 0.21.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

### `stid_trueclock`, RMSE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 1.5714 ± 0.0086 | 10.1647 ± 0.0655 | 10.1902 ± 0.5916 | 4.2490 ± 0.0340 |
| head mse | 1.6864 ± 0.0230 | 9.8451 ± 0.0862 | 13.1092 ± 1.0531 | 4.2446 ± 0.0605 |
| head huber | 1.6184 ± 0.0025 | 9.9665 ± 0.0777 | 12.2423 ± 0.4159 | 4.2412 ± 0.0357 |
| head focal | 1.5919 ± 0.0034 | 10.0258 ± 0.0533 | 11.1568 ± 0.1391 | 4.2276 ± 0.0160 |
| head wmae2 | 1.6016 ± 0.0112 | 10.0922 ± 0.1217 | 11.7105 ± 1.2279 | 4.2671 ± 0.0718 |
| head wmae4 | 1.6677 ± 0.0020 | 10.0360 ± 0.0673 | 11.5655 ± 0.4519 | 4.2652 ± 0.0141 |
| composite per regime, validation choice | 1.5714 (+0.0 σ) | 9.8451 (+4.9 σ) | 10.1902 (+0.0 σ) | 4.1377 (+3.3 σ) |
| composite per sensor and regime, validation choice | 1.5645 (+0.8 σ) | 9.8470 (+4.9 σ) | 11.2708 (-1.8 σ) | 4.1597 (+2.6 σ) |
| ceiling per regime | 1.5714 (+0.0 σ) | 9.8451 (+4.9 σ) | 10.1902 (+0.0 σ) | 4.1377 (+3.3 σ) |
| ceiling per sensor and regime | 1.5658 (+0.7 σ) | 9.7869 (+5.8 σ) | 10.2691 (-0.1 σ) | 4.1172 (+3.9 σ) |

Head chosen per regime on the validation split: free mae, transition mse, congested mae.  Share of the sensor-regime cells per head: mae 0.52, mse 0.18, huber 0.06, focal 0.06, wmae2 0.07, wmae4 0.11.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

## chengdu (rule relative, km/h); share of the targets: free 0.207, transition 0.788, congested 0.005

### `59d2d9e09e`, MAE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 2.0096 ± 0.0036 | 2.4312 ± 0.0051 | 3.9240 ± 0.0167 | 2.3518 ± 0.0044 |
| head mse | 2.0679 ± 0.0058 | 2.4449 ± 0.0090 | 3.7847 ± 0.0282 | 2.3739 ± 0.0074 |
| head huber | 2.0357 ± 0.0079 | 2.4397 ± 0.0098 | 3.7913 ± 0.0296 | 2.3632 ± 0.0093 |
| head focal | 2.0237 ± 0.0054 | 2.4373 ± 0.0049 | 3.8372 ± 0.0525 | 2.3591 ± 0.0047 |
| head wmae2 | 2.0340 ± 0.0067 | 2.4211 ± 0.0050 | 3.9252 ± 0.0202 | 2.3489 ± 0.0038 |
| head wmae4 | 2.0682 ± 0.0023 | 2.4144 ± 0.0039 | 3.8943 ± 0.0320 | 2.3505 ± 0.0032 |
| composite per regime, validation choice | 2.0096 (+0.0 σ) | 2.4144 (+3.3 σ) | 3.7847 (+8.4 σ) | 2.3378 (+3.2 σ) |
| composite per sensor and regime, validation choice | 2.0085 (+0.3 σ) | 2.4147 (+3.3 σ) | 3.7735 (+9.0 σ) | 2.3378 (+3.2 σ) |
| ceiling per regime | 2.0096 (+0.0 σ) | 2.4144 (+3.3 σ) | 3.7927 (+7.9 σ) | 2.3378 (+3.2 σ) |
| ceiling per sensor and regime | 2.0087 (+0.2 σ) | 2.4155 (+3.1 σ) | 3.7888 (+8.1 σ) | 2.3385 (+3.1 σ) |
| chronos2_joint | 1.9181 | 2.2905 | 2.6197 | 2.2153 |
| share of the gap to the frozen model that the composite per regime closes | 0.000 | 0.120 | 0.107 | 0.103 |

Head chosen per regime on the validation split: free mae, transition wmae4, congested mse.  Share of the sensor-regime cells per head: mae 0.49, mse 0.08, huber 0.08, focal 0.08, wmae2 0.08, wmae4 0.19.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

### `59d2d9e09e`, RMSE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 2.6760 ± 0.0041 | 3.7174 ± 0.0090 | 5.7362 ± 0.0290 | 3.5414 ± 0.0084 |
| head mse | 2.7585 ± 0.0060 | 3.6712 ± 0.0138 | 5.4883 ± 0.0513 | 3.5144 ± 0.0115 |
| head huber | 2.7095 ± 0.0088 | 3.6852 ± 0.0150 | 5.5232 ± 0.0407 | 3.5184 ± 0.0138 |
| head focal | 2.6908 ± 0.0053 | 3.6924 ± 0.0072 | 5.6335 ± 0.0721 | 3.5222 ± 0.0069 |
| head wmae2 | 2.7090 ± 0.0086 | 3.6966 ± 0.0125 | 5.7415 ± 0.0707 | 3.5295 ± 0.0113 |
| head wmae4 | 2.7536 ± 0.0033 | 3.6748 ± 0.0070 | 5.7030 ± 0.0425 | 3.5184 ± 0.0059 |
| composite per regime, validation choice | 2.6760 (+0.0 σ) | 3.6712 (+5.1 σ) | 5.4883 (+8.6 σ) | 3.5012 (+4.8 σ) |
| composite per sensor and regime, validation choice | 2.6726 (+0.8 σ) | 3.6634 (+6.0 σ) | 5.5104 (+7.8 σ) | 3.4944 (+5.6 σ) |
| ceiling per regime | 2.6760 (+0.0 σ) | 3.6712 (+5.1 σ) | 5.4883 (+8.6 σ) | 3.5012 (+4.8 σ) |
| ceiling per sensor and regime | 2.6725 (+0.8 σ) | 3.6612 (+6.2 σ) | 5.4965 (+8.3 σ) | 3.4925 (+5.9 σ) |

Head chosen per regime on the validation split: free mae, transition mse, congested mse.  Share of the sensor-regime cells per head: mae 0.47, mse 0.19, huber 0.11, focal 0.09, wmae2 0.03, wmae4 0.12.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

### `stid_trueclock`, MAE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 2.0526 ± 0.0032 | 2.4674 ± 0.0019 | 3.7085 ± 0.0274 | 2.3881 ± 0.0020 |
| head mse | 2.1092 ± 0.0025 | 2.4927 ± 0.0017 | 3.6865 ± 0.0656 | 2.4196 ± 0.0013 |
| head huber | 2.0788 ± 0.0021 | 2.4841 ± 0.0014 | 3.6895 ± 0.0267 | 2.4066 ± 0.0011 |
| head focal | 2.0722 ± 0.0058 | 2.4770 ± 0.0015 | 3.6650 ± 0.0617 | 2.3995 ± 0.0014 |
| head wmae2 | 2.0822 ± 0.0061 | 2.4595 ± 0.0021 | 3.6891 ± 0.0456 | 2.3879 ± 0.0018 |
| head wmae4 | 2.1166 ± 0.0064 | 2.4560 ± 0.0018 | 3.6622 ± 0.0466 | 2.3921 ± 0.0005 |
| composite per regime, validation choice | 2.0526 (+0.0 σ) | 2.4560 (+6.0 σ) | 3.6650 (+1.6 σ) | 2.3789 (+4.7 σ) |
| composite per sensor and regime, validation choice | 2.0512 (+0.4 σ) | 2.4543 (+6.8 σ) | 3.6191 (+3.3 σ) | 2.3770 (+5.7 σ) |
| ceiling per regime | 2.0526 (+0.0 σ) | 2.4560 (+6.0 σ) | 3.6864 (+0.8 σ) | 2.3790 (+4.7 σ) |
| ceiling per sensor and regime | 2.0517 (+0.3 σ) | 2.4552 (+6.4 σ) | 3.6194 (+3.3 σ) | 2.3778 (+5.2 σ) |
| chronos2_joint | 1.9181 | 2.2905 | 2.6197 | 2.2153 |
| share of the gap to the frozen model that the composite per regime closes | 0.000 | 0.065 | 0.040 | 0.054 |

Head chosen per regime on the validation split: free mae, transition wmae4, congested focal.  Share of the sensor-regime cells per head: mae 0.54, mse 0.07, huber 0.05, focal 0.05, wmae2 0.09, wmae4 0.21.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

### `stid_trueclock`, RMSE

| Row | free | transition | congested | labelled |
|---|---|---|---|---|
| head mae | 2.7495 ± 0.0055 | 3.7857 ± 0.0038 | 5.5809 ± 0.0443 | 3.6082 ± 0.0036 |
| head mse | 2.8295 ± 0.0035 | 3.7538 ± 0.0031 | 5.4425 ± 0.0956 | 3.5936 ± 0.0028 |
| head huber | 2.7814 ± 0.0024 | 3.7671 ± 0.0008 | 5.4639 ± 0.0278 | 3.5970 ± 0.0004 |
| head focal | 2.7700 ± 0.0082 | 3.7661 ± 0.0024 | 5.4759 ± 0.0928 | 3.5944 ± 0.0011 |
| head wmae2 | 2.7913 ± 0.0095 | 3.7637 ± 0.0039 | 5.5269 ± 0.0595 | 3.5962 ± 0.0032 |
| head wmae4 | 2.8363 ± 0.0102 | 3.7523 ± 0.0032 | 5.4835 ± 0.0643 | 3.5938 ± 0.0015 |
| composite per regime, validation choice | 2.7495 (+0.0 σ) | 3.7538 (+8.5 σ) | 5.4425 (+3.1 σ) | 3.5807 (+7.5 σ) |
| composite per sensor and regime, validation choice | 2.7446 (+0.9 σ) | 3.7387 (+12.5 σ) | 5.3962 (+4.2 σ) | 3.5671 (+11.3 σ) |
| ceiling per regime | 2.7495 (+0.0 σ) | 3.7552 (+8.1 σ) | 5.5066 (+1.7 σ) | 3.5824 (+7.1 σ) |
| ceiling per sensor and regime | 2.7449 (+0.8 σ) | 3.7390 (+12.4 σ) | 5.3833 (+4.5 σ) | 3.5673 (+11.2 σ) |

Head chosen per regime on the validation split: free mae, transition mse, congested mse.  Share of the sensor-regime cells per head: mae 0.51, mse 0.16, huber 0.06, focal 0.05, wmae2 0.04, wmae4 0.18.  Pass clause: True.  Ceiling within 2 σ in every regime: False.

## The lines

| Metric | City | Pass clause, one model at least | Ceiling within 2 σ in every regime, both models |
|---|---|---|---|
| MAE | metrla | True | False |
| MAE | pemsbay | True | False |
| MAE | chengdu | True | False |
| RMSE | metrla | True | False |
| RMSE | pemsbay | True | False |
| RMSE | chengdu | True | False |
