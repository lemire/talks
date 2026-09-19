#!/usr/bin/env python3
"""SIMD width and L1 load/store bandwidth per cycle: Zen 3 / Zen 4 / Zen 5."""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 24,
    "axes.titlesize": 24,
    "xtick.labelsize": 22,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "svg.fonttype": "path",  # embed glyphs so browsers render the same layout as the PNG
})

gens = ["Zen 3\n2022", "Zen 4\n2023", "Zen 5\n2024"]
colors = ["#a9c8ee", "#6aa0e0", "#2a78d6"]
# bar height = bits per cycle (units x width); label = units x width
metrics = [
    ("SIMD arithmetic units", [4 * 256, 4 * 256, 4 * 512], ["4 ×\n256-bit", "4 ×\n256-bit", "4 ×\n512-bit"]),
    ("Loads per cycle", [2 * 256, 2 * 256, 2 * 512], ["2 ×\n256-bit", "2 ×\n256-bit", "2 ×\n512-bit"]),
    ("Stores per cycle", [256, 256, 512], ["1 ×\n256-bit", "1 ×\n256-bit", "1 ×\n512-bit"]),
]

fig, axes = plt.subplots(1, len(metrics), figsize=(17, 6))
for ax, (title, vals, labels) in zip(axes, metrics):
    bars = ax.bar(gens, vals, color=colors, width=0.62)
    top = max(vals)
    for i, (bar, lab) in enumerate(zip(bars, labels)):
        lift = top * 0.14 if i == 1 else 0  # stagger the middle label so it never collides with its neighbours
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + top * 0.02 + lift, lab,
                ha="center", va="bottom", fontsize=21, fontweight="bold", linespacing=1.1)
    ax.set_title(title, pad=12)
    ax.set_ylim(0, top * 1.40)
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="x", length=0)

fig.tight_layout(w_pad=3)
fig.savefig("zen_simd_specs.svg", bbox_inches="tight")
fig.savefig("zen_simd_specs.png", dpi=180, bbox_inches="tight")
plt.close()
