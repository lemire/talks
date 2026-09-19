#!/usr/bin/env python3
"""Whitespace-tolerant Base64 decoding, 64 bytes at a time (simdutf; ES2026 Uint8Array.fromBase64)."""
from svgkit import *

W, H = 1400, 720
lane, gap, x0 = 44, 4, 300
svg = SVG(W, H)
chars = list("SGVsbG8s\nIFdvcmxk")   # "Hello, World" with a line feed in the middle
n = len(chars)
rowW = n * (lane + gap) - gap
def show(c): return "\\n" if c == "\n" else c

def label(y, title, code):
    svg.text(20, y + 18, title, size=24, weight="bold")
    svg.text(20, y + 46, code, size=18, fill=BLUE, mono=True)
def lanes(y, vals, fills, tcols, size=20, h=48):
    for i, (v, f, t) in enumerate(zip(vals, fills, tcols)):
        svg.cell(x0 + i * (lane + gap), y, lane, h, v, f, tcolor=t, size=size)

y = 40
label(y, "64-byte block", "load(in + p)")
lanes(y, [show(c) for c in chars], [ORANGE if c == "\n" else BLUE for c in chars], ["white"] * n)
svg.text(x0 + rowW + 12, y + 30, "… 64 lanes", size=18, fill=GRAY)

y = 130
m = [1 if c == "\n" else 0 for c in chars]
label(y, "m = not alphabet", "two nibble lookups, cmp")
lanes(y, [str(b) for b in m], [ORANGE if b else PALE for b in m], ["white" if b else GRAY for b in m], h=44)
svg.text(x0 + rowW + 12, y + 20, "m == 0 and stack empty:", size=18, fill=GREEN, weight="bold")
svg.text(x0 + rowW + 12, y + 42, "decode 64 → 48 bytes, done", size=18, fill=GREEN, weight="bold")

y = 215
w = [1 if c in " \t\n\r\f" else 0 for c in chars]
label(y, "w = whitespace", "only computed when m != 0")
lanes(y, [str(b) for b in w], [YELLOW if b else PALE for b in w], ["white" if b else GRAY for b in w], h=44)
svg.text(x0 + rowW + 12, y + 20, "m & ~w != 0:", size=18, fill=ORANGE, weight="bold")
svg.text(x0 + rowW + 12, y + 42, "invalid byte, report offset", size=18, fill=ORANGE, weight="bold")

y = 300
label(y, "compact", "vpcompressb(block, ~m)")
kept = [c for c in chars if c != "\n"]
lanes(y, [show(c) for c in kept] + [""], [BLUE] * len(kept) + [LIGHT], ["white"] * len(kept) + [GRAY])
svg.text(x0 + rowW + 12, y + 30, "63 chars, one instruction", size=18, fill=GRAY)

# stack buffer
y = 400
label(y, "stack buffer", "append; decode when ≥ 64")
sx = x0
segs = [("older chars", 5, AQUA), ("this block: 63", 6, BLUE), ("", 5, LIGHT)]
x = sx
for name, k, col in segs:
    wdt = k * (lane + gap) - gap
    svg.rect(x, y, wdt, 48, col, rx=6, stroke="white")
    if name: svg.text(x + wdt / 2, y + 31, name, size=18, fill="white", anchor="middle", weight="bold")
    x += wdt + gap
svg.line(sx + 8 * (lane + gap) - gap / 2, y - 8, sx + 8 * (lane + gap) - gap / 2, y + 56, stroke=INK, sw=3, dash="5,4")
svg.text(sx + 8 * (lane + gap), y + 74, "64: decode this much straight to the output, slide the rest to the front", size=18, fill=GRAY)
svg.text(x0 + rowW + 12, y + 30, "384–640 bytes", size=18, fill=GRAY)

# summary boxes
y = 520
bw = 420
for i, (title, body, col) in enumerate([
    ("clean input", "no whitespace: every block takes the fast path;\nthe stack buffer is never touched", GREEN),
    ("MIME / DNS / JSON", "a line break every 76 chars: one compaction\nper block, still SIMD throughput", BLUE),
    ("garbage", "first byte that is neither alphabet nor\nwhitespace → error with its offset", ORANGE)]):
    x = 20 + i * (bw + 30)
    svg.rect(x, y, bw, 150, PALE, rx=12, stroke=col, sw=3)
    svg.text(x + 18, y + 38, title, size=22, weight="bold", fill=col)
    for j, ln in enumerate(body.split("\n")):
        svg.text(x + 18, y + 76 + j * 30, ln, size=19, fill=INK)
svg.save("../base64_blocks.svg")
