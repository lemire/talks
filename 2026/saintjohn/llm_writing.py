#!/usr/bin/env python3
"""Share of PubMed Central papers showing LLM-assisted writing (full paper).
Holzwarth, González-Márquez and Kobak, arXiv:2608.10715 (2026), Table 1."""
import matplotlib.pyplot as plt

PERIODS = ["2023", "2024", "2025", "Dec. 2025"]
SHARE = [0.19, 0.52, 0.77, 0.89]
# One hue, light to dark: later means more.
COLORS = ["#f4b183", "#eb6834", "#c4452a", "#9a2b2b"]

plt.rcParams.update({
    "font.size": 30,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

fig, ax = plt.subplots(figsize=(16.0, 9.0), dpi=150)

xs = range(len(PERIODS))
ax.bar(xs, [100 * s for s in SHARE], width=0.66, color=COLORS, zorder=3)
for x, s in zip(xs, SHARE):
    ax.text(x, 100 * s + 2.5, f"{round(100 * s)}%", ha="center", va="bottom",
            fontsize=54, fontweight="bold", color="#1c1c28")

ax.set_xticks(list(xs))
ax.set_xticklabels(PERIODS, fontsize=32, color="#1c1c28")
ax.set_ylim(0, 106)
ax.set_yticks([0, 25, 50, 75])
ax.set_yticklabels(["0", "25%", "50%", "75%"], fontsize=24,
                   color="#5c5c6b")
ax.tick_params(axis="both", length=0)
ax.grid(axis="y", color="#e4ded3", linewidth=1.5, zorder=0)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#5c5c6b")

fig.subplots_adjust(left=0.08, right=0.98, top=0.82, bottom=0.16)
fig.text(0.01, 0.97, "Most biomedical papers now show LLM-assisted writing",
         fontsize=34, fontweight="bold", color="#1c1c28", ha="left", va="top")
fig.text(0.01, 0.895, "Share of open-access papers in PubMed Central (full text)",
         fontsize=26, color="#5c5c6b", ha="left", va="top")
fig.text(0.01, 0.025,
         "Holzwarth, González-Márquez & Kobak, arXiv:2608.10715 (2026), "
         "Table 1. Standard errors: 2 to 5 points.",
         fontsize=20, color="#5c5c6b", ha="left", va="bottom")
fig.savefig("llm_writing.png", facecolor="white")
