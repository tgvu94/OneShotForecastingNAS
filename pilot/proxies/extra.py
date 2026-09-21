"""Zero-cost measures implemented directly on the wrapped net (Sections 3.1 / 3.2).

* all-parameter variants of the "sum over parameters" measures: ``grad_norm_all``, ``snip_all``, ``plain_all``,
  ``l2_norm_all``, ``grasp_all``, ``synflow_all`` -- NASLib's copies only see Conv2d/Conv1d/Linear weights, so on a
  GRU/LSTM/transformer-heavy architecture they score only the embedding, TCN and head layers;
* ``params``, ``flops`` (``torch.utils.flop_counter``), ``nwot`` (with ``n_hooks``), ``zen`` (feature hook on the
  two nets' head inputs) and ``zico`` (four probe batches).

Every function takes the ``ProxyWrapper`` (``net``) and returns ``(value, meta)`` or, for a *group*, a dict
``{name: (value, meta)}`` computed from one forward/backward.
"""
from __future__ import annotations

import copy
import math

import torch
from torch import nn
from torch.nn.modules.batchnorm import _BatchNorm

ACTIVATION_TYPES = (nn.ReLU, nn.ReLU6, nn.LeakyReLU, nn.GELU, nn.SiLU, nn.ELU, nn.Tanh, nn.PReLU)


def double_backward_ctx():
    """Attention math kernel: the flash / mem-efficient SDPA kernels have no double backward."""
    try:
        from torch.nn.attention import SDPBackend, sdpa_kernel
        return sdpa_kernel(SDPBackend.MATH)
    except Exception:  # noqa: BLE001
        import contextlib
        return contextlib.nullcontext()


def _trainable(net):
    return [p for p in net.parameters() if p.requires_grad]


def params(net: nn.Module):
    return float(sum(p.numel() for p in net.parameters() if p.requires_grad)), {}


@torch.no_grad()
def flops(net: nn.Module, x: torch.Tensor):
    """FLOPs of one forward pass on the probe batch (batch 32).  cuDNN GRU/LSTM kernels may be under-counted."""
    from torch.utils.flop_counter import FlopCounterMode

    was_training = net.training
    net.eval()
    try:
        with FlopCounterMode(display=False) as fc:
            net(x)
    finally:
        net.train(was_training)
    return float(fc.get_total_flops()), {"batch": int(x.shape[0])}


def l2_norm_all(net: nn.Module):
    return float(sum(p.detach().norm(2).item() for p in _trainable(net))), {"n_param_tensors": len(_trainable(net))}


def grad_group_all(net: nn.Module, x: torch.Tensor, target: torch.Tensor, loss_fn):
    """One forward/backward -> grad_norm_all = sum_p ||g_p||_2, snip_all = sum_p |g_p * p|, plain_all = sum_p (g_p * p)."""
    net.zero_grad(set_to_none=True)
    out = net(x)
    loss = loss_fn(out, target)
    loss.backward()
    gn, snip, plain, n_with_grad, n_params = 0.0, 0.0, 0.0, 0, 0
    for p in _trainable(net):
        n_params += 1
        if p.grad is not None:
            g = p.grad.detach()
            n_with_grad += 1
            gn += g.norm(2).item()
            snip += (g * p.detach()).abs().sum().item()
            plain += (g * p.detach()).sum().item()
    net.zero_grad(set_to_none=True)
    meta = {"loss": float(loss.detach()), "n_param_tensors": n_params, "n_with_grad": n_with_grad}
    return {"grad_norm_all": (float(gn), meta), "snip_all": (float(snip), meta), "plain_all": (float(plain), meta)}


def grad_norm_all(net, x, target, loss_fn):  # W1 name, kept for compatibility
    return grad_group_all(net, x, target, loss_fn)["grad_norm_all"]


def grasp_all(net: nn.Module, x: torch.Tensor, target: torch.Tensor, loss_fn, T: float = 1.0):
    """NASLib's GRASP recipe over every trainable parameter: g = dL/dw (pass 1), z = <g, dL/dw> with graph (pass 2),
    dz/dw = H g, score = sum_p (-p * Hg)_sum (NASLib's sign).  Needs a double backward -> cuDNN RNN kernels are
    disabled (they do not implement it) and attention uses the math kernel."""
    weights = _trainable(net)
    net.zero_grad(set_to_none=True)
    with torch.backends.cudnn.flags(enabled=False), double_backward_ctx():
        out = net(x) / T
        loss = loss_fn(out, target)
        grad_w = torch.autograd.grad(loss, weights, allow_unused=True)
        out = net(x) / T
        loss = loss_fn(out, target)
        grad_f = torch.autograd.grad(loss, weights, create_graph=True, allow_unused=True)
        z, n_used = 0.0, 0
        for gw, gf in zip(grad_w, grad_f):
            if gw is not None and gf is not None:
                z = z + (gw.detach() * gf).sum()
                n_used += 1
        z.backward()
    score = 0.0
    for p in weights:
        if p.grad is not None:
            score += (-p.detach() * p.grad.detach()).sum().item()
    net.zero_grad(set_to_none=True)
    return float(score), {"n_param_tensors": len(weights), "n_in_hvp": n_used, "cudnn_disabled": True, "T": T}


def synflow_all(net: nn.Module, x: torch.Tensor):
    """NASLib's synflow on a deep copy (double, |params|, all-ones input of batch 1, sum(output).backward()),
    summed over *every* trainable parameter: sum_p |p * dR/dp|.  BatchNorm modules are put in eval mode
    (NASLib evaluates synflow on BN-free nets)."""
    cp = copy.deepcopy(net).double()
    for m in cp.modules():
        if isinstance(m, _BatchNorm):
            m.eval()
    with torch.no_grad():
        for _, p in cp.state_dict().items():
            p.abs_()
    cp.zero_grad(set_to_none=True)
    ones = torch.ones([1] + list(x.shape[1:]), dtype=torch.float64, device=x.device)
    out = cp(ones)
    torch.sum(out).backward()
    score, n_with_grad, n_params = 0.0, 0, 0
    for p in _trainable(cp):
        n_params += 1
        if p.grad is not None:
            n_with_grad += 1
            score += (p.detach() * p.grad.detach()).abs().sum().item()
    del cp
    finite = math.isfinite(score)
    return float(score), {"finite": finite, "log_score": math.log(score) if finite and score > 0 else None,
                          "n_param_tensors": n_params, "n_with_grad": n_with_grad, "output_finite": bool(torch.isfinite(out).all())}


@torch.no_grad()
def nwot(net: nn.Module, x: torch.Tensor):
    """NASWOT (Mellor et al. 2021), NASLib recipe: hook every activation module, binarise its *input* (> 0),
    K += c c^T + (1-c)(1-c)^T over the flattened batch, score = slogdet(K)[1].  Records ``n_hooks``.
    GRU/LSTM (cuDNN) and the transformer's functional ReLU expose no activation module -> not counted."""
    B = x.shape[0]
    K = torch.zeros(B, B, dtype=torch.float64, device=x.device)
    fired, skipped = [0], []

    def hook(module, inp, out):
        t = inp[0] if isinstance(inp, (tuple, list)) else inp
        if not torch.is_tensor(t) or t.dim() == 0 or t.shape[0] != B:
            skipped.append(type(module).__name__ + str(tuple(t.shape) if torch.is_tensor(t) else ()))
            return
        c = (t.reshape(B, -1) > 0).to(torch.float64)
        K.add_(c @ c.t())
        K.add_((1.0 - c) @ (1.0 - c).t())
        fired[0] += 1

    handles = [m.register_forward_hook(hook) for m in net.modules() if isinstance(m, ACTIVATION_TYPES)]
    try:
        net(x)
    finally:
        for h in handles:
            h.remove()
    sign, logdet = torch.linalg.slogdet(K)
    return float(logdet), {"n_hooks": len(handles), "n_fired": fired[0], "n_skipped": len(skipped),
                           "skipped": skipped[:10], "sign": float(sign)}


def _gaussian_init(net: nn.Module):
    """NASLib's zen init (N(0,1) weights, zero bias for Conv/Linear; ones/zeros for BN), extended to Conv1d/BatchNorm1d."""
    with torch.no_grad():
        for m in net.modules():
            if isinstance(m, (nn.Conv1d, nn.Conv2d, nn.Linear)):
                nn.init.normal_(m.weight)
                if getattr(m, "bias", None) is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, (_BatchNorm, nn.GroupNorm)):
                if m.weight is not None:
                    nn.init.ones_(m.weight)
                    nn.init.zeros_(m.bias)


@torch.no_grad()
def zen(net: nn.Module, x: torch.Tensor, repeat: int = 3, mixup_gamma: float = 1e-2):
    """Zen score (Lin et al. 2021) on the pre-head features: the input of ``seq_net.head`` (decoder features) and the
    flat net's output (its head is bypassed by ``forward_only_with_net=True`` in the combined forward, so the flat
    forecast is its last feature) -- the two tensors entering the fixed 0.5/0.5 combiner.  Gaussian re-init as
    in NASLib, features compared between ``x`` and ``x + gamma * eps``; score = mean over repeats of
    log( mean_b sum |delta features| ) + sum_BN log sqrt(mean running_var).  Works on a deep copy."""
    cp = copy.deepcopy(net)
    cp.train()
    feats = {}
    hooks = []
    def pre_hook(module, inp):  # input of the seq head = decoder features (B, H, d_model)
        t = inp[0] if isinstance(inp, (tuple, list)) else inp
        feats.setdefault("seq", []).append(t.detach().reshape(t.shape[0], -1))

    def flat_hook(module, inp, out):  # forward_only_with_net=True bypasses the flat head: the flat forecast is the feature
        t = out[1] if isinstance(out, (tuple, list)) else out
        feats.setdefault("flat", []).append(t.detach().reshape(t.shape[0], -1))

    def graph_hook(module, inp, out):  # graph forecast (B, H, N), the third combiner input
        feats.setdefault("graph", []).append(out.detach().reshape(out.shape[0], -1))

    hooks.append(cp.net.seq_net.head.register_forward_pre_hook(pre_hook))
    hooks.append(cp.net.flat_net.register_forward_hook(flat_hook))
    if hasattr(cp.net, "graph_net"):
        hooks.append(cp.net.graph_net.register_forward_hook(graph_hook))
    scores = []
    try:
        for _ in range(repeat):
            _gaussian_init(cp)
            feats.clear()
            cp(x)
            eps = torch.randn_like(x)
            cp(x + mixup_gamma * eps)
            total = 0.0
            for label, fs in feats.items():
                if len(fs) != 2:
                    raise RuntimeError(f"expected 2 feature captures for {label}, got {len(fs)}")
                total = total + (fs[0] - fs[1]).abs().sum(dim=1).mean()
            log_bn = 0.0
            for m in cp.modules():
                if isinstance(m, _BatchNorm) and m.running_var is not None:
                    log_bn += float(torch.log(torch.sqrt(torch.mean(m.running_var))))
            scores.append(float(torch.log(total)) + log_bn)
    finally:
        for h in hooks:
            h.remove()
    del cp
    return float(sum(scores) / len(scores)), {"repeat": repeat, "mixup_gamma": mixup_gamma, "per_repeat": scores,
                                              "n_feature_hooks": len(hooks), "feature_labels": sorted(feats)}


def zico(net: nn.Module, batches: list[dict], loss_fn, device: torch.device):
    """ZiCo (Li et al. 2023), the authors' recipe: per parameter tensor, over >= 2 batches, the element-wise mean of
    |grad| and std of grad; score = sum_tensors log( sum_{i: std_i > 0} mean_i / std_i ).  Uses probe batches 0-3."""
    grads = {}
    saved_extras = net.batch_extras
    for b in batches:
        x, target = b["x_past"].to(device), b["target"].to(device)
        net.batch_extras = {"x_future": b["x_future"], "loc": b["loc"], "scale": b["scale"]}
        net.zero_grad(set_to_none=True)
        out = net(x)
        loss = loss_fn(out, target)
        loss.backward()
        for name, p in net.named_parameters():
            if p.requires_grad and p.grad is not None:
                grads.setdefault(name, []).append(p.grad.detach().clone())
    net.zero_grad(set_to_none=True)
    net.batch_extras = saved_extras
    score, n_used, n_zero = 0.0, 0, 0
    for name, gs in grads.items():
        if len(gs) < 2:
            continue
        g = torch.stack(gs, 0)
        std = g.std(dim=0, unbiased=False)
        mean_abs = g.abs().mean(dim=0)
        nz = std > 0
        tmpsum = (mean_abs[nz] / std[nz]).sum().item()
        if tmpsum > 0:
            score += math.log(tmpsum)
            n_used += 1
        else:
            n_zero += 1
    return float(score), {"n_batches": len(batches), "n_param_tensors_used": n_used, "n_param_tensors_zero": n_zero}


# name -> (kind, callable).  kind tells score_proxies what to pass.
#   "net"   : f(net)                           "x"     : f(net, x)
#   "loss"  : f(net, x, target, loss_fn)       "zico"  : f(net, batches, loss_fn, device)
#   "group" : f(net, x, target, loss_fn) -> {name: (value, meta)}
REGISTRY = {
    "params": ("net", params),
    "flops": ("x", flops),
    "l2_norm_all": ("net", l2_norm_all),
    "grad_norm_all": ("group", grad_group_all),
    "snip_all": ("group", grad_group_all),
    "plain_all": ("group", grad_group_all),
    "grasp_all": ("loss", grasp_all),
    "synflow_all": ("x", synflow_all),
    "nwot": ("x", nwot),
    "zen": ("x", zen),
    "zico": ("zico", zico),
}
ALIASES = {"grad_norm": "grad_norm_all"}  # W1 alias; W2's score_proxies maps the 13 plan names itself
