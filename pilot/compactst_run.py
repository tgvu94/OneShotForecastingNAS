"""Fits the released CompactST model at a city, in the released form or in one changed form of the adaptation.

The released classes are imported unchanged: the model (model.py), the wrapper AdaptiveTune of few_shot.py, the loader
(lib/load_data.py), the trainer (lib/trainer.py) and the metrics (lib/metrics.py).  This file repeats the statements of the
main block of few_shot.py, which cannot be imported, and adds what that block does not have: the path of the released
checkpoint, a seed per run, the share of the training split as a number, a form of the adaptation, the metrics on the
validation and the test part as numbers, one json per run and a skip of finished runs.
Survey/experiments/compactst-plan.md.

  python -m pilot.compactst_run --up $NAS_ROOT/CompactST --city shenzhen --forms C0 --seeds 999 --out results/compactst/shenzhen_in96_out48/fit

Forms (each one change against C0, but C5, which is one change against C6):
  C0  the released form: every weight trains, a prompt on the last layer, the mixing block starts at zero (inactive)
  C1  the mixing block starts with Xavier values (active)
  C2  C1 with the pre-trained weights frozen: only the prompt and the mixing block train
  C3  C2, and the normaliser router with its experts and the prediction heads train too
  C4  no prompt and no mixing block: plain full fine-tuning
  C5  a prompt on every layer, each starts at one
  C6  the prompt of the last layer starts at one
  C7  MAE loss in place of Huber
  C8  no fit: the pre-trained model with no prompt and no mixing block
--init random leaves the released weights out (the same architecture from a random start).
--share is the share of the training split (0.05 in the paper); the loader takes the first share * 0.7 of all windows.

Differences from the released main block: the test loader is built once and serves as the loader of the unseen dataset (the
block builds it twice from the same file); the test pass before the fit and the torchinfo summary are left out; the
scheduler gets no `verbose` argument; the checkpoint loads on the CPU.
"""
import argparse, contextlib, io, json, os, sys, time, types
from pathlib import Path

import numpy as np

from pilot.compactst_data import CITIES

FORMS = ("C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8")


def load_upstream(up):
    up = Path(up).resolve()
    os.chdir(up)
    sys.path.insert(0, str(up))
    try:
        import torchinfo  # noqa: F401  (few_shot.py imports it for a summary that this file does not print)
    except ImportError:
        sys.modules["torchinfo"] = types.SimpleNamespace(summary=lambda *a, **k: None)
    import few_shot as fs
    return fs, up


def make_args(fs, up, city, share, max_epochs, device):
    import yaml
    with open(up / "model_config" / "compactst.yaml") as f:
        config = yaml.safe_load(f)["stmixer_heter"]
    name, steps_per_day = CITIES[city]
    a = argparse.Namespace(
        dataset_path=str(Path(os.environ["NAS_DATA_ROOT"]) / "compactst") + "/", dataset=name, unseen=name,
        in_steps=config["in_steps"], out_steps=config["out_steps"], batch_size=config["batch_size"],
        max_epochs=max_epochs if max_epochs is not None else config["max_epochs"], lr=config["lr"], clip_grad=config["clip_grad"],
        weight_decay=config.get("weight_decay", 0), milestones=config["milestones"], lr_decay_rate=config.get("lr_decay_rate", 0.1),
        eps=config.get("eps", 1e-8), early_stop=config.get("early_stop", 10), log_step=config["log_step"],
        use_revin=config["use_revin"], train_ratio=0.7 * share, mode=config.get("mode", "train"), save_path=None, device=device)
    for k in ("patch_length", "patch_stride", "downsample_factor", "in_dim", "out_dim", "num_patches", "hidden_dim", "num_experts",
              "num_layers", "expansion_factor", "dropout", "add_position", "gated_attn"):
        setattr(a, k, config["model_args"][k])
    with open(Path(a.dataset_path) / "adj_mx" / f"{name}.json") as f:
        shape = json.load(f)["shape"]
    a.time_dict, a.node_dict = {name: steps_per_day}, {name: shape[1]}
    a.dataset_list, a.unseen_list, a.add_time_features = [name], [name], False
    a.num_nodes, a.num_times = shape[1], steps_per_day
    return a


def build(fs, args, form, init, up):
    """The model of one run.  Returns (wrapper, list of the names of the frozen weights)."""
    import torch
    import torch.nn as nn
    args.use_prompt, args.use_spatial = form not in ("C4", "C8"), form not in ("C4", "C8")
    model = fs.CompactST(args)
    if init == "pretrained":
        model.load_state_dict(torch.load(up / "checkpoint" / "stmixer.pt", map_location="cpu"))
    if form == "C5":
        class EveryLayer(fs.AdaptiveTune):
            """The released forward with one prompt for each layer output (the release: the last layer only)."""
            def __init__(self, pre_trained_model, a):
                super().__init__(pre_trained_model, a)
                self.layer_prompts = nn.ParameterList(
                    [nn.Parameter(torch.ones(1, self.num_nodes, 1, self.hidden_dim)) for _ in range(a.num_layers - 1)])

            def forward(self, x, adj):
                x_in = x[..., [0]]
                _, out_all, stat = self.pre_trained_model(x_in, adj)
                gamma_buff, beta_buff, mean_spatial, std_spatial, mean_domain, std_domain = stat
                assert len(out_all) == len(self.layer_prompts) + 1, len(out_all)
                for i, p in enumerate(self.layer_prompts):
                    out_all[i] = p * out_all[i]
                out_all[-1] = self.spatial_mixer(self.spatial_prompt1 * out_all[-1])
                out = self.pre_trained_model.predictor(out_all)
                if self.use_revin:
                    out = self.pre_trained_model.denorm(out, gamma_buff, beta_buff, mean_spatial, std_spatial, mean_domain, std_domain)
                return out, out_all, stat
        wrapper = EveryLayer(model, args)
    else:
        wrapper = fs.AdaptiveTune(model, args)
    if form in ("C5", "C6"):
        nn.init.ones_(wrapper.spatial_prompt1)
    if form in ("C1", "C2", "C3"):
        mix = wrapper.spatial_mixer.spatial_mixing1
        nn.init.xavier_uniform_(mix.e1); nn.init.xavier_uniform_(mix.e2)
    frozen = []
    if form in ("C2", "C3"):
        keep = ("nested_norm.", "predictor.") if form == "C3" else ()
        for n, p in wrapper.pre_trained_model.named_parameters():
            if not n.startswith(keep):
                p.requires_grad_(False); frozen.append(n)
    return wrapper, frozen


def evaluate(fs, wrapper, loaders, adj_dict, args):
    """RMSE, MAE and MAPE with the released metric functions (the statements of trainer.test_model, with a return)."""
    import torch
    wrapper.eval()
    name, loader = loaders[0]
    ys, outs = [], []
    with torch.no_grad():
        adj = adj_dict[name].to(args.device)
        for x_batch, y_batch in loader:
            out_batch, _, _ = wrapper(x_batch.to(args.device), adj)
            outs.append(out_batch.cpu().numpy()); ys.append(y_batch.numpy())
    y, out = np.vstack(ys).squeeze(), np.vstack(outs).squeeze()
    rmse, mae, mape = fs.cal_metrics(y, out, name)
    return {"mae": float(mae), "rmse": float(rmse), "mape": float(mape), "windows": int(len(y))}


def run_one(fs, up, city, form, init, share, seed, max_epochs, out_file):
    import torch
    import torch.nn as nn
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    fs.set_seed(seed)
    args = make_args(fs, up, city, share, max_epochs, device)
    fs.args = args                                   # AdaptiveTune.forward reads the global `args` of its module
    t0 = time.time()
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        trainset_loader, valset_loader, testset_loader, scaler_dict, adj_dict = fs.load_data(args.dataset_list, args)
    print(buf.getvalue().strip().splitlines()[-1])
    t_data = time.time() - t0
    wrapper, frozen = build(fs, args, form, init, up)
    wrapper = wrapper.to(device)
    n_train = sum(p.numel() for p in wrapper.parameters() if p.requires_grad)
    n_all = sum(p.numel() for p in wrapper.parameters())
    rec = {"city": city, "dataset": args.dataset, "form": form, "init": init, "share": share, "seed": seed, "nodes": args.num_nodes,
           "train_batches": len(trainset_loader), "weights": n_all, "trained_weights": n_train, "frozen_tensors": len(frozen),
           "device": str(device), "gpu": torch.cuda.get_device_name(0) if device.type == "cuda" else None, "data_seconds": t_data}
    if form != "C8":
        loss = [fs.MaskedMAELoss(), nn.L1Loss() if form == "C7" else nn.HuberLoss()]
        optimizer = torch.optim.Adam([p for p in wrapper.parameters() if p.requires_grad], lr=args.lr,
                                     weight_decay=args.weight_decay, eps=args.eps)
        scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=args.milestones, gamma=args.lr_decay_rate)
        tr = fs.trainer(args, wrapper, trainset_loader, valset_loader, testset_loader, testset_loader, scaler_dict, scaler_dict,
                        adj_dict, adj_dict, loss, optimizer, scheduler)
        val_curve, stamps = [], []
        released_eval = tr.eval_model

        def eval_model(epoch):
            v = released_eval(epoch)
            val_curve.append(float(v)); stamps.append(time.time())
            print(f"epoch {epoch + 1} val_loss {v:.6f} elapsed {time.time() - t1:.0f} s", flush=True)
            return v
        tr.eval_model = eval_model
        tr.test_model = lambda: None                 # the released call prints the test error; evaluate() returns it below
        t1 = time.time()
        tr.train_multi_epoch()                       # the released loop; the wrapper holds the best state at its end
        if device.type == "cuda":
            torch.cuda.synchronize()
        rec.update(fit_seconds=time.time() - t1, epochs_run=len(val_curve), best_epoch=int(np.argmin(val_curve)) + 1,
                   val_loss_curve=val_curve)
    t2 = time.time()
    rec["val"] = evaluate(fs, wrapper, valset_loader, adj_dict, args)
    rec["test"] = evaluate(fs, wrapper, testset_loader, adj_dict, args)
    rec["eval_seconds"] = time.time() - t2
    if device.type == "cuda":
        rec["peak_gpu_gb"] = torch.cuda.max_memory_allocated() / 2 ** 30
    tmp = out_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(rec, indent=1)); tmp.replace(out_file)
    print(f"done {out_file.name}: epochs {rec.get('epochs_run', 0)} best {rec.get('best_epoch', 0)} fit {rec.get('fit_seconds', 0):.0f} s "
          f"val MAE {rec['val']['mae']:.4f} test MAE {rec['test']['mae']:.4f} RMSE {rec['test']['rmse']:.4f} trained weights {n_train}", flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--up", required=True, help="the upstream tree (pilot/compactst_setup.sh)")
    ap.add_argument("--city", required=True, choices=sorted(CITIES))
    ap.add_argument("--forms", nargs="+", default=["C0"], choices=FORMS)
    ap.add_argument("--seeds", nargs="+", type=int, default=[999])
    ap.add_argument("--share", type=float, default=0.05)
    ap.add_argument("--init", default="pretrained", choices=("pretrained", "random"))
    ap.add_argument("--max-epochs", type=int, default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    fs, up = load_upstream(args.up)
    for form in args.forms:
        for seed in args.seeds:
            f = out / f"{form}_{args.init}_share{args.share:g}_seed{seed}.json"
            if f.exists():
                print(f"skip {f.name}"); continue
            run_one(fs, up, args.city, form, args.init, args.share, seed, args.max_epochs, f)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
