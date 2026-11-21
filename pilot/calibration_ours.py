"""pilot.train_arch with settings of the Hydra config changed, and no change of pilot.train_arch itself.

    CALIB_OVERRIDES="train.targe_scaler=none train.grad_clip=5.0" python -m pilot.calibration_ours <arguments of pilot.train_arch>
    CALIB_TRUE_CLOCK=1 python -m pilot.calibration_ours <arguments of pilot.train_arch>

CALIB_OVERRIDES are Hydra overrides of experiments/configs/base.yaml.  metrics.json of the run records the scaler, the clip norm
and the AMP switch that the trainer read.
The clock.  pilot.data repairs the time features of a file that has rows absent (pilot.datasets.absent_rows).  This wrapper
keeps the clock of the row position (PILOT_ROW_CLOCK=1), which the stored runs had, unless CALIB_TRUE_CLOCK=1.
Job script: pilot/calibration_ours.sbatch (Survey/experiments/calibration-plan.md).
"""
import os

import pilot.data as data

_get_cfg = data.get_cfg
EXTRA = os.environ.get("CALIB_OVERRIDES", "").split()
TRUE_CLOCK = os.environ.get("CALIB_TRUE_CLOCK", "0") == "1"
os.environ["PILOT_ROW_CLOCK"] = "0" if TRUE_CLOCK else "1"


def get_cfg(benchmark: str = data.DEFAULT_BENCHMARK, model: str = data.DEFAULT_MODEL, overrides=()):
    return _get_cfg(benchmark, model, [*overrides, *EXTRA])


data.get_cfg = get_cfg                                  # pilot.train_arch imports the name from pilot.data inside main()

if __name__ == "__main__":
    from pilot.train_arch import main
    print(f"config overrides: {EXTRA or 'none'}; true clock: {TRUE_CLOCK}", flush=True)
    raise SystemExit(main())
