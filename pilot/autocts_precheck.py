"""AutoCTS fallback pre-check (P3, Section 1 fallback).  Runs *their* code from ``~/nas/AutoCTS`` on PEMS04:
one discrete cell from their operator list (random ops, their discretisation: 2 incoming edges per node, cells
chained), 1 epoch with their loss / optimiser, then ``params, grad_norm_all, nwot`` on their first train batch.

    python -m pilot.autocts_precheck --autocts ~/nas/AutoCTS --data ~/scratch/all_datasets/PEMS --epochs 1
Writes results/autocts_precheck.json and results/autocts_precheck.md.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import random
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from torch import nn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autocts", default=os.path.join(os.environ.get("NAS_ROOT", os.path.expanduser("~/nas")), "AutoCTS"))
    ap.add_argument("--data", default=os.path.expanduser("~/scratch/all_datasets/PEMS"))
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--layers", type=int, default=4)
    ap.add_argument("--steps", type=int, default=4)
    ap.add_argument("--hid-dim", type=int, default=32)
    ap.add_argument("--out", default="results/autocts_precheck")
    ap.add_argument("--our-adj", default="results/data/pems04_adj.npy")
    args = ap.parse_args()

    sys.path.insert(0, args.autocts)
    commit = subprocess.check_output(["git", "-C", args.autocts, "rev-parse", "HEAD"], text=True).strip()
    import model_search as ms  # noqa: E402
    from genotypes import PRIMITIVES  # noqa: E402
    from operations import OPS  # noqa: E402
    from utils import generate_data, get_adj_matrix, masked_mae, masked_rmse  # noqa: E402

    random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed); torch.cuda.manual_seed_all(args.seed)
    device = torch.device("cuda")
    rec = {"autocts_commit": commit, "torch": torch.__version__, "gpu": torch.cuda.get_device_name(0),
           "date": _dt.datetime.now().isoformat(timespec="seconds"), "args": vars(args)}

    # ---- operator list and cell size (plan step 2)
    rec["primitives"] = list(PRIMITIVES)
    rec["ops_registry"] = sorted(OPS)
    n_edges_cell = sum(1 + i for i in range(args.steps))
    rec["cell"] = {"layers": args.layers, "steps(nodes)": args.steps, "edges_per_cell": n_edges_cell,
                   "kept_edges_per_node_in_genotype": 2, "hid_dim": args.hid_dim, "partial_channel_k": 4,
                   "note": "MixedOp operates on C/k = hid_dim/4 channels (PC-DARTS partial channels); DARTS-style DAG, "
                           "node i sums its incoming edges, cell output = last node; cells chained; skip-sum of all cell outputs -> 2 linear layers"}

    # ---- data + adjacency, their loaders (plan step 3)
    adj = get_adj_matrix(str(Path(args.data) / "PEMS04.csv"), 307)
    rec["adjacency"] = {"source": "PEMS04.csv via utils.get_adj_matrix(type_='connectivity')", "shape": list(adj.shape),
                        "n_undirected_edges": int(adj.sum() // 2), "symmetric": bool(np.array_equal(adj, adj.T)),
                        "diff_gcn_supports": "asym_adj(A), asym_adj(A^T) (row-normalised random walks) + adaptive softmax(relu(E1 E2))"}
    if Path(args.our_adj).exists():
        rec["adjacency"]["equals_pilot_pems04_adj"] = bool(np.array_equal(np.load(args.our_adj).astype(np.float32), adj))
    t0 = time.time()
    data = generate_data(str(Path(args.data) / "PEMS04.npz"), args.batch_size, args.batch_size)
    scaler = data["scaler"]
    rec["data"] = {"loader": "utils.generate_data", "split": "60/20/20 by time (generate_from_data)", "window": 12, "horizon": 12,
                   "features_used": "channel 0 (flow) only (generate_seq slices [..., 0:1])",
                   "normalisation": "StandardScaler(mean, std of train x[..., 0]) on inputs; loss on inverse-transformed prediction vs raw targets",
                   "loss": "masked_mae(pred, y, null_val=0.0)", "n_train": int(len(data["x_train"])), "n_val": int(len(data["x_val"])),
                   "n_test": int(len(data["x_test"])), "batches_per_epoch": int(data["train_loader"].num_batch),
                   "load_seconds": round(time.time() - t0, 1)}

    # ---- discrete network: their Network with one op per edge and their genotype's 2-edges-per-node rule
    class Args:  # what Network.__init__ reads
        pass
    a = Args()
    a.layers, a.steps, a.temp, a.randomadj, a.num_nodes, a.hid_dim, a.in_dim, a.seq_len = args.layers, args.steps, 5.0, True, 307, args.hid_dim, 1, 12
    rng = random.Random(args.seed)
    non_none = [k for k, p in enumerate(PRIMITIVES) if p != "none"]

    class DiscreteNetwork(ms.Network):
        def __init__(self):
            super().__init__(adj, scaler, a)
            for v in self._arch_parameters:
                v.requires_grad_(False)
            # library drift (torch 2.14): the repo builds skip connections as nn.Conv1d(C, 8C, (1, 1)) and applies them
            # to 4-D (B, C, N, T) tensors; conv1d now rejects that.  Conv2d with the same (1, 1) kernel has the identical
            # weight shape (8C, C, 1, 1) and the same arithmetic.
            self.skip_connect = nn.ModuleList([nn.Conv2d(a.hid_dim, a.hid_dim * 8, (1, 1)) for _ in range(a.layers)])
            self.genes = []
            for cell in self.cells:
                gene, k = [], 0
                for i in range(self._steps):
                    keep = {i} | ({rng.randrange(i)} if i > 0 else set())  # previous node + one random other (genotype(): max_edge + [i])
                    for j in range(i + 1):
                        op = cell._ops[k]
                        op.chosen = rng.choice(non_none) if j in keep else None
                        if op.chosen is not None:
                            gene.append((i, j, PRIMITIVES[op.chosen]))
                        k += 1
                self.genes.append(gene)

        def forward(self, input, count=-1):
            x = self.start_linear(input)
            b, D, N, T = x.shape
            x = x.permute(0, 2, 3, 1).reshape(-1, T, D)
            x = x * math.sqrt(self._args.hid_dim)
            x = x + self.pe(x)
            x = x.reshape(b, -1, T, D).permute(0, 3, 1, 2)
            skip = 0
            for ci, cell in enumerate(self.cells):        # inter-cell: previous cell only (one-hot gamma)
                states = [cell.preprocess(x)]
                k = 0
                for i in range(cell._steps):
                    s = None
                    for j, h in enumerate(states):
                        op = cell._ops[k]
                        if op.chosen is not None:
                            out = mixed_forward(op, h)
                            s = out if s is None else s + out
                        k += 1
                    states.append(s)
                x = states[-1]
                skip = self.skip_connect[ci](x) + skip
            state = torch.max(F.relu(skip), dim=-1, keepdim=True)[0]
            out = F.relu(self.end_linear_1(state))
            return self.end_linear_2(out)

    def mixed_forward(op, x):  # MixedOp.forward with a single chosen op (PC-DARTS partial channels + shuffle kept)
        dim_2 = x.shape[1]
        xtemp, xtemp2 = x[:, :dim_2 // op.k], x[:, dim_2 // op.k:]
        ans = torch.cat([op._ops[op.chosen](xtemp), xtemp2], dim=1)
        return ms.channel_shuffle(ans, op.k)

    model = DiscreteNetwork().to(device)
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    rec["network"] = {"genes": model.genes, "params": int(n_params),
                      "library_drift_patches": ["skip_connect Conv1d(C, 8C, (1,1)) on 4-D input -> Conv2d (torch 2.14 rejects the original)",
                                                "nn.utils.clip_grad_norm (removed) -> clip_grad_norm_"]}
    print("genes:", model.genes, "params", n_params)

    # ---- 1 epoch with their loop (train(), minus the architect step), optimiser and clipping
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
    model.train()
    losses, rmses = [], []
    torch.cuda.reset_peak_memory_stats(device)
    epoch_times = []
    for ep in range(args.epochs):
        t0 = time.time()
        for i, (x, y) in enumerate(data["train_loader"].get_iterator()):
            x = torch.Tensor(x).to(device).transpose(1, 3)
            y = torch.Tensor(y).to(device).transpose(1, 3)[:, 0, :, :]
            optimizer.zero_grad()
            logits = model(x, i).transpose(1, 3)
            y = torch.unsqueeze(y, dim=1)
            predict = scaler.inverse_transform(logits)
            loss = masked_mae(predict, y, 0.0)
            rmse = masked_rmse(predict, y, 0.0)
            losses.append(loss.item()); rmses.append(rmse.item())
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 5)
            optimizer.step()
            if i % 40 == 0:
                print(f"  ep {ep} it {i}: train_loss {losses[-1]:.3f} rmse {rmses[-1]:.3f}")
        epoch_times.append(time.time() - t0)
    peak_gb = torch.cuda.max_memory_allocated(device) / 1e9
    # validation with their infer()
    model.eval()
    vl = []
    with torch.no_grad():
        for x, y in data["val_loader"].get_iterator():
            x = torch.Tensor(x).to(device).transpose(1, 3)
            y = torch.Tensor(y).to(device).transpose(1, 3)[:, 0, :, :]
            logits = model(x, -1).transpose(1, 3)
            vl.append(masked_mae(scaler.inverse_transform(logits), torch.unsqueeze(y, 1), 0.0).item())
    rec["train_1_epoch"] = {"epochs": args.epochs, "seconds_per_epoch": round(float(np.mean(epoch_times)), 1),
                            "epoch_seconds": [round(t, 1) for t in epoch_times], "peak_mem_gb": round(peak_gb, 3),
                            "train_loss_first": losses[0], "train_loss_last": losses[-1], "train_loss_mean_last50": float(np.mean(losses[-50:])),
                            "val_loss": float(np.mean(vl)), "loss_units": "raw vehicle counts (masked MAE, null 0)",
                            "optimizer": "Adam lr 1e-3 wd 1e-4, grad clip 5, batch %d" % args.batch_size}
    print(json.dumps(rec["train_1_epoch"], indent=1))

    # ---- proxies on their first train batch (plan step 5)
    from pilot.proxies import extra

    class AutoCTSWrapper(nn.Module):
        """f(x: (B, 1, N, T)) -> (B, N, H) on the scaled input; loss = their masked MAE on the inverse-transformed prediction."""
        def __init__(self, net):
            super().__init__()
            self.net = net
            self.head = None

        def forward(self, x):
            return self.net(x, -1).transpose(1, 3)[:, 0]          # (B, N, H)

        def loss_fn(self, out, y):
            return masked_mae(scaler.inverse_transform(out), y[: out.shape[0]].to(out.device), 0.0)

    xb, yb = next(data["train_loader"].get_iterator())
    xb = torch.Tensor(xb).to(device).transpose(1, 3)                     # (B, 1, N, 12)
    yb = torch.Tensor(yb).to(device).transpose(1, 3)[:, 0, :, :]         # (B, N, 12)
    torch.manual_seed(args.seed)
    fresh = AutoCTSWrapper(DiscreteNetwork().to(device))
    fresh.train()
    px = {}
    v, m = extra.params(fresh); px["params"] = {"value": v, "meta": m}
    v, m = extra.nwot(fresh, xb); px["nwot"] = {"value": v, "meta": m}
    grp = extra.grad_group_all(fresh, xb, yb, fresh.loss_fn)
    v, m = grp["grad_norm_all"]; px["grad_norm_all"] = {"value": v, "meta": m}
    rec["proxies"] = px
    rec["probe_batch"] = {"x_shape": list(xb.shape), "y_shape": list(yb.shape), "source": "first batch of their unshuffled train_loader"}
    print("proxies:", {k: v["value"] for k, v in px.items()}, "n_hooks", px["nwot"]["meta"]["n_hooks"])

    # ---- gate
    spe = rec["train_1_epoch"]["seconds_per_epoch"]
    gpu_h = spe * 20 * 50 / 3600
    rec["gate"] = {"finite_loss": bool(math.isfinite(rec["train_1_epoch"]["train_loss_last"]) and math.isfinite(rec["train_1_epoch"]["val_loss"])),
                   "gpu_hours_20ep_x50": round(gpu_h, 2), "fits_30_gpu_h": bool(gpu_h <= 30),
                   "proxies_finite": all(math.isfinite(p["value"]) for p in px.values()), "n_hooks": px["nwot"]["meta"]["n_hooks"]}
    rec["gate"]["pass"] = bool(rec["gate"]["finite_loss"] and rec["gate"]["fits_30_gpu_h"] and rec["gate"]["proxies_finite"] and rec["gate"]["n_hooks"] > 0)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".json").write_text(json.dumps(rec, indent=2, default=str))
    md = [f"# AutoCTS pre-check ({rec['date'][:10]})", "",
          f"AutoCTS commit `{commit[:8]}` run from `{args.autocts}` inside the pilot venv (torch {torch.__version__}); no separate venv was needed.", "",
          "## Operator list and cell", "",
          f"- `PRIMITIVES` = {rec['primitives']} (the repo also ships, commented out: cheb_gcn, cnn, att1, att2, lstm, gru, dcc_1)",
          f"- cell: {args.steps} nodes, {n_edges_cell} candidate edges, {args.layers} cells chained; genotype keeps 2 incoming edges per node; hid_dim {args.hid_dim}, PC-DARTS partial channels k=4",
          f"- sampled discrete genes (cell: [(node, from, op)]): {model.genes}", f"- params: {n_params:,}",
          f"- library-drift patches needed to run on torch {torch.__version__}: {rec['network']['library_drift_patches']}", "",
          "## Data and adjacency (their pipeline)", "",
          f"- {rec['data']['loader']}: {rec['data']['split']}, window {rec['data']['window']}, horizon {rec['data']['horizon']}, {rec['data']['features_used']}",
          f"- {rec['data']['normalisation']}; loss {rec['data']['loss']}",
          f"- train/val/test windows: {rec['data']['n_train']} / {rec['data']['n_val']} / {rec['data']['n_test']}; {rec['data']['batches_per_epoch']} batches of {args.batch_size} per epoch",
          f"- adjacency: {rec['adjacency']['source']}, {rec['adjacency']['n_undirected_edges']} undirected edges, equals the pilot's `pems04_adj.npy`: {rec['adjacency'].get('equals_pilot_pems04_adj')}",
          f"- diff_gcn supports: {rec['adjacency']['diff_gcn_supports']}", "",
          "## 1-epoch training (their loss, optimiser and clipping)", "",
          f"- seconds per epoch: {spe} (peak GPU memory {rec['train_1_epoch']['peak_mem_gb']} GB)",
          f"- train masked-MAE: first batch {rec['train_1_epoch']['train_loss_first']:.2f}, last batch {rec['train_1_epoch']['train_loss_last']:.2f}, mean of last 50 {rec['train_1_epoch']['train_loss_mean_last50']:.2f} (raw vehicle counts)",
          f"- val masked-MAE after 1 epoch: {rec['train_1_epoch']['val_loss']:.2f}", "",
          "## Proxies on their first train batch", "",
          f"- params {px['params']['value']:.0f}, grad_norm_all {px['grad_norm_all']['value']:.4g} ({px['grad_norm_all']['meta']['n_with_grad']}/{px['grad_norm_all']['meta']['n_param_tensors']} tensors with grad), nwot {px['nwot']['value']:.2f} (n_hooks {px['nwot']['meta']['n_hooks']}, fired {px['nwot']['meta']['n_fired']})", "",
          "## Fallback gate", "",
          f"- finite loss: {rec['gate']['finite_loss']}; {spe} s/epoch x 20 epochs x 50 archs = {gpu_h:.1f} GPU-h (<= 30: {rec['gate']['fits_30_gpu_h']}); proxies finite: {rec['gate']['proxies_finite']}; n_hooks {rec['gate']['n_hooks']}",
          f"- **GATE {'PASS' if rec['gate']['pass'] else 'FAIL'}**", ""]
    out.with_suffix(".md").write_text("\n".join(md))
    print("GATE", "PASS" if rec["gate"]["pass"] else "FAIL", "->", out.with_suffix(".md"))


if __name__ == "__main__":
    main()
