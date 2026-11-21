# FROZEN: proxy task `t50_L` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 3 lines of the list of the city root; sha1 `4ca9be840d645`.
- Timing root: 3 architectures, 3 epochs; a run of this root is not a label.
- `subset.json`: sha1 `6205e4e4fc1b3`; 627 of 627 sensors, 2109 of 2109 edges, isolated share 0.008; 4933 of 10261 training windows.
- Sensor rule: `null`. Period rule: `{"method": "L", "row_share": 0.4861111111111111, "share": 0.5, "steps_per_week": 1008, "weeks_kept": [5, 6, 7, 8, 9], "weeks_total": 10}`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
