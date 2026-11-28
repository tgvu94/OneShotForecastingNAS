"""Reads the closed-form runs of pilot/evost_closed.py next to the maintenance runs of the same period and seed
(Survey/experiments/evost-plan.md, the oracle test of the closed-form update).  No GPU.

  python -m pilot.evost_closed_compare [--periods pems06:2020 pems06:2025 pems03:2020 pems03:2025] [--seeds 51 52 53]

Measure: the calibrated MAE over the steps 1 to 12 (H12) on the test portion, all sensors; a ratio is the mean of an arm over
the seeds, divided by the same mean of the reference of the maintenance run.  The recovered share of an arm is
(Old - arm) / (Old - EvoST).  The line: at the feature place with the lowest geometric mean, the share is at least one half in
the geometric mean and at three of four periods.
Writes results/evost/compare/closed.md and closed.json.  A period or a seed with no finished run is left out and named.
"""
import argparse
import json

from pilot.evost_compare import REPO, fmt, geo, mean, metrics, ours

PLACES = (('cf_proj', 'Values in front of the output projection'), ('cf_last', 'Values in front of the last linear layer'),
          ('cf_calib', 'Input-side features of the calibrator'))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--periods', nargs='+', default=['pems06:2020', 'pems06:2025', 'pems03:2020', 'pems03:2025'])
    ap.add_argument('--seeds', type=int, nargs='+', default=[51, 52, 53])
    opt = ap.parse_args()
    periods = [(p.split(':')[0], int(p.split(':')[1])) for p in opt.periods]
    data, absent, drift = {}, [], 0.
    for d, y in periods:
        cell = dict(runs={}, info={}, evost=[])
        for seed in opt.seeds:
            m, c = ours(d, y, 'maintenance', seed), ours(d, y, 'closed', seed)
            if m is None or c is None:
                absent.append('%s %d seed %d' % (d, y, seed))
                continue
            row = {k: v for k, v in metrics(m / 'e3_metrics.jsonl').items() if k in ('same', 'stale5o', 'fit_emb_sel')}
            mine = metrics(c / 'e3_metrics.jsonl')
            for k in ('same', 'stale5o'):                               # the two arms that both runs hold: they must agree
                drift = max(drift, abs(mine[k][0] / row[k][0] - 1.))
            row.update({k: mine[k] for k, _ in PLACES if k in mine})
            cell['runs'][seed] = row
            info = json.loads((c / 'closed_info.json').read_text())
            for k, _ in PLACES:
                if k in info:
                    cell['info'].setdefault(k, []).append(info[k])
            cell['evost'].append(json.loads((m / 'e10_info.json').read_text())['fit_emb_sel'])
        data[(d, y)] = cell
    full = [p for p in periods if len(data[p]['runs']) == len(opt.seeds)]

    def ratio(p, arm):
        runs = [r for r in data[p]['runs'].values() if arm in r]
        return mean([r[arm][0] for r in runs]) / mean([r['same'][0] for r in runs]) if runs else float('nan')

    def share(old, arm, evost):
        return (old - arm) / (old - evost) if old == old and old != evost else float('nan')

    name = lambda p: '%s, %d' % (p[0].upper(), p[1])
    lines = ['# Closed-form update of the old checkpoint against the gradient refresh', '',
             'Measure: calibrated test MAE over the steps 1 to 12, all sensors. A ratio is the mean of an arm over the seeds, divided by the same mean of the reference. '
             'The share is (Old - arm) / (Old - EvoST).', '',
             '## Ratios to the reference, and the recovered share', '',
             '| Period | Seeds | Old | EvoST | ' + ' | '.join('%s (share)' % label for _, label in PLACES) + ' |', '|---' * (4 + len(PLACES)) + '|']
    for p in periods:
        if not data[p]['runs']:
            continue
        old, ev = ratio(p, 'stale5o'), ratio(p, 'fit_emb_sel')
        lines.append('| %s | %s | %s | %s | ' % (name(p), ' '.join(map(str, sorted(data[p]['runs']))), fmt(old), fmt(ev))
                     + ' | '.join('%s (%s)' % (fmt(ratio(p, k)), fmt(share(old, ratio(p, k), ev), 2)) for k, _ in PLACES) + ' |')
    g_old, g_ev = geo([ratio(p, 'stale5o') for p in full]), geo([ratio(p, 'fit_emb_sel') for p in full])
    g_arm = {k: geo([ratio(p, k) for p in full]) for k, _ in PLACES}
    lines.append('| Geometric mean, %d periods with every seed | | %s | %s | ' % (len(full), fmt(g_old), fmt(g_ev))
                 + ' | '.join('%s (%s)' % (fmt(g_arm[k]), fmt(share(g_old, g_arm[k], g_ev), 2)) for k, _ in PLACES) + ' |')
    verdict = None
    if full:
        best = min(g_arm, key=lambda k: g_arm[k] if g_arm[k] == g_arm[k] else float('inf'))
        g_share = share(g_old, g_arm[best], g_ev)
        hold = sum(share(ratio(p, 'stale5o'), ratio(p, best), ratio(p, 'fit_emb_sel')) >= .5 for p in full)
        need = 3 if len(full) >= 4 else len(full)
        passed = bool(g_share >= .5 and hold >= need and len(full) >= 4)
        verdict = dict(best=best, share_geometric_mean=g_share, periods_with_half=int(hold), periods=len(full), passed=passed)
        lines += ['', '## The line', '', 'Best place: `%s`. Share in the geometric mean: %s (the line: 0.50). Periods with a share of at least one half: %d of %d (the line: three of four).'
                  % (best, fmt(g_share, 2), hold, len(full)), '',
                  'Line: **%s**.' % ('pass' if passed else ('fail' if len(full) >= 4 else 'not complete: fewer than four periods'))]
    lines += ['', 'Largest relative difference of the arms `same` and `stale5o` between a closed-form run and its maintenance run: %.2e.' % drift, '',
              '## The fit, and its cost in seconds on the GPU unit of the runs (mean over the seeds)', '',
              '| Period | Place | Features per sensor | Selected ridge (seeds) | Holdout MAE: no update | Holdout MAE | Leave-one-out MAE | Forward passes | Seconds: forward | Seconds: solve | Seconds: all | Peak GPU memory (GiB) | EvoST, three fits: seconds | EvoST: peak (GiB) |',
              '|---' * 14 + '|']
    for p in periods:
        for k, _ in PLACES:
            rows = data[p]['info'].get(k)
            if not rows:
                continue
            pick = [r['ridges'].index(r['selected_ridge']) for r in rows]
            ev = data[p]['evost']
            lines.append('| %s | `%s` | %d | %s | %s | %s | %s | %d | %s | %s | %s | %s | %s | %s |' % (
                name(p), k, rows[0]['features'], ' '.join('%g' % r['selected_ridge'] for r in rows), fmt(mean([r['holdout_mae_no_update'] for r in rows])),
                fmt(mean([r['holdout_mae'][i] for r, i in zip(rows, pick)])), fmt(mean([r['loo_mae'][i] for r, i in zip(rows, pick)])),
                rows[0]['forward_passes_over_fit_windows'], fmt(mean([r['seconds_forward'] for r in rows]), 1), fmt(mean([r['seconds_solve'] for r in rows]), 1),
                fmt(mean([r['seconds'] for r in rows]), 1), fmt(mean([r['peak_gpu_gib'] or float('nan') for r in rows]), 1),
                fmt(mean([e['seconds'] for e in ev]), 0), fmt(mean([e.get('peak_gpu_gib') or float('nan') for e in ev]), 1)))
    if absent:
        lines += ['', 'No finished pair of runs: ' + '; '.join(absent) + '.']
    target = REPO / 'results' / 'evost' / 'compare'
    target.mkdir(parents=True, exist_ok=True)
    (target / 'closed.md').write_text('\n'.join(lines) + '\n')
    (target / 'closed.json').write_text(json.dumps(dict(
        periods=opt.periods, seeds=opt.seeds, line=verdict, drift=drift, absent=absent,
        ratios={'%s:%d' % p: {k: ratio(p, k) for k in ('stale5o', 'fit_emb_sel') + tuple(k for k, _ in PLACES)} for p in periods if data[p]['runs']}), indent=2) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
