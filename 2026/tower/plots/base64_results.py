#!/usr/bin/env python3
"""Base64 decoding with whitespace: C++ on the Xeon Gold 6548N (results/intel.txt of the paper)
and in production browsers on an Apple M4 Max (Enron e-mail dataset)."""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 22, "axes.titlesize": 25, "axes.labelsize": 22,
    "xtick.labelsize": 20, "ytick.labelsize": 20,
    "font.family": "sans-serif", "figure.facecolor": "white", "axes.facecolor": "white",
    "svg.fonttype": "path",
})
BLUE, ORANGE, GRAY, AQUA = "#2a78d6", "#eb6834", "#a3a29e", "#1baf7a"

fig, (ax, bx) = plt.subplots(1, 2, figsize=(17, 6.8), gridspec_kw={"width_ratios": [1.5, 1]})

datasets = ["Google logo\n3 KB, clean", "Enron e-mail\n2 MB, 76-col lines", ".se DNS zone\n35 MB, spaces"]
series = [("OpenSSL 3.3", [0.47, 0.47, 0.49], GRAY), ("Node.js 19", [1.81, 1.79, 1.71], ORANGE), ("simdutf (AVX-512)", [27.8, 17.3, 10.8], BLUE)]
x = np.arange(len(datasets)); w = 0.26
for i, (name, vals, col) in enumerate(series):
    bars = ax.bar(x + (i - 1) * w, vals, w, color=col, label=name)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.5, f"{v:.3g}", ha="center", va="bottom", fontsize=19, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(datasets)
ax.set_ylabel("GB/s"); ax.set_ylim(0, 32)
ax.set_title("C++, Intel Xeon Gold 6548N", pad=14)
ax.legend(frameon=False, loc="upper right", fontsize=19)
ax.tick_params(axis="x", length=0)

browsers = ["Firefox 151\nSpiderMonkey", "Chrome 149\nV8", "Safari 18.6\nWebKit"]
vals = [3.3, 6.6, 10.2]; cols = [GRAY, BLUE, BLUE]
bars = bx.bar(browsers, vals, color=cols, width=0.6)
for b, v in zip(bars, vals):
    bx.text(b.get_x() + b.get_width() / 2, v + 0.2, f"{v:.1f}", ha="center", va="bottom", fontsize=20, fontweight="bold")
bx.set_ylim(0, 12.5); bx.set_ylabel("GB/s")
bx.set_title("Uint8Array.fromBase64, Apple M4 Max", pad=14)
bx.text(1.5, 11.8, "blue: ships our decoder", ha="center", fontsize=19, color=BLUE)
bx.tick_params(axis="x", length=0)

for a in (ax, bx):
    a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
    a.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5); a.set_axisbelow(True)
fig.tight_layout(w_pad=3)
fig.savefig("base64_results.svg", bbox_inches="tight")
fig.savefig("base64_results.png", dpi=150, bbox_inches="tight")
plt.close()
