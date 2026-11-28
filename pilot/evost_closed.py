"""A closed-form update of an old STAEFormer checkpoint, under the protocol of the upstream maintenance study
(Survey/experiments/evost-plan.md, the oracle test of the closed-form update).

The old checkpoint runs one time over the fit windows in evaluation mode, with no backward pass.  A ridge fit per sensor maps
a stored feature of that forward pass to the residual of the base forecast.  The base forecast of the arm is the old forecast
plus the fitted correction; the calibrator, the stream and the metrics are the unchanged upstream protocol (e3_confirm.run).

Arms (base forecast):
  same       the checkpoint of the target year (the reference)
  stale5o    the five-year-old checkpoint, its own embeddings and input statistics (no update)
  cf_proj    stale5o + ridge on the 1,248 values in front of the output projection of the backbone
  cf_last    stale5o + ridge on the 12 values in front of the last linear layer
  cf_calib   stale5o + ridge on the 29 input-side features of the upstream calibrator (the control: no feature of the model
             but its forecast)

The fit reads the windows of the gradient fits of the upstream study: the last 2,048 training windows of the target year.  The
last 512 of them are the holdout that chooses one ridge strength per arm from RIDGES; the final weights come from all the fit
windows with that strength.  No validation or test value is read by a fit.  For every strength the file closed_<place>.npz
keeps, per sensor, the holdout error, the leave-one-out error and the error with no update.

With EVOST_CLOSED_STUDY=budget the run is the history-budget study of the upstream tree (history_budget/e16_budget.py) with
one more arm.  For each budget b of 64, 256, 1,024 and 2,048 windows, everything that reads labels of the target year before
the stream is cut to b windows, and one run of the protocol holds the three actions: stale5o (no update), cf_proj (the
closed-form update; the last b/4 windows choose its ridge strength) and fit_emb (the gradient refresh of the upstream budget
study, at its fixed rate).  Outputs: <out>/b<budget>/ per budget, <out>/closed_info.json, <out>/closed_<place>_b<budget>.npz.

Run by `python -m pilot.evost_run maintain --studies closed` or `--studies closed_budget`, with the arguments of the upstream
drivers:
  python pilot/evost_closed.py --bundle B.npz --seed 51 --out NEW_DIR --device cuda:0
Env: EVOST_UPSTREAM (the upstream tree), EVOST_CLOSED_STUDY (budget, or not set), EVOST_CLOSED_PLACES (a space list, default
"proj last calib"; "proj" in the budget study), EVOST_CLOSED_FIT_WINDOWS (a bounded check only: fewer fit windows for the
ridge and for the calibrator), EVOST_CLOSED_BUDGETS (a bounded check only: a space list of budgets).
"""
import json
import os
from pathlib import Path
import sys
import time

UP = Path(os.environ.get('EVOST_UPSTREAM') or Path(__file__).resolve().parents[2] / 'EvoST')
BUDGET = os.environ.get('EVOST_CLOSED_STUDY') == 'budget'
sys.path.insert(0, str(UP / 'experiments' / 'evost' / ('history_budget' if BUDGET else 'parameter_groups')))
import numpy as np                                                       # noqa: E402
import torch                                                             # noqa: E402
import e3_confirm as e3                                                  # noqa: E402
import e5_stae as e5                                                     # noqa: E402
import e10_refresh as e10                                                # noqa: E402
import g28_common as g                                                   # noqa: E402

if BUDGET:
    import e16_budget as e16                                             # noqa: E402

PLACES = tuple(os.environ.get('EVOST_CLOSED_PLACES', 'proj' if BUDGET else 'proj last calib').split())
RIDGES = (1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1., 10., 100.)             # times the mean diagonal of the Gram matrix of the sensor; the constant is free
BOUNDED = int(os.environ.get('EVOST_CLOSED_FIT_WINDOWS', '0'))
if BOUNDED:
    e3.FIT_WINDOWS = BOUNDED


class Closed:
    """The closed-form arms, on top of a bundle class of the upstream tree.  A variant is `cf_<place>`, or `cf_<place>@<budget>` in
    the budget study; each variant has its own weights."""

    def __init__(self, path):
        super().__init__(path)
        self._theta, self._unit, self._scale, self.arrays = {}, {}, {}, {}

    def scale(self):
        """The scale of the targets, as e3_confirm.run computes it for the calibrator on the current fit windows."""
        if e3.FIT_WINDOWS not in self._scale:
            raw = self.z['raw_train']
            n_fit = min(e3.FIT_WINDOWS, g.n_windows(raw))
            y = g.clean_y(g.get_windows(raw, g.n_windows(raw) - n_fit, n_fit)[1])
            self._scale[e3.FIT_WINDOWS] = float(y[g.target_valid(y)].std())
        return self._scale[e3.FIT_WINDOWS]

    def feats(self, place, x, device, cols=slice(None)):
        """Old forecast b [B, N, 12] and the feature [B, sensors of cols, d] (last column: ones) for normalised inputs x [B, N, 12]."""
        model, table = self.model(self.old, device), e5.StaeBundle.table(self, self.old, device)
        grab = {}
        hooks = [model.backbone.output_proj.register_forward_hook(lambda m, i, o: grab.__setitem__('proj', i[0])),
                 model.fc.register_forward_hook(lambda m, i, o: grab.__setitem__('last', i[0]))]
        try:
            b = model(x, table)
        finally:
            for h in hooks:
                h.remove()
        if place == 'calib':
            return b, g.features(x[:, cols], b[:, cols], self.scale())
        if place not in self._unit:                                      # one scalar per place, from the first batch of the fit
            self._unit[place] = float(grab[place].pow(2).mean().sqrt().clamp_min(1e-12))
        h = grab[place][:, cols] / self._unit[place]
        return b, torch.cat((h, torch.ones_like(h[..., :1])), -1)

    def closed(self, variant, device):
        """theta [N, d, 12] in the units of the targets: forecast = old forecast + feature @ theta."""
        if variant in self._theta:
            return self._theta[variant]
        place = variant[3:].split('@')[0]
        assert '@' not in variant or int(variant.split('@')[1]) == e3.FIT_WINDOWS
        began, raw, n, scale = time.time(), self.z['raw_train'], self.n, self.scale()
        T = min(e3.FIT_WINDOWS, g.n_windows(raw))
        first, cut = g.n_windows(raw) - T, T - max(1, min(e10.FIT['holdout'], T // 4))
        x_raw, y_raw = g.get_windows(raw, first, T)
        x, y = g.normalize_x(x_raw, *self.norm[self.old]), g.clean_y(y_raw)                      # [T, N, 12] on the CPU
        d = dict(proj=12 * self.model(self.old, device).backbone.model_dim + 1, last=g.Y_LEN + 1, calib=g.D_FEAT)[place]
        cuda = device.type == 'cuda'
        if cuda:
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
        room = .25 * torch.cuda.get_device_properties(device).total_memory if cuda else 2e9
        group = int(max(1, min(n, room // (T * d * 4))))                # sensors whose features of all fit windows stay on the device
        part = int(max(1, min(group, 2e9 // (T * d * 8))))               # sensors of one batched solve
        L = len(RIDGES)
        acc = {k: np.zeros((L, n)) for k in ('hold_abs', 'loo_abs', 'fit_abs')}
        acc.update({k: np.zeros(n) for k in ('hold_cnt', 'hold_abs0', 'all_cnt', 'all_abs0', 'windows')})
        theta = torch.zeros(L, n, d, g.Y_LEN, dtype=torch.float32)
        seconds = dict(forward=0., solve=0.)
        penalty = torch.ones(d, dtype=torch.float64, device=device)
        penalty[-1] = 0.                                                 # the constant is not shrunk
        eye = torch.eye(d, dtype=torch.float64, device=device)
        base = None
        for lo in range(0, n, group):
            cols = slice(lo, min(lo + group, n))
            t0, phis, bs, s = time.time(), [], [], 0
            while s < T:                                                 # the forward pass, with a smaller batch after an out-of-memory error
                try:
                    b, phi = self.feats(place, x[s:s + self._sub].to(device), device, cols)
                except torch.cuda.OutOfMemoryError:
                    assert self._sub > 1, 'out of GPU memory with one window per forward'
                    self._sub = max(1, self._sub // 2)
                    torch.cuda.empty_cache()
                    continue
                phis.append(phi.to(torch.float32))
                if base is None:
                    bs.append(b.to(torch.float32).cpu())
                s += self._sub
            phi = torch.cat(phis)                                        # [T, sensors, d]
            if base is None:
                base = torch.cat(bs)                                     # [T, N, 12]
            del phis, bs
            if cuda:
                torch.cuda.synchronize()
            seconds['forward'] += time.time() - t0
            t0 = time.time()
            for a in range(cols.start, cols.stop, part):
                c = slice(a, min(a + part, cols.stop))
                P = phi[:, c.start - lo:c.stop - lo].transpose(0, 1).to(torch.float64)                       # [c, T, d]
                yy = y[:, c].transpose(0, 1).to(device)
                tv = g.target_valid(yy).to(torch.float64)                                                    # [c, T, 12]
                w = g.window_valid(yy).to(torch.float64)                                                     # [c, T]: the rows of the fit
                r = (yy.to(torch.float64) - base[:, c].transpose(0, 1).to(device).to(torch.float64)) / scale
                Pw = P * w.unsqueeze(-1)
                tr, ho = slice(0, cut), slice(cut, T)
                gram = {k: Pw[:, sl].transpose(1, 2) @ P[:, sl] for k, sl in (('tr', tr), ('ho', ho))}
                rhs = {k: Pw[:, sl].transpose(1, 2) @ r[:, sl] for k, sl in (('tr', tr), ('ho', ho))}
                gram['all'], rhs['all'] = gram['tr'] + gram['ho'], rhs['tr'] + rhs['ho']
                ids = np.arange(c.start, c.stop)
                acc['hold_cnt'][ids] = tv[:, ho].sum((1, 2)).cpu().numpy()
                acc['hold_abs0'][ids] = (r[:, ho].abs() * tv[:, ho]).sum((1, 2)).cpu().numpy() * scale
                both = tv * w.unsqueeze(-1)
                acc['all_cnt'][ids] = both.sum((1, 2)).cpu().numpy()
                acc['all_abs0'][ids] = (r.abs() * both).sum((1, 2)).cpu().numpy() * scale
                acc['windows'][ids] = w.sum(1).cpu().numpy()

                def system(k, strength):
                    G = gram[k]
                    level = G.diagonal(dim1=1, dim2=2)[:, :-1].mean(1) if d > 1 else G.new_zeros(len(G))
                    return G + ((strength * level + 1e-8)[:, None, None] * penalty.diag()) + (1e-9 * (level + 1.))[:, None, None] * eye

                for i, strength in enumerate(RIDGES):
                    th = torch.cholesky_solve(rhs['tr'], torch.linalg.cholesky(system('tr', strength)))
                    acc['hold_abs'][i, ids] = ((r[:, ho] - P[:, ho] @ th).abs() * tv[:, ho]).sum((1, 2)).cpu().numpy() * scale
                    chol = torch.linalg.cholesky(system('all', strength))
                    th = torch.cholesky_solve(rhs['all'], chol)
                    lever = torch.linalg.solve_triangular(chol, Pw.transpose(1, 2), upper=False).pow(2).sum(1)       # [c, T]
                    err = r - P @ th
                    acc['fit_abs'][i, ids] = (err.abs() * both).sum((1, 2)).cpu().numpy() * scale
                    acc['loo_abs'][i, ids] = ((err / (1. - lever).clamp_min(1e-6).unsqueeze(-1)).abs() * both).sum((1, 2)).cpu().numpy() * scale
                    theta[i, ids] = (th * scale).to(torch.float32).cpu()
                del P, Pw, gram, rhs, r, yy, tv, w, both
            del phi
            if cuda:
                torch.cuda.synchronize()
                torch.cuda.empty_cache()
            seconds['solve'] += time.time() - t0
        hold = acc['hold_abs'].sum(1) / max(acc['hold_cnt'].sum(), 1.)
        pick = int(np.argmin(hold))
        mae = lambda v, cnt: float(v.sum() / max(cnt.sum(), 1.))
        self.info[variant] = dict(
            place=place, features=int(d), fit_windows=int(T), holdout_windows=int(T - cut), ridges=list(RIDGES), selected_ridge=RIDGES[pick],
            ridge_on_grid_boundary=bool(pick in (0, L - 1)), holdout_mae=[float(v) for v in hold], holdout_mae_no_update=mae(acc['hold_abs0'], acc['hold_cnt']),
            loo_mae=[mae(acc['loo_abs'][i], acc['all_cnt']) for i in range(L)], fit_mae=[mae(acc['fit_abs'][i], acc['all_cnt']) for i in range(L)],
            fit_mae_no_update=mae(acc['all_abs0'], acc['all_cnt']), trained_values=int(n * d * g.Y_LEN), sensor_groups=int(-(-n // group)),
            forward_passes_over_fit_windows=int(-(-n // group)), seconds_forward=seconds['forward'], seconds_solve=seconds['solve'],
            seconds=time.time() - began, peak_gpu_gib=torch.cuda.max_memory_allocated() / 2 ** 30 if cuda else None, bounded=bool(BOUNDED))
        self.arrays[variant] = dict(acc, ridges=np.asarray(RIDGES), selected=np.asarray(pick))
        self._theta[variant] = theta[pick].to(device).contiguous()
        return self._theta[variant]

    def _forward(self, key, x_raw, device, sub):
        base, ckpt, norm, variant = key
        if not str(variant).startswith('cf_'):
            return super()._forward(key, x_raw, device, sub)
        place = variant[3:].split('@')[0]
        theta = self.closed(variant, device)
        x, out = g.normalize_x(x_raw, *self.norm[norm]).to(device), []
        for i in range(0, len(x), sub):
            b, phi = self.feats(place, x[i:i + sub], device)
            out.append(b + torch.einsum('bnd,ndh->bnh', phi.to(torch.float32), theta))
        return torch.cat(out).to(torch.float32).to(self.cache_device(device))


class ClosedBundle(Closed, e16.BudgetBundle if BUDGET else e10.RefreshBundle):
    pass


def arms_of(B, seed):
    B.seed = seed
    arm = lambda name, ckpt, variant: dict(name=name, base='stae', ckpt=ckpt, norm=ckpt, age=B.year - ckpt, variant=variant)
    arms = [arm('same', B.year, 'full'), arm('stale5o', B.old, 'full')]
    if BUDGET:
        return arms + [arm('fit_emb', B.old, 'fit@%d' % e3.FIT_WINDOWS)] + [arm('cf_' + p, B.old, 'cf_%s@%d' % (p, e3.FIT_WINDOWS)) for p in PLACES]
    return arms + [arm('cf_' + p, B.old, 'cf_' + p) for p in PLACES]


def check_reference(B, seed, arms, weights, adj, device):
    return e5.check_reference(B, seed, [a for a in arms if a.get('variant') == 'full'], weights, adj, device)


e3.Bundle = ClosedBundle
e3.arms_of = arms_of
e3.check_reference = check_reference


def budget_main():
    """The loop of e16_budget.main with the bundle class and the arms of this file."""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--bundle', required=True)
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--device', default='auto')
    ap.add_argument('--max-windows', type=int, default=0, help='a bounded check only')
    opt = ap.parse_args()
    budgets = [int(b) for b in os.environ.get('EVOST_CLOSED_BUDGETS', '').split()] or list(e16.BUDGETS)
    out = Path(opt.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    device = torch.device('cuda:0' if (opt.device == 'auto' and torch.cuda.is_available()) else ('cpu' if opt.device == 'auto' else opt.device))
    start = time.time()
    B = ClosedBundle(opt.bundle)
    assert opt.seed in B.meta['seeds']
    bounded = bool(opt.max_windows or tuple(budgets) != e16.BUDGETS or e10.FIT['epochs'] != 16)
    for b in budgets:
        e16.set_budget(b)
        sub, began = out / ('b%d' % b), time.time()
        sub.mkdir()
        with torch.no_grad():
            rows, arms, reference, extra = e3.run(B, opt.seed, device, opt.max_windows, sub)
        with (sub / 'e3_metrics.jsonl').open('w') as f:
            for row in rows:
                f.write(json.dumps(dict(row, budget=b), allow_nan=False) + '\n')
        g.save_json(sub / 'e3_setup.json', dict(dataset=B.meta['dataset'], year=B.year, seed=opt.seed, nodes=B.n, budget=b, fit_windows=e3.FIT_WINDOWS,
            select_windows=e3.SELECT_WINDOWS, fit_holdout=e10.FIT['holdout'], arms=arms, reference_check=reference, device=str(device),
            gpu=torch.cuda.get_device_name(0) if device.type == 'cuda' else None, torch=torch.__version__, max_windows=opt.max_windows, **extra))
        g.save_json(sub / 'completed.json', dict(status='completed', rows=len(rows), seconds=time.time() - began, bounded_smoke=bounded, budget=b))
        print(json.dumps(dict(status='budget_completed', budget=b, seconds=round(time.time() - began, 1))), flush=True)
    B.info.update(sensors=B.n, budgets=budgets)
    (out / 'closed_info.json').write_text(json.dumps(B.info, indent=2) + '\n')
    for variant, arrays in B.arrays.items():
        np.savez_compressed(out / ('closed_%s_b%s.npz' % tuple(variant[3:].split('@'))), **arrays)
    g.save_json(out / 'completed.json', dict(status='completed', budgets=budgets, seconds=time.time() - start, bounded_smoke=bounded))
    print(json.dumps(dict(status='closed_budget_completed', dataset=B.meta['dataset'], year=B.year, seed=opt.seed, nodes=B.n, seconds=round(time.time() - start, 1))), flush=True)


if __name__ == '__main__':
    torch.manual_seed(0)
    torch.use_deterministic_algorithms(True, warn_only=True)
    if BUDGET:
        budget_main()
        sys.exit(0)
    e3.main()
    out = Path(sys.argv[sys.argv.index('--out') + 1]).resolve()
    B = e10.RefreshBundle.last
    B.info.update(sensors=B.n)
    (out / 'closed_info.json').write_text(json.dumps(B.info, indent=2) + '\n')
    for variant, arrays in B.arrays.items():
        np.savez_compressed(out / ('closed_%s.npz' % variant[3:]), **arrays)
