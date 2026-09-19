#!/usr/bin/env python3
"""AMD Ryzen 7 (3800X → 7800X3D): clock frequency and transistor count over years."""

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

chips = ["Ryzen 7 5800X3D", "Ryzen 7 7800X3D", "Ryzen 7 9800X3D"]
years = [2022, 2023, 2024]
uarch = ["Zen 3", "Zen 4", "Zen 5"]
base = [3.4, 4.2, 4.7]
boost = [4.5, 5.0, 5.2]
ccd = [4.15, 6.57, 8.315]
vcache = [4.7, 4.7, 4.7]
iod = [2.09, 3.4, 3.4]
total = [10.9, 14.7, 16.4]

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
GRAY = "#52514e"


def style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xticks(years)
    ax.set_xticklabels([f"{y}\n{c.replace('Ryzen 7 ', '')}\n{u}" for y, c, u in zip(years, chips, uarch)])


# --- Frequency -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(years, boost, marker="o", markersize=10, linewidth=2.5, color=ORANGE, label="Max boost")
ax.plot(years, base, marker="o", markersize=10, linewidth=2.5, color=BLUE, label="Base")
for y, b, m in zip(years, base, boost):
    ax.annotate(f"{m:.1f}", (y, m), textcoords="offset points", xytext=(0, 12),
                ha="center", fontsize=21, color=GRAY)
    ax.annotate(f"{b:.1f}", (y, b), textcoords="offset points", xytext=(0, -24),
                ha="center", fontsize=21, color=GRAY)
ax.set_ylabel("GHz")
ax.set_ylim(0, 6)
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
ax.set_xlim(2021.5, 2024.5)
ax.legend(frameon=False, loc="lower right")
style(ax)
fig.tight_layout()
fig.savefig("ryzen_frequency.svg", bbox_inches="tight")
fig.savefig("ryzen_frequency.png", dpi=180, bbox_inches="tight")
plt.close()

# --- Transistors -----------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 6))
w = 0.6
ax.bar(years, ccd, w, color=BLUE, edgecolor="white", linewidth=1.5, label="Core")
ax.bar(years, iod, w, bottom=ccd, color=AQUA, edgecolor="white", linewidth=1.5, label="I/O")
bottoms = [c + i for c, i in zip(ccd, iod)]
ax.bar(years, vcache, w, bottom=bottoms, color=ORANGE, edgecolor="white", linewidth=1.5, label="Cache")
for y, t in zip(years, total):
    ax.text(y, t + 0.25, f"~{t:.1f} B", ha="center", va="bottom", fontsize=22, fontweight="bold")
ax.set_ylabel("Transistors (billions)")
ax.set_ylim(0, 18.5)
ax.set_yticks([0, 4, 8, 12, 16])
ax.set_xlim(2021.5, 2024.5)
ax.legend(frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5), handlelength=1.2)
style(ax)
fig.tight_layout()
fig.savefig("ryzen_transistors.svg", bbox_inches="tight")
fig.savefig("ryzen_transistors.png", dpi=180, bbox_inches="tight")
plt.close()
