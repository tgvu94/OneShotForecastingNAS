"""Bridge to the copied NASLib pruners (``pilot/proxies/naslib_pruners``, see its CHANGES.md).

Each measure returns per-layer arrays for the Conv2d/Conv1d/Linear layers (or a scalar for jacov / nwot); the
score is the sum over all elements, exactly what NASLib's ``find_measures`` does (``sum_arr``).  The ``@measure``
decorator deep-copies the wrapper first, so the original net's parameters and gradients are untouched.
"""
from __future__ import annotations

import math

import torch

from pilot.proxies.naslib_pruners import NASLIB_COMMIT
from pilot.proxies.naslib_pruners.measures import available_measures, calc_measure
from pilot.proxies.naslib_pruners.p_utils import is_prunable
from pilot.proxies.wrapper import loss_fn

NASLIB_MEASURES = ["grad_norm", "snip", "grasp", "fisher", "jacov", "plain", "synflow", "l2_norm"]


def sum_arr(arr) -> tuple[float, int]:
    """Sum of every element of a (possibly nested) list of tensors; also returns the number of tensors."""
    if torch.is_tensor(arr):
        return float(arr.double().sum().item()), 1
    if isinstance(arr, (list, tuple)):
        total, n = 0.0, 0
        for a in arr:
            s, k = sum_arr(a)
            total, n = total + s, n + k
        return total, n
    return float(arr), 1


def n_prunable(net) -> int:
    return sum(1 for m in net.modules() if is_prunable(m))


def naslib_measure(name: str, wrapper, x: torch.Tensor, target: torch.Tensor):
    """Run one NASLib measure on the probe batch. Returns (score, meta)."""
    if name not in available_measures:
        raise KeyError(f"{name} not in NASLib measures {available_measures}")
    device = x.device
    from pilot.proxies.extra import double_backward_ctx
    ctx = torch.backends.cudnn.flags(enabled=False) if name == "grasp" else _null()
    with ctx, (double_backward_ctx() if name == "grasp" else _null()):
        # grasp needs a double backward through GRU/LSTM, which cuDNN does not implement -> native RNN kernels
        arr = calc_measure(name, wrapper, device, x, target, loss_fn=loss_fn)
    if name == "jacov":
        score, n_layers = float(arr), 0
    else:
        score, n_layers = sum_arr(arr)
    meta = {"n_layers": n_layers, "n_prunable_modules": n_prunable(wrapper), "finite": bool(math.isfinite(score))}
    if name == "grasp":
        meta["cudnn_disabled"] = True
    if name == "synflow":
        meta["log_score"] = math.log(score) if score > 0 and math.isfinite(score) else None
    return score, meta


class _null:
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


__all__ = ["NASLIB_COMMIT", "NASLIB_MEASURES", "naslib_measure"]
