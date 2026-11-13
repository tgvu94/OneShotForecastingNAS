# Spatial coupling of each city (BasicTS+ r1, r2) and series statistics, training split

Indistinguishable pair: cosine(history) > 0.9 and cosine(future) < 0.5. r1 = indistinguishable / (T N N); r2 = indistinguishable / similar-history pairs. Per-mille scale as in the paper's Fig. 4. The paper reports W = H = 12 on 11 datasets without a value table; the raw and z-scored rows bracket its unstated normalisation.

| dataset | scaling | W | H | steps | r1 (permille) | r2 (permille) | indistinguishable | similar history |
|---|---|---|---|---|---|---|---|---|
| pems03 | zscore | 12 | 12 | 15701 | 27.452 | 42.36 | 55242260 | 1304222104 |
| pems03 | raw | 12 | 12 | 15701 | 0.566 | 0.61 | 1138146 | 1869115287 |
| pems07 | zscore | 12 | 12 | 16911 | 31.414 | 51.96 | 414207466 | 7971197383 |
| pems07 | raw | 12 | 12 | 16911 | 0.422 | 0.43 | 5567753 | 12954815883 |
| pemsbay | zscore | 12 | 12 | 31246 | 29.961 | 68.90 | 98881234 | 1435087646 |
| pemsbay | raw | 12 | 12 | 31246 | 0.001 | 0.00 | 2986 | 3285160996 |
| chengdu | zscore | 12 | 12 | 10345 | 17.804 | 119.17 | 50572190 | 424381392 |
| chengdu | raw | 12 | 12 | 10345 | 0.000 | 0.00 | 674 | 2815372698 |
| shenzhen | zscore | 12 | 12 | 10345 | 14.086 | 133.48 | 57288284 | 429196781 |
| shenzhen | raw | 12 | 12 | 10345 | 0.000 | 0.00 | 496 | 4049316121 |
| expytky | zscore | 12 | 12 | 7925 | 4.991 | 290.13 | 134362182 | 463109691 |
| expytky | raw | 12 | 12 | 7925 | 0.448 | 0.53 | 12053989 | 22922712867 |

## Series statistics (training split, channel 0, raw unless stated)

| dataset | N | T | mean | std | CV (median node) | skew | kurtosis | zeros | ACF lag 1 / 12 / 288 (z-scored) | diff std / std | edges | density | naive last-value val MAE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pems03 | 358 | 15724 | 181.4 | 144.4 | 0.56 | -0.10 | -1.19 | 0.007 | 0.974 / 0.887 / 0.880 | 0.256 | nan | nan | nan |
| pems07 | 883 | 16934 | 309.5 | 189.5 | 0.48 | -0.41 | -1.00 | 0.005 | 0.976 / 0.885 / 0.866 | 0.226 | nan | nan | nan |
| pemsbay | 325 | 31269 | 62.8 | 9.4 | 0.13 | -2.70 | 8.47 | 0.000 | 0.982 / 0.687 / 0.627 | 0.230 | nan | nan | nan |
| chengdu | 524 | 10368 | 29.6 | 9.7 | 0.21 | 0.17 | 0.36 | 0.000 | 0.839 / 0.545 / 0.685 | 0.610 | nan | nan | nan |
| shenzhen | 627 | 10368 | 31.1 | 11.1 | 0.17 | -0.23 | 1.36 | 0.000 | 0.809 / 0.497 / 0.612 | 0.662 | nan | nan | nan |
| expytky | 1843 | 7948 | 58.2 | 23.7 | 0.22 | -0.90 | 3.56 | 0.003 | 0.583 / 0.238 / 0.337 | 0.934 | nan | nan | nan |
