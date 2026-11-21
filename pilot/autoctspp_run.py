"""Trains architectures of the AutoCTS++ search space with the released training function, unchanged.

The released script (exps/generate_seeds.py of the upstream repository) is imported, so the model, the loader, the loss, the
optimiser and the metrics are its own.  This file adds what the released script does not have: a list of architectures from a
file, a seed per run, an epoch count, a batch size for the validation and test parts (the released value is 1), one json per
run, and a skip of finished runs.  Survey/experiments/autoctspp-plan.md.

  python -m pilot.autoctspp_run sample --n 30 --sample-seed 0 --out results/autoctspp/pemsbay_p12/sample.json
  python -m pilot.autoctspp_run train --archs FILE --seeds 0 1 2 --epochs 100 --eval-batch 64 --out results/autoctspp/pemsbay_p12/train
FILE is a json list of architectures or the .npy that the released search writes.  An architecture is 7 pairs (input node,
operator).  Its id is the 14 digits in a row.
"""
import argparse, contextlib, io, json, os, re, sys, time
from pathlib import Path

import numpy as np

DATASET_FLAGS = {"pemsbay": ["--dataset", "PEMS-BAY/pems-bay", "--datatype", "h5", "--in_dim", "1", "--num_nodes", "325",
                             "--ratio", "0.7", "0.1", "0.2"]}


def arch_id(arch):
    return "".join(str(int(v)) for pair in arch for v in pair)


def load_upstream(up, dataset, seq_len):
    """Imports the released training script with the flags of its README; the working directory becomes <up>/scripts."""
    up = Path(up).resolve()
    os.chdir(up / "scripts")
    sys.path[:0] = [str(up), str(up / "exps")]
    sys.argv = ["generate_seeds.py", *DATASET_FLAGS[dataset], "--seq_len", str(seq_len), "--mode", "train"]
    import generate_seeds as gs
    return gs


def read_archs(path):
    path = Path(path)
    archs = np.load(path).tolist() if path.suffix == ".npy" else json.loads(path.read_text())
    return [[[int(a), int(b)] for a, b in arch] for arch in archs]


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
    for arch, seed in runs:
        d = out / arch_id(arch) / f"seed{seed}"
        if (d / "metrics.json").exists():
            print(f"skip {arch_id(arch)} seed {seed}", flush=True); continue
        d.mkdir(parents=True, exist_ok=True)
        utils.set_seed(seed)
        torch.backends.cudnn.deterministic = True
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
        buf = io.StringIO()
        t0 = time.time()
        with contextlib.redirect_stdout(buf):
            tr, va, te = gs.train_arch_from_scratch(loader, adj_mx, loader["scaler"], arch)
        sec = time.time() - t0
        train_sec = [float(x) for x in re.findall(r"train epoch time: ([0-9.]+)", buf.getvalue())]
        va_mae = [float(v[0]) for v in va]
        best = int(np.argmin(va_mae))
        rec = {"arch": arch, "arch_id": arch_id(arch), "seed": seed, "epochs": a.epochs, "eval_batch": a.eval_batch,
               "seconds": sec, "train_seconds": float(np.sum(train_sec)), "sec_per_train_epoch": float(np.mean(train_sec)),
               "sec_per_eval_epoch": (sec - float(np.sum(train_sec))) / a.epochs,
               "peak_mem_gb": torch.cuda.max_memory_allocated() / 2 ** 30 if torch.cuda.is_available() else None,
               "best_epoch": best, "val_mae": va_mae[best],
               "test_mae": float(te[best][0]), "test_rmse": float(te[best][1]), "test_mape": float(te[best][2]),
               "train": np.array(tr, dtype=float).tolist(), "valid": np.array(va, dtype=float).tolist(),
               "test": np.array(te, dtype=float)[:, :3].tolist()}
        (d / "metrics.json").write_text(json.dumps(rec))
        print(f"done {rec['arch_id']} seed {seed} epochs {a.epochs} eval_batch {a.eval_batch} seconds {sec:.0f} "
              f"train_epoch {rec['sec_per_train_epoch']:.1f} eval_epoch {rec['sec_per_eval_epoch']:.1f} "
              f"best {best} val {rec['val_mae']:.4f} test {rec['test_mae']:.4f} {rec['test_rmse']:.4f} {rec['test_mape']:.4f}", flush=True)


if __name__ == "__main__":
    main()
