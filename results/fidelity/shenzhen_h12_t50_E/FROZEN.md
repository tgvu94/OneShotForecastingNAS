# FROZEN: proxy task `t50_E` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 50 lines of the list of the city root; sha1 `459b1db47a878`.
- One of the 14 proxy tasks of arm D; the settings are fixed in the plan before any run.
- `subset.json`: sha1 `1047076b865b1`; 627 of 627 sensors, 2109 of 2109 edges, isolated share 0.008; 4505 of 10261 training windows.
- Sensor rule: `null`. Period rule: `{"share": 0.5, "method": "E", "weeks_total": 10, "weeks_kept": [0, 2, 4, 7, 9], "steps_per_week": 1008, "row_share": 0.4861111111111111}`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
