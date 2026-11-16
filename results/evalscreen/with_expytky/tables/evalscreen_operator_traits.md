# evalscreen operator_traits: a predictor that reads what an operator is

Each operator has a fixed list of traits (SEQ_TRAITS, FLAT_TRAITS, GRAPH_TRAITS in pilot/evalscreen.py). An architecture is encoded by the count of each trait in each cell. Test: one city and one operator family are held out together; Kendall with -test MAE on the held-out family at the held-out city, n-weighted over the families with 8 architectures or more. Pass: 0.5 or more at three of four cities and above the operator-count predictor at three of four cities.

### Verdict

| model | cities_kendall_ge_05 | cities_above_operator_counts | mean_gain | pass |
|---|---|---|---|---|
| gbr_traits | 1 | 3 | 0.003 | False |
| gbr_traits_and_counts | 1 | 3 | -0.002 | False |
| ridge_traits | 2 | 4 | 0.001 | False |
| ridge_traits_and_counts | 2 | 3 | -0.000 | False |

### n-weighted Kendall on the held-out family at the held-out city

| model | chengdu | expytky | metrla | pems04 | shenzhen |
|---|---|---|---|---|---|
| gbr_operator_counts | 0.439 | 0.438 | 0.521 | 0.444 | 0.578 |
| gbr_traits | 0.448 | 0.434 | 0.491 | 0.465 | 0.595 |
| gbr_traits_and_counts | 0.443 | 0.431 | 0.491 | 0.463 | 0.583 |
| ridge_operator_counts | 0.433 | 0.457 | 0.511 | 0.465 | 0.589 |
| ridge_traits | 0.434 | 0.456 | 0.514 | 0.466 | 0.591 |
| ridge_traits_and_counts | 0.433 | 0.458 | 0.512 | 0.462 | 0.588 |

### Kendall per held-out family

| held_out_family | model | chengdu | expytky | metrla | pems04 | shenzhen |
|---|---|---|---|---|---|---|
| adaptive-only | gbr_operator_counts | 0.471 | 0.382 | 0.574 | 0.515 | 0.559 |
| adaptive-only | gbr_traits | 0.485 | 0.412 | 0.603 | 0.559 | 0.632 |
| adaptive-only | gbr_traits_and_counts | 0.515 | 0.412 | 0.618 | 0.574 | 0.588 |
| adaptive-only | ridge_operator_counts | 0.529 | 0.412 | 0.515 | 0.529 | 0.559 |
| adaptive-only | ridge_traits | 0.529 | 0.412 | 0.515 | 0.559 | 0.559 |
| adaptive-only | ridge_traits_and_counts | 0.529 | 0.426 | 0.529 | 0.529 | 0.574 |
| diffusion | gbr_operator_counts | 0.581 | 0.410 | 0.467 | 0.676 | 0.524 |
| diffusion | gbr_traits | 0.543 | 0.333 | 0.467 | 0.657 | 0.505 |
| diffusion | gbr_traits_and_counts | 0.505 | 0.333 | 0.448 | 0.638 | 0.524 |
| diffusion | ridge_operator_counts | 0.543 | 0.486 | 0.505 | 0.676 | 0.619 |
| diffusion | ridge_traits | 0.543 | 0.486 | 0.505 | 0.676 | 0.638 |
| diffusion | ridge_traits_and_counts | 0.543 | 0.467 | 0.505 | 0.657 | 0.619 |
| gcn | gbr_operator_counts | 0.515 | 0.455 | 0.788 | 0.455 | 0.818 |
| gcn | gbr_traits | 0.515 | 0.485 | 0.727 | 0.515 | 0.758 |
| gcn | gbr_traits_and_counts | 0.515 | 0.485 | 0.758 | 0.545 | 0.788 |
| gcn | ridge_operator_counts | 0.515 | 0.697 | 0.697 | 0.515 | 0.697 |
| gcn | ridge_traits | 0.515 | 0.697 | 0.697 | 0.515 | 0.727 |
| gcn | ridge_traits_and_counts | 0.515 | 0.697 | 0.697 | 0.545 | 0.758 |
| gru | gbr_operator_counts | 0.513 | 0.103 | 0.051 | 0.385 | 0.308 |
| gru | gbr_traits | 0.487 | 0.051 | 0.179 | 0.410 | 0.308 |
| gru | gbr_traits_and_counts | 0.462 | 0.077 | 0.051 | 0.436 | 0.308 |
| gru | ridge_operator_counts | 0.462 | 0.000 | 0.308 | 0.359 | 0.359 |
| gru | ridge_traits | 0.487 | -0.051 | 0.333 | 0.308 | 0.359 |
| gru | ridge_traits_and_counts | 0.436 | 0.077 | 0.308 | 0.359 | 0.359 |
| lstm | gbr_operator_counts | 0.429 | 0.202 | 0.433 | 0.251 | 0.571 |
| lstm | gbr_traits | 0.374 | 0.256 | 0.394 | 0.340 | 0.586 |
| lstm | gbr_traits_and_counts | 0.384 | 0.232 | 0.409 | 0.340 | 0.576 |
| lstm | ridge_operator_counts | 0.340 | 0.345 | 0.507 | 0.227 | 0.483 |
| lstm | ridge_traits | 0.335 | 0.355 | 0.507 | 0.241 | 0.498 |
| lstm | ridge_traits_and_counts | 0.340 | 0.355 | 0.517 | 0.232 | 0.498 |
| mixed | gbr_operator_counts | 0.406 | 0.486 | 0.638 | 0.558 | 0.550 |
| mixed | gbr_traits | 0.440 | 0.457 | 0.559 | 0.570 | 0.585 |
| mixed | gbr_traits_and_counts | 0.414 | 0.437 | 0.566 | 0.564 | 0.576 |
| mixed | ridge_operator_counts | 0.476 | 0.476 | 0.489 | 0.605 | 0.620 |
| mixed | ridge_traits | 0.472 | 0.459 | 0.490 | 0.595 | 0.617 |
| mixed | ridge_traits_and_counts | 0.474 | 0.459 | 0.477 | 0.591 | 0.610 |
| mlp_mix | gbr_operator_counts | 0.470 | 0.573 | 0.383 | 0.447 | 0.597 |
| mlp_mix | gbr_traits | 0.494 | 0.557 | 0.470 | 0.399 | 0.534 |
| mlp_mix | gbr_traits_and_counts | 0.486 | 0.557 | 0.478 | 0.415 | 0.534 |
| mlp_mix | ridge_operator_counts | 0.455 | 0.502 | 0.439 | 0.462 | 0.542 |
| mlp_mix | ridge_traits | 0.447 | 0.502 | 0.439 | 0.462 | 0.542 |
| mlp_mix | ridge_traits_and_counts | 0.462 | 0.510 | 0.431 | 0.455 | 0.542 |
| none | gbr_operator_counts | 0.411 | 0.449 | 0.504 | 0.376 | 0.580 |
| none | gbr_traits | 0.401 | 0.447 | 0.452 | 0.374 | 0.574 |
| none | gbr_traits_and_counts | 0.392 | 0.449 | 0.468 | 0.378 | 0.560 |
| none | ridge_operator_counts | 0.335 | 0.413 | 0.528 | 0.388 | 0.551 |
| none | ridge_traits | 0.330 | 0.420 | 0.534 | 0.388 | 0.544 |
| none | ridge_traits_and_counts | 0.330 | 0.415 | 0.528 | 0.387 | 0.537 |
| sep_tcn | gbr_operator_counts | 0.486 | 0.486 | 0.696 | 0.355 | 0.609 |
| sep_tcn | gbr_traits | 0.500 | 0.464 | 0.609 | 0.377 | 0.645 |
| sep_tcn | gbr_traits_and_counts | 0.514 | 0.464 | 0.587 | 0.370 | 0.609 |
| sep_tcn | ridge_operator_counts | 0.536 | 0.551 | 0.623 | 0.406 | 0.630 |
| sep_tcn | ridge_traits | 0.543 | 0.543 | 0.630 | 0.406 | 0.638 |
| sep_tcn | ridge_traits_and_counts | 0.543 | 0.543 | 0.645 | 0.406 | 0.630 |
| skip_connection | gbr_operator_counts | 0.267 | 0.467 | 0.500 | 0.483 | 0.583 |
| skip_connection | gbr_traits | 0.333 | 0.433 | 0.400 | 0.583 | 0.617 |
| skip_connection | gbr_traits_and_counts | 0.317 | 0.467 | 0.383 | 0.483 | 0.617 |
| skip_connection | ridge_operator_counts | 0.200 | 0.567 | 0.417 | 0.467 | 0.617 |
| skip_connection | ridge_traits | 0.217 | 0.617 | 0.417 | 0.500 | 0.617 |
| skip_connection | ridge_traits_and_counts | 0.200 | 0.567 | 0.417 | 0.467 | 0.617 |
| tcn | gbr_operator_counts | 0.376 | 0.591 | 0.591 | 0.437 | 0.652 |
| tcn | gbr_traits | 0.411 | 0.604 | 0.570 | 0.445 | 0.703 |
| tcn | gbr_traits_and_counts | 0.419 | 0.600 | 0.587 | 0.449 | 0.703 |
| tcn | ridge_operator_counts | 0.381 | 0.596 | 0.609 | 0.492 | 0.677 |
| tcn | ridge_traits | 0.389 | 0.591 | 0.613 | 0.497 | 0.682 |
| tcn | ridge_traits_and_counts | 0.394 | 0.596 | 0.609 | 0.488 | 0.686 |
| transformer | gbr_operator_counts | 0.560 | 0.407 | 0.275 | 0.451 | 0.582 |
| transformer | gbr_traits | 0.604 | 0.473 | 0.297 | 0.473 | 0.648 |
| transformer | gbr_traits_and_counts | 0.626 | 0.495 | 0.275 | 0.473 | 0.560 |
| transformer | ridge_operator_counts | 0.626 | 0.341 | 0.407 | 0.451 | 0.714 |
| transformer | ridge_traits | 0.626 | 0.363 | 0.385 | 0.451 | 0.692 |
| transformer | ridge_traits_and_counts | 0.626 | 0.341 | 0.407 | 0.451 | 0.670 |

### No family held out: Spearman inside the heads at the held-out city

| model | chengdu | expytky | metrla | pems04 | shenzhen |
|---|---|---|---|---|---|
| gbr_operator_counts | 0.636 | 0.541 | 0.553 | 0.638 | 0.844 |
| gbr_traits | 0.631 | 0.562 | 0.556 | 0.630 | 0.854 |
| gbr_traits_and_counts | 0.634 | 0.565 | 0.559 | 0.630 | 0.854 |
| ridge_operator_counts | 0.607 | 0.512 | 0.553 | 0.587 | 0.770 |
| ridge_traits | 0.608 | 0.513 | 0.557 | 0.585 | 0.769 |
| ridge_traits_and_counts | 0.608 | 0.512 | 0.546 | 0.581 | 0.769 |
