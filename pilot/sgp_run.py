"""SGP [cini2023sgp] with a runner of our own, and closed-form readouts on its embedding (Survey/experiments/sgp-plan.md).

    python -m pilot.sgp_run check --city metrla                      the checks without a GPU
    python -m pilot.sgp_run fit --city metrla --setting release --seed 0 --forms R0
    python -m pilot.sgp_run fit --city metrla --setting release --seed 0 --split strict --forms R0 R1 R2 R3 R4 R5 R6
    python -m pilot.sgp_run fit --city metrla --setting gesn --seed 0 --forms R7
    python -m pilot.sgp_run headroom                                 SGP against STID on the common test windows (no GPU)

Settings (the files of the release under config/traffic): release = sgp_la.yaml / sgp_bay.yaml; paper = the reservoir of the
paper at METR-LA (3 layers of 32 units); nospace = sgp_*_abl1.yaml (no spatial blocks, no graph-wide mean); gesn = gesn_*.yaml.
Forms: R0 the released readout; R1 without the node embedding; R2 one linear layer (gradient, masked MAE); R3 ridge, one model
for all sensors; R4 ridge, one model per sensor; R5 = R4 without the spatial blocks; R6 = R3, then a ridge model per sensor on
its residual; R7 the closed-form baseline of the release (one ridge model, weight 0.001, no mask in the fit).
Split: `release` is the split of the released code, where the training samples include the validation samples.  `strict` takes
the validation samples out of the training samples.  A ridge weight is always selected on a fit that did not see the validation
samples; with `release` the model is then fitted again on all training samples.
What differs from the release: the reservoir states stay on the device and the spatial blocks are computed for each batch (the
release stores the full embedding in system memory); our loop replaces Lightning; the graph comes from the DCRNN pickle of the
project without its diagonal.  `check` measures the last point.

Output: <root>/train/<setting>_<split>/<form>_s<seed>/ with metrics.json, sensors.npz (errors by sensor) and forecast_test.npy
(float32 [test samples, 12, sensors], raw unit; metrics.json gives the position of the first target row).  root =
results/sgp/<city>_h12.  A run with metrics.json is skipped.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import pickle
import resource
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch

from pilot import datasets
from pilot.sgp_model import (GraphReservoir, LinearReadout, Reservoir, SGPReadout, expand, gesn_support, powers, supports)

REPO = Path(__file__).resolve().parents[1]
UP = Path(os.environ.get('NAS_ROOT', REPO.parent)) / 'sgp'
HORIZON, STEP_NS, DAY_NS = 12, 300 * 10 ** 9, 86400 * 10 ** 9
# First validation stamp, last validation stamp, first test stamp (year, month, day, hour, minute): the constants of the
# release, experiments/run_traffic_sgp.py:52-60.
SPLIT_TS = {'metrla': ((2012, 5, 25, 16, 0), (2012, 6, 4, 3, 20), (2012, 6, 4, 4, 20)),
            'pemsbay': ((2017, 5, 11, 7, 20), (2017, 5, 25, 17, 40), (2017, 5, 25, 18, 40))}
_LA = dict(leak=0.9, k=4, glob=True, lr=0.004, milestones=(40, 80, 120))
_BAY = dict(size=128, layers=1, leak=0.8, k=4, glob=True, lr=0.0035, milestones=(100, 150))
SETTINGS = {('metrla', 'release'): dict(_LA, size=64, layers=2), ('metrla', 'paper'): dict(_LA, size=32, layers=3),
            ('metrla', 'nospace'): dict(_LA, size=64, layers=2, k=0, glob=False),
            ('pemsbay', 'release'): dict(_BAY), ('pemsbay', 'nospace'): dict(_BAY, k=0, glob=False),
            ('metrla', 'gesn'): dict(size=320, layers=3, leak=0.9), ('pemsbay', 'gesn'): dict(size=128, layers=4, leak=0.9)}
TRAIN = dict(epochs=200, batches=300, batch=64, patience=100, clip=5.0)                 # sgp_la.yaml / sgp_bay.yaml
ALPHAS = (1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0, 1e3, 1e4)                                  # ridge weights, fixed before any run
PUBLISHED = {'metrla': {'release': 3.00, 'paper': 3.00, 'nospace': 3.22, 'gesn': 3.98},  # Table 1 of the paper, mean of 12 steps
             'pemsbay': {'release': 1.54, 'nospace': 1.62, 'gesn': 2.09}}
GRADIENT, PER_SENSOR = ('R0', 'R1', 'R2'), ('R4', 'R5', 'R6')


# ------------------------------------------------------------------------------------------------------------- the city
def load_city(ds: str) -> dict:
    """The series as the bundled library of the release builds it (tsl/datasets/metr_la.py, pems_bay.py): the rows on the
    full 5-minute index, the mask, and the absent values filled with the last value."""
    import h5py
    with h5py.File(datasets._resolve(datasets.info(ds)['stamps']), 'r') as f:
        g = f[list(f.keys())[0]]
        t, ids, v = g['axis1'][:].astype(np.int64), [str(i.decode() if isinstance(i, bytes) else i) for i in g['axis0'][:]], \
            g['block0_values'][:].astype(np.float32)
    if t[-1] < 10 ** 17:                                               # microseconds in the METR-LA file
        t = t * 1000
    pos = (t - t[0]) // STEP_NS
    assert np.all((t - t[0]) % STEP_NS == 0) and np.all(np.diff(pos) > 0)
    full = np.full((int(pos[-1]) + 1, v.shape[1]), np.nan, np.float32)
    full[pos] = v
    present = ~np.isnan(full)
    mask = present & (full != 0)
    keep = present if ds == 'pemsbay' else mask                        # METR-LA: zeros are filled; PEMS-BAY: absent rows only
    idx = np.maximum.accumulate(np.where(keep, np.arange(len(full))[:, None], 0), axis=0)
    filled = np.nan_to_num(np.take_along_axis(full, idx, axis=0), nan=0.0)
    stamps = t[0] + np.arange(len(full), dtype=np.int64) * STEP_NS
    with open(datasets.adj_pickle_path(ds), 'rb') as f:
        pk_ids, _, adj = pickle.load(f, encoding='latin1')
    assert [str(i) for i in pk_ids] == ids, 'the sensor order of the graph differs from the order of the series'
    return {'ds': ds, 'filled': filled, 'mask': mask, 'stamps': stamps, 'file_rows': pos, 'adj': np.asarray(adj, np.float32), 'ids': ids}


def splits(c: dict, max_rows: int | None = None) -> dict:
    """Sample i reads row i and has its targets at rows i+1 .. i+12 (window 1).  tsl/data/datamodule/splitters.py,
    AtTimeStepSplitter with drop_following_steps: the training samples are all samples before the first test sample."""
    T = len(c['filled']) if max_rows is None else max_rows
    last = T - HORIZON - 1
    if max_rows is None:
        ns = [int(np.datetime64(datetime.datetime(*s), 'ns').astype(np.int64)) for s in SPLIT_TS[c['ds']]]
        v0 = int(np.searchsorted(c['stamps'], ns[0], 'left')) - 1
        v1 = int(np.searchsorted(c['stamps'], ns[1], 'right')) - 2
        t0 = int(np.searchsorted(c['stamps'], ns[2], 'left')) - 1
    else:                                                              # a bounded check: the same fractions by position
        v0, v1, t0 = int(0.72 * T), int(0.795 * T), int(0.8 * T)
    val = np.arange(v0, min(v1, t0))
    return {'T': T, 'train': np.arange(t0), 'val': val, 'strict': np.setdiff1d(np.arange(t0), val), 'test': np.arange(t0, last + 1)}


def scaler(c: dict, sp: dict):
    """tsl/data/preprocessing/scalers.py, StandardScaler(axis=(0, 1)) on the rows of the training samples, masked."""
    rows = slice(0, int(sp['train'][-1]) + HORIZON + 1)
    x = np.where(c['mask'][rows], c['filled'][rows], np.nan).astype(np.float32)
    return float(np.nanmean(x)), float(np.nanstd(x))


def clock(c: dict, T: int) -> np.ndarray:
    """tsl/datasets/prototypes/mixin.py, datetime_encoded('day'): sine and cosine of the time of day."""
    a = c['stamps'][:T] * (2 * np.pi / DAY_NS)
    return np.stack([np.sin(a), np.cos(a)], -1).astype(np.float32)


def tensors(c: dict, sp: dict, dev) -> dict:
    mu, sd = scaler(c, sp)
    T = sp['T']
    scaled = torch.from_numpy((c['filled'][:T] - mu) / sd).to(dev)
    u = torch.from_numpy(clock(c, T)).to(dev)
    x = torch.cat([scaled[:, :, None], u[:, None, :].expand(-1, scaled.shape[1], -1)], -1)
    return {'mu': mu, 'sd': sd, 'scaled': scaled, 'x': x, 'y': torch.from_numpy(c['filled'][:T]).to(dev),
            'm': torch.from_numpy(c['mask'][:T]).to(dev)}


def window(a: torch.Tensor, idx: torch.Tensor) -> torch.Tensor:
    """a [rows, n] -> [len(idx), n, 12]: the 12 target rows of each sample."""
    off = torch.arange(1, HORIZON + 1, device=a.device)
    return a[idx[:, None] + off[None, :]].permute(0, 2, 1)


# --------------------------------------------------------------------------------------------------------- the encoder
def encode(c: dict, ten: dict, cfg: dict, seed: int, dev, gesn: bool) -> dict:
    torch.manual_seed(seed)                                            # the reservoir is the first draw of the seed
    cls = GraphReservoir if gesn else Reservoir
    res = cls(3, cfg['size'], cfg['layers'], cfg['leak'], 0.9, 1.0 if gesn else 0.7, True, 1.0).to(dev)
    sha = hashlib.sha1(b''.join(l.w_hh.cpu().numpy().tobytes() for l in res.reservoir_layers)).hexdigest()[:12]
    adj = torch.from_numpy(c['adj']).to(dev)
    off = adj - torch.diag(torch.diag(adj))
    t0 = time.time()
    states = res.encode(ten['x'], gesn_support(adj) if gesn else None)
    if dev.type == 'cuda':
        torch.cuda.synchronize()
    p, q = supports(off)
    return {'S': states, 'p': p, 'q': q, 'sha': sha, 'seconds': time.time() - t0, 'k': cfg.get('k', 0), 'glob': cfg.get('glob', False)}


def features(enc: dict, ten: dict, idx: torch.Tensor, k=None, glob=None):
    """The inputs of a readout for the samples idx: the embedding [b, n, F] and the scaled value [b, n, 1]."""
    k, glob = (enc['k'] if k is None else k), (enc['glob'] if glob is None else glob)
    return expand(enc['S'][idx], enc['p'], enc['q'], k, glob), ten['scaled'][idx][:, :, None]


# --------------------------------------------------------------------------------------------------------------- errors
class Errors:
    """Sum of the absolute error and count of the valid targets, by sensor and step, in the raw unit."""

    def __init__(self, n, dev):
        self.e, self.c = torch.zeros(n, HORIZON, dtype=torch.float64, device=dev), torch.zeros(n, HORIZON, dtype=torch.float64, device=dev)

    def add(self, pred, y, m):                                         # [b, n, 12]
        self.e += ((pred - y).abs() * m).sum(0).double()
        self.c += m.sum(0).double()

    def mae(self):
        return float(self.e.sum() / self.c.sum())

    def summary(self):
        at = lambda h: float(self.e[:, h].sum() / self.c[:, h].sum())  # noqa: E731
        return {'mae': self.mae(), 'mae_step3': at(2), 'mae_step6': at(5), 'mae_step12': at(11)}


def evaluate(predict, ten: dict, idx: np.ndarray, dev, dump: bool = False, batch: int = 256):
    n = ten['scaled'].shape[1]
    err, out = Errors(n, dev), []
    for i in range(0, len(idx), batch):
        b = torch.from_numpy(idx[i:i + batch]).to(dev)
        pred = predict(b) * ten['sd'] + ten['mu']
        err.add(pred, window(ten['y'], b), window(ten['m'], b))
        if dump:
            out.append(pred.permute(0, 2, 1).float().cpu().numpy())
    return err, (np.concatenate(out) if dump else None)


# ------------------------------------------------------------------------------------------------- gradient readouts
def fit_gradient(form: str, enc: dict, ten: dict, sp: dict, cfg: dict, train_idx: np.ndarray, seed: int, dev, epochs=None, log=print):
    """experiments/run_traffic_sgp.py with tsl/predictors/base_predictor.py: masked MAE in the raw unit, Adam, MultiStepLR
    (gamma 0.25), gradient clip 5, 300 batches of 64 samples per epoch, the weights of the lowest validation MAE."""
    n, F0 = ten['scaled'].shape[1], enc['S'].shape[-1]
    blocks = 1 + 2 * enc['k'] + int(enc['glob'])
    if form == 'R2':
        model = LinearReadout(F0 * blocks).to(dev)
    else:
        model = SGPReadout(F0 * blocks, blocks * cfg['layers'], n, node_emb=(form == 'R0')).to(dev)
    opt = torch.optim.Adam(model.parameters(), lr=cfg['lr'])
    sched = torch.optim.lr_scheduler.MultiStepLR(opt, milestones=list(cfg['milestones']), gamma=0.25)
    gen = torch.Generator().manual_seed(seed)
    tr = torch.from_numpy(train_idx)
    predict = lambda b: model(*features(enc, ten, b))                  # noqa: E731
    best, best_state, best_epoch, epochs_run, t0 = float('inf'), None, -1, 0, time.time()
    for epoch in range(epochs or TRAIN['epochs']):
        model.train()
        perm = tr[torch.randperm(len(tr), generator=gen)]
        for i in range(min(TRAIN['batches'], len(perm) // TRAIN['batch'])):
            b = perm[i * TRAIN['batch']:(i + 1) * TRAIN['batch']].to(dev)
            pred = predict(b) * ten['sd'] + ten['mu']
            m = window(ten['m'], b)
            loss = ((pred - window(ten['y'], b)).abs() * m).sum() / m.sum()
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), TRAIN['clip'])
            opt.step()
        sched.step()
        model.eval()
        with torch.no_grad():
            val = evaluate(predict, ten, sp['val'], dev)[0].mae()
        epochs_run = epoch + 1
        if val < best:
            best, best_epoch = val, epoch
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        if epoch % 10 == 0 or epoch - best_epoch >= TRAIN['patience']:
            log(f'  {form} epoch {epoch} loss {float(loss):.4f} val {val:.4f} best {best:.4f} ({best_epoch}) {time.time() - t0:.0f} s')
        if epoch - best_epoch >= TRAIN['patience']:
            break
    seconds = time.time() - t0
    model.load_state_dict(best_state)
    model.eval()
    info = {'epochs': epochs_run, 'best_epoch': best_epoch, 'fit_seconds': seconds,
            'weights': int(sum(p.numel() for p in model.parameters()))}
    return predict, info


# --------------------------------------------------------------------------------------------------- closed-form readouts
def gram(X, Y, M):
    """X [r, d], Y [r, 12], M [r, 12] (float64; M is 0 or 1) -> the sums of a ridge fit with an intercept, one fit per step.
    A row with a masked target is left out of the fit of that step."""
    G0, s0 = X.T @ X, X.sum(0)
    G, sx = G0.expand(HORIZON, -1, -1).clone(), s0.expand(HORIZON, -1).clone()
    for h in range(HORIZON):
        bad = M[:, h] == 0
        if bool(bad.any()):
            Xb = X[bad]
            G[h] -= Xb.T @ Xb
            sx[h] -= Xb.sum(0)
    Ym = Y * M
    return {'G': G, 'c': (X.T @ Ym).T.contiguous(), 'sx': sx, 'sy': Ym.sum(0), 'n': M.sum(0)}


def add(a, b):
    return b if a is None else {k: a[k] + b[k] for k in a}


def solve(g, alphas):
    """-> W [alphas, 12, d], b [alphas, 12]: (Xc'Xc + alpha I) w = Xc'yc with centred sums, as sklearn Ridge with an intercept."""
    n = g['n'].clamp(min=1.0)
    mx, my = g['sx'] / n[:, None], g['sy'] / n
    Gc = g['G'] - n[:, None, None] * mx[:, :, None] * mx[:, None, :]
    cc = g['c'] - n[:, None] * mx * my[:, None]
    eye = torch.eye(Gc.shape[-1], dtype=Gc.dtype, device=Gc.device)
    W, B, eig = [], [], None
    for a in alphas:
        L, info = torch.linalg.cholesky_ex(Gc + a * eye)
        w = torch.cholesky_solve(cc[:, :, None], L)[:, :, 0]
        if bool((info > 0).any()) or not bool(torch.isfinite(w).all()):
            eig = torch.linalg.eigh(Gc) if eig is None else eig        # the Gram matrix is not positive definite in float64
            lam, V = eig
            w = torch.einsum('hij,hj->hi', V, torch.einsum('hji,hj->hi', V, cc) / (lam.clamp(min=0.0) + a))
        W.append(w)
        B.append(my - (mx * w).sum(-1))
    return torch.stack(W), torch.stack(B)


def loo(g, w, b, alpha, X, Y, M, day: int = 288):
    """Leave-one-out error of one ridge fit (mean absolute residual by step, scaled unit): the plain form, and the form that
    leaves out one day of consecutive rows.  X [r, d], Y, M [r, 12], rows in time order."""
    n = g['n'].clamp(min=1.0)
    mx = g['sx'] / n[:, None]
    Gc = g['G'] - n[:, None, None] * mx[:, :, None] * mx[:, None, :]
    eye = torch.eye(Gc.shape[-1], dtype=Gc.dtype, device=Gc.device)
    r = X.shape[0]
    pad = (-r) % day
    plain, blocked = [], []
    for h in range(HORIZON):
        L, info = torch.linalg.cholesky_ex(Gc[h] + alpha * eye)
        if int(info) > 0:
            return None, None
        m = M[:, h]
        Xc = (X - mx[h]) * m[:, None]
        e = (Y[:, h] - X @ w[h] - b[h]) * m
        Z = torch.cholesky_solve(Xc.T.contiguous(), L).T               # Xc (Gc + alpha I)^-1
        lev = (Z * Xc).sum(1) + m / n[h]
        plain.append(float((e / (1 - lev).clamp(min=1e-6)).abs().sum() / n[h]))
        Zp, Xp = torch.nn.functional.pad(Z, (0, 0, 0, pad)), torch.nn.functional.pad(Xc, (0, 0, 0, pad))
        ep, mp = torch.nn.functional.pad(e, (0, pad)), torch.nn.functional.pad(m, (0, pad))
        Zp, Xp, ep, mp = Zp.view(-1, day, Z.shape[1]), Xp.view(-1, day, Z.shape[1]), ep.view(-1, day), mp.view(-1, day)
        H = Zp @ Xp.transpose(1, 2) + mp[:, :, None] * mp[:, None, :] / n[h]
        res = torch.linalg.solve(torch.eye(day, dtype=H.dtype, device=H.device) - H, ep[:, :, None])[:, :, 0]
        blocked.append(float((res.abs() * mp).sum() / n[h]))
    return plain, blocked


def rows_of(enc, ten, idx, dev, k, glob, sensors=None, pw=None, chunk=1024):
    """Features [u, embedding] of the samples idx, float32: [len(idx), n or len(sensors), d]."""
    out = []
    for i in range(0, len(idx), chunk):
        b = torch.from_numpy(idx[i:i + chunk]).to(dev)
        if sensors is None:
            x, u = features(enc, ten, b, k, glob)
        else:
            x = expand(enc['S'][b], pw[0], pw[1], k, glob, rows=sensors)
            u = ten['scaled'][b][:, sensors][:, :, None]
        out.append(torch.cat([u, x], -1))
    return torch.cat(out)


def targets(ten, idx, dev, masked: bool):
    b = torch.from_numpy(idx).to(dev)
    m = window(ten['m'], b).double()
    return window(ten['scaled'], b).double(), (m if masked else torch.ones_like(m))


def fit_pooled(enc, ten, sp, fit_idx, dev, alphas, masked=True, select=True, chunk=128):
    """One ridge model for all sensors, one fit per step.  -> predict for the final fit, predict of the selection fit, info."""
    k, glob = enc['k'], enc['glob']
    val_set = set(sp['val'].tolist())
    sel_idx = np.array([i for i in fit_idx if i not in val_set]) if select else fit_idx
    t0 = time.time()

    def accumulate(idx):
        g = None
        for i in range(0, len(idx), chunk):
            part = idx[i:i + chunk]
            X = rows_of(enc, ten, part, dev, k, glob).double()
            Y, M = targets(ten, part, dev, masked)
            d = X.shape[-1]
            g = add(g, gram(X.reshape(-1, d), Y.reshape(-1, HORIZON), M.reshape(-1, HORIZON)))
        return g

    g_sel = accumulate(sel_idx)
    rest = np.setdiff1d(fit_idx, sel_idx)
    g_fit = add(g_sel, accumulate(rest)) if len(rest) else g_sel
    W, B = solve(g_sel, alphas)
    mk = lambda w, b: (lambda idx: rows_of(enc, ten, idx.cpu().numpy(), dev, k, glob).double() @ w.T + b)  # noqa: E731
    best, val_by_alpha = 0, []
    if select:
        for j in range(len(alphas)):
            val_by_alpha.append(evaluate(mk(W[j], B[j]), ten, sp['val'], dev)[0].mae())
        best = int(np.argmin(val_by_alpha))
    sel = (W[best], B[best])
    fin = sel if g_fit is g_sel else tuple(t[0] for t in solve(g_fit, [alphas[best]]))
    info = {'alpha': float(alphas[best]), 'val_mae_by_alpha': val_by_alpha, 'fit_seconds': time.time() - t0,
            'weights': int(fin[0].numel() + fin[1].numel()), 'fit_rows': int(len(fit_idx)), 'selection_rows': int(len(sel_idx))}
    return mk(*fin), mk(*sel), info, fin, sel


def fit_per_sensor(enc, ten, sp, fit_idx, dev, alphas, k, glob, pooled=None, group=8, log=print):
    """One ridge model per sensor and step.  pooled = (final, selection) weights of a pooled fit: then the target is the
    residual of that fit.  -> errors of validation (selection fit) and test (final fit), the test forecast, info by sensor."""
    n, T = ten['scaled'].shape[1], sp['T']
    val_set = set(sp['val'].tolist())
    sel_idx = np.array([i for i in fit_idx if i not in val_set])
    refit = len(sel_idx) != len(fit_idx)
    all_idx = np.arange(T - HORIZON)
    pos = {name: torch.from_numpy(idx).to(dev) for name, idx in (('sel', sel_idx), ('fit', fit_idx), ('val', sp['val']), ('test', sp['test']))}
    err_val, err_test = Errors(n, dev), Errors(n, dev)
    forecast = np.zeros((len(sp['test']), HORIZON, n), np.float32)
    alpha_s, loo_plain, loo_block = np.zeros(n), np.full((n, HORIZON), np.nan), np.full((n, HORIZON), np.nan)
    t0 = time.time()
    for s0 in range(0, n, group):
        sensors = torch.arange(s0, min(s0 + group, n), device=dev)
        pw = (powers(enc['p'], k, sensors), powers(enc['q'], k, sensors))
        X_all = rows_of(enc, ten, all_idx, dev, k, glob, sensors, pw)                    # [samples, group, d] float32
        for j, s in enumerate(sensors.tolist()):
            Xs = X_all[:, j]
            Y = ten['scaled'][:, s][pos_rows(all_idx, dev)].double()                     # [samples, 12]
            M = ten['m'][:, s][pos_rows(all_idx, dev)].double()
            Xd = Xs.double()
            base = {}
            if pooled is not None:                                      # the features of the pooled fit are the features here
                base = {'fit': Xd @ pooled[0][0].T + pooled[0][1], 'sel': Xd @ pooled[1][0].T + pooled[1][1]}
            y_of = lambda name: Y - base[name] if base else Y           # noqa: E731
            g_sel = gram(Xd[pos['sel']], y_of('sel')[pos['sel']], M[pos['sel']])
            W, B = solve(g_sel, alphas)
            pv = torch.einsum('rd,ahd->arh', Xd[pos['val']], W) + B[:, None, :]          # [alphas, val, 12]
            if base:
                pv = pv + base['sel'][pos['val']][None]
            yv, mv = ten['y'][:, s][pos_rows(sp['val'], dev)], ten['m'][:, s][pos_rows(sp['val'], dev)]
            ev = ((pv * ten['sd'] + ten['mu'] - yv[None]).abs() * mv[None]).sum((1, 2)) / mv.sum().clamp(min=1)
            a = int(torch.argmin(ev))
            alpha_s[s] = alphas[a]
            err_val.e[s] += ((pv[a] * ten['sd'] + ten['mu'] - yv).abs() * mv).sum(0)
            err_val.c[s] += mv.sum(0)
            if refit:
                g_fit = gram(Xd[pos['fit']], y_of('fit')[pos['fit']], M[pos['fit']])
                w, b = (t[0] for t in solve(g_fit, [alphas[a]]))
            else:
                g_fit, w, b = g_sel, W[a], B[a]
            pt = Xd[pos['test']] @ w.T + b
            if base:
                pt = pt + base['fit'][pos['test']]
            pt = pt * ten['sd'] + ten['mu']
            yt, mt = ten['y'][:, s][pos_rows(sp['test'], dev)], ten['m'][:, s][pos_rows(sp['test'], dev)]
            err_test.e[s] += ((pt - yt).abs() * mt).sum(0)
            err_test.c[s] += mt.sum(0)
            forecast[:, :, s] = pt.float().cpu().numpy()
            lp, lb = loo(g_fit, w, b, alphas[a], Xd[pos['fit']], y_of('fit')[pos['fit']], M[pos['fit']])
            if lp is not None:
                loo_plain[s], loo_block[s] = lp, lb
        del X_all
        log(f'  sensors {s0 + len(sensors)}/{n} {time.time() - t0:.0f} s')
    info = {'fit_seconds': time.time() - t0, 'fit_rows': int(len(fit_idx)), 'selection_rows': int(len(sel_idx)),
            'alpha_counts': {str(a): int((alpha_s == a).sum()) for a in alphas}}
    return err_val, err_test, forecast, info, {'alpha': alpha_s, 'loo_plain': loo_plain * ten['sd'], 'loo_blocked': loo_block * ten['sd']}


def pos_rows(idx: np.ndarray, dev) -> torch.Tensor:
    """[len(idx), 12] target rows of the samples idx."""
    return torch.from_numpy(idx).to(dev)[:, None] + torch.arange(1, HORIZON + 1, device=dev)[None, :]


# ------------------------------------------------------------------------------------------------------------- commands
def commit(path: Path) -> str:
    return subprocess.run(['git', '-C', str(path), 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()


def fit(opt) -> int:
    dev = torch.device('cuda' if torch.cuda.is_available() and not opt.cpu else 'cpu')
    key = (opt.city, opt.setting)
    assert key in SETTINGS, f'no setting {opt.setting} at {opt.city}'
    gesn = opt.setting == 'gesn'
    bad = [f for f in opt.forms if (f == 'R7') != gesn]
    assert not bad, f'forms {bad}: R7 needs the setting gesn, and the setting gesn has the form R7 only'
    cfg = SETTINGS[key]
    base = REPO / 'results' / 'sgp' / (f'check_{opt.city}_h12' if opt.max_rows or opt.max_sensors else f'{opt.city}_h12')
    out_of = lambda form: base / 'train' / f'{opt.setting}_{opt.split}' / f'{form}_s{opt.seed}'   # noqa: E731
    forms = [f for f in opt.forms if not (out_of(f) / 'metrics.json').exists()]
    if not forms:
        print(f'{opt.city} {opt.setting} {opt.split} seed {opt.seed}: every form is done')
        return 0
    c = load_city(opt.city)
    if opt.max_sensors:
        k = opt.max_sensors
        c.update(filled=c['filled'][:, :k], mask=c['mask'][:, :k], adj=c['adj'][:k, :k], ids=c['ids'][:k])
    sp = splits(c, opt.max_rows)
    ten = tensors(c, sp, dev)
    enc = encode(c, ten, cfg, opt.seed, dev, gesn)
    fit_idx = sp['train'] if opt.split == 'release' else sp['strict']
    n = ten['scaled'].shape[1]
    print(f"{opt.city} {opt.setting} {opt.split} seed {opt.seed} on {dev}: rows {sp['T']} sensors {n} samples train {len(sp['train'])} "
          f"strict {len(sp['strict'])} val {len(sp['val'])} test {len(sp['test'])}; states {tuple(enc['S'].shape)} in {enc['seconds']:.1f} s; "
          f"reservoir {enc['sha']}", flush=True)
    common = {'city': opt.city, 'setting': opt.setting, 'split': opt.split, 'seed': opt.seed, 'device': str(dev),
              'gpu': torch.cuda.get_device_name(0) if dev.type == 'cuda' else None, 'commit': commit(REPO), 'reservoir_sha1': enc['sha'],
              'rows': sp['T'], 'sensors': n, 'samples': {k: int(len(sp[k])) for k in ('train', 'strict', 'val', 'test')},
              'scaler': [ten['mu'], ten['sd']], 'encode_seconds': enc['seconds'], 'state_gb': enc['S'].numel() * 4 / 1e9,
              'embedding_gb_as_released': enc['S'].numel() * 4 / 1e9 * (1 + 2 * enc['k'] + int(enc['glob'])),
              'first_target_row': int(sp['test'][0]) + 1, 'first_target_stamp_ns': int(c['stamps'][int(sp['test'][0]) + 1]),
              'published_mae': PUBLISHED[opt.city].get(opt.setting)}
    pooled = None
    log = lambda s: print(s, flush=True)                               # noqa: E731
    for form in forms:
        if dev.type == 'cuda':
            torch.cuda.reset_peak_memory_stats()
        sens = {}
        if form in GRADIENT:
            torch.manual_seed(opt.seed + 1)
            predict, info = fit_gradient(form, enc, ten, sp, cfg, fit_idx, opt.seed, dev, opt.epochs, log)
            with torch.no_grad():
                err_val = evaluate(predict, ten, sp['val'], dev)[0]
                err_test, forecast = evaluate(predict, ten, sp['test'], dev, dump=True)
        elif form in ('R3', 'R7'):
            alphas = [1e-3] if form == 'R7' else list(ALPHAS)
            predict, predict_sel, info, fin, sel = fit_pooled(enc, ten, sp, fit_idx, dev, alphas, masked=(form == 'R3'), select=(form == 'R3'))
            pooled = (fin, sel) if form == 'R3' else pooled
            err_val = evaluate(predict_sel, ten, sp['val'], dev)[0]
            err_test, forecast = evaluate(predict, ten, sp['test'], dev, dump=True)
        else:
            if form == 'R6' and pooled is None:
                pooled = fit_pooled(enc, ten, sp, fit_idx, dev, list(ALPHAS))[3:]
            k, glob = (0, False) if form == 'R5' else (enc['k'], enc['glob'])
            err_val, err_test, forecast, info, sens = fit_per_sensor(enc, ten, sp, fit_idx, dev, list(ALPHAS), k, glob,
                                                                     pooled if form == 'R6' else None, log=log)
        out = out_of(form)
        out.mkdir(parents=True, exist_ok=True)
        np.save(out / 'forecast_test.npy', forecast)
        np.savez(out / 'sensors.npz', val_err=err_val.e.cpu().numpy(), val_count=err_val.c.cpu().numpy(),
                 test_err=err_test.e.cpu().numpy(), test_count=err_test.c.cpu().numpy(), **sens)
        rec = dict(common, form=form, test=err_test.summary(), val=err_val.summary(), **info,
                   peak_gpu_gb=(torch.cuda.max_memory_allocated() / 1e9 if dev.type == 'cuda' else None),
                   peak_rss_gb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6)
        (out / 'metrics.json').write_text(json.dumps(rec, indent=1))
        print(f"{form}: test MAE {rec['test']['mae']:.4f} (steps 3/6/12: {rec['test']['mae_step3']:.4f} {rec['test']['mae_step6']:.4f} "
              f"{rec['test']['mae_step12']:.4f}) val {rec['val']['mae']:.4f} published {common['published_mae']} fit {info['fit_seconds']:.0f} s", flush=True)
    return 0


def upstream_reservoir():
    """The class Reservoir of the release, from its source file, with stand-ins for the three names that the nas venv lacks."""
    import types

    def rearrange(x, pattern, **kw):
        if pattern == 'b s n f -> s (b n) f':
            b, s, n, f = x.shape
            return x.permute(1, 0, 2, 3).reshape(s, b * n, f)
        if pattern == 's l (b n) f -> b s n (l f)':
            s, l, _, f = x.shape
            return x.view(s, l, kw['b'], kw['n'], f).permute(2, 0, 3, 1, 4).reshape(kw['b'], s, kw['n'], l * f)
        raise ValueError(pattern)

    mods = {'einops': types.SimpleNamespace(rearrange=rearrange), 'tsl': types.ModuleType('tsl'), 'tsl.nn': types.ModuleType('tsl.nn'),
            'tsl.nn.utils': types.SimpleNamespace(get_functional_activation=lambda name: getattr(torch, name)),
            'lib': types.ModuleType('lib'), 'lib.utils': types.SimpleNamespace(self_normalizing_activation=None)}
    saved = {k: sys.modules.get(k) for k in mods}
    sys.modules.update(mods)
    try:
        ns = {'__name__': 'upstream_reservoir'}
        exec(compile((UP / 'lib/nn/reservoir/reservoir.py').read_text(), 'reservoir.py', 'exec'), ns)
    finally:
        for k, v in saved.items():
            sys.modules.pop(k) if v is None else sys.modules.__setitem__(k, v)
    return ns['Reservoir']


def check(opt) -> int:
    ds, L = opt.city, []
    c = load_city(ds)
    npz = np.load(datasets.npz_path(ds), allow_pickle=True)['data'][:, :, 0]
    held = c['filled'][c['file_rows']]
    same = np.abs(np.where(c['mask'][c['file_rows']], held - npz, 0)).max()
    L.append(f"series: {len(c['filled'])} rows on the full index, {len(c['file_rows'])} rows in the file, {c['filled'].shape[1]} sensors; "
             f"rows absent from the file: {len(c['filled']) - len(c['file_rows'])}; largest difference to the .npz of the project on valid values: {same:.2e}; "
             f"masked share: {1 - c['mask'].mean():.4f}")
    # the graph of the release from the raw distances, against the DCRNN pickle of the project without its diagonal
    import pandas as pd
    dist_file = datasets._resolve(datasets.info(ds)['raw_distances'])
    d = pd.read_csv(dist_file)
    if str(d.columns[0]).replace('.', '').isdigit():                   # a file with no header line
        d = pd.read_csv(dist_file, header=None)
    n = len(c['ids'])
    to = {int(float(s)): i for i, s in enumerate(c['ids'])}
    dist = np.full((n, n), np.inf, np.float32)
    for a, b, w in d.values:
        if int(a) in to and int(b) in to:
            dist[to[int(a)], to[int(b)]] = w
    sim = np.exp(-np.square(dist / dist[~np.isinf(dist)].std()))
    sim[sim < 0.1] = 0
    np.fill_diagonal(sim, 0)
    off = c['adj'] - np.diag(np.diag(c['adj']))
    L.append(f"graph: {int((sim > 0).sum())} edges from the raw distances with the kernel of the release (Table 3 of the paper: "
             f"{ {'metrla': 1515, 'pemsbay': 2369}[ds] }); {int((off > 0).sum())} edges in the pickle without its diagonal; edges in one and not "
             f"in the other: {int(((sim > 0) != (off > 0)).sum())}; largest difference in a weight: {np.abs(sim - off).max():.2e}; "
             f"diagonal of the pickle: min {np.diag(c['adj']).min():.2f} max {np.diag(c['adj']).max():.2f}")
    sp = splits(c)
    T = sp['T']
    L.append(f"split of the release: {len(sp['train'])} training samples (they include the {len(sp['val'])} validation samples), "
             f"{len(sp['strict'])} without them, {len(sp['test'])} test samples; first validation sample at {sp['val'][0] / T:.4f} of the rows, "
             f"first test sample at {sp['test'][0] / T:.4f}; rows between the last validation sample and the first test sample: {sp['test'][0] - sp['val'][-1] - 1}")
    rows_file = len(npz)
    test_len = int(rows_file * 0.2)
    pub = (rows_file - test_len) + 12 + np.arange(test_len - 23)                         # pilot.calibration: first target row, file rows
    file_pos = np.full(T, -1)
    file_pos[c['file_rows']] = np.arange(rows_file)
    ours = file_pos[sp['test'] + 1]
    L.append(f"test windows: {len(pub)} under the published protocol of pilot.calibration, {len(sp['test'])} here; common first target rows: "
             f"{len(np.intersect1d(pub, ours[ours >= 0]))}; test samples here whose first target row is absent from the file: {int((ours < 0).sum())}")
    mu, sd = scaler(c, sp)
    L.append(f"scaler: mean {mu:.4f} deviation {sd:.4f} (rows of the training samples, masked)")
    # 2,000 steps on the CPU
    torch.manual_seed(0)
    cfg = SETTINGS[(ds, 'release')]
    dev = torch.device('cpu')
    sp2 = splits(c, 2000)
    ten = tensors(c, sp2, dev)
    enc = encode(c, ten, cfg, 0, dev, False)
    x, u = features(enc, ten, torch.arange(4))
    full = T * n * x.shape[-1] * 4 / 2 ** 30
    L.append(f"encoding of 2,000 steps on the CPU ({torch.get_num_threads()} threads): {enc['seconds'] / 2:.2f} s per 1,000 steps; embedding size "
             f"{x.shape[-1]}; the full embedding of the release would hold {full:.1f} GiB (about {2 * full:.0f} GiB at the peak, estimate); "
             f"the states that this runner holds: {T * n * enc['S'].shape[-1] * 4 / 2 ** 30:.1f} GiB")
    # ridge from accumulated sums against sklearn on the same rows
    from sklearn.linear_model import Ridge
    idx = np.arange(1500)
    X = rows_of(enc, ten, idx, dev, enc['k'], enc['glob'])[:, :20].double()
    Y, M = targets(ten, idx, dev, masked=False)
    Y, M, d = Y[:, :20], M[:, :20], X.shape[-1]
    g = None
    for i in range(0, 1500, 200):
        g = add(g, gram(X[i:i + 200].reshape(-1, d), Y[i:i + 200].reshape(-1, HORIZON), M[i:i + 200].reshape(-1, HORIZON)))
    W, B = solve(g, [1.0])
    sk = Ridge(alpha=1.0).fit(X.reshape(-1, d).numpy(), Y.reshape(-1, HORIZON).numpy())
    ours_p, sk_p = X.reshape(-1, d) @ W[0].T + B[0], torch.from_numpy(sk.predict(X.reshape(-1, d).numpy()))
    L.append(f"ridge from accumulated sums against sklearn Ridge (30,000 rows, {d} features, weight 1): largest difference in a weight "
             f"{np.abs(W[0].numpy() - sk.coef_).max():.2e} (largest weight {np.abs(sk.coef_).max():.2e}); largest difference in a fitted value "
             f"{float((ours_p - sk_p).abs().max()):.2e}")
    if (UP / 'lib/nn/reservoir/reservoir.py').exists():
        torch.manual_seed(0)
        up = upstream_reservoir()(input_size=3, hidden_size=cfg['size'], num_layers=cfg['layers'], leaking_rate=cfg['leak'], spectral_radius=0.9,
                                  density=0.7, alpha_decay=True)
        torch.manual_seed(0)
        mine = Reservoir(3, cfg['size'], cfg['layers'], cfg['leak'], 0.9, 0.7, True, 1.0)
        dw = max(float((a.w_hh - b.w_hh).abs().max()) + float((a.w_ih - b.w_ih).abs().max()) + float((a.b_ih - b.b_ih).abs().max())
                 for a, b in zip(up.reservoir_layers, mine.reservoir_layers))
        xin = ten['x'][:300, :5]
        ds_ = float((up(xin[None])[0] - mine.encode(xin)).abs().max())
        L.append(f"reservoir of this runner against the source of the release (commit {commit(UP)}), seed 0: largest difference in a weight {dw:.1e}, "
                 f"in a state over 300 steps {ds_:.1e}")
    else:
        L.append(f'reservoir against the release: not run, {UP} is absent (pilot/sgp_setup.sh)')
    out = REPO / 'results' / 'sgp' / f'{ds}_h12' / 'CHECKS.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f'# sgp: checks without a GPU, {ds}\n\nFork commit {commit(REPO)}; host class: login node.\n\n' + '\n'.join(f'- {s}' for s in L) + '\n')
    print('\n'.join(L))
    return 0


def headroom(opt) -> int:
    """SGP against STID under the published protocol, on the common test windows of pilot.calibration (the test windows of the
    benchst split), with its scorer: the masked MAE in the raw unit, a target of 0 is missing."""
    from pilot import calibration as cal
    from pilot.fmroute import HORIZON as H, WINDOW, load_raw, split_rows
    basicts = Path(os.environ.get('NAS_ROOT', REPO.parent)) / 'BasicTS'
    L = ['# sgp: headroom of the fixed random encoder against STID', '',
         'Masked MAE in the raw unit on the common test windows of `pilot.calibration` (a target of 0 is missing).  Mean and standard',
         'deviation (ddof = 1) over the seeds.  g = (row of the reference - SGP) / pooled deviation, on the mean of the 12 steps; a',
         'positive g means that SGP has the lower error.  The two sides differ in the scaler, in the treatment of zeros in the input',
         'and in the split fractions; the common windows remove the difference in the test set only.', '']
    for ds in opt.cities:
        c = load_city(ds)
        raw = load_raw(ds)[:, :, 0].astype(np.float32)
        rows = split_rows(len(raw), WINDOW, H, 'test')                                 # first target row of each window, file rows
        y = raw[rows[:, None] + np.arange(H)[None]]
        v = y != 0
        file_pos = np.full(len(c['filled']), -1)
        file_pos[c['file_rows']] = np.arange(len(raw))
        table = {}
        for d in sorted((REPO / 'results' / 'sgp' / f'{ds}_h12' / 'train').glob('*/*_s*')):
            if not (d / 'metrics.json').exists():
                continue
            m = json.loads((d / 'metrics.json').read_text())
            f = np.load(d / 'forecast_test.npy', mmap_mode='r')
            first = file_pos[m['first_target_row'] + np.arange(len(f))]
            take = np.searchsorted(first, rows)
            assert np.array_equal(first[take], rows), f'{d}: a common window is absent from the forecast'
            p = np.asarray(f[take], dtype=np.float64)
            err = np.where(v, np.abs(p - y), 0.0)
            table.setdefault((d.parent.name, m['form']), []).append([err[:, h].sum() / v[:, h].sum() for h in (2, 5, 11)] + [err.sum() / v.sum()])
        ref = cal.city(ds, basicts)['rows']
        L += [f'## {ds} ({len(rows)} windows)', '', '| Row | seeds | step 3 | step 6 | step 12 | mean of 12 | sd | g against SGP (release_release, R0) |', '|---|---|---|---|---|---|---|---|']
        stat = {k: (np.mean(a, 0), np.std(np.array(a)[:, 3], ddof=1) if len(a) > 1 else float('nan'), len(a)) for k, a in table.items()}
        base = stat.get(('release_release', 'R0'))
        g = lambda mean, sd: '' if base is None or not sd == sd else f'{(mean - base[0][3]) / np.sqrt((sd ** 2 + base[1] ** 2) / 2):+.1f}'   # noqa: E731
        for name, r in ref.items():
            if r['sd'] is not None:
                L.append(f"| {name} | {r['seeds']} | " + ' | '.join(f'{x:.4f}' for x in r['mean'][:4]) + f" | {r['sd'][3]:.4f} | {g(r['mean'][3], r['sd'][3])} |")
        for (setting, form), (mean, sd, k) in sorted(stat.items()):
            L.append(f'| SGP runner, {setting}, {form} | {k} | ' + ' | '.join(f'{x:.4f}' for x in mean) + f' | {sd:.4f} | {g(mean[3], sd)} |')
        L.append('')
    out = REPO / 'results' / 'sgp' / 'compare' / 'HEADROOM.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(L) + f'\nFork commit {commit(REPO)}.\n')
    print('\n'.join(L))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('check')
    a.add_argument('--city', required=True, choices=sorted(SPLIT_TS))
    a = sub.add_parser('fit')
    a.add_argument('--city', required=True, choices=sorted(SPLIT_TS))
    a.add_argument('--setting', default='release')
    a.add_argument('--split', default='release', choices=('release', 'strict'))
    a.add_argument('--seed', type=int, default=0)
    a.add_argument('--forms', nargs='+', default=['R0'], choices=['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7'])
    a.add_argument('--epochs', type=int, default=None, help='bounded checks only')
    a.add_argument('--max-rows', type=int, default=None, help='bounded checks only: the first rows of the series; output under check_<city>_h12')
    a.add_argument('--max-sensors', type=int, default=None, help='bounded checks only: the first sensors of the city')
    a.add_argument('--cpu', action='store_true')
    a = sub.add_parser('headroom')
    a.add_argument('--cities', nargs='+', default=sorted(SPLIT_TS))
    opt = ap.parse_args(argv)
    return {'check': check, 'fit': fit, 'headroom': headroom}[opt.cmd](opt)


if __name__ == '__main__':
    sys.exit(main())
