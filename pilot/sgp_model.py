"""The parts of SGP [cini2023sgp] that the runner pilot/sgp_run.py calls (Survey/experiments/sgp-plan.md).

Ported from github.com/Graph-Machine-Learning-Group/sgp at commit ae1abd5 (MIT licence, Copyright (c) 2022 Graph Machine
Learning Group).  The release needs einops, PyTorch Geometric, torch_sparse and its bundled library; none of them is in the
nas venv.  Each class names the file of the release that it follows.  `python -m pilot.sgp_run check` compares the reservoir
of this file with the source of the release (the same seed gives the same weights and the same states).  The readout blocks
are ported by reading; no run of the release checks them.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class ReservoirLayer(nn.Module):
    """lib/nn/reservoir/reservoir.py, ReservoirLayer: fixed random weights, leaky tanh update.  The order of the random
    draws is the order of the release."""

    def __init__(self, input_size, hidden_size, spectral_radius, leaking_rate, density=1.0, in_scaling=1.0, bias_scale=1.0):
        super().__init__()
        self.hidden_size, self.alpha = hidden_size, float(leaking_rate)
        self.w_ih = nn.Parameter(torch.empty(hidden_size, input_size).uniform_(-1, 1).mul_(in_scaling), requires_grad=False)
        self.b_ih = nn.Parameter(torch.empty(hidden_size).uniform_(-1, 1).mul_(bias_scale), requires_grad=False)
        w = torch.empty(hidden_size, hidden_size).uniform_(-1, 1)
        if density < 1:
            n_units = hidden_size * hidden_size
            mask = w.new_ones(n_units)
            mask[torch.randperm(n_units)[:int(n_units * (1 - density))]] = 0.0
            w.mul_(mask.view(hidden_size, hidden_size))
        w.mul_(spectral_radius / torch.max(torch.linalg.eigvals(w).abs()))
        self.w_hh = nn.Parameter(w, requires_grad=False)

    def forward(self, x, h):
        h_new = torch.tanh(F.linear(x, self.w_ih, self.b_ih) + F.linear(h, self.w_hh))
        return (1 - self.alpha) * h + self.alpha * h_new


def _alphas(leaking_rate, num_layers, alpha_decay):
    out, alpha = [], leaking_rate
    for _ in range(num_layers):
        out.append(float(alpha))
        if alpha_decay:
            alpha = np.clip(alpha - 0.1, 0.1, 1.0)
    return out


class Reservoir(nn.Module):
    """lib/nn/reservoir/reservoir.py, Reservoir: a stack of layers, one state per sensor; the states of the layers are
    concatenated layer by layer."""

    def __init__(self, input_size, hidden_size, num_layers=1, leaking_rate=0.9, spectral_radius=0.9, density=0.7,
                 alpha_decay=True, input_scaling=1.0):
        super().__init__()
        self.hidden_size = hidden_size
        self.reservoir_layers = nn.ModuleList([
            ReservoirLayer(input_size if i == 0 else hidden_size, hidden_size, spectral_radius, a, density, input_scaling)
            for i, a in enumerate(_alphas(leaking_rate, num_layers, alpha_decay))])

    @property
    def out_size(self):
        return self.hidden_size * len(self.reservoir_layers)

    @torch.no_grad()
    def encode(self, x, adj=None):
        """x [steps, sensors, features] -> states [steps, sensors, layers * hidden]; the state before the first step is 0."""
        steps, n, _ = x.shape
        out = torch.empty(steps, n, self.out_size, dtype=x.dtype, device=x.device)
        h = [x.new_zeros(n, self.hidden_size) for _ in self.reservoir_layers]
        for s in range(steps):
            x_s = x[s]
            for i, layer in enumerate(self.reservoir_layers):
                h[i] = x_s = layer(x_s, h[i]) if adj is None else layer(x_s, h[i], adj)
            out[s] = torch.cat(h, -1)
        return out


class GESNLayer(ReservoirLayer):
    """lib/nn/reservoir/graph_reservoir.py, GESNLayer: the graph acts inside the recurrence."""

    def forward(self, x, h, adj):
        h_new = torch.tanh(F.linear(x, self.w_ih, self.b_ih) + adj @ F.linear(h, self.w_hh))
        return (1 - self.alpha) * h + self.alpha * h_new


class GraphReservoir(Reservoir):
    """lib/nn/reservoir/graph_reservoir.py, GraphESN (the DynGESN baseline of the paper)."""

    def __init__(self, input_size, hidden_size, num_layers=1, leaking_rate=0.9, spectral_radius=0.9, density=1.0,
                 alpha_decay=True, input_scaling=1.0):
        nn.Module.__init__(self)
        self.hidden_size = hidden_size
        self.reservoir_layers = nn.ModuleList([
            GESNLayer(input_size if i == 0 else hidden_size, hidden_size, spectral_radius, a, density, input_scaling)
            for i, a in enumerate(_alphas(leaking_rate, num_layers, alpha_decay))])


def row_norm(m: torch.Tensor) -> torch.Tensor:
    inv = m.sum(1).pow(-1.0)
    inv[torch.isinf(inv)] = 0
    return inv.view(-1, 1) * m


def supports(adj: torch.Tensor):
    """lib/sgp_preprocessing.py, preprocess_adj with the two directions of sgp_spatial_embedding.  adj[i, j] is the weight
    of the edge from i to j, with no diagonal.  The forward operator is the row-normalised transpose; the backward operator
    is the row-normalised matrix."""
    return row_norm(adj.t().contiguous()), row_norm(adj)


def gesn_support(adj_with_diag: torch.Tensor) -> torch.Tensor:
    """lib/nn/encoders/dyn_gesn_encoder.py: self loops of weight 1 are added to the graph that already holds its diagonal,
    then the incoming weights of each sensor are normalised to sum 1."""
    a = adj_with_diag + torch.eye(len(adj_with_diag), dtype=adj_with_diag.dtype, device=adj_with_diag.device)
    return row_norm(a.t().contiguous())


def expand(h, p, q, k: int, global_attr: bool, rows=None):
    """lib/sgp_preprocessing.py, sgp_spatial_embedding, and lib/nn/encoders/sgp_spatial_encoder.py: h [b, n, f] ->
    [b, n, f * (1 + 2k + global)]: the states, k powers of the forward operator, k powers of the backward operator, the
    mean over the sensors.  rows selects output sensors (then p and q are lists of the powers, rows already selected)."""
    if rows is None:
        out, x = [h], h
        for _ in range(k):
            x = torch.einsum('ij,bjf->bif', p, x)
            out.append(x)
        x = h
        for _ in range(k):
            x = torch.einsum('ij,bjf->bif', q, x)
            out.append(x)
        if global_attr:
            out.append(h.mean(-2, keepdim=True).expand_as(h))
        return torch.cat(out, -1)
    out = [h[:, rows]]
    out += [torch.einsum('ij,bjf->bif', m, h) for m in p[:k]] + [torch.einsum('ij,bjf->bif', m, h) for m in q[:k]]
    if global_attr:
        out.append(h.mean(-2, keepdim=True).expand(-1, len(rows), -1))
    return torch.cat(out, -1)


def powers(m: torch.Tensor, k: int, rows) -> list:
    out, x = [], m
    for _ in range(k):
        out.append(x[rows].contiguous())
        x = m @ x
    return out


class SGPReadout(nn.Module):
    """lib/nn/models/sgp_model.py, SGPModel with resnet=True and fully_connected=False, and the blocks of the bundled
    library (tsl/nn/base/dense.py, tsl/nn/blocks/encoders/mlp.py ResidualMLP with parametrized_skip, tsl/nn/base/embedding.py
    with the uniform initialiser, tsl/nn/blocks/decoders/linear_readout.py).  x [b, n, f], u [b, n, exog] -> [b, n, horizon]."""

    def __init__(self, input_size, order, n_nodes, hidden_size=960, mlp_size=256, horizon=12, n_layers=2, dropout=0.3,
                 emb_size=32, node_emb=True, exog_size=1):
        super().__init__()
        out_ch = hidden_size - hidden_size % order
        self.conv = nn.Conv1d(input_size, out_ch, kernel_size=1, groups=order)
        self.drop = nn.Dropout(dropout)
        if node_emb:
            bound = 1.0 / np.sqrt(emb_size)
            self.emb = nn.Parameter(torch.empty(n_nodes, emb_size).uniform_(-bound, bound))
            self.lin_emb = nn.Linear(emb_size, out_ch)
        else:
            self.emb = None
        sizes = [out_ch + exog_size] + [mlp_size] * n_layers
        self.layers = nn.ModuleList([
            nn.Sequential(nn.Linear(sizes[i], mlp_size), nn.SiLU(), nn.Dropout(dropout), nn.Linear(mlp_size, mlp_size))
            for i in range(n_layers)])
        self.skips = nn.ModuleList([nn.Linear(sizes[i], mlp_size) for i in range(n_layers)])
        self.out = nn.Linear(mlp_size, horizon)

    def forward(self, x, u):
        x = self.drop(F.silu(self.conv(x.transpose(1, 2)).transpose(1, 2)))
        if self.emb is not None:
            x = x + self.lin_emb(self.emb)
        x = torch.cat([x, u], -1)
        for layer, skip in zip(self.layers, self.skips):
            x = layer(x) + skip(x)
        return self.out(x)


class LinearReadout(nn.Module):
    """One linear layer on the embedding and the scaled value (not in the release; form R2 of the plan)."""

    def __init__(self, input_size, horizon=12, exog_size=1):
        super().__init__()
        self.out = nn.Linear(input_size + exog_size, horizon)

    def forward(self, x, u):
        return self.out(torch.cat([x, u], -1))
