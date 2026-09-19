#!/usr/bin/env python3
"""Compare the whole key at once: 16-byte load, shuffle-mask to the key length, one vector compare."""
from svgkit import *
import random

W, H = 1420, 640
lane, gap, x0 = 50, 4, 380
n = 16
rowW = n * (lane + gap) - gap
svg = SVG(W, H)
random.seed(7)
garbage = [random.choice("x@k;#=)Zq?~.9m") for _ in range(13)]

def label(y, title, code):
    svg.text(20, y + 18, title, size=24, weight="bold")
    svg.text(20, y + 46, code, size=18, fill=BLUE, mono=True)

def lanes(y, vals, fills, tcols, size=22):
    for i, (v, f, t) in enumerate(zip(vals, fills, tcols)):
        svg.cell(x0 + i * (lane + gap), y, lane, 50, v, f, tcolor=t, size=size)

y = 40
label(y, "1. load 16 bytes at p", "vld1q_u8(p)  ·  _mm_loadu_si128(p)")
vals = list("PUT") + garbage
lanes(y, vals, [AQUA] * 3 + [LIGHT] * 13, ["white"] * 3 + [GRAY] * 13)
svg.bracket(x0, x0 + 3 * lane + 2 * gap, y - 6, "key, len = 3", AQUA, size=18)
svg.bracket(x0 + 3 * (lane + gap), x0 + rowW, y - 6, "whatever follows in memory", GRAY, size=18)

y = 160
label(y, "2. shuffle with mask[len]", "vqtbl1q_u8(v, mask[3])  ·  pshufb")
mask = ["0", "1", "2"] + ["80"] * 13
lanes(y, mask, [PALE] * 16, [INK] * 3 + [GRAY] * 13, size=18)
svg.text(x0 + rowW + 12, y + 32, "0x80 → zero", size=18, fill=GRAY)
svg.text(x0 + rowW / 2, y + 84, "↓", size=26, fill=GRAY, anchor="middle")
y = 250
lanes(y, list("PUT") + ["0"] * 13, [AQUA] * 3 + [LIGHT] * 13, ["white"] * 3 + [GRAY] * 13)
svg.text(x0 + rowW + 12, y + 32, "query, zero-padded", size=18, fill=GRAY)

y = 340
label(y, "3. stored key, padded", "at compile time")
lanes(y, list("PUT") + ["0"] * 13, [BLUE] * 3 + [LIGHT] * 13, ["white"] * 3 + [GRAY] * 13)
svg.text(x0 + rowW / 2, y + 84, "= ?", size=26, fill=GRAY, anchor="middle")

y = 440
label(y, "4. compare, reduce", "vceqq_u8, vminvq_u8  ·  pcmpeqb, pmovmskb")
lanes(y, ["1"] * 16, [GREEN] * 16, ["white"] * 16)
svg.text(x0 + rowW + 12, y + 32, "all lanes equal", size=18, fill=GREEN, weight="bold")

svg.rect(20, 540, 1380, 70, PALE, rx=10)
svg.text(710, 585, "byte loop: ~40 instructions, up to 8 branches   →   5 instructions, 0 branches, every key, every length", size=22, anchor="middle")
svg.save("../phf_compare16.svg")
