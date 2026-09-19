#!/usr/bin/env python3
"""Geekbench 6 scores, Apple M1 -> M5 base chips (browser.geekbench.com Mac chart, Sept 2026).

Machines: Mac mini (M1, Late 2020), Mac mini (M2, 2023), MacBook Pro 14" (M3, Nov 2023),
Mac mini (M4, 2024), MacBook Pro 14" (M5, 2025).
"""

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
labels = ["2020\nM1\n4P+4E", "2022\nM2\n4P+4E", "2023\nM3\n4P+4E", "2024\nM4\n4P+6E", "2025\nM5\n4P+6E"]
single = [2187, 2401, 2767, 3278, 3642]
multi = [8582, 9814, 11544, 15345, 17955]

fig, axes = plt.subplots(1, 2, figsize=(17, 6.5))
for ax, vals, title, top in zip(axes, [single, multi], ["Single-core", "Multi-core"], [4400, 21500]):
    bars = ax.bar(labels, vals, color=BLUE, width=0.6)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + top * 0.015, f"{v:,}",
                ha="center", va="bottom", fontsize=21, fontweight="bold")
    ax.set_title(title, pad=14)
    ax.set_ylim(0, top)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(lambda x, _: f"{int(x):,}")

axes[0].set_ylabel("Geekbench 6 score")
fig.tight_layout(w_pad=3)
fig.savefig("apple_geekbench.svg", bbox_inches="tight")
fig.savefig("apple_geekbench.png", dpi=180, bbox_inches="tight")
plt.close()
