"""Reads the EvoST runs of pilot.evost_run and compares them with the saved records of the upstream tree
(Survey/experiments/evost-plan.md, Sections 3.2 to 3.4).  No GPU.

  python -m pilot.evost_compare [--periods pems06:2020 pems06:2025 pems03:2020 pems03:2025] [--seeds 51 52 53]

Measure: the calibrated MAE over the steps 1 to 12 (H12) on the test portion, all sensors.  The ratio of an arm is the mean
of its MAE over the seeds, divided by the same mean of the reference (the checkpoint of the target year).
Writes results/evost/compare/reproduction.md and reproduction.json: the ratios against the records, the line of the
reproduction, the seed spread, the cost of each arm in seconds on the GPU unit of the runs, and the two parts of the headroom.
A period or a seed with no finished run is left out and named.
"""
import argparse
import json
import math
import statistics
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
UP = REPO.parent / 'EvoST'
ARMS = (('same', 'Reference', 'maintenance'), ('stale5o', 'Old', 'maintenance'), ('fit_head', 'Head', 'maintenance'),
        ('fit_prompt', 'Prompt', 'prompt'), ('fit_scratch', 'Scratch', 'prompt'), ('fit_shared', 'Shared', 'maintenance'),
        ('fit_emb_sel', 'EvoST', 'maintenance'), ('fit_all', 'Full fine-tuning', 'maintenance'))
FITS = (('fit_head', 'Head', 'maintenance'), ('fit_shared', 'Shared', 'maintenance'), ('fit_emb_sel', 'EvoST', 'maintenance'),
        ('fit_all', 'Full fine-tuning', 'maintenance'), ('fit_prompt', 'Prompt', 'prompt'), ('fit_scratch', 'Scratch', 'prompt'))
RECORD_DIRS = dict(maintenance=('parameter_groups', 'mnt'), prompt=('prompt_and_scratch', 'eac'))


def metrics(path):
    """arm -> (calibrated, uncalibrated) H12 MAE on the test portion, all sensors."""
    out = {}
    if not path.is_file():
        return out
    for line in path.read_text().splitlines():
        r = json.loads(line)
        if r.get('portion') == 'test' and r.get('cohort') == 'all':
            out[r['arm']] = (r['calibrated']['H12_MAE'], r['uncalibrated']['H12_MAE'])
    return out


def ours(district, year, study, seed):
    folder = REPO / 'results' / 'evost' / ('%s_%d' % (district, year)) / ('%s_s%d' % (study, seed))
    return folder if (folder / 'completed.json').is_file() else None


def record(district, year, study, seed):
    group, tag = RECORD_DIRS[study]
    name = district.upper()
    return UP / 'results' / 'evost' / group / 'runs' / ('%s-%s-%d-s%d' % (tag, name, year, seed)) / ('%s_%d' % (name, year)) / ('seed%d' % seed)


def mean(v):
    return sum(v) / len(v) if v else float('nan')


def sd(v):
    return statistics.stdev(v) if len(v) > 1 else float('nan')


def geo(v):
    v = [x for x in v if x == x]
    return math.exp(mean([math.log(x) for x in v])) if v else float('nan')


def fmt(x, digits=3):
    return '-' if x != x else ('%.' + str(digits) + 'f') % x


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--periods', nargs='+', default=['pems06:2020', 'pems06:2025', 'pems03:2020', 'pems03:2025'])
    ap.add_argument('--seeds', type=int, nargs='+', default=[51, 52, 53])
    opt = ap.parse_args()
    periods = [(p.split(':')[0], int(p.split(':')[1])) for p in opt.periods]
    data, lines, absent = {}, [], []
    for d, y in periods:
        cell = dict(ours={}, records={}, fits={}, seeds=[])
        for seed in opt.seeds:
            o, r = {}, {}
            for study in ('maintenance', 'prompt'):
                folder = ours(d, y, study, seed)
                if folder is None:
                    absent.append('%s %d %s seed %d' % (d, y, study, seed))
                    continue
                o.update({k: v for k, v in metrics(folder / 'e3_metrics.jsonl').items() if k not in o})
                info = json.loads((folder / 'e10_info.json').read_text())
                for key, label, st in FITS:
                    if st == study and key in info:
                        f = info[key]
                        cell['fits'].setdefault(label, []).append(dict(seconds=f['seconds'], seconds_per_epoch=f.get('seconds_per_epoch'), epochs=f.get('epochs_run'),
                                                                       peak_gpu_gib=f.get('peak_gpu_gib'), trained_values=f.get('trained_values')))
                cell.setdefault('run_seconds', {}).setdefault(study, []).append(json.loads((folder / 'completed.json').read_text())['seconds'])
                r.update({k: v for k, v in metrics(record(d, y, study, seed) / 'e3_metrics.jsonl').items() if k not in r})
            if 'same' in o:
                cell['ours'][seed], cell['seeds'] = o, cell['seeds'] + [seed]
            if 'same' in r:
                cell['records'][seed] = r
        cell['train'] = {}
        for f in sorted((REPO / 'results' / 'evost' / d / 'train').glob('*_s*.json')):
            t = json.loads(f.read_text())
            cell['train'].setdefault(int(t['year']), []).append(dict(seed=t['seed'], seconds=t['train_seconds'], epochs=t['epochs'], seconds_per_epoch=t['seconds_per_epoch'],
                                                                     peak_gpu_gib=t['peak_gpu_gib'], sensors=t['sensors'], gpu=t['gpu']))
        data[(d, y)] = cell

    def ratio(side, d, y, arm):
        runs = data[(d, y)][side]
        seeds = [s for s in runs if arm in runs[s] and 'same' in runs[s]]
        return mean([runs[s][arm][0] for s in seeds]) / mean([runs[s]['same'][0] for s in seeds]) if seeds else float('nan')

    lines += ['# EvoST: our runs against the saved records of the upstream tree', '',
              'Measure: calibrated test MAE over the steps 1 to 12, all sensors. A ratio is the mean of an arm over the seeds, divided by the same mean of the reference.', '']
    lines += ['## Ratios to the reference', '', '| Period | Seeds | Side | Reference MAE (SD) | ' + ' | '.join(label for _, label, _ in ARMS[1:]) + ' |', '|---|---|---|---|' + '---|' * (len(ARMS) - 1)]
    for d, y in periods:
        for side, name in (('ours', 'ours'), ('records', 'records')):
            runs = data[(d, y)][side]
            ref = [runs[s]['same'][0] for s in runs]
            lines.append('| %s, %d | %s | %s | %s (%s) | ' % (d.upper(), y, ' '.join(str(s) for s in sorted(runs)) or '-', name, fmt(mean(ref)), fmt(sd(ref)))
                         + ' | '.join(fmt(ratio(side, d, y, arm)) for arm, _, _ in ARMS[1:]) + ' |')
    full = [p for p in periods if len(data[p]['ours']) == len(opt.seeds)]
    lines.append('| Geometric mean, %d periods with every seed | | ours | | ' % len(full) + ' | '.join(fmt(geo([ratio('ours', d, y, arm) for d, y in full])) for arm, _, _ in ARMS[1:]) + ' |')
    lines.append('| Geometric mean, the same periods | | records | | ' + ' | '.join(fmt(geo([ratio('records', d, y, arm) for d, y in full])) for arm, _, _ in ARMS[1:]) + ' |')

    # the line of the reproduction (plan, Section 3.2)
    ref_ok = [abs(mean([v['same'][0] for v in data[p]['ours'].values()]) / mean([v['same'][0] for v in data[p]['records'].values()]) - 1) <= 0.05 for p in full if data[p]['records']]
    gaps = {label: abs(geo([ratio('ours', d, y, arm) for d, y in full]) - geo([ratio('records', d, y, arm) for d, y in full])) for arm, label, _ in ARMS[1:]}
    order = [ratio('ours', d, y, 'stale5o') > ratio('ours', d, y, 'fit_head') > ratio('ours', d, y, 'fit_shared') > ratio('ours', d, y, 'fit_emb_sel') for d, y in full]
    need = max(1, math.ceil(0.75 * len(periods)))
    complete = len(full) == len(periods)
    clauses = [('Reference MAE within 5 % of the record', sum(ref_ok), sum(ref_ok) >= need),
               ('Geometric mean within 0.03 for Old (difference %s)' % fmt(gaps['Old']), None, gaps['Old'] <= 0.03),
               ('Geometric mean within 0.02 for EvoST (difference %s)' % fmt(gaps['EvoST']), None, gaps['EvoST'] <= 0.02),
               ('Geometric mean within 0.02 for full fine-tuning (difference %s)' % fmt(gaps['Full fine-tuning']), None, gaps['Full fine-tuning'] <= 0.02),
               ('Order Old > Head > Shared > EvoST', sum(order), sum(order) >= need)]
    lines += ['', '## The line of the reproduction', '', '| Clause | Periods that hold | Holds |', '|---|---|---|']
    lines += ['| %s | %s | %s |' % (c, '-' if k is None else '%d of %d' % (k, len(full)), 'yes' if ok else 'no') for c, k, ok in clauses]
    verdict = ('pass' if all(ok for _, _, ok in clauses) else 'fail') if complete else 'not complete: %d of %d periods have every seed' % (len(full), len(periods))
    lines += ['', 'Line: **%s**.' % verdict]

    # the seed spread and Part B of the headroom
    lines += ['', '## Seed spread, and the interval between Old and EvoST', '', '| Period | SD of Old (MAE) | SD of EvoST (MAE) | Pooled SD | Old minus EvoST (MAE) | Interval in pooled SD |', '|---|---|---|---|---|---|']
    part_b = []
    for d, y in periods:
        runs = data[(d, y)]['ours']
        old, evo = [runs[s]['stale5o'][0] for s in runs if 'stale5o' in runs[s]], [runs[s]['fit_emb_sel'][0] for s in runs if 'fit_emb_sel' in runs[s]]
        pooled = math.sqrt((sd(old) ** 2 + sd(evo) ** 2) / 2) if len(old) > 1 and len(evo) > 1 else float('nan')
        units = (mean(old) - mean(evo)) / pooled if pooled == pooled and pooled > 0 else float('nan')
        part_b.append(units)
        lines.append('| %s, %d | %s | %s | %s | %s | %s |' % (d.upper(), y, fmt(sd(old)), fmt(sd(evo)), fmt(pooled), fmt(mean(old) - mean(evo)), fmt(units, 1)))
    b_hold = sum(1 for u in part_b if u == u and u > 2)
    lines += ['', 'Part B of the headroom (the interval is above two pooled SD at three of four periods): %d of %d periods hold.' % (b_hold, len(periods))]

    # the cost of each arm, and Part A of the headroom
    lines += ['', '## Cost at the period, in seconds on the GPU unit of the runs (mean over the seeds)', '',
              '| Period | Training on 31 days (epochs) | ' + ' | '.join('%s, three fits' % label for _, label, _ in FITS) + ' | EvoST / training | Run of `maintenance` | Run of `prompt` |', '|---|---|' + '---|' * (len(FITS) + 3)]
    share = {}
    for d, y in periods:
        cell = data[(d, y)]
        tr = cell['train'].get(y, [])
        fits = {label: mean([f['seconds'] for f in cell['fits'].get(label, [])]) for _, label, _ in FITS}
        share[(d, y)] = fits['EvoST'] / mean([t['seconds'] for t in tr]) if tr else float('nan')
        lines.append('| %s, %d | %s (%s) | ' % (d.upper(), y, fmt(mean([t['seconds'] for t in tr]), 0), fmt(mean([t['epochs'] for t in tr]), 0)) + ' | '.join(fmt(fits[label], 0) for _, label, _ in FITS)
                     + ' | %s | %s | %s |' % (fmt(share[(d, y)], 2), fmt(mean(cell.get('run_seconds', {}).get('maintenance', [])), 0), fmt(mean(cell.get('run_seconds', {}).get('prompt', [])), 0)))
    lines += ['', '## Training of each checkpoint', '', '| District | Year | Sensors | Seeds | Seconds (SD) | Epochs | Seconds per epoch | Peak GPU memory (GiB) | GPU unit |', '|---|---|---|---|---|---|---|---|---|']
    for d in sorted({p[0] for p in periods}):
        years = {}
        for p in periods:
            if p[0] == d:
                years.update(data[p]['train'])
        for y in sorted(years):
            t = years[y]
            lines.append('| %s | %d | %d | %s | %s (%s) | %s | %s | %s | %s |' % (d.upper(), y, t[0]['sensors'], ' '.join(str(x['seed']) for x in t), fmt(mean([x['seconds'] for x in t]), 0),
                         fmt(sd([x['seconds'] for x in t]), 0), fmt(mean([x['epochs'] for x in t]), 1), fmt(mean([x['seconds_per_epoch'] for x in t]), 1),
                         fmt(max(x['peak_gpu_gib'] or float('nan') for x in t), 1), t[0]['gpu']))
    if absent:
        lines += ['', 'Runs that are absent: ' + '; '.join(absent) + '.']
    target = REPO / 'results' / 'evost' / 'compare'
    target.mkdir(parents=True, exist_ok=True)
    (target / 'reproduction.md').write_text('\n'.join(lines) + '\n')
    (target / 'reproduction.json').write_text(json.dumps(dict(periods=opt.periods, seeds=opt.seeds, line=verdict, part_b=part_b, refresh_share_of_training={'%s:%d' % k: v for k, v in share.items()},
                                                               ratios={'%s:%d' % (d, y): {label: ratio('ours', d, y, arm) for arm, label, _ in ARMS[1:]} for d, y in periods}), indent=1) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
