#!/usr/bin/env python3
"""simdjson PartialTweets (single core, GB/s) on the Ryzen 7 5800X3D / 7800X3D / 9800X3D.
From lemire.me, "How stagnant is CPU technology?" (January 2026), openbenchmarking.org data."""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 24, "axes.labelsize": 24, "xtick.labelsize": 22, "ytick.labelsize": 22,
    "font.family": "sans-serif", "figure.facecolor": "white", "axes.facecolor": "white", "svg.fonttype": "path",
})
colors = ["#a9c8ee", "#6aa0e0", "#2a78d6"]
labels = ["2022\n5800X3D\nZen 3", "2023\n7800X3D\nZen 4", "2024\n9800X3D\nZen 5"]
gbps = [5.2, 9.0, 12.7]

fig, ax = plt.subplots(figsize=(8, 6.5))
bars = ax.bar(labels, gbps, color=colors, width=0.62)
for b, v in zip(bars, gbps):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.25, f"{v:g} GB/s", ha="center", va="bottom", fontsize=24, fontweight="bold")
ax.set_ylabel("JSON parsing, GB/s (one core)")
ax.set_ylim(0, 15)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5); ax.set_axisbelow(True)
ax.tick_params(axis="x", length=0)
fig.tight_layout()
fig.savefig("simdjson_ryzen.svg", bbox_inches="tight")
fig.savefig("simdjson_ryzen.png", dpi=150, bbox_inches="tight")
plt.close()
