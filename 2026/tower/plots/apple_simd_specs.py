#!/usr/bin/env python3
"""SIMD resources per P-core, Apple M1 -> M5: NEON units, L1 loads/stores, and the SME unit.

NEON: 4 x 128-bit FP/SIMD pipes, 3 loads + 2 stores per cycle (M1: Anandtech/Dougall Johnson;
unchanged through M5). SME (Scalable Matrix Extension) arrived with the M4 as a separate
per-cluster unit with a 512-bit streaming vector length.
"""

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

gens = ["M1\n2020", "M2\n2022", "M3\n2023", "M4\n2024", "M5\n2025"]
colors = ["#c5dbf4", "#a9c8ee", "#6aa0e0", "#3f87dc", "#2a78d6"]
# bar height = bits per cycle (units x width); label = units x width
metrics = [
    ("NEON arithmetic units", [4 * 128] * 5, ["4 ×\n128-bit"] * 5),
    ("Loads per cycle", [3 * 128] * 5, ["3 ×\n128-bit"] * 5),
    ("Stores per cycle", [2 * 128] * 5, ["2 ×\n128-bit"] * 5),
    ("SME matrix unit (M4+)", [0, 0, 0, 512, 512], ["—", "—", "—", "512-bit\nSVL", "512-bit\nSVL"]),
]

fig, axes = plt.subplots(2, 2, figsize=(16, 9.5))
for ax, (title, vals, labels) in zip(axes.flatten(), metrics):
    bars = ax.bar(gens, vals, color=colors, width=0.62)
    top = max(vals)
    for bar, lab in zip(bars, labels):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + top * 0.02, lab,
                ha="center", va="bottom", fontsize=20, fontweight="bold", linespacing=1.1)
    ax.set_title(title, pad=12)
    ax.set_ylim(0, top * 1.35)
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="x", length=0)

fig.tight_layout(w_pad=3, h_pad=3)
fig.savefig("apple_simd_specs.svg", bbox_inches="tight")
fig.savefig("apple_simd_specs.png", dpi=180, bbox_inches="tight")
plt.close()
