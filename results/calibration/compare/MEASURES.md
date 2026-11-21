# calibration: hand designs under the published protocol, the frozen model and the benchst protocol

Masked MAE in the raw unit (mph); a target of 0 is missing.  A trained value is the mean ± standard deviation (ddof = 1) of 3 seeds.
The regime columns are the mean of the 12 steps over the targets of a window with that regime label (absolute rule).

## metrla

Published test split: 6831 windows; common windows: 6748.  Training rows: 23991 under the published split, 20563 under benchst.

**The whole published test split, mean of the 12 steps.**

| Model | Ours, 3 seeds | Published, one run | Difference |
|---|---|---|---|
| STID | 3.1232 ± 0.0051 | 3.12 | +0.10 % |

**The common windows.**

| Model | step 3 | step 6 | step 12 | mean of 12 | free | transition | congested |
|---|---|---|---|---|---|---|---|
| STID, published protocol | 2.8104 ± 0.0047 | 3.1866 ± 0.0050 | 3.5556 ± 0.0068 | 3.1254 ± 0.0049 | 1.4044 ± 0.0049 | 5.6457 ± 0.0166 | 5.0135 ± 0.1048 |
| chronos2_joint, zero-shot | 2.8373 | 3.2611 | 3.7476 | 3.2189 | 1.4498 | 5.8643 | 4.3574 |
| stid_trueclock, benchst protocol | 3.2021 ± 0.0075 | 3.8226 ± 0.0088 | 4.6353 ± 0.0032 | 3.7919 ± 0.0068 | 1.6105 ± 0.0059 | 6.3378 ± 0.0077 | 6.1203 ± 0.1117 |

| Trained model | Frozen minus trained, mean of 12 | In sigma_seed | Read |
|---|---|---|---|
| STID, published protocol | +0.0936 | +19.0 | the trained model wins |
| stid_trueclock, benchst protocol | -0.5730 | -84.4 | the frozen model wins |

## pemsbay

Published test split: 10400 windows; common windows: 10317.  Training rows: 36482 under the published split, 31269 under benchst.

**The whole published test split, mean of the 12 steps.**

| Model | Ours, 3 seeds | Published, one run | Difference |
|---|---|---|---|
| STID | 1.5597 ± 0.0011 | 1.56 | -0.02 % |

**The common windows.**

| Model | step 3 | step 6 | step 12 | mean of 12 | free | transition | congested |
|---|---|---|---|---|---|---|---|
| STID, published protocol | 1.3105 ± 0.0012 | 1.6314 ± 0.0014 | 1.9115 ± 0.0029 | 1.5654 ± 0.0011 | 0.9154 ± 0.0009 | 5.2260 ± 0.0083 | 3.4170 ± 0.1500 |
| chronos2_joint, zero-shot | 1.3174 | 1.6290 | 1.9070 | 1.5698 | 0.8751 | 5.4889 | 3.4464 |
| stid_trueclock, benchst protocol | 1.3959 ± 0.0008 | 1.8248 ± 0.0014 | 2.3351 ± 0.0089 | 1.7824 ± 0.0025 | 0.9917 ± 0.0021 | 6.2264 ± 0.0200 | 4.1976 ± 0.0223 |

| Trained model | Frozen minus trained, mean of 12 | In sigma_seed | Read |
|---|---|---|---|
| STID, published protocol | +0.0045 | +4.0 | the trained model wins |
| stid_trueclock, benchst protocol | -0.2126 | -84.6 | the frozen model wins |

