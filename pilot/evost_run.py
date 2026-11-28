"""EvoST with its released code (Survey/experiments/evost-plan.md).  Run with the Python of the EvoST venv
(pilot/evost_setup.sh); the upstream tree is $NAS_ROOT/EvoST and stays unchanged.

  python -m pilot.evost_run metadata   --districts pems03 pems06 --years 2015 2020 2025
  python -m pilot.evost_run checkdata  --districts pems03 pems06 --years 2015 2020 2025
  python -m pilot.evost_run cut        --district pems06 --years 2015 2020 --sensors 20
  python -m pilot.evost_run train      --district pems06 --years 2015 2020 2025 --seeds 42 43 44
  python -m pilot.evost_run export     --district pems06 --years 2020 2025
  python -m pilot.evost_run maintain   --district pems06 --year 2020 --seeds 51 52 53

metadata   writes sensor_metadata.csv per district and year from the catalog of the dataset.
checkdata  compares each full-year matrix with the catalog and with the benchmark cache of the same year (no GPU).
cut        writes a small copy of a district (the first sensors, the first 31 days) under $NAS_DATA_ROOT/evoxxl_cut: a check
           of the code path on a CPU.  --data cut selects it in the other modes; its outputs go to results/evost/cut_<district>.
train      trains the STAEFormer checkpoint of each year and seed with the baseline pipeline of the upstream tree (main.py).
           The configuration is the released file of the district with the values of the recorded configuration of the paper
           runs (experiments/evost/sensor_arrival/stae_conf.json: learning rate, batch size, loss, dropout, gradient clip).
           One process per checkpoint.  A finished checkpoint is skipped; an unfinished one starts again (no resume upstream).
export     writes the maintenance bundles with the exporter of the upstream tree.
maintain   runs the studies `maintenance` and `prompt` of the upstream tree for one period and each evaluation seed.

Outputs: results/evost/<district>/train/<year>_s<seed>.json (seconds, epochs, peak memory, test errors),
results/evost/<district>/data/ (checkpoints, logs, bundles; large), results/evost/<district>_<year>/<study>_s<seed>/ (the
records of the upstream run) and results/evost/<district>_<year>/wall.jsonl (wall-clock seconds per run).
"""
import argparse
import csv
import json
import os
import runpy
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NAS_ROOT = Path(os.environ.get('NAS_ROOT', REPO.parent))
DATA_ROOT = Path(os.environ.get('NAS_DATA_ROOT', NAS_ROOT.parent / 'all_datasets'))
UP = NAS_ROOT / 'EvoST'
ROWS_31_DAYS = 31 * 288
RECIPE_KEYS = ('lr', 'batch_size', 'loss', 'dropout', 'epoch', 'grad_clip', 'warmup_epochs')


def data_dir(kind):
    return DATA_ROOT / ('evoxxl' if kind == 'full' else 'evoxxl_cut')


def out_dir(kind, district):
    return REPO / 'results' / 'evost' / (district if kind == 'full' else 'cut_' + district)


def period_dir(kind, district, year):
    return REPO / 'results' / 'evost' / ('%s_%d' % (district if kind == 'full' else 'cut_' + district, year))


def upstream_commit():
    return subprocess.run(['git', '-C', str(UP), 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()


def catalog():
    entries = json.loads((data_dir('full') / 'hf' / 'full_year' / 'catalog.json').read_text())['entries']
    return {(e['district'].lower(), int(e['year'])): e for e in entries}


def write_metadata(folder, ids):
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / 'sensor_metadata.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['sensor_index', 'node_id'])
        w.writerows((i, s) for i, s in enumerate(ids))


def metadata(opt):
    cat = catalog()
    for d in opt.districts:
        for y in opt.years:
            ids = [str(s) for s in cat[(d, y)]['sensor_ids']]
            assert len(ids) == int(cat[(d, y)]['sensors']) and len(set(ids)) == len(ids), (d, y)
            write_metadata(data_dir('full') / 'sensor_metadata' / d / str(y), ids)
            print('metadata %s %d: %d sensors' % (d, y, len(ids)))


def checkdata(opt):
    import numpy as np
    cat, report = catalog(), {}
    for d in opt.districts:
        for y in opt.years:
            e, base = cat[(d, y)], data_dir('full')
            x = np.load(base / d / 'RawData' / ('%d.npz' % y))['x']
            adj = np.load(base / d / 'graph' / ('%d_adj.npz' % y))['x']
            r = dict(shape=list(x.shape), dtype=str(x.dtype), catalog_slots=int(e['slots']), catalog_sensors=int(e['sensors']), start=e['start'],
                     graph_shape=list(adj.shape), starts_on_1_january=e['start'].startswith('%d-01-01T00:00' % y),
                     nonfinite=int((~np.isfinite(x)).sum()), zero_share_31_days=float((x[:ROWS_31_DAYS] == 0).mean()), zero_share_year=float((x == 0).mean()),
                     days=x.shape[0] / 288)
            r['ok'] = (list(x.shape) == [int(e['slots']), int(e['sensors'])] and adj.shape == (x.shape[1], x.shape[1]) and r['starts_on_1_january'])
            cache = base / 'hf' / 'caches' / d / str(y) / 'data.npz'
            if cache.is_file():
                with np.load(cache, allow_pickle=True) as z:
                    cy, obs, ids, bounds = np.asarray(z['y']), np.asarray(z['observed']).astype(bool), [str(s) for s in z['sensor_ids']], [int(b) for b in z['bounds']]
                same_ids = ids == [str(s) for s in e['sensor_ids']]
                r['cache'] = dict(shape=list(cy.shape), bounds=bounds, same_sensor_order=same_ids, observed_share=float(obs.mean()))
                if same_ids and cy.shape == x[:ROWS_31_DAYS].shape:
                    diff = np.abs(x[:ROWS_31_DAYS].astype(np.float64) - cy.astype(np.float64))[obs]
                    # rows of the full-year matrix that the cache does not accept as targets: these are filled values
                    r['cache'].update(max_abs_diff_where_observed=float(diff.max()) if diff.size else None, share_equal_where_observed=float((diff < 1e-3).mean()) if diff.size else None,
                                      share_of_31_days_not_observed=float(1 - obs.mean()),
                                      train_split_rows_upstream=int(ROWS_31_DAYS * 0.6), train_split_rows_cache=bounds[1])
                r['ok'] = r['ok'] and same_ids
            report['%s_%d' % (d, y)] = r
            print(json.dumps({'%s_%d' % (d, y): r}), flush=True)
    target = REPO / 'results' / 'evost' / 'compare'
    target.mkdir(parents=True, exist_ok=True)
    (target / 'data_check.json').write_text(json.dumps(dict(upstream=upstream_commit(), report=report), indent=1) + '\n')
    print('checkdata ' + ('pass' if all(r['ok'] for r in report.values()) else 'FAIL'))
    return 0 if all(r['ok'] for r in report.values()) else 1


def cut(opt):
    import numpy as np
    cat, d = catalog(), opt.district
    for y in opt.years:
        x = np.load(data_dir('full') / d / 'RawData' / ('%d.npz' % y))['x'][:ROWS_31_DAYS, :opt.sensors]
        adj = np.load(data_dir('full') / d / 'graph' / ('%d_adj.npz' % y))['x'][:opt.sensors, :opt.sensors]
        base = data_dir('cut') / d
        (base / 'RawData').mkdir(parents=True, exist_ok=True)
        (base / 'graph').mkdir(parents=True, exist_ok=True)
        np.savez(base / 'RawData' / ('%d.npz' % y), x=x)
        np.savez(base / 'graph' / ('%d_adj.npz' % y), x=adj)
        fast = base / 'FastData' / ('%d.npz' % y)
        if fast.is_file():
            fast.unlink()
        write_metadata(data_dir('cut') / 'sensor_metadata' / d / str(y), [str(s) for s in cat[(d, y)]['sensor_ids']][:opt.sensors])
        print('cut %s %d: %s' % (d, y, x.shape))


def recipe(district):
    """The released configuration of the district with the recorded values of the paper runs."""
    low, name = district.lower(), district.upper()
    conf = json.loads((UP / 'conf' / name / ('retrain_staeformer_%s.json' % low)).read_text())
    recorded = json.loads((UP / 'experiments' / 'evost' / 'sensor_arrival' / 'stae_conf.json').read_text())[name]
    released = {k: conf.get(k) for k in RECIPE_KEYS}
    for k in RECIPE_KEYS:
        if recorded.get(k) is not None:
            conf[k] = recorded[k]
    return conf, released, {k: recorded.get(k) for k in RECIPE_KEYS}


def checkpoint_folder(kind, district, year, seed):
    return out_dir(kind, district) / 'data' / 'log' / district.upper() / ('retrain_staeformer_%s-%d' % (district.lower(), seed)) / str(year)


def train_one(opt):
    """One checkpoint, in this process: the entry point of the upstream tree runs as released, with a configuration file of ours."""
    d, year, seed, kind = opt.district, opt.year, opt.seed, opt.data
    conf, released, recorded = recipe(d)
    base, root = data_dir(kind) / d, out_dir(kind, d)
    fast = base / 'FastData' / ('%d.npz' % year)
    conf.update(begin_year=year, end_year=year, raw_data_path=str(base / 'RawData') + '/', save_data_path=str(base / 'FastData') + '/',
                graph_path=str(base / 'graph') + '/', model_path=str(root / 'data' / 'log' / d.upper()) + '/', data_process=0 if fast.is_file() else 1, train=1)
    if opt.max_epochs:
        conf['epoch'] = opt.max_epochs
    (root / 'conf').mkdir(parents=True, exist_ok=True)
    (root / 'train').mkdir(parents=True, exist_ok=True)
    conf_path = root / 'conf' / ('%d_s%d.json' % (year, seed))
    conf_path.write_text(json.dumps(conf, indent=1) + '\n')

    import torch
    import torch_geometric.loader as loader
    if opt.workers is not None:                       # the upstream loaders ask for 32 worker processes; a login node gets fewer
        original = loader.DataLoader

        class FewWorkers(original):
            def __init__(self, *a, **k):
                k['num_workers'] = opt.workers
                super().__init__(*a, **k)
        loader.DataLoader = FewWorkers
    os.chdir(UP)
    sys.path.insert(0, str(UP))
    sys.argv = ['main.py', '--conf', str(conf_path), '--gpuid', str(opt.gpuid), '--seed', str(seed)]
    began = time.time()
    g = runpy.run_path(str(UP / 'main.py'), run_name='__main__')
    seconds = time.time() - began
    args = g['args']
    result = args.result
    cuda = torch.cuda.is_available() and opt.gpuid >= 0
    files = sorted(checkpoint_folder(kind, d, year, seed).glob('*.pkl'), key=lambda f: float(f.stem))
    info = dict(district=d, year=year, seed=seed, data=kind, sensors=int(args.graph_size), upstream=upstream_commit(), conf=conf,
                released_recipe=released, recorded_recipe=recorded, workers=opt.workers, bounded=bool(opt.max_epochs),
                train_seconds=float(result[year]['total_time']), seconds_per_epoch=float(result[year]['average_time']), epochs=int(result[year]['epoch_num']),
                wall_seconds=seconds, peak_gpu_gib=(torch.cuda.max_memory_allocated() / 2 ** 30 if cuda else None),
                gpu=(torch.cuda.get_device_name(0) if cuda else None), torch=torch.__version__, host=os.uname().nodename,
                best_checkpoint=files[0].name if files else None, checkpoints_saved=len(files),
                test={h: {m.strip(): float(result[h][m][year]) for m in result[h] if year in result[h][m]} for h in ('3', '6', '12', 'Avg')})
    (root / 'train' / ('%d_s%d.json' % (year, seed))).write_text(json.dumps(info, indent=1) + '\n')
    print('done train %s %d seed %d: %d epochs, %.0f s, T12 MAE %s' % (d, year, seed, info['epochs'], info['train_seconds'], info['test']['12'].get('MAE')), flush=True)


def train(opt):
    failed = 0
    for year in opt.years:
        for seed in opt.seeds:
            record = out_dir(opt.data, opt.district) / 'train' / ('%d_s%d.json' % (year, seed))
            folder = checkpoint_folder(opt.data, opt.district, year, seed)
            if record.is_file() and any(folder.glob('*.pkl')):
                print('skip train %s %d seed %d' % (opt.district, year, seed), flush=True)
                continue
            if folder.is_dir():                       # an unfinished run: the upstream trainer has no resume
                shutil.rmtree(folder, ignore_errors=True)
            folder.parent.mkdir(parents=True, exist_ok=True)   # two jobs of one seed start together: the upstream mkdirs fails on a folder that appears
            cmd = [sys.executable, '-u', '-m', 'pilot.evost_run', 'trainone', '--district', opt.district, '--year', str(year), '--seed', str(seed),
                   '--data', opt.data, '--gpuid', str(opt.gpuid)]
            cmd += (['--max-epochs', str(opt.max_epochs)] if opt.max_epochs else []) + (['--workers', str(opt.workers)] if opt.workers is not None else [])
            if subprocess.run(cmd, cwd=REPO).returncode != 0:
                print('failed train %s %d seed %d' % (opt.district, year, seed), flush=True)
                failed = 1
    return failed


def bundle_path(kind, district, year):
    return out_dir(kind, district) / 'data' / 'bundles' / 'stae' / ('%s_%d.npz' % (district.upper(), year))


def export(opt):
    d, kind = opt.district, opt.data
    todo = [y for y in opt.years if not bundle_path(kind, d, y).is_file()]
    for y in set(opt.years) - set(todo):
        print('skip export %s %d' % (d, y), flush=True)
    if not todo:
        return 0
    cmd = [sys.executable, '-u', str(UP / 'experiments' / 'evost' / 'export_bundles.py'), 'stae', '--dataset', d.upper(),
           '--out', str(bundle_path(kind, d, 0).parent), '--years'] + [str(y) for y in todo]
    cmd += ['--data-root', str(data_dir(kind)), '--model-root', str(out_dir(kind, d) / 'data' / 'log'),
            '--metadata-root', str(data_dir(kind) / 'sensor_metadata'), '--seeds'] + [str(s) for s in opt.seeds]
    return subprocess.run(cmd, cwd=UP).returncode


def maintain(opt):
    d, year, kind, failed = opt.district, opt.year, opt.data, 0
    bundle, root = bundle_path(kind, d, year), period_dir(kind, d, year)
    assert bundle.is_file(), 'no bundle at %s (python -m pilot.evost_run export)' % bundle
    root.mkdir(parents=True, exist_ok=True)
    for seed in opt.seeds:
        for study in opt.studies:
            target = root / ('%s_s%d' % (study, seed))
            if (target / 'completed.json').is_file():
                print('skip %s %s %d seed %d' % (study, d, year, seed), flush=True)
                continue
            if target.exists():                       # the upstream drivers refuse an output folder that exists
                shutil.rmtree(target)
            cmd = [sys.executable, '-u', str(UP / 'experiments' / 'evost' / 'run.py'), study, '--bundle', str(bundle), '--seed', str(seed),
                   '--out', str(target), '--device', opt.device] + (['--max-windows', str(opt.max_windows)] if opt.max_windows else [])
            began = time.time()
            code = subprocess.run(cmd, cwd=UP).returncode
            row = dict(study=study, district=d, year=year, seed=seed, wall_seconds=time.time() - began, returncode=code, device=opt.device,
                       max_windows=opt.max_windows, upstream=upstream_commit(), host=os.uname().nodename, job=os.environ.get('SLURM_JOB_ID'))
            with open(root / 'wall.jsonl', 'a') as f:
                f.write(json.dumps(row) + '\n')
            print(('done' if code == 0 else 'failed') + ' %s %s %d seed %d: %.0f s' % (study, d, year, seed, row['wall_seconds']), flush=True)
            failed = failed or int(code != 0)
    return failed


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = ap.add_subparsers(dest='mode', required=True)
    for name in ('metadata', 'checkdata'):
        p = sub.add_parser(name)
        p.add_argument('--districts', nargs='+', default=['pems03', 'pems06'])
        p.add_argument('--years', type=int, nargs='+', default=[2015, 2020, 2025])
    p = sub.add_parser('cut')
    p.add_argument('--district', required=True)
    p.add_argument('--years', type=int, nargs='+', required=True)
    p.add_argument('--sensors', type=int, default=20)
    for name in ('train', 'trainone', 'export', 'maintain'):
        p = sub.add_parser(name)
        p.add_argument('--district', required=True)
        p.add_argument('--data', choices=('full', 'cut'), default='full')
        if name == 'train':
            p.add_argument('--years', type=int, nargs='+', required=True)
            p.add_argument('--seeds', type=int, nargs='+', default=[42, 43, 44])
        if name == 'trainone':
            p.add_argument('--year', type=int, required=True)
            p.add_argument('--seed', type=int, required=True)
        if name in ('train', 'trainone'):
            p.add_argument('--gpuid', type=int, default=0, help='-1 runs on the CPU')
            p.add_argument('--max-epochs', type=int, default=0, help='a bounded check only')
            p.add_argument('--workers', type=int, default=None, help='worker processes of the upstream loaders (upstream: 32)')
        if name == 'export':
            p.add_argument('--years', type=int, nargs='+', required=True, help='target years')
            p.add_argument('--seeds', type=int, nargs='+', default=[51, 52, 53], help='evaluation seeds; seed s reads the checkpoint of seed s - 9')
        if name == 'maintain':
            p.add_argument('--year', type=int, required=True)
            p.add_argument('--seeds', type=int, nargs='+', default=[51, 52, 53])
            p.add_argument('--studies', nargs='+', default=['maintenance', 'prompt'])
            p.add_argument('--device', default='cuda:0')
            p.add_argument('--max-windows', type=int, default=0, help='a bounded check only')
    opt = ap.parse_args()
    sys.exit(dict(metadata=metadata, checkdata=checkdata, cut=cut, train=train, trainone=train_one, export=export, maintain=maintain)[opt.mode](opt) or 0)


if __name__ == '__main__':
    main()
