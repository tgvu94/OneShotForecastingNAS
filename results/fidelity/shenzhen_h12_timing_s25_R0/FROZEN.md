# FROZEN: proxy task `s25_R0` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 3 lines of the list of the city root; sha1 `4ca9be840d645`.
- Timing root: 3 architectures, 3 epochs; a run of this root is not a label.
- `subset.json`: sha1 `52189e396f474`; 157 of 627 sensors, 129 of 2109 edges, isolated share 0.236; 10261 of 10261 training windows.
- Sensor rule: `{"draw": 0, "method": "R", "seed": 1000, "share": 0.25}`. Period rule: `null`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
