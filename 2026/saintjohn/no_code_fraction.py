#!/usr/bin/env python3
"""Two-bar chart: share of respondents writing no code by hand."""
import matplotlib.pyplot as plt

PAPER = "#faf8f4"
INK = "#1c1c28"
MUTED = "#5c5c6b"
ACCENT = "#9a2b2b"
ACCENT_SOFT = "#c45c52"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial"],
    "font.size": 18,
    "axes.titlesize": 26,
    "axes.labelsize": 18,
    "xtick.labelsize": 20,
    "ytick.labelsize": 16,
    "figure.facecolor": PAPER,
    "axes.facecolor": PAPER,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": MUTED,
    "axes.edgecolor": INK,
})

labels = ["March 15", "August 16"]
values = [21.7, 38.9]
colors = [ACCENT_SOFT, ACCENT]

fig, ax = plt.subplots(figsize=(12.2, 5.0), dpi=180)
bars = ax.bar(labels, values, width=0.52, color=colors, zorder=3)

ax.set_title("Fraction writing no code", pad=14, fontfamily="Iowan Old Style",
             fontweight="semibold", color=INK)
ax.set_ylim(0, 48)
ax.set_ylabel("%")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}"))
ax.yaxis.grid(True, linestyle=":", color="#e4ded3", zorder=0)
ax.set_axisbelow(True)
for spine in ("top", "right", "left"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(INK)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", length=0, pad=8)

for bar, value in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1.4,
        f"{value:.1f}%",
        ha="center",
        va="bottom",
        fontsize=22,
        fontweight="medium",
        color=INK,
    )

fig.tight_layout()
fig.savefig("no_code_fraction.png", dpi=180, facecolor=PAPER, bbox_inches="tight")
