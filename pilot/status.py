"""Print one line per (arch, seed) training run from <root>/train/**/metrics.json + log.csv, plus a timing summary.

    python -m pilot.status --root results                    # table
    python -m pilot.status --root results/pems08_h12 --timing-csv results/pems08_h12/tables/status.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path

from pilot.paths import Root


def collect(root: Path) -> list[dict]:
    rows = []
    for m in sorted(root.glob("*/seed*/metrics.json")):
        try:
            rec = json.load(open(m))
        except Exception:  # noqa: BLE001
            rec = {"status": "corrupt"}
        hist = rec.get("history") or []
        secs = [h["seconds"] for h in hist if "seconds" in h]
        rows.append({
            "arch_id": m.parts[-3], "seed": int(m.parts[-2][4:]), "status": rec.get("status"),
            "epochs_run": rec.get("epochs_run", len(hist)), "max_epochs": (rec.get("schedule") or {}).get("max_epochs"),
            "stopped_early": rec.get("stopped_early"), "best_epoch": rec.get("best_epoch"),
            "val_mae": rec.get("val_mae"), "test_mae": rec.get("test_mae"), "val_mse": rec.get("val_mse"), "test_mse": rec.get("test_mse"),
            "params": rec.get("params"), "flops": rec.get("flops"),
            "sec_first_epoch": secs[0] if secs else None,
            "sec_per_epoch": round(statistics.mean(secs[1:]), 1) if len(secs) > 1 else (secs[0] if secs else None),
            "train_seconds": rec.get("train_seconds", round(sum(secs), 1) if secs else None),
            "peak_mem_gb": rec.get("peak_mem_gb", max((h.get("peak_mem_gb", 0) for h in hist), default=None)),
            "lock": (m.parent / "LOCK").exists(),
        })
    return rows


def fmt(v, nd=4):
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


def main():
    ap = argparse.ArgumentParser()
    Root.add_args(ap)
    ap.add_argument("--train-dir", default=None, help="default: <root>/train")
    ap.add_argument("--timing-csv", default=None)
    args = ap.parse_args()
    rows = collect(Path(args.train_dir) if args.train_dir else Root.from_args(args).train)
    cols = ["arch_id", "seed", "status", "epochs_run", "best_epoch", "val_mae", "test_mae", "sec_first_epoch",
            "sec_per_epoch", "train_seconds", "peak_mem_gb", "lock"]
    print(" ".join(f"{c:>15s}" for c in cols))
    for r in rows:
        print(" ".join(f"{fmt(r[c]):>15s}" for c in cols))
    done = [r for r in rows if r["status"] == "done"]
    print(f"\n{len(done)} done / {len(rows)} total; "
          f"{sum(1 for r in rows if r['status'] == 'running')} running, {sum(1 for r in rows if r['status'] == 'failed')} failed")
    if done:
        spe = [r["sec_per_epoch"] for r in done if r["sec_per_epoch"]]
        print(f"seconds/epoch over done runs: mean {statistics.mean(spe):.1f}, min {min(spe):.1f}, max {max(spe):.1f}; "
              f"x{done[0]['max_epochs']} epochs = {statistics.mean(spe) * (done[0]['max_epochs'] or 0) / 60:.1f} min; "
              f"peak mem max {max(r['peak_mem_gb'] or 0 for r in done):.2f} GB")
    if args.timing_csv:
        out = Path(args.timing_csv)
        out.parent.mkdir(parents=True, exist_ok=True)
        tcols = ["arch_id", "seed", "status", "epochs_run", "max_epochs", "stopped_early", "sec_first_epoch", "sec_per_epoch",
                 "train_seconds", "peak_mem_gb", "params", "flops", "best_epoch", "val_mae", "test_mae"]
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=tcols, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print(f"wrote {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
