#!/usr/bin/env python3
"""IP address parsing throughput on the Intel Xeon Gold 6548N (Emerald Rapids), from
Lemire & Nizipli, "Parsing IP Addresses with AVX-512" (Tables 2 and 4)."""

import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 22,
    "axes.titlesize": 26,
    "axes.labelsize": 22,
    "xtick.labelsize": 20,
    "ytick.labelsize": 22,
    "font.family": "sans-serif",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "svg.fonttype": "path",
})

BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#a3a29e"

ipv4 = [  # name, Mv/s, color
    ("getaddrinfo", 8.9, ORANGE),
    ("inet_aton", 19, ORANGE),
    ("Boost.Asio", 25, ORANGE),
    ("inet_pton", 30, ORANGE),
    ("ada (scalar)", 35, ORANGE),
    ("SSE (Muła)", 52, GRAY),
    ("SSE (simdzone)", 290, GRAY),
    ("AVX-512, table-free", 240, BLUE),
    ("AVX-512, table", 299, BLUE),
]
ipv6 = [
    ("ipv6-parse", 4.6, ORANGE),
    ("getaddrinfo", 5.2, ORANGE),
    ("Boost.Asio", 8.3, ORANGE),
    ("ipaddress", 8.7, ORANGE),
    ("inet_pton", 9.8, ORANGE),
    ("ada (scalar)", 11, ORANGE),
    ("AVX-512 (ours)", 103, BLUE),
]

fig, axes = plt.subplots(1, 2, figsize=(17, 7), gridspec_kw={"width_ratios": [1.1, 1]})
for ax, data, title, xmax in zip(axes, [ipv4, ipv6], ["IPv4, random addresses", "IPv6, traffic-like addresses"], [360, 125]):
    names = [d[0] for d in data]
    vals = [d[1] for d in data]
    cols = [d[2] for d in data]
    bars = ax.barh(names, vals, color=cols, height=0.68)
    for bar, v in zip(bars, vals):
        ax.text(v + xmax * 0.012, bar.get_y() + bar.get_height() / 2, f"{v:g}", va="center", ha="left",
                fontsize=20, fontweight="bold")
    ax.set_title(title, pad=14)
    ax.set_xlim(0, xmax)
    ax.set_xlabel("million addresses / second")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.grid(True, linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)

fig.tight_layout(w_pad=3)
fig.savefig("ip_results.svg", bbox_inches="tight")
fig.savefig("ip_results.png", dpi=150, bbox_inches="tight")
plt.close()
