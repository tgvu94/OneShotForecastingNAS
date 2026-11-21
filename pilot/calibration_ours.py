"""pilot.train_arch with settings of the Hydra config changed, and no change of pilot.train_arch itself.

    CALIB_OVERRIDES="train.targe_scaler=none train.grad_clip=5.0" python -m pilot.calibration_ours <arguments of pilot.train_arch>
    CALIB_TRUE_CLOCK=1 python -m pilot.calibration_ours <arguments of pilot.train_arch>

CALIB_OVERRIDES are Hydra overrides of experiments/configs/base.yaml.  metrics.json of the run records the scaler, the clip norm
and the AMP switch that the trainer read.
CALIB_TRUE_CLOCK=1 repairs the time features of a file that has rows missing.  The loader counts the clock from the row position,
so after a hole of k rows every time feature is k steps behind the clock of the data.  CLOCK_HOLES lists the holes (first row
after the hole, missing rows), read from the time stamps of the BasicTS copy of the file.  The repair gives row r behind a hole
the features of position r + k; the last rows take the features one week earlier (minute, hour and day of week are right; day of
month and day of year, which no hand model reads, are not).
Job script: pilot/calibration_ours.sbatch (Survey/experiments/calibration-plan.md).
"""
import os

import pilot.data as data

CLOCK_HOLES = {"pemsbay": [(20184, 12)]}            # PEMS-BAY: one hour is absent (the change to summer time)
WEEK = {"pemsbay": 7 * 288}

_get_cfg = data.get_cfg
_get_loaders = data.get_dataset_and_loaders
EXTRA = os.environ.get("CALIB_OVERRIDES", "").split()
TRUE_CLOCK = os.environ.get("CALIB_TRUE_CLOCK", "0") == "1"


def get_cfg(benchmark: str = data.DEFAULT_BENCHMARK, model: str = data.DEFAULT_MODEL, overrides=()):
    return _get_cfg(benchmark, model, [*overrides, *EXTRA])


def repair_clock(features, holes, week):
    """features [rows, F] counted from the row position -> the same array with the clock of the data, in place."""
    import numpy as np
    n = len(features)
    src = np.arange(n)
    for first, k in holes:
        src[first:] += k
    src = np.where(src >= n, src - week, src)
    features[:] = features[src]
    return int((src != np.arange(n)).sum())


def get_dataset_and_loaders(cfg, *args, **kwargs):
    out = _get_loaders(cfg, *args, **kwargs)
    name = str(cfg.benchmark.name).split("_")[0].lower()
    if TRUE_CLOCK and kwargs.get("freq"):
        if name not in CLOCK_HOLES:
            raise SystemExit(f"CALIB_TRUE_CLOCK: no holes are recorded for {name}")
        moved = sum(repair_clock(d._cached_time_features, CLOCK_HOLES[name], WEEK[name]) for d in out[0].datasets)
        print(f"true clock: the time features of {moved} rows moved ({CLOCK_HOLES[name]})", flush=True)
    return out


data.get_cfg = get_cfg                                  # pilot.train_arch imports both names from pilot.data inside main()
data.get_dataset_and_loaders = get_dataset_and_loaders

if __name__ == "__main__":
    from pilot.train_arch import main
    print(f"config overrides: {EXTRA or 'none'}; true clock: {TRUE_CLOCK}", flush=True)
    raise SystemExit(main())
