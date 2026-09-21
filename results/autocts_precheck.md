# AutoCTS pre-check (2026-09-20)

AutoCTS commit `ef9a40cb` run from `/home/adamvu/nas/AutoCTS` inside the pilot venv (torch 2.14.0); no separate venv was needed.

## Operator list and cell

- `PRIMITIVES` = ['none', 'skip_connect', 'dcc_2', 'trans', 's_trans', 'diff_gcn'] (the repo also ships, commented out: cheb_gcn, cnn, att1, att2, lstm, gru, dcc_1)
- cell: 4 nodes, 10 candidate edges, 4 cells chained; genotype keeps 2 incoming edges per node; hid_dim 32, PC-DARTS partial channels k=4
- sampled discrete genes (cell: [(node, from, op)]): [[(0, 0, 's_trans'), (1, 0, 'skip_connect'), (1, 1, 'trans'), (2, 1, 's_trans'), (2, 2, 'trans'), (3, 1, 'trans'), (3, 3, 'diff_gcn')], [(0, 0, 'dcc_2'), (1, 0, 'trans'), (1, 1, 'dcc_2'), (2, 0, 'diff_gcn'), (2, 2, 'trans'), (3, 2, 'diff_gcn'), (3, 3, 'dcc_2')], [(0, 0, 'trans'), (1, 0, 'skip_connect'), (1, 1, 'trans'), (2, 1, 'diff_gcn'), (2, 2, 'skip_connect'), (3, 1, 's_trans'), (3, 3, 'trans')], [(0, 0, 'diff_gcn'), (1, 0, 'diff_gcn'), (1, 1, 's_trans'), (2, 1, 'diff_gcn'), (2, 2, 'trans'), (3, 0, 'diff_gcn'), (3, 3, 'skip_connect')]]
- params: 276,620
- library-drift patches needed to run on torch 2.14.0: ['skip_connect Conv1d(C, 8C, (1,1)) on 4-D input -> Conv2d (torch 2.14 rejects the original)', 'nn.utils.clip_grad_norm (removed) -> clip_grad_norm_']

## Data and adjacency (their pipeline)

- utils.generate_data: 60/20/20 by time (generate_from_data), window 12, horizon 12, channel 0 (flow) only (generate_seq slices [..., 0:1])
- StandardScaler(mean, std of train x[..., 0]) on inputs; loss on inverse-transformed prediction vs raw targets; loss masked_mae(pred, y, null_val=0.0)
- train/val/test windows: 10172 / 3375 / 3376; 159 batches of 64 per epoch
- adjacency: PEMS04.csv via utils.get_adj_matrix(type_='connectivity'), 340 undirected edges, equals the pilot's `pems04_adj.npy`: True
- diff_gcn supports: asym_adj(A), asym_adj(A^T) (row-normalised random walks) + adaptive softmax(relu(E1 E2))

## 1-epoch training (their loss, optimiser and clipping)

- seconds per epoch: 37.7 (peak GPU memory 3.615 GB)
- train masked-MAE: first batch 8578.87, last batch 217.91, mean of last 50 248.38 (raw vehicle counts)
- val masked-MAE after 1 epoch: 169.23

## Proxies on their first train batch

- params 276620, grad_norm_all 2.583e+05 (182/1537 tensors with grad), nwot 628.16 (n_hooks 80, fired 13)

## Fallback gate

- finite loss: True; 37.7 s/epoch x 20 epochs x 50 archs = 10.5 GPU-h (<= 30: True); proxies finite: True; n_hooks 80
- **GATE PASS**
