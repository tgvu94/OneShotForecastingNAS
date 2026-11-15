# Predictor on our labels, leave-one-city-out

Target: within-city rank of -val MAE (seed 0) in [0, 1]. Features: operator counts per cell, edge counts, head, decoder, log params, log FLOPs; task statistics ['n_nodes', 'r1_permille_w12', 'r2_permille_w12', 'acf_lag1', 'acf_lag12', 'acf_lag288', 'cv_median_node', 'frac_zero', 'density', 'naive_last_value_val_mae', 'diff_std_over_std'] (z-scored over the training cities); the stored proxies ['fisher', 'flops', 'glass', 'glass_s', 'glass_t', 'grad_norm_all', 'grasp_all', 'jacov', 'l2_norm_all', 'nwot', 'nwot_per_layer', 'params', 'plain_all', 'snip_all', 'swap', 'synflow_all', 'zen', 'zico', 'zico_s', 'zico_sizectrl', 'zico_t'] rank-normalised inside each city. Spearman with -val MAE on the held-out city, 95 % bootstrap CI (2000 samples), partial rho after the rank regression on log params. Boosting predictions are the mean over fit seeds [0, 1, 2].

With 3 training cities every task statistic takes 3 values in the training set, so the task-aware model can learn only a city x operator interaction, and the held-out city's statistics are an extrapolation. This is a property of a benchmark with few cities, not of the predictor.

| held-out city | N | trained on | predictor | rho (95 % CI) | partial rho (log params) |
|---|---|---|---|---|---|
| metrla | 150 | pems04+chengdu+shenzhen (450) | ridge arch-only | +0.68 (+0.59, +0.76) | +0.70 |
| metrla | 150 | pems04+chengdu+shenzhen (450) | gbr arch-only | +0.57 (+0.45, +0.69) | +0.58 |
| metrla | 150 | pems04+chengdu+shenzhen (450) | gbr arch + task stats | +0.57 (+0.44, +0.68) | +0.57 |
| metrla | 150 | pems04+chengdu+shenzhen (450) | gbr proxies only | +0.59 (+0.47, +0.70) | +0.60 |
| metrla | 150 | pems04+chengdu+shenzhen (450) | gbr arch + proxies | +0.57 (+0.44, +0.68) | +0.58 |
| metrla | 150 | metrla (5-fold CV, reference) (150) | gbr arch-only, within city | +0.90 (+0.86, +0.92) | +0.90 |
| pems04 | 150 | metrla+chengdu+shenzhen (450) | ridge arch-only | +0.53 (+0.39, +0.65) | +0.50 |
| pems04 | 150 | metrla+chengdu+shenzhen (450) | gbr arch-only | +0.56 (+0.44, +0.68) | +0.55 |
| pems04 | 150 | metrla+chengdu+shenzhen (450) | gbr arch + task stats | +0.57 (+0.44, +0.68) | +0.55 |
| pems04 | 150 | metrla+chengdu+shenzhen (450) | gbr proxies only | +0.57 (+0.45, +0.68) | +0.55 |
| pems04 | 150 | metrla+chengdu+shenzhen (450) | gbr arch + proxies | +0.57 (+0.45, +0.68) | +0.55 |
| pems04 | 150 | pems04 (5-fold CV, reference) (150) | gbr arch-only, within city | +0.75 (+0.66, +0.82) | +0.73 |
| chengdu | 150 | metrla+pems04+shenzhen (450) | ridge arch-only | +0.66 (+0.56, +0.75) | +0.64 |
| chengdu | 150 | metrla+pems04+shenzhen (450) | gbr arch-only | +0.72 (+0.62, +0.79) | +0.70 |
| chengdu | 150 | metrla+pems04+shenzhen (450) | gbr arch + task stats | +0.71 (+0.62, +0.79) | +0.70 |
| chengdu | 150 | metrla+pems04+shenzhen (450) | gbr proxies only | +0.70 (+0.60, +0.79) | +0.68 |
| chengdu | 150 | metrla+pems04+shenzhen (450) | gbr arch + proxies | +0.72 (+0.62, +0.80) | +0.69 |
| chengdu | 150 | chengdu (5-fold CV, reference) (150) | gbr arch-only, within city | +0.61 (+0.50, +0.71) | +0.58 |
| shenzhen | 150 | metrla+pems04+chengdu (450) | ridge arch-only | +0.81 (+0.74, +0.86) | +0.80 |
| shenzhen | 150 | metrla+pems04+chengdu (450) | gbr arch-only | +0.81 (+0.74, +0.86) | +0.80 |
| shenzhen | 150 | metrla+pems04+chengdu (450) | gbr arch + task stats | +0.77 (+0.69, +0.83) | +0.76 |
| shenzhen | 150 | metrla+pems04+chengdu (450) | gbr proxies only | +0.81 (+0.73, +0.86) | +0.79 |
| shenzhen | 150 | metrla+pems04+chengdu (450) | gbr arch + proxies | +0.82 (+0.75, +0.87) | +0.80 |
| shenzhen | 150 | shenzhen (5-fold CV, reference) (150) | gbr arch-only, within city | +0.73 (+0.65, +0.80) | +0.73 |

## Leave one operator family out, within a city (gbr arch-only)

Fit on the other families of the same city, score the held-out family. Pass line F2: Kendall >= 0.5 on the held-out family on two of three cities.

| city | family kind | held-out family | n held out | n train | Spearman | Kendall |
|---|---|---|---|---|---|---|
| metrla | seq_family | gru | 13 | 137 | +0.87 | +0.72 |
| metrla | seq_family | lstm | 29 | 121 | +0.85 | +0.64 |
| metrla | seq_family | mlp_mix | 23 | 127 | +0.90 | +0.71 |
| metrla | seq_family | sep_tcn | 24 | 126 | +0.90 | +0.73 |
| metrla | seq_family | skip_connection | 16 | 134 | +0.87 | +0.70 |
| metrla | seq_family | tcn | 31 | 119 | +0.89 | +0.74 |
| metrla | seq_family | transformer | 14 | 136 | +0.85 | +0.69 |
| metrla | graph_family | adaptive-only | 17 | 133 | +0.92 | +0.78 |
| metrla | graph_family | diffusion | 15 | 135 | +0.95 | +0.85 |
| metrla | graph_family | gcn | 12 | 138 | +0.88 | +0.79 |
| metrla | graph_family | mixed | 57 | 93 | +0.91 | +0.74 |
| metrla | graph_family | none | 48 | 102 | +0.88 | +0.70 |
| pems04 | seq_family | gru | 13 | 137 | +0.19 | +0.13 |
| pems04 | seq_family | lstm | 29 | 121 | +0.74 | +0.57 |
| pems04 | seq_family | mlp_mix | 23 | 127 | +0.89 | +0.72 |
| pems04 | seq_family | sep_tcn | 24 | 126 | +0.79 | +0.61 |
| pems04 | seq_family | skip_connection | 16 | 134 | +0.80 | +0.62 |
| pems04 | seq_family | tcn | 31 | 119 | +0.76 | +0.57 |
| pems04 | seq_family | transformer | 14 | 136 | +0.85 | +0.76 |
| pems04 | graph_family | adaptive-only | 17 | 133 | +0.84 | +0.66 |
| pems04 | graph_family | diffusion | 15 | 135 | +0.66 | +0.50 |
| pems04 | graph_family | gcn | 12 | 138 | +0.76 | +0.52 |
| pems04 | graph_family | mixed | 57 | 93 | +0.77 | +0.59 |
| pems04 | graph_family | none | 48 | 102 | +0.73 | +0.53 |
| chengdu | seq_family | gru | 13 | 137 | +0.27 | +0.18 |
| chengdu | seq_family | lstm | 29 | 121 | +0.59 | +0.42 |
| chengdu | seq_family | mlp_mix | 23 | 127 | +0.67 | +0.53 |
| chengdu | seq_family | sep_tcn | 24 | 126 | +0.81 | +0.62 |
| chengdu | seq_family | skip_connection | 16 | 134 | +0.84 | +0.67 |
| chengdu | seq_family | tcn | 31 | 119 | +0.60 | +0.44 |
| chengdu | seq_family | transformer | 14 | 136 | +0.57 | +0.45 |
| chengdu | graph_family | adaptive-only | 17 | 133 | +0.70 | +0.56 |
| chengdu | graph_family | diffusion | 15 | 135 | +0.51 | +0.39 |
| chengdu | graph_family | gcn | 12 | 138 | +0.78 | +0.64 |
| chengdu | graph_family | mixed | 57 | 93 | +0.67 | +0.49 |
| chengdu | graph_family | none | 48 | 102 | +0.69 | +0.51 |
| shenzhen | seq_family | gru | 13 | 137 | +0.54 | +0.38 |
| shenzhen | seq_family | lstm | 29 | 121 | +0.77 | +0.56 |
| shenzhen | seq_family | mlp_mix | 23 | 127 | +0.87 | +0.68 |
| shenzhen | seq_family | sep_tcn | 24 | 126 | +0.74 | +0.56 |
| shenzhen | seq_family | skip_connection | 16 | 134 | +0.64 | +0.47 |
| shenzhen | seq_family | tcn | 31 | 119 | +0.73 | +0.52 |
| shenzhen | seq_family | transformer | 14 | 136 | +0.80 | +0.65 |
| shenzhen | graph_family | adaptive-only | 17 | 133 | +0.77 | +0.57 |
| shenzhen | graph_family | diffusion | 15 | 135 | +0.86 | +0.70 |
| shenzhen | graph_family | gcn | 12 | 138 | +0.80 | +0.64 |
| shenzhen | graph_family | mixed | 57 | 93 | +0.76 | +0.58 |
| shenzhen | graph_family | none | 48 | 102 | +0.74 | +0.53 |

| city | family kind | families | n-weighted Kendall | families with Kendall >= 0.5 |
|---|---|---|---|---|
| chengdu | graph_family | 5 | +0.50 | 3 |
| chengdu | seq_family | 7 | +0.48 | 3 |
| metrla | graph_family | 5 | +0.75 | 5 |
| metrla | seq_family | 7 | +0.70 | 7 |
| pems04 | graph_family | 5 | +0.56 | 5 |
| pems04 | seq_family | 7 | +0.58 | 6 |
| shenzhen | graph_family | 5 | +0.58 | 5 |
| shenzhen | seq_family | 7 | +0.55 | 5 |

## Learning curve within a city

Fit on n random labels of the city, score the rest; mean and 5-95 % range of Spearman over 20 draws; cost = the logged GPU-hours of the n labels.

| city | predictor | n labels | GPU-hours of the labels | Spearman mean (5 %, 95 %) |
|---|---|---|---|---|
| metrla | gbr arch-only | 10 | 2.22 | +0.68 (+0.39, +0.87) |
| metrla | gbr arch + proxies | 10 | 2.22 | +0.59 (+0.34, +0.82) |
| metrla | gbr arch-only | 25 | 5.53 | +0.84 (+0.78, +0.89) |
| metrla | gbr arch + proxies | 25 | 5.53 | +0.82 (+0.78, +0.88) |
| metrla | gbr arch-only | 50 | 10.95 | +0.88 (+0.85, +0.89) |
| metrla | gbr arch + proxies | 50 | 10.95 | +0.86 (+0.80, +0.89) |
| metrla | gbr arch-only | 75 | 16.37 | +0.89 (+0.87, +0.92) |
| metrla | gbr arch + proxies | 75 | 16.37 | +0.88 (+0.84, +0.91) |
| metrla | gbr arch-only | 100 | 21.88 | +0.89 (+0.85, +0.93) |
| metrla | gbr arch + proxies | 100 | 21.88 | +0.88 (+0.85, +0.92) |
| metrla | gbr arch-only | 125 | 27.45 | +0.89 (+0.82, +0.95) |
| metrla | gbr arch + proxies | 125 | 27.45 | +0.88 (+0.81, +0.93) |
| pems04 | gbr arch-only | 10 | 1.94 | +0.46 (+0.30, +0.65) |
| pems04 | gbr arch + proxies | 10 | 1.94 | +0.51 (+0.31, +0.64) |
| pems04 | gbr arch-only | 25 | 4.74 | +0.62 (+0.49, +0.72) |
| pems04 | gbr arch + proxies | 25 | 4.74 | +0.66 (+0.59, +0.76) |
| pems04 | gbr arch-only | 50 | 9.53 | +0.68 (+0.62, +0.75) |
| pems04 | gbr arch + proxies | 50 | 9.53 | +0.70 (+0.65, +0.76) |
| pems04 | gbr arch-only | 75 | 14.32 | +0.70 (+0.65, +0.77) |
| pems04 | gbr arch + proxies | 75 | 14.32 | +0.73 (+0.66, +0.80) |
| pems04 | gbr arch-only | 100 | 19.14 | +0.76 (+0.66, +0.82) |
| pems04 | gbr arch + proxies | 100 | 19.14 | +0.79 (+0.71, +0.86) |
| pems04 | gbr arch-only | 125 | 23.88 | +0.75 (+0.59, +0.84) |
| pems04 | gbr arch + proxies | 125 | 23.88 | +0.74 (+0.61, +0.87) |
| chengdu | gbr arch-only | 10 | 1.46 | +0.42 (+0.15, +0.58) |
| chengdu | gbr arch + proxies | 10 | 1.46 | +0.41 (+0.18, +0.60) |
| chengdu | gbr arch-only | 25 | 3.55 | +0.53 (+0.32, +0.64) |
| chengdu | gbr arch + proxies | 25 | 3.55 | +0.54 (+0.34, +0.64) |
| chengdu | gbr arch-only | 50 | 7.04 | +0.59 (+0.54, +0.66) |
| chengdu | gbr arch + proxies | 50 | 7.04 | +0.59 (+0.50, +0.64) |
| chengdu | gbr arch-only | 75 | 10.53 | +0.66 (+0.61, +0.71) |
| chengdu | gbr arch + proxies | 75 | 10.53 | +0.63 (+0.55, +0.73) |
| chengdu | gbr arch-only | 100 | 14.24 | +0.65 (+0.61, +0.72) |
| chengdu | gbr arch + proxies | 100 | 14.24 | +0.66 (+0.60, +0.73) |
| chengdu | gbr arch-only | 125 | 17.68 | +0.69 (+0.56, +0.83) |
| chengdu | gbr arch + proxies | 125 | 17.68 | +0.66 (+0.50, +0.83) |
| shenzhen | gbr arch-only | 10 | 2.04 | +0.36 (+0.14, +0.60) |
| shenzhen | gbr arch + proxies | 10 | 2.04 | +0.41 (+0.25, +0.59) |
| shenzhen | gbr arch-only | 25 | 4.94 | +0.60 (+0.39, +0.74) |
| shenzhen | gbr arch + proxies | 25 | 4.94 | +0.59 (+0.33, +0.71) |
| shenzhen | gbr arch-only | 50 | 10.01 | +0.67 (+0.60, +0.73) |
| shenzhen | gbr arch + proxies | 50 | 10.01 | +0.68 (+0.62, +0.73) |
| shenzhen | gbr arch-only | 75 | 15.01 | +0.70 (+0.64, +0.78) |
| shenzhen | gbr arch + proxies | 75 | 15.01 | +0.72 (+0.67, +0.76) |
| shenzhen | gbr arch-only | 100 | 20.03 | +0.73 (+0.68, +0.80) |
| shenzhen | gbr arch + proxies | 100 | 20.03 | +0.74 (+0.67, +0.82) |
| shenzhen | gbr arch-only | 125 | 25.07 | +0.77 (+0.66, +0.86) |
| shenzhen | gbr arch + proxies | 125 | 25.07 | +0.74 (+0.59, +0.84) |

| city | predictor | smallest n with mean Spearman >= 0.6 | its GPU-hours |
|---|---|---|---|
| metrla | gbr arch-only | 10 | 2.22 |
| metrla | gbr arch + proxies | 25 | 5.53 |
| pems04 | gbr arch-only | 25 | 4.74 |
| pems04 | gbr arch + proxies | 25 | 4.74 |
| chengdu | gbr arch-only | 75 | 10.53 |
| chengdu | gbr arch + proxies | 75 | 10.53 |
| shenzhen | gbr arch-only | 25 | 4.94 |
| shenzhen | gbr arch + proxies | 50 | 10.01 |
