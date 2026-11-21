# calibration: stid_trueclock under our pipeline with the two settings of the trainer taken out

Masked MAE in the raw unit (mph) on the test windows that every variant and the benchst split hold.  A value is the mean of
the seeds of the row; the column 'against stock' is the mean of the 12 steps against the row 'stock' (STID under the stock
BasicTS run on this cluster); 'sd' is the standard deviation (ddof = 1) of the mean of the 12 steps over the seeds.

## metrla (6747 windows)

| Variant | seeds | step 3 | step 6 | step 12 | mean of 12 | free | transition | congested | sd | against stock |
|---|---|---|---|---|---|---|---|---|---|---|
| stock | 1 | 2.8074 | 3.1770 | 3.5493 | 3.1192 | 1.4108 | 5.6319 | 4.7506 |  | +0.00 % |
| ours, base | 3 | 3.2020 | 3.8208 | 4.6351 | 3.7913 | 1.6204 | 6.3289 | 6.0150 | 0.0208 | +21.55 % |
| ours, both | 3 | 2.8343 | 3.2093 | 3.5960 | 3.1534 | 1.4190 | 5.6907 | 5.1243 | 0.0048 | +1.09 % |
| ours, both_noamp | 3 | 2.8350 | 3.2108 | 3.5990 | 3.1549 | 1.4195 | 5.6967 | 5.0788 | 0.0034 | +1.14 % |
| ours, clip5 | 3 | 3.2099 | 3.8327 | 4.6533 | 3.8038 | 1.6179 | 6.3614 | 6.1682 | 0.0103 | +21.95 % |
| ours, noinstnorm | 3 | 2.8318 | 3.2077 | 3.5945 | 3.1508 | 1.4183 | 5.6899 | 5.0804 | 0.0066 | +1.01 % |
| benchst, stid_trueclock | 3 | 3.2021 | 3.8226 | 4.6357 | 3.7919 | 1.6105 | 6.3378 | 6.1203 | 0.0068 | +21.57 % |
| chronos2_joint | 1 | 2.8373 | 3.2611 | 3.7477 | 3.2189 | 1.4498 | 5.8643 | 4.3574 |  | +3.20 % |

## pemsbay (10316 windows)

| Variant | seeds | step 3 | step 6 | step 12 | mean of 12 | free | transition | congested | sd | against stock |
|---|---|---|---|---|---|---|---|---|---|---|
| stock | 1 | 1.3131 | 1.6357 | 1.9202 | 1.5705 | 0.9170 | 5.2542 | 3.3742 |  | +0.00 % |
| ours, base | 3 | 1.3970 | 1.8235 | 2.3293 | 1.7806 | 0.9897 | 6.2284 | 4.1427 | 0.0082 | +13.38 % |
| ours, both | 3 | 1.3706 | 1.7811 | 2.2586 | 1.7368 | 0.9654 | 6.0954 | 3.6871 | 0.0030 | +10.59 % |
| ours, both_noamp | 3 | 1.3709 | 1.7818 | 2.2588 | 1.7374 | 0.9656 | 6.1002 | 3.6477 | 0.0033 | +10.63 % |
| ours, clip5 | 3 | 1.3965 | 1.8250 | 2.3354 | 1.7829 | 0.9914 | 6.2275 | 4.2554 | 0.0019 | +13.52 % |
| ours, clock | 3 | 1.3649 | 1.7355 | 2.1165 | 1.6780 | 0.9643 | 5.6816 | 3.9744 | 0.0017 | +6.84 % |
| ours, noinstnorm | 3 | 1.3731 | 1.7831 | 2.2645 | 1.7398 | 0.9663 | 6.1197 | 3.5389 | 0.0052 | +10.78 % |
| ours, noinstnorm_clock | 3 | 1.3344 | 1.6720 | 1.9708 | 1.6045 | 0.9312 | 5.3765 | 3.8567 | 0.0018 | +2.16 % |
| benchst, stid_trueclock | 3 | 1.3960 | 1.8248 | 2.3352 | 1.7825 | 0.9917 | 6.2264 | 4.1976 | 0.0025 | +13.50 % |
| chronos2_joint | 1 | 1.3174 | 1.6291 | 1.9071 | 1.5699 | 0.8751 | 5.4889 | 3.4464 |  | -0.04 % |

