#!/usr/bin/env python3
"""Apple M2 -> M5 (base chips, 2022-2025), one figure per slide.

Geekbench 6: browser.geekbench.com Mac chart, Sept 2026 (Mac mini M2, MacBook Pro 14" M3,
Mac mini M4, MacBook Pro 14" M5). Frequencies: P-core / E-core max. Transistors: Apple
keynote figures (none disclosed for the M5). Decode width: public microarchitecture analyses.
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

chips = ["M2", "M3", "M4", "M5"]
years = [2022, 2023, 2024, 2025]
node = ["N5P", "N3B", "N3E", "N3P"]
BLUE, ORANGE, AQUA, GRAY = "#2a78d6", "#eb6834", "#1baf7a", "#52514e"
XLIM = (2021.5, 2025.5)


def style(ax, extra=None):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xticks(years)
    third = extra if extra is not None else node
    ax.set_xticklabels([f"{y}\n{c}\n{n}" for y, c, n in zip(years, chips, third)])
    ax.set_xlim(*XLIM)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{name}.svg", bbox_inches="tight")
    fig.savefig(f"{name}.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


# --- Geekbench 6 ------------------------------------------------------------
single = [2401, 2767, 3278, 3642]
multi = [9814, 11544, 15345, 17955]
labels = [f"{y}\n{c}\n{e}" for y, c, e in zip(years, chips, ["4P+4E", "4P+4E", "4P+6E", "4P+6E"])]
fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))
for ax, vals, title, top in zip(axes, [single, multi], ["Single-core", "Multi-core"], [4400, 21500]):
    bars = ax.bar(labels, vals, color=BLUE, width=0.6)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + top * 0.015, f"{v:,}",
                ha="center", va="bottom", fontsize=22, fontweight="bold")
    ax.set_title(title, pad=14)
    ax.set_ylim(0, top)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(lambda x, _: f"{int(x):,}")
axes[0].set_ylabel("Geekbench 6 score")
fig.tight_layout(w_pad=3)
save(fig, "apple_m2m5_geekbench")

# --- Frequency -------------------------------------------------------------
pcore = [3.49, 4.05, 4.41, 4.61]
ecore = [2.42, 2.75, 2.89, 3.05]
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(years, pcore, marker="o", markersize=10, linewidth=2.5, color=ORANGE, label="P-core max")
ax.plot(years, ecore, marker="o", markersize=10, linewidth=2.5, color=BLUE, label="E-core max")
for y, p, e in zip(years, pcore, ecore):
    ax.annotate(f"{p:.1f}", (y, p), textcoords="offset points", xytext=(0, 12), ha="center", fontsize=21, color=GRAY)
    ax.annotate(f"{e:.1f}", (y, e), textcoords="offset points", xytext=(0, -24), ha="center", fontsize=21, color=GRAY)
ax.set_ylabel("GHz")
ax.set_ylim(0, 6)
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
ax.legend(frameon=False, loc="lower right")
style(ax)
save(fig, "apple_m2m5_frequency")

# --- Transistors -----------------------------------------------------------
transistors = [20, 25, 28]
fig, ax = plt.subplots(figsize=(8, 6))
w = 0.6
ax.bar(years[:3], transistors, w, color=BLUE, edgecolor="white", linewidth=1.5)
for y, t in zip(years, transistors):
    ax.text(y, t + 0.5, f"{t} B", ha="center", va="bottom", fontsize=22, fontweight="bold")
# Apple has not published a transistor count for the M5
ax.bar([2025], [28], w, color="none", edgecolor=GRAY, linewidth=1.5, linestyle="--")
ax.text(2025, 14, "not\ndisclosed", ha="center", va="center", fontsize=17, color=GRAY)
ax.set_ylabel("Transistors (billions)")
ax.set_ylim(0, 32)
ax.set_yticks([0, 8, 16, 24, 32])
style(ax)
save(fig, "apple_m2m5_transistors")

# --- Cores -----------------------------------------------------------------
pcores = [4, 4, 4, 4]
ecores = [4, 4, 6, 6]
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(years, pcores, w, color=ORANGE, edgecolor="white", linewidth=1.5, label="Performance")
ax.bar(years, ecores, w, bottom=pcores, color=BLUE, edgecolor="white", linewidth=1.5, label="Efficiency")
for y, p, e in zip(years, pcores, ecores):
    ax.text(y, p / 2, f"{p}P", ha="center", va="center", fontsize=22, fontweight="bold", color="white")
    ax.text(y, p + e / 2, f"{e}E", ha="center", va="center", fontsize=22, fontweight="bold", color="white")
    ax.text(y, p + e + 0.2, f"{p + e}", ha="center", va="bottom", fontsize=22, fontweight="bold")
ax.set_ylabel("CPU cores")
ax.set_ylim(0, 14.5)
ax.set_yticks([0, 2, 4, 6, 8, 10, 12])
ax.legend(frameon=False, loc="upper left", ncol=2, fontsize=20, handlelength=1.2)
style(ax)
save(fig, "apple_m2m5_cores")

# --- Decode width (P-core) -------------------------------------------------
decode = [8, 9, 10, 10]
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(years, decode, w, color=BLUE, edgecolor="white", linewidth=1.5)
for y, d in zip(years, decode):
    ax.text(y, d + 0.15, f"{d}", ha="center", va="bottom", fontsize=22, fontweight="bold")
ax.set_ylabel("Decode width (instr./cycle)")
ax.set_ylim(0, 12)
ax.set_yticks([0, 2, 4, 6, 8, 10, 12])
style(ax)
save(fig, "apple_m2m5_decode")

# --- Memory bandwidth ------------------------------------------------------
bw = [100, 100, 120, 153.6]
mem = ["LPDDR5\n6400", "LPDDR5\n6400", "LPDDR5X\n7500", "LPDDR5X\n9600"]
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(years, bw, w, color=AQUA, edgecolor="white", linewidth=1.5)
for y, b in zip(years, bw):
    ax.text(y, b + 2, f"{b:.0f}", ha="center", va="bottom", fontsize=22, fontweight="bold")
ax.set_ylabel("GB/s")
ax.set_ylim(0, 175)
ax.set_yticks([0, 50, 100, 150])
style(ax, extra=mem)
ax.tick_params(axis="x", labelsize=19)
save(fig, "apple_m2m5_bandwidth")
