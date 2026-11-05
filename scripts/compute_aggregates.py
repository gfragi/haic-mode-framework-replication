"""Compute the aggregate tables released with the paper from the private decision-level file.

Usage: python scripts/compute_aggregates.py private/decisions.csv data/
Input columns: model, app, ai_decision, routed, ai_latency_ms, op_id, op_decision, duration_s, correct.
Regimes are defined by the AI decision that routed a case: flag (Flagged for verification) or
reject (Rejected). T_r = share of routed cases with correct == True; D = mean operator duration_s.
"""
import csv, os, sys, statistics as st

REG = {"Flagged for verification": "flag", "Rejected": "reject"}
rows = list(csv.DictReader(open(sys.argv[1]))); out = sys.argv[2]
os.makedirs(out, exist_ok=True)

def tr(rs): return round(sum(r["correct"] == "True" for r in rs) / len(rs), 4) if rs else ""
def D(rs): return round(st.mean(float(r["duration_s"]) for r in rs), 2) if rs else ""
def write(name, recs):
    with open(os.path.join(out, name), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(recs[0])); w.writeheader(); w.writerows(recs)
    print(f"{name}: {len(recs)} rows")

M = {m: [r for r in rows if r["model"] == m] for m in "ABC"}
RT = {m: [r for r in M[m] if r["routed"] == "True"] for m in "ABC"}

# Table 6: AI decisions and routing
recs = []
for m in "ABC":
    R, rt = M[m], RT[m]; c = lambda k: sum(r["ai_decision"] == k for r in R)
    lat = [float(r["ai_latency_ms"]) / 1000 for r in R]
    recs.append(dict(model=m, n=len(R), accepted=c("Accepted"), corrected_by_model=c("Corrected by model"),
        flagged=c("Flagged for verification"), rejected=c("Rejected"), ai_alone=len(R) - len(rt),
        ai_alone_pct=round(100 * (len(R) - len(rt)) / len(R), 1), routed=len(rt),
        routed_pct=round(100 * len(rt) / len(R), 1), ai_latency_mean_s=round(st.mean(lat), 2),
        ai_latency_sd_s=round(st.stdev(lat), 2)))
write("dataset_by_model.csv", recs)

# Table 9: regimes
recs = []
for m in "ABC":
    for g in ("reject", "flag", "all"):
        v = RT[m] if g == "all" else [r for r in RT[m] if REG[r["ai_decision"]] == g]
        recs.append(dict(model=m, regime=g, n=len(v), w=round(len(v) / len(RT[m]), 4), Tr=tr(v), D_s=D(v)))
write("regimes.csv", recs)

# Table 10 and Fig. 2: per operator
recs = []
for m in "ABC":
    for o in sorted({r["op_id"] for r in RT[m]}, key=int):
        v = [r for r in RT[m] if r["op_id"] == o]; rj = [r for r in v if REG[r["ai_decision"]] == "reject"]
        recs.append(dict(model=m, operator=f"Op-{o}", n_flag=len(v) - len(rj), n_reject=len(rj),
                         Tr=tr(v), D_s=D(v), Tr_reject_regime=tr(rj)))
write("operators.csv", recs)

# Table 8 (allocation values)
recs = []
for m in "ABC":
    R, rt = M[m], RT[m]
    fl = [r for r in rt if REG[r["ai_decision"]] == "flag"]; rj = [r for r in rt if REG[r["ai_decision"]] == "reject"]
    ovr = sum(r["op_decision"] == "Accepted" for r in rj); fix = sum(r["op_decision"] == "Fixed & accepted" for r in rj)
    recs.append(dict(model=m, flag_share_of_routed=round(len(fl) / len(rt), 4), overrides_of_rejections=ovr,
        override_rate_reject=round(ovr / len(rj), 4), fixed_and_accepted=fix,
        human_decisive_pct=round(100 * (ovr + fix + len(fl)) / len(R), 1)))
write("allocation.csv", recs)

# Eq. 1 and Fig. 3: decomposition with model A's within-regime values held fixed
A = {g: [r for r in RT["A"] if REG[r["ai_decision"]] == g] for g in ("flag", "reject")}
recs = []
for m in "ABC":
    w = {g: sum(REG[r["ai_decision"]] == g for r in RT[m]) / len(RT[m]) for g in ("flag", "reject")}
    recs.append(dict(model=m, D_observed_s=D(RT[m]), D_predicted_s=round(sum(w[g] * st.mean(float(r["duration_s"]) for r in A[g]) for g in w), 2),
        Tr_observed=tr(RT[m]), Tr_predicted=round(sum(w[g] * sum(r["correct"] == "True" for r in A[g]) / len(A[g]) for g in w), 4)))
write("decomposition.csv", recs)

# Section 5.3: repeated exposure
rid = {m: {r["app"]: r for r in RT[m]} for m in "ABC"}
recs = []
seen = {"B": set(rid["A"]), "C": set(rid["A"]) | set(rid["B"])}
for m in "BC":
    for g in ("reject", "flag"):
        for lab, cond in (("seen_before", True), ("first_time", False)):
            v = [r for a, r in rid[m].items() if REG[r["ai_decision"]] == g and (a in seen[m]) == cond]
            recs.append(dict(model=m, regime=g, group=lab, n=len(v), D_s=D(v), Tr=tr(v)))
write("repeat_exposure.csv", recs)
recs = []
for m, p in (("B", "A"), ("C", "A"), ("C", "B")):
    ov = [a for a in rid[m] if a in rid[p]]
    same_ai = [a for a in ov if rid[m][a]["ai_decision"] == rid[p][a]["ai_decision"]]
    recs.append(dict(model=m, earlier_model=p, routed_in_both=len(ov), same_ai_decision=len(same_ai),
        same_operator_decision=sum(rid[m][a]["op_decision"] == rid[p][a]["op_decision"] for a in same_ai),
        same_operator=sum(rid[m][a]["op_id"] == rid[p][a]["op_id"] for a in ov)))
write("repeat_overlap.csv", recs)
