# FROZEN: proxy task `both_s25_t25` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 3 lines of the list of the city root; sha1 `4ca9be840d645`.
- Timing root: 3 architectures, 3 epochs; a run of this root is not a label.
- `subset.json`: sha1 `850c67efdf54e`; 157 of 627 sensors, 129 of 2109 edges, isolated share 0.280; 2917 of 10261 training windows.
- Sensor rule: `{"draw": 0, "method": "P", "seed": 3000, "share": 0.25, "strata": 27}`. Period rule: `{"method": "L", "row_share": 0.2916666666666667, "share": 0.25, "steps_per_week": 1008, "weeks_kept": [7, 8, 9], "weeks_total": 10}`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
