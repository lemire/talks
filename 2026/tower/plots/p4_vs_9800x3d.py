#!/usr/bin/env python3
"""Clock frequency range: Pentium 4 (2000) vs Ryzen 7 9800X3D (2024)."""

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.size": 24,
    "axes.labelsize": 24,
    "xtick.labelsize": 22,
    "ytick.labelsize": 22,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

chips = ["Pentium 4\n2000", "Ryzen 7 9800X3D\n2024"]
low = [1.3, 4.7]
high = [2.0, 5.2]

BLUE, ORANGE = "#2a78d6", "#eb6834"

x = np.arange(len(chips))
w = 0.36
fig, ax = plt.subplots(figsize=(7, 6.5))
b1 = ax.bar(x - w / 2, low, w, color=BLUE, label="Min")
b2 = ax.bar(x + w / 2, high, w, color=ORANGE, label="Max")
for bars in (b1, b2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.08,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=22, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(chips)
ax.set_ylabel("GHz")
ax.set_ylim(0, 6)
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
ax.legend(frameon=False, loc="upper left")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("p4_vs_9800x3d.svg", bbox_inches="tight")
fig.savefig("p4_vs_9800x3d.png", dpi=180, bbox_inches="tight")
plt.close()
