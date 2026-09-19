#!/usr/bin/env python3
"""Where a simdutf routine ends up: library -> engines -> products, with measured speed-ups."""
from svgkit import *

def fanout(path, root, root_sub, engines, foot):
    k = len(engines)
    W, H = 1300, 150 + k * 120
    svg = SVG(W, H)
    # root
    rx, ry, rw, rh = 40, (H - 60) / 2 - 75, 300, 150
    svg.rect(rx, ry, rw, rh, BLUE, rx=16)
    svg.text(rx + rw / 2, ry + 62, root, size=34, fill="white", anchor="middle", weight="bold")
    svg.text(rx + rw / 2, ry + 100, root_sub, size=20, fill="white", anchor="middle")
    # engines
    eh = 96
    total = k * eh + (k - 1) * 24
    ey0 = (H - 60 - total) / 2
    ex, ew = 480, 300
    for i, (name, sub, color, products) in enumerate(engines):
        ey = ey0 + i * (eh + 24)
        svg.path(f"M{rx+rw},{ry+rh/2} C{rx+rw+70},{ry+rh/2} {ex-70},{ey+eh/2} {ex-6},{ey+eh/2}", stroke=GRAY, sw=3, arrow=True)
        svg.rect(ex, ey, ew, eh, PALE, rx=12, stroke=color, sw=4)
        svg.text(ex + ew / 2, ey + 42, name, size=26, anchor="middle", weight="bold", fill=color)
        svg.text(ex + ew / 2, ey + 72, sub, size=18, anchor="middle", fill=GRAY)
        px = ex + ew + 60
        svg.line(ex + ew, ey + eh / 2, px - 8, ey + eh / 2, stroke=GRAY, sw=3, arrow=True)
        svg.text(px, ey + eh / 2 + 9, products, size=22, fill=INK)
    svg.text(W / 2, H - 20, foot, size=20, fill=GRAY, anchor="middle")
    svg.save(path)

fanout("../utf16fix_deploy.svg", "simdutf", "to_well_formed_utf16",
       [("V8", "JavaScript engine", BLUE, "Chrome, Edge, Brave, Opera, Electron, Deno"),
        ("Node.js 25", "String.prototype.toWellFormed", GREEN, "5× faster than Node.js 24")],
       "one C++ function, every V8 embedder, every well-formedness check on a JavaScript string")

fanout("../base64_deploy.svg", "simdutf", "base64_to_binary_safe",
       [("V8", "JavaScript engine", BLUE, "Chrome, Edge, Brave, Opera, Deno"),
        ("WebKit", "JavaScriptCore", VIOLET, "Safari, Bun"),
        ("Node.js 25", "Buffer.from(s, 'base64')", GREEN, "Uint8Array.fromBase64: 4.7–6× faster")],
       "Uint8Array.fromBase64 / toBase64 landed in ES2026; the decoder underneath is this one")
