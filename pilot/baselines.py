"""Naive forecasting baselines on the repo's PEMS04-12 splits, in the same units the trainer reports (dataset-normalised
targets): ``last``: repeat the last observed value over the horizon; ``mean``: predict the training mean (0 in z-units).
Written once to results/tables/naive_baselines.json; ``pilot.check --phase 4`` uses them to detect collapsed runs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from pilot.data import DEFAULT_BENCHMARK, get_cfg, get_dataset_and_loaders, seed_everything


def evaluate(loader, window_size: int) -> dict:
    mae_last = mae_mean = mse_last = mse_mean = 0.0
    n = 0
    for X, y in loader:
        past = X["past_targets"].float()[:, -window_size:, :]
        target = y["future_targets"].float()
        last = past[:, -1:, :].expand_as(target)
        b = target.shape[0]
        mae_last += (last - target).abs().mean().item() * b
        mse_last += ((last - target) ** 2).mean().item() * b
        mae_mean += target.abs().mean().item() * b
        mse_mean += (target ** 2).mean().item() * b
        n += b
    return {"last_value": {"mae": mae_last / n, "mse": mse_last / n}, "train_mean": {"mae": mae_mean / n, "mse": mse_mean / n}, "n_windows": n}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", default=DEFAULT_BENCHMARK)
    ap.add_argument("--out", default="results/tables/naive_baselines.json")
    args = ap.parse_args()
    cfg = get_cfg(args.benchmark)
    seed_everything(0)
    dataset, (train_loader, val_loader, test_loader), dims = get_dataset_and_loaders(cfg, batch_size=128, num_workers=2)
    res = {"benchmark": args.benchmark, "units": "dataset-normalised (z-score) targets, same as metrics.json val_mae/test_mae",
           "val": evaluate(val_loader, dims["window_size"]), "test": evaluate(test_loader, dims["window_size"])}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
