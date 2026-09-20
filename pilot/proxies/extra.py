"""Zero-cost measures implemented directly on the wrapped net (all-parameter variants, Section 3.1/3.2).

W1 ships ``params``, ``grad_norm_all`` and ``nwot``; the NASLib pruners (Conv2d/Linear-only variants) are copied
in W2 and stored under their own names, so ``v1`` scores stay comparable.
"""
from __future__ import annotations

import torch
from torch import nn

ACTIVATION_TYPES = (nn.ReLU, nn.ReLU6, nn.LeakyReLU, nn.GELU, nn.SiLU, nn.ELU, nn.Tanh, nn.PReLU)


def params(net: nn.Module):
    return float(sum(p.numel() for p in net.parameters() if p.requires_grad)), {}


def grad_norm_all(net: nn.Module, x: torch.Tensor, target: torch.Tensor, loss_fn):
    """sum_p ||grad_p||_2 over every trainable parameter (NASLib's grad_norm only sums Conv2d/Linear)."""
    net.zero_grad(set_to_none=True)
    out = net(x)
    loss = loss_fn(out, target)
    loss.backward()
    total, n_with_grad, n_params = 0.0, 0, 0
    for p in net.parameters():
        if not p.requires_grad:
            continue
        n_params += 1
        if p.grad is not None:
            n_with_grad += 1
            total += p.grad.detach().norm(2).item()
    net.zero_grad(set_to_none=True)
    return float(total), {"loss": float(loss.detach()), "n_param_tensors": n_params, "n_with_grad": n_with_grad}


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


REGISTRY = {"params": params, "grad_norm_all": grad_norm_all, "nwot": nwot}
ALIASES = {"grad_norm": "grad_norm_all"}
