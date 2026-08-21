#!/usr/bin/env python3
"""LLM API input prices at model launch. Log-scale redraw of token_prices-2.png."""
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

FRONTIER = [
    ("GPT-4", "2023-03-14", 30.00),
    ("Turbo", "2023-11-06", 10.00),
    ("Opus", "2024-03-04", 15.00),
    ("4o", "2024-05-13", 5.00),
    ("Sonnet", "2024-06-20", 3.00),
    ("4.1", "2025-04-14", 2.00),
    ("Grok 4.5", "2026-07-16", 2.00),
    ("Grok 4.6", "2026-08-12", 2.00),
]

SMALL = [
    ("3.5", "2023-03-01", 2.00),
    ("Haiku", "2024-03-04", 0.25),
    ("mini", "2024-07-18", 0.15),
    ("V3", "2024-12-26", 0.27),
    ("Flash", "2025-01-30", 0.10),
    ("nano", "2025-04-14", 0.10),
]

BLUE = "#1f77b4"
RED = "#d62728"

# Short names placed in data coordinates (log-friendly y).
# (text, date, y, ha, va, color)
LABELS = [
    ("GPT-4", "2023-07-01", 40, "center", "top", BLUE),
    ("Turbo", "2023-10-01", 7.0, "center", "top", BLUE),
    ("Opus", "2024-03-04", 22, "center", "bottom", BLUE),
    ("4o", "2024-06-01", 6.2, "left", "bottom", BLUE),
    ("Sonnet", "2024-08-01", 3.5, "left", "bottom", BLUE),
    ("4.1", "2025-05-25", 2.55, "center", "bottom", BLUE),
    ("4.5", "2026-06-01", 1.35, "center", "top", BLUE),
    ("Grok 4.6", "2026-07-01", 3.4, "center", "bottom", BLUE),
    ("3.5", "2023-04-20", 2.0, "left", "bottom", RED),
    ("Haiku", "2024-01-15", 0.34, "center", "bottom", RED),
    ("mini", "2024-07-18", 0.105, "center", "top", RED),
    ("V3", "2024-11-20", 0.36, "center", "bottom", RED),
    ("Flash", "2025-03-25", 0.08, "left", "top", RED),
    ("nano", "2025-06-10", 0.13, "left", "bottom", RED),
]


def to_dt(s):
    return datetime.strptime(s, "%Y-%m-%d")


plt.rcParams.update({
    "font.size": 34,
    "axes.titlesize": 48,
    "axes.labelsize": 38,
    "xtick.labelsize": 32,
    "ytick.labelsize": 32,
    "legend.fontsize": 34,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

fig, ax = plt.subplots(figsize=(12.0, 7.2), dpi=180)

fx = [to_dt(d) for _, d, _ in FRONTIER]
fy = [p for _, _, p in FRONTIER]
sx = [to_dt(d) for _, d, _ in SMALL]
sy = [p for _, _, p in SMALL]

ax.plot(fx, fy, color=BLUE, marker="o", markersize=16, linewidth=3.6, zorder=3)
ax.plot(sx, sy, color=RED, marker="s", markersize=14, linewidth=3.6, zorder=3)

for text, date, y, ha, va, color in LABELS:
    ax.text(to_dt(date), y, text, color=color, fontsize=30,
            ha=ha, va=va, clip_on=False)

ax.set_yscale("log")
ax.set_title("Token price at launch", pad=16)
ax.set_ylabel("$ / million tokens")
ax.set_ylim(0.045, 80)
ax.set_xlim(to_dt("2022-12-01"), to_dt("2027-04-01"))
ax.set_yticks([0.1, 1, 10, 30])
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
ax.yaxis.set_minor_formatter(plt.NullFormatter())
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.grid(True, which="major", linestyle="-", color="0.88", zorder=0)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig("token_prices-2.png", dpi=180, bbox_inches="tight", facecolor="white")
