"""Presents a DARTS-TS discrete net to zero-cost measures as ``f(x_past) -> (B, H, N)``.

Verified W1: ``MixedConcatSampledNet.forward(x_past, x_future)``; ``x_past`` is (B, W, N+F) scaled past targets +
past time features, ``x_future`` is (B, H, F) future time features.  The return is a tensor for the mse/mae
heads and a list of three tensors (quantiles 0.1, 0.9, 0.5) for the quantile head; ``get_inference_prediction``
picks the median.  The training loss is ``head.loss(target, rescale_output(prediction, loc, scale))``.
"""
from __future__ import annotations

import copy

import torch
from torch import nn

from tsf_oneshot.training.training_utils import rescale_output


class ProxyWrapper(nn.Module):
    def __init__(self, net: nn.Module, batch_extras: dict):
        super().__init__()
        self.net = net
        # every forward input except the window itself: x_future, loc, scale
        self.batch_extras = {k: v for k, v in batch_extras.items()}
        self._last = {}

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
        self._last = {"raw": raw, "loc": ex["loc"], "scale": ex["scale"]}
        return self.net.get_inference_prediction(raw) if isinstance(raw, (list, tuple)) else raw

    def loss_fn(self, outputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """Same quantity SampledForecastingNetTrainer.update_weights minimises. For the quantile head the
        full three-quantile output of the last forward is used (``outputs`` is its median)."""
        raw = self._last.get("raw")
        if not (isinstance(raw, (list, tuple)) and raw[-1] is outputs):
            raw = outputs
        pred = rescale_output(raw, self._last["loc"], self._last["scale"], device=outputs.device)
        targets = targets[: outputs.shape[0]].to(device=outputs.device, dtype=outputs.dtype)
        return self.net.get_training_loss(targets, pred)

    def get_prunable_copy(self, bn: bool = True):
        return copy.deepcopy(self)
