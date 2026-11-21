# STID under the stock BasicTS pipeline with one part of OUR pipeline (pilot.train_arch, benchst protocol) put in at a time.
# The job script pilot/calibration_parts.sbatch copies this file to $NAS_ROOT/BasicTS/baselines/STID/pipeline_parts.py.
# Selected by environment variables, so that one config file serves every run:
#   PART_DATASET  METR-LA | PEMS-BAY          PART_SEED  integer (default 0)
#   PART_VARIANT  stock      the stock config of baselines/STID/<DATASET>.py
#                 split      split 0.6 / 0.2 / 0.2 in place of 0.7 / 0.1 / 0.2 (the test part is the same last 20 %)
#                 nodescale  z-score per sensor in place of one z-score for the city (input and output scaling)
#                 nodeloss   training loss = masked MAE of the error divided by the standard deviation of the sensor
#                            (the MAE in the per-sensor normalised unit, the loss of our pipeline); metrics unchanged
#                 instnorm   a history of 96 steps; each sensor of a window is standardised by its mean and standard deviation
#                            over the 96 steps, STID reads the last 12 scaled steps, and its output is scaled back
#                            (the target scaler 'standard' of our trainer)
#                 clip       gradient clipping at the norm 0.1 in place of 5.0
#                 sched      20 epochs, Adam lr 0.001 without weight decay, one cosine cycle over the 20 epochs, batch 32
#                 all        every part above together
# Everything else is the stock config.  The test batch size divides the number of test windows, because the save function of
# this BasicTS commit writes a last partial batch at a wrong offset.
import os
import sys

import numpy as np
import torch
from easydict import EasyDict
sys.path.append(os.path.abspath(__file__ + '/../../..'))

from basicts.metrics import masked_mae, masked_mape, masked_rmse
from basicts.data import TimeSeriesForecastingDataset
from basicts.runners import SimpleTimeSeriesForecastingRunner
from basicts.scaler import ZScoreScaler
from basicts.utils import get_regular_settings, load_dataset_desc

from .arch import STID

DATA_NAME = os.environ.get('PART_DATASET', 'METR-LA')
VARIANT = os.environ.get('PART_VARIANT', 'stock')
SEED = int(os.environ.get('PART_SEED', '0'))
PARTS = ('split', 'nodescale', 'nodeloss', 'instnorm', 'clip', 'sched')
assert VARIANT in ('stock', 'all') + PARTS, VARIANT
on = lambda part: VARIANT in (part, 'all')                       # noqa: E731

regular_settings = get_regular_settings(DATA_NAME)
desc = load_dataset_desc(DATA_NAME)
NUM_STEPS, NUM_NODES = desc['shape'][0], desc['shape'][1]
OUTPUT_LEN = regular_settings['OUTPUT_LEN']
MODEL_INPUT_LEN = regular_settings['INPUT_LEN']                    # 12: what STID reads
INPUT_LEN = 96 if on('instnorm') else MODEL_INPUT_LEN            # what the dataset gives
TRAIN_VAL_TEST_RATIO = [0.6, 0.2, 0.2] if on('split') else regular_settings['TRAIN_VAL_TEST_RATIO']
NULL_VAL = regular_settings['NULL_VAL']
NUM_EPOCHS = 20 if on('sched') else 100
BATCH = 32 if on('sched') else 64
N_TEST = int(NUM_STEPS * TRAIN_VAL_TEST_RATIO[2]) - INPUT_LEN - OUTPUT_LEN + 1
TEST_BATCH = max(d for d in range(1, 257) if N_TEST % d == 0)
if TEST_BATCH < 16:
    TEST_BATCH = N_TEST

_data = np.memmap(f'datasets/{DATA_NAME}/data.dat', dtype='float32', mode='r', shape=tuple(desc['shape']))
_train = np.asarray(_data[:int(NUM_STEPS * TRAIN_VAL_TEST_RATIO[0]), :, 0])
NODE_MEAN, NODE_STD = _train.mean(0), _train.std(0)
NODE_STD[NODE_STD == 0] = 1.0


class NodeZScoreScaler(ZScoreScaler):
    """One mean and one standard deviation per sensor, from the training rows."""

    def __init__(self, dataset_name, train_ratio, norm_each_channel, rescale):
        super().__init__(dataset_name, train_ratio, norm_each_channel, rescale)
        self.mean, self.std = torch.tensor(NODE_MEAN), torch.tensor(NODE_STD)


def node_normalised_mae(prediction, target, null_val=np.nan):
    """Masked MAE of the error in the per-sensor normalised unit; prediction and target [B, L, N, 1] in the raw unit."""
    sd = torch.tensor(NODE_STD, device=target.device, dtype=target.dtype).view(1, 1, -1, 1)
    mask = (~torch.isclose(target, torch.full_like(target, null_val), atol=5e-5, rtol=0.0)).float()
    mask = torch.nan_to_num(mask / torch.mean(mask))
    return torch.mean(torch.nan_to_num(torch.abs(prediction - target) / sd * mask))


class InstNormSTID(STID):
    """STID on the last 12 steps of a window of 96 steps that is standardised per sensor over the 96 steps."""

    def forward(self, history_data, future_data, batch_seen, epoch, train, **kwargs):
        x = history_data[..., 0]                                  # [B, 96, N]
        loc, scale = x.mean(1, keepdim=True), x.std(1, keepdim=True)
        scale = torch.where(scale < 1e-4, torch.ones_like(scale), scale)
        h = history_data[:, -MODEL_INPUT_LEN:].clone()
        h[..., 0] = (h[..., 0] - loc) / scale
        out = super().forward(h, future_data, batch_seen, epoch, train, **kwargs)     # [B, 12, N, 1]
        return out * scale.unsqueeze(-1) + loc.unsqueeze(-1)


MODEL_ARCH = InstNormSTID if on('instnorm') else STID
MODEL_PARAM = {
    "num_nodes": NUM_NODES, "input_len": MODEL_INPUT_LEN, "input_dim": 3, "embed_dim": 32, "output_len": OUTPUT_LEN,
    "num_layer": 3, "if_node": True, "node_dim": 32, "if_T_i_D": True, "if_D_i_W": True,
    "temp_dim_tid": 32, "temp_dim_diw": 32, "time_of_day_size": 288, "day_of_week_size": 7,
}

CFG = EasyDict()
CFG.DESCRIPTION = f'STID pipeline part {VARIANT} on {DATA_NAME}, seed {SEED}'
CFG.GPU_NUM = 1
CFG.RUNNER = SimpleTimeSeriesForecastingRunner
CFG.ENV = EasyDict()
CFG.ENV.SEED = SEED

CFG.DATASET = EasyDict()
CFG.DATASET.NAME = DATA_NAME
CFG.DATASET.TYPE = TimeSeriesForecastingDataset
CFG.DATASET.PARAM = EasyDict({'dataset_name': DATA_NAME, 'train_val_test_ratio': TRAIN_VAL_TEST_RATIO,
                              'input_len': INPUT_LEN, 'output_len': OUTPUT_LEN})

CFG.SCALER = EasyDict()
CFG.SCALER.TYPE = NodeZScoreScaler if on('nodescale') else ZScoreScaler
CFG.SCALER.PARAM = EasyDict({'dataset_name': DATA_NAME, 'train_ratio': TRAIN_VAL_TEST_RATIO[0],
                             'norm_each_channel': regular_settings['NORM_EACH_CHANNEL'], 'rescale': regular_settings['RESCALE']})

CFG.MODEL = EasyDict()
CFG.MODEL.NAME = 'STID'
CFG.MODEL.ARCH = MODEL_ARCH
CFG.MODEL.PARAM = MODEL_PARAM
CFG.MODEL.FORWARD_FEATURES = [0, 1, 2]
CFG.MODEL.TARGET_FEATURES = [0]

CFG.METRICS = EasyDict()
CFG.METRICS.FUNCS = EasyDict({'MAE': masked_mae, 'MAPE': masked_mape, 'RMSE': masked_rmse})
CFG.METRICS.TARGET = 'MAE'
CFG.METRICS.NULL_VAL = NULL_VAL

CFG.TRAIN = EasyDict()
CFG.TRAIN.NUM_EPOCHS = NUM_EPOCHS
CFG.TRAIN.CKPT_SAVE_DIR = os.path.join('checkpoints', 'STID_parts', DATA_NAME, f'{VARIANT}_s{SEED}')
CFG.TRAIN.LOSS = node_normalised_mae if on('nodeloss') else masked_mae
CFG.TRAIN.OPTIM = EasyDict()
CFG.TRAIN.OPTIM.TYPE = "Adam"
CFG.TRAIN.LR_SCHEDULER = EasyDict()
if on('sched'):
    CFG.TRAIN.OPTIM.PARAM = {"lr": 0.001, "weight_decay": 0.0}
    CFG.TRAIN.LR_SCHEDULER.TYPE = "CosineAnnealingLR"
    CFG.TRAIN.LR_SCHEDULER.PARAM = {"T_max": NUM_EPOCHS, "eta_min": 1e-8}
else:
    CFG.TRAIN.OPTIM.PARAM = {"lr": 0.002, "weight_decay": 0.0001}
    CFG.TRAIN.LR_SCHEDULER.TYPE = "MultiStepLR"
    CFG.TRAIN.LR_SCHEDULER.PARAM = {"milestones": [1, 50, 80], "gamma": 0.5}
CFG.TRAIN.CLIP_GRAD_PARAM = {'max_norm': 0.1 if on('clip') else 5.0}
CFG.TRAIN.DATA = EasyDict()
CFG.TRAIN.DATA.BATCH_SIZE = BATCH
CFG.TRAIN.DATA.SHUFFLE = True

CFG.VAL = EasyDict()
CFG.VAL.INTERVAL = 1
CFG.VAL.DATA = EasyDict()
CFG.VAL.DATA.BATCH_SIZE = 64

CFG.TEST = EasyDict()
CFG.TEST.INTERVAL = NUM_EPOCHS                                   # the test part is read once, at the last epoch
CFG.TEST.DATA = EasyDict()
CFG.TEST.DATA.BATCH_SIZE = TEST_BATCH

CFG.EVAL = EasyDict()
CFG.EVAL.HORIZONS = [3, 6, 12]
CFG.EVAL.USE_GPU = True
