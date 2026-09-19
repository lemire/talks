#!/usr/bin/env python3
"""The memory-page trick: a 16-byte load is safe if it does not cross a 4 KB page boundary."""
from svgkit import *

W, H = 1300, 640
svg = SVG(W, H)

# two pages side by side
px, py, pw, ph = 60, 110, 560, 170
svg.text(px, 40, "memory, in 4 KB pages", size=24, weight="bold")
svg.rect(px, py, pw, ph, PALE, rx=10, stroke=GRAY, sw=2)
svg.text(px + 16, py + 34, "page n (mapped)", size=20, fill=GRAY)
svg.rect(px + pw + 8, py, pw, ph, "url(#hatch)", rx=10, stroke=GRAY, sw=2)
svg.text(px + 2 * pw - 8, py + 34, "page n+1: maybe unmapped", size=20, fill=GRAY, anchor="end")
svg.text(px + pw + 4, py + ph + 30, "page boundary (addr & 4095 == 0)", size=18, fill=INK, anchor="middle")
svg.line(px + pw + 4, py - 10, px + pw + 4, py + ph + 6, stroke=INK, sw=3)

# key "PUT" at the end of page n, then a 16-byte load
cw = 34
kx = px + pw - 3 * cw - 8
ky = py + 84
for i, c in enumerate("PUT"):
    svg.cell(kx + i * cw, ky, cw - 3, 44, c, AQUA, size=20)
svg.text(kx - 12, ky + 30, "p →", size=20, anchor="end", mono=True)
# 16-byte window
wx = kx
ww = 16 * cw
svg.rect(wx, ky - 12, ww, 68, "none", rx=8, stroke=ORANGE, sw=4, extra='stroke-dasharray="8,6"')
svg.text(wx, py - 16, "16-byte load at p: 3 bytes here, 13 bytes in the next page", size=21, fill=ORANGE, weight="bold")
svg.text(px + 2 * pw + 8, py + ph + 30, "unmapped → SIGSEGV", size=20, fill=ORANGE, anchor="end", weight="bold")

# the rule
y = 330
svg.rect(60, y, 1180, 100, PALE, rx=12)
svg.text(650, y + 42, "a load that stays inside one page cannot fault", size=26, anchor="middle", weight="bold")
svg.text(650, y + 80, "the OS maps memory page by page; the protection unit is 4 KB, never a single byte", size=20, fill=GRAY, anchor="middle")

# the code
y = 470
svg.rect(60, y, 700, 150, "#1f1f1d", rx=12)
lines = [("if ((addr & 4095) <= 4096 - 16)  [[likely]]", "#e8e6df"),
         ("\u00a0\u00a0\u00a0\u00a0return load16(p);            // wide, branch-free", AQUA),
         ("copy len bytes to a 16-byte buffer;  // rare", ORANGE),
         ("return load16(buffer);", ORANGE)]
for i, (ln, col) in enumerate(lines):
    svg.text(80, y + 40 + i * 32, ln, size=20, fill=col, mono=True)
svg.text(800, y + 34, "one branch, taken 99.6% of the time", size=22, weight="bold")
svg.text(800, y + 66, "(15 of every 4096 addresses)", size=20, fill=GRAY)
svg.text(800, y + 104, "the predictor learns it instantly;", size=20, fill=GRAY)
svg.text(800, y + 132, "8 unpredictable branches → 1 predictable one", size=20, fill=GRAY)
svg.save("../page_trick.svg")
