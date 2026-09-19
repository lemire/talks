#!/usr/bin/env python3
"""STREAM bandwidth vs strstr search speed (Zen 5 AWS, single thread)."""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 20,
    "axes.titlesize": 22,
    "axes.labelsize": 20,
    "xtick.labelsize": 20,
    "ytick.labelsize": 18,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

labels = ["STREAM", "strstr"]
values = [46, 9.5]
colors = ["#1f77b4", "#ff7f0e"]

fig, ax = plt.subplots(figsize=(6.2, 6.4))
bars = ax.bar(labels, values, color=colors, width=0.62)

for bar, value in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1.2,
        f"{value:g} GB/s",
        ha="center",
        va="bottom",
        fontsize=20,
        fontweight="bold",
    )

ax.set_ylabel("GB/s")
ax.set_ylim(0, 56)
ax.set_yticks([0, 10, 20, 30, 40, 50])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("strstr_bandwidth.svg", bbox_inches="tight")
fig.savefig("strstr_bandwidth.png", dpi=180, bbox_inches="tight")
plt.close()
