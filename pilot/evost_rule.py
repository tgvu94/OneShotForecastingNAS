"""Reads the history-budget runs of pilot/evost_closed.py and tests a rule that chooses the action of a period
(Survey/experiments/evost-plan.md, the oracle test of the rule).  No GPU.

  python -m pilot.evost_rule [--periods pems06:2020 pems06:2025 pems03:2020 pems03:2025] [--seeds 51 52 53]

A cell is a period and a history budget (64, 256, 1,024 or 2,048 windows).  The actions of a cell: no update (`stale5o`), the
closed-form update (`cf_proj`), the gradient refresh (`fit_emb`), and `mix`: per sensor, the closed-form update where its
leave-one-out error is below the error with no update, and no update at the other sensors.  The calibrator is per sensor, so
the error of `mix` comes from the sums per sensor of the two runs with no new run.
Measure: calibrated test MAE over the steps 1 to 12, all sensors; the ratio of an action in a cell is its mean over the seeds,
divided by the same mean of the reference of that budget.
The oracle reads the test error and takes the best action of each cell.  A rule reads only numbers of the fit:
  Q   the leave-one-out error of the closed-form update over all sensors, divided by the error with no update;
  S   the share of sensors whose leave-one-out error is not below their error with no update.
Rule `share` (the form of the plan): the gradient refresh runs when S is above a threshold; `mix` runs in the other runs.
Rule `gain`: the gradient refresh runs when Q is below a threshold; `mix` runs in the other runs.
The threshold of a rule is fit on the runs of one district (lowest geometric mean of the ratio; the larger count of runs with
no gradient refresh on a tie) and applied to the other district.
The line: the rule is within one seed SD of the oracle in the geometric mean, the gradient refresh runs in fewer runs than
"always refresh", and the rule is not above "always refresh".
Writes results/evost/compare/rule.md and rule.json.
"""
import argparse
import json
import statistics

import numpy as np

from pilot.evost_compare import REPO, fmt, geo, mean, ours

BUDGETS = (64, 256, 1024, 2048)
ACTIONS = (('stale5o', 'No update'), ('cf_proj', 'Closed form'), ('mix', 'Closed form where the leave-one-out error falls'), ('fit_emb', 'Gradient refresh'))


def load(folder, budget):
    """One run of one budget: MAE of each action, the statistics of the fit and the seconds of the two fits."""
    sums = np.load(folder / ('b%d' % budget) / 'e3_sums.npz')
    node = {a: sums['test/%s/cal/node' % a] for a in ('same', 'stale5o', 'cf_proj', 'fit_emb')}          # [sensors, (abs, sq, count)]
    fit = np.load(folder / ('closed_proj_b%d.npz' % budget))
    pick = int(fit['selected'])
    loo, none = fit['loo_abs'][pick], fit['all_abs0']
    use = loo < none                                                     # sensors where the fit predicts a gain
    info = json.loads((folder / 'closed_info.json').read_text())
    mae = {a: float(v[:, 0].sum() / max(v[:, 2].sum(), 1.)) for a, v in node.items()}
    mae['mix'] = float((np.where(use, node['cf_proj'][:, 0], node['stale5o'][:, 0]).sum()) / max(node['stale5o'][:, 2].sum(), 1.))
    known = none > 0
    return dict(mae=mae, Q=float(loo.sum() / max(none.sum(), 1e-12)), S=float(1. - use[known].mean()) if known.any() else 1.,
                seconds=dict(cf=info['cf_proj@%d' % budget]['seconds'], grad=info['fit@%d' % budget]['seconds']))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--periods', nargs='+', default=['pems06:2020', 'pems06:2025', 'pems03:2020', 'pems03:2025'])
    ap.add_argument('--seeds', type=int, nargs='+', default=[51, 52, 53])
    opt = ap.parse_args()
    periods = [(p.split(':')[0], int(p.split(':')[1])) for p in opt.periods]
    runs, absent = {}, []
    for d, y in periods:
        for seed in opt.seeds:
            folder = ours(d, y, 'closed_budget', seed)
            if folder is None:
                absent.append('%s %d seed %d' % (d, y, seed))
                continue
            for b in BUDGETS:
                runs[(d, y, b, seed)] = load(folder, b)
    cells = [(d, y, b) for d, y in periods for b in BUDGETS if all((d, y, b, s) in runs for s in opt.seeds)]
    name = lambda c: '%s, %d, %d windows' % (c[0].upper(), c[1], c[2])

    def ratio(cell, choose, seeds=None):
        """choose(run) -> the action of a run."""
        seeds = seeds or opt.seeds
        rs = [runs[cell + (s,)] for s in seeds]
        return mean([r['mae'][choose(r)] for r in rs]) / mean([r['mae']['same'] for r in rs])

    fixed = {a: {c: ratio(c, lambda r, a=a: a) for c in cells} for a, _ in ACTIONS}
    best = {c: min((a for a, _ in ACTIONS), key=lambda a: fixed[a][c]) for c in cells}
    oracle = lambda cs: geo([fixed[best[c]][c] for c in cs])

    def rule(kind, threshold):
        return (lambda r: 'fit_emb' if r['S'] > threshold else 'mix') if kind == 'share' else (lambda r: 'fit_emb' if r['Q'] < threshold else 'mix')

    def fit(kind, district):
        """The threshold from the runs of one district."""
        own = [c for c in cells if c[0] == district]
        values = sorted({runs[c + (s,)]['S' if kind == 'share' else 'Q'] for c in own for s in opt.seeds})
        grid = [-np.inf] + [(a + b) / 2 for a, b in zip(values, values[1:])] + [np.inf]
        score = lambda t: (round(geo([ratio(c, rule(kind, t)) for c in own]), 6),
                           sum(rule(kind, t)(runs[c + (s,)]) == 'fit_emb' for c in own for s in opt.seeds))
        return min(grid, key=score) if own else np.inf

    districts = sorted({c[0] for c in cells})
    lines = ['# A rule for the action of a period, against the oracle', '',
             'Measure: calibrated test MAE over the steps 1 to 12, all sensors. A ratio is the mean of an action over the seeds, divided by the same mean of the reference of that budget.', '',
             '## Ratio of each action in each cell', '',
             '| Cell | ' + ' | '.join(label for _, label in ACTIONS) + ' | Best action | Q (seeds) | S (seeds) |', '|---' * (len(ACTIONS) + 4) + '|']
    for c in cells:
        rs = [runs[c + (s,)] for s in opt.seeds]
        lines.append('| %s | ' % name(c) + ' | '.join(fmt(fixed[a][c]) for a, _ in ACTIONS) + ' | %s | %s | %s |' % (
            dict(ACTIONS)[best[c]], ' '.join(fmt(r['Q'], 2) for r in rs), ' '.join(fmt(r['S'], 2) for r in rs)))
    out = dict(periods=opt.periods, seeds=opt.seeds, absent=absent, cells=len(cells))
    if cells and len(districts) == 2:
        per_seed = [geo([ratio(c, lambda r, c=c: best[c], [s]) for c in cells]) for s in opt.seeds]
        spread = statistics.stdev(per_seed) if len(per_seed) > 1 else float('nan')
        total = len(cells) * len(opt.seeds)
        seconds = lambda choose: mean([runs[c + (s,)]['seconds']['cf'] * (choose(runs[c + (s,)]) in ('mix', 'cf_proj'))
                                       + runs[c + (s,)]['seconds']['grad'] * (choose(runs[c + (s,)]) == 'fit_emb') for c in cells for s in opt.seeds])
        table = [('Oracle (reads the test error)', oracle(cells), sum(best[c] == 'fit_emb' for c in cells) * len(opt.seeds), float('nan'), '')]
        for a, label in ACTIONS:
            table.append(('Always: ' + label.lower(), geo([fixed[a][c] for c in cells]), total if a == 'fit_emb' else 0, seconds(lambda r, a=a: a), ''))
        verdicts = {}
        for kind in ('share', 'gain'):
            thresholds = {d: fit(kind, d) for d in districts}
            other = {districts[0]: districts[1], districts[1]: districts[0]}
            choose = {c: rule(kind, thresholds[other[c[0]]]) for c in cells}
            value = geo([ratio(c, choose[c]) for c in cells])
            count = sum(choose[c](runs[c + (s,)]) == 'fit_emb' for c in cells for s in opt.seeds)
            cost = mean([runs[c + (s,)]['seconds']['cf'] + runs[c + (s,)]['seconds']['grad'] * (choose[c](runs[c + (s,)]) == 'fit_emb') for c in cells for s in opt.seeds])
            note = '; '.join('threshold from %s: %s' % (d.upper(), fmt(t, 3)) for d, t in thresholds.items())
            table.append(('Rule `%s`, threshold from the other district' % kind, value, count, cost, note))
            always = geo([fixed['fit_emb'][c] for c in cells])
            verdicts[kind] = dict(ratio=value, oracle=oracle(cells), seed_sd=spread, gradient_runs=int(count), runs=total, always_refresh=always,
                                  thresholds={d: float(t) for d, t in thresholds.items()},
                                  passed=bool(value - oracle(cells) <= spread and count < total and value <= always))
        lines += ['', '## Geometric mean over the %d cells' % len(cells), '',
                  '| Policy | Ratio | Runs with a gradient refresh (of %d) | Fit seconds per run | Note |' % total, '|---|---|---|---|---|']
        lines += ['| %s | %s | %d | %s | %s |' % (label, fmt(v), n, fmt(sec, 1), note) for label, v, n, sec, note in table]
        lines += ['', 'Seed SD of the oracle (geometric mean per seed): %s.' % fmt(spread, 4), '']
        for kind, v in verdicts.items():
            lines.append('Rule `%s`: %s above the oracle (the line: one seed SD); gradient refresh in %d of %d runs; "always refresh" is %s. Line: **%s**.' % (
                kind, fmt(v['ratio'] - v['oracle'], 4), v['gradient_runs'], v['runs'], fmt(v['always_refresh']), 'pass' if v['passed'] else 'fail'))
        out.update(rules=verdicts, oracle=oracle(cells), seed_sd=spread)
    if absent:
        lines += ['', 'No finished run: ' + '; '.join(absent) + '.']
    out['ratios'] = {'%s:%d:%d' % c: {a: fixed[a][c] for a, _ in ACTIONS} for c in cells}
    target = REPO / 'results' / 'evost' / 'compare'
    target.mkdir(parents=True, exist_ok=True)
    (target / 'rule.md').write_text('\n'.join(lines) + '\n')
    (target / 'rule.json').write_text(json.dumps(out, indent=2) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
