"""Fits the released OpenCity model at a city, in the released form or in one changed form of the adaptation.

The released classes and functions are imported unchanged: the model (model/OpenCity/OpenCity.py), the window dataset, the split
and the time features (lib/data_process.py), the Laplacian code (lib/predifineGraph.py) and the metrics (lib/metrics.py).  This
file repeats the statements of model/Run.py (mode eval), model/OpenCity/args.py and model/BasicTrainer.py, which cannot be
imported without their relative paths and their configuration file, and adds what they do not have: a city and a size as
arguments, a seed per run, a share of the training split, a span of the series in days, a form of the adaptation, timers, the
metrics on the validation and the test part as numbers, one json per run and a skip of finished runs.
Survey/experiments/opencity-plan.md.

  python -m pilot.opencity_run --up $NAS_ROOT/OpenCity --city sz_didi --sizes mini --forms H0 --seeds 12 --out results/opencity/sz_didi_in1day_out1day/fit

Forms:
  H0  the released fit: only the last linear layer (the head) trains, 3 epochs
  H1  H0 with early stop within 100 epochs (patience 15), the default of the released code
  H2  H0 with dropout off in the frozen part (the model stays in eval mode in the fit)
  H3  H1 with a new head from a random start
  H4  H1, and every norm layer trains too
  H5  H1, and the last block trains too
  H6  every weight trains (full fine-tuning), early stop within 100 epochs
  H7  H6 with a learning rate of 0.0001
  H8  no fit (zero-shot)
--init random leaves the released weights out (the same architecture from a random start; use it with H6).
--share is the share of the training split, taken from its start.  --days cuts the series to its first days before the split.

Differences from the released code: the checkpoint loads on the CPU; the unused file of hop distances is not written; the
test pass leaves the correlation out; the model is the class OpenCity without the wrapper Traffic_model (the wrapper only
passes its arguments on); the degree matrix of the graph is inverted as a vector.
"""
import argparse, configparser, contextlib, copy, io, json, os, random, sys, time
from pathlib import Path

import numpy as np

# city -> (name of the released files, minutes per step, weekday of the first step, holiday list of the released loader)
CITIES = {"cd_didi": ("CD_DIDI", 10, 1, [4]), "sz_didi": ("SZ_DIDI", 10, 1, [4]),
          "sd": ("sd", 5, 5, None), "ca_d6": ("ca_d6", 5, 5, None), "ca_d10": ("ca_d10", 5, 5, None)}   # LargeST: pilot.opencity_data
SIZES = {"mini": (128, 3, "OpenCity-mini.pth"), "base": (256, 3, "OpenCity-base.pth"), "plus": (512, 6, "OpenCity-plus.pth")}
FORMS = ("H0", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8")
MASK = 0.001                                         # mape_thresh of conf/general_conf/pretrain.conf: the loss leaves targets <= MASK out


def load_upstream(up):
    up = Path(up).resolve()
    sys.path.insert(0, str(up / "model")); sys.path.insert(0, str(up))
    from OpenCity.OpenCity import OpenCity
    from lib import data_process, metrics
    from lib.predifineGraph import cal_lape
    return argparse.Namespace(OpenCity=OpenCity, dp=data_process, metrics=metrics, cal_lape=cal_lape), up


def model_args(up, size, name, adj):
    """The arguments of the class OpenCity, as model/OpenCity/args.py builds them."""
    import torch
    c = configparser.ConfigParser(); c.read(up / "conf" / "OpenCity" / "OpenCity.conf")
    m = c["model"]
    width, depth, _ = SIZES[size]
    a = argparse.Namespace(
        input_window=int(c["data"]["input_window"]), output_window=int(c["data"]["output_window"]), embed_dim=width, skip_dim=width,
        lape_dim=int(m["lape_dim"]), geo_num_heads=int(m["geo_num_heads"]), sem_num_heads=int(m["sem_num_heads"]),
        tc_num_heads=int(m["tc_num_heads"]), t_num_heads=int(m["t_num_heads"]), mlp_ratio=int(m["mlp_ratio"]),
        qkv_bias=m["qkv_bias"] == "True", drop=float(m["drop"]), attn_drop=float(m["attn_drop"]), drop_path=float(m["drop_path"]),
        s_attn_size=int(m["s_attn_size"]), t_attn_size=int(m["t_attn_size"]), enc_depth=depth, type_ln=m["type_ln"],
        far_mask_delta=int(m["far_mask_delta"]))
    sh = adj.copy(); sh[sh > 0] = 1; sh[sh == 0] = 511
    with contextlib.redirect_stdout(io.StringIO()):
        lap = UP.cal_lape(copy.deepcopy(adj))
    d = adj.sum(axis=1) ** -0.5
    a.adj_mx_dict = {name: torch.FloatTensor(np.identity(adj.shape[0]) + d[:, None] * adj * d[None, :])}
    a.sh_mx_dict = {name: torch.FloatTensor(sh)}
    a.lap_mx_dict = {name: torch.FloatTensor(lap)}
    return a


def load_city(city, days):
    """The array (steps, sensors, 3) of the released loader: the value, the minute of the day, the day of the week."""
    name, interval, week_start, holidays = CITIES[city]
    root = Path(os.environ["NAS_DATA_ROOT"]) / "opencity" / name
    data = np.load(root / f"{name}.npz")["data"][:, :, 0]
    if days:
        data = data[: days * 1440 // interval]
    day, week, _ = UP.dp.time_add(data, week_start, interval=interval, weekday_only=False, holiday_list=holidays)
    data = np.concatenate([data[..., None], day[..., None].astype(int), week[..., None].astype(int)], axis=-1)
    return name, interval, data, np.load(root / f"{name}_rn_adj.npy")


def set_trained(model, form):
    head = lambda n: n.startswith("linear.")
    rule = {"H4": lambda n: head(n) or "norm" in n, "H5": lambda n: head(n) or n.startswith(f"encoder_blocks.{len(model.encoder_blocks) - 1}."),
            "H6": lambda n: True, "H7": lambda n: True}.get(form, head)
    for n, p in model.named_parameters():
        p.requires_grad = bool(rule(n))


def evaluate(model, loader, name, device):
    import torch
    M = UP.metrics
    model.eval()
    mae = mse = mape = count = mape_count = 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.squeeze(0).to(device), y.squeeze(0).to(device)
            out, lbl = model(x, y, name), y[..., :1]
            a, n = M.MAE_torch(out, lbl, 0.0); s, _ = M.MSE_torch(out, lbl, 0.0); p, pn = M.MAPE_torch(out, lbl, MASK)
            mae += a.item() * n; mse += s.item() * n; mape += p.item() * pn; count += n; mape_count += pn
    return {"mae": mae / count, "rmse": (mse / count) ** 0.5, "mape": mape / mape_count, "targets": count}


def run_one(up, city, size, form, init, share, days, seed, max_epochs, batch_size, out_file, check=False):
    import torch
    from torch.utils.data import DataLoader
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    sync = (lambda: torch.cuda.synchronize()) if device.type == "cuda" else (lambda: None)
    np.random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed(seed); random.seed(seed)   # lib/TrainInits.init_seed
    t0 = time.time()
    name, interval, data, adj = load_city(city, days)
    train, val, test = UP.dp.split_data_by_ratio(data, 0.1, 0.4)
    if share < 1:
        train = train[: int(len(train) * share)]
    a = model_args(up, size, name, adj)
    iw, ow = a.input_window // (interval // 5), a.output_window // (interval // 5)
    sets = [UP.dp.TrafficDataset(train, batch_size, input_window=iw, output_window=ow, eval_only=False),
            UP.dp.TrafficDataset(val, batch_size, input_window=iw, output_window=ow, eval_only=True),
            UP.dp.TrafficDataset(test, batch_size, input_window=iw, output_window=ow, eval_only=True)]
    if form != "H8" and len(sets[0]) == 0:
        raise SystemExit(f"no training batch: {len(train)} steps for windows of {iw} + {ow} and a batch of {batch_size}")
    train_loader, val_loader, test_loader = (DataLoader(s, batch_size=1, shuffle=i == 0) for i, s in enumerate(sets))
    model = UP.OpenCity(a, [name], device, 1)
    if init == "pretrained":
        state = torch.load(up / "model_weights" / "OpenCity" / SIZES[size][2], map_location="cpu")
        model.load_state_dict({k.replace("module.", "").replace("predictor.", "", 1): v for k, v in state.items()})
    if form == "H3":
        model.linear.reset_parameters()
    model = model.to(device)
    set_trained(model, form)
    n_all = sum(p.numel() for p in model.parameters()); n_train = sum(p.numel() for p in model.parameters() if p.requires_grad)
    epochs = max_epochs if max_epochs is not None else (3 if form in ("H0", "H2") else 100)
    if check:                                    # one batch forward and one update; nothing is written
        x, y = (t.squeeze(0).to(device) for t in next(iter(train_loader)))
        opt = torch.optim.Adam(params=model.parameters(), lr=0.001)
        loss, _ = UP.metrics.MAE_torch(pred=model(x, y, name), true=y[..., :1], mask_value=MASK)
        loss.backward(); opt.step()
        trained = sorted({n.split('.')[0] for n, p in model.named_parameters() if p.requires_grad})
        print(f"check {city} {size} {form} {init}: data {data.shape} steps {len(train)}/{len(val)}/{len(test)} windows {iw}+{ow} "
              f"batches {[len(s) for s in sets]} batch {tuple(x.shape)} loss {loss.item():.4f} weights {n_all} trained {n_train} {trained}")
        return
    rec = {"city": city, "dataset": name, "size": size, "form": form, "init": init, "share": share, "days": days or len(data) * interval // 1440,
           "seed": seed, "nodes": data.shape[1], "steps": [len(train), len(val), len(test)], "in_steps": iw, "out_steps": ow,
           "batch_size": batch_size, "train_batches": len(sets[0]), "weights": n_all, "trained_weights": 0 if form == "H8" else n_train,
           "max_epochs": epochs, "device": str(device), "gpu": torch.cuda.get_device_name(0) if device.type == "cuda" else None,
           "data_seconds": time.time() - t0}
    if form != "H8":
        optimizer = torch.optim.Adam(params=model.parameters(), lr=0.0001 if form == "H7" else 0.001, eps=1.0e-8, weight_decay=0, amsgrad=False)
        best, bad, best_state, curve, t_train, t_val = float("inf"), 0, None, [], 0.0, 0.0
        for epoch in range(epochs):                  # BasicTrainer.multi_train
            sync(); t1 = time.time()
            model.eval() if form == "H2" else model.train()
            total = 0.0
            for x, y in train_loader:
                x, y = x.squeeze(0).to(device), y.squeeze(0).to(device)
                out = model(x, y, name)
                optimizer.zero_grad()
                loss, _ = UP.metrics.MAE_torch(pred=out, true=y[..., :1], mask_value=MASK)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 5)
                optimizer.step()
                total += loss.item()
            sync(); t2 = time.time(); t_train += t2 - t1
            if total / len(train_loader) > 1e6:
                print("gradient explosion; the fit stops"); break
            model.eval(); v = 0.0
            with torch.no_grad():
                for x, y in val_loader:
                    x, y = x.squeeze(0).to(device), y.squeeze(0).to(device)
                    l, _ = UP.metrics.MAE_torch(pred=model(x, y, name), true=y[..., :1], mask_value=MASK)
                    if not torch.isnan(l):
                        v += l.item()
            v /= len(val_loader); curve.append(v)
            sync(); t_val += time.time() - t2
            print(f"epoch {epoch + 1} train_loss {total / len(train_loader):.6f} val_loss {v:.6f} elapsed {t_train + t_val:.0f} s", flush=True)
            if v < best:
                best, bad, best_state = v, 0, copy.deepcopy(model.state_dict())
            else:
                bad += 1
                if bad == 15:
                    break
        if best_state is not None:
            model.load_state_dict(best_state)
        rec.update(train_seconds=t_train, val_seconds=t_val, fit_seconds=t_train + t_val, epochs_run=len(curve),
                   best_epoch=int(np.argmin(curve)) + 1 if curve else 0, val_loss_curve=curve)
    sync(); t3 = time.time()
    rec["val"] = evaluate(model, val_loader, name, device)
    sync(); t4 = time.time()
    rec["test"] = evaluate(model, test_loader, name, device)
    sync(); rec["val_eval_seconds"], rec["test_seconds"] = t4 - t3, time.time() - t4
    if device.type == "cuda":
        rec["peak_gpu_gb"] = torch.cuda.max_memory_allocated() / 2 ** 30
    tmp = out_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(rec, indent=1)); tmp.replace(out_file)
    print(f"done {out_file.name}: epochs {rec.get('epochs_run', 0)} best {rec.get('best_epoch', 0)} fit {rec.get('fit_seconds', 0):.0f} s "
          f"test pass {rec['test_seconds']:.0f} s val MAE {rec['val']['mae']:.4f} test MAE {rec['test']['mae']:.4f} "
          f"RMSE {rec['test']['rmse']:.4f} trained weights {rec['trained_weights']} of {n_all}", flush=True)


def main(argv=None):
    global UP
    ap = argparse.ArgumentParser()
    ap.add_argument("--up", required=True, help="the upstream tree (pilot/opencity_setup.sh)")
    ap.add_argument("--city", required=True, choices=sorted(CITIES))
    ap.add_argument("--sizes", nargs="+", default=["mini"], choices=sorted(SIZES))
    ap.add_argument("--forms", nargs="+", default=["H0"], choices=FORMS)
    ap.add_argument("--seeds", nargs="+", type=int, default=[12])
    ap.add_argument("--share", type=float, default=1.0)
    ap.add_argument("--days", type=int, default=0, help="the first days of the series (0: all of it)")
    ap.add_argument("--init", default="pretrained", choices=("pretrained", "random"))
    ap.add_argument("--max-epochs", type=int, default=None)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--check", action="store_true", help="one batch forward and one update per run on this device; writes nothing")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    UP, up = load_upstream(args.up)
    failed = 0
    for seed in args.seeds:
        for size in args.sizes:
            for form in args.forms:
                tag = f"{size}_{form}_{args.init}_share{args.share:g}_days{args.days or 'all'}_seed{seed}"
                # A fit that does not fit in the GPU memory runs again with half the batch; its file name says so.
                files = [out / (tag + (f"_batch{b}" if b != 64 else "") + ".json") for b in (args.batch_size, args.batch_size // 2)]
                done = [f for f in files if f.exists()]
                if done and not args.check:
                    print(f"skip {done[0].name}"); continue
                for batch, f in zip((args.batch_size, args.batch_size // 2), files):
                    try:
                        run_one(up, args.city, size, form, args.init, args.share, args.days, seed, args.max_epochs, batch, f, args.check)
                        break
                    except RuntimeError as e:
                        if "out of memory" not in str(e).lower():
                            raise
                    import gc, torch
                    gc.collect(); torch.cuda.empty_cache()
                    print(f"out of GPU memory: {f.name}", flush=True)
                else:
                    failed = 1
    return failed


UP = None
if __name__ == "__main__":
    raise SystemExit(main())
