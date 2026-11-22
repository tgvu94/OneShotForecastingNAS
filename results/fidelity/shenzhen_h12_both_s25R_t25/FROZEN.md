# FROZEN: proxy task `both_s25R_t25` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 50 lines of the list of the city root; sha1 `459b1db47a878`.
- A proxy task on both axes, added after the timing run: only a task on both axes has a cost share of 0.25 or less.
- `subset.json`: sha1 `314b8244b2d4e`; 157 of 627 sensors, 129 of 2109 edges, isolated share 0.236; 2917 of 10261 training windows.
- Sensor rule: `{"share": 0.25, "method": "R", "draw": 0, "seed": 1000}`. Period rule: `{"share": 0.25, "method": "L", "weeks_total": 10, "weeks_kept": [7, 8, 9], "steps_per_week": 1008, "row_share": 0.2916666666666667}`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
