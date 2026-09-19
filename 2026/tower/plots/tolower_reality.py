#!/usr/bin/env python3
"""llvm-mca model vs measured cycles/byte for the to-lower kernels (Xeon Gold 6548N, big4).
Measured numbers come from ../bench/results_big4.csv (bench/tolower_bench.cpp)."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.size": 24,
    "axes.labelsize": 24,
    "xtick.labelsize": 21,
    "ytick.labelsize": 22,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "svg.fonttype": "path",
})

BLUE, ORANGE = "#2a78d6", "#eb6834"

rows = list(csv.DictReader(open(Path(__file__).parent.parent / "bench" / "results_big4.csv")))
def cpb(kernel, nbytes, upper):
    for r in rows:
        if r["kernel"] == kernel and int(r["bytes"]) == nbytes and float(r["upper_fraction"]) == upper:
            return float(r["cycles_per_byte"])
    raise KeyError((kernel, nbytes, upper))

KB, MB = 1 << 10, 1 << 20
conditions = [
    ("llvm-mca\nmodel", 2.06, 0.034),
    ("16 KB in L1\nall lowercase", cpb("scalar", 16 * KB, 0.0), cpb("avx512", 16 * KB, 0.0)),
    ("16 KB in L1\n50% uppercase", cpb("scalar", 16 * KB, 0.5), cpb("avx512", 16 * KB, 0.5)),
    ("256 MB in RAM\n50% uppercase", cpb("scalar", 256 * MB, 0.5), cpb("avx512", 256 * MB, 0.5)),
]

x = np.arange(len(conditions))
w = 0.38
fig, ax = plt.subplots(figsize=(15, 7))
scalar = [c[1] for c in conditions]
avx = [c[2] for c in conditions]
b1 = ax.bar(x - w / 2, scalar, w, color=ORANGE, label="scalar")
b2 = ax.bar(x + w / 2, avx, w, color=BLUE, label="AVX-512")
for bars in (b1, b2):
    for bar in bars:
        v = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, v * 1.15, f"{v:.2g}" if v < 1 else f"{v:.1f}",
                ha="center", va="bottom", fontsize=22, fontweight="bold")

ax.set_yscale("log")
ax.set_ylim(0.01, 40)
ax.set_yticks([0.01, 0.1, 1, 10])
ax.set_yticklabels(["0.01", "0.1", "1", "10"])
ax.set_ylabel("cycles per byte (log scale)")
ax.set_xticks(x)
ax.set_xticklabels([c[0] for c in conditions])
ax.tick_params(axis="x", length=0)
ax.legend(frameon=False, loc="upper left", ncol=2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
ax.set_axisbelow(True)
ax.axvline(0.5, color="#8a8985", linestyle=":", linewidth=1.5)

fig.tight_layout()
fig.savefig("tolower_reality.svg", bbox_inches="tight")
fig.savefig("tolower_reality.png", dpi=180, bbox_inches="tight")
plt.close()
