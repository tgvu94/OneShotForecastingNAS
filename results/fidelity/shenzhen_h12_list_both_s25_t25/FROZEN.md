# FROZEN: proxy task `both_s25_t25` of shenzhen

- City root: `results/benchst/shenzhen_h12` (labels, schedule, zero mask, probe batch, adjacency).
- `archs.jsonl`: the first 150 lines of the list of the city root; sha1 `11eac76e13dd5`.
- The proxy task both_s25_t25 as a filter on a longer part of the list; a run of this root has few epochs.
- `subset.json`: sha1 `850c67efdf54e`; 157 of 627 sensors, 129 of 2109 edges, isolated share 0.280; 2917 of 10261 training windows.
- Sensor rule: `{"share": 0.25, "method": "P", "draw": 0, "seed": 3000, "strata": 27}`. Period rule: `{"share": 0.25, "method": "L", "weeks_total": 10, "weeks_kept": [7, 8, 9], "steps_per_week": 1008, "row_share": 0.2916666666666667}`.
- Runs: `pilot.train_arch --mask-zeros`; the trainer reads `subset.json` of the root.
