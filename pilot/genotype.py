"""Genotype = one discrete DARTS-TS architecture, JSON-serialisable, hashed to an ``arch_id``.

The encoding mirrors ``tsf_oneshot.networks.sampled_net.MixedConcatSampledNet`` (verified P1, 2026-09-20):

* one flat edge list per cell type, in the k-order of ``SampledEncoderCell.__init__``::

      for i in range(n_input_nodes, n_input_nodes + n_nodes):
          for j in range(i):            # edge "i<-j", index k

  entry k is ``[i, j, op_name]`` or ``[i, j, None]`` (``has_edges[k] == False``);
* the same list is shared by all ``n_cells`` cells of that type (the repo passes one
  ``operations``/``has_edges`` pair to every cell);
* the seq decoder shares the encoder topology.  All 9 shipped PEMS architectures have
  ``mask_encoder_seq == mask_decoder_seq`` and ``SampledDecoderCell.get_edge_out`` reads
  ``cell_encoder_output[node_str]``, so a decoder-only edge would raise ``KeyError``;
* edges of nodes that ``SampledEncoderCell`` prunes (not connected to the cell output, using the
  repo's own ``check_node_is_connected_to_out``) are set to ``None`` by :func:`canonicalize`, so one
  ``arch_id`` corresponds to exactly one built network.

Genotype schema::

    {"space": "dartsts_v1" | "dartsts_graph_v1",
     "seq":  {"encoder": [[i, j, op | null], ...], "decoder": [[i, j, op | null], ...],
              "decoder_type": "seq" | "linear"},
     "flat": {"cell": [[i, j, op | null], ...]},
     "graph": {"cell": [[i, j, op | null], ...]} | null,   # P3: graph cell (ops in GRAPH_PRIMITIVES); null = graph-blind
     "head": "quantile" | "mse" | "mae",
     "hparams": {"d_model", "n_cells_seq", "n_nodes_seq", "n_cell_input_nodes_seq",
                 "n_cells_flat", "n_nodes_flat", "n_cell_input_nodes_flat", "nets_weights",
                 + (graph only) "n_cells_graph", "n_nodes_graph", "n_cell_input_nodes_graph", "graph_channels"}}

``dartsts_graph_v1`` = ``dartsts_v1`` + the graph cell; a genotype with ``graph: null`` in the graph space
builds exactly the same network as in ``dartsts_v1`` but hashes differently (the space string is part of the id).
"""
from __future__ import annotations

import copy
import hashlib
import json
import random
from pathlib import Path

from omegaconf import OmegaConf

from tsf_oneshot.cells.utils import check_node_is_connected_to_out

REPO = Path(__file__).resolve().parents[1]
SPACE_V1 = "dartsts_v1"
SPACE_GRAPH_V1 = "dartsts_graph_v1"
_MODEL_YAML = REPO / "experiments" / "configs" / "model" / "mixed_concat_darts.yaml"
SPACES = {SPACE_V1: _MODEL_YAML, SPACE_GRAPH_V1: _MODEL_YAML}
GRAPH_PRIMITIVES = ["graph_identity", "gcn", "diffusion", "adaptive"]
GRAPH_HPARAMS = {"n_cells_graph": 1, "n_nodes_graph": 4, "n_cell_input_nodes_graph": 1, "graph_channels": 32}


def _container(node, default):
    if node is None:
        return copy.deepcopy(default)
    if OmegaConf.is_config(node):
        return OmegaConf.to_container(node, resolve=True)
    return copy.deepcopy(node)


def load_space(space: str = SPACE_V1) -> dict:
    """Operator registries and fixed cell hyper-parameters, read from the repo's model config."""
    if space not in SPACES:
        raise ValueError(f"unknown space {space!r}; known: {sorted(SPACES)}")
    m = OmegaConf.load(SPACES[space])
    seq, flat = m.seq_model, m.flat_model
    sp = {
        "space": space,
        "seq": {
            "PRIMITIVES_encoder": list(seq.PRIMITIVES_encoder),
            "PRIMITIVES_decoder": list(seq.PRIMITIVES_decoder),
            "DECODERS": list(seq.DECODERS),
            "n_cells": int(seq.n_cells),
            "n_nodes": int(seq.n_nodes),
            "n_cell_input_nodes": int(seq.n_cell_input_nodes),
            "d_model": int(seq.d_model),
            "ops_kwargs": _container(seq.get("ops_kwargs"), {}),
            "model_kwargs": _container(seq.get("model_kwargs"), {}),
            "head_kwargs": _container(seq.get("head_kwargs"), {}),
            "backcast_loss_ration": float(seq.get("backcast_loss_ration", 0.0)),
        },
        "flat": {
            "PRIMITIVES_encoder": list(flat.PRIMITIVES_encoder),
            "n_cells": int(flat.n_cells),
            "n_nodes": int(flat.n_nodes),
            "n_cell_input_nodes": int(flat.n_cell_input_nodes),
            "ops_kwargs": _container(flat.get("ops_kwargs"), {}),
            "model_kwargs": _container(flat.get("model_kwargs"), {}),
            "head_kwargs": _container(flat.get("head_kwargs"), {}),
            "backcast_loss_ration": float(flat.get("backcast_loss_ration", 0.0)),
        },
        "HEADs": list(m.HEADs),
        # The searched nets keep arch_p_nets fixed (requires_grad=False) after search. For random
        # architectures there is no searched value, so both nets get sigmoid(0)/sum = 0.5.
        "nets_weights": [0.0, 0.0],
        "graph": None,
    }
    if space == SPACE_GRAPH_V1:
        sp["graph"] = {"PRIMITIVES": list(GRAPH_PRIMITIVES), **GRAPH_HPARAMS}
        sp["nets_weights_graph"] = [0.0, 0.0, 0.0]   # softmax -> 1/3 each, learnable (P3)
    return sp


# --------------------------------------------------------------------------- edge bookkeeping

def edge_pairs(n_input_nodes: int, n_nodes: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(n_input_nodes, n_input_nodes + n_nodes) for j in range(i)]


def edges_to_lists(edges: list, primitives: list[str]) -> tuple[list[int], list[bool]]:
    """Genotype edge list -> (operations, has_edges) as SampledEncoderCell expects them."""
    operations = [primitives.index(op) if op is not None else 0 for _, _, op in edges]
    has_edges = [op is not None for _, _, op in edges]
    return operations, has_edges


def lists_to_edges(operations, has_edges, primitives, n_input_nodes, n_nodes) -> list:
    pairs = edge_pairs(n_input_nodes, n_nodes)
    if not (len(pairs) == len(operations) == len(has_edges)):
        raise ValueError(f"edge count mismatch: {len(pairs)} pairs, {len(operations)} ops, {len(has_edges)} flags")
    return [[i, j, primitives[int(o)] if bool(h) else None] for (i, j), o, h in zip(pairs, operations, has_edges)]


def prune_dangling(edges: list, n_input_nodes: int, n_nodes: int) -> list:
    """Null the edges that SampledEncoderCell.__init__ removes: same function, same loop order."""
    max_nodes = n_input_nodes + n_nodes
    present = {f"{i}<-{j}" for i, j, op in edges if op is not None}
    nodes_to_remove = set(range(n_input_nodes, max_nodes - 1))
    for i in range(n_input_nodes, max_nodes - 1):
        check_node_is_connected_to_out(i, n_nodes_max=max_nodes, nodes_to_remove=nodes_to_remove, edges=present)
    out = []
    for i, j, op in edges:
        if op is not None and (i in nodes_to_remove or j in nodes_to_remove):
            op = None
        out.append([i, j, op])
    return out


def canonicalize(g: dict) -> dict:
    sp = load_space(g["space"])
    g = copy.deepcopy(g)
    hp = g["hparams"]
    enc = prune_dangling(g["seq"]["encoder"], hp["n_cell_input_nodes_seq"], hp["n_nodes_seq"])
    g["seq"]["encoder"] = enc
    if g["seq"]["decoder_type"] == "linear":
        g["seq"]["decoder"] = [[i, j, None] for i, j, _ in enc]
    else:
        dec = g["seq"]["decoder"]
        if [e[:2] for e in dec] != [e[:2] for e in enc]:
            raise ValueError("decoder edge order differs from encoder edge order")
        g["seq"]["decoder"] = [[i, j, dop if eop is not None else None]
                               for (i, j, eop), (_, _, dop) in zip(enc, dec)]
        missing = [(i, j) for (i, j, eop), (_, _, dop) in zip(enc, g["seq"]["decoder"])
                   if eop is not None and dop is None]
        if missing:
            raise ValueError(f"decoder must carry an op on every encoder edge; missing {missing}")
    g["flat"]["cell"] = prune_dangling(g["flat"]["cell"], hp["n_cell_input_nodes_flat"], hp["n_nodes_flat"])
    if g["seq"]["decoder_type"] not in sp["seq"]["DECODERS"] or g["head"] not in sp["HEADs"]:
        raise ValueError("decoder_type / head outside the space")
    if g.get("graph") is not None:
        if sp["graph"] is None:
            raise ValueError(f"space {g['space']} has no graph cell")
        bad = {op for _, _, op in g["graph"]["cell"] if op is not None} - set(sp["graph"]["PRIMITIVES"])
        if bad:
            raise ValueError(f"graph ops outside the space: {bad}")
        g["graph"]["cell"] = prune_dangling(g["graph"]["cell"], hp["n_cell_input_nodes_graph"], hp["n_nodes_graph"])
        if len(hp["nets_weights"]) != 3:
            raise ValueError("graph genotypes carry three nets_weights")
    else:
        g["graph"] = None
        if len(hp["nets_weights"]) != 2:
            raise ValueError("graph-blind genotypes carry two nets_weights")
    return g


def arch_id(g: dict) -> str:
    return hashlib.sha1(json.dumps(g, sort_keys=True).encode()).hexdigest()[:10]


# --------------------------------------------------------------------------- sampling

def _sample_cell(rng: random.Random, primitives, n_input_nodes, n_nodes, edges_per_node):
    edges = []
    for i in range(n_input_nodes, n_input_nodes + n_nodes):
        chosen = set(rng.sample(range(i), min(edges_per_node, i)))
        for j in range(i):
            edges.append([i, j, rng.choice(primitives) if j in chosen else None])
    return edges


def random_genotype(rng: random.Random, space: str = SPACE_V1, edges_per_node: int = 2, p_graph: float = 1.0) -> dict:
    """Uniform random genotype: each intermediate node keeps ``min(edges_per_node, i)`` incoming
    edges (2 = the DARTS-PT discretisation the shipped archs use: 8/14 seq, 7/10 flat), each with
    a uniform operator; decoder type and head uniform over the config lists.  In the graph space a graph
    cell is drawn with probability ``p_graph`` (uniform over the four graph ops), else ``graph: null``."""
    sp = load_space(space)
    s, f = sp["seq"], sp["flat"]
    enc = _sample_cell(rng, s["PRIMITIVES_encoder"], s["n_cell_input_nodes"], s["n_nodes"], edges_per_node)
    dec = [[i, j, rng.choice(s["PRIMITIVES_decoder"]) if op is not None else None] for i, j, op in enc]
    hp = {
        "d_model": s["d_model"],
        "n_cells_seq": s["n_cells"], "n_nodes_seq": s["n_nodes"],
        "n_cell_input_nodes_seq": s["n_cell_input_nodes"],
        "n_cells_flat": f["n_cells"], "n_nodes_flat": f["n_nodes"],
        "n_cell_input_nodes_flat": f["n_cell_input_nodes"],
        "nets_weights": list(sp["nets_weights"]),
    }
    graph = None
    if sp["graph"] is not None and rng.random() < p_graph:
        gsp = sp["graph"]
        graph = {"cell": _sample_cell(rng, gsp["PRIMITIVES"], gsp["n_cell_input_nodes_graph"], gsp["n_nodes_graph"], edges_per_node)}
        hp.update({k: gsp[k] for k in GRAPH_HPARAMS})
        hp["nets_weights"] = list(sp["nets_weights_graph"])
    g = {
        "space": space,
        "seq": {"encoder": enc, "decoder": dec, "decoder_type": rng.choice(s["DECODERS"])},
        "flat": {"cell": _sample_cell(rng, f["PRIMITIVES_encoder"], f["n_cell_input_nodes"], f["n_nodes"], edges_per_node)},
        "graph": graph,
        "head": rng.choice(sp["HEADs"]),
        "hparams": hp,
    }
    return canonicalize(g)


# --------------------------------------------------------------------------- family labels (Section 3.5)

def graph_ops(g: dict) -> list[str]:
    return [op for _, _, op in g["graph"]["cell"] if op is not None] if g.get("graph") else []


def has_graph_op(g: dict) -> bool:
    """True if the graph cell contains at least one op that is not the identity."""
    return any(op != "graph_identity" for op in graph_ops(g))


def graph_family(g: dict) -> str:
    ops = set(graph_ops(g))
    if not ops:
        return "none"
    if ops <= {"graph_identity"}:
        return "identity-only"
    if ops <= {"graph_identity", "adaptive"}:
        return "adaptive-only"
    if "gcn" in ops and "diffusion" in ops:
        return "mixed"
    return "gcn" if "gcn" in ops else "diffusion"


# --------------------------------------------------------------------------- round trip

def genotype_from_meta(meta: dict, space: str) -> dict:
    """Rebuild the genotype from ``MixedConcat[Graph]SampledNet.meta_info`` (the kwargs the net was built with)."""
    hp = {
        "d_model": int(meta["d_model"]),
        "n_cells_seq": int(meta["n_cells_seq"]), "n_nodes_seq": int(meta["n_nodes_seq"]),
        "n_cell_input_nodes_seq": int(meta["n_cell_input_nodes_seq"]),
        "n_cells_flat": int(meta["n_cells_flat"]), "n_nodes_flat": int(meta["n_nodes_flat"]),
        "n_cell_input_nodes_flat": int(meta["n_cell_input_nodes_flat"]),
        "nets_weights": [float(w) for w in meta["nets_weights"]],
    }
    enc = lists_to_edges(meta["operations_encoder_seq"], meta["has_edges_encoder_seq"],
                         list(meta["PRIMITIVES_encoder_seq"]), hp["n_cell_input_nodes_seq"], hp["n_nodes_seq"])
    dec = lists_to_edges(meta["operations_decoder_seq"], meta["has_edges_decoder_seq"],
                         list(meta["PRIMITIVES_decoder_seq"]), hp["n_cell_input_nodes_seq"], hp["n_nodes_seq"])
    flat = lists_to_edges(meta["operations_encoder_flat"], meta["has_edges_encoder_flat"],
                          list(meta["PRIMITIVES_encoder_flat"]), hp["n_cell_input_nodes_flat"], hp["n_nodes_flat"])
    graph = None
    if meta.get("graph") is not None:
        gm = meta["graph"]
        hp.update({"n_cells_graph": int(gm["n_cells"]), "n_nodes_graph": int(gm["n_nodes"]),
                   "n_cell_input_nodes_graph": int(gm["n_cell_input_nodes"]), "graph_channels": int(gm["channels"])})
        graph = {"cell": lists_to_edges(gm["operations"], gm["has_edges"], list(gm.get("PRIMITIVES", GRAPH_PRIMITIVES)),
                                        hp["n_cell_input_nodes_graph"], hp["n_nodes_graph"])}
    g = {"space": space,
         "seq": {"encoder": enc, "decoder": dec, "decoder_type": meta["DECODER_seq"]},
         "flat": {"cell": flat}, "graph": graph, "head": meta["HEAD"], "hparams": hp}
    return canonicalize(g)


# --------------------------------------------------------------------------- storage helpers

def load_archs(path: str | Path) -> list[dict]:
    """Read ``results/archs.jsonl``: one record ``{"arch_id", "genotype", ...}`` per line."""
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def find_arch(arch_id_: str, archs_path: str | Path = "results/archs.jsonl") -> dict:
    per_file = Path(archs_path).parent / "archs" / f"{arch_id_}.json"
    if per_file.exists():
        return json.load(open(per_file))
    for rec in load_archs(archs_path):
        if rec["arch_id"] == arch_id_:
            return rec
    raise KeyError(f"arch_id {arch_id_} not in {archs_path} or {per_file}")


def summarize(g: dict) -> str:
    def ops(edges):
        return ",".join(f"{i}<-{j}:{op}" for i, j, op in edges if op is not None)
    s = (f"head={g['head']} dec={g['seq']['decoder_type']} | seq.enc[{ops(g['seq']['encoder'])}] "
         f"| seq.dec[{ops(g['seq']['decoder'])}] | flat[{ops(g['flat']['cell'])}]")
    if g.get("graph") is not None:
        s += f" | graph[{ops(g['graph']['cell'])}] ({graph_family(g)})"
    return s
