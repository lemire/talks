#!/usr/bin/env python3
"""Flat for two years, then a summer surge. Step series read off the plots in
'A summer of AI optimization' (lemire.me, 2026-09-22); dates are approximate."""
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

START = "2024-08-01"
END = "2026-09-20"

# (label, color, [(date the value takes effect, speedup), ...], label y)
SERIES = [
    ("CRoaring, cardinality", "#2a78d6",
     [(START, 1.0), ("2025-03-10", 0.85), ("2026-08-20", 4.87)], 4.87),
    ("roaring (Go), union", "#eb6834",
     [(START, 1.0), ("2026-05-24", 2.5), ("2026-08-05", 2.85),
      ("2026-08-28", 3.1)], 3.1),
    ("ada, URL parsing", "#1baf7a",
     [(START, 1.0), ("2026-06-28", 1.32), ("2026-08-05", 2.36)], 2.36),
    ("simdutf, ASCII", "#e87ba4",
     [(START, 1.0), ("2026-08-19", 1.94)], 2.0),
    ("fast_float, numbers", "#008300",
     [(START, 1.0), ("2026-02-01", 0.94), ("2026-03-09", 1.13),
      ("2026-06-01", 1.28), ("2026-06-09", 1.59), ("2026-07-13", 1.70)], 1.62),
]


def to_dt(s):
    return datetime.strptime(s, "%Y-%m-%d")


plt.rcParams.update({
    "font.size": 30,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

fig, ax = plt.subplots(figsize=(16.0, 9.0), dpi=150)

# Summer 2026 band.
ax.axvspan(to_dt("2026-06-01"), to_dt(END), color="#f3efe7", zorder=0)
ax.text(to_dt("2026-06-05"), 5.45, "summer\n2026", fontsize=24,
        color="#5c5c6b", va="top", ha="left")

ax.axhline(1.0, color="#5c5c6b", linewidth=2, zorder=1)

for label, color, steps, label_y in SERIES:
    xs = [to_dt(d) for d, _ in steps] + [to_dt(END)]
    ys = [v for _, v in steps] + [steps[-1][1]]
    ax.step(xs, ys, where="post", color=color, linewidth=4.5, zorder=3,
            solid_joinstyle="miter")
    ax.text(to_dt(END), label_y, f"  {steps[-1][1]:.1f}×  {label}",
            color="#1c1c28", fontsize=24, va="center", ha="left",
            clip_on=False)
    ax.plot([to_dt(END)], [steps[-1][1]], marker="o", markersize=11,
            color=color, zorder=4, clip_on=False)

ax.text(to_dt("2025-06-01"), 1.12, "flat for about two years",
        fontsize=30, color="#5c5c6b", ha="center", va="bottom",
        style="italic")

ax.set_xlim(to_dt(START), to_dt(END))
ax.set_ylim(0.5, 5.5)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(["1×", "2×", "3×", "4×", "5×"], fontsize=26)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
ax.tick_params(axis="x", labelsize=26)
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", color="#e4ded3", linewidth=1.5, zorder=0)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#5c5c6b")

fig.subplots_adjust(left=0.06, right=0.66, top=0.86, bottom=0.12)
fig.text(0.01, 0.97, "Speedup vs. August 2024, every commit, same machine",
         fontsize=34, color="#1c1c28", ha="left", va="top")
fig.savefig("summer_timeline.png", facecolor="white")
