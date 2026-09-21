"""``build_discrete_net(genotype, dims) -> MixedConcatSampledNet | MixedConcatGraphSampledNet``.

Mirrors the ``mixed_concat`` branch of ``experiments/test_evaluated_model.py`` line for line, so the discrete
net the pilot trains is the one the repo's own paper trained; only the operator choices come from the genotype
instead of from ``opt_arch_weights.pth``.  A genotype with a non-null ``graph`` cell gets the P3 graph net as a
third forecaster, built on the adjacency of the setting: ``adj_path`` if given, else the conventional file of the
setting the ``dims`` came from (``dims['benchmark']`` = 'pems04_12' -> results/data/pems04_adj.npy,
'pems08_12' -> results/pems08_h12/data/pems08_adj.npy).  The adjacency must be (d_output, d_output).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from tsf_oneshot.networks.sampled_net import MixedConcatSampledNet

from pilot.adjacency import DEFAULT_ADJ, load_adj
from pilot.genotype import edges_to_lists, load_space
from pilot.paths import default_adj_for_dims

_ADJ_CACHE: dict = {}


def get_adjacency(path: str | Path = DEFAULT_ADJ) -> np.ndarray:
    path = str(path)
    if path not in _ADJ_CACHE:
        _ADJ_CACHE[path] = load_adj(path)
    return _ADJ_CACHE[path]


def net_init_kwargs(g: dict, dims: dict) -> dict:
    sp = load_space(g["space"])
    s, f, hp = sp["seq"], sp["flat"], g["hparams"]
    ops_enc, has_enc = edges_to_lists(g["seq"]["encoder"], s["PRIMITIVES_encoder"])
    ops_dec, has_dec = edges_to_lists(g["seq"]["decoder"], s["PRIMITIVES_decoder"])
    ops_flat, has_flat = edges_to_lists(g["flat"]["cell"], f["PRIMITIVES_encoder"])
    if g["seq"]["decoder_type"] == "seq" and has_dec != has_enc:
        raise ValueError("seq decoder topology must equal the encoder topology")
    ops_kwargs_seq = dict(s["ops_kwargs"])
    ops_kwargs_seq.update(s["model_kwargs"])
    ops_kwargs_flat = dict(f["ops_kwargs"])
    ops_kwargs_flat.update(f["model_kwargs"])
    return dict(
        d_input_past=dims["d_input_past"],
        d_input_future=dims["d_input_future"],
        d_output=dims["d_output"],
        d_model=int(hp["d_model"]),
        n_cells_seq=int(hp["n_cells_seq"]),
        n_nodes_seq=int(hp["n_nodes_seq"]),
        n_cell_input_nodes_seq=int(hp["n_cell_input_nodes_seq"]),
        operations_encoder_seq=ops_enc,
        has_edges_encoder_seq=has_enc,
        operations_decoder_seq=ops_dec,
        has_edges_decoder_seq=has_dec,
        PRIMITIVES_encoder_seq=list(s["PRIMITIVES_encoder"]),
        PRIMITIVES_decoder_seq=list(s["PRIMITIVES_decoder"]),
        DECODER_seq=g["seq"]["decoder_type"],
        OPS_kwargs_seq=ops_kwargs_seq,
        backcast_loss_ration_seq=float(s["backcast_loss_ration"]),
        window_size=dims["window_size"],
        forecasting_horizon=dims["n_prediction_steps"],
        n_cells_flat=int(hp["n_cells_flat"]),
        n_nodes_flat=int(hp["n_nodes_flat"]),
        n_cell_input_nodes_flat=int(hp["n_cell_input_nodes_flat"]),
        operations_encoder_flat=ops_flat,
        has_edges_encoder_flat=has_flat,
        PRIMITIVES_encoder_flat=list(f["PRIMITIVES_encoder"]),
        OPS_kwargs_flat=ops_kwargs_flat,
        nets_weights=[float(w) for w in hp["nets_weights"]],
        HEAD=g["head"],
        HEADs_kwargs_seq=dict(s["head_kwargs"]),
        HEADs_kwargs_flat=dict(f["head_kwargs"]),
        backcast_loss_ration_flat=float(f["backcast_loss_ration"]),
    )


def graph_init_kwargs(g: dict) -> dict:
    sp = load_space(g["space"])
    gsp, hp = sp["graph"], g["hparams"]
    ops, has = edges_to_lists(g["graph"]["cell"], gsp["PRIMITIVES"])
    return dict(channels=int(hp["graph_channels"]), n_cells=int(hp["n_cells_graph"]), n_nodes=int(hp["n_nodes_graph"]),
                n_cell_input_nodes=int(hp["n_cell_input_nodes_graph"]), operations=ops, has_edges=has,
                PRIMITIVES=list(gsp["PRIMITIVES"]))


def build_discrete_net(g: dict, dims: dict, adjacency: np.ndarray | None = None, adj_path: str | Path | None = None):
    kwargs = net_init_kwargs(g, dims)
    if g.get("graph") is None:
        return MixedConcatSampledNet(**kwargs)
    from tsf_oneshot.networks.graph_net import MixedConcatGraphSampledNet

    A = adjacency if adjacency is not None else get_adjacency(adj_path or default_adj_for_dims(dims))
    n = int(dims["d_output"])
    if tuple(A.shape) != (n, n):
        raise ValueError(f"adjacency {tuple(A.shape)} does not match d_output = {n} of benchmark {dims.get('benchmark')}")
    return MixedConcatGraphSampledNet(graph=graph_init_kwargs(g), adjacency=A, **kwargs)


def count_params(net) -> int:
    return int(sum(p.numel() for p in net.parameters() if p.requires_grad))
