"""Graph operators for the pilot's Graph Net family (Section 1, Option 1).

Common interface: ``forward(x: (B, T, N, C), pack: dict) -> (B, T, N, C)`` where ``pack`` holds the adjacency
tensors built by ``pilot.adjacency.adj_pack`` (``A``, ``gcn``, ``p_fwd``, ``p_bwd``).  Every op that mixes nodes
is residual (``x + relu(W . mix(x))``) so that a randomly sampled cell stays trainable; ``nn.ReLU`` modules are
used (not ``F.relu``) so that NASWOT-style hooks fire.
"""
from __future__ import annotations

import torch
from torch import nn


def _mix(M: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
    """(N, N) x (B, T, N, C) -> (B, T, N, C): out[b,t,n,:] = sum_m M[n,m] x[b,t,m,:]."""
    return torch.einsum("nm,btmc->btnc", M.to(x.dtype), x)


class GraphIdentity(nn.Module):
    uses_adjacency = False

    def forward(self, x: torch.Tensor, pack: dict) -> torch.Tensor:
        return x


class GCNOp(nn.Module):
    """Kipf & Welling: A_hat X W per time step, A_hat = D^-1/2 (A+I) D^-1/2."""
    uses_adjacency = True

    def __init__(self, channels: int):
        super().__init__()
        self.lin = nn.Linear(channels, channels)
        self.act = nn.ReLU()

    def forward(self, x: torch.Tensor, pack: dict) -> torch.Tensor:
        return x + self.act(self.lin(_mix(pack["gcn"], x)))


class DiffusionConvOp(nn.Module):
    """DCRNN-style diffusion convolution: sum_{dir in fwd,bwd} sum_{k=1..K} (P_dir^k X) W_{dir,k}, K = 2."""
    uses_adjacency = True

    def __init__(self, channels: int, K: int = 2):
        super().__init__()
        self.K = K
        self.lins = nn.ModuleList([nn.Linear(channels, channels, bias=(d == 0 and k == 0)) for d in range(2) for k in range(K)])
        self.act = nn.ReLU()

    def forward(self, x: torch.Tensor, pack: dict) -> torch.Tensor:
        out = None
        for d, key in enumerate(("p_fwd", "p_bwd")):
            h = x
            for k in range(self.K):
                h = _mix(pack[key], h)
                term = self.lins[d * self.K + k](h)
                out = term if out is None else out + term
        return x + self.act(out)


class AdaptiveAdjOp(nn.Module):
    """Graph WaveNet self-adaptive adjacency: A_adp = softmax(relu(E1 E2^T)), E1, E2 in R^{N x 10}; ignores ``pack``."""
    uses_adjacency = False

    def __init__(self, channels: int, n_graph_nodes: int, emb_dim: int = 10):
        super().__init__()
        self.E1 = nn.Parameter(torch.randn(n_graph_nodes, emb_dim))
        self.E2 = nn.Parameter(torch.randn(n_graph_nodes, emb_dim))
        self.lin = nn.Linear(channels, channels)
        self.act = nn.ReLU()
        self.act_adj = nn.ReLU()

    def adaptive_adjacency(self) -> torch.Tensor:
        return torch.softmax(self.act_adj(self.E1 @ self.E2.t()), dim=1)

    def forward(self, x: torch.Tensor, pack: dict) -> torch.Tensor:
        return x + self.act(self.lin(_mix(self.adaptive_adjacency(), x)))


GRAPH_OPS = {
    "graph_identity": lambda channels, n_graph_nodes: GraphIdentity(),
    "gcn": lambda channels, n_graph_nodes: GCNOp(channels),
    "diffusion": lambda channels, n_graph_nodes: DiffusionConvOp(channels, K=2),
    "adaptive": lambda channels, n_graph_nodes: AdaptiveAdjOp(channels, n_graph_nodes),
}
GRAPH_PRIMITIVES = list(GRAPH_OPS)
