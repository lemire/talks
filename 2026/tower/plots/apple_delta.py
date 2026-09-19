#!/usr/bin/env python3
"""What +12 B transistors bought: Apple M1 (2020) -> M4 (2024), base chips.

Apple does not break the die down by function (monolithic SoC), so instead of
"where the transistors went" we show what grew, relative to the M1.
Geekbench 6 scores from browser.geekbench.com (Sept 2026).
"""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 28,
    "axes.labelsize": 28,
    "xtick.labelsize": 22,
    "ytick.labelsize": 26,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

BLUE, AQUA, ORANGE, GRAY = "#2a78d6", "#1baf7a", "#eb6834", "#8a8984"

# label, M1 value, M4 value, unit
rows = [
    ("Multi-core", 8582, 15345, ""),
    ("Single-core", 2187, 3278, ""),
    ("Memory BW", 68.25, 120, " GB/s"),
    ("GPU cores", 8, 10, ""),
    ("CPU cores", 8, 10, ""),
    ("Transistors", 16, 28, " B"),
]
parts = [r[0] for r in rows]
growth = [(b - a) / a for _, a, b, _ in rows]
colors = [ORANGE, ORANGE, AQUA, GRAY, GRAY, BLUE]

fig, ax = plt.subplots(figsize=(10, 6.5))
bars = ax.barh(parts, growth, color=colors, height=0.6)
for bar, g, (_, a, b, u) in zip(bars, growth, rows):
    fmt = (lambda v: f"{v:,.0f}") if u != " GB/s" else (lambda v: f"{v:.0f}")
    ax.text(g + 0.02, bar.get_y() + bar.get_height() / 2,
            f"+{g:.0%}  ({fmt(a)}→{fmt(b)}{u})", va="center", ha="left",
            fontsize=22, fontweight="bold")

ax.set_xlabel("Growth, M1 → M4")
ax.set_xlim(0, 2.0)
ax.set_xticks([0, 0.5, 1.0])
ax.xaxis.set_major_formatter(lambda x, _: f"+{x:.0%}")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.xaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("apple_delta.svg", bbox_inches="tight")
fig.savefig("apple_delta.png", dpi=180, bbox_inches="tight")
plt.close()
