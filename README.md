# Replication package: mode-based HAIC evaluation applied to a municipal permit workflow

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23973173.svg)](https://doi.org/10.5281/zenodo.23973173)

This repository accompanies the paper

> Fragiadakis, G., Pnevmatikakis, A., Diou, C., Kousiouris, G., Talantzis, F., & Nikolaidou, M.
> *Evaluating Human–AI Collaboration by Collaboration Mode: A Framework and Its Application to a
> Live Municipal Decision Workflow.* Submitted to the International Journal of Human–Computer Interaction.

It contains the analysis scripts and the aggregate tables behind every number, table, and figure
of the field study (Sections 4–5). Table and figure numbers refer to the submitted version.

## What is and is not included

| Included | Not included |
|---|---|
| Aggregate tables per model version, allocation regime, and operator (`data/`) | The anonymized pilot records (`app_*.json`) |
| Scripts that compute the aggregates from decision-level data | The decision-level file (`private/decisions.csv`) |
| Scripts that reproduce the figures and check every reported value from the aggregates | Any applicant or operator personal data |
| The metric-coverage assessment of the Symbiotic branch (`docs/`) | |

The pilot records belong to Novoville Ltd. and the municipal authority and remain with them.
Operator identifiers in the tables are anonymized labels (Op-1 to Op-5).

## Quick start (public data only)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/check_paper_values.py data/      # prints OK/FAIL per value; ends with ALL VALUES MATCH
python scripts/make_figures.py data/ figures/   # writes Figs. 2 and 3
```

## Map from paper to files

| Paper item | Released file | Produced by |
|---|---|---|
| Table 6 (AI decisions, routing, latency) | `data/dataset_by_model.csv` | `compute_aggregates.py` |
| Table 7 (correctness mapping) | `scripts/extract_decisions.py` (`CORRECT`) | — |
| Table 8 (coverage values) | `data/allocation.csv`, `data/regimes.csv`, `docs/coverage_symbiotic_branch.md` | `compute_aggregates.py` |
| Table 9 (allocation regimes) | `data/regimes.csv` | `compute_aggregates.py` |
| Table 10 (per operator) and reject-regime spread (Sec. 5.2) | `data/operators.csv` | `compute_aggregates.py` |
| Eq. 1, predicted vs. observed values (Sec. 5.3) | `data/decomposition.csv` | `compute_aggregates.py` |
| Repeated-exposure checks (Sec. 5.3) | `data/repeat_exposure.csv`, `data/repeat_overlap.csv` | `compute_aggregates.py` |
| Fig. 2 (routing by operator) | `figures/fig_routing_by_operator.pdf` | `make_figures.py` |
| Fig. 3 (observed vs. predicted duration) | `figures/fig_composition_vs_observed.pdf` | `make_figures.py` |
| All values above | — | `check_paper_values.py` |

## Full pipeline (requires the pilot records)

```bash
pip install -r requirements-full.txt
python scripts/extract_decisions.py <export_A> <export_B> <export_C> private/decisions.csv
python scripts/compute_aggregates.py private/decisions.csv data/
python scripts/crosscheck_haic_metrics.py private/decisions.csv   # D and T_r with haic-metrics 0.3.0
```

`extract_decisions.py` reads only the AI decision, routing, operator decision, review duration, and
AI latency of each application; it does not read names, field values, or comments.
`crosscheck_haic_metrics.py` recomputes $D$ and $T_r$ with the published library
([haic-metrics 0.3.0](https://doi.org/10.5281/zenodo.23896317)) and gives the same values as
`compute_aggregates.py`.

## Definitions

- **Allocation regime**: the AI decision that routed an application to an operator, `flag`
  (Flagged for verification) or `reject` (Rejected).
- **T_r**: share of routed applications in which the operator's decision validated the AI's
  assessment under the mapping in Table 7.
- **D**: mean operator review duration in seconds.
- **Predicted values** (Eq. 1): regime shares of the model in question combined with model A's
  within-regime values.

## Citation

Please cite the paper and this repository:

> Fragiadakis, G., Pnevmatikakis, A., Diou, C., Kousiouris, G., Talantzis, F., & Nikolaidou, M. (2026).
> *Replication package: mode-based HAIC evaluation applied to a municipal permit workflow* (v1.0.0).
> Zenodo. https://doi.org/10.5281/zenodo.23973173

Machine-readable metadata are in `CITATION.cff`.

## License

Code: MIT. Aggregate tables and documentation: CC BY 4.0.
