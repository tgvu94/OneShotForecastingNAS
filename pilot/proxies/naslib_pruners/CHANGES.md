# Pilot patches to the NASLib pruner copy

Source: `github.com/automl/NASLib`, commit `8cb5d2ba1e29784de43039d9824c68e88fb1a1da`, paths `naslib/predictors/utils/pruners/measures/` and
`naslib/predictors/utils/pruners/p_utils.py`. Copied (not pip-installed) on 2026-09-20; NASLib is not a dependency.

1. `p_utils.py`: removed `from ..models import *` (NASLib-internal). Added `PRUNABLE_TYPES = (Conv2d, Conv1d, Linear)` and
   `is_prunable()`; `get_layer_metric_array` uses it, so `nn.Conv1d` (the TCN / sep_tcn ops) is no longer silently skipped.
2. `measures/fisher.py`, `measures/snip.py`: added `*_forward_conv1d` (F.conv1d) and the Conv1d branch of the
   forward-override loop, using `is_prunable`. Without this, patch 1 alone would raise AttributeError on Conv1d
   (`weight_mask` / `act` are only attached in those loops).
2b. `measures/fisher.py`: the `dummy` Identity + `register_backward_hook` mechanism stored one activation per
   module (`layer.act`) and deleted it inside the hook. DARTS-TS calls some Linear modules twice in one forward
   (encoder + decoder cells), which raised `AttributeError: 'Linear' object has no attribute 'act'`. Replaced by a
   per-tensor autograd hook (`_fisher_capture`) that binds each call's activation to its own gradient; the per-channel
   Fisher formula (`0.5 * mean_b (sum_spatial act*grad)^2`) is unchanged.
3. `measures/grasp.py`: the two `Conv2d or Linear` loops use `is_prunable`, so Conv1d weights enter the Hessian-vector product.
4. `measures/__init__.py`: `zen` is not imported (its `forward_before_global_avg_pool` / `dim=[1,2,3]` assume a CNN);
   the pilot's Zen score lives in `pilot/proxies/extra.py`. `model_stats.py` (needs `tensorwatch`) is not copied.
5. Unchanged: `grad_norm`, `plain`, `l2_norm`, `synflow`, `jacov`, `nwot`, `epe_nas`. GRU/LSTM weights (`weight_ih_l0`, ...)
   and the transformer's `in_proj_weight` are still outside these Conv/Linear-only measures; the all-parameter
   variants (`*_all`) in `pilot/proxies/extra.py` cover them.
