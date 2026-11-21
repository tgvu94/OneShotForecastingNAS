"""pilot.train_arch with settings of the Hydra config changed, and no change of pilot.train_arch itself.

    CALIB_OVERRIDES="train.targe_scaler=none train.grad_clip=5.0" python -m pilot.calibration_ours <arguments of pilot.train_arch>

The overrides are Hydra overrides of experiments/configs/base.yaml.  metrics.json of the run records the scaler, the clip norm
and the AMP switch that the trainer read.  Job script: pilot/calibration_ours.sbatch (Survey/experiments/calibration-plan.md).
"""
import os

import pilot.data as data

_get_cfg = data.get_cfg
EXTRA = os.environ.get("CALIB_OVERRIDES", "").split()


def get_cfg(benchmark: str = data.DEFAULT_BENCHMARK, model: str = data.DEFAULT_MODEL, overrides=()):
    return _get_cfg(benchmark, model, [*overrides, *EXTRA])


data.get_cfg = get_cfg          # pilot.train_arch imports get_cfg from pilot.data inside main()

if __name__ == "__main__":
    from pilot.train_arch import main
    print(f"config overrides: {EXTRA or 'none'}", flush=True)
    raise SystemExit(main())
