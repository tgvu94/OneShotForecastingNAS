# FROZEN: proxy task `s25_P0` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 50 lines of the list of the city root; sha1 `459b1db47a878`.
- One of the 14 proxy tasks of arm D; the settings are fixed in the plan before any run.
- `subset.json`: sha1 `1fafcf2639036`; 157 of 627 sensors, 129 of 2109 edges, isolated share 0.280; 10261 of 10261 training windows.
- Sensor rule: `{"share": 0.25, "method": "P", "draw": 0, "seed": 3000, "strata": 27}`. Period rule: `null`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
