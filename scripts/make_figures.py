"""Reproduce Figs. 2 and 3 of the paper from the released aggregate tables.

Usage: python scripts/make_figures.py data/ figures/
"""
import csv, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

data, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
def load(n): return list(csv.DictReader(open(os.path.join(data, n))))
BLUE, ORANGE = "#2a78d6", "#eb6834"; INK, MUTED, GRID = "#1f1f1e", "#6b6a64", "#e4e3de"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": MUTED,
    "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False})

ops = load("operators.csv")
fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.3), sharey=True)
for ax, m in zip(axes, "ABC"):
    R = [r for r in ops if r["model"] == m]
    rj = [int(r["n_reject"]) for r in R]; fl = [int(r["n_flag"]) for r in R]; x = range(len(R))
    ax.bar(x, rj, width=0.6, color=BLUE, edgecolor="white", linewidth=1, label="AI-rejected")
    ax.bar(x, fl, width=0.6, bottom=rj, color=ORANGE, edgecolor="white", linewidth=1, label="AI-flagged")
    for xi, r in zip(x, R):
        ax.text(xi, rj[xi] + fl[xi] + 0.8, f"{float(r['D_s']):.0f} s", ha="center", va="bottom", fontsize=7, color=INK)
    ax.set_xticks(list(x)); ax.set_xticklabels([r["operator"] for r in R])
    ax.set_title(f"Model {m}", fontsize=8.5, color=INK, loc="left")
    ax.yaxis.grid(True, color=GRID, linewidth=0.6); ax.set_axisbelow(True)
axes[0].set_ylabel("Routed cases"); axes[0].set_ylim(0, 40)
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="upper right", ncol=2, frameon=False, fontsize=7.5, bbox_to_anchor=(0.99, 1.02))
fig.tight_layout(rect=(0, 0, 1, 0.93))
for ext in ("pdf", "png"): fig.savefig(os.path.join(out, f"fig_routing_by_operator.{ext}"), dpi=300)

dec = load("decomposition.csv")
obs = [float(r["D_observed_s"]) for r in dec]; pred = [float(r["D_predicted_s"]) for r in dec]
fig, ax = plt.subplots(figsize=(3.4, 2.3)); x = range(3); wb = 0.34
b1 = ax.bar([i - wb/2 - 0.01 for i in x], obs, width=wb, color=BLUE, label="Observed")
b2 = ax.bar([i + wb/2 + 0.01 for i in x], pred, width=wb, color=ORANGE, label="Predicted from routing only")
for bars in (b1, b2):
    for b in bars: ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1.5, f"{b.get_height():.1f}", ha="center", fontsize=7, color=INK)
ax.set_xticks(list(x)); ax.set_xticklabels(["Model A", "Model B", "Model C"])
ax.set_ylabel("Mean operator duration D (s)"); ax.set_ylim(0, 125)
ax.yaxis.grid(True, color=GRID, linewidth=0.6); ax.set_axisbelow(True)
fig.legend(*ax.get_legend_handles_labels(), frameon=False, fontsize=7, loc="upper center", ncol=2, bbox_to_anchor=(0.55, 1.0))
fig.tight_layout(rect=(0, 0, 1, 0.9))
for ext in ("pdf", "png"): fig.savefig(os.path.join(out, f"fig_composition_vs_observed.{ext}"), dpi=300)
print("figures written to", out)
