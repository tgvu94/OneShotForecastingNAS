# sgp: checks without a GPU, pemsbay

Fork commit 4a1b61f; host class: login node.

- series: 52128 rows on the full index, 52116 rows in the file, 325 sensors; rows absent from the file: 12; largest difference to the .npz of the project on valid values: 0.00e+00; masked share: 0.0003
- graph: 2369 edges from the raw distances with the kernel of the release (Table 3 of the paper: 2369); 2369 edges in the pickle without its diagonal; edges in one and not in the other: 0; largest difference in a weight: 1.19e-07; diagonal of the pickle: min 1.00 max 1.00
- split of the release: 41695 training samples (they include the 4156 validation samples), 37539 without them, 10421 test samples; first validation sample at 0.7199 of the rows, first test sample at 0.7999; rows between the last validation sample and the first test sample: 12
- test windows: 10400 under the published protocol of pilot.calibration, 10421 here; common first target rows: 10400; test samples here whose first target row is absent from the file: 0
- scaler: mean 62.6591 deviation 9.5740 (rows of the training samples, masked)
- encoding of 2,000 steps on the CPU (4 threads): 0.26 s per 1,000 steps; embedding size 1280; the full embedding of the release would hold 80.8 GiB (about 162 GiB at the peak, estimate); the states that this runner holds: 8.1 GiB
- ridge from accumulated sums against sklearn Ridge (30,000 rows, 1281 features, weight 1): largest difference in a weight 1.94e-10 (largest weight 3.24e+00); largest difference in a fitted value 4.79e-11
- reservoir of this runner against the source of the release (commit ae1abd5), seed 0: largest difference in a weight 0.0e+00, in a state over 300 steps 0.0e+00
