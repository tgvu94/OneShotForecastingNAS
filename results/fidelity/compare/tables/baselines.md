# fidelity baselines: stored runs of the seed subset

Label = mean test MAE of seeds 0 to 2 (20 epochs, zero mask). Scores come from seed 0. rho is Spearman with the label; "inside heads" is the count-weighted mean of the per-head values with a bootstrap interval (1,000 draws). Regret is that of the best of the first b picks, in sigma_seed. Cost share = logged seconds over the logged seconds of the full training of the same architectures (seed 0). Cost to one sigma = the evaluator on all architectures plus the rest of the full training of its picks, until a pick lies within one sigma_seed of the best label.

## metrla

N = 50; heads {'mse': np.int64(20), 'quantile': np.int64(16), 'mae': np.int64(14)}; sigma_seed 0.00142; std of the label 5.55 sigma_seed; full training of seed 0: 10.3 GPU-hours logged on nibi, 10.3 on the reference unit.

| kind | evaluator | rho | rho inside heads (95 % interval) | regret b = 1 | regret b = 5 | cost share | picks to one sigma | cost to one sigma |
|---|---|---|---|---|---|---|---|---|
| ceiling | seed 0 against the mean of seeds 1 and 2 | 0.96 | 0.87 (0.70, 0.94) |  |  | 1.000 |  |  |
| full training | seed 0, 20 epochs | 0.98 | 0.94 (0.83, 0.97) | 0.11 | 0.00 | 1.000 | 1 | 1.000 |
| epoch fidelity | val MAE after 1 epochs | 0.65 | 0.52 (0.20, 0.72) | 1.09 | 0.11 | 0.072 | 2 | 0.110 |
| epoch fidelity | val MAE after 2 epochs | 0.86 | 0.66 (0.42, 0.79) | 0.00 | 0.00 | 0.136 | 1 | 0.163 |
| epoch fidelity | val MAE after 3 epochs | 0.87 | 0.56 (0.28, 0.74) | 0.11 | 0.00 | 0.199 | 1 | 0.224 |
| epoch fidelity | val MAE after 4 epochs | 0.93 | 0.66 (0.37, 0.82) | 1.09 | 0.00 | 0.262 | 3 | 0.320 |
| epoch fidelity | val MAE after 5 epochs | 0.93 | 0.67 (0.43, 0.84) | 0.00 | 0.00 | 0.326 | 1 | 0.349 |
| epoch fidelity | val MAE after 6 epochs | 0.94 | 0.77 (0.52, 0.90) | 0.11 | 0.00 | 0.390 | 1 | 0.411 |
| epoch fidelity | val MAE after 7 epochs | 0.94 | 0.80 (0.58, 0.91) | 0.11 | 0.00 | 0.453 | 1 | 0.472 |
| epoch fidelity | val MAE after 8 epochs | 0.94 | 0.76 (0.55, 0.87) | 1.09 | 0.00 | 0.516 | 2 | 0.541 |
| epoch fidelity | val MAE after 9 epochs | 0.94 | 0.76 (0.54, 0.88) | 0.00 | 0.00 | 0.577 | 1 | 0.594 |
| epoch fidelity | val MAE after 10 epochs | 0.94 | 0.76 (0.55, 0.89) | 0.00 | 0.00 | 0.632 | 1 | 0.648 |
| epoch fidelity | val MAE after 11 epochs | 0.94 | 0.79 (0.58, 0.89) | 1.09 | 0.00 | 0.684 | 2 | 0.702 |
| epoch fidelity | val MAE after 12 epochs | 0.94 | 0.81 (0.61, 0.91) | 0.11 | 0.00 | 0.733 | 1 | 0.744 |
| epoch fidelity | val MAE after 13 epochs | 0.94 | 0.79 (0.57, 0.90) | 0.36 | 0.00 | 0.775 | 1 | 0.785 |
| epoch fidelity | val MAE after 14 epochs | 0.94 | 0.83 (0.63, 0.93) | 0.00 | 0.00 | 0.816 | 1 | 0.825 |
| epoch fidelity | val MAE after 15 epochs | 0.94 | 0.84 (0.64, 0.93) | 0.00 | 0.00 | 0.853 | 1 | 0.861 |
| epoch fidelity | val MAE after 16 epochs | 0.94 | 0.85 (0.67, 0.94) | 0.00 | 0.00 | 0.889 | 1 | 0.896 |
| epoch fidelity | val MAE after 17 epochs | 0.94 | 0.86 (0.68, 0.94) | 0.11 | 0.00 | 0.919 | 1 | 0.924 |
| epoch fidelity | val MAE after 18 epochs | 0.94 | 0.86 (0.68, 0.94) | 0.00 | 0.00 | 0.950 | 1 | 0.953 |
| epoch fidelity | val MAE after 19 epochs | 0.94 | 0.86 (0.68, 0.94) | 0.11 | 0.00 | 0.976 | 1 | 0.978 |
| epoch fidelity | val MAE after 20 epochs | 0.94 | 0.85 (0.67, 0.94) | 0.11 | 0.00 | 1.000 | 1 | 1.000 |
| successive halving | r0 = 1, eta = 2 |  |  | 0.00 | 0.00 | 0.204 |  |  |
| successive halving | r0 = 1, eta = 3 |  |  | 0.00 | 0.00 | 0.170 |  |  |
| successive halving | r0 = 2, eta = 2 |  |  | 0.11 | 0.00 | 0.346 |  |  |
| successive halving | r0 = 2, eta = 3 |  |  | 0.00 | 0.00 | 0.322 |  |  |
| successive halving | r0 = 3, eta = 3 |  |  | 0.11 | 0.00 | 0.405 |  |  |
| transfer | pooled rank of the other cities | 0.81 | 0.70 (0.46, 0.85) | 0.00 | 0.00 | 0.000 | 1 | 0.030 |
| random | random picks (mean of 5,000 draws) |  |  | 7.89 | 2.02 | 0.000 |  |  |

## pems04

N = 50; heads {'mse': np.int64(20), 'quantile': np.int64(16), 'mae': np.int64(14)}; sigma_seed 0.00042; std of the label 5.18 sigma_seed; full training of seed 0: 9.5 GPU-hours logged on nibi, 9.5 on the reference unit.

| kind | evaluator | rho | rho inside heads (95 % interval) | regret b = 1 | regret b = 5 | cost share | picks to one sigma | cost to one sigma |
|---|---|---|---|---|---|---|---|---|
| ceiling | seed 0 against the mean of seeds 1 and 2 | 0.96 | 0.96 (0.87, 0.99) |  |  | 1.000 |  |  |
| full training | seed 0, 20 epochs | 0.98 | 0.98 (0.91, 1.00) | 0.19 | 0.00 | 1.000 | 1 | 1.000 |
| epoch fidelity | val MAE after 1 epochs | 0.17 | 0.42 (0.12, 0.64) | 13.79 | 2.67 | 0.057 | 11 | 0.285 |
| epoch fidelity | val MAE after 2 epochs | 0.10 | 0.23 (-0.07, 0.50) | 5.82 | 5.82 | 0.106 | 13 | 0.340 |
| epoch fidelity | val MAE after 3 epochs | 0.27 | 0.43 (0.13, 0.65) | 7.02 | 2.67 | 0.155 | 6 | 0.272 |
| epoch fidelity | val MAE after 4 epochs | 0.45 | 0.52 (0.21, 0.71) | 2.67 | 2.67 | 0.204 | 8 | 0.343 |
| epoch fidelity | val MAE after 5 epochs | 0.52 | 0.56 (0.27, 0.74) | 2.67 | 0.19 | 0.253 | 4 | 0.323 |
| epoch fidelity | val MAE after 6 epochs | 0.61 | 0.70 (0.45, 0.83) | 4.66 | 0.67 | 0.303 | 3 | 0.362 |
| epoch fidelity | val MAE after 7 epochs | 0.75 | 0.74 (0.51, 0.89) | 5.34 | 0.19 | 0.352 | 3 | 0.409 |
| epoch fidelity | val MAE after 8 epochs | 0.81 | 0.83 (0.65, 0.91) | 4.86 | 0.19 | 0.402 | 3 | 0.445 |
| epoch fidelity | val MAE after 9 epochs | 0.81 | 0.82 (0.63, 0.93) | 4.86 | 0.19 | 0.452 | 3 | 0.491 |
| epoch fidelity | val MAE after 10 epochs | 0.82 | 0.83 (0.63, 0.92) | 5.34 | 0.00 | 0.502 | 2 | 0.529 |
| epoch fidelity | val MAE after 11 epochs | 0.89 | 0.89 (0.73, 0.95) | 0.19 | 0.19 | 0.552 | 1 | 0.565 |
| epoch fidelity | val MAE after 12 epochs | 0.91 | 0.93 (0.80, 0.97) | 0.19 | 0.19 | 0.602 | 1 | 0.613 |
| epoch fidelity | val MAE after 13 epochs | 0.89 | 0.89 (0.74, 0.95) | 0.19 | 0.00 | 0.651 | 1 | 0.661 |
| epoch fidelity | val MAE after 14 epochs | 0.93 | 0.92 (0.80, 0.96) | 0.19 | 0.19 | 0.701 | 1 | 0.709 |
| epoch fidelity | val MAE after 15 epochs | 0.93 | 0.93 (0.81, 0.97) | 0.19 | 0.00 | 0.750 | 1 | 0.758 |
| epoch fidelity | val MAE after 16 epochs | 0.94 | 0.93 (0.81, 0.97) | 0.19 | 0.19 | 0.800 | 1 | 0.806 |
| epoch fidelity | val MAE after 17 epochs | 0.94 | 0.94 (0.82, 0.97) | 0.19 | 0.00 | 0.850 | 1 | 0.854 |
| epoch fidelity | val MAE after 18 epochs | 0.94 | 0.93 (0.81, 0.97) | 0.19 | 0.00 | 0.900 | 1 | 0.903 |
| epoch fidelity | val MAE after 19 epochs | 0.95 | 0.95 (0.85, 0.98) | 0.19 | 0.00 | 0.950 | 1 | 0.952 |
| epoch fidelity | val MAE after 20 epochs | 0.94 | 0.93 (0.81, 0.97) | 0.19 | 0.00 | 1.000 | 1 | 1.000 |
| successive halving | r0 = 1, eta = 2 |  |  | 0.67 | 0.67 | 0.163 |  |  |
| successive halving | r0 = 1, eta = 3 |  |  | 0.67 | 0.67 | 0.140 |  |  |
| successive halving | r0 = 2, eta = 2 |  |  | 0.67 | 0.67 | 0.275 |  |  |
| successive halving | r0 = 2, eta = 3 |  |  | 0.67 | 0.67 | 0.238 |  |  |
| successive halving | r0 = 3, eta = 3 |  |  | 0.67 | 0.00 | 0.311 |  |  |
| transfer | pooled rank of the other cities | 0.64 | 0.61 (0.36, 0.79) | 0.00 | 0.00 | 0.000 | 1 | 0.021 |
| random | random picks (mean of 5,000 draws) |  |  | 8.72 | 3.10 | 0.000 |  |  |

## chengdu

N = 50; heads {'mse': np.int64(20), 'quantile': np.int64(16), 'mae': np.int64(14)}; sigma_seed 0.00131; std of the label 3.13 sigma_seed; full training of seed 0: 7.3 GPU-hours logged on rorqual, 7.2 on the reference unit.

| kind | evaluator | rho | rho inside heads (95 % interval) | regret b = 1 | regret b = 5 | cost share | picks to one sigma | cost to one sigma |
|---|---|---|---|---|---|---|---|---|
| ceiling | seed 0 against the mean of seeds 1 and 2 | 0.83 | 0.76 (0.52, 0.89) |  |  | 1.000 |  |  |
| full training | seed 0, 20 epochs | 0.91 | 0.83 (0.63, 0.93) | 0.46 | 0.00 | 1.000 | 1 | 1.000 |
| epoch fidelity | val MAE after 1 epochs | 0.16 | 0.40 (0.10, 0.65) | 3.44 | 1.78 | 0.063 | 9 | 0.236 |
| epoch fidelity | val MAE after 2 epochs | 0.37 | 0.53 (0.25, 0.72) | 1.78 | 1.78 | 0.123 | 6 | 0.199 |
| epoch fidelity | val MAE after 3 epochs | 0.52 | 0.55 (0.32, 0.74) | 3.37 | 1.78 | 0.184 | 6 | 0.264 |
| epoch fidelity | val MAE after 4 epochs | 0.58 | 0.61 (0.35, 0.78) | 3.44 | 0.00 | 0.244 | 3 | 0.297 |
| epoch fidelity | val MAE after 5 epochs | 0.66 | 0.63 (0.36, 0.78) | 3.44 | 0.00 | 0.305 | 2 | 0.346 |
| epoch fidelity | val MAE after 6 epochs | 0.71 | 0.68 (0.44, 0.82) | 3.44 | 0.00 | 0.366 | 2 | 0.403 |
| epoch fidelity | val MAE after 7 epochs | 0.75 | 0.73 (0.53, 0.84) | 3.44 | 0.00 | 0.426 | 2 | 0.452 |
| epoch fidelity | val MAE after 8 epochs | 0.74 | 0.73 (0.51, 0.86) | 3.44 | 0.00 | 0.487 | 2 | 0.510 |
| epoch fidelity | val MAE after 9 epochs | 0.72 | 0.67 (0.45, 0.82) | 0.00 | 0.00 | 0.547 | 1 | 0.567 |
| epoch fidelity | val MAE after 10 epochs | 0.78 | 0.77 (0.56, 0.88) | 0.00 | 0.00 | 0.607 | 1 | 0.624 |
| epoch fidelity | val MAE after 11 epochs | 0.81 | 0.77 (0.54, 0.88) | 0.00 | 0.00 | 0.665 | 1 | 0.681 |
| epoch fidelity | val MAE after 12 epochs | 0.82 | 0.80 (0.59, 0.90) | 3.44 | 0.00 | 0.719 | 2 | 0.738 |
| epoch fidelity | val MAE after 13 epochs | 0.80 | 0.76 (0.51, 0.89) | 0.00 | 0.00 | 0.768 | 1 | 0.779 |
| epoch fidelity | val MAE after 14 epochs | 0.82 | 0.76 (0.53, 0.89) | 0.00 | 0.00 | 0.815 | 1 | 0.825 |
| epoch fidelity | val MAE after 15 epochs | 0.81 | 0.79 (0.58, 0.90) | 0.00 | 0.00 | 0.857 | 1 | 0.865 |
| epoch fidelity | val MAE after 16 epochs | 0.81 | 0.75 (0.51, 0.88) | 0.00 | 0.00 | 0.895 | 1 | 0.901 |
| epoch fidelity | val MAE after 17 epochs | 0.81 | 0.76 (0.54, 0.88) | 0.00 | 0.00 | 0.931 | 1 | 0.935 |
| epoch fidelity | val MAE after 18 epochs | 0.81 | 0.77 (0.55, 0.89) | 0.00 | 0.00 | 0.959 | 1 | 0.961 |
| epoch fidelity | val MAE after 19 epochs | 0.82 | 0.77 (0.56, 0.89) | 0.00 | 0.00 | 0.983 | 1 | 0.983 |
| epoch fidelity | val MAE after 20 epochs | 0.81 | 0.77 (0.54, 0.89) | 0.00 | 0.00 | 1.000 | 1 | 1.000 |
| successive halving | r0 = 1, eta = 2 |  |  | 0.00 | 0.00 | 0.203 |  |  |
| successive halving | r0 = 1, eta = 3 |  |  | 0.00 | 0.00 | 0.163 |  |  |
| successive halving | r0 = 2, eta = 2 |  |  | 0.00 | 0.00 | 0.341 |  |  |
| successive halving | r0 = 2, eta = 3 |  |  | 0.00 | 0.00 | 0.292 |  |  |
| successive halving | r0 = 3, eta = 3 |  |  | 0.00 | 0.00 | 0.346 |  |  |
| transfer | pooled rank of the other cities | 0.46 | 0.66 (0.45, 0.79) | 3.44 | 0.00 | 0.000 | 5 | 0.139 |
| random | random picks (mean of 5,000 draws) |  |  | 5.97 | 2.49 | 0.000 |  |  |

## shenzhen

N = 50; heads {'mse': np.int64(20), 'quantile': np.int64(16), 'mae': np.int64(14)}; sigma_seed 0.00116; std of the label 3.60 sigma_seed; full training of seed 0: 10.4 GPU-hours logged on fir, 11.0 on the reference unit.

| kind | evaluator | rho | rho inside heads (95 % interval) | regret b = 1 | regret b = 5 | cost share | picks to one sigma | cost to one sigma |
|---|---|---|---|---|---|---|---|---|
| ceiling | seed 0 against the mean of seeds 1 and 2 | 0.90 | 0.87 (0.70, 0.93) |  |  | 1.000 |  |  |
| full training | seed 0, 20 epochs | 0.95 | 0.93 (0.81, 0.98) | 0.00 | 0.00 | 1.000 | 1 | 1.000 |
| epoch fidelity | val MAE after 1 epochs | 0.02 | 0.44 (0.13, 0.64) | 9.28 | 4.91 | 0.057 | 12 | 0.284 |
| epoch fidelity | val MAE after 2 epochs | 0.17 | 0.55 (0.30, 0.72) | 1.53 | 1.53 | 0.111 | 8 | 0.243 |
| epoch fidelity | val MAE after 3 epochs | 0.27 | 0.50 (0.18, 0.73) | 4.31 | 1.53 | 0.165 | 6 | 0.270 |
| epoch fidelity | val MAE after 4 epochs | 0.56 | 0.62 (0.34, 0.78) | 3.20 | 1.53 | 0.220 | 12 | 0.404 |
| epoch fidelity | val MAE after 5 epochs | 0.59 | 0.62 (0.36, 0.80) | 3.27 | 1.53 | 0.274 | 7 | 0.354 |
| epoch fidelity | val MAE after 6 epochs | 0.66 | 0.65 (0.36, 0.82) | 1.53 | 0.00 | 0.328 | 4 | 0.388 |
| epoch fidelity | val MAE after 7 epochs | 0.72 | 0.70 (0.44, 0.85) | 1.53 | 1.41 | 0.382 | 7 | 0.482 |
| epoch fidelity | val MAE after 8 epochs | 0.82 | 0.80 (0.57, 0.89) | 1.53 | 0.00 | 0.437 | 2 | 0.469 |
| epoch fidelity | val MAE after 9 epochs | 0.82 | 0.78 (0.53, 0.90) | 1.53 | 0.00 | 0.491 | 3 | 0.527 |
| epoch fidelity | val MAE after 10 epochs | 0.84 | 0.79 (0.58, 0.91) | 1.53 | 0.00 | 0.546 | 2 | 0.572 |
| epoch fidelity | val MAE after 11 epochs | 0.82 | 0.81 (0.58, 0.92) | 1.53 | 0.00 | 0.599 | 2 | 0.623 |
| epoch fidelity | val MAE after 12 epochs | 0.84 | 0.86 (0.69, 0.94) | 0.00 | 0.00 | 0.653 | 1 | 0.667 |
| epoch fidelity | val MAE after 13 epochs | 0.83 | 0.80 (0.58, 0.92) | 0.00 | 0.00 | 0.703 | 1 | 0.715 |
| epoch fidelity | val MAE after 14 epochs | 0.83 | 0.81 (0.58, 0.91) | 1.53 | 0.00 | 0.750 | 3 | 0.776 |
| epoch fidelity | val MAE after 15 epochs | 0.85 | 0.83 (0.61, 0.94) | 1.41 | 0.00 | 0.795 | 2 | 0.812 |
| epoch fidelity | val MAE after 16 epochs | 0.85 | 0.84 (0.62, 0.95) | 1.41 | 0.00 | 0.839 | 2 | 0.853 |
| epoch fidelity | val MAE after 17 epochs | 0.86 | 0.87 (0.69, 0.95) | 0.00 | 0.00 | 0.884 | 1 | 0.889 |
| epoch fidelity | val MAE after 18 epochs | 0.86 | 0.86 (0.65, 0.95) | 1.41 | 0.00 | 0.925 | 2 | 0.932 |
| epoch fidelity | val MAE after 19 epochs | 0.86 | 0.86 (0.67, 0.95) | 0.00 | 0.00 | 0.963 | 1 | 0.965 |
| epoch fidelity | val MAE after 20 epochs | 0.86 | 0.88 (0.69, 0.95) | 1.41 | 0.00 | 1.000 | 2 | 1.000 |
| successive halving | r0 = 1, eta = 2 |  |  | 1.53 | 1.53 | 0.163 |  |  |
| successive halving | r0 = 1, eta = 3 |  |  | 1.53 | 1.53 | 0.139 |  |  |
| successive halving | r0 = 2, eta = 2 |  |  | 0.00 | 0.00 | 0.285 |  |  |
| successive halving | r0 = 2, eta = 3 |  |  | 0.00 | 0.00 | 0.240 |  |  |
| successive halving | r0 = 3, eta = 3 |  |  | 0.00 | 0.00 | 0.327 |  |  |
| transfer | pooled rank of the other cities | 0.80 | 0.83 (0.65, 0.92) | 1.53 | 0.00 | 0.000 | 4 | 0.115 |
| random | random picks (mean of 5,000 draws) |  |  | 6.74 | 2.93 | 0.000 |  |  |

## expytky

N = 50; heads {'mse': np.int64(20), 'quantile': np.int64(16), 'mae': np.int64(14)}; sigma_seed 0.00188; std of the label 2.67 sigma_seed; full training of seed 0: 19.3 GPU-hours logged on rorqual, 19.1 on the reference unit.

| kind | evaluator | rho | rho inside heads (95 % interval) | regret b = 1 | regret b = 5 | cost share | picks to one sigma | cost to one sigma |
|---|---|---|---|---|---|---|---|---|
| ceiling | seed 0 against the mean of seeds 1 and 2 | 0.84 | 0.82 (0.61, 0.91) |  |  | 1.000 |  |  |
| full training | seed 0, 20 epochs | 0.92 | 0.91 (0.77, 0.95) | 0.00 | 0.00 | 1.000 | 1 | 1.000 |
| epoch fidelity | val MAE after 1 epochs | -0.15 | 0.10 (-0.21, 0.40) | 0.00 | 0.00 | 0.077 | 1 | 0.090 |
| epoch fidelity | val MAE after 2 epochs | 0.21 | 0.52 (0.27, 0.74) | 0.00 | 0.00 | 0.153 | 1 | 0.165 |
| epoch fidelity | val MAE after 3 epochs | 0.50 | 0.61 (0.36, 0.81) | 0.00 | 0.00 | 0.229 | 1 | 0.239 |
| epoch fidelity | val MAE after 4 epochs | 0.68 | 0.62 (0.35, 0.79) | 0.00 | 0.00 | 0.304 | 1 | 0.314 |
| epoch fidelity | val MAE after 5 epochs | 0.79 | 0.64 (0.37, 0.81) | 0.00 | 0.00 | 0.380 | 1 | 0.389 |
| epoch fidelity | val MAE after 6 epochs | 0.81 | 0.66 (0.40, 0.84) | 0.00 | 0.00 | 0.456 | 1 | 0.463 |
| epoch fidelity | val MAE after 7 epochs | 0.84 | 0.67 (0.41, 0.84) | 0.00 | 0.00 | 0.532 | 1 | 0.538 |
| epoch fidelity | val MAE after 8 epochs | 0.89 | 0.76 (0.54, 0.89) | 0.00 | 0.00 | 0.608 | 1 | 0.613 |
| epoch fidelity | val MAE after 9 epochs | 0.88 | 0.72 (0.47, 0.87) | 0.00 | 0.00 | 0.678 | 1 | 0.682 |
| epoch fidelity | val MAE after 10 epochs | 0.90 | 0.78 (0.57, 0.88) | 1.15 | 0.00 | 0.738 | 2 | 0.743 |
| epoch fidelity | val MAE after 11 epochs | 0.89 | 0.77 (0.55, 0.88) | 1.15 | 0.00 | 0.790 | 2 | 0.794 |
| epoch fidelity | val MAE after 12 epochs | 0.88 | 0.75 (0.52, 0.87) | 0.00 | 0.00 | 0.840 | 1 | 0.840 |
| epoch fidelity | val MAE after 13 epochs | 0.88 | 0.76 (0.54, 0.88) | 1.15 | 0.00 | 0.878 | 2 | 0.880 |
| epoch fidelity | val MAE after 14 epochs | 0.87 | 0.76 (0.53, 0.88) | 1.15 | 0.00 | 0.910 | 2 | 0.912 |
| epoch fidelity | val MAE after 15 epochs | 0.88 | 0.75 (0.53, 0.87) | 1.15 | 0.00 | 0.940 | 2 | 0.941 |
| epoch fidelity | val MAE after 16 epochs | 0.89 | 0.76 (0.54, 0.87) | 1.15 | 0.00 | 0.962 | 2 | 0.963 |
| epoch fidelity | val MAE after 17 epochs | 0.88 | 0.74 (0.52, 0.86) | 1.15 | 0.00 | 0.982 | 2 | 0.983 |
| epoch fidelity | val MAE after 18 epochs | 0.88 | 0.75 (0.53, 0.87) | 1.15 | 0.00 | 0.991 | 2 | 0.991 |
| epoch fidelity | val MAE after 19 epochs | 0.88 | 0.75 (0.53, 0.87) | 1.15 | 0.00 | 0.997 | 2 | 0.997 |
| epoch fidelity | val MAE after 20 epochs | 0.88 | 0.75 (0.53, 0.87) | 1.15 | 0.00 | 1.000 | 2 | 1.000 |
| successive halving | r0 = 1, eta = 2 |  |  | 0.00 | 0.00 | 0.247 |  |  |
| successive halving | r0 = 1, eta = 3 |  |  | 0.00 | 0.00 | 0.207 |  |  |
| successive halving | r0 = 2, eta = 2 |  |  | 0.00 | 0.00 | 0.365 |  |  |
| successive halving | r0 = 2, eta = 3 |  |  | 0.00 | 0.00 | 0.313 |  |  |
| successive halving | r0 = 3, eta = 3 |  |  | 1.15 | 0.00 | 0.420 |  |  |
| transfer | pooled rank of the other cities | 0.81 | 0.68 (0.42, 0.82) | 0.00 | 0.00 | 0.000 | 1 | 0.015 |
| random | random picks (mean of 5,000 draws) |  |  | 5.39 | 2.32 | 0.000 |  |  |

## pemsbay

N = 50; heads {'mse': np.int64(20), 'quantile': np.int64(16), 'mae': np.int64(14)}; sigma_seed 0.00110; std of the label 6.23 sigma_seed; full training of seed 0: 31.8 GPU-hours logged on narval, 25.4 on the reference unit.

| kind | evaluator | rho | rho inside heads (95 % interval) | regret b = 1 | regret b = 5 | cost share | picks to one sigma | cost to one sigma |
|---|---|---|---|---|---|---|---|---|
| ceiling | seed 0 against the mean of seeds 1 and 2 | 0.89 | 0.79 (0.60, 0.91) |  |  | 1.000 |  |  |
| full training | seed 0, 20 epochs | 0.96 | 0.90 (0.75, 0.96) | 0.00 | 0.00 | 1.000 | 1 | 1.000 |
| epoch fidelity | val MAE after 1 epochs | 0.58 | 0.40 (0.11, 0.62) | 1.60 | 0.00 | 0.059 | 2 | 0.101 |
| epoch fidelity | val MAE after 2 epochs | 0.70 | 0.52 (0.26, 0.71) | 0.32 | 0.32 | 0.117 | 1 | 0.136 |
| epoch fidelity | val MAE after 3 epochs | 0.73 | 0.67 (0.41, 0.82) | 2.81 | 0.00 | 0.174 | 2 | 0.219 |
| epoch fidelity | val MAE after 4 epochs | 0.76 | 0.58 (0.30, 0.74) | 1.60 | 0.32 | 0.232 | 3 | 0.299 |
| epoch fidelity | val MAE after 5 epochs | 0.76 | 0.62 (0.35, 0.78) | 0.86 | 0.00 | 0.290 | 1 | 0.314 |
| epoch fidelity | val MAE after 6 epochs | 0.82 | 0.76 (0.53, 0.87) | 0.00 | 0.00 | 0.348 | 1 | 0.369 |
| epoch fidelity | val MAE after 7 epochs | 0.84 | 0.77 (0.54, 0.88) | 0.32 | 0.00 | 0.406 | 1 | 0.420 |
| epoch fidelity | val MAE after 8 epochs | 0.81 | 0.69 (0.42, 0.85) | 0.32 | 0.00 | 0.464 | 1 | 0.476 |
| epoch fidelity | val MAE after 9 epochs | 0.83 | 0.75 (0.53, 0.87) | 0.00 | 0.00 | 0.522 | 1 | 0.538 |
| epoch fidelity | val MAE after 10 epochs | 0.84 | 0.73 (0.48, 0.87) | 0.00 | 0.00 | 0.578 | 1 | 0.593 |
| epoch fidelity | val MAE after 11 epochs | 0.86 | 0.82 (0.63, 0.91) | 0.00 | 0.00 | 0.628 | 1 | 0.642 |
| epoch fidelity | val MAE after 12 epochs | 0.86 | 0.80 (0.59, 0.90) | 0.00 | 0.00 | 0.678 | 1 | 0.690 |
| epoch fidelity | val MAE after 13 epochs | 0.87 | 0.83 (0.64, 0.93) | 0.00 | 0.00 | 0.726 | 1 | 0.737 |
| epoch fidelity | val MAE after 14 epochs | 0.91 | 0.83 (0.63, 0.92) | 0.00 | 0.00 | 0.773 | 1 | 0.782 |
| epoch fidelity | val MAE after 15 epochs | 0.92 | 0.82 (0.62, 0.92) | 0.00 | 0.00 | 0.818 | 1 | 0.825 |
| epoch fidelity | val MAE after 16 epochs | 0.93 | 0.84 (0.64, 0.94) | 0.00 | 0.00 | 0.857 | 1 | 0.863 |
| epoch fidelity | val MAE after 17 epochs | 0.92 | 0.81 (0.59, 0.92) | 0.00 | 0.00 | 0.894 | 1 | 0.899 |
| epoch fidelity | val MAE after 18 epochs | 0.93 | 0.83 (0.62, 0.93) | 0.00 | 0.00 | 0.932 | 1 | 0.935 |
| epoch fidelity | val MAE after 19 epochs | 0.93 | 0.84 (0.64, 0.94) | 0.00 | 0.00 | 0.968 | 1 | 0.969 |
| epoch fidelity | val MAE after 20 epochs | 0.93 | 0.84 (0.63, 0.93) | 0.00 | 0.00 | 1.000 | 1 | 1.000 |
| successive halving | r0 = 1, eta = 2 |  |  | 0.32 | 0.32 | 0.195 |  |  |
| successive halving | r0 = 1, eta = 3 |  |  | 0.00 | 0.00 | 0.144 |  |  |
| successive halving | r0 = 2, eta = 2 |  |  | 0.00 | 0.00 | 0.319 |  |  |
| successive halving | r0 = 2, eta = 3 |  |  | 0.32 | 0.32 | 0.261 |  |  |
| successive halving | r0 = 3, eta = 3 |  |  | 0.00 | 0.00 | 0.371 |  |  |
| transfer | pooled rank of the other cities | 0.67 | 0.37 (0.06, 0.63) | 0.32 | 0.00 | 0.000 | 1 | 0.022 |
| random | random picks (mean of 5,000 draws) |  |  | 7.87 | 1.83 | 0.000 |  |  |
