# FROZEN: proxy task `full` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 3 lines of the list of the city root; sha1 `4ca9be840d645`.
- Timing root: 3 architectures, 3 epochs; a run of this root is not a label.
- No `subset.json`: the whole city, as the reference of the timing run.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
