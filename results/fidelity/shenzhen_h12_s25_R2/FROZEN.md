# FROZEN: proxy task `s25_R2` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 50 lines of the list of the city root; sha1 `459b1db47a878`.
- One of the 14 proxy tasks of arm D; the settings are fixed in the plan before any run.
- `subset.json`: sha1 `e31dc80588f56`; 157 of 627 sensors, 154 of 2109 edges, isolated share 0.229; 10261 of 10261 training windows.
- Sensor rule: `{"share": 0.25, "method": "R", "draw": 2, "seed": 1002}`. Period rule: `null`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
