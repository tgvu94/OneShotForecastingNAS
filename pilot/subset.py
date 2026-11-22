"""Proxy task of a city: a subset of its sensors and of its training period (arm D of the fidelity plan).

A root carries its proxy task in ``<root>/subset.json`` (``Root.subset``).  ``pilot.train_arch`` reads the file; a root
without it trains on the whole city, as before.  The file holds the kept sensor indices (or null = all sensors) and the
kept row ranges of the training part (or null = the whole training part), with the rule that made them.

    python -m pilot.subset make   --source results/benchst/shenzhen_h12 --dataset shenzhen --horizon 12
    python -m pilot.subset timing --source results/benchst/shenzhen_h12 --dataset shenzhen --horizon 12
    python -m pilot.subset link   --source results/benchst/shenzhen_h12 --dataset shenzhen --horizon 12
    python -m pilot.subset check  --source results/benchst/metrla_h12   --dataset metrla   --horizon 12

What a subset changes, and what it does not:
* sensors: the columns of the series, the adjacency (induced subgraph; the net normalises it again) and the zero code;
* period: the training windows (every window lies inside one kept range) and the scaler (fit on the kept rows of the kept
  sensors).  The validation and the test part keep their periods;
* the time features are a function of the row index of the whole series, so no subset moves them.
With all sensors and the whole training part the batches are byte-equal to the batches of the city (``check``).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import deque
from pathlib import Path

import numpy as np

from pilot.paths import Root

BASE = "results/fidelity"
FLAT = 1e-6   # a kept sensor whose std on the kept rows is below this share of its std on the whole training part counts as constant
N_ARCHS = 50
# name -> (sensor share, sensor method, draw, period share, period method); None = not reduced on that axis
SETTINGS = {
    "s10_R0": (0.10, "R", 0, None, None), "s10_C0": (0.10, "C", 0, None, None), "s10_P0": (0.10, "P", 0, None, None),
    "s25_R0": (0.25, "R", 0, None, None), "s25_R1": (0.25, "R", 1, None, None), "s25_R2": (0.25, "R", 2, None, None),
    "s25_C0": (0.25, "C", 0, None, None), "s25_P0": (0.25, "P", 0, None, None),
    "s50_R0": (0.50, "R", 0, None, None),
    "t25_L": (None, None, None, 0.25, "L"), "t50_L": (None, None, None, 0.50, "L"),
    "t25_E": (None, None, None, 0.25, "E"), "t50_E": (None, None, None, 0.50, "E"),
    "both_s25_t25": (0.25, "P", 0, 0.25, "L"),
}
# two more proxy tasks on both axes, with the period of both_s25_t25: the sensor rule and the sensor share change
TWO_AXIS = {"both_s25R_t25": (0.25, "R", 0, 0.25, "L"), "both_s10C_t25": (0.10, "C", 0, 0.25, "L")}
TIMING = ["full", "s10_R0", "s25_R0", "s50_R0", "t25_L", "t50_L", "both_s25_t25"]
SEED_BASE = {"R": 1000, "C": 2000, "P": 3000}


# ---------------------------------------------------------------- the city
def city_inputs(source: Root) -> dict:
    """Raw series, borders, window, horizon, steps per week and adjacency of the city of a benchst root."""
    import pandas as pd
    from pilot.adjacency import load_adj
    from pilot.data import get_cfg

    cfg = get_cfg(source.benchmark)
    raw = np.load(Path(cfg.benchmark.dataset_root) / cfg.benchmark.type / cfg.benchmark.file_name, allow_pickle=True)["data"][:, :, 0]
    week = int(pd.Timedelta("7D") / pd.Timedelta(str(cfg.benchmark.freq)))
    return {"raw": raw, "num_train": int(len(raw) * 0.6), "window": int(cfg.benchmark.dataloader.window_size),
            "horizon": int(cfg.benchmark.external_forecast_horizon), "week": week, "freq": str(cfg.benchmark.freq),
            "adj": load_adj(source.adj), "benchmark": source.benchmark}


# ---------------------------------------------------------------- selection of the sensors
def _terciles(v: np.ndarray) -> np.ndarray:
    r = np.argsort(np.argsort(v, kind="stable"), kind="stable")
    return (r * 3 // len(v)).astype(int)


def select_sensors(method: str, n_keep: int, A: np.ndarray, raw_train: np.ndarray, seed: int) -> tuple[list, dict]:
    """R = uniform random; C = breadth-first walk from a random sensor (a new random start when a component ends);
    P = random inside strata of the degree, the mean and the variance of the series (terciles of each), with a share of
    each stratum in proportion to its size."""
    n = A.shape[0]
    rng = np.random.default_rng(seed)
    info = {}
    if method == "R":
        idx = rng.choice(n, n_keep, replace=False)
    elif method == "C":
        seen, order, starts = np.zeros(n, bool), [], 0
        while len(order) < n_keep:
            start = int(rng.choice(np.where(~seen)[0])); starts += 1
            seen[start] = True; q = deque([start])
            while q and len(order) < n_keep:
                u = q.popleft(); order.append(u)
                for v in np.where(A[u] > 0)[0]:
                    if not seen[v]:
                        seen[v] = True; q.append(int(v))
        idx = np.array(order); info["walk_starts"] = starts
    elif method == "P":
        deg = (A > 0).sum(1)
        strata = _terciles(deg) * 9 + _terciles(raw_train.mean(0)) * 3 + _terciles(raw_train.var(0))
        keys, counts = np.unique(strata, return_counts=True)
        quota = n_keep * counts / n
        take = np.floor(quota).astype(int)
        for j in np.argsort(-(quota - take), kind="stable")[: n_keep - take.sum()]:
            take[j] += 1
        idx = np.concatenate([rng.choice(np.where(strata == k)[0], t, replace=False) for k, t in zip(keys, take) if t > 0])
        info["strata"] = int(len(keys))
    else:
        raise ValueError(f"unknown sensor method {method!r}")
    idx = sorted(int(i) for i in idx)
    assert len(idx) == n_keep == len(set(idx))
    return idx, info


def graph_stats(A: np.ndarray, idx: list | None) -> dict:
    S = A if idx is None else A[np.ix_(idx, idx)]
    deg = (S > 0).sum(1)
    return {"n_sensors": int(S.shape[0]), "edges": int((S > 0).sum() // 2), "isolated_share": float((deg == 0).mean()),
            "mean_degree": float(deg.mean()), "edges_city": int((A > 0).sum() // 2)}


# ---------------------------------------------------------------- selection of the period
def week_segments(num_train: int, week: int, share: float, method: str) -> tuple[list, dict]:
    """Whole weeks of the training part, counted back from its end.  L = the latest weeks; E = weeks spread evenly.
    Returns row ranges [a, b) with neighbouring weeks merged."""
    K = num_train // week
    if K < 2:
        raise ValueError(f"the training part holds {K} whole weeks; a period subset needs 2 or more")
    n = min(K, max(1, int(share * K + 0.5)))
    first = num_train - K * week
    if method == "L":
        weeks = list(range(K - n, K))
    elif method == "E":
        weeks = sorted({int(round(float(x))) for x in np.linspace(0, K - 1, n)})
        assert len(weeks) == n, weeks
    else:
        raise ValueError(f"unknown period method {method!r}")
    segs = []
    for w in weeks:
        a, b = first + w * week, first + (w + 1) * week
        if segs and segs[-1][1] == a:
            segs[-1][1] = b
        else:
            segs.append([a, b])
    return segs, {"weeks_total": int(K), "weeks_kept": weeks, "steps_per_week": int(week), "row_share": float(n * week / num_train)}


def train_split(segments: list, window: int, horizon: int) -> np.ndarray:
    """Index of the last past row of every training window that lies inside one kept range (past = window rows, future = horizon rows).
    For the one range [0, num_train) this is the split of the city: arange(window - 1, num_train - horizon)."""
    return np.concatenate([np.arange(a + window - 1, b - horizon) for a, b in segments])


# ---------------------------------------------------------------- the subset record
def make_subset(name: str, city: dict, s, s_method, draw, t, t_method) -> dict:
    A, raw, nt = city["adj"], city["raw"], city["num_train"]
    rec = {"name": name, "benchmark": city["benchmark"], "n_sensors_city": int(raw.shape[1]), "num_train": int(nt),
           "window": city["window"], "horizon": city["horizon"], "sensors": None, "segments": None}
    if s is not None:
        seed = SEED_BASE[s_method] + int(draw)
        n_keep = int(round(s * raw.shape[1]))
        idx, info = select_sensors(s_method, n_keep, A, raw[:nt], seed)
        rec.update({"sensors": idx, "sensor_rule": {"share": s, "method": s_method, "draw": int(draw), "seed": seed, **info}})
    if t is not None:
        segs, info = week_segments(nt, city["week"], t, t_method)
        rec.update({"segments": segs, "period_rule": {"share": t, "method": t_method, **info}})
    rec["graph"] = graph_stats(A, rec["sensors"])
    segs = rec["segments"] or [[0, nt]]
    rec["train_windows"] = int(len(train_split(segs, city["window"], city["horizon"])))
    rec["train_windows_city"] = int(nt - city["horizon"] - city["window"] + 1)
    return rec


def dump_subset(rec: dict, root_dir: Path) -> str:
    text = json.dumps(rec, indent=1, sort_keys=True) + "\n"
    (root_dir / "subset.json").write_text(text)
    sha1 = hashlib.sha1(text.encode()).hexdigest()
    (root_dir / "subset.sha1").write_text(sha1 + "\n")
    return sha1


def load_subset(path: str | Path) -> dict:
    path = Path(path)
    text = path.read_text()
    rec = json.loads(text)
    rec["sha1"] = hashlib.sha1(text.encode()).hexdigest()
    sha_file = path.with_suffix(".sha1")
    if sha_file.exists() and sha_file.read_text().strip() != rec["sha1"]:
        raise ValueError(f"{path}: content does not match {sha_file}")
    return rec


# ---------------------------------------------------------------- applying a subset
def full_period(subset: dict, num_train: int) -> bool:
    return subset.get("segments") is None or [list(s) for s in subset["segments"]] == [[0, int(num_train)]]


def kept_rows(subset: dict, n_rows: int, num_train: int) -> np.ndarray:
    keep = np.zeros(n_rows, bool)
    for a, b in (subset.get("segments") or [[0, num_train]]):
        keep[a:b] = True
    return keep


def apply_to_data_info(data_info: dict, subset: dict, num_train: int) -> None:
    """In place: keep the sensor columns; with a reduced period, standardise again on the kept rows.  The series arrives
    standardised on the whole training part, and the two steps compose to (raw - mean_kept) / std_kept per sensor."""
    y = data_info["y"]
    if len(y) != 1:
        raise NotImplementedError("a subset needs the multi-variant layout (one series of all sensors)")
    data = np.asarray(y[0])
    if int(num_train) != int(subset["num_train"]) or data.shape[1] != int(subset["n_sensors_city"]):
        raise ValueError(f"subset {subset['name']} was made for another series: num_train {subset['num_train']} / "
                         f"{num_train}, sensors {subset['n_sensors_city']} / {data.shape[1]}")
    out = data if subset.get("sensors") is None else data[:, np.asarray(subset["sensors"])]
    if not full_period(subset, num_train):
        ref = out[kept_rows(subset, len(out), num_train)].astype(np.float64)
        m, s = ref.mean(0), ref.std(0)
        s = np.where(s < FLAT, 1.0, s)   # a sensor that is constant on the kept rows keeps the scale of the whole training part
        out = ((out.astype(np.float64) - m) / s).astype(data.dtype)
    data_info["y"] = [out]


def subset_scaler(raw: np.ndarray, subset: dict, num_train: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(raw series of the kept sensors, mean, scale) of the scaler that apply_to_data_info composes, in float64:
    mean and std of the kept training rows; a sensor that is constant there keeps the std of the whole training part."""
    r = raw if subset.get("sensors") is None else raw[:, np.asarray(subset["sensors"])]
    full = r[:num_train].astype(np.float64)
    sd_full = full.std(0); sd_full = np.where(sd_full == 0, 1.0, sd_full)
    if full_period(subset, num_train):
        return r, full.mean(0), sd_full
    ref = r[kept_rows(subset, len(r), num_train)].astype(np.float64)
    sd = ref.std(0)
    return r, ref.mean(0), np.where(sd / sd_full < FLAT, sd_full, sd)


def induced_adjacency(A: np.ndarray, subset: dict) -> np.ndarray:
    if subset.get("sensors") is None:
        return A
    idx = np.asarray(subset["sensors"])
    return np.ascontiguousarray(A[np.ix_(idx, idx)])


# ---------------------------------------------------------------- roots
def root_dir(dataset: str, horizon: int, name: str, base: str = BASE) -> Path:
    return Path(base) / f"{dataset}_h{horizon}_{name}"


def link_data(root: Path, source: Root) -> None:
    """data/ of a subset root = links to the probe batch and the adjacency of the city (data/ is not in git)."""
    d = root / "data"; d.mkdir(parents=True, exist_ok=True)
    for f in (source.probe, source.adj):
        link = d / f.name
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(os.path.relpath(f.resolve(), d.resolve()))


def frozen_text(name: str, rec: dict | None, source: Root, n_archs: int, list_sha1: str, sub_sha1: str | None, note: str) -> str:
    lines = [f"# FROZEN: proxy task `{name}` of {source.dataset}", "",
             f"- City root: `{source.dir}` (labels, schedule, zero mask, probe batch, adjacency).",
             f"- `archs.jsonl`: the first {n_archs} lines of the list of the city root; sha1 `{list_sha1[:13]}`.",
             f"- {note}"]
    if rec is not None:
        g = rec["graph"]
        lines += [f"- `subset.json`: sha1 `{sub_sha1[:13]}`; {g['n_sensors']} of {rec['n_sensors_city']} sensors, {g['edges']} of {g['edges_city']} edges, "
                  f"isolated share {g['isolated_share']:.3f}; {rec['train_windows']} of {rec['train_windows_city']} training windows.",
                  f"- Sensor rule: `{json.dumps(rec.get('sensor_rule'))}`. Period rule: `{json.dumps(rec.get('period_rule'))}`."]
    else:
        lines.append("- No `subset.json`: the whole city, as the reference of the timing run.")
    lines += ["- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.", ""]
    return "\n".join(lines)


def write_root(name: str, rec: dict | None, source: Root, arch_lines: list, base: str, note: str, tag: str = "") -> dict:
    d = root_dir(source.dataset, source.horizon, tag + name, base)
    d.mkdir(parents=True, exist_ok=True)
    text = "".join(arch_lines)
    (d / "archs.jsonl").write_text(text)
    sub_sha1 = dump_subset({k: v for k, v in rec.items() if k != "sha1"}, d) if rec is not None else None
    link_data(d, source)
    (d / "FROZEN.md").write_text(frozen_text(name, rec, source, len(arch_lines), hashlib.sha1(text.encode()).hexdigest(), sub_sha1, note))
    row = {"root": str(d), "name": name, "subset_sha1": (sub_sha1 or "")[:13], "n_archs": len(arch_lines)}
    if rec is not None:
        row.update({**rec["graph"], "train_windows": rec["train_windows"], "train_windows_city": rec["train_windows_city"],
                    "sensor_rule": json.dumps(rec.get("sensor_rule")), "period_rule": json.dumps(rec.get("period_rule"))})
    return row


def cmd_make(source: Root, base: str, n_archs: int, group: str = "plan") -> None:
    import pandas as pd
    city = city_inputs(source)
    lines = open(source.archs_jsonl).readlines()[:n_archs]
    rows = []
    settings, note, tail = (SETTINGS, "One of the 14 proxy tasks of arm D; the settings are fixed in the plan before any run.", "") if group == "plan" else \
        (TWO_AXIS, "A proxy task on both axes, added after the timing run: only a task on both axes has a cost share of 0.25 or less.", "_twoaxis")
    for name, spec in settings.items():
        rec = make_subset(name, city, *spec)
        rows.append(write_root(name, rec, source, lines, base, note))
        print(rows[-1]["root"], rows[-1]["subset_sha1"], rec["graph"], rec["train_windows"])
    out = Path(base) / "compare" / "tables"; out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / f"subsets_{source.dataset}{tail}.csv", index=False)


def timing_archs(source: Root, n_archs: int) -> list:
    """Three of the first n_archs: the lowest, the median and the highest seconds per epoch of the stored seed-0 runs."""
    lines = open(source.archs_jsonl).readlines()[:n_archs]
    sec = []
    for ln in lines:
        m = json.load(open(source.train / json.loads(ln)["arch_id"] / "seed0" / "metrics.json"))
        sec.append(float(np.mean([r["seconds"] for r in m["history"]])))
    order = np.argsort(sec, kind="stable")
    pick = [int(order[0]), int(order[len(order) // 2]), int(order[-1])]
    for i in pick:
        print(f"timing architecture {json.loads(lines[i])['arch_id']}: {sec[i]:.1f} s per epoch in the stored run")
    return [lines[i] for i in pick]


def cmd_timing(source: Root, base: str, n_archs: int, tag: str = "timing_") -> None:
    lines = timing_archs(source, n_archs)
    for name in TIMING:
        rec = None
        if name != "full":
            rec = load_subset(root_dir(source.dataset, source.horizon, name, base) / "subset.json")
        row = write_root(name, rec, source, lines, base, "Timing root: 3 architectures, 3 epochs; a run of this root is not a label.", tag=tag)
        print(row["root"], row["subset_sha1"])


def cmd_link(source: Root, base: str) -> None:
    for d in sorted(Path(base).glob(f"{source.dataset}_h{source.horizon}_*")):
        if (d / "archs.jsonl").exists():
            link_data(d, source); print("linked", d)


# ---------------------------------------------------------------- checks with no GPU
def _batches(loader, n: int) -> list:
    out = []
    for i, b in enumerate(loader):
        if i >= n:
            break
        out.append(b)
    return out


def _same(a, b, path: str, bad: list) -> None:
    import torch
    if isinstance(a, dict):
        if set(a) != set(b):
            bad.append(f"{path}: keys differ"); return
        for k in a:
            _same(a[k], b[k], f"{path}.{k}", bad)
    elif isinstance(a, (list, tuple)):
        if len(a) != len(b):
            bad.append(f"{path}: length differs"); return
        for i, (x, y) in enumerate(zip(a, b)):
            _same(x, y, f"{path}[{i}]", bad)
    elif torch.is_tensor(a):
        if a.shape != b.shape or a.dtype != b.dtype or a.numpy().tobytes() != b.numpy().tobytes():
            bad.append(f"{path}: tensors differ")
    elif isinstance(a, np.ndarray):
        if a.tobytes() != b.tobytes():
            bad.append(f"{path}: arrays differ")
    elif a != b:
        bad.append(f"{path}: {a!r} != {b!r}")


def cmd_check(source: Root, n_batches: int) -> int:
    import torch
    from sklearn.preprocessing import StandardScaler
    from pilot.data import get_cfg, get_dataset_and_loaders, seed_everything, zero_code_for

    city = city_inputs(source)
    raw, nt, W, H, A = city["raw"], city["num_train"], city["window"], city["horizon"], city["adj"]
    cfg = get_cfg(source.benchmark)
    fails = []

    def loaders(subset):
        seed_everything(0)
        ds, ld, dims = get_dataset_and_loaders(cfg, num_workers=0, subset=subset)
        seed_everything(0)
        return ds, [_batches(l, n_batches) for l in ld], dims

    # 1. all sensors and the whole training part, through the subset code: byte-equal batches
    ident = {"name": "identity", "num_train": nt, "n_sensors_city": int(raw.shape[1]), "sensors": list(range(raw.shape[1])), "segments": [[0, nt]]}
    _, ref_b, ref_dims = loaders(None)
    _, id_b, id_dims = loaders(ident)
    bad = []
    _same(ref_b, id_b, "batches", bad)
    if ref_dims["split_sizes"] != id_dims["split_sizes"]:
        bad.append(f"split sizes {ref_dims['split_sizes']} != {id_dims['split_sizes']}")
    z0, s0 = zero_code_for(cfg); z1, s1 = zero_code_for(cfg, ident)
    # the zero code of a subset is computed in float64; the code of the city is a float32 mean, so the two are not byte-equal.
    # What must hold: the two codes mark the same targets.
    zdiff = float((z0 - z1).abs().max())
    n_mask = 0
    for part in ref_b:
        for _, yb in part:
            t = yb["future_targets"].float()
            m0, m1 = (t - z0).abs() > 1e-4, (t - z1).abs() > 1e-4
            n_mask += int((~m0).sum())
            if not torch.equal(m0, m1):
                bad.append("the zero mask differs")
    if s0 != s1:
        bad.append("zero share differs")
    if induced_adjacency(A, ident).tobytes() != A.tobytes():
        bad.append("adjacency differs")
    print(f"[{'PASS' if not bad else 'FAIL'}] identity subset: {n_batches} batches of each of the 3 loaders, the split sizes and the adjacency are byte-equal; "
          f"the zero mask is equal on these batches ({n_mask} masked targets; the codes differ by {zdiff:.1e} at most)"
          + ("" if not bad else f" -- {bad[:5]}"))
    fails += bad

    # 2. a reduced subset: sensors by R at 0.25 and the latest weeks at 0.25
    sub = make_subset("check", city, 0.25, "R", 0, 0.25, "L")
    idx, keep = np.asarray(sub["sensors"]), kept_rows(sub, len(raw), nt)
    ds, b, dims = loaders(sub)
    bad = []
    # composition check on a series standardised on the whole training part
    full = StandardScaler().fit(raw[:nt]).transform(raw)
    info = {"y": [full]}
    apply_to_data_info(info, sub, nt)
    _, mu, sd = subset_scaler(raw, sub, nt)
    direct = (raw[:, idx].astype(np.float64) - mu) / sd
    flat = int((raw[keep][:, idx].astype(np.float64).std(0) / np.where(raw[:nt][:, idx].std(0) == 0, 1.0, raw[:nt][:, idx].std(0)) < FLAT).sum())
    plain = StandardScaler().fit(raw[keep][:, idx]).transform(raw[:, idx])
    live = np.abs(plain - direct).max(0) < 1e-3
    if int((~live).sum()) > flat:
        bad.append(f"{int((~live).sum())} sensors differ from a plain scaler fit on the kept rows; {flat} are constant there")
    err = float(np.abs(info["y"][0] - direct).max())
    if err > 1e-4:
        bad.append(f"scaler: max difference {err:.2e} against a scaler fit on the kept rows")
    want = len(train_split(sub["segments"], W, H))
    if dims["split_sizes"][0] != want or dims["num_targets"] != len(idx):
        bad.append(f"train windows {dims['split_sizes'][0]} (want {want}), sensors {dims['num_targets']} (want {len(idx)})")
    if dims["split_sizes"][1:] != ref_dims["split_sizes"][1:]:
        bad.append("the validation or the test split changed")
    X, y = b[0][0]
    if X["past_targets"].shape[-1] != len(idx) or y["future_targets"].shape[-1] != len(idx):
        bad.append("batch does not hold the kept sensors only")
    # the time features of the first validation batch are the features of the city (the validation loader is not shuffled)
    if b[1][0][0]["past_features"].numpy().tobytes() != ref_b[1][0][0]["past_features"].numpy().tobytes():
        bad.append("time features of the validation part moved")
    print(f"[{'PASS' if not bad else 'FAIL'}] reduced subset ({len(idx)} sensors, {sub['train_windows']} training windows): scaler (max diff {err:.1e}; {flat} kept sensors are constant on the kept rows), "
          f"split sizes, batch shapes, time features" + ("" if not bad else f" -- {bad}"))
    fails += bad

    # 3. the zero mask of the subset marks exactly the raw zeros of the kept sensors in the validation targets
    bad = []
    zc, share = zero_code_for(cfg, sub)
    seed_everything(0)
    _, (_, val_loader, _), _ = get_dataset_and_loaders(cfg, num_workers=0, subset=sub)
    masked = total = 0
    for _, yb in val_loader:
        t = yb["future_targets"].float()
        masked += int(((t - zc).abs() <= 1e-4).sum()); total += t.numel()
    num_vali = int(len(raw) * 0.8) - nt
    val_idx = np.arange(nt + W - 1, nt + num_vali - H)
    expect = int(sum((raw[m + 1: m + 1 + H][:, idx] == 0).sum() for m in val_idx))
    if masked != expect or total != len(val_idx) * H * len(idx):
        bad.append(f"masked {masked} of {total}, expected {expect} of {len(val_idx) * H * len(idx)}")
    print(f"[{'PASS' if not bad else 'FAIL'}] zero mask of the reduced subset on the validation targets: {masked} masked, {expect} raw zeros"
          + ("" if not bad else f" -- {bad}"))
    fails += bad

    # 4. the induced adjacency and the training windows
    bad = []
    S = induced_adjacency(A, sub)
    if S.shape != (len(idx), len(idx)) or int((S > 0).sum() // 2) != sub["graph"]["edges"] or not np.array_equal(S, S.T):
        bad.append("induced adjacency")
    sp = train_split(sub["segments"], W, H)
    if not all(any(a <= m - W + 1 and m + H < b for a, b in sub["segments"]) for m in sp):
        bad.append("a training window leaves its kept range")
    if not np.array_equal(train_split([[0, nt]], W, H), np.arange(W - 1, nt - H)):
        bad.append("the split of the whole training part differs from the split of the city")
    print(f"[{'PASS' if not bad else 'FAIL'}] induced adjacency ({sub['graph']['edges']} edges) and training windows inside the kept ranges"
          + ("" if not bad else f" -- {bad}"))
    fails += bad
    print("check subset:", "PASS" if not fails else f"FAIL ({len(fails)})")
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["make", "timing", "link", "check"])
    ap.add_argument("--source", required=True, help="the benchst root of the city")
    ap.add_argument("--dataset", default=None); ap.add_argument("--horizon", type=int, default=None)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--n-archs", type=int, default=N_ARCHS)
    ap.add_argument("--batches", type=int, default=3)
    ap.add_argument("--group", default="plan", choices=["plan", "twoaxis"], help="make: the 14 settings of the plan or the two added settings on both axes")
    ap.add_argument("--tag", default="timing_", help="timing: prefix of the setting name in the root name")
    a = ap.parse_args()
    source = Root(a.source, a.dataset, a.horizon)
    if a.cmd == "make":
        cmd_make(source, a.base, a.n_archs, a.group)
    elif a.cmd == "timing":
        cmd_timing(source, a.base, a.n_archs, a.tag)
    elif a.cmd == "link":
        cmd_link(source, a.base)
    else:
        return cmd_check(source, a.batches)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
