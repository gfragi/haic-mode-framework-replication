"""Cross-check D and T_r against haic-metrics 0.3.0. Requires private/decisions.csv.

Usage: python scripts/crosscheck_haic_metrics.py private/decisions.csv
"""
import csv, sys
from haic_metrics import compute_metrics
rows = list(csv.DictReader(open(sys.argv[1])))
REG = {"Flagged for verification": "flag", "Rejected": "reject"}
for m in "ABC":
    for g in ("all", "reject", "flag"):
        R = [r for r in rows if r["model"] == m and r["routed"] == "True" and (g == "all" or REG[r["ai_decision"]] == g)]
        dec = [{"actor_type": "human", "action": "operator_verified", "t": float(i),
                "duration_s": float(r["duration_s"]), "correct": r["correct"] == "True"} for i, r in enumerate(R)]
        met = compute_metrics(dec, rt_max_s=300.0)["metrics"]
        print(f"model {m} {g:6s} n={len(R):3d}  D={met['D']:.1f}  Tr={met['Tr']:.3f}")
