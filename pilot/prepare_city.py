"""Bring a candidate city into the PEMS layout the loaders read: <NAS_DATA_ROOT>/PEMS/<NAME>.npz with ``data`` of shape
(T, N, 1), channel 0 = the target, plus a pickled binary N x N adjacency ``adj_<NAME>.pkl`` (ndarray, as adj_PEMS07.pkl).

    python -m pilot.prepare_city tpb --city chengdu_m --name CHENGDU
    python -m pilot.prepare_city tpb --city shenzhen --name SHENZHEN
    python -m pilot.prepare_city expytky --name EXPYTKY

TPB (Liu et al. 2023, Traffic Pattern Bank): ``data_unzipped/<city>/dataset.npy`` (T, N, 2) at 10-minute steps, channel 0 =
speed, channel 1 = time of day; ``matrix.npy`` (N, N) non-negative weights.  EXPY-TKY (Jiang et al. 2023, MegaCRN): three
monthly long csv files (timestamp, linkid, speed) over 2,841 links; the paper's 1,843-link subset is ``tokyo_link_idx.csv``
(row indices into ``expy-tky_link_info.csv``); ``expy-tky_adj01.npy`` is the binary 2,841 x 2,841 adjacency.  Missing
(timestamp, link) pairs become 0, the same convention as METR-LA, which the masked pipeline skips.
"""
from __future__ import annotations

import argparse
import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(os.environ["NAS_DATA_ROOT"])
OUT = ROOT / "PEMS"


def save(name: str, data: np.ndarray, adj: np.ndarray, note: str):
    data = data.astype(np.float32)
    if data.ndim == 2:
        data = data[:, :, None]
    assert data.ndim == 3 and data.shape[1] == adj.shape[0] == adj.shape[1], (data.shape, adj.shape)
    adj = (adj > 0).astype(np.float32)
    np.fill_diagonal(adj, 0)
    np.savez_compressed(OUT / f"{name}.npz", data=data)
    pickle.dump(adj, open(OUT / f"adj_{name}.pkl", "wb"))
    zeros = float((data[:, :, 0] == 0).mean()); nans = float(np.isnan(data[:, :, 0]).mean())
    print(f"{name}: data {data.shape}, zeros {zeros:.4f}, nan {nans:.4f}, min {np.nanmin(data):.2f} max {np.nanmax(data):.2f} "
          f"mean {np.nanmean(data):.2f}; adj {adj.shape}, edges {int(adj.sum())}, symmetric {bool(np.allclose(adj, adj.T))}; {note}")
    (OUT / f"{name}_README.md").write_text(f"# {name}\n\n{note}\n\ndata {data.shape}, zeros {zeros:.4f}, edges {int(adj.sum())}.\n")


def tpb(args):
    d = ROOT / "TPB" / "TrafficPatternBank" / "data_unzipped" / args.city
    x = np.load(d / "dataset.npy")
    m = np.load(d / "matrix.npy")
    print(f"{args.city}: dataset {x.shape}; channel 0 range {x[..., 0].min():.2f} to {x[..., 0].max():.2f}, "
          f"channel 1 range {x[..., 1].min():.3f} to {x[..., 1].max():.3f}; matrix range {m.min():.3f} to {m.max():.3f}, nonzero {int((m > 0).sum())}")
    save(args.name, x[:, :, 0], m, f"TPB {args.city}: channel 0 of dataset.npy (speed), 10-minute steps, adjacency = matrix.npy > 0 with the diagonal dropped.")


def expytky(args):
    d = ROOT / "EXPYTKY"
    info = pd.read_csv(d / "expy-tky_link_info.csv", index_col=0)
    idx = pd.read_csv(d / "tokyo_link_idx.csv", header=None)[0].astype(int).values
    links = info.loc[idx, "link_id"].values if "link_id" in info else info.iloc[idx, 0].values
    frames = [pd.read_csv(d / f"expy-tky_2021{m}.csv.gz") for m in ("10", "11", "12")]
    df = pd.concat(frames, ignore_index=True)
    df = df[df.linkid.isin(set(links))]
    wide = df.pivot_table(index="timestamp", columns="linkid", values="speed", aggfunc="mean")
    full_index = pd.date_range(wide.index.min(), wide.index.max(), freq="10min").strftime("%Y-%m-%d %H:%M:%S")
    wide = wide.reindex(index=full_index, columns=links)
    missing = float(wide.isna().mean().mean())
    wide = wide.fillna(0.0)
    adj_all = np.load(d / "expy-tky_adj01.npy")
    adj = adj_all[np.ix_(idx, idx)]
    pd.Series(links).to_csv(OUT / "EXPYTKY_link_ids.txt", index=False, header=False)
    save(args.name, wide.values, adj, f"EXPY-TKY, the 1,843-link subset of MegaCRN in tokyo_link_idx.csv order; 10-minute steps "
         f"{full_index[0]} to {full_index[-1]}; {missing:.4f} of the (time, link) cells were missing and are stored as 0; adjacency = expy-tky_adj01.npy restricted to the subset.")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("tpb"); a.add_argument("--city", required=True); a.add_argument("--name", required=True); a.set_defaults(fn=tpb)
    b = sp.add_parser("expytky"); b.add_argument("--name", default="EXPYTKY"); b.set_defaults(fn=expytky)
    args = ap.parse_args(); args.fn(args)


if __name__ == "__main__":
    main()
