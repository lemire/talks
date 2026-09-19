#!/usr/bin/env python3
"""Core microarchitecture parameters: Zen 3 / Zen 4 / Zen 5 (Ryzen 7 X3D parts)."""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 24,
    "axes.titlesize": 24,
    "xtick.labelsize": 22,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

gens = ["Zen 3\n2022", "Zen 4\n2023", "Zen 5\n2024"]
colors = ["#a9c8ee", "#6aa0e0", "#2a78d6"]
metrics = [
    ("L2 cache per core", [512, 1024, 1024], ["512 KB", "1 MB", "1 MB"]),
    ("L1 data cache", [32, 32, 48], ["32 KB", "32 KB", "48 KB"]),
    ("Dispatch width", [6, 6, 8], ["6", "6", "8"]),
    ("Integer ALUs", [4, 4, 6], ["4", "4", "6"]),
    ("Reorder buffer", [256, 320, 448], ["256", "320", "448"]),
]

fig, axes = plt.subplots(2, 3, figsize=(16, 9.5))
axes = axes.flatten()
axes[-1].axis("off")
for ax, (title, vals, labels) in zip(axes, metrics):
    bars = ax.bar(gens, vals, color=colors, width=0.62)
    top = max(vals)
    for bar, lab in zip(bars, labels):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + top * 0.02, lab,
                ha="center", va="bottom", fontsize=22, fontweight="bold")
    ax.set_title(title, pad=12)
    ax.set_ylim(0, top * 1.22)
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="x", length=0)

fig.tight_layout(w_pad=3, h_pad=3)
fig.savefig("zen_core_specs.svg", bbox_inches="tight")
fig.savefig("zen_core_specs.png", dpi=180, bbox_inches="tight")
plt.close()
