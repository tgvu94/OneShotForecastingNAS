# FROZEN: proxy task `s50_R0` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 50 lines of the list of the city root; sha1 `459b1db47a878`.
- One of the 14 proxy tasks of arm D; the settings are fixed in the plan before any run.
- `subset.json`: sha1 `2299e7feafa5c`; 314 of 627 sensors, 542 of 2109 edges, isolated share 0.061; 10261 of 10261 training windows.
- Sensor rule: `{"share": 0.5, "method": "R", "draw": 0, "seed": 1000}`. Period rule: `null`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
