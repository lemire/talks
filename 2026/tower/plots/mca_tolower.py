#!/usr/bin/env python3
"""llvm-mca: scalar vs AVX-512 to-lower loop, instructions per byte and IPC."""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 24,
    "axes.titlesize": 26,
    "xtick.labelsize": 24,
    "ytick.labelsize": 20,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "svg.fonttype": "path",
})

BLUE, ORANGE = "#2a78d6", "#eb6834"
labels = ["scalar", "AVX-512"]
colors = [ORANGE, BLUE]
# llvm-mca, 100 iterations: 900 instr / 100 bytes vs 800 instr / 6400 bytes
ipb = [900 / 100, 800 / 6400]
ipc = [4.37, 3.70]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
for ax, vals, title, fmt, top in zip(axes, [ipb, ipc], ["Instructions per byte", "Instructions per cycle (IPC)"],
                                     ["{:g}", "{:.2f}"], [10.5, 5.2]):
    bars = ax.bar(labels, vals, color=colors, width=0.55)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + top * 0.015, fmt.format(v),
                ha="center", va="bottom", fontsize=26, fontweight="bold")
    ax.set_title(title, pad=14)
    ax.set_ylim(0, top)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", length=0)

fig.tight_layout(w_pad=4)
fig.savefig("mca_tolower.svg", bbox_inches="tight")
fig.savefig("mca_tolower.png", dpi=180, bbox_inches="tight")
plt.close()
