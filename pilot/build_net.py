"""``build_discrete_net(genotype, dims) -> MixedConcatSampledNet``.

Mirrors the ``mixed_concat`` branch of ``experiments/test_evaluated_model.py`` line for line, so the discrete
net the pilot trains is the one the repo's own paper trained; only the operator choices come from the genotype
instead of from ``opt_arch_weights.pth``.
"""
from __future__ import annotations

from tsf_oneshot.networks.sampled_net import MixedConcatSampledNet

from pilot.genotype import edges_to_lists, load_space


def net_init_kwargs(g: dict, dims: dict) -> dict:
    if g.get("graph") is not None:
        raise NotImplementedError("graph family is added in W3; this space is graph-blind")
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


def build_discrete_net(g: dict, dims: dict) -> MixedConcatSampledNet:
    return MixedConcatSampledNet(**net_init_kwargs(g, dims))


def count_params(net) -> int:
    return int(sum(p.numel() for p in net.parameters() if p.requires_grad))
