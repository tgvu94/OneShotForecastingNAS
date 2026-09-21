"""Train one genotype with the fixed schedule (Section 4.1), resumable, one result directory per (arch, seed).

    results/train/<arch_id>/seed<s>/{metrics.json, log.csv, ckpt.pt}

The training loop is the repo's own ``SampledForecastingNetTrainer`` (same preprocessing, AMP, grad clip, loss
and evaluation as ``experiments/test_evaluated_model.py``), with the repo's eval optimiser / scheduler config
(``w_optimizer_eval``: Adam 1e-3, wd 0; ``lr_scheduler_eval``: CosineAnnealingWarmRestarts T_0=20, eta_min 1e-8;
``grad_clip`` 0.1; AMP on; TargetScaler 'standard').  Early stopping is on val MAE (the correlation target),
with a minimum number of epochs.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import math
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_BENCHMARK = "PEMS/pems04/pems04_12"


def parse_args(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--arch-id", required=True)
    ap.add_argument("--archs", "--archs-file", dest="archs", default="results/archs.jsonl")
    ap.add_argument("--epochs", "--max-epochs", dest="epochs", type=int, default=20, help="max epochs")
    ap.add_argument("--patience", type=int, default=5, help="early-stopping patience on val_mae")
    ap.add_argument("--min-epochs", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--benchmark", default=DEFAULT_BENCHMARK)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--num-workers", type=int, default=2)
    ap.add_argument("--out-root", default="results/train")
    ap.add_argument("--prune-ckpt", action="store_true", help="delete ckpt.pt once status is done")
    return ap.parse_args(argv)


def write_json(path: Path, obj: dict):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, indent=2))
    tmp.replace(path)


def fork_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def main(argv=None) -> int:
    args = parse_args(argv)
    out_dir = Path(args.out_root) / args.arch_id / f"seed{args.seed}"
    metrics_path = out_dir / "metrics.json"
    # cheap "already done" exit before any heavy import (< 5 s)
    if metrics_path.exists():
        rec = json.load(open(metrics_path))
        if rec.get("status") == "done":
            print(f"already done: {metrics_path} (epochs_run={rec.get('epochs_run')}, "
                  f"val_mae={rec.get('val_mae')}, schedule max_epochs={rec.get('schedule', {}).get('max_epochs')})")
            return 0

    import numpy as np
    import torch
    import wandb
    from autoPyTorch.pipeline.components.setup.forecasting_target_scaling.utils import TargetScaler
    from omegaconf import OmegaConf
    from tsf_oneshot.training.samplednet_trainer import SampledForecastingNetTrainer
    from tsf_oneshot.training.utils import LR_SCHEDULER_TYPE, get_lr_scheduler, get_optimizer

    from pilot.build_net import build_discrete_net, count_params
    from pilot.data import get_cfg, get_dataset_and_loaders, seed_everything
    from pilot.genotype import find_arch, summarize

    torch.multiprocessing.set_sharing_strategy("file_system")
    wandb.init(mode="disabled")

    class PilotTrainer(SampledForecastingNetTrainer):
        """train_epoch of the repo, plus the mean training loss of the epoch."""

        def train_epoch(self, epoch: int):
            self.model.train()
            losses = []
            for (train_X, train_y) in self.train_loader:
                torch.cuda.empty_cache()
                w_loss, _ = self.update_weights(train_X, train_y)
                losses.append(float(w_loss.detach()))
                torch.cuda.empty_cache()
            self.last_train_loss = float(np.mean(losses)) if losses else float("nan")
            val_res = self.evaluate(self.val_loader, epoch, "val")
            test_res = self.evaluate(self.test_loader, epoch, "test")
            if self.lr_scheduler_w is not None and self.lr_scheduler_type == LR_SCHEDULER_TYPE.epoch:
                self.lr_scheduler_w.step()
            return val_res, test_res

    rec_arch = find_arch(args.arch_id, args.archs)
    g = rec_arch["genotype"]
    print(f"arch {args.arch_id}: {summarize(g)}")
    out_dir.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda")

    cfg = get_cfg(args.benchmark)
    seed_everything(args.seed)
    dataset, (train_loader, val_loader, test_loader), dims = get_dataset_and_loaders(
        cfg, batch_size=args.batch_size, num_workers=args.num_workers)
    seed_everything(args.seed)  # init seed, immediately before build
    model = build_discrete_net(g, dims)
    n_params = count_params(model)

    optim_groups = model.get_weight_optimizer_parameters(cfg.w_optimizer_eval.weight_decay)
    optimizer = get_optimizer(cfg_optimizer=cfg.w_optimizer_eval, optim_groups=optim_groups, wd_in_p_groups=True)
    scheduler = get_lr_scheduler(optimizer=optimizer, cfg_lr_scheduler=cfg.lr_scheduler_eval,
                                 steps_per_epoch=len(train_loader))
    trainer = PilotTrainer(
        model=model, w_optimizer=optimizer, lr_scheduler_w=scheduler,
        train_loader=train_loader, val_loader=val_loader, test_loader=test_loader,
        window_size=dims["window_size"], n_prediction_steps=dataset.n_prediction_steps,
        lagged_values=dataset.lagged_value, sample_interval=1,
        target_scaler=TargetScaler(cfg.train.targe_scaler), grad_clip=cfg.train.grad_clip,
        device=device, amp_enable=cfg.train.amp_enable)

    min_epochs = min(args.min_epochs, args.epochs)
    schedule = {
        "benchmark": args.benchmark, "max_epochs": args.epochs, "patience": args.patience, "min_epochs": min_epochs,
        "early_stopping_metric": "val_mae", "batch_size": args.batch_size, "batch_size_test": dims["batch_size_test"],
        "optimizer": OmegaConf.to_container(cfg.w_optimizer_eval, resolve=True),
        "lr_scheduler": OmegaConf.to_container(cfg.lr_scheduler_eval, resolve=True),
        "grad_clip": float(cfg.train.grad_clip), "amp": bool(cfg.train.amp_enable),
        "target_scaler": str(cfg.train.targe_scaler), "loss": f"head={g['head']}",
        "train_windows": dims["split_sizes"][0], "iters_per_epoch": len(train_loader),
    }

    # FLOPs of one forward pass on one training batch (torch.utils.flop_counter; cuDNN RNN kernels may be invisible)
    flops, flops_note = None, None
    try:
        from torch.utils.flop_counter import FlopCounterMode
        X0, _ = next(iter(train_loader))
        x_past, x_future, _ = trainer.preprocessing(X0)  # returns (x_past, x_future, (loc, scale))
        model.eval()
        with torch.no_grad(), FlopCounterMode(display=False) as fc:
            model(x_past, x_future)
        flops = int(fc.get_total_flops())
        flops_note = f"one forward, batch {x_past.shape[0]}, FlopCounterMode"
        model.train()
    except Exception as e:  # noqa: BLE001
        flops_note = f"failed: {e!r}"

    # ---- resume
    ckpt_path, log_path = out_dir / "ckpt.pt", out_dir / "log.csv"
    history, best, no_improve, train_seconds, start_epoch = [], None, 0, 0.0, 0
    if ckpt_path.exists():
        ck = torch.load(ckpt_path, map_location="cpu", weights_only=False)
        model.load_state_dict(ck["model"])
        optimizer.load_state_dict(ck["optimizer"])
        scheduler.load_state_dict(ck["scheduler"])
        trainer.scaler.load_state_dict(ck["amp_scaler"])
        torch.set_rng_state(ck["rng"]["torch"])
        torch.cuda.set_rng_state_all(ck["rng"]["cuda"])
        np.random.set_state(ck["rng"]["numpy"])
        import random as _random
        _random.setstate(ck["rng"]["python"])
        history, best, no_improve = ck["history"], ck["best"], ck["no_improve"]
        train_seconds, start_epoch = ck["train_seconds"], ck["epoch"]
        print(f"resumed from {ckpt_path} at epoch {start_epoch}")
    model.to(device)

    base = {"arch_id": args.arch_id, "space": g["space"], "seed": args.seed, "params": n_params,
            "flops": flops, "flops_note": flops_note, "schedule": schedule, "fork_commit": fork_commit(),
            "torch": torch.__version__, "gpu": torch.cuda.get_device_name(0)}
    write_json(metrics_path, {**base, "status": "running", "epochs_run": len(history), "history": history,
                              "started_at": _dt.datetime.now().isoformat(timespec="seconds")})

    stopped_early = False
    for epoch in range(start_epoch, args.epochs):
        torch.cuda.reset_peak_memory_stats(device)
        t0 = time.time()
        val_res, test_res = trainer.train_epoch(epoch)
        seconds = time.time() - t0
        train_seconds += seconds
        row = {"epoch": epoch, "train_loss": trainer.last_train_loss,
               "val_mse": float(val_res["MSE loss"]), "val_mae": float(val_res["MAE loss"]),
               "test_mse": float(test_res["MSE loss"]), "test_mae": float(test_res["MAE loss"]),
               "lr": float(optimizer.param_groups[0]["lr"]), "seconds": round(seconds, 1),
               "peak_mem_gb": round(torch.cuda.max_memory_allocated(device) / 1e9, 3),
               "wall": _dt.datetime.now().isoformat(timespec="seconds")}
        history.append(row)
        new_file = not log_path.exists()
        fieldnames = list(row)
        if not new_file:  # keep the header of a file written by an older version (resume)
            with open(log_path, newline="") as f:
                fieldnames = next(csv.reader(f), fieldnames)
        with open(log_path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            if new_file:
                w.writeheader()
            w.writerow(row)
        if best is None or (math.isfinite(row["val_mae"]) and row["val_mae"] < best["val_mae"]):
            best, no_improve = dict(row), 0
        else:
            no_improve += 1
        print(f"epoch {epoch}: train_loss={row['train_loss']:.4f} val_mae={row['val_mae']:.4f} "
              f"test_mae={row['test_mae']:.4f} ({seconds:.0f}s, {row['peak_mem_gb']} GB)")
        import random as _random
        torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict(),
                    "scheduler": scheduler.state_dict(), "amp_scaler": trainer.scaler.state_dict(),
                    "epoch": epoch + 1, "history": history, "best": best, "no_improve": no_improve,
                    "train_seconds": train_seconds,
                    "rng": {"torch": torch.get_rng_state(), "cuda": torch.cuda.get_rng_state_all(),
                            "numpy": np.random.get_state(), "python": _random.getstate()}}, ckpt_path)
        write_json(metrics_path, {**base, "status": "running", "epochs_run": len(history), "history": history})
        if not math.isfinite(row["val_mae"]):
            print("non-finite val_mae -> stop")
            break
        if epoch + 1 >= min_epochs and no_improve >= args.patience:
            stopped_early = True
            print(f"early stop: no val_mae improvement for {args.patience} epochs")
            break

    final = {**base, "status": "done", "epochs_run": len(history), "stopped_early": stopped_early,
             "best_epoch": best["epoch"], "val_mae": best["val_mae"], "val_mse": best["val_mse"],
             "test_mae": best["test_mae"], "test_mse": best["test_mse"],
             "train_seconds": round(train_seconds, 1),
             "peak_mem_gb": max(r["peak_mem_gb"] for r in history), "history": history,
             "finished_at": _dt.datetime.now().isoformat(timespec="seconds")}
    if not math.isfinite(best["val_mae"]):
        final["status"] = "failed"
        final["error"] = "non-finite val_mae"
    write_json(metrics_path, final)
    if args.prune_ckpt and final["status"] == "done":
        ckpt_path.unlink(missing_ok=True)
    print(f"{final['status']}: best epoch {best['epoch']} val_mae={best['val_mae']:.4f} test_mae={best['test_mae']:.4f} "
          f"in {train_seconds:.0f}s -> {metrics_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
