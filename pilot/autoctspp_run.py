"""Trains architectures of the AutoCTS++ search space with the released training function, unchanged.

The released script (exps/generate_seeds.py of the upstream repository) is imported, so the model, the loader, the loss, the
optimiser and the metrics are its own.  This file adds what the released script does not have: a list of architectures from a
file, a seed per run, an epoch count, a batch size for the validation and test parts (the released value is 1), one json per
run, a skip of finished runs, and a resume of a run across jobs (a checkpoint after each epoch).  The resume keeps the
released statements: it takes the source of the released function and inserts three lines (resumable()).
Survey/experiments/autoctspp-plan.md.

  python -m pilot.autoctspp_run sample --n 30 --sample-seed 0 --out results/autoctspp/pemsbay_p12/sample.json
  python -m pilot.autoctspp_run train --archs FILE --seeds 0 1 2 --epochs 100 --eval-batch 64 --out results/autoctspp/pemsbay_p12/train
FILE is a json list of architectures or the .npy that the released search writes.  An architecture is 7 pairs (input node,
operator).  Its id is the 14 digits in a row.
An entry of FILE can also be a hand model: {"hand_model": "stid" | "staeformer", "clock": "index" | "none"} (pilot.hand_models,
published sizes).  It takes the place of the released network inside the released training function, so the split, the scaler, the
loss, the optimiser, the schedule and the metrics are the same.  With the clock "index" the input gets two more channels, the step
of the day and the day of the week of the file index; the released loader gives the value only.  Its id is <model>_<clock>.
An entry can also be an architecture of the search space that reads the clock: {"arch": [7 pairs], "clock": "channels" | "embed"}.
The released network is built unchanged but for its input layer (pilot.hand_models.ClockStart).  Its id is <14 digits>_clock_<mode>.
"""
import argparse, contextlib, inspect, io, json, os, random, re, sys, textwrap, time
from pathlib import Path

import numpy as np

DATASET_FLAGS = {"pemsbay": ["--dataset", "PEMS-BAY/pems-bay", "--datatype", "h5", "--in_dim", "1", "--num_nodes", "325",
                             "--ratio", "0.7", "0.1", "0.2"]}


def arch_id(arch):
    if isinstance(arch, dict) and "arch" in arch:
        return f"{arch_id(arch['arch'])}_clock_{arch['clock']}"
    if isinstance(arch, dict):
        return f"{arch['hand_model']}_{arch['clock']}"
    return "".join(str(int(v)) for pair in arch for v in pair)


def load_upstream(up, dataset, seq_len):
    """Imports the released training script with the flags of its README; the working directory becomes <up>/scripts."""
    up = Path(up).resolve()
    os.chdir(up / "scripts")
    sys.path[:0] = [str(up), str(up / "exps")]
    sys.argv = ["generate_seeds.py", *DATASET_FLAGS[dataset], "--seq_len", str(seq_len), "--mode", "train"]
    import generate_seeds as gs
    return gs


def with_clock(loader, h5_path, ratio, seq_len, batch, eval_batch, utils):
    """The released loader with two more input channels: the step of the day (0..287) and the day of the week (0..6) of each step."""
    import pandas as pd
    idx = pd.read_hdf(h5_path).index
    assert (idx[1] - idx[0]).total_seconds() == 300, "the clock of the hand models counts steps of 5 minutes"
    tod, dow = ((idx.hour * 60 + idx.minute) // 5).to_numpy(), idx.dayofweek.to_numpy()
    n = len(idx)
    l1, l2 = int(n * ratio[0]), int(n * (ratio[0] + ratio[1]))
    out = dict(loader)
    for key, a, b in (("train", 0, l1), ("val", l1, l2), ("test", l2, n)):
        x = loader["x_" + key]
        S, L, N, _ = x.shape
        assert S == b - a - 2 * seq_len + 1 and L == seq_len, f"the windows of {key} do not match the split of the release"
        pos = a + np.arange(S)[:, None] + np.arange(L)[None]
        clock = np.stack([tod[pos], dow[pos]], -1).astype("float32")
        out["x_" + key] = np.concatenate([x, np.broadcast_to(clock[:, :, None, :], (S, L, N, 2))], -1)
    out["train_loader"] = utils.DataLoader(out["x_train"], out["y_train"], batch)
    out["val_loader"] = utils.DataLoader(out["x_val"], out["y_val"], eval_batch)
    out["test_loader"] = utils.DataLoader(out["x_test"], out["y_test"], eval_batch)
    return out


def hand_network(gs):
    """gs.Network also builds a hand model when the architecture is a hand-model record."""
    released = gs.Network

    def network(adj_mx, scaler, args, arch):
        if isinstance(arch, dict) and "arch" in arch:
            import copy
            from pilot.hand_models import ClockStart
            args_clock = copy.copy(args)
            args_clock.in_dim = 3 if arch["clock"] == "channels" else 1
            net = released(adj_mx, scaler, args_clock, arch["arch"])
            net.start_linear = ClockStart(net.start_linear, arch["clock"], args.hid_dim)
            return net
        if isinstance(arch, dict):
            from pilot.hand_models import ReleaseNet
            return ReleaseNet(arch["hand_model"], arch["clock"], args.num_nodes, args.output_len)
        return released(adj_mx, scaler, args, arch)
    gs.Network = network


class Paused(Exception):
    """The job has no time for one more epoch; the checkpoint holds the run."""


class Stopped(Exception):
    """The run reached --stop-epoch; the checkpoint holds it, and a later call with a larger value or none continues it."""


def resumable(gs):
    """The released train_arch_from_scratch with three inserted lines: load a checkpoint, start at its epoch, save after an epoch."""
    src = textwrap.dedent(inspect.getsource(gs.train_arch_from_scratch))
    edits = [
        ("def train_arch_from_scratch(dataloader, adj_mx, scaler, arch):",
         "def train_arch_resumable(dataloader, adj_mx, scaler, arch, _hook):"),
        ("    test_metrics_list = []\n",
         "    test_metrics_list = []\n"
         "    _start = _hook.resume(model, optimizer, dataloader, train_metrics_list, valid_metrics_list, test_metrics_list)\n"),
        ("    for epoch_num in range(args.epochs):\n", "    for epoch_num in range(_start, args.epochs):\n"),
        ("\n    return train_metrics_list, valid_metrics_list, test_metrics_list",
         "\n        _hook.after_epoch(epoch_num, model, optimizer, train_metrics_list, valid_metrics_list, test_metrics_list)\n"
         "\n    return train_metrics_list, valid_metrics_list, test_metrics_list"),
    ]
    for old, new in edits:
        assert src.count(old) == 1, f"the released function changed: {old!r}"
        src = src.replace(old, new)
    exec(compile(src, "<train_arch_from_scratch of the release, with resume>", "exec"), gs.__dict__)
    return gs.__dict__["train_arch_resumable"]


class Hook:
    """State of one run across jobs: the weights, the optimiser, the metric lists, every random state, the order of the train set."""

    def __init__(self, path, epochs, deadline, pause_after, buf, label, stop_epoch=None):
        self.path, self.epochs, self.deadline, self.pause_after, self.buf, self.label = path, epochs, deadline, pause_after, buf, label
        self.stop_epoch, self.curves = stop_epoch, None
        self.seconds, self.train_secs, self.epoch_secs, self.new, self.segments, self.last = 0.0, [], [], 0, 1, -1

    def resume(self, model, optimizer, loader, tr, va, te):
        import torch
        tl = loader["train_loader"]
        if not hasattr(tl, "_xs0"):
            tl._xs0, tl._ys0 = tl.xs, tl.ys                 # the order of a new loader; every run starts from it
        tl.xs, tl.ys = tl._xs0, tl._ys0
        self.order = np.arange(tl.size)
        hook = self

        def shuffle():                                      # the released shuffle; it also records the order
            perm = np.random.permutation(tl.size)
            tl.xs, tl.ys = tl.xs[perm], tl.ys[perm]
            hook.order = hook.order[perm]
        tl.shuffle = shuffle
        self.t = time.time()
        if not self.path.exists():
            return 0
        ck = torch.load(self.path, map_location="cpu", weights_only=False)      # the random states stay on the CPU; the weights are copied
        model.load_state_dict(ck["model"]); optimizer.load_state_dict(ck["optimizer"])
        tr[:], va[:], te[:] = ck["train"], ck["valid"], ck["test"]
        self.order = ck["order"]; tl.xs, tl.ys = tl._xs0[self.order], tl._ys0[self.order]
        np.random.set_state(ck["np_rng"]); random.setstate(ck["py_rng"]); torch.set_rng_state(ck["torch_rng"])
        if torch.cuda.is_available():
            torch.cuda.set_rng_state_all(ck["cuda_rng"])
        self.seconds, self.train_secs, self.epoch_secs, self.segments = ck["seconds"], ck["train_secs"], ck["epoch_secs"], ck["segments"] + 1
        self.last = ck["epoch"]
        print(f"resume {self.label} after epoch {self.last}", file=sys.__stdout__, flush=True)
        return self.last + 1

    def after_epoch(self, epoch, model, optimizer, tr, va, te):
        import torch
        now = time.time()
        self.epoch_secs.append(now - self.t); self.seconds += now - self.t; self.t = now
        self.train_secs.append(float(re.findall(r"train epoch time: ([0-9.]+)", self.buf.getvalue())[-1]))
        self.buf.seek(0); self.buf.truncate(0)
        self.last, self.new, self.curves = epoch, self.new + 1, (tr, va, te)
        print(f"epoch {epoch} {self.label} seconds {self.epoch_secs[-1]:.0f} val {float(va[-1][0]):.4f} test {float(te[-1][0]):.4f}",
              file=sys.__stdout__, flush=True)
        if epoch + 1 >= self.epochs:
            return
        ck = {"epoch": epoch, "model": model.state_dict(), "optimizer": optimizer.state_dict(), "train": list(tr), "valid": list(va),
              "test": list(te), "order": self.order, "np_rng": np.random.get_state(), "py_rng": random.getstate(),
              "torch_rng": torch.get_rng_state(), "cuda_rng": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
              "seconds": self.seconds, "train_secs": self.train_secs, "epoch_secs": self.epoch_secs, "segments": self.segments}
        tmp = self.path.with_suffix(".tmp")
        torch.save(ck, tmp); os.replace(tmp, self.path)
        self.seconds += time.time() - self.t; self.t = time.time()
        if self.stop_epoch and epoch + 1 >= self.stop_epoch:
            raise Stopped()
        if (self.pause_after and self.new >= self.pause_after) or self.deadline - self.t < 1.5 * max(self.epoch_secs) + 120:
            raise Paused()


def read_archs(path):
    path = Path(path)
    archs = np.load(path).tolist() if path.suffix == ".npy" else json.loads(path.read_text())
    return [arch if isinstance(arch, dict) else [[int(a), int(b)] for a, b in arch] for arch in archs]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["sample", "train"])
    p.add_argument("--up", default=os.path.join(os.environ.get("NAS_ROOT", ".."), "AutoCTS_plusplus"))
    p.add_argument("--dataset", default="pemsbay")
    p.add_argument("--seq-len", type=int, default=12)
    p.add_argument("--n", type=int, default=30)
    p.add_argument("--sample-seed", type=int, default=0)
    p.add_argument("--archs")
    p.add_argument("--seeds", type=int, nargs="+", default=[0])
    p.add_argument("--epochs", type=int, default=100)
    p.add_argument("--eval-batch", type=int, default=1, help="released value: 1")
    p.add_argument("--shard", default=None, help="k/n: every n-th run from the k-th")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--out", required=True)
    p.add_argument("--wall-hours", type=float, default=7.5, help="time of this call when the job gives no end time")
    p.add_argument("--pause-after", type=int, default=None, help="stop after this number of new epochs (a check of the resume)")
    p.add_argument("--stop-epoch", type=int, default=None,
                   help="end each run after this number of epochs of the --epochs schedule, keep its checkpoint, write partial.json, go to the next run")
    a = p.parse_args()
    out = Path(a.out).resolve()
    archs_path = Path(a.archs).resolve() if a.archs else None
    gs = load_upstream(a.up, a.dataset, a.seq_len)
    import torch, utils

    if a.cmd == "sample":                       # the sampler of the released script, distinct architectures
        np.random.seed(a.sample_seed)
        seen, archs = set(), []
        while len(archs) < a.n:
            arch = [[int(x), int(y)] for x, y in gs.Random_NAS.sample_arch()]
            if arch_id(arch) not in seen:
                seen.add(arch_id(arch)); archs.append(arch)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(archs))
        print(f"wrote {len(archs)} architectures to {out}")
        return

    archs = read_archs(archs_path)
    runs = [(arch, s) for arch in archs for s in a.seeds]
    if a.shard:
        k, n = (int(v) for v in a.shard.split("/"))
        runs = [r for i, r in enumerate(runs) if i % n == k]
    if a.limit:
        runs = runs[:a.limit]
    g = gs.args
    g.epochs = a.epochs
    adj_mx = gs.load_adj("../data/PEMS-BAY/adj_mx_bay.pkl")[2]
    t0 = time.time()
    loader = gs.generate_data(os.path.join("../data", g.dataset + ".h5"), g.task, g.seq_len, g.output_len, g.in_dim, g.datatype,
                              g.batch_size, a.eval_batch, g.ratio)
    print(f"data {time.time() - t0:.0f} s; train {loader['x_train'].shape} val {loader['x_val'].shape} test {loader['x_test'].shape}; "
          f"gpu {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none'}", flush=True)
    train = resumable(gs)
    hand_network(gs)
    clock_loader = None
    end = os.environ.get("SLURM_JOB_END_TIME")
    deadline = float(end) if end else time.time() + a.wall_hours * 3600
    for arch, seed in runs:
        d = out / arch_id(arch) / f"seed{seed}"
        if (d / "metrics.json").exists():
            print(f"skip {arch_id(arch)} seed {seed}", flush=True); continue
        if a.stop_epoch and (d / "partial.json").exists() and json.loads((d / "partial.json").read_text())["epochs_done"] >= a.stop_epoch:
            print(f"skip {arch_id(arch)} seed {seed} (stopped)", flush=True); continue
        d.mkdir(parents=True, exist_ok=True)
        utils.set_seed(seed)
        torch.backends.cudnn.deterministic = True
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
        buf = io.StringIO()
        run_loader = loader
        if isinstance(arch, dict) and arch["clock"] != "none":
            if clock_loader is None:
                clock_loader = with_clock(loader, os.path.join("../data", g.dataset + ".h5"), g.ratio, g.seq_len, g.batch_size, a.eval_batch, utils)
            run_loader = clock_loader
        hook = Hook(d / "ckpt.pt", a.epochs, deadline, a.pause_after, buf, f"{arch_id(arch)} seed {seed}", a.stop_epoch)
        try:
            with contextlib.redirect_stdout(buf):
                tr, va, te = train(run_loader, adj_mx, loader["scaler"], arch, hook)
        except Paused:
            print(f"paused {arch_id(arch)} seed {seed} after epoch {hook.last} of {a.epochs}; "
                  f"mean seconds per epoch {np.mean(hook.epoch_secs):.0f}", flush=True)
            break                                           # the job ends; the next job continues this run
        except Stopped:
            tr, va, te = hook.curves
            va_mae = [float(v[0]) for v in va]
            best = int(np.argmin(va_mae))
            rec = {"arch": arch, "arch_id": arch_id(arch), "seed": seed, "epochs": a.epochs, "epochs_done": hook.last + 1,
                   "eval_batch": a.eval_batch, "seconds": hook.seconds, "segments": hook.segments,
                   "sec_per_train_epoch": float(np.mean(hook.train_secs)), "best_epoch": best, "val_mae": va_mae[best],
                   "test_mae": float(te[best][0]), "test_rmse": float(te[best][1]), "test_mape": float(te[best][2]),
                   "train": np.array(tr, dtype=float).tolist(), "valid": np.array(va, dtype=float).tolist(),
                   "test": np.array(te, dtype=float)[:, :3].tolist()}
            (d / "partial.json").write_text(json.dumps(rec))
            print(f"stopped {arch_id(arch)} seed {seed} after epoch {hook.last} of {a.epochs} seconds {hook.seconds:.0f} "
                  f"best {best} val {rec['val_mae']:.4f} test {rec['test_mae']:.4f}", flush=True)
            continue
        sec, train_sec = hook.seconds, hook.train_secs
        va_mae = [float(v[0]) for v in va]
        best = int(np.argmin(va_mae))
        rec = {"arch": arch, "arch_id": arch_id(arch), "seed": seed, "epochs": a.epochs, "eval_batch": a.eval_batch,
               "seconds": sec, "segments": hook.segments, "train_seconds": float(np.sum(train_sec)), "sec_per_train_epoch": float(np.mean(train_sec)),
               "sec_per_eval_epoch": (sec - float(np.sum(train_sec))) / a.epochs,
               "peak_mem_gb": torch.cuda.max_memory_allocated() / 2 ** 30 if torch.cuda.is_available() else None,
               "best_epoch": best, "val_mae": va_mae[best],
               "test_mae": float(te[best][0]), "test_rmse": float(te[best][1]), "test_mape": float(te[best][2]),
               "train": np.array(tr, dtype=float).tolist(), "valid": np.array(va, dtype=float).tolist(),
               "test": np.array(te, dtype=float)[:, :3].tolist()}
        (d / "metrics.json").write_text(json.dumps(rec))
        (d / "ckpt.pt").unlink(missing_ok=True)
        print(f"done {rec['arch_id']} seed {seed} epochs {a.epochs} eval_batch {a.eval_batch} seconds {sec:.0f} "
              f"train_epoch {rec['sec_per_train_epoch']:.1f} eval_epoch {rec['sec_per_eval_epoch']:.1f} "
              f"best {best} val {rec['val_mae']:.4f} test {rec['test_mae']:.4f} {rec['test_rmse']:.4f} {rec['test_mape']:.4f}", flush=True)


if __name__ == "__main__":
    main()
