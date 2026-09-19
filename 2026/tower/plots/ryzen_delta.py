#!/usr/bin/env python3
"""Where the +5.5 B transistors went: Ryzen 7 5800X3D (2022) -> 9800X3D (2024)."""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 28,
    "axes.labelsize": 28,
    "xtick.labelsize": 26,
    "ytick.labelsize": 30,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

BLUE, AQUA, ORANGE = "#2a78d6", "#1baf7a", "#eb6834"

parts = ["Cache", "I/O", "Core"]
delta = [0.0, 3.4 - 2.09, 8.315 - 4.15]
colors = [ORANGE, AQUA, BLUE]
total = sum(delta)

fig, ax = plt.subplots(figsize=(8, 6.5))
bars = ax.barh(parts, delta, color=colors, height=0.6)
for bar, d in zip(bars, delta):
    ax.text(d + 0.12, bar.get_y() + bar.get_height() / 2,
            f"+{d:.1f} B  ({d / total:.0%})", va="center", ha="left",
            fontsize=28, fontweight="bold")

ax.set_xlabel("Added transistors (billions)")
ax.set_xlim(0, 6.9)
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.xaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("ryzen_delta.svg", bbox_inches="tight")
fig.savefig("ryzen_delta.png", dpi=180, bbox_inches="tight")
plt.close()
