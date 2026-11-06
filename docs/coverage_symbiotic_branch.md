# RQ1: Coverage of the Symbiotic branch in the Novoville deployment

Classification (method section, not an RQ): Table 4 (classification rules), step 1, does not apply, because by design operators decide a share of cases (routed: 29.0% / 27.6% / 19.1% in models A/B/C). Step 2 does not apply either, because the AI decides 71–81% of cases alone. Step 3 applies, since authority is allocated case by case, so the deployment is **Symbiotic**, as in the third published example (Table 5). Model C adds an AI-only "Corrected by model" path (30 cases), which shifts allocation further towards the AI without changing the class.

| Branch question | Metric (framework definition) | Status in this deployment | Value / note |
|---|---|---|---|
| **Q1: How easily does the AI adapt to human feedback?** | Adaptability Score (performance after − before adaptation) | **Partial**: only across model versions, not during use (batch evaluation; the AI does not adapt within a version); attribution to operator feedback unknown | Reject-regime agreement 0.629 → 0.657 → 0.600 (A/B/C) |
| | Strategy Adaptation Effectiveness (query selection improved by feedback) | **Not applicable**: no active querying | — |
| | Feedback Quality (relevance and specificity of feedback) | **Other instrument**: operator field-level corrections and comments are logged, but quality needs expert review | `op_fields_with_error`, `op_comment` present |
| | Feedback Impact (performance change due to feedback) | **Not computable**: no recorded link between operator feedback and retraining | Needs the vendor's training records |
| **Q2: How well are tasks allocated to use human and AI strengths?** | Dynamic Task Allocation (adjustment of task distribution) | **Partial**: allocation is fixed within a version, so only its change across versions is observable | Auto 71.0/72.4/80.9%; flag share of routed 19.5/10.3/21.3%; Op-5 = all flags (A) → mixed (B) → spread (C) |
| | Query Efficiency (queries to reach target accuracy) | **Not applicable**: no active learning | — |
| | Expertise Utilization (% decisions where human input is decisive) | **Computable** | Human-decisive share of all applications 18.4/15.0/11.8% (overrides, corrections, and flagged cases; 12.7/12.2/7.8% without flagged cases); reject-regime override rate 0.371/0.343/0.400 (= 1 − reject-regime T_r) |
| | Knowledge Retention | **Not applicable**: no periods of non-use | — |
| | Model Improvement Rate (Δ performance / Δ time) | **Partial**: across versions only, with an agreement proxy | Same caveat as Adaptability Score |
| | Decision Effectiveness (share of decisions leading to task success) | **Other instrument**: needs ground truth on permit validity; auto-accepted cases are never verified | Audit sample required |
| | Trust & Safety (trust score; safety incidents) | **Partial**: behavioral trust proxy T_r computable per regime; safety incidents (wrongly auto-accepted permits) need an audit | T_r 0.701/0.692/0.685; flag-regime T_r = 1.000 by construction |

## Gaps the case exposes (feedback to the framework)
1. **Allocation share / deferral rate** is the most informative allocation descriptor here, and the tree has no explicit metric for it. Dynamic Task Allocation is defined as *adaptation* of the distribution, not the distribution itself.
2. **Complementary Team Performance** is again missing from the Symbiotic branch (as in Example 3). It cannot be computed here without human-alone and AI-alone decisions on the same cases.
3. **Mode-dependent interpretation:** one logged signal (operator overrides of AI rejections) is *low trust* under Trust & Safety and *high expertise utilization* under Expertise Utilization. The framework should state which reading applies in which mode.
4. **Regime stratification:** any metric over routed cases must be reported per allocation regime (RQ2), because aggregates mix regimes with different durations and agreement by construction.
5. **Within-use vs across-version adaptation:** batch deployments only support across-version comparisons; the tree should say so.

Totals: 11 prescribed metrics → 1 computable, 4 partial, 2 need another instrument, 4 not applicable or not computable.

## Classification criteria
- **Computable:** every field the metric requires is logged.
- **Partial:** the required fields are logged, but only across model versions or as a proxy for part of the construct.
- **Other instrument:** the construct exists in the deployment, but the data it needs (expert ratings, ground truth) are not in the logs.
- **Not applicable:** the deployment lacks the mechanism the metric measures (active querying, periods of non-use).
