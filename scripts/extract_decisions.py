# Requires the anonymized pilot records (not distributed). Usage:
#   python scripts/extract_decisions.py <export_A> <export_B> <export_C> private/decisions.csv
"""Extract non-personal fields from the anonymized Smart City pilot files.

Reads app_*.json for one model version and returns one row per application with:
model, app, ai_decision, routed, op_id, op_decision, duration_s, ai_latency_ms, correct.
No applicant or operator text fields (names, addresses, comments, field values) are read out.
`correct` follows the correctness mapping fixed before data collection (paper, Table 7).
"""
import glob, json, os, sys

CORRECT = {
    ("Flagged for verification", "Accepted after verification"): True,
    ("Flagged for verification", "Rejected after verification"): False,
    ("Rejected", "Fixed & accepted"): True,
    ("Rejected", "Rejected"): True,
    ("Rejected", "Accepted"): False,
}

def load(folder, model):
    rows = []
    for f in sorted(glob.glob(os.path.join(folder, "app_*.json"))):
        dec = json.load(open(f))["logs"][0]["decisions"]
        ai = next(e for e in dec if e["action"] == "ai_evaluated")
        op = next((e for e in dec if e["action"] == "operator_verified"), None)
        ai_dec = ai["payload"]["ai_decision"]
        r = dict(model=model, app=os.path.basename(f)[:-5], ai_decision=ai_dec,
                 routed=op is not None, ai_latency_ms=ai.get("latency_ms"),
                 op_id=None, op_decision=None, duration_s=None, correct=None)
        if op:
            p = op["payload"]
            r.update(op_id=p.get("op_id"), op_decision=p.get("op_decision"),
                     duration_s=op.get("duration_s"),
                     correct=CORRECT.get((ai_dec, p.get("op_decision"))))
        rows.append(r)
    return rows

if __name__ == "__main__":
    # Usage: python scripts/extract_decisions.py <export_A> <export_B> <export_C> private/decisions.csv
    # Each <export_X> is the folder of anonymized application records (app_*.json) exported by
    # the pilot operator for one model version.
    import csv
    if len(sys.argv) != 5:
        sys.exit("usage: extract_decisions.py <export_A> <export_B> <export_C> <out.csv>")
    rows = []
    for folder, m in zip(sys.argv[1:4], "ABC"):
        rows += load(folder, m)
    out = sys.argv[4]
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(len(rows), "rows ->", out)
