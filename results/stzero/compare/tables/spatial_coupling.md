# Spatial coupling of each city (BasicTS+ r1, r2) and series statistics, training split

Indistinguishable pair: cosine(history) > 0.9 and cosine(future) < 0.5. r1 = indistinguishable / (T N N); r2 = indistinguishable / similar-history pairs. Per-mille scale as in the paper's Fig. 4. The paper reports W = H = 12 on 11 datasets without a value table; the raw and z-scored rows bracket its unstated normalisation.

| dataset | scaling | W | H | steps | r1 (permille) | r2 (permille) | indistinguishable | similar history |
|---|---|---|---|---|---|---|---|---|
| pems04 | zscore | 12 | 12 | 10172 | 29.603 | 51.48 | 28380158 | 551293660 |
| pems04 | raw | 12 | 12 | 10172 | 1.041 | 1.11 | 997559 | 895679779 |
| pems04 | zscore | 96 | 12 | 10088 | 62.772 | 160.53 | 59682836 | 371792540 |
| pems04 | raw | 96 | 12 | 10088 | 16.289 | 18.40 | 15487637 | 841714624 |
| pems08 | zscore | 12 | 12 | 10690 | 28.580 | 50.14 | 8829392 | 176109176 |
| pems08 | raw | 12 | 12 | 10690 | 0.032 | 0.03 | 9918 | 300509876 |
| pems08 | zscore | 96 | 12 | 10606 | 72.276 | 167.61 | 22153698 | 132174162 |
| pems08 | raw | 96 | 12 | 10606 | 0.923 | 0.98 | 282933 | 289415439 |
| metrla | zscore | 12 | 12 | 20540 | 40.939 | 86.28 | 36031540 | 417603424 |
| metrla | raw | 12 | 12 | 20540 | 8.685 | 9.68 | 7643799 | 789632770 |
| metrla | zscore | 96 | 12 | 20456 | 28.575 | 114.80 | 25046936 | 218174820 |
| metrla | raw | 96 | 12 | 20456 | 32.952 | 37.35 | 28882653 | 773217843 |

## Series statistics (training split, channel 0, raw unless stated)

| dataset | N | T | mean | std | CV (median node) | skew | kurtosis | zeros | ACF lag 1 / 12 / 288 (z-scored) | diff std / std | edges | density | naive last-value val MAE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pems04 | 307 | 10195 | 207.2 | 156.5 | 0.58 | -0.02 | -1.19 | 0.017 | 0.971 / 0.886 / 0.844 | 0.280 | 340 | 0.0072 | 0.2773 |
| pems08 | 170 | 10713 | 229.7 | 145.6 | 0.46 | -0.24 | -1.09 | 0.003 | 0.968 / 0.891 / 0.859 | 0.280 | 274 | 0.0191 | 0.2714 |
| metrla | 207 | 20563 | 54.1 | 19.8 | 0.34 | -2.15 | 3.34 | 0.076 | 0.936 / 0.719 / 0.201 | 0.363 | 1313 | 0.0616 | 0.2563 |
