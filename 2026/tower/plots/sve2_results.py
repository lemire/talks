#!/usr/bin/env python3
"""simdjson indexing stage (stage 1), NEON classifier vs SVE2 MATCH classifier, GB/s over the
22-file simdjson corpus. AWS Graviton 4 (c8g.2xlarge) and Graviton 5 (c9g.2xlarge), GCC 15 and
clang 21, -mcpu=native. From lemire.me, "Faster JSON parsing with SVE2 on ARM processors" (2026)."""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 22, "axes.labelsize": 22, "xtick.labelsize": 21, "ytick.labelsize": 20,
    "font.family": "sans-serif", "figure.facecolor": "white", "axes.facecolor": "white",
    "svg.fonttype": "path",
})
GRAY, BLUE = "#a3a29e", "#2a78d6"
groups = ["Graviton 4\nclang 21", "Graviton 4\nGCC 15", "Graviton 5\nclang 21", "Graviton 5\nGCC 15"]
neon = [4.8, 5.5, 6.3, 7.1]
sve2 = [5.3, 5.8, 6.6, 7.3]

x = np.arange(len(groups)); w = 0.36
fig, ax = plt.subplots(figsize=(14, 6.5))
b1 = ax.bar(x - w / 2, neon, w, color=GRAY, label="NEON: tbl classifier (4 instructions)")
b2 = ax.bar(x + w / 2, sve2, w, color=BLUE, label="SVE2: match (1 instruction)")
for b, v in zip(b1, neon):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.08, f"{v:.1f}", ha="center", va="bottom", fontsize=20, fontweight="bold", color="#52514e")
for b, v, v0 in zip(b2, sve2, neon):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.08, f"{v:.1f}", ha="center", va="bottom", fontsize=20, fontweight="bold", color=BLUE)
    ax.text(b.get_x() + b.get_width() / 2, v + 0.62, f"+{(v / v0 - 1) * 100:.0f}%", ha="center", va="bottom", fontsize=18, color=BLUE)
ax.set_xticks(x); ax.set_xticklabels(groups)
ax.set_ylabel("indexing stage, GB/s"); ax.set_ylim(0, 9.2)
ax.legend(frameon=False, loc="upper left", fontsize=19)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5); ax.set_axisbelow(True)
ax.tick_params(axis="x", length=0)
fig.tight_layout()
fig.savefig("sve2_results.svg", bbox_inches="tight")
fig.savefig("sve2_results.png", dpi=150, bbox_inches="tight")
plt.close()
