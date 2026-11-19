# largestsd: composite with a learned gate over (window, sensor) cells

Test split; the gate is fit on the second half of the validation windows, one gate per seed; sigma_seed of the full model 0.039.  gate_positive: every cell with a positive predicted gain, its share is measured.

| score | share of cells | test MAE | sd of 3 seeds | gain kept | above the full model, in sigma_seed |
|---|---|---|---|---|---|
| base | 0.00 | 18.082 | 0.051 | 0.000 | 13.5 |
| full | 1.00 | 17.557 | 0.039 | 1.000 | 0.0 |
| gate | 0.10 | 17.876 | 0.035 | 0.391 | 8.2 |
| gate | 0.25 | 17.763 | 0.030 | 0.607 | 5.3 |
| gate | 0.50 | 17.662 | 0.029 | 0.800 | 2.7 |
| gate_time | 0.10 | 17.895 | 0.027 | 0.356 | 8.7 |
| gate_time | 0.25 | 17.824 | 0.024 | 0.490 | 6.9 |
| gate_time | 0.50 | 17.725 | 0.030 | 0.679 | 4.3 |
| rnd | 0.10 | 18.029 | 0.048 | 0.100 | 12.1 |
| rnd | 0.25 | 17.951 | 0.044 | 0.249 | 10.1 |
| rnd | 0.50 | 17.821 | 0.040 | 0.498 | 6.8 |
| gate_positive | 0.66 | 17.622 | 0.026 | 0.876 | 1.7 |
