"""spatialgate, the neural stage: STID with one spatial module that runs for a set of receiver sensors only.

A genotype record: ``{"hand_model": "stid_spatial", "clock": "true", "head": "mae", "graph": None, "space": "hand_v1",
"spatial": {"root": "results/spatialgate/largestsd_h12", "set": "none" | "all" | "<name>", "k": 16}}``.
  set = none : plain STID (the base model); the module does not exist
  set = all  : every sensor is a receiver (the full model)
  set = name : the receivers are the sensors of ``<root>/sets/<name>.json`` (the gated model)
The senders of a receiver are its first k columns in ``<root>/data/<dataset>_senders.npy`` ([N, k_max] sensor indices, nearest
first, -1 = no further neighbour; written by ``python -m pilot.spatialgate prepare``).  The module reads the hidden state of STID
before its regression layer: one attention over the senders of each receiver, then an MLP on (own state, attended state) that
gives a correction of the forecast of the receiver.  A sensor that is no receiver keeps the forecast of STID.  The cost of the
module grows with (receivers x k), not with the square of the sensor count.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

from pilot.hand_models import IN_STEPS, STID, MAEHead, clock_indices

REPO = Path(__file__).resolve().parents[1]


class GatedSpatial(nn.Module):
    def __init__(self, hidden: int, horizon: int, receivers: np.ndarray, senders: np.ndarray, dim: int = 64, dropout: float = 0.15):
        super().__init__()
        self.register_buffer("receivers", torch.as_tensor(receivers, dtype=torch.long))
        self.register_buffer("senders", torch.as_tensor(np.maximum(senders, 0), dtype=torch.long))      # [S, k]
        self.register_buffer("has_sender", torch.as_tensor(senders >= 0))
        self.dim = dim
        self.q, self.k, self.v = nn.Linear(hidden, dim), nn.Linear(hidden, dim), nn.Linear(hidden, dim)
        self.out = nn.Sequential(nn.Linear(hidden + dim, hidden), nn.ReLU(), nn.Dropout(dropout), nn.Linear(hidden, horizon))

    def forward(self, h: torch.Tensor) -> torch.Tensor:          # h [B, N, D] -> correction [B, S, H]
        own = h[:, self.receivers]                                # [B, S, D]
        hs = h[:, self.senders]                                   # [B, S, k, D]
        att = (self.k(hs) * self.q(own)[:, :, None]).sum(-1) / math.sqrt(self.dim)
        att = att.masked_fill(~self.has_sender[None], float("-inf"))
        alpha = torch.nan_to_num(torch.softmax(att.float(), dim=-1), nan=0.0).to(hs.dtype)   # a receiver with no sender: all zero
        agg = (alpha[..., None] * self.v(hs)).sum(2)              # [B, S, dim]
        return self.out(torch.cat([own, agg], dim=-1))


class STIDSpatial(STID):
    def __init__(self, num_nodes, horizon, clock, receivers=None, senders=None):
        super().__init__(num_nodes, horizon, clock)
        hidden = self.regression.in_features
        self.spatial = GatedSpatial(hidden, horizon, receivers, senders) if receivers is not None and len(receivers) else None

    def forward(self, values, feat):                              # the body of STID.forward, with the hidden state kept
        B, L, N = values.shape
        tod, dow = clock_indices(feat, self.clock)
        chan = torch.stack([values, (tod.float() / self.n_tod)[..., None].expand(B, L, N), (dow.float() / 7)[..., None].expand(B, L, N)], dim=-1)
        h = self.series(chan.permute(0, 2, 1, 3).reshape(B, N, L * 3))
        h = torch.cat([h, self.node_emb[None].expand(B, N, -1), self.tod_emb[tod[:, -1]][:, None].expand(B, N, -1),
                       self.dow_emb[dow[:, -1]][:, None].expand(B, N, -1)], dim=-1)
        for layer in self.layers:
            h = h + layer(h)
        y = self.regression(h)                                    # [B, N, H]
        if self.spatial is not None:
            corr = self.spatial(h)
            y = y.index_add(1, self.spatial.receivers, corr.to(y.dtype))
        return y.transpose(1, 2)                                  # [B, H, N]


def load_receivers(spec: dict, n: int, dataset: str):
    """(receivers or None, senders or None) of a genotype's ``spatial`` record."""
    name = spec["set"]
    if name == "none":
        return None, None
    root = REPO / spec["root"]
    table = np.load(root / "data" / f"{dataset}_senders.npy")
    if table.shape[0] != n:
        raise ValueError(f"sender table {table.shape} does not match {n} sensors")
    if name == "all":
        rec = np.arange(n)
    else:
        rec = np.asarray(json.load(open(root / "sets" / f"{name}.json"))["sensors"], dtype=np.int64)
        if len(rec) == 0 or rec.min() < 0 or rec.max() >= n or len(np.unique(rec)) != len(rec):
            raise ValueError(f"set {name}: {len(rec)} sensors, not distinct indices of 0..{n - 1}")
    return rec, table[rec, :int(spec.get("k", 16))]


class SpatialHandNet(nn.Module):
    """The interface of a discrete net of the pilot (as pilot.hand_models.HandNet) around STIDSpatial."""

    forecast_only = True
    backcast_loss_ration = 0.0

    def __init__(self, g: dict, dims: dict):
        super().__init__()
        self.num_nodes = int(dims["d_output"])
        dataset = str(dims["benchmark"]).rsplit("_", 1)[0]
        rec, snd = load_receivers(g["spatial"], self.num_nodes, dataset)
        self.body = STIDSpatial(self.num_nodes, int(dims["n_prediction_steps"]), g.get("clock", "true"), rec, snd)
        self.head = MAEHead()

    def forward(self, x_past, x_future=None):
        x = x_past[:, -IN_STEPS:]
        return self.body(x[..., :self.num_nodes], x[..., self.num_nodes:])

    def get_inference_prediction(self, prediction):
        return self.head.get_inference_pred(prediction)

    def get_training_loss(self, target, prediction):
        return self.head.loss(target, prediction)

    @torch.no_grad()
    def grad_norm(self):
        return sum(float(p.grad.detach().norm(2)) ** 2 for p in self.parameters() if p.grad is not None) ** 0.5

    def get_weight_optimizer_parameters(self, weight_decay: float):
        return [{"params": [p for p in self.parameters() if p.requires_grad], "weight_decay": weight_decay}]
