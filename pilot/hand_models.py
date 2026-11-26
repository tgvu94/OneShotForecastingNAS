"""Hand-designed reference models under the pilot pipeline: STID and STAEformer.

``build_hand_model(g, dims)`` returns a net with the interface that ``pilot.train_arch`` asks of a discrete net: ``forward(x_past,
x_future)`` on the pipeline tensors (x_past [B, W, N+F] = scaled targets and time features, x_future [B, H, F]), the MAE loss with the
zero mask, ``forecast_only``.  Only the model differs from a list architecture: the loader, the split, the scaler, the optimiser, the
schedule and the metric are those of the trainer.

A genotype record of a hand model: ``{"hand_model": "stid" | "staeformer", "clock": "pipeline" | "true", "head": "mae",
"graph": None, "space": "hand_v1"}``.  ``clock`` names the time features that the model reads:
  pipeline: the features of the loader as every list architecture gets them (the upstream PEMS loader counts one hour per step, so
            feature 0 has 24 values and feature 1 has 7; they are not the time of day and the day of the week of the data);
  true:     the loader is called with the frequency of the benchmark file, so the features are minute of hour, hour of day and day
            of week of the data clock (the series starts at midnight; the start date is not known, so the day of the week is right
            up to a fixed rotation, which an embedding does not see).
The model sizes are the published ones (STID: BasicTS ``baselines/STID/PEMS04.py``; STAEformer: the authors PEMS04 configuration);
both read the last 12 steps of the window, as published.
"""
from __future__ import annotations

import torch
import torch.nn as nn

from tsf_oneshot.prediction_heads.heads import _masked_l1

IN_STEPS = 12


class MAEHead(nn.Module):
    def loss(self, targets, predictions, mask=None):
        return _masked_l1(targets, predictions, mask)

    def get_inference_pred(self, predictions):
        return predictions


def _quant(x: torch.Tensor, n: int) -> torch.Tensor:
    """A time feature in [-0.5, 0.5] with n levels -> its level 0..n-1."""
    return torch.clamp(torch.round((x + 0.5) * (n - 1)), 0, n - 1).long()


def clock_indices(feat: torch.Tensor, clock: str):
    """feat [B, T, F] -> (time-of-day index, day-of-week index), each [B, T]."""
    if clock == "pipeline":                       # feature 0: 24 levels, feature 1: 7 levels
        return _quant(feat[..., 0], 24), _quant(feat[..., 1], 7)
    if clock == "true":                           # minute of hour (60), hour of day (24), day of week (7)
        return _quant(feat[..., 1], 24) * 60 + _quant(feat[..., 0], 60), _quant(feat[..., 2], 7)
    if clock == "index":                          # feature 0: the step of the day (288 steps of 5 minutes), feature 1: the day of the week
        return feat[..., 0].round().long(), feat[..., 1].round().long()
    if clock == "none":                           # no time feature: one constant level
        z = torch.zeros(feat.shape[:2], dtype=torch.long, device=feat.device)
        return z, z
    raise ValueError(f"unknown clock {clock}")


N_TOD = {"pipeline": 24, "true": 24 * 60, "index": 288, "none": 1}


class STID(nn.Module):
    """Shao et al. 2022.  Three channels per step (value, time of day, day of week) flattened per node, plus a node embedding and
    the embeddings of the last time of day and day of week; three residual MLP layers; one linear regression to the horizon."""

    def __init__(self, num_nodes, horizon, clock, node_dim=32, embed_dim=32, temp_dim=32, num_layer=3, dropout=0.15):
        super().__init__()
        self.clock, self.n_tod = clock, N_TOD[clock]
        self.node_emb = nn.Parameter(torch.empty(num_nodes, node_dim)); nn.init.xavier_uniform_(self.node_emb)
        self.tod_emb = nn.Parameter(torch.empty(self.n_tod, temp_dim)); nn.init.xavier_uniform_(self.tod_emb)
        self.dow_emb = nn.Parameter(torch.empty(7, temp_dim)); nn.init.xavier_uniform_(self.dow_emb)
        self.series = nn.Linear(3 * IN_STEPS, embed_dim)
        hidden = embed_dim + node_dim + 2 * temp_dim
        self.layers = nn.ModuleList(nn.Sequential(nn.Linear(hidden, hidden), nn.ReLU(), nn.Dropout(dropout), nn.Linear(hidden, hidden))
                                    for _ in range(num_layer))
        self.regression = nn.Linear(hidden, horizon)

    def forward(self, values, feat):              # values [B, L, N], feat [B, L, F]
        B, L, N = values.shape
        tod, dow = clock_indices(feat, self.clock)
        chan = torch.stack([values, (tod.float() / self.n_tod)[..., None].expand(B, L, N), (dow.float() / 7)[..., None].expand(B, L, N)], dim=-1)
        h = self.series(chan.permute(0, 2, 1, 3).reshape(B, N, L * 3))                       # [B, N, E]
        h = torch.cat([h, self.node_emb[None].expand(B, N, -1), self.tod_emb[tod[:, -1]][:, None].expand(B, N, -1),
                       self.dow_emb[dow[:, -1]][:, None].expand(B, N, -1)], dim=-1)
        for layer in self.layers:
            h = h + layer(h)
        return self.regression(h).transpose(1, 2)                                            # [B, H, N]


class _SelfAttention(nn.Module):
    def __init__(self, dim, ff, heads, dropout):
        super().__init__()
        self.attn = nn.MultiheadAttention(dim, heads, batch_first=True)
        self.ff = nn.Sequential(nn.Linear(dim, ff), nn.ReLU(), nn.Linear(ff, dim))
        self.n1, self.n2, self.drop = nn.LayerNorm(dim), nn.LayerNorm(dim), nn.Dropout(dropout)

    def forward(self, x):                         # [batch, sequence, dim]
        x = self.n1(x + self.drop(self.attn(x, x, x, need_weights=False)[0]))
        return self.n2(x + self.drop(self.ff(x)))


class STAEformer(nn.Module):
    """Liu et al. 2023.  A linear input embedding with the embeddings of the time of day and the day of week and an adaptive
    embedding per (step, node); three attention layers along time, three along the nodes; one linear regression to the horizon."""

    def __init__(self, num_nodes, horizon, clock, in_dim=24, tod_dim=24, dow_dim=24, adp_dim=80, ff=256, heads=4, num_layers=3, dropout=0.1):
        super().__init__()
        self.clock, self.n_tod = clock, N_TOD[clock]
        self.input_proj = nn.Linear(3, in_dim)
        self.tod_emb, self.dow_emb = nn.Embedding(self.n_tod, tod_dim), nn.Embedding(7, dow_dim)
        self.adaptive = nn.Parameter(torch.empty(IN_STEPS, num_nodes, adp_dim)); nn.init.xavier_uniform_(self.adaptive)
        dim = in_dim + tod_dim + dow_dim + adp_dim
        self.time_layers = nn.ModuleList(_SelfAttention(dim, ff, heads, dropout) for _ in range(num_layers))
        self.node_layers = nn.ModuleList(_SelfAttention(dim, ff, heads, dropout) for _ in range(num_layers))
        self.regression = nn.Linear(IN_STEPS * dim, horizon)

    def forward(self, values, feat):
        B, L, N = values.shape
        tod, dow = clock_indices(feat, self.clock)
        chan = torch.stack([values, (tod.float() / self.n_tod)[..., None].expand(B, L, N), (dow.float() / 7)[..., None].expand(B, L, N)], dim=-1)
        h = torch.cat([self.input_proj(chan), self.tod_emb(tod)[:, :, None].expand(B, L, N, -1), self.dow_emb(dow)[:, :, None].expand(B, L, N, -1),
                       self.adaptive[None].expand(B, L, N, -1)], dim=-1)                      # [B, L, N, D]
        D = h.shape[-1]
        h = h.transpose(1, 2).reshape(B * N, L, D)
        for layer in self.time_layers:
            h = layer(h)
        h = h.reshape(B, N, L, D).transpose(1, 2).reshape(B * L, N, D)
        for layer in self.node_layers:
            h = layer(h)
        h = h.reshape(B, L, N, D).transpose(1, 2).reshape(B, N, L * D)
        return self.regression(h).transpose(1, 2)                                            # [B, H, N]


class HandNet(nn.Module):
    """The interface of a discrete net of the pilot around one hand model."""

    forecast_only = True
    backcast_loss_ration = 0.0

    def __init__(self, name: str, clock: str, dims: dict):
        super().__init__()
        self.num_nodes = int(dims["d_output"])
        cls = {"stid": STID, "staeformer": STAEformer}[name]
        self.body = cls(self.num_nodes, int(dims["n_prediction_steps"]), clock)
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


class ReleaseNet(nn.Module):
    """A hand model behind the interface of the AutoCTS++ network (pilot.autoctspp_run): the input is [B, C, N, T] with the scaled
    value in channel 0 and, for the clock "index", the step of the day and the day of the week in channels 1 and 2; the output is
    [B, H, N, 1] in the scaled unit.  The clock "none" reads channel 0 only."""

    def __init__(self, name: str, clock: str, num_nodes: int, horizon: int):
        super().__init__()
        self.body = {"stid": STID, "staeformer": STAEformer}[name](num_nodes, horizon, clock)

    def forward(self, x):
        values = x[:, 0].transpose(1, 2)                                                     # [B, T, N]
        feat = x[:, 1:3, 0].transpose(1, 2) if x.shape[1] >= 3 else values.new_zeros(values.shape[0], values.shape[1], 2)
        return self.body(values[:, -IN_STEPS:], feat[:, -IN_STEPS:]).unsqueeze(-1)


def build_hand_model(g: dict, dims: dict):
    if g["hand_model"] == "stid_spatial":         # STID with a spatial module for a set of receiver sensors (pilot.spatialgate_model)
        from pilot.spatialgate_model import SpatialHandNet
        return SpatialHandNet(g, dims)
    return HandNet(g["hand_model"], g.get("clock", "pipeline"), dims)
