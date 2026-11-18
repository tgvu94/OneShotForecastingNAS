# evalscreen operator_traits: a predictor that reads what an operator is

Each operator has a fixed list of traits (SEQ_TRAITS, FLAT_TRAITS, GRAPH_TRAITS in pilot/evalscreen.py). An architecture is encoded by the count of each trait in each cell. Test: one city and one operator family are held out together; Kendall with -test MAE on the held-out family at the held-out city, n-weighted over the families with 8 architectures or more. Pass: 0.5 or more at three of four cities and above the operator-count predictor at three of four cities.

### Verdict

| model | cities_kendall_ge_05 | cities_above_operator_counts | mean_gain | pass |
|---|---|---|---|---|
| gbr_traits | 2 | 3 | 0.000 | False |
| gbr_traits_and_counts | 2 | 3 | 0.002 | False |
| ridge_traits | 2 | 2 | 0.001 | False |
| ridge_traits_and_counts | 2 | 1 | -0.002 | False |

### n-weighted Kendall on the held-out family at the held-out city

| model | chengdu | expytky | metrla | pems04 | pemsbay | shenzhen |
|---|---|---|---|---|---|---|
| gbr_operator_counts | 0.408 | 0.447 | 0.632 | 0.434 | 0.467 | 0.562 |
| gbr_traits | 0.425 | 0.437 | 0.623 | 0.442 | 0.469 | 0.556 |
| gbr_traits_and_counts | 0.423 | 0.440 | 0.630 | 0.438 | 0.479 | 0.553 |
| ridge_operator_counts | 0.392 | 0.477 | 0.596 | 0.445 | 0.408 | 0.555 |
| ridge_traits | 0.391 | 0.478 | 0.596 | 0.448 | 0.408 | 0.554 |
| ridge_traits_and_counts | 0.390 | 0.475 | 0.589 | 0.447 | 0.406 | 0.554 |

### Kendall per held-out family

| held_out_family | model | chengdu | expytky | metrla | pems04 | pemsbay | shenzhen |
|---|---|---|---|---|---|---|---|
| adaptive-only | gbr_operator_counts | 0.412 | 0.426 | 0.691 | 0.500 | 0.662 | 0.559 |
| adaptive-only | gbr_traits | 0.500 | 0.456 | 0.735 | 0.574 | 0.647 | 0.529 |
| adaptive-only | gbr_traits_and_counts | 0.485 | 0.485 | 0.706 | 0.574 | 0.676 | 0.588 |
| adaptive-only | ridge_operator_counts | 0.412 | 0.471 | 0.618 | 0.515 | 0.485 | 0.515 |
| adaptive-only | ridge_traits | 0.441 | 0.485 | 0.618 | 0.515 | 0.500 | 0.515 |
| adaptive-only | ridge_traits_and_counts | 0.412 | 0.485 | 0.559 | 0.529 | 0.485 | 0.485 |
| diffusion | gbr_operator_counts | 0.638 | 0.505 | 0.619 | 0.676 | 0.448 | 0.524 |
| diffusion | gbr_traits | 0.562 | 0.390 | 0.600 | 0.695 | 0.410 | 0.505 |
| diffusion | gbr_traits_and_counts | 0.581 | 0.410 | 0.562 | 0.657 | 0.429 | 0.467 |
| diffusion | ridge_operator_counts | 0.638 | 0.581 | 0.524 | 0.733 | 0.429 | 0.733 |
| diffusion | ridge_traits | 0.638 | 0.600 | 0.524 | 0.733 | 0.429 | 0.733 |
| diffusion | ridge_traits_and_counts | 0.638 | 0.581 | 0.505 | 0.733 | 0.429 | 0.714 |
| gcn | gbr_operator_counts | 0.545 | 0.515 | 0.818 | 0.394 | 0.485 | 0.818 |
| gcn | gbr_traits | 0.515 | 0.545 | 0.879 | 0.515 | 0.394 | 0.758 |
| gcn | gbr_traits_and_counts | 0.515 | 0.545 | 0.879 | 0.515 | 0.455 | 0.727 |
| gcn | ridge_operator_counts | 0.545 | 0.667 | 0.758 | 0.576 | 0.273 | 0.727 |
| gcn | ridge_traits | 0.545 | 0.667 | 0.788 | 0.576 | 0.273 | 0.727 |
| gcn | ridge_traits_and_counts | 0.545 | 0.667 | 0.758 | 0.576 | 0.303 | 0.758 |
| gru | gbr_operator_counts | 0.487 | 0.128 | 0.385 | 0.385 | 0.308 | 0.385 |
| gru | gbr_traits | 0.462 | 0.103 | 0.436 | 0.333 | 0.462 | 0.308 |
| gru | gbr_traits_and_counts | 0.462 | 0.077 | 0.487 | 0.333 | 0.462 | 0.308 |
| gru | ridge_operator_counts | 0.410 | 0.128 | 0.538 | 0.282 | 0.462 | 0.385 |
| gru | ridge_traits | 0.462 | 0.103 | 0.538 | 0.282 | 0.436 | 0.359 |
| gru | ridge_traits_and_counts | 0.385 | 0.128 | 0.538 | 0.282 | 0.462 | 0.385 |
| lstm | gbr_operator_counts | 0.394 | 0.192 | 0.557 | 0.266 | 0.310 | 0.517 |
| lstm | gbr_traits | 0.399 | 0.227 | 0.571 | 0.300 | 0.394 | 0.527 |
| lstm | gbr_traits_and_counts | 0.409 | 0.202 | 0.596 | 0.305 | 0.389 | 0.527 |
| lstm | ridge_operator_counts | 0.320 | 0.374 | 0.567 | 0.300 | 0.384 | 0.488 |
| lstm | ridge_traits | 0.320 | 0.389 | 0.567 | 0.291 | 0.384 | 0.473 |
| lstm | ridge_traits_and_counts | 0.320 | 0.384 | 0.567 | 0.300 | 0.374 | 0.483 |
| mixed | gbr_operator_counts | 0.380 | 0.489 | 0.655 | 0.531 | 0.581 | 0.533 |
| mixed | gbr_traits | 0.419 | 0.477 | 0.617 | 0.538 | 0.573 | 0.544 |
| mixed | gbr_traits_and_counts | 0.430 | 0.467 | 0.627 | 0.536 | 0.575 | 0.528 |
| mixed | ridge_operator_counts | 0.444 | 0.491 | 0.580 | 0.564 | 0.446 | 0.585 |
| mixed | ridge_traits | 0.432 | 0.486 | 0.573 | 0.569 | 0.445 | 0.581 |
| mixed | ridge_traits_and_counts | 0.436 | 0.491 | 0.563 | 0.569 | 0.432 | 0.589 |
| mlp_mix | gbr_operator_counts | 0.431 | 0.581 | 0.534 | 0.494 | 0.391 | 0.542 |
| mlp_mix | gbr_traits | 0.415 | 0.557 | 0.534 | 0.415 | 0.336 | 0.518 |
| mlp_mix | gbr_traits_and_counts | 0.399 | 0.549 | 0.573 | 0.431 | 0.336 | 0.534 |
| mlp_mix | ridge_operator_counts | 0.415 | 0.526 | 0.470 | 0.470 | 0.154 | 0.502 |
| mlp_mix | ridge_traits | 0.407 | 0.510 | 0.470 | 0.470 | 0.138 | 0.502 |
| mlp_mix | ridge_traits_and_counts | 0.439 | 0.510 | 0.470 | 0.470 | 0.146 | 0.502 |
| none | gbr_operator_counts | 0.383 | 0.450 | 0.635 | 0.362 | 0.480 | 0.555 |
| none | gbr_traits | 0.349 | 0.424 | 0.594 | 0.356 | 0.500 | 0.557 |
| none | gbr_traits_and_counts | 0.346 | 0.440 | 0.615 | 0.349 | 0.496 | 0.555 |
| none | ridge_operator_counts | 0.287 | 0.420 | 0.567 | 0.330 | 0.449 | 0.484 |
| none | ridge_traits | 0.287 | 0.431 | 0.566 | 0.337 | 0.456 | 0.484 |
| none | ridge_traits_and_counts | 0.287 | 0.417 | 0.566 | 0.332 | 0.457 | 0.477 |
| sep_tcn | gbr_operator_counts | 0.493 | 0.442 | 0.790 | 0.384 | 0.551 | 0.594 |
| sep_tcn | gbr_traits | 0.536 | 0.420 | 0.761 | 0.413 | 0.536 | 0.594 |
| sep_tcn | gbr_traits_and_counts | 0.536 | 0.442 | 0.754 | 0.428 | 0.551 | 0.594 |
| sep_tcn | ridge_operator_counts | 0.471 | 0.565 | 0.754 | 0.333 | 0.449 | 0.572 |
| sep_tcn | ridge_traits | 0.464 | 0.558 | 0.754 | 0.326 | 0.442 | 0.580 |
| sep_tcn | ridge_traits_and_counts | 0.471 | 0.558 | 0.739 | 0.348 | 0.449 | 0.594 |
| skip_connection | gbr_operator_counts | 0.117 | 0.433 | 0.617 | 0.417 | 0.333 | 0.517 |
| skip_connection | gbr_traits | 0.200 | 0.450 | 0.617 | 0.383 | 0.283 | 0.500 |
| skip_connection | gbr_traits_and_counts | 0.167 | 0.450 | 0.617 | 0.383 | 0.283 | 0.483 |
| skip_connection | ridge_operator_counts | 0.150 | 0.467 | 0.583 | 0.333 | 0.333 | 0.417 |
| skip_connection | ridge_traits | 0.150 | 0.433 | 0.600 | 0.367 | 0.333 | 0.433 |
| skip_connection | ridge_traits_and_counts | 0.133 | 0.450 | 0.600 | 0.333 | 0.333 | 0.417 |
| tcn | gbr_operator_counts | 0.308 | 0.613 | 0.647 | 0.402 | 0.505 | 0.643 |
| tcn | gbr_traits | 0.376 | 0.609 | 0.647 | 0.419 | 0.523 | 0.673 |
| tcn | gbr_traits_and_counts | 0.381 | 0.609 | 0.626 | 0.406 | 0.518 | 0.665 |
| tcn | ridge_operator_counts | 0.308 | 0.570 | 0.665 | 0.480 | 0.531 | 0.656 |
| tcn | ridge_traits | 0.303 | 0.583 | 0.660 | 0.488 | 0.531 | 0.647 |
| tcn | ridge_traits_and_counts | 0.312 | 0.578 | 0.677 | 0.475 | 0.540 | 0.652 |
| transformer | gbr_operator_counts | 0.560 | 0.429 | 0.560 | 0.451 | 0.253 | 0.648 |
| transformer | gbr_traits | 0.604 | 0.429 | 0.560 | 0.451 | 0.209 | 0.604 |
| transformer | gbr_traits_and_counts | 0.560 | 0.473 | 0.560 | 0.407 | 0.319 | 0.626 |
| transformer | ridge_operator_counts | 0.538 | 0.451 | 0.582 | 0.495 | 0.275 | 0.670 |
| transformer | ridge_traits | 0.516 | 0.473 | 0.582 | 0.495 | 0.297 | 0.714 |
| transformer | ridge_traits_and_counts | 0.516 | 0.429 | 0.582 | 0.495 | 0.253 | 0.670 |

### No family held out: Spearman inside the heads at the held-out city

| model | chengdu | expytky | metrla | pems04 | pemsbay | shenzhen |
|---|---|---|---|---|---|---|
| gbr_operator_counts | 0.614 | 0.549 | 0.575 | 0.650 | 0.170 | 0.836 |
| gbr_traits | 0.607 | 0.567 | 0.574 | 0.640 | 0.175 | 0.833 |
| gbr_traits_and_counts | 0.610 | 0.570 | 0.570 | 0.645 | 0.178 | 0.838 |
| ridge_operator_counts | 0.569 | 0.528 | 0.575 | 0.597 | 0.102 | 0.756 |
| ridge_traits | 0.566 | 0.531 | 0.578 | 0.598 | 0.106 | 0.757 |
| ridge_traits_and_counts | 0.568 | 0.533 | 0.574 | 0.593 | 0.106 | 0.756 |
