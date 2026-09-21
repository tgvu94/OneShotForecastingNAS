"""Graph Net family for the pilot: ``GraphForecastNet`` (a third parallel forecaster on the raw window) and
``MixedConcatGraphSampledNet`` (Seq + Flat + Graph, combined as softmax(w) . [f_flat, f_seq, f_graph]).

``GraphForecastNet.forward(x_past, x_future) -> (B, H, N)`` takes the same inputs as the Seq/Flat nets:
``x_past`` (B, T, N + F) = scaled past targets + past time features, ``x_future`` (B, H, F) is unused.
The adjacency tensors are non-persistent buffers, so ``set_adjacency`` swaps them for Experiment B without
touching the state dict.
"""
from __future__ import annotations

import copy

import numpy as np
import torch
from torch import nn

from pilot.adjacency import adj_pack
from tsf_oneshot.cells.encoders.graph_cell import GraphCell
from tsf_oneshot.cells.encoders.graph_components import GRAPH_PRIMITIVES
from tsf_oneshot.networks.combined_net_utils import forward_concat_graph_net
from tsf_oneshot.networks.sampled_net import MixedConcatSampledNet

PACK_KEYS = ("A", "gcn", "p_fwd", "p_bwd")


class GraphForecastNet(nn.Module):
    def __init__(self, d_output: int, n_time_features: int, window_size: int, forecasting_horizon: int,
                 channels: int, n_cells: int, n_nodes: int, n_cell_input_nodes: int,
                 operations: list[int], has_edges: list[bool], PRIMITIVES: list[str], adjacency: np.ndarray):
        super().__init__()
        assert n_cell_input_nodes == 1, "the pilot graph cell takes one input node"
        self.d_output, self.n_time_features = d_output, n_time_features
        self.window_size, self.forecasting_horizon, self.channels = window_size, forecasting_horizon, channels
        self.embed = nn.Linear(1 + n_time_features, channels)
        self.cells = nn.ModuleList([
            GraphCell(n_nodes, n_cell_input_nodes, channels, d_output, operations, has_edges, PRIMITIVES)
            for _ in range(n_cells)])
        self.time_head = nn.Linear(window_size, forecasting_horizon)
        self.chan_head = nn.Linear(channels, 1)
        for k in PACK_KEYS:
            self.register_buffer(f"adj_{k}", torch.zeros(d_output, d_output), persistent=False)
        self.set_adjacency(adjacency)

    @torch.no_grad()
    def set_adjacency(self, A: np.ndarray) -> None:
        assert A.shape == (self.d_output, self.d_output), A.shape
        pack = adj_pack(np.asarray(A, dtype=np.float32))
        for k in PACK_KEYS:
            getattr(self, f"adj_{k}").copy_(pack[k].to(getattr(self, f"adj_{k}").device))

    @property
    def pack(self) -> dict:
        return {k: getattr(self, f"adj_{k}") for k in PACK_KEYS}

    def forward(self, x_past: torch.Tensor, x_future: torch.Tensor | None = None) -> torch.Tensor:
        B, T, _ = x_past.shape
        N = self.d_output
        targets = x_past[:, :, :N].unsqueeze(-1)                                     # (B, T, N, 1)
        feats = x_past[:, :, N:].unsqueeze(2).expand(B, T, N, self.n_time_features)  # (B, T, N, F)
        h = self.embed(torch.cat([targets, feats], dim=-1))                          # (B, T, N, C)
        pack = self.pack
        for cell in self.cells:
            h = cell([h], pack)
        h = self.time_head(h.permute(0, 2, 3, 1))          # (B, N, C, H)
        h = self.chan_head(h.permute(0, 1, 3, 2)).squeeze(-1)  # (B, N, H)
        return h.permute(0, 2, 1)                          # (B, H, N)


class MixedConcatGraphSampledNet(MixedConcatSampledNet):
    """MixedConcatSampledNet + GraphForecastNet; three learnable net weights through a softmax (init equal)."""

    def __init__(self, graph: dict, adjacency: np.ndarray, **kwargs):
        super().__init__(**kwargs)
        graph = dict(graph)
        self.meta_info["graph"] = copy.deepcopy(graph)
        self.graph_net = GraphForecastNet(
            d_output=kwargs["d_output"], n_time_features=kwargs["d_input_past"] - kwargs["d_output"],
            window_size=kwargs["window_size"], forecasting_horizon=kwargs["forecasting_horizon"],
            channels=int(graph["channels"]), n_cells=int(graph["n_cells"]), n_nodes=int(graph["n_nodes"]),
            n_cell_input_nodes=int(graph["n_cell_input_nodes"]), operations=list(graph["operations"]),
            has_edges=list(graph["has_edges"]), PRIMITIVES=list(graph.get("PRIMITIVES", GRAPH_PRIMITIVES)),
            adjacency=adjacency)
        nets_weights = list(kwargs["nets_weights"])
        assert len(nets_weights) == 3, "graph nets need three net weights (flat, seq, graph)"
        self.nets_weights = nn.Parameter(torch.tensor(nets_weights, dtype=torch.float32), requires_grad=True)
        if not self.seq_net.forecast_only:
            raise NotImplementedError("the graph net only supports forecast_only seq nets (backcast_loss_ration_seq == 0)")

    def transform_nets_weights(self):
        return torch.softmax(self.nets_weights, dim=0)

    def forward(self, x_past: torch.Tensor, x_future: torch.Tensor):
        return forward_concat_graph_net(
            flat_net=self.flat_net, seq_net=self.seq_net, graph_net=self.graph_net,
            x_past=x_past, x_future=x_future, decompose=self.decompose,
            out_weights=self.transform_nets_weights())
