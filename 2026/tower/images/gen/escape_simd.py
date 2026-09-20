#!/usr/bin/env python3
"""JSON string escaping: scalar loop (one byte at a time, 3 compares + 1 branch each) vs SIMD
(load 32 bytes, three vector compares, OR, one branch on the mask; mask == 0 is the fast path)."""
from svgkit import *

W, H = 1400, 640
n = 32
lane, gap, x0 = 28, 3, 330
rowW = n * (lane + gap) - gap
svg = SVG(W, H)
text = list("Almost no string needs escaping!")
assert len(text) == n

def label(y, title, code=None, color=BLUE):
    svg.text(20, y + 18, title, size=22, weight="bold")
    if code: svg.text(20, y + 44, code, size=17, fill=color, mono=True)
def lanes(y, vals, fills, tcols, size=19, h=42):
    for i, (v, f, t) in enumerate(zip(vals, fills, tcols)):
        svg.cell(x0 + i * (lane + gap), y, lane, h, v, f, tcolor=t, size=size)
def band(y, h, title, color, w=150):
    svg.rect(10, y, W - 20, h, "none", rx=12, stroke=color, sw=3)
    svg.rect(10, y, w, 34, color, rx=10)
    svg.text(10 + w / 2, y + 24, title, size=19, fill="white", anchor="middle", weight="bold")

# ---------- input string
y = 22
label(y, "32 bytes of a string")
lanes(y, text, [LIGHT] * n, [INK] * n, h=46)

# ---------- scalar band
by = 92
band(by, 150, "1 byte at a time", GRAY, w=190)
y = by + 48
svg.text(20, y + 14, "for (char c : str)", size=16, fill=GRAY, mono=True)
svg.text(20, y + 36, "  if (c == '\"' || c == '\\\\'", size=16, fill=GRAY, mono=True)
svg.text(20, y + 58, "      || c < 0x20) ...", size=16, fill=GRAY, mono=True)
# one step per byte, chained by arrows: the loop cannot start byte i+1 before the branch on byte i resolves
r = 12
cy = y + 22
for i in range(n):
    cx = x0 + i * (lane + gap) + lane / 2
    svg.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PALE}" stroke="{GRAY}" stroke-width="2"/>')
    svg.text(cx, cy + 5, str(i + 1), size=12, fill=GRAY, anchor="middle", weight="bold")
    if i + 1 < n:
        svg.line(cx + r, cy, cx + lane + gap - r, cy, stroke=GRAY, sw=2, arrow=True)
svg.text(x0, cy + 52, "32 iterations, each: 3 compares + 1 data-dependent branch. The loop waits for each branch before the next byte.",
         size=17, fill=GRAY)

# ---------- SIMD band
by = 262
band(by, 362, "32 bytes at once", BLUE, w=190)
rows = [('== \'"\'', '"', ORANGE), ("== '\\\\'", "\\", VIOLET), ("< 0x20", "0x20", AQUA)]
masks = []
y = by + 48
for j, (code, const, color) in enumerate(rows):
    label(y, f"{j + 1}. " + ("control characters" if j == 2 else f"quote  '{const}'" if j == 0 else "backslash  '\\'"), "vector " + code, color=color)
    m = [1 if (c == '"' if j == 0 else c == "\\" if j == 1 else ord(c) < 0x20) else 0 for c in text]
    masks.append(m)
    lanes(y, [str(b) for b in m], [color if b else PALE for b in m],
          ["white" if b else GRAY for b in m], h=38)
    svg.text(x0 + rowW + 12, y + 25, "mask", size=17, fill=color, weight="bold")
    y += 56
# OR
y += 4
label(y, "4. OR the three masks", "needs_escape = m1 | m2 | m3")
m = [a | b | c for a, b, c in zip(*masks)]
lanes(y, [str(b) for b in m], [BLUE if b else PALE for b in m], ["white" if b else GRAY for b in m], h=38)
svg.text(x0 + rowW + 12, y + 25, "= 0", size=17, fill=BLUE, weight="bold")
# verdict
y += 66
svg.rect(x0, y, rowW, 60, BLUE, rx=10)
svg.text(x0 + 16, y + 26, "5. one branch:  mask == 0  →  copy the 32 bytes verbatim (the fast path)", size=20, fill="white", weight="bold")
svg.text(x0 + 16, y + 50, "mask ≠ 0 (rare)  →  the first set bit points at the byte to escape", size=17, fill="white")
svg.text(20, y + 40, "3 compares + 1 branch", size=17, fill=BLUE, mono=True)
svg.text(20, y + 62, "per 32 bytes", size=17, fill=BLUE, mono=True)
svg.save("../escape_simd.svg")
