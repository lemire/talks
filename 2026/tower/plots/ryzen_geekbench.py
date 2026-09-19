#!/usr/bin/env python3
"""Geekbench 6 scores: Ryzen 7 5800X3D / 7800X3D / 9800X3D (browser.geekbench.com, Sept 2026)."""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 24,
    "axes.titlesize": 26,
    "axes.labelsize": 24,
    "xtick.labelsize": 22,
    "ytick.labelsize": 22,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

BLUE = "#2a78d6"
labels = ["2022\n5800X3D\nZen 3", "2023\n7800X3D\nZen 4", "2024\n9800X3D\nZen 5"]
single = [2016, 2426, 2969]
multi = [11832, 15508, 18751]

fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))
for ax, vals, title, top in zip(axes, [single, multi], ["Single-core", "Multi-core"], [3600, 22000]):
    bars = ax.bar(labels, vals, color=BLUE, width=0.6)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + top * 0.015, f"{v:,}",
                ha="center", va="bottom", fontsize=22, fontweight="bold")
    ax.set_title(title, pad=14)
    ax.set_ylim(0, top)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(lambda x, _: f"{int(x):,}")

axes[0].set_ylabel("Geekbench 6 score")
fig.tight_layout(w_pad=3)
fig.savefig("ryzen_geekbench.svg", bbox_inches="tight")
fig.savefig("ryzen_geekbench.png", dpi=180, bbox_inches="tight")
plt.close()
