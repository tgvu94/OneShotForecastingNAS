# FROZEN: results/freshlist/pemsbay_h12 — a fresh list at the city of a shared-list root

A second random draw of 150 architectures from the space of the shared list, trained at PEMS-BAY under the benchst
protocol (`pilot.train_arch --mask-zeros`, 20 epochs, patience 5, min 8, seed 0, h = 12). No architecture of this
list is in the shared list. No model, rule or setting is fit on the labels of this root before its readings exist.

- `archs.jsonl`: 150 architectures, space `dartsts_graph_v1`, sampler seed 2031, `--stratify`
  (sha1 `6eb6bb29128ecbf542d9b219c759377c557a5bc7`). Drawn by `pilot.sample_archs --n 150 --seed 2031 --stratify`
  on a copy of the shared list, so the sampler skipped every shared `arch_id`; the file is the 150 added lines.
- Strata, equal to the shared list: 48 graph-blind, 30 gcn, 30 diffusion, 18 control, 24 any graph.
- Mix of the other axes, a property of the draw and not corrected:

  | list | mae | mse | quantile | linear decoder | seq decoder |
  |---|---|---|---|---|---|
  | shared | 40 | 55 | 55 | 66 | 84 |
  | fresh | 51 | 45 | 54 | 78 | 72 |

- `data/`: byte copy of `results/benchst/pemsbay_h12/data` (probe batch sha1 `2afa33cc29a3`..., adjacency, 8 permutations).
- `train/`: written by the jobs of this root only.
- Cluster: Narval, one `a100_3g.20gb` slice, as the shared-list root of this city.
