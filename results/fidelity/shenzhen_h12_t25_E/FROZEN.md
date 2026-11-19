# FROZEN: proxy task `t25_E` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 50 lines of the list of the city root; sha1 `459b1db47a878`.
- One of the 14 proxy tasks of arm D; the settings are fixed in the plan before any run.
- `subset.json`: sha1 `5602e5956fe03`; 627 of 627 sensors, 2109 of 2109 edges, isolated share 0.008; 2703 of 10261 training windows.
- Sensor rule: `null`. Period rule: `{"share": 0.25, "method": "E", "weeks_total": 10, "weeks_kept": [0, 4, 9], "steps_per_week": 1008, "row_share": 0.2916666666666667}`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
