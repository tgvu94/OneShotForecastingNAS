# FROZEN: proxy task `s10_C0` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 50 lines of the list of the city root; sha1 `459b1db47a878`.
- One of the 14 proxy tasks of arm D; the settings are fixed in the plan before any run.
- `subset.json`: sha1 `f77a98039955f`; 63 of 627 sensors, 221 of 2109 edges, isolated share 0.000; 10261 of 10261 training windows.
- Sensor rule: `{"share": 0.1, "method": "C", "draw": 0, "seed": 2000, "walk_starts": 1}`. Period rule: `null`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
