"""Data access for the pilot: the repo's own PEMS loaders, the repo's preprocessing, the repo's loss.

Nothing here re-implements a loader. ``get_dataset_and_loaders`` is a verbatim copy of the PEMS branch of
``experiments/test_evaluated_model.py`` (60/20/20 borders from ``get_PEMS_dataset.get_test_dataset``,
``regenerate_splits(splits_ms=...)``, ``get_dataloader(is_test_sets=[False, True, True])``).
``preprocess_batch`` is a functional copy of ``SampledForecastingNetTrainer.preprocessing``.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import random
from pathlib import Path

import numpy as np
import torch

REPO = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO / "experiments" / "configs"
DEFAULT_BENCHMARK = "PEMS/pems04/pems04_12"
DEFAULT_MODEL = "mixed_concat_darts"
DEFAULT_PROBE = "results/data/pems04_probe_batch.pt"


def seed_everything(seed: int, deterministic: bool = False) -> None:
    """Same seeds as experiments/test_evaluated_model.py::seed_everything; cudnn flags switchable."""
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = deterministic
    torch.backends.cudnn.benchmark = not deterministic


def get_cfg(benchmark: str = DEFAULT_BENCHMARK, model: str = DEFAULT_MODEL, overrides=()):
    """Hydra config exactly as ``python test_evaluated_model.py +benchmark=... +model=...`` would see it."""
    from hydra import compose, initialize_config_dir
    from hydra.core.global_hydra import GlobalHydra

    GlobalHydra.instance().clear()
    with initialize_config_dir(config_dir=str(CONFIG_DIR), version_base=None):
        return compose(config_name="base.yaml",
                       overrides=[f"+benchmark={benchmark}", f"+model={model}", *overrides])


def get_dataset_and_loaders(cfg, batch_size: int = 32, batch_size_test: int = 128, num_workers: int = 2):
    """Returns (dataset, (train, val, test), dims). Copy of the PEMS branch of test_evaluated_model.py."""
    from experiments.datasets import get_PEMS_dataset
    from experiments.datasets.get_data_loader import get_dataloader, get_forecasting_dataset, regenerate_splits

    if cfg.benchmark.type != "PEMS":
        raise NotImplementedError("the pilot only handles the PEMS benchmark type")
    root = Path(cfg.benchmark.dataset_root) / cfg.benchmark.type
    window_size = int(cfg.benchmark.dataloader.window_size)
    data_info, _, _, (border1s, border2s) = get_PEMS_dataset.get_test_dataset(
        root, dataset_name=cfg.benchmark.name, file_name=cfg.benchmark.file_name,
        series_type=cfg.benchmark.series_type, window_size=window_size,
        do_normalization=cfg.benchmark.do_normalization,
        forecasting_horizon=cfg.benchmark.external_forecast_horizon,
        make_dataset_uni_variant=cfg.benchmark.get("make_dataset_uni_variant", False), flag="test")
    dataset = get_forecasting_dataset(dataset_name=cfg.benchmark.name, **data_info)
    dataset.lagged_value = [0]
    horizon = dataset.n_prediction_steps
    split_ms = [
        np.arange(window_size - 1, border2s[0] - horizon),
        np.arange(border1s[1] - 1, border2s[1] - horizon),
        np.arange(border1s[2] - 1, border2s[2] - horizon),
    ]
    split = regenerate_splits(dataset, val_share=None, splits_ms=split_ms)
    loaders = get_dataloader(dataset=dataset, splits=split, batch_size=batch_size, window_size=window_size,
                             is_test_sets=[False, True, True], batch_size_test=batch_size_test,
                             num_workers=num_workers)
    num_targets = int(dataset.num_targets)
    n_time_features = len(dataset.time_feature_transform)
    search_sample_interval = int(cfg.benchmark.dataloader.get("search_sample_interval", 1))
    if search_sample_interval != 1:
        raise NotImplementedError("pilot assumes search_sample_interval == 1 (true for all PEMS configs)")
    dims = {
        "benchmark": str(cfg.benchmark.name),
        "window_size": window_size,
        "n_prediction_steps": int(horizon),
        "num_targets": num_targets,
        "n_time_features": n_time_features,
        "d_input_past": num_targets + n_time_features,
        # mixed_concat: the flat forecast (num_targets) is concatenated to the future time features
        "d_input_future": num_targets + n_time_features,
        "d_output": num_targets,
        "split_sizes": [int(len(s)) for s in split],
        "batch_size": batch_size,
        "batch_size_test": batch_size_test,
    }
    return dataset, loaders, dims


def preprocess_batch(X: dict, target_scaler, window_size: int, device: torch.device):
    """Functional copy of SampledForecastingNetTrainer.preprocessing (lagged_values=[0], no cached mask).
    Returns x_past (B, W, N+F), x_future (B, H, F), loc, scale."""
    from autoPyTorch.pipeline.components.setup.network.forecasting_architecture import get_lagged_subsequences
    from tsf_oneshot.training.trainer import pad_tensor
    from tsf_oneshot.training.training_utils import scale_value

    past_targets = X["past_targets"].float()
    past_features = X["past_features"]
    if past_features is not None:
        past_features = past_features.float()
    past_observed_targets = X["past_observed_targets"]
    future_features = X["future_features"]
    if future_features is None:
        raise ValueError("future_features is None; the mixed_concat net needs future time features")
    future_features = future_features.float()

    if window_size < past_targets.shape[1]:
        past_targets = past_targets.to(device)
        past_observed_targets = past_observed_targets.to(device)
        past_targets[:, -window_size:], _, loc, scale = target_scaler.transform(
            past_targets[:, -window_size:], past_observed_targets[:, -window_size:])
        past_targets[:, :-window_size] = torch.where(
            past_observed_targets[:, :-window_size],
            scale_value(past_targets[:, :-window_size], loc, scale, device=device),
            past_targets[:, :-window_size])
    else:
        past_targets, _, loc, scale = target_scaler.transform(
            past_targets.to(device), past_observed_targets.to(device))
    truncated_past_targets, _ = get_lagged_subsequences(past_targets, window_size, [0], None)

    if past_features is not None:
        if window_size <= past_features.shape[1]:
            past_features = past_features[:, -window_size:]
        else:
            past_features = pad_tensor(past_features, window_size)
        x_past = torch.cat([truncated_past_targets, past_features.to(device=device)], dim=-1)
    else:
        x_past = truncated_past_targets
    x_future = future_features.to(device)
    return x_past, x_future, loc, scale


def repo_loss(model, target: torch.Tensor, prediction, loc, scale, device: torch.device) -> torch.Tensor:
    """The loss SampledForecastingNetTrainer.update_weights minimises: the head's loss on the
    rescaled prediction against the raw (dataset-normalised) future targets."""
    from tsf_oneshot.training.training_utils import rescale_output

    prediction = rescale_output(prediction, loc, scale, device=device)
    return model.get_training_loss(target, prediction)


def _to_cpu_float(t):
    return t.detach().to("cpu", torch.float32).contiguous() if torch.is_tensor(t) else t


def save_probe_batch(benchmark: str, out: str | Path, batch_size: int = 32, n_batches: int = 4, seed: int = 0) -> dict:
    """W1 / Section 3.3: seed 0, the repo's train loader (shuffle=True), first n_batches batches, preprocessed
    with the repo's TargetScaler, saved to CPU. Every proxy run loads this file, never a live loader."""
    from autoPyTorch.pipeline.components.setup.forecasting_target_scaling.utils import TargetScaler

    cfg = get_cfg(benchmark)
    seed_everything(seed)
    dataset, (train_loader, _, _), dims = get_dataset_and_loaders(cfg, batch_size=batch_size)
    target_scaler = TargetScaler(cfg.train.targe_scaler)
    batches = []
    it = iter(train_loader)
    for b in range(n_batches):
        X, y = next(it)
        x_past, x_future, loc, scale = preprocess_batch(X, target_scaler, dims["window_size"], torch.device("cpu"))
        batches.append({
            "x_past": _to_cpu_float(x_past),
            "x_future": _to_cpu_float(x_future),
            "target": _to_cpu_float(y["future_targets"]),
            "loc": _to_cpu_float(loc),
            "scale": _to_cpu_float(scale),
        })
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "benchmark": benchmark, "seed": seed, "batch_size": batch_size, "n_batches": n_batches,
        "target_scaler": str(cfg.train.targe_scaler), "dims": dims, "batches": batches,
        "shapes": {k: list(v.shape) for k, v in batches[0].items() if torch.is_tensor(v)},
        "created": _dt.datetime.now().isoformat(timespec="seconds"), "torch": torch.__version__,
    }
    torch.save(payload, out)
    sha1 = hashlib.sha1(out.read_bytes()).hexdigest()
    out.with_suffix(".sha1").write_text(sha1 + "\n")
    meta = {k: v for k, v in payload.items() if k != "batches"}
    meta["sha1"] = sha1
    out.with_suffix(".json").write_text(json.dumps(meta, indent=2))
    return meta


def load_probe_batch(path: str | Path = DEFAULT_PROBE):
    path = Path(path)
    payload = torch.load(path, map_location="cpu", weights_only=False)
    sha_file = path.with_suffix(".sha1")
    sha1 = sha_file.read_text().strip() if sha_file.exists() else hashlib.sha1(path.read_bytes()).hexdigest()
    return payload, sha1


def main():
    ap = argparse.ArgumentParser(description="pilot data utilities")
    ap.add_argument("--save-probe-batch", action="store_true")
    ap.add_argument("--benchmark", default=DEFAULT_BENCHMARK)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--n-batches", type=int, default=4)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=DEFAULT_PROBE)
    args = ap.parse_args()
    if args.save_probe_batch:
        meta = save_probe_batch(args.benchmark, args.out, args.batch_size, args.n_batches, args.seed)
        print(json.dumps(meta, indent=2))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
