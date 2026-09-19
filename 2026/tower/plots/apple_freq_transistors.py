#!/usr/bin/env python3
"""Apple M1 -> M5 (base chips): max clock frequency and transistor count over years.

Frequencies: P-core / E-core max as reported by Geekbench and powermetrics.
Transistors: Apple keynote figures. Apple did not disclose a count for the M5.
"""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 24,
    "axes.titlesize": 26,
    "axes.labelsize": 24,
    "xtick.labelsize": 22,
    "ytick.labelsize": 22,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

chips = ["M1", "M2", "M3", "M4", "M5"]
years = [2020, 2022, 2023, 2024, 2025]
node = ["N5", "N5P", "N3B", "N3E", "N3P"]
pcore = [3.20, 3.49, 4.05, 4.41, 4.61]
ecore = [2.06, 2.42, 2.75, 2.89, 3.05]
transistors = [16, 20, 25, 28, None]

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
GRAY = "#52514e"


def style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xticks(years)
    ax.set_xticklabels([f"{y}\n{c}\n{n}" for y, c, n in zip(years, chips, node)])


# --- Frequency -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(years, pcore, marker="o", markersize=10, linewidth=2.5, color=ORANGE, label="P-core max")
ax.plot(years, ecore, marker="o", markersize=10, linewidth=2.5, color=BLUE, label="E-core max")
for y, p, e in zip(years, pcore, ecore):
    ax.annotate(f"{p:.1f}", (y, p), textcoords="offset points", xytext=(0, 12),
                ha="center", fontsize=21, color=GRAY)
    ax.annotate(f"{e:.1f}", (y, e), textcoords="offset points", xytext=(0, -24),
                ha="center", fontsize=21, color=GRAY)
ax.set_ylabel("GHz")
ax.set_ylim(0, 6)
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
ax.set_xlim(2019.4, 2025.6)
ax.legend(frameon=False, loc="lower right")
style(ax)
fig.tight_layout()
fig.savefig("apple_frequency.svg", bbox_inches="tight")
fig.savefig("apple_frequency.png", dpi=180, bbox_inches="tight")
plt.close()

# --- Transistors -----------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 6))
w = 0.6
known = [(y, t) for y, t in zip(years, transistors) if t is not None]
ax.bar([y for y, _ in known], [t for _, t in known], w, color=BLUE, edgecolor="white", linewidth=1.5)
for y, t in known:
    ax.text(y, t + 0.5, f"{t} B", ha="center", va="bottom", fontsize=22, fontweight="bold")
# Apple has not published a transistor count for the M5
ax.bar([2025], [28], w, color="none", edgecolor=GRAY, linewidth=1.5, linestyle="--")
ax.text(2025, 14, "not\ndisclosed", ha="center", va="center", fontsize=16, color=GRAY)
ax.set_ylabel("Transistors (billions)")
ax.set_ylim(0, 32)
ax.set_yticks([0, 8, 16, 24, 32])
ax.set_xlim(2019.4, 2025.6)
style(ax)
fig.tight_layout()
fig.savefig("apple_transistors.svg", bbox_inches="tight")
fig.savefig("apple_transistors.png", dpi=180, bbox_inches="tight")
plt.close()
