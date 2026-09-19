#!/usr/bin/env python3
"""Fixing ill-formed UTF-16 with two overlapping vectors (Clausecker & Lemire)."""
from svgkit import *

W, H = 1400, 700
lane, gap, x0 = 70, 5, 330
svg = SVG(W, H)
units = ["w", "o", "r", 0xD800, "l", "d", 0xD83D, 0xDE0A, "!", 0xDC00, "x", "y"]
n = len(units)
rowW = n * (lane + gap) - gap
prev = 0x0020

def show(u):
    return f"{u:04X}" if isinstance(u, int) else u
def kind(u):
    if isinstance(u, int) and 0xD800 <= u <= 0xDBFF: return "high"
    if isinstance(u, int) and 0xDC00 <= u <= 0xDFFF: return "low"
    return "other"
KC = {"high": ORANGE, "low": VIOLET, "other": LIGHT}
TC = {"high": "white", "low": "white", "other": INK}

def label(y, title, code):
    svg.text(20, y + 18, title, size=24, weight="bold")
    svg.text(20, y + 46, code, size=18, fill=BLUE, mono=True)

def lanes(y, vals, fills, tcols, size=18, h=50):
    for i, (v, f, t) in enumerate(zip(vals, fills, tcols)):
        svg.cell(x0 + i * (lane + gap), y, lane, h, v, f, tcolor=t, size=size)

# index row
for i in range(n):
    svg.text(x0 + i * (lane + gap) + lane / 2, 30, str(i), size=16, fill=GRAY, anchor="middle")

y = 40
label(y, "block", "load(in)")
lanes(y, [show(u) for u in units], [KC[kind(u)] for u in units], [TC[kind(u)] for u in units])
y = 120
lb = [prev] + units[:-1]
label(y, "lookback", "load(in - 1)")
lanes(y, [show(u) for u in lb], [KC[kind(u)] for u in lb], [TC[kind(u)] for u in lb])
svg.text(x0 + rowW + 12, y + 24, "one lane", size=18, fill=GRAY)
svg.text(x0 + rowW + 12, y + 46, "earlier", size=18, fill=GRAY)

y = 220
lb_high = [1 if kind(u) == "high" else 0 for u in lb]
bl_low = [1 if kind(u) == "low" else 0 for u in units]
label(y, "lb_is_high", "(lookback & FC00) == D800")
lanes(y, [str(b) for b in lb_high], [ORANGE if b else PALE for b in lb_high], ["white" if b else GRAY for b in lb_high], size=20, h=44)
y = 290
label(y, "block_is_low", "(block & FC00) == DC00")
lanes(y, [str(b) for b in bl_low], [VIOLET if b else PALE for b in bl_low], ["white" if b else GRAY for b in bl_low], size=20, h=44)

y = 375
ill = [a ^ b for a, b in zip(lb_high, bl_low)]
label(y, "illseq = XOR", "lb_is_high ^ block_is_low")
lanes(y, [str(b) for b in ill], [MAGENTA if b else PALE for b in ill], ["white" if b else GRAY for b in ill], size=20, h=44)
svg.text(x0 + rowW + 12, y + 20, "all zero:", size=18, fill=GREEN, weight="bold")
svg.text(x0 + rowW + 12, y + 42, "copy, done", size=18, fill=GREEN, weight="bold")
# annotate the valid pair
i = 7
svg.text(x0 + i * (lane + gap) + lane / 2, y + 66, "1 ^ 1 = 0: a valid pair", size=16, fill=GREEN, anchor="middle")

y = 480
label(y, "output (rare path)", "blend(block, FFFD, mask)")
out = list(units)
out[3] = 0xFFFD; out[9] = 0xFFFD
fills = [GREEN if (i in (6, 7)) else (MAGENTA if out[i] == 0xFFFD else KC[kind(u)]) for i, u in enumerate(out)]
tcols = ["white" if fills[i] != LIGHT else INK for i in range(n)]
lanes(y, [show(u) for u in out], fills, tcols)
svg.text(x0 + 3 * (lane + gap) + lane / 2, y + 74, "lone high → U+FFFD", size=16, fill=MAGENTA, anchor="middle")
svg.text(x0 + 6.5 * (lane + gap) + lane / 2, y + 74, "😊 kept", size=16, fill=GREEN, anchor="middle")
svg.text(x0 + 9 * (lane + gap) + lane / 2, y + 74, "lone low → U+FFFD", size=16, fill=MAGENTA, anchor="middle")

svg.rect(20, 590, 1360, 80, PALE, rx=10)
svg.text(700, 622, "2 loads, 2 ANDs, 2 compares, 1 XOR, 1 test per block: no loop-carried state, no per-unit branch", size=21, anchor="middle")
svg.text(700, 654, "idempotent, so the tail is just one more block aligned to the end of the input", size=20, fill=GRAY, anchor="middle")
svg.save("../utf16fix_flow.svg")
