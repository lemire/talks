#!/usr/bin/env python3
"""Performance-core parameters, Apple M1 -> M5 (base chips, 4 P-cores throughout).

Decode width and cache sizes from public microarchitecture analyses
(Anandtech M1 deep dive; Geekerwan / Chips and Cheese for later cores).
"""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 24,
    "axes.titlesize": 24,
    "xtick.labelsize": 22,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

gens = ["M1\n2020", "M2\n2022", "M3\n2023", "M4\n2024", "M5\n2025"]
colors = ["#c5dbf4", "#a9c8ee", "#6aa0e0", "#3f87dc", "#2a78d6"]
metrics = [
    ("L2 cache (shared by 4 P-cores)", [12, 16, 16, 16, 16], ["12 MB", "16 MB", "16 MB", "16 MB", "16 MB"]),
    ("L1 data cache per core", [128, 128, 128, 128, 128], ["128 KB"] * 5),
    ("Decode width", [8, 8, 9, 10, 10], ["8", "8", "9", "10", "10"]),
    ("Memory bandwidth", [68.25, 100, 100, 120, 153.6], ["68", "100", "100", "120", "154"]),
]

fig, axes = plt.subplots(2, 2, figsize=(16, 9.5))
axes = axes.flatten()
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
axes[3].set_title("Memory bandwidth (GB/s)", pad=12)

fig.tight_layout(w_pad=3, h_pad=3)
fig.savefig("apple_core_specs.svg", bbox_inches="tight")
fig.savefig("apple_core_specs.png", dpi=180, bbox_inches="tight")
plt.close()
