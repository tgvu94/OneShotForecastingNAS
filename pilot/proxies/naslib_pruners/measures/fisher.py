# Copyright 2021 Samsung Electronics Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import torch
import torch.nn as nn
import torch.nn.functional as F

import types

from . import measure
from ..p_utils import get_layer_metric_array, reshape_elements, is_prunable


def _fisher_accumulate(layer, act, grad):
    """pilot patch: called by a tensor hook with the exact (activation, gradient) pair of one call of ``layer``."""
    if len(act.shape) > 2:
        g_nk = torch.sum((act * grad), list(range(2, len(act.shape))))
    else:
        g_nk = act * grad
    del_k = g_nk.pow(2).mean(0).mul(0.5)
    if layer.fisher is None:
        layer.fisher = del_k
    else:
        layer.fisher = layer.fisher + del_k


def _fisher_capture(layer, x):
    """pilot patch: replaces the ``dummy`` Identity + module backward hook.  A module used twice in one forward
    (DARTS-TS decoder cells) overwrote ``layer.act`` and the original hook deleted it after the first backward."""
    if x.requires_grad:
        x.register_hook(lambda grad, _act=x.detach(): _fisher_accumulate(layer, _act, grad.detach()))
    return x


def fisher_forward_conv2d(self, x):
    x = F.conv2d(
        x, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups
    )
    return _fisher_capture(self, x)


def fisher_forward_conv1d(self, x):  # pilot patch
    x = F.conv1d(
        x, self.weight, self.bias, self.stride, self.padding, self.dilation, self.groups
    )
    return _fisher_capture(self, x)


def fisher_forward_linear(self, x):
    x = F.linear(x, self.weight, self.bias)
    return _fisher_capture(self, x)


@measure("fisher", bn=True, mode="channel")
def compute_fisher_per_weight(net, inputs, targets, loss_fn, mode, split_data=1):

    device = inputs.device

    if mode == "param":
        raise ValueError("Fisher pruning does not support parameter pruning.")

    net.train()
    all_hooks = []
    for layer in net.modules():
        if is_prunable(layer):  # pilot patch
            # variables/op needed for fisher computation
            layer.fisher = None

            # replace forward method of conv/linear
            if isinstance(layer, nn.Conv2d):
                layer.forward = types.MethodType(fisher_forward_conv2d, layer)
            if isinstance(layer, nn.Conv1d):  # pilot patch
                layer.forward = types.MethodType(fisher_forward_conv1d, layer)
            if isinstance(layer, nn.Linear):
                layer.forward = types.MethodType(fisher_forward_linear, layer)

            # pilot patch: gradients are captured by the tensor hooks registered in _fisher_capture

    N = inputs.shape[0]
    for sp in range(split_data):
        st = sp * N // split_data
        en = (sp + 1) * N // split_data

        net.zero_grad()
        outputs = net(inputs[st:en])
        loss = loss_fn(outputs, targets[st:en])
        loss.backward()

    # retrieve fisher info
    def fisher(layer):
        if layer.fisher is not None:
            return torch.abs(layer.fisher.detach())
        else:
            return torch.zeros(layer.weight.shape[0])  # size=ch

    grads_abs_ch = get_layer_metric_array(net, fisher, mode)

    # broadcast channel value here to all parameters in that channel
    # to be compatible with stuff downstream (which expects per-parameter metrics)
    # TODO cleanup on the selectors/apply_prune_mask side (?)
    shapes = get_layer_metric_array(net, lambda l: l.weight.shape[1:], mode)

    grads_abs = reshape_elements(grads_abs_ch, shapes, device)

    return grads_abs
