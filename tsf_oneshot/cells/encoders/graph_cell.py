"""``GraphCell``: a DARTS-style DAG over the four graph operators, same edge encoding as ``SampledEncoderCell``.

Edges are enumerated ``for i in range(n_input_nodes, n_input_nodes + n_nodes): for j in range(i)`` (index k);
``operations[k]`` indexes ``PRIMITIVES`` and ``has_edges[k]`` switches the edge on.  Each intermediate node is
the sum of its incoming edge outputs; nodes that are not connected to the last (output) node are pruned with the
repo's ``check_node_is_connected_to_out``; the cell output is the last node.
"""
from __future__ import annotations

import torch
from torch import nn

from tsf_oneshot.cells.encoders.graph_components import GRAPH_OPS
from tsf_oneshot.cells.utils import check_node_is_connected_to_out


class GraphCell(nn.Module):
    def __init__(self, n_nodes: int, n_input_nodes: int, channels: int, n_graph_nodes: int,
                 operations: list[int], has_edges: list[bool], PRIMITIVES: list[str]):
        super().__init__()
        self.n_input_nodes, self.max_nodes = n_input_nodes, n_input_nodes + n_nodes
        self.edges = nn.ModuleDict()
        k = 0
        for i in range(n_input_nodes, self.max_nodes):
            for j in range(i):
                if has_edges[k]:
                    self.edges[f"{i}<-{j}"] = GRAPH_OPS[PRIMITIVES[operations[k]]](channels, n_graph_nodes)
                k += 1
        assert k == len(operations) == len(has_edges), (k, len(operations), len(has_edges))
        nodes_to_remove = set(range(n_input_nodes, self.max_nodes - 1))
        for i in range(n_input_nodes, self.max_nodes - 1):
            check_node_is_connected_to_out(i, n_nodes_max=self.max_nodes, nodes_to_remove=nodes_to_remove, edges=self.edges)
        for edge in list(self.edges):
            a, b = (int(v) for v in edge.split("<-"))
            if a in nodes_to_remove or b in nodes_to_remove:
                self.edges.pop(edge)
        self.pruned_nodes = sorted(nodes_to_remove)

    def forward(self, inputs: list[torch.Tensor], pack: dict) -> torch.Tensor:
        states = list(inputs)
        assert len(states) == self.n_input_nodes
        for i in range(self.n_input_nodes, self.max_nodes):
            acc = None
            for j in range(i):
                key = f"{i}<-{j}"
                if key in self.edges:
                    out = self.edges[key](states[j], pack)
                    acc = out if acc is None else acc + out
            states.append(acc if acc is not None else states[-1])
        return states[-1]
