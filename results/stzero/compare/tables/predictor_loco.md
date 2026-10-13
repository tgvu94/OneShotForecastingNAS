# Option 3 of Branch 3b: predictor on our labels, leave-one-city-out

Target: within-city rank of -val MAE (seed 0) in [0, 1]. Features: operator counts per cell, edge counts, head, decoder, log params, log FLOPs; task statistics ['n_nodes', 'r1_permille_w12', 'r2_permille_w12', 'acf_lag1', 'acf_lag12', 'acf_lag288', 'cv_median_node', 'frac_zero', 'density', 'naive_last_value_val_mae', 'diff_std_over_std'] (z-scored over the training cities). Spearman with -val MAE on the held-out city, 95 % bootstrap CI (2000 samples), partial rho after the rank regression on log params. Boosting predictions are the mean over fit seeds [0, 1, 2].

With two training cities every task statistic takes two values in the training set, so the task-aware model can learn only a city x operator interaction, and the held-out city's statistics are an extrapolation. This is a property of a three-city benchmark, not of the predictor.

| held-out city | N | trained on | predictor | rho (95 % CI) | partial rho (log params) |
|---|---|---|---|---|---|
| pems04 | 300 | pems08+metrla (300) | ridge arch-only | +0.51 (+0.41, +0.60) | +0.52 |
| pems04 | 300 | pems08+metrla (300) | gbr arch-only | +0.46 (+0.36, +0.55) | +0.46 |
| pems04 | 300 | pems08+metrla (300) | gbr arch + task stats | +0.50 (+0.41, +0.59) | +0.50 |
| pems04 | 300 | pems04 (5-fold CV, reference) (300) | gbr arch-only, within city | +0.77 (+0.72, +0.82) | +0.77 |
| pems08 | 150 | pems04+metrla (450) | ridge arch-only | +0.78 (+0.72, +0.83) | +0.78 |
| pems08 | 150 | pems04+metrla (450) | gbr arch-only | +0.76 (+0.67, +0.83) | +0.76 |
| pems08 | 150 | pems04+metrla (450) | gbr arch + task stats | +0.63 (+0.52, +0.72) | +0.62 |
| pems08 | 150 | pems08 (5-fold CV, reference) (150) | gbr arch-only, within city | +0.86 (+0.82, +0.89) | +0.86 |
| metrla | 150 | pems04+pems08 (450) | ridge arch-only | +0.46 (+0.32, +0.58) | +0.49 |
| metrla | 150 | pems04+pems08 (450) | gbr arch-only | +0.50 (+0.38, +0.60) | +0.52 |
| metrla | 150 | pems04+pems08 (450) | gbr arch + task stats | +0.53 (+0.42, +0.63) | +0.55 |
| metrla | 150 | metrla (5-fold CV, reference) (150) | gbr arch-only, within city | +0.86 (+0.82, +0.89) | +0.87 |
