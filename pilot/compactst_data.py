"""Dataset files in the format that the released loader of CompactST reads, and the naive baselines of its protocol.

    python -m pilot.compactst_data --city chengdu shenzhen sd gba        # write the files
    python -m pilot.compactst_data --city chengdu --naive                # print the naive baselines only
    python -m pilot.compactst_data --city ca_d3 gba_n500                 # one more district of LargeST; a sensor subset of gba

Files (lib/load_data.py of the upstream repository):
  $NAS_DATA_ROOT/compactst/data/<name>.dat        raw float32, [T, N, 1], row-major
  $NAS_DATA_ROOT/compactst/adj_mx/<name>.json     {"shape": [T, N, 1], "adj_mx": N x N}
<name> is the dataset name of the released script: chengdu_traffic, shenzhen_traffic, sd; gba is our addition.

Sources:
  chengdu, shenzhen   $NAS_DATA_ROOT/PEMS/<CITY>.npz (speed, 10-minute steps) and adj_<CITY>.pkl
  sd, gba             $NAS_DATA_ROOT/LargeST/2019.h5, the sensors of district 11 (716) or 4 (2,352), every sensor kept; a
                      15-minute value is the mean of the valid 5-minute values, an absent value is 0; adjacency.npy > 0.
                      (pilot.spatialgate.load_largest differs: it reads a zero as absent, and its files drop sensors.)
  ca_d<k>             the same rules for district k of LargeST (3, 5, 6, 7, 8, 10, 12)
  gba_n<n>            n sensors of gba, drawn without replacement by numpy default_rng(0), kept in the order of gba
With these rules the mean of the look-back window gives the published error of the HA row of the paper at chengdu, shenzhen
and sd (Table 4), so the values agree with the files of the paper.  The adjacency of the paper is not released.

Naive baselines on the test windows of the released split (96 steps in, 48 out, the last 20 % of the windows):
  lookback      the mean of the look-back window (the HA of the paper)
  slot_day      the mean of the same slot of the day in the first `share` of the training data
  slot_week     the mean of the same slot of the week (only when the data hold two weeks or more)
"""
import argparse, json, os, pickle
from pathlib import Path

import numpy as np

CITIES = {"chengdu": ("chengdu_traffic", 144), "shenzhen": ("shenzhen_traffic", 144), "sd": ("sd", 96), "gba": ("gba", 96)}
DISTRICT = {"sd": 11, "gba": 4}
for _k in (3, 5, 6, 7, 8, 10, 12):
    CITIES[f"ca_d{_k}"] = (f"ca_d{_k}", 96); DISTRICT[f"ca_d{_k}"] = _k
SUBSET = {"gba_n500": ("gba", 500), "gba_n1000": ("gba", 1000)}      # name: (parent city, count of sensors)
for _k in SUBSET:
    CITIES[_k] = (_k, 96)
IN_STEPS, OUT_STEPS = 96, 48


def data_root() -> Path:
    return Path(os.environ["NAS_DATA_ROOT"])


def load_source(city):
    """[T, N] float32 values and the N x N adjacency (0/1, zero diagonal)."""
    d = data_root()
    if city in SUBSET:
        parent, n = SUBSET[city]
        x, A = load_source(parent)
        keep = np.sort(np.random.default_rng(0).choice(x.shape[1], n, replace=False))
        return x[:, keep], np.ascontiguousarray(A[np.ix_(keep, keep)])
    if city in DISTRICT:
        import h5py, pandas as pd
        meta = pd.read_csv(d / "LargeST" / "ca_meta.csv")
        keep = np.flatnonzero((meta["District"] == DISTRICT[city]).to_numpy())
        with h5py.File(d / "LargeST" / "2019.h5", "r") as f:
            g = f[list(f.keys())[0]]
            ids = [s.decode() for s in g["axis0"][:]]
            assert ids == [str(i) for i in meta["ID"]], "sensor order of 2019.h5 differs from ca_meta.csv"
            v = g["block0_values"]
            T5 = v.shape[0] - v.shape[0] % 3
            x = np.zeros((T5 // 3, len(keep)), dtype=np.float32)
            step = 3 * 2880
            for s in range(0, T5, step):
                blk = v[s:min(s + step, T5)][:, keep].astype(np.float64).reshape(-1, 3, len(keep))
                ok = np.isfinite(blk)
                cnt = ok.sum(1)
                x[s // 3:s // 3 + len(blk)] = np.where(cnt > 0, np.where(ok, blk, 0).sum(1) / np.maximum(cnt, 1), 0)
        A = np.load(d / "LargeST" / "adjacency.npy", mmap_mode="r")
        A = np.asarray(A[np.ix_(keep, keep)] > 0).astype(np.float32)
    else:
        z = np.load(d / "PEMS" / f"{city.upper()}.npz")
        a = z[z.files[0]]
        x = (a[..., 0] if a.ndim == 3 else a).astype(np.float32)
        with open(d / "PEMS" / f"adj_{city.upper()}.pkl", "rb") as f:
            A = (np.asarray(pickle.load(f)) > 0).astype(np.float32)
    np.fill_diagonal(A, 0)
    return x, A


def naive(x, steps_per_day, share=0.05):
    """MAE and RMSE of the naive baselines on the test windows; `share` is the share of the training split (0.05 = few-shot)."""
    x = x.astype(np.float64)
    T, N = x.shape
    L, H = IN_STEPS, OUT_STEPS
    nw = T - L - H + 1
    idx = np.arange(int(nw * 0.8), nw)
    n_train = int(nw * 0.7 * share) + L + H - 1              # the steps that the training windows of the share cover
    out = {"test_windows": int(len(idx)), "train_steps": int(n_train), "train_days": round(n_train / steps_per_day, 1)}

    def score(pred_of_h):
        a = s = 0.0
        for h in range(H):
            e = x[idx + L + h] - pred_of_h(h)
            a += np.abs(e).mean(); s += (e ** 2).mean()
        return {"mae": float(a / H), "rmse": float((s / H) ** 0.5)}

    cs = np.concatenate([np.zeros((1, N)), np.cumsum(x, 0)])
    look = (cs[idx + L] - cs[idx]) / L
    out["lookback"] = score(lambda h: look)
    for name, per in (("slot_day", steps_per_day), ("slot_week", 7 * steps_per_day)):
        if n_train < 2 * per:
            continue
        slot = np.arange(T) % per
        prof = np.stack([x[:n_train][slot[:n_train] == k].mean(0) for k in range(per)])
        out[name] = score(lambda h: prof[slot[idx + L + h]])
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", nargs="+", required=True, choices=sorted(CITIES))
    ap.add_argument("--naive", action="store_true", help="print the naive baselines and write no file")
    ap.add_argument("--shares", nargs="+", type=float, default=[0.05, 1.0])
    args = ap.parse_args(argv)
    out = data_root() / "compactst"
    for city in args.city:
        name, spd = CITIES[city]
        x, A = load_source(city)
        T, N = x.shape
        print(f"{city}: {name} shape [{T}, {N}, 1], mean {x.mean():.3f}, zero share {float((x == 0).mean()):.4f}, edges {int(A.sum())}")
        for share in args.shares:
            print(f"  naive, share {share}: {json.dumps(naive(x, spd, share))}")
        if args.naive:
            continue
        (out / "data").mkdir(parents=True, exist_ok=True); (out / "adj_mx").mkdir(parents=True, exist_ok=True)
        x[:, :, None].astype(np.float32).tofile(out / "data" / f"{name}.dat")
        with open(out / "adj_mx" / f"{name}.json", "w") as f:
            json.dump({"shape": [T, N, 1], "adj_mx": A.astype(int).tolist()}, f)
        print(f"  wrote {out / 'data' / (name + '.dat')} and {out / 'adj_mx' / (name + '.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
