# evalscreen variance: which design axis moves the label

Label = test MAE, seed 0. marginal_r2 = adjusted R2 of a one-axis model (the share of the label variance that the axis explains alone), with a bootstrap CI; unique_r2 = the adjusted R2 of the additive model of all axes minus that of the model without the axis. (seed) = sigma_seed squared over the label variance. axis_var_over_seed_var = marginal_r2 over the seed share; the rule of the map gives an axis a search budget only above 1. best_level_gain_sigma = the mean of the list minus the mean of the best level of the axis, in sigma_seed; level_range_sigma = worst level mean minus best level mean (levels with 5 architectures or more). 'MAE head only' repeats the analysis with the head fixed.

### metrla, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.780 |  |  |  | 4.110 |  |  |  |
| (seed) | 150 | 0.190 |  |  |  | 1.000 |  |  |  |
| head | 150 | 0.709 | 0.526 | 0.843 | 0.726 | 3.738 | mae | 2.059 | 4.536 |
| decoder | 150 | -0.000 | -0.007 | 0.049 | 0.026 | -0.000 | seq | 0.165 | 0.376 |
| seq_family | 150 | 0.045 | 0.011 | 0.176 | 0.001 | 0.239 | mlp_mix | 1.425 | 2.214 |
| graph_family | 150 | 0.040 | -0.015 | 0.166 | 0.012 | 0.212 | gcn | 0.431 | 0.750 |
| flat_family | 150 | -0.005 | -0.021 | 0.106 | 0.001 | -0.027 | nbeats_g | 0.649 | 1.034 |
| log_params | 150 | 0.009 | -0.007 | 0.103 | 0.014 | 0.049 |  |  |  |

### metrla, MAE head only

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 40 | 0.359 |  |  |  | 0.301 |  |  |  |
| (seed) | 40 | 1.193 |  |  |  | 1.000 |  |  |  |
| decoder | 40 | 0.291 | 0.114 | 0.487 | 0.401 | 0.244 | seq | 0.502 | 1.005 |
| seq_family | 40 | -0.004 | -0.058 | 0.379 | 0.005 | -0.004 | mlp_mix | 0.613 | 0.844 |
| graph_family | 40 | 0.001 | -0.070 | 0.326 | 0.053 | 0.001 | none | 0.077 | 0.427 |
| flat_family | 40 | 0.050 | -0.085 | 0.435 | 0.061 | 0.042 | nbeats_s | 0.286 | 0.870 |
| log_params | 40 | -0.026 | -0.026 | 0.158 | 0.023 | -0.022 |  |  |  |

### pems04, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.519 |  |  |  | 36.892 |  |  |  |
| (seed) | 150 | 0.014 |  |  |  | 1.000 |  |  |  |
| head | 150 | 0.094 | 0.005 | 0.268 | 0.155 | 6.658 | mae | 3.790 | 6.919 |
| decoder | 150 | 0.174 | 0.096 | 0.279 | 0.223 | 12.374 | seq | 3.157 | 7.174 |
| seq_family | 150 | 0.053 | 0.009 | 0.206 | 0.018 | 3.794 | mlp_mix | 3.681 | 7.453 |
| graph_family | 150 | 0.072 | 0.009 | 0.187 | 0.128 | 5.089 | adaptive-only | 3.717 | 6.596 |
| flat_family | 150 | 0.053 | 0.007 | 0.178 | 0.014 | 3.744 | nbeats_g | 4.840 | 7.120 |
| log_params | 150 | 0.050 | 0.009 | 0.148 | 0.024 | 3.527 |  |  |  |

### pems04, MAE head only

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 40 | 0.242 |  |  |  | 29.705 |  |  |  |
| (seed) | 40 | 0.008 |  |  |  | 1.000 |  |  |  |
| decoder | 40 | 0.219 | 0.070 | 0.573 | 0.291 | 26.805 | seq | 5.341 | 10.682 |
| seq_family | 40 | 0.010 | -0.048 | 0.342 | -0.111 | 1.186 | mlp_mix | 4.783 | 11.751 |
| graph_family | 40 | 0.156 | 0.045 | 0.467 | 0.090 | 19.145 | adaptive-only | 4.487 | 10.921 |
| flat_family | 40 | 0.089 | -0.026 | 0.347 | -0.098 | 10.863 | nbeats_g | 4.871 | 12.315 |
| log_params | 40 | -0.026 | -0.026 | 0.072 | -0.030 | -3.220 |  |  |  |

### chengdu, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.586 |  |  |  | 4.110 |  |  |  |
| (seed) | 150 | 0.143 |  |  |  | 1.000 |  |  |  |
| head | 150 | 0.149 | 0.072 | 0.259 | 0.168 | 1.043 | mae | 1.406 | 2.653 |
| decoder | 150 | 0.290 | 0.192 | 0.386 | 0.252 | 2.031 | seq | 1.269 | 2.885 |
| seq_family | 150 | 0.027 | -0.006 | 0.164 | -0.010 | 0.190 | mlp_mix | 1.172 | 2.159 |
| graph_family | 150 | 0.153 | 0.067 | 0.290 | 0.081 | 1.071 | none | 1.483 | 3.261 |
| flat_family | 150 | -0.012 | -0.021 | 0.074 | -0.008 | -0.082 | nbeats_g | 0.413 | 0.912 |
| log_params | 150 | 0.052 | 0.000 | 0.142 | 0.014 | 0.366 |  |  |  |

### chengdu, MAE head only

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 40 | 0.600 |  |  |  | 2.522 |  |  |  |
| (seed) | 40 | 0.238 |  |  |  | 1.000 |  |  |  |
| decoder | 40 | 0.509 | 0.344 | 0.677 | 0.734 | 2.140 | seq | 1.462 | 2.925 |
| seq_family | 40 | -0.147 | -0.117 | 0.306 | -0.047 | -0.618 | mlp_mix | 0.199 | 0.599 |
| graph_family | 40 | 0.035 | -0.041 | 0.369 | 0.089 | 0.149 | none | 0.662 | 1.480 |
| flat_family | 40 | -0.033 | -0.099 | 0.347 | 0.052 | -0.138 | skip_connection | 0.920 | 1.713 |
| log_params | 40 | -0.023 | -0.026 | 0.100 | -0.017 | -0.095 |  |  |  |

### shenzhen, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.668 |  |  |  | 6.782 |  |  |  |
| (seed) | 150 | 0.099 |  |  |  | 1.000 |  |  |  |
| head | 150 | 0.291 | 0.193 | 0.423 | 0.326 | 2.956 | mae | 2.101 | 4.260 |
| decoder | 150 | 0.205 | 0.097 | 0.312 | 0.207 | 2.078 | seq | 1.290 | 2.932 |
| seq_family | 150 | 0.062 | 0.014 | 0.200 | 0.001 | 0.631 | mlp_mix | 1.846 | 3.600 |
| graph_family | 150 | 0.094 | 0.001 | 0.228 | 0.047 | 0.954 | none | 1.045 | 2.617 |
| flat_family | 150 | -0.013 | -0.023 | 0.083 | 0.008 | -0.129 | nbeats_g | 0.759 | 1.067 |
| log_params | 150 | 0.074 | 0.006 | 0.163 | 0.033 | 0.755 |  |  |  |

### shenzhen, MAE head only

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 40 | 0.565 |  |  |  | 3.697 |  |  |  |
| (seed) | 40 | 0.153 |  |  |  | 1.000 |  |  |  |
| decoder | 40 | 0.465 | 0.305 | 0.626 | 0.435 | 3.042 | seq | 1.748 | 3.495 |
| seq_family | 40 | -0.044 | -0.096 | 0.390 | -0.062 | -0.285 | mlp_mix | 1.161 | 2.175 |
| graph_family | 40 | 0.033 | -0.052 | 0.355 | 0.065 | 0.218 | none | 0.494 | 1.231 |
| flat_family | 40 | 0.105 | -0.059 | 0.483 | 0.075 | 0.688 | skip_connection | 0.934 | 2.782 |
| log_params | 40 | 0.014 | -0.026 | 0.182 | 0.007 | 0.090 |  |  |  |
