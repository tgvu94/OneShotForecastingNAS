# evalscreen variance: which design axis moves the label

Label = test MAE, seed 0. marginal_r2 = adjusted R2 of a one-axis model (the share of the label variance that the axis explains alone), with a bootstrap CI; unique_r2 = the adjusted R2 of the additive model of all axes minus that of the model without the axis. (seed) = sigma_seed squared over the label variance. axis_var_over_seed_var = marginal_r2 over the seed share; the rule of the map gives an axis a search budget only above 1. best_level_gain_sigma = the mean of the list minus the mean of the best level of the axis, in sigma_seed; level_range_sigma = worst level mean minus best level mean (levels with 5 architectures or more). 'MAE head only' repeats the analysis with the head fixed.

### metrla, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.780 |  |  |  | 24.927 |  |  |  |
| (seed) | 150 | 0.031 |  |  |  | 1.000 |  |  |  |
| head | 150 | 0.709 | 0.526 | 0.843 | 0.726 | 22.668 | mae | 5.069 | 11.171 |
| decoder | 150 | -0.000 | -0.007 | 0.049 | 0.026 | -0.002 | seq | 0.407 | 0.925 |
| seq_family | 150 | 0.045 | 0.011 | 0.176 | 0.001 | 1.447 | mlp_mix | 3.509 | 5.453 |
| graph_family | 150 | 0.040 | -0.015 | 0.166 | 0.012 | 1.286 | gcn | 1.062 | 1.846 |
| flat_family | 150 | -0.005 | -0.021 | 0.106 | 0.001 | -0.164 | nbeats_g | 1.599 | 2.547 |
| log_params | 150 | 0.009 | -0.007 | 0.103 | 0.014 | 0.298 |  |  |  |

### metrla, MAE head only

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 40 | 0.359 |  |  |  | 1.823 |  |  |  |
| (seed) | 40 | 0.197 |  |  |  | 1.000 |  |  |  |
| decoder | 40 | 0.291 | 0.114 | 0.487 | 0.401 | 1.477 | seq | 1.237 | 2.474 |
| seq_family | 40 | -0.004 | -0.058 | 0.379 | 0.005 | -0.023 | mlp_mix | 1.509 | 2.078 |
| graph_family | 40 | 0.001 | -0.070 | 0.326 | 0.053 | 0.007 | none | 0.190 | 1.052 |
| flat_family | 40 | 0.050 | -0.085 | 0.435 | 0.061 | 0.252 | nbeats_s | 0.705 | 2.141 |
| log_params | 40 | -0.026 | -0.026 | 0.158 | 0.023 | -0.132 |  |  |  |

### pems04, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.519 |  |  |  | 15.332 |  |  |  |
| (seed) | 150 | 0.034 |  |  |  | 1.000 |  |  |  |
| head | 150 | 0.094 | 0.005 | 0.268 | 0.155 | 2.767 | mae | 2.443 | 4.461 |
| decoder | 150 | 0.174 | 0.096 | 0.279 | 0.223 | 5.143 | seq | 2.035 | 4.625 |
| seq_family | 150 | 0.053 | 0.009 | 0.206 | 0.018 | 1.577 | mlp_mix | 2.373 | 4.805 |
| graph_family | 150 | 0.072 | 0.009 | 0.187 | 0.128 | 2.115 | adaptive-only | 2.396 | 4.252 |
| flat_family | 150 | 0.053 | 0.007 | 0.178 | 0.014 | 1.556 | nbeats_g | 3.120 | 4.590 |
| log_params | 150 | 0.050 | 0.009 | 0.148 | 0.024 | 1.466 |  |  |  |

### pems04, MAE head only

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 40 | 0.242 |  |  |  | 12.345 |  |  |  |
| (seed) | 40 | 0.020 |  |  |  | 1.000 |  |  |  |
| decoder | 40 | 0.219 | 0.070 | 0.573 | 0.291 | 11.140 | seq | 3.443 | 6.886 |
| seq_family | 40 | 0.010 | -0.048 | 0.342 | -0.111 | 0.493 | mlp_mix | 3.084 | 7.575 |
| graph_family | 40 | 0.156 | 0.045 | 0.467 | 0.090 | 7.957 | adaptive-only | 2.892 | 7.041 |
| flat_family | 40 | 0.089 | -0.026 | 0.347 | -0.098 | 4.515 | nbeats_g | 3.140 | 7.939 |
| log_params | 40 | -0.026 | -0.026 | 0.072 | -0.030 | -1.338 |  |  |  |

### chengdu, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.586 |  |  |  | 7.727 |  |  |  |
| (seed) | 150 | 0.076 |  |  |  | 1.000 |  |  |  |
| head | 150 | 0.149 | 0.072 | 0.259 | 0.168 | 1.961 | mae | 1.927 | 3.637 |
| decoder | 150 | 0.290 | 0.192 | 0.386 | 0.252 | 3.819 | seq | 1.741 | 3.956 |
| seq_family | 150 | 0.027 | -0.006 | 0.164 | -0.010 | 0.358 | mlp_mix | 1.606 | 2.960 |
| graph_family | 150 | 0.153 | 0.067 | 0.290 | 0.081 | 2.013 | none | 2.034 | 4.471 |
| flat_family | 150 | -0.012 | -0.021 | 0.074 | -0.008 | -0.155 | nbeats_g | 0.566 | 1.250 |
| log_params | 150 | 0.052 | 0.000 | 0.142 | 0.014 | 0.687 |  |  |  |

### chengdu, MAE head only

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 40 | 0.600 |  |  |  | 4.741 |  |  |  |
| (seed) | 40 | 0.126 |  |  |  | 1.000 |  |  |  |
| decoder | 40 | 0.509 | 0.344 | 0.677 | 0.734 | 4.024 | seq | 2.005 | 4.010 |
| seq_family | 40 | -0.147 | -0.117 | 0.306 | -0.047 | -1.161 | mlp_mix | 0.273 | 0.822 |
| graph_family | 40 | 0.035 | -0.041 | 0.369 | 0.089 | 0.281 | none | 0.908 | 2.030 |
| flat_family | 40 | -0.033 | -0.099 | 0.347 | 0.052 | -0.259 | skip_connection | 1.262 | 2.348 |
| log_params | 40 | -0.023 | -0.026 | 0.100 | -0.017 | -0.178 |  |  |  |

### shenzhen, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.668 |  |  |  | 9.907 |  |  |  |
| (seed) | 150 | 0.067 |  |  |  | 1.000 |  |  |  |
| head | 150 | 0.291 | 0.193 | 0.423 | 0.326 | 4.318 | mae | 2.540 | 5.149 |
| decoder | 150 | 0.205 | 0.097 | 0.312 | 0.207 | 3.036 | seq | 1.559 | 3.544 |
| seq_family | 150 | 0.062 | 0.014 | 0.200 | 0.001 | 0.922 | mlp_mix | 2.232 | 4.351 |
| graph_family | 150 | 0.094 | 0.001 | 0.228 | 0.047 | 1.393 | none | 1.264 | 3.162 |
| flat_family | 150 | -0.013 | -0.023 | 0.083 | 0.008 | -0.189 | nbeats_g | 0.917 | 1.290 |
| log_params | 150 | 0.074 | 0.006 | 0.163 | 0.033 | 1.103 |  |  |  |

### shenzhen, MAE head only

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 40 | 0.565 |  |  |  | 5.401 |  |  |  |
| (seed) | 40 | 0.105 |  |  |  | 1.000 |  |  |  |
| decoder | 40 | 0.465 | 0.305 | 0.626 | 0.435 | 4.444 | seq | 2.112 | 4.224 |
| seq_family | 40 | -0.044 | -0.096 | 0.390 | -0.062 | -0.416 | mlp_mix | 1.403 | 2.629 |
| graph_family | 40 | 0.033 | -0.052 | 0.355 | 0.065 | 0.318 | none | 0.597 | 1.488 |
| flat_family | 40 | 0.105 | -0.059 | 0.483 | 0.075 | 1.004 | skip_connection | 1.129 | 3.362 |
| log_params | 40 | 0.014 | -0.026 | 0.182 | 0.007 | 0.132 |  |  |  |

### expytky, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.395 |  |  |  | 4.096 |  |  |  |
| (seed) | 150 | 0.096 |  |  |  | 1.000 |  |  |  |
| head | 150 | 0.272 | 0.151 | 0.421 | 0.285 | 2.820 | mae | 2.426 | 4.328 |
| decoder | 150 | 0.070 | 0.015 | 0.154 | 0.054 | 0.728 | seq | 0.786 | 1.787 |
| seq_family | 150 | 0.035 | -0.002 | 0.172 | -0.008 | 0.366 | mlp_mix | 1.778 | 3.263 |
| graph_family | 150 | 0.028 | -0.005 | 0.135 | -0.008 | 0.288 | adaptive-only | 1.199 | 2.595 |
| flat_family | 150 | 0.014 | -0.014 | 0.133 | 0.001 | 0.143 | nbeats_g | 0.960 | 1.845 |
| log_params | 150 | 0.042 | -0.005 | 0.131 | 0.013 | 0.439 |  |  |  |

### expytky, MAE head only

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 40 | 0.070 |  |  |  | 0.752 |  |  |  |
| (seed) | 40 | 0.094 |  |  |  | 1.000 |  |  |  |
| decoder | 40 | 0.231 | 0.071 | 0.446 | 0.172 | 2.470 | seq | 1.617 | 3.233 |
| seq_family | 40 | -0.118 | -0.141 | 0.313 | -0.120 | -1.256 | mlp_mix | 0.840 | 1.700 |
| graph_family | 40 | -0.027 | -0.070 | 0.286 | -0.031 | -0.293 | adaptive-only | 0.184 | 0.524 |
| flat_family | 40 | 0.050 | -0.081 | 0.405 | 0.051 | 0.539 | mlp | 1.063 | 3.165 |
| log_params | 40 | 0.010 | -0.026 | 0.179 | -0.038 | 0.110 |  |  |  |

### pemsbay, all heads

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 150 | 0.737 |  |  |  | 23.737 |  |  |  |
| (seed) | 150 | 0.031 |  |  |  | 1.000 |  |  |  |
| head | 150 | 0.709 | 0.594 | 0.804 | 0.712 | 22.858 | mae | 4.648 | 10.857 |
| decoder | 150 | 0.013 | -0.007 | 0.081 | 0.003 | 0.405 | linear | 0.884 | 1.579 |
| seq_family | 150 | -0.003 | -0.017 | 0.129 | -0.005 | -0.100 | mlp_mix | 2.078 | 3.815 |
| graph_family | 150 | 0.023 | -0.018 | 0.153 | 0.008 | 0.729 | gcn | 1.396 | 1.841 |
| flat_family | 150 | -0.013 | -0.021 | 0.094 | -0.004 | -0.414 | nbeats_g | 1.229 | 1.977 |
| log_params | 150 | 0.003 | -0.007 | 0.065 | 0.021 | 0.098 |  |  |  |

### pemsbay, MAE head only

| axis | n | marginal_r2 | ci_lo | ci_hi | unique_r2 | axis_var_over_seed_var | best_level | best_level_gain_sigma | level_range_sigma |
|---|---|---|---|---|---|---|---|---|---|
| (all axes, additive) | 40 | -0.084 |  |  |  | -1.063 |  |  |  |
| (seed) | 40 | 0.079 |  |  |  | 1.000 |  |  |  |
| decoder | 40 | -0.005 | -0.026 | 0.126 | -0.035 | -0.065 | seq | 0.506 | 1.013 |
| seq_family | 40 | -0.091 | -0.120 | 0.316 | -0.121 | -1.154 | tcn | 0.429 | 1.962 |
| graph_family | 40 | -0.024 | -0.074 | 0.224 | -0.106 | -0.305 | adaptive-only | 0.473 | 1.386 |
| flat_family | 40 | 0.112 | -0.014 | 0.423 | -0.027 | 1.422 | nbeats_g | 1.913 | 4.366 |
| log_params | 40 | 0.102 | -0.025 | 0.401 | -0.015 | 1.302 |  |  |  |
