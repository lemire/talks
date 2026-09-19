#!/usr/bin/env python3
"""A perfect hash for {GET, PUT, POST, DELETE}: slot = (len + asso[key[0]]) & 7, then one compare."""
from svgkit import *

W, H = 1300, 620
svg = SVG(W, H)
asso = {"G": 0, "P": 1, "D": 0}
keys = ["GET", "PUT", "POST", "DELETE"]
KCOL = {"GET": BLUE, "PUT": AQUA, "POST": VIOLET, "DELETE": MAGENTA}

# formula
svg.rect(40, 30, 1220, 62, PALE, rx=10)
svg.text(650, 72, "slot = (len + asso[key[0]]) & 7", size=30, fill=INK, anchor="middle", mono=True, weight="bold")

# left: the keys
x, y = 40, 140
svg.text(x, y, "keys, known at compile time", size=24, weight="bold")
hdr = ["key", "len", "key[0]", "asso", "slot"]
cols = [x, x + 190, x + 280, x + 380, x + 470]
for c, h in zip(cols, hdr):
    svg.text(c, y + 40, h, size=20, fill=GRAY)
for i, k in enumerate(keys):
    yy = y + 90 + i * 52
    svg.cell(cols[0], yy - 32, 150, 44, k, KCOL[k], size=22)
    svg.text(cols[1] + 10, yy, str(len(k)), size=24, mono=True)
    svg.text(cols[2] + 20, yy, k[0], size=24, mono=True)
    svg.text(cols[3] + 16, yy, str(asso[k[0]]), size=24, mono=True)
    svg.text(cols[4] + 12, yy, str((len(k) + asso[k[0]]) & 7), size=24, mono=True, weight="bold")
svg.text(x, y + 330, "asso: G → 0, P → 1, D → 0", size=22, fill=GRAY, mono=True)
svg.text(x, y + 364, "found by a bounded greedy search", size=20, fill=GRAY)
svg.text(x, y + 392, "at compile time (constexpr)", size=20, fill=GRAY)

# right: the 8 slots
sx, sy = 700, 180
sw, sh = 66, 66
svg.text(sx, sy - 30, "8 slots, one candidate each", size=24, weight="bold")
slot_of = {(len(k) + asso[k[0]]) & 7: k for k in keys}
for s in range(8):
    k = slot_of.get(s)
    svg.cell(sx + s * (sw + 6), sy, sw, sh, k if k else "", KCOL[k] if k else LIGHT, size=15)
    svg.text(sx + s * (sw + 6) + sw / 2, sy + sh + 24, str(s), size=18, fill=GRAY, anchor="middle")

# lookups
def lookup(yy, q, ok, xoff, level):
    s = (len(q) + asso[q[0]]) & 7
    col = AQUA if ok else ORANGE
    svg.cell(sx, yy, 130, 48, q, INK, size=22)
    svg.text(sx + 148, yy + 32, f"→ {len(q)} + {asso[q[0]]} = slot {s}", size=22, mono=True)
    tx = sx + s * (sw + 6) + sw / 2
    svg.path(f"M{sx+xoff},{yy} V{sy + sh + level} H{tx} V{sy + sh + 34}", stroke=col, sw=2.5, arrow=True, dash="6,5")
    cand = slot_of[s]
    verdict = f'"{q}" == "{cand}"?  ' + ("yes: return the value" if ok else "no: not in the set")
    svg.text(sx + 148, yy + 70, verdict, size=20, fill=(GREEN if ok else ORANGE))

lookup(sy + 150, "PUT", True, 100, 44)
lookup(sy + 270, "PATCH", False, 30, 62)
svg.text(sx, sy + 400, "one hash, one comparison, no probing, no chain", size=22, fill=INK, weight="bold")
svg.save("../phf_slots.svg")
