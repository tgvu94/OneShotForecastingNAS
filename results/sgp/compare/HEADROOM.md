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
| SGP runner, release_strict, R0 | 3 | 2.6899 | 3.0580 | 3.4525 | 3.0090 | 0.0036 | +4.5 |
| SGP runner, release_strict, R1 | 3 | 2.8432 | 3.2846 | 3.8532 | 3.2525 | 0.0021 | +136.2 |
| SGP runner, release_strict, R2 | 3 | 3.1001 | 3.7366 | 4.6573 | 3.7339 | 0.0055 | +180.4 |
| SGP runner, release_strict, R3 | 3 | 3.2831 | 4.0358 | 5.0805 | 4.0215 | 0.0066 | +212.1 |
| SGP runner, release_strict, R4 | 3 | 3.0375 | 3.5415 | 4.0613 | 3.4681 | 0.0130 | +50.8 |
| SGP runner, release_strict, R5 | 3 | 3.0797 | 3.6410 | 4.2877 | 3.5896 | 0.0265 | +31.6 |
| SGP runner, release_strict, R6 | 3 | 3.0313 | 3.5527 | 4.1046 | 3.4824 | 0.0135 | +50.4 |

## pemsbay (10317 windows)

| Row | seeds | step 3 | step 6 | step 12 | mean of 12 | sd | g against SGP (release_release, R0) |
|---|---|---|---|---|---|---|---|
| STID, published protocol | 3 | 1.3105 | 1.6314 | 1.9115 | 1.5654 | 0.0011 | +14.5 |
| stid_trueclock, benchst protocol | 3 | 1.3959 | 1.8248 | 2.3351 | 1.7824 | 0.0025 | +81.8 |
| SGP runner, gesn_release, R7 | 3 | 1.5656 | 2.1203 | 2.8123 | 2.0820 | 0.0097 | +76.0 |
| SGP runner, nospace_release, R0 | 3 | 1.3336 | 1.6706 | 1.9936 | 1.6093 | 0.0030 | +24.8 |
| SGP runner, release_release, R0 | 3 | 1.2910 | 1.5874 | 1.8547 | 1.5264 | 0.0036 | +0.0 |
| SGP runner, release_strict, R0 | 3 | 1.2987 | 1.6062 | 1.8920 | 1.5467 | 0.0036 | +5.6 |
| SGP runner, release_strict, R1 | 3 | 1.5735 | 2.8182 | 5.5245 | 3.1177 | 1.6871 | +1.3 |
| SGP runner, release_strict, R2 | 3 | 1.4632 | 1.9621 | 2.5863 | 1.9290 | 0.0060 | +80.8 |
| SGP runner, release_strict, R3 | 3 | 1.5166 | 2.0709 | 2.7499 | 2.0315 | 0.0069 | +91.8 |
| SGP runner, release_strict, R4 | 3 | 1.4653 | 1.8901 | 2.2912 | 1.8193 | 0.0077 | +48.9 |
| SGP runner, release_strict, R5 | 3 | 1.4651 | 1.9313 | 2.4285 | 1.8731 | 0.0076 | +57.9 |
| SGP runner, release_strict, R6 | 3 | 1.4556 | 1.8885 | 2.2969 | 1.8166 | 0.0047 | +68.6 |

Fork commit b488330.
