"""City files of LargeST in the format that the released loader of OpenCity reads (Survey/experiments/opencity-plan.md).

    python -m pilot.opencity_data --city sd ca_d6

Files, as the released DiDi files:
  $NAS_DATA_ROOT/opencity/<name>/<name>.npz            key `data`, float64, [T, N, 1]
  $NAS_DATA_ROOT/opencity/<name>/<name>_rn_adj.npy     float64, N x N

Source: $NAS_DATA_ROOT/LargeST/2019.h5, ca_meta.csv and adjacency.npy.  Rules, after the released script
data/generate_ca_data.py and the default branch of lib/data_process.load_st_dataset:
  - every sensor of the district is kept, in the order of ca_meta.csv;
  - the values stay at 5-minute steps; the span is March and April (61 days, 17,568 steps), the span that the released
    loader cuts for a CAD set; the year is 2019 (the release uses 2020, which this project does not hold);
  - an absent value is 0 (the loss and the metrics of the release leave zero targets out);
  - the graph is the block of adjacency.npy for the sensors, with its weights, and a diagonal of 1 as in the DiDi files.
The first step is a Friday; pilot.opencity_run gives this to the time features of the release.
"""
import argparse, os
from pathlib import Path

import numpy as np

DISTRICT = {"sd": 11, "ca_d6": 6, "ca_d10": 10}       # districts that the pre-training of OpenCity does not hold
FIRST, LAST = 288 * (31 + 28), 288 * (31 + 28 + 31 + 30)


def build(city):
    import h5py, pandas as pd
    d = Path(os.environ["NAS_DATA_ROOT"])
    meta = pd.read_csv(d / "LargeST" / "ca_meta.csv")
    keep = np.flatnonzero((meta["District"] == DISTRICT[city]).to_numpy())
    with h5py.File(d / "LargeST" / "2019.h5", "r") as f:
        g = f[list(f.keys())[0]]
        assert [s.decode() for s in g["axis0"][:]] == [str(i) for i in meta["ID"]], "sensor order of 2019.h5 differs from ca_meta.csv"
        x = g["block0_values"][FIRST:LAST][:, keep].astype(np.float64)
    absent = float(np.isnan(x).mean())
    x[np.isnan(x)] = 0
    A = np.load(d / "LargeST" / "adjacency.npy", mmap_mode="r")
    A = np.asarray(A[np.ix_(keep, keep)]).astype(np.float64)
    np.fill_diagonal(A, 1)
    out = d / "opencity" / city
    out.mkdir(parents=True, exist_ok=True)
    np.savez(out / f"{city}.npz", data=x[..., None])
    np.save(out / f"{city}_rn_adj.npy", A)
    print(f"{city}: district {DISTRICT[city]} data {x[..., None].shape} absent {absent:.4f} zero {float((x == 0).mean()):.4f} mean {x.mean():.2f} "
          f"max {x.max():.0f} | graph {A.shape} entries per row {float((A > 0).sum(1).mean()):.1f} symmetric {bool(np.allclose(A, A.T))}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", nargs="+", required=True, choices=sorted(DISTRICT))
    for c in ap.parse_args().city:
        build(c)
