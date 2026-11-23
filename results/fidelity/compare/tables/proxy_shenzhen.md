# fidelity: proxy tasks at shenzhen

N = 50; label = mean test MAE of seeds 0 to 2 at the city; sigma_seed 0.00116. Proxy runs: seed 0. Baseline = the epoch fidelity of the city at the same cost share (linear between two k). d = rho inside heads less the baseline.

| setting | score | rho | rho inside heads (95 % interval) | baseline at this cost | d | regret b = 1 | regret b = 5 | cost share | cost to one sigma |
|---|---|---|---|---|---|---|---|---|---|
| both_s25_t25 | best val MAE of the run | 0.72 | 0.72 (0.52, 0.82) | 0.52 | 0.21 | 3.20 | 1.41 | 0.174 | 0.332 |
| both_s25_t25 | val MAE after 1 epochs | 0.08 | 0.37 (0.10, 0.58) | 0.44 | -0.06 | 1.53 | 0.00 | 0.010 | 0.104 |
| both_s25_t25 | val MAE after 2 epochs | 0.08 | 0.63 (0.40, 0.76) | 0.44 | 0.19 | 6.48 | 0.00 | 0.019 | 0.070 |
| both_s25_t25 | val MAE after 3 epochs | 0.19 | 0.63 (0.41, 0.79) | 0.44 | 0.20 | 3.20 | 1.53 | 0.028 | 0.266 |
| both_s25_t25 | val MAE after 4 epochs | 0.31 | 0.76 (0.57, 0.86) | 0.44 | 0.32 | 3.20 | 1.53 | 0.037 | 0.392 |
| both_s25_t25 | val MAE after 5 epochs | 0.43 | 0.74 (0.53, 0.83) | 0.44 | 0.30 | 3.20 | 1.53 | 0.046 | 0.188 |
| both_s25_t25 | val MAE after 6 epochs | 0.48 | 0.78 (0.57, 0.88) | 0.44 | 0.34 | 3.20 | 1.53 | 0.055 | 0.193 |
| both_s25_t25 | val MAE after 7 epochs | 0.59 | 0.73 (0.52, 0.85) | 0.45 | 0.28 | 3.20 | 1.53 | 0.064 | 0.253 |
| both_s25_t25 | val MAE after 8 epochs | 0.64 | 0.74 (0.54, 0.84) | 0.47 | 0.27 | 1.53 | 1.53 | 0.073 | 0.242 |
| both_s25_t25 | val MAE after 9 epochs | 0.64 | 0.66 (0.43, 0.79) | 0.49 | 0.17 | 3.20 | 1.53 | 0.082 | 0.272 |
| both_s25_t25 | val MAE after 10 epochs | 0.67 | 0.72 (0.53, 0.83) | 0.51 | 0.21 | 1.53 | 1.53 | 0.091 | 0.319 |
| both_s25_t25 | val MAE after 11 epochs | 0.70 | 0.77 (0.58, 0.86) | 0.53 | 0.24 | 3.20 | 1.41 | 0.100 | 0.233 |
| both_s25_t25 | val MAE after 12 epochs | 0.71 | 0.72 (0.49, 0.84) | 0.55 | 0.17 | 3.20 | 0.00 | 0.109 | 0.184 |
| both_s25_t25 | val MAE after 13 epochs | 0.69 | 0.69 (0.46, 0.79) | 0.55 | 0.14 | 3.20 | 1.41 | 0.118 | 0.337 |
| both_s25_t25 | val MAE after 14 epochs | 0.69 | 0.72 (0.51, 0.83) | 0.54 | 0.18 | 1.53 | 1.41 | 0.127 | 0.294 |
| both_s25_t25 | val MAE after 15 epochs | 0.72 | 0.74 (0.54, 0.83) | 0.53 | 0.21 | 3.20 | 1.41 | 0.135 | 0.312 |
| both_s25_t25 | val MAE after 16 epochs | 0.71 | 0.71 (0.51, 0.82) | 0.52 | 0.19 | 3.20 | 1.41 | 0.143 | 0.310 |
| both_s25_t25 | val MAE after 17 epochs | 0.72 | 0.73 (0.53, 0.84) | 0.51 | 0.22 | 3.20 | 1.41 | 0.150 | 0.289 |
| both_s25_t25 | val MAE after 18 epochs | 0.70 | 0.70 (0.48, 0.81) | 0.51 | 0.20 | 3.20 | 1.41 | 0.158 | 0.306 |
| both_s25_t25 | val MAE after 19 epochs | 0.71 | 0.71 (0.51, 0.80) | 0.50 | 0.21 | 3.20 | 1.41 | 0.164 | 0.313 |
| both_s25_t25 | val MAE after 20 epochs | 0.71 | 0.71 (0.49, 0.82) | 0.51 | 0.20 | 3.20 | 1.41 | 0.171 | 0.319 |
| both_s25R_t25 | best val MAE of the run | 0.67 | 0.70 (0.47, 0.82) | 0.51 | 0.18 | 3.20 | 1.41 | 0.172 | 0.366 |
| both_s25R_t25 | val MAE after 1 epochs | 0.05 | 0.36 (0.09, 0.58) | 0.44 | -0.07 | 4.91 | 4.67 | 0.010 | 0.210 |
| both_s25R_t25 | val MAE after 2 epochs | 0.10 | 0.68 (0.44, 0.81) | 0.44 | 0.24 | 4.91 | 0.00 | 0.019 | 0.093 |
| both_s25R_t25 | val MAE after 3 epochs | 0.10 | 0.59 (0.34, 0.76) | 0.44 | 0.16 | 3.20 | 1.53 | 0.028 | 0.187 |
| both_s25R_t25 | val MAE after 4 epochs | 0.22 | 0.66 (0.42, 0.79) | 0.44 | 0.22 | 3.20 | 1.53 | 0.036 | 0.205 |
| both_s25R_t25 | val MAE after 5 epochs | 0.32 | 0.68 (0.44, 0.82) | 0.44 | 0.24 | 3.20 | 1.53 | 0.045 | 0.196 |
| both_s25R_t25 | val MAE after 6 epochs | 0.38 | 0.72 (0.50, 0.84) | 0.44 | 0.28 | 3.20 | 1.53 | 0.054 | 0.199 |
| both_s25R_t25 | val MAE after 7 epochs | 0.49 | 0.75 (0.55, 0.85) | 0.45 | 0.31 | 1.53 | 0.00 | 0.063 | 0.185 |
| both_s25R_t25 | val MAE after 8 epochs | 0.51 | 0.73 (0.52, 0.84) | 0.47 | 0.26 | 1.53 | 1.53 | 0.071 | 0.202 |
| both_s25R_t25 | val MAE after 9 epochs | 0.54 | 0.67 (0.41, 0.83) | 0.49 | 0.19 | 3.20 | 1.53 | 0.080 | 0.362 |
| both_s25R_t25 | val MAE after 10 epochs | 0.57 | 0.74 (0.53, 0.85) | 0.50 | 0.23 | 1.53 | 1.53 | 0.088 | 0.239 |
| both_s25R_t25 | val MAE after 11 epochs | 0.61 | 0.71 (0.49, 0.84) | 0.52 | 0.19 | 1.53 | 1.53 | 0.097 | 0.300 |
| both_s25R_t25 | val MAE after 12 epochs | 0.67 | 0.77 (0.56, 0.88) | 0.54 | 0.23 | 1.53 | 1.53 | 0.105 | 0.249 |
| both_s25R_t25 | val MAE after 13 epochs | 0.68 | 0.72 (0.49, 0.84) | 0.55 | 0.17 | 1.53 | 1.41 | 0.114 | 0.279 |
| both_s25R_t25 | val MAE after 14 epochs | 0.63 | 0.64 (0.39, 0.80) | 0.54 | 0.10 | 1.53 | 1.41 | 0.123 | 0.328 |
| both_s25R_t25 | val MAE after 15 epochs | 0.66 | 0.72 (0.48, 0.84) | 0.53 | 0.18 | 1.53 | 1.41 | 0.131 | 0.324 |
| both_s25R_t25 | val MAE after 16 epochs | 0.67 | 0.71 (0.48, 0.83) | 0.52 | 0.18 | 3.20 | 1.41 | 0.139 | 0.334 |
| both_s25R_t25 | val MAE after 17 epochs | 0.66 | 0.70 (0.48, 0.82) | 0.52 | 0.18 | 3.20 | 1.41 | 0.147 | 0.340 |
| both_s25R_t25 | val MAE after 18 epochs | 0.67 | 0.69 (0.46, 0.83) | 0.51 | 0.19 | 3.20 | 1.41 | 0.155 | 0.359 |
| both_s25R_t25 | val MAE after 19 epochs | 0.67 | 0.70 (0.47, 0.83) | 0.50 | 0.20 | 1.53 | 1.41 | 0.162 | 0.367 |
| both_s25R_t25 | val MAE after 20 epochs | 0.66 | 0.70 (0.48, 0.82) | 0.51 | 0.20 | 3.20 | 1.41 | 0.169 | 0.362 |
| both_s10C_t25 | best val MAE of the run | 0.64 | 0.49 (0.23, 0.72) | 0.55 | -0.05 | 3.20 | 1.41 | 0.117 | 0.598 |
| both_s10C_t25 | val MAE after 1 epochs | 0.20 | 0.53 (0.28, 0.71) | 0.44 | 0.09 | 4.91 | 0.00 | 0.008 | 0.083 |
| both_s10C_t25 | val MAE after 2 epochs | 0.10 | 0.50 (0.22, 0.70) | 0.44 | 0.06 | 6.48 | 0.00 | 0.015 | 0.154 |
| both_s10C_t25 | val MAE after 3 epochs | 0.14 | 0.56 (0.30, 0.74) | 0.44 | 0.13 | 1.53 | 1.53 | 0.022 | 0.343 |
| both_s10C_t25 | val MAE after 4 epochs | 0.31 | 0.57 (0.29, 0.76) | 0.44 | 0.13 | 3.20 | 1.53 | 0.028 | 0.155 |
| both_s10C_t25 | val MAE after 5 epochs | 0.32 | 0.48 (0.19, 0.68) | 0.44 | 0.04 | 3.20 | 1.53 | 0.035 | 0.319 |
| both_s10C_t25 | val MAE after 6 epochs | 0.42 | 0.50 (0.20, 0.72) | 0.44 | 0.07 | 3.20 | 1.41 | 0.041 | 0.327 |
| both_s10C_t25 | val MAE after 7 epochs | 0.51 | 0.56 (0.27, 0.73) | 0.44 | 0.12 | 3.20 | 1.53 | 0.047 | 0.348 |
| both_s10C_t25 | val MAE after 8 epochs | 0.48 | 0.44 (0.15, 0.66) | 0.44 | 0.00 | 3.20 | 1.53 | 0.054 | 0.503 |
| both_s10C_t25 | val MAE after 9 epochs | 0.55 | 0.48 (0.20, 0.70) | 0.44 | 0.03 | 3.20 | 1.41 | 0.060 | 0.521 |
| both_s10C_t25 | val MAE after 10 epochs | 0.61 | 0.47 (0.19, 0.70) | 0.46 | 0.01 | 3.20 | 1.41 | 0.067 | 0.422 |
| both_s10C_t25 | val MAE after 11 epochs | 0.66 | 0.57 (0.32, 0.75) | 0.47 | 0.10 | 3.20 | 1.41 | 0.073 | 0.405 |
| both_s10C_t25 | val MAE after 12 epochs | 0.62 | 0.49 (0.20, 0.71) | 0.48 | 0.01 | 3.20 | 1.41 | 0.079 | 0.404 |
| both_s10C_t25 | val MAE after 13 epochs | 0.63 | 0.48 (0.21, 0.70) | 0.50 | -0.01 | 3.20 | 1.41 | 0.084 | 0.502 |
| both_s10C_t25 | val MAE after 14 epochs | 0.66 | 0.55 (0.27, 0.77) | 0.51 | 0.04 | 3.20 | 1.41 | 0.090 | 0.496 |
| both_s10C_t25 | val MAE after 15 epochs | 0.62 | 0.48 (0.20, 0.71) | 0.52 | -0.04 | 3.20 | 1.41 | 0.095 | 0.571 |
| both_s10C_t25 | val MAE after 16 epochs | 0.64 | 0.50 (0.22, 0.72) | 0.53 | -0.03 | 3.20 | 1.41 | 0.100 | 0.516 |
| both_s10C_t25 | val MAE after 17 epochs | 0.63 | 0.48 (0.21, 0.71) | 0.54 | -0.06 | 3.20 | 1.41 | 0.105 | 0.534 |
| both_s10C_t25 | val MAE after 18 epochs | 0.61 | 0.43 (0.17, 0.68) | 0.55 | -0.11 | 3.20 | 1.41 | 0.109 | 0.565 |
| both_s10C_t25 | val MAE after 19 epochs | 0.62 | 0.47 (0.21, 0.70) | 0.55 | -0.08 | 3.20 | 1.41 | 0.113 | 0.582 |
| both_s10C_t25 | val MAE after 20 epochs | 0.62 | 0.48 (0.21, 0.71) | 0.55 | -0.07 | 3.20 | 1.41 | 0.116 | 0.546 |
