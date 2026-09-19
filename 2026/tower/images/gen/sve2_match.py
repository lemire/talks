#!/usr/bin/env python3
"""Structural-character classifier in simdjson: NEON (4 instructions) vs SVE2 MATCH (1 instruction),
plus the predicate-to-mask trick. From lemire.me, "Faster JSON parsing with SVE2 on ARM processors" (2026)."""
from svgkit import *

W, H = 1400, 640
lane, gap, x0 = 52, 4, 330
svg = SVG(W, H)
text = list('{"id":[7,{"k":2}]}'[:16])
n = 16
rowW = n * (lane + gap) - gap
STRUCT = set(',:[]{}')
op_table = [0xff, 0, ord(','), ord(':'), 0, ord('['), ord(']'), ord('{'), ord('}'), 0, 0, 0, 0, 0, 0, 0]

def label(y, title, code, note=None):
    svg.text(20, y + 18, title, size=24, weight="bold")
    svg.text(20, y + 46, code, size=18, fill=BLUE, mono=True)
def lanes(y, vals, fills, tcols, size=20, h=46):
    for i, (v, f, t) in enumerate(zip(vals, fills, tcols)):
        svg.cell(x0 + i * (lane + gap), y, lane, h, v, f, tcolor=t, size=size)
def band(y, h, title, color):
    svg.rect(10, y, W - 20, h, "none", rx=12, stroke=color, sw=3)
    svg.rect(10, y, 150, 34, color, rx=10)
    svg.text(85, y + 24, title, size=19, fill="white", anchor="middle", weight="bold")

# ---------- input
y = 30
label(y, "16 input bytes", "d0")
lanes(y, text, [ORANGE if c in STRUCT else LIGHT for c in text], ["white" if c in STRUCT else INK for c in text])

# ---------- NEON band
by = 100
band(by, 240, "NEON", GRAY)
y = by + 44
nib = [((ord(c) + 3) >> 4) & 0xF for c in text]
label(y, "1–2. add 3, high nibble", "vshrq_n_u8(vaddq_u8(d0,3),4)")
lanes(y, [f"{v:X}" for v in nib], [PALE] * n, [INK] * n, h=42)
y = by + 108
look = [op_table[v] for v in nib]
label(y, "3. table lookup", "vqtbl1q_u8(op_table, nibble)")
lanes(y, [chr(v) if 0x20 < v < 0x7f else ("ff" if v == 0xff else "0") for v in look],
      [ORANGE if look[i] == ord(text[i]) else PALE for i, v in enumerate(look)], ["white" if look[i] == ord(text[i]) else GRAY for i, v in enumerate(look)], h=42)
y = by + 172
eq = [1 if look[i] == ord(text[i]) else 0 for i in range(n)]
label(y, "4. compare with input", "vceqq_u8(lookup, d0)")
lanes(y, ["ff" if b else "00" for b in eq], [ORANGE if b else PALE for b in eq], ["white" if b else GRAY for b in eq], h=42)

# ---------- SVE2 band
by = 360
band(by, 110, "SVE2", BLUE)
y = by + 44
label(y, "1. match against a set", "svmatch_u8(pg, d0, operators)")
lanes(y, [str(b) for b in eq], [BLUE if b else PALE for b in eq], ["white" if b else GRAY for b in eq], h=42)
svg.text(x0 + rowW + 12, y + 28, "predicate", size=18, fill=BLUE, weight="bold")

# ---------- predicate to 64-bit mask
by = 490
band(by, 140, "→ mask", AQUA)
y = by + 44
label(y, "predicate → bytes", "svsel_u8(p, weights, 0)")
wts = [1 << (i % 8) for i in range(n)]
lanes(y, [f"{w:02X}" if eq[i] else "00" for i, w in enumerate(wts)], [AQUA if eq[i] else PALE for i in range(n)], ["white" if eq[i] else GRAY for i in range(n)], h=42)
y = by + 98
m = sum(1 << i for i in range(n) if eq[i])
svg.text(20, y + 18, "3 × vpaddq_u8 over four blocks → 64-bit mask", size=19, fill=BLUE, mono=True)
svg.text(x0 + rowW, y + 18, f"= 0x{m:04X}… : bit i set ⇔ byte i is structural", size=19, fill=INK, anchor="end", mono=True)
svg.save("../sve2_match.svg")
