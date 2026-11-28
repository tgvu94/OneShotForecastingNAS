# sgp: headroom of the fixed random encoder against STID

Masked MAE in the raw unit on the common test windows of `pilot.calibration` (a target of 0 is missing).  Mean and standard
deviation (ddof = 1) over the seeds.  g = (row of the reference - SGP) / pooled deviation, on the mean of the 12 steps; a
positive g means that SGP has the lower error.  The two sides differ in the scaler, in the treatment of zeros in the input
and in the split fractions; the common windows remove the difference in the test set only.

## metrla (6748 windows)

| Row | seeds | step 3 | step 6 | step 12 | mean of 12 | sd | g against SGP (release_release, R0) |
|---|---|---|---|---|---|---|---|
| STID, published protocol | 3 | 2.8104 | 3.1866 | 3.5556 | 3.1254 | 0.0049 | +35.2 |
| stid_trueclock, benchst protocol | 3 | 3.2021 | 3.8226 | 4.6353 | 3.7919 | 0.0068 | +161.0 |
| SGP runner, gesn_release, R7 | 3 | 3.2615 | 3.9741 | 4.9878 | 3.9681 | 0.0017 | +577.7 |
| SGP runner, nospace_release, R0 | 3 | 2.8441 | 3.2582 | 3.7303 | 3.2107 | 0.0040 | +69.6 |
| SGP runner, paper_release, R0 | 3 | 2.6886 | 3.0477 | 3.4349 | 2.9991 | 0.0028 | +1.2 |
| SGP runner, release_release, R0 | 3 | 2.6836 | 3.0445 | 3.4336 | 2.9963 | 0.0017 | +0.0 |
| SGP runner, release_strict, R0 | 1 | 2.6913 | 3.0578 | 3.4539 | 3.0104 | nan |  |
| SGP runner, release_strict, R1 | 1 | 2.8428 | 3.2838 | 3.8530 | 3.2516 | nan |  |
| SGP runner, release_strict, R2 | 1 | 3.1049 | 3.7412 | 4.6690 | 3.7401 | nan |  |
| SGP runner, release_strict, R3 | 1 | 3.2929 | 4.0419 | 5.0844 | 4.0281 | nan |  |
| SGP runner, release_strict, R4 | 1 | 3.0423 | 3.5481 | 4.0663 | 3.4726 | nan |  |
| SGP runner, release_strict, R5 | 1 | 3.0793 | 3.6407 | 4.2905 | 3.5905 | nan |  |
| SGP runner, release_strict, R6 | 1 | 3.0291 | 3.5488 | 4.0963 | 3.4772 | nan |  |

## pemsbay (10317 windows)

| Row | seeds | step 3 | step 6 | step 12 | mean of 12 | sd | g against SGP (release_release, R0) |
|---|---|---|---|---|---|---|---|
| STID, published protocol | 3 | 1.3105 | 1.6314 | 1.9115 | 1.5654 | 0.0011 | +14.5 |
| stid_trueclock, benchst protocol | 3 | 1.3959 | 1.8248 | 2.3351 | 1.7824 | 0.0025 | +81.8 |
| SGP runner, gesn_release, R7 | 3 | 1.5656 | 2.1203 | 2.8123 | 2.0820 | 0.0097 | +76.0 |
| SGP runner, nospace_release, R0 | 3 | 1.3336 | 1.6706 | 1.9936 | 1.6093 | 0.0030 | +24.8 |
| SGP runner, release_release, R0 | 3 | 1.2910 | 1.5874 | 1.8547 | 1.5264 | 0.0036 | +0.0 |

Fork commit c60e767.
