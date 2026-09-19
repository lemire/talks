#!/usr/bin/env python3
"""The table-driven AVX-512 IPv4 parser on 192.168.0.1 (Lemire & Nizipli, "Parsing IP Addresses with AVX-512")."""
from svgkit import *

W, H = 1340, 760
lane, gap, x0 = 52, 4, 400
n = 16
rowW = n * (lane + gap) - gap
svg = SVG(W, H)

def label(y, title, code, note=None):
    svg.text(20, y + 18, title, size=24, weight="bold")
    svg.text(20, y + 46, esc(code), size=18, fill=BLUE, mono=True)
    if note: svg.text(20, y + 70, esc(note), size=18, fill=GRAY)

def lanes(y, vals, fills, tcols, h=52, size=22, mono=True):
    for i, (v, f, t) in enumerate(zip(vals, fills, tcols)):
        svg.cell(x0 + i * (lane + gap), y, lane, h, v, f, tcolor=t, size=size, mono=mono)

def lane_index(y):
    for i in range(n):
        svg.text(x0 + i * (lane + gap) + lane / 2, y, str(i), size=16, fill=GRAY, anchor="middle")

addr = "192.168.0.1"
L = len(addr)
inp = list(addr) + ["0"] * (n - L)
is_dot = [c == "." for c in inp[:L]] + [False] * (n - L)
octet_of = []
o = 0
for i, c in enumerate(inp):
    if i >= L: octet_of.append(None); continue
    if c == ".": octet_of.append(None); o += 1
    else: octet_of.append(o)
OCT = [BLUE, AQUA, VIOLET, MAGENTA]

# row 0: masked load
y = 40
lane_index(y - 10)
label(y, "1. masked load, len = 11", "mask_loadu_epi8(pad='0', len)", "pad with '0': neither dot nor error")
fills = [ORANGE if is_dot[i] else (LIGHT if i >= L else OCT[octet_of[i]]) for i in range(n)]
tcols = [INK if i >= L else "white" for i in range(n)]
lanes(y, inp, fills, tcols)

# row 1: dots + terminator -> partition
y = 150
label(y, "2. dots → partition p", "p = cmpeq(v, '.') | 1 << len", "p = 0xA88: the whole layout in 16 bits")
bits = [1 if is_dot[i] else 0 for i in range(n)]
bits[L] = 1
fills = [ORANGE if is_dot[i] else (YELLOW if i == L else LIGHT) for i in range(n)]
tcols = ["white" if bits[i] else GRAY for i in range(n)]
lanes(y, [str(b) for b in bits], fills, tcols)
svg.text(x0 + 11 * (lane + gap) + lane / 2, y + 74, "end", size=17, fill=YELLOW, anchor="middle", weight="bold")

# row 2: perfect hash (text only)
y = 250
label(y, "3. perfect hash → key", "k = (p * 0x00CF7800) >> 24", "81 layouts → 81 distinct keys")
svg.rect(x0, y + 2, rowW, 48, PALE, rx=8)
svg.text(x0 + rowW / 2, y + 34, "0xA88 × 0x00CF7800  →  k = 136   →   shuffle_table[136], aux_table[136]", size=21, fill=INK, anchor="middle", mono=True)

# row 3: shuffle -> [0, h, t, o] per octet
y = 340
label(y, "4. table shuffle", "shuffle_epi8(v, table[k])", "octet → [0, hundreds, tens, ones]")
digits = [["", "1", "9", "2"], ["", "1", "6", "8"], ["", "", "", "0"], ["", "", "", "1"]]
vals, fills, tcols = [], [], []
for o in range(4):
    for j in range(4):
        d = digits[o][j]
        vals.append(d if d else "0")
        fills.append(OCT[o] if d else LIGHT)
        tcols.append("white" if d else GRAY)
lanes(y, vals, fills, tcols)
for o in range(4):
    xa = x0 + 4 * o * (lane + gap); xb = xa + 4 * lane + 3 * gap
    svg.bracket(xa, xb, y + 66, f"octet {o}", OCT[o], size=17, up=False)

# row 4: VNNI dot product
y = 470
label(y, "5. VNNI dot product", "dpbusd_epi32(digits, weights)", "weights [0, 100, 10, 1] × 4")
wts = ["0", "100", "10", "1"] * 4
lanes(y, wts, [PALE] * n, [GRAY] * n, h=40, size=17)
svg.text(x0 + rowW / 2, y + 74, "↓", size=26, fill=GRAY, anchor="middle")
y2 = y + 90
for o, v in enumerate([192, 168, 0, 1]):
    xa = x0 + 4 * o * (lane + gap)
    svg.cell(xa, y2, 4 * lane + 3 * gap, 52, f"{v}", OCT[o], size=24)

# row 5: validation + result
y = 650
label(y, "6. validate", "p == aux[k] | non-digit | > 255", "all in mask registers: one branch")
svg.rect(x0, y + 2, rowW, 52, PALE, rx=8)
svg.text(x0 + rowW / 2, y + 36, "192.168.0.1  →  0xC0A80001    ·    ~50 instructions, no loop, no per-digit branch", size=21, fill=INK, anchor="middle")

svg.save("../ipv4_pipeline.svg")
