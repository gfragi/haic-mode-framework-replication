"""Check that the values reported in the paper match the released aggregate tables.

Usage: python scripts/check_paper_values.py data/
Exits with status 1 if any value differs after rounding to the precision used in the paper.
"""
import csv, os, sys
data = sys.argv[1]
def load(n): return list(csv.DictReader(open(os.path.join(data, n))))
def get(rows, **k): return next(r for r in rows if all(r[a] == v for a, v in k.items()))
ok = True
def check(label, value, expected, nd):
    global ok
    v = round(float(value), nd); good = abs(v - expected) < 1e-9
    ok &= good; print(f"{'OK  ' if good else 'FAIL'} {label}: {v} (paper {expected})")

ds, rg, op, al, dc, rx, ro = (load(n) for n in ("dataset_by_model.csv", "regimes.csv", "operators.csv",
    "allocation.csv", "decomposition.csv", "repeat_exposure.csv", "repeat_overlap.csv"))
for m, auto, pct, lat in (("A", 402, 71.0, 45.1), ("B", 410, 72.4, 15.0), ("C", 458, 80.9, 18.0)):
    r = get(ds, model=m)
    check(f"Table 6 {m} decided by AI alone", r["ai_alone"], auto, 0)
    check(f"Table 6 {m} AI alone %", r["ai_alone_pct"], pct, 1)
    check(f"Table 6 {m} AI latency s", r["ai_latency_mean_s"], lat, 1)
for (m, g), (w, t, d) in {("A","reject"): (.805,.629,77.5), ("A","flag"): (.195,1.0,222.2), ("A","all"): (1,.701,105.7),
        ("B","reject"): (.897,.657,78.5), ("B","flag"): (.103,1.0,222.8), ("B","all"): (1,.692,93.3),
        ("C","reject"): (.787,.600,53.9), ("C","flag"): (.213,1.0,173.1), ("C","all"): (1,.685,79.2)}.items():
    r = get(rg, model=m, regime=g)
    check(f"Table 9 {m} {g} w", r["w"], w, 3); check(f"Table 9 {m} {g} Tr", r["Tr"], t, 3); check(f"Table 9 {m} {g} D", r["D_s"], d, 1)
for m, o, t, d in (("A","Op-5",1.0,222.2), ("B","Op-5",.903,164.0), ("C","Op-5",.571,65.7), ("C","Op-2",.818,94.0)):
    r = get(op, model=m, operator=o); check(f"Table 10 {m} {o} Tr", r["Tr"], t, 3); check(f"Table 10 {m} {o} D", r["D_s"], d, 1)
for m, ov, hd in (("A",.371,18.4), ("B",.343,15.0), ("C",.400,11.8)):
    r = get(al, model=m); check(f"Table 8 {m} override rate", r["override_rate_reject"], ov, 3); check(f"Table 8 {m} human decisive %", r["human_decisive_pct"], hd, 1)
for m, dp, tp in (("B",92.3,.667), ("C",108.3,.708)):
    r = get(dc, model=m); check(f"Sec 5.3 {m} predicted D", r["D_predicted_s"], dp, 1); check(f"Sec 5.3 {m} predicted Tr", r["Tr_predicted"], tp, 3)
for g, lab, d in (("reject","seen_before",52.3), ("reject","first_time",55.1), ("flag","seen_before",171.0), ("flag","first_time",176.2)):
    check(f"Sec 5.3 C {g} {lab} D", get(rx, model="C", regime=g, group=lab)["D_s"], d, 1)
for m, p, n, s in (("B","A",25,11), ("C","A",23,16), ("C","B",19,9)):
    r = get(ro, model=m, earlier_model=p); check(f"Sec 5.3 {p}-{m} same AI decision", r["same_ai_decision"], n, 0); check(f"Sec 5.3 {p}-{m} same operator decision", r["same_operator_decision"], s, 0)
print("ALL VALUES MATCH" if ok else "MISMATCHES FOUND"); sys.exit(0 if ok else 1)
