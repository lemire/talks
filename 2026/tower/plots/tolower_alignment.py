#!/usr/bin/env python3
"""AVX-512 to-lower, 16 KB in L1: cycles per byte vs start offset from a 64-byte boundary
(Xeon Gold 6548N, big4). Data from ../bench/results_alignment_big4.csv."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 24,
    "axes.labelsize": 24,
    "xtick.labelsize": 22,
    "ytick.labelsize": 22,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "svg.fonttype": "path",
})

BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#52514e"
rows = list(csv.DictReader(open(Path(__file__).parent.parent / "bench" / "results_alignment_big4.csv")))
offsets = [int(r["offset"]) for r in rows]
cpb = [float(r["cycles_per_byte"]) for r in rows]

fig, ax = plt.subplots(figsize=(15, 6.5))
colors = [BLUE if o == 0 else ORANGE for o in offsets]
ax.bar(offsets, cpb, color=colors, width=0.8)
ax.axhline(0.034, color=GRAY, linestyle="--", linewidth=2)
ax.text(63.5, 0.034, "llvm-mca: 0.034", ha="right", va="bottom", fontsize=22, color=GRAY)
ax.annotate(f"aligned: {cpb[0]:.3f}", (0, cpb[0]), xytext=(4, 0.0515), textcoords="data",
            fontsize=22, fontweight="bold", color=BLUE, va="center",
            arrowprops=dict(arrowstyle="-", color=BLUE, lw=1.5))
mid = sum(cpb[1:]) / len(cpb[1:])
ax.text(32, mid + 0.004, f"unaligned: {mid:.3f}  (+{(mid / cpb[0] - 1) * 100:.0f}%)", ha="center", va="bottom",
        fontsize=22, fontweight="bold", color=ORANGE)

ax.set_xlabel("start offset from a 64-byte boundary (bytes)")
ax.set_ylabel("cycles per byte")
ax.set_xlim(-1, 64)
ax.set_xticks([0, 8, 16, 24, 32, 40, 48, 56, 63])
ax.set_ylim(0, 0.058)
ax.set_yticks([0, 0.01, 0.02, 0.03, 0.04, 0.05])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("tolower_alignment.svg", bbox_inches="tight")
fig.savefig("tolower_alignment.png", dpi=180, bbox_inches="tight")
plt.close()
