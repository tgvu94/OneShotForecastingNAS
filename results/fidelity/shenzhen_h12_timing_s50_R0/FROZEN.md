# FROZEN: proxy task `s50_R0` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 3 lines of the list of the city root; sha1 `4ca9be840d645`.
- Timing root: 3 architectures, 3 epochs; a run of this root is not a label.
- `subset.json`: sha1 `2299e7feafa5c`; 314 of 627 sensors, 542 of 2109 edges, isolated share 0.061; 10261 of 10261 training windows.
- Sensor rule: `{"draw": 0, "method": "R", "seed": 1000, "share": 0.5}`. Period rule: `null`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
