#!/usr/bin/env python3
"""String -> value lookup, URL protocols (6 keys), ns per lookup on an Apple M3 Max.
From the ConstexprCore perfect_hash benchmarks (sudo perf counters, shuffled key stream)."""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 22,
    "axes.labelsize": 22,
    "xtick.labelsize": 20,
    "ytick.labelsize": 22,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "svg.fonttype": "path",
})
BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#a3a29e"

data = [  # name, ns, color   (static perfect-hash / static tables in gray, dynamic tables in orange)
    ("std::unordered_map", 12.80, ORANGE),
    ("ankerl::unordered_dense", 12.16, ORANGE),
    ("absl::flat_hash_map", 9.82, ORANGE),
    ("pthash", 9.71, GRAY),
    ("frozen::unordered_map", 8.27, GRAY),
    ("naive if-chain", 7.54, GRAY),
    ("gperf (1989)", 5.56, GRAY),
    ("kronuz::phf", 5.10, GRAY),
    ("ConstexprCore perfect_hash", 1.19, BLUE),
]
data = data[::-1]
fig, ax = plt.subplots(figsize=(14, 7))
names = [d[0] for d in data]; vals = [d[1] for d in data]; cols = [d[2] for d in data]
bars = ax.barh(names, vals, color=cols, height=0.68)
for bar, v in zip(bars, vals):
    ax.text(v + 0.2, bar.get_y() + bar.get_height() / 2, f"{v:.2f} ns", va="center", fontsize=20, fontweight="bold")
ax.set_xlim(0, 15.5)
ax.set_xlabel("nanoseconds per lookup (lower is better)")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.xaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5); ax.set_axisbelow(True)
ax.tick_params(axis="y", length=0)
fig.tight_layout()
fig.savefig("phf_results.svg", bbox_inches="tight")
fig.savefig("phf_results.png", dpi=150, bbox_inches="tight")
plt.close()
