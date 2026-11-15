# evalscreen operator_traits: a predictor that reads what an operator is

Each operator has a fixed list of traits (SEQ_TRAITS, FLAT_TRAITS, GRAPH_TRAITS in pilot/evalscreen.py). An architecture is encoded by the count of each trait in each cell. Test: one city and one operator family are held out together; Kendall with -test MAE on the held-out family at the held-out city, n-weighted over the families with 8 architectures or more. Pass: 0.5 or more at three of four cities and above the operator-count predictor at three of four cities.

### Verdict

| model | cities_kendall_ge_05 | cities_above_operator_counts | mean_gain | pass |
|---|---|---|---|---|
| gbr_traits | 1 | 2 | 0.000 | False |
| gbr_traits_and_counts | 1 | 2 | -0.003 | False |
| ridge_traits | 1 | 3 | 0.001 | False |
| ridge_traits_and_counts | 1 | 1 | -0.001 | False |

### n-weighted Kendall on the held-out family at the held-out city

| model | chengdu | metrla | pems04 | shenzhen |
|---|---|---|---|---|
| gbr_operator_counts | 0.444 | 0.473 | 0.455 | 0.569 |
| gbr_traits | 0.441 | 0.450 | 0.472 | 0.578 |
| gbr_traits_and_counts | 0.439 | 0.450 | 0.471 | 0.570 |
| ridge_operator_counts | 0.430 | 0.462 | 0.457 | 0.589 |
| ridge_traits | 0.427 | 0.463 | 0.459 | 0.593 |
| ridge_traits_and_counts | 0.430 | 0.466 | 0.451 | 0.586 |

### Kendall per held-out family

| held_out_family | model | chengdu | metrla | pems04 | shenzhen |
|---|---|---|---|---|---|
| adaptive-only | gbr_operator_counts | 0.397 | 0.559 | 0.515 | 0.603 |
| adaptive-only | gbr_traits | 0.426 | 0.588 | 0.529 | 0.618 |
| adaptive-only | gbr_traits_and_counts | 0.426 | 0.574 | 0.559 | 0.603 |
| adaptive-only | ridge_operator_counts | 0.471 | 0.426 | 0.456 | 0.574 |
| adaptive-only | ridge_traits | 0.471 | 0.426 | 0.500 | 0.574 |
| adaptive-only | ridge_traits_and_counts | 0.471 | 0.426 | 0.500 | 0.574 |
| diffusion | gbr_operator_counts | 0.505 | 0.448 | 0.676 | 0.371 |
| diffusion | gbr_traits | 0.467 | 0.448 | 0.714 | 0.390 |
| diffusion | gbr_traits_and_counts | 0.448 | 0.448 | 0.676 | 0.410 |
| diffusion | ridge_operator_counts | 0.562 | 0.486 | 0.657 | 0.619 |
| diffusion | ridge_traits | 0.562 | 0.486 | 0.657 | 0.600 |
| diffusion | ridge_traits_and_counts | 0.562 | 0.505 | 0.657 | 0.619 |
| gcn | gbr_operator_counts | 0.576 | 0.697 | 0.455 | 0.697 |
| gcn | gbr_traits | 0.515 | 0.727 | 0.485 | 0.636 |
| gcn | gbr_traits_and_counts | 0.545 | 0.727 | 0.515 | 0.667 |
| gcn | ridge_operator_counts | 0.455 | 0.606 | 0.545 | 0.667 |
| gcn | ridge_traits | 0.455 | 0.606 | 0.545 | 0.697 |
| gcn | ridge_traits_and_counts | 0.485 | 0.636 | 0.545 | 0.697 |
| gru | gbr_operator_counts | 0.462 | 0.026 | 0.359 | 0.128 |
| gru | gbr_traits | 0.436 | 0.051 | 0.436 | 0.154 |
| gru | gbr_traits_and_counts | 0.385 | -0.026 | 0.436 | 0.154 |
| gru | ridge_operator_counts | 0.462 | 0.103 | 0.359 | 0.231 |
| gru | ridge_traits | 0.462 | 0.154 | 0.333 | 0.231 |
| gru | ridge_traits_and_counts | 0.436 | 0.179 | 0.333 | 0.282 |
| lstm | gbr_operator_counts | 0.429 | 0.369 | 0.271 | 0.542 |
| lstm | gbr_traits | 0.394 | 0.345 | 0.320 | 0.562 |
| lstm | gbr_traits_and_counts | 0.414 | 0.355 | 0.325 | 0.576 |
| lstm | ridge_operator_counts | 0.345 | 0.438 | 0.222 | 0.493 |
| lstm | ridge_traits | 0.350 | 0.433 | 0.212 | 0.493 |
| lstm | ridge_traits_and_counts | 0.355 | 0.458 | 0.217 | 0.498 |
| mixed | gbr_operator_counts | 0.432 | 0.556 | 0.591 | 0.568 |
| mixed | gbr_traits | 0.429 | 0.492 | 0.603 | 0.600 |
| mixed | gbr_traits_and_counts | 0.437 | 0.526 | 0.589 | 0.585 |
| mixed | ridge_operator_counts | 0.494 | 0.455 | 0.590 | 0.632 |
| mixed | ridge_traits | 0.485 | 0.455 | 0.591 | 0.634 |
| mixed | ridge_traits_and_counts | 0.487 | 0.440 | 0.568 | 0.617 |
| mlp_mix | gbr_operator_counts | 0.494 | 0.399 | 0.447 | 0.644 |
| mlp_mix | gbr_traits | 0.518 | 0.407 | 0.391 | 0.557 |
| mlp_mix | gbr_traits_and_counts | 0.526 | 0.407 | 0.399 | 0.542 |
| mlp_mix | ridge_operator_counts | 0.470 | 0.407 | 0.462 | 0.549 |
| mlp_mix | ridge_traits | 0.462 | 0.407 | 0.439 | 0.565 |
| mlp_mix | ridge_traits_and_counts | 0.462 | 0.407 | 0.447 | 0.565 |
| none | gbr_operator_counts | 0.397 | 0.459 | 0.379 | 0.596 |
| none | gbr_traits | 0.395 | 0.410 | 0.365 | 0.585 |
| none | gbr_traits_and_counts | 0.379 | 0.422 | 0.363 | 0.566 |
| none | ridge_operator_counts | 0.344 | 0.500 | 0.402 | 0.564 |
| none | ridge_traits | 0.340 | 0.495 | 0.404 | 0.562 |
| none | ridge_traits_and_counts | 0.342 | 0.504 | 0.395 | 0.560 |
| sep_tcn | gbr_operator_counts | 0.558 | 0.609 | 0.377 | 0.572 |
| sep_tcn | gbr_traits | 0.529 | 0.572 | 0.377 | 0.630 |
| sep_tcn | gbr_traits_and_counts | 0.529 | 0.507 | 0.399 | 0.580 |
| sep_tcn | ridge_operator_counts | 0.565 | 0.529 | 0.391 | 0.638 |
| sep_tcn | ridge_traits | 0.565 | 0.529 | 0.384 | 0.638 |
| sep_tcn | ridge_traits_and_counts | 0.580 | 0.529 | 0.391 | 0.630 |
| skip_connection | gbr_operator_counts | 0.317 | 0.500 | 0.417 | 0.633 |
| skip_connection | gbr_traits | 0.333 | 0.417 | 0.483 | 0.567 |
| skip_connection | gbr_traits_and_counts | 0.317 | 0.450 | 0.450 | 0.600 |
| skip_connection | ridge_operator_counts | 0.117 | 0.450 | 0.383 | 0.583 |
| skip_connection | ridge_traits | 0.100 | 0.450 | 0.400 | 0.617 |
| skip_connection | ridge_traits_and_counts | 0.117 | 0.450 | 0.383 | 0.583 |
| tcn | gbr_operator_counts | 0.385 | 0.531 | 0.467 | 0.622 |
| tcn | gbr_traits | 0.415 | 0.544 | 0.492 | 0.682 |
| tcn | gbr_traits_and_counts | 0.402 | 0.535 | 0.492 | 0.660 |
| tcn | ridge_operator_counts | 0.406 | 0.561 | 0.523 | 0.695 |
| tcn | ridge_traits | 0.411 | 0.566 | 0.527 | 0.695 |
| tcn | ridge_traits_and_counts | 0.415 | 0.544 | 0.518 | 0.699 |
| transformer | gbr_operator_counts | 0.538 | 0.275 | 0.495 | 0.692 |
| transformer | gbr_traits | 0.582 | 0.297 | 0.560 | 0.714 |
| transformer | gbr_traits_and_counts | 0.582 | 0.275 | 0.538 | 0.736 |
| transformer | ridge_operator_counts | 0.516 | 0.407 | 0.429 | 0.714 |
| transformer | ridge_traits | 0.516 | 0.407 | 0.473 | 0.714 |
| transformer | ridge_traits_and_counts | 0.495 | 0.429 | 0.429 | 0.604 |

### No family held out: Spearman inside the heads at the held-out city

| model | chengdu | metrla | pems04 | shenzhen |
|---|---|---|---|---|
| gbr_operator_counts | 0.669 | 0.491 | 0.638 | 0.810 |
| gbr_traits | 0.675 | 0.490 | 0.641 | 0.824 |
| gbr_traits_and_counts | 0.672 | 0.492 | 0.638 | 0.826 |
| ridge_operator_counts | 0.612 | 0.510 | 0.543 | 0.761 |
| ridge_traits | 0.614 | 0.503 | 0.539 | 0.761 |
| ridge_traits_and_counts | 0.609 | 0.499 | 0.539 | 0.763 |
