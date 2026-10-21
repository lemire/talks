#!/usr/bin/env python3
"""Open-weight frontier models: total vs. active parameters, and 4-bit size."""
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


def tint(color, amount=0.35):
    """Opaque mix of color with white, so the grid does not show through."""
    r, g, b = mcolors.to_rgb(color)
    return (1 - amount * (1 - r), 1 - amount * (1 - g), 1 - amount * (1 - b))


# (model, lab, total params in billions, active params in billions, 4-bit size, color)
MODELS = [
    ("Kimi K3", "Moonshot", 2800, 104, "1.4 TB", "#eb6834"),
    ("Qwen3.8 Max", "Alibaba", 2400, 95, "1.2 TB", "#2a78d6"),
    ("DeepSeek V4 Pro", "DeepSeek", 1600, 49, "800 GB", "#1baf7a"),
]

plt.rcParams.update({
    "font.size": 30,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

fig, ax = plt.subplots(figsize=(16.0, 9.0), dpi=150)

rows = list(reversed(MODELS))
for i, (model, lab, total, active, size, color) in enumerate(rows):
    ax.barh(i, total, height=0.62, color=tint(color), zorder=2)
    ax.barh(i, active, height=0.62, color=color, zorder=3)
    ax.text(total + 40, i + 0.12, f"{total / 1000:.1f}T", va="center",
            ha="left", fontsize=40, fontweight="bold", color="#1c1c28")
    ax.text(total + 40, i - 0.22, f"{size} at 4-bit", va="center",
            ha="left", fontsize=24, color="#5c5c6b")
    ax.text(active + 30, i, f"~{active}B active", va="center", ha="left",
            fontsize=26, color="#1c1c28", zorder=4)

ax.set_yticks(range(len(rows)))
ax.set_yticklabels([f"{m}\n{lab}" for m, lab, *_ in rows], fontsize=30,
                   color="#1c1c28", linespacing=1.3)
for tick in ax.get_yticklabels():
    tick.set_fontweight("bold")

ax.set_xlim(0, 3500)
ax.set_xticks([0, 500, 1000, 1500, 2000, 2500, 3000])
ax.set_xticklabels(["0", "0.5T", "1T", "1.5T", "2T", "2.5T", "3T"], fontsize=26)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color="#e4ded3", linewidth=1.5, zorder=0)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#5c5c6b")

fig.subplots_adjust(left=0.27, right=0.97, top=0.86, bottom=0.10)
fig.text(0.01, 0.97, "Open-weight models: total parameters (dark = active per token)",
         fontsize=32, color="#1c1c28", ha="left", va="top")
fig.savefig("open_weights.png", facecolor="white")
