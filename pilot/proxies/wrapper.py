"""Presents a DARTS-TS discrete net to zero-cost measures as ``f(x_past) -> (B, H, N)``.

Verified P1: ``MixedConcatSampledNet.forward(x_past, x_future)``; ``x_past`` is (B, W, N+F) scaled past targets +
past time features, ``x_future`` is (B, H, F) future time features.  The return is a tensor for the mse/mae
heads and a list of three tensors (quantiles 0.1, 0.9, 0.5) for the quantile head; ``get_inference_prediction``
picks the median.  The training loss is ``head.loss(target, rescale_output(prediction, loc, scale))``.

P2: the NASLib measures deep-copy the wrapper (``get_prunable_copy``) *before* calling it and receive ``loss_fn``
as a plain argument, so the loss cannot be a bound method of the copy.  Every wrapper forward (original or copy)
therefore records its raw output in the module-level ``_LAST`` and :func:`loss_fn` reads it back.  Proxies run
one after another, so "the last forward" is unambiguous.
"""
from __future__ import annotations

import copy

import torch
from torch import nn
from torch.nn.modules.batchnorm import _BatchNorm

from tsf_oneshot.training.training_utils import rescale_output

_LAST: dict = {}


def loss_fn(outputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    """Same quantity SampledForecastingNetTrainer.update_weights minimises, on the last wrapper forward.

    ``outputs`` is what the wrapper returned (the median for the quantile head).  If a measure transformed it
    (GRASP divides by its temperature T) the transformed tensor replaces the median so gradients still flow
    through the measure's graph."""
    raw, head = _LAST["raw"], _LAST["head"]
    if isinstance(raw, (list, tuple)):
        raw = [outputs if q is _LAST["median"] else q for q in raw]
    else:
        raw = outputs
    pred = rescale_output(raw, _LAST["loc"], _LAST["scale"], device=outputs.device)
    targets = targets[: outputs.shape[0]].to(device=outputs.device, dtype=outputs.dtype)
    return head.loss(targets, pred)


class ProxyWrapper(nn.Module):
    def __init__(self, net: nn.Module, batch_extras: dict):
        super().__init__()
        self.net = net
        # every forward input except the window itself: x_future, loc, scale
        self.batch_extras = {k: v for k, v in batch_extras.items()}

    def _sliced(self, x: torch.Tensor) -> dict:
        """Slice every extra to the batch size of ``x`` (synflow calls the net on a batch of ones of size 1)
        and move it to ``x``'s device / floating dtype (synflow runs the net in double)."""
        out = {}
        for k, v in self.batch_extras.items():
            if torch.is_tensor(v):
                v = v[: x.shape[0]].to(device=x.device)
                if v.is_floating_point():
                    v = v.to(dtype=x.dtype)
            out[k] = v
        return out

    def forward(self, x: torch.Tensor):
        ex = self._sliced(x)
        raw = self.net(x, ex["x_future"])
        out = self.net.get_inference_prediction(raw) if isinstance(raw, (list, tuple)) else raw
        _LAST.update({"raw": raw, "median": out, "loc": ex["loc"], "scale": ex["scale"], "head": self.net.head})
        return out

    def loss_fn(self, outputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        return loss_fn(outputs, targets)

    def get_prunable_copy(self, bn: bool = True):
        """Deep copy.  NASLib builds its nets without BatchNorm when ``bn=False`` (synflow); the DARTS-TS flat
        MLP ops carry ``BatchNorm1d`` we cannot remove, so those modules are put in eval mode instead: with fresh
        running stats (mean 0, var 1) and default affine (1, 0) that is the identity."""
        cp = copy.deepcopy(self)
        if not bn:
            for m in cp.modules():
                if isinstance(m, _BatchNorm):
                    m.eval()
        return cp
