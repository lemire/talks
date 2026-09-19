#!/usr/bin/env python3
"""From an AVX-512 kernel to Node.js: the deployment chain of the IP parsers."""
from svgkit import *

W, H = 1300, 560
svg = SVG(W, H)

def box(x, y, w, h, title, lines, color, tcolor=INK):
    svg.rect(x, y, w, h, PALE, rx=14, stroke=color, sw=4)
    svg.rect(x, y, w, 58, color, rx=14)
    svg.rect(x, y + 40, w, 18, color, rx=0)  # square off the bottom of the header
    svg.text(x + w / 2, y + 39, title, size=28, fill="white", anchor="middle", weight="bold")
    for i, ln in enumerate(lines):
        svg.text(x + w / 2, y + 96 + i * 32, esc(ln), size=21, fill=tcolor, anchor="middle")

y = 60
bw, bh = 340, 230
xs = [40, 480, 920]
box(xs[0], y, bw, bh, "AVX-512 kernels", ["IPv4 in a 16-byte register", "IPv6 in a 64-byte register", "~50 instructions", "one branch"], BLUE)
box(xs[1], y, bw, bh, "ada", ["WHATWG URL parser, C++", "github.com/ada-url/ada", "picks the kernel", "at compile time"], AQUA)
box(xs[2], y, bw, bh, "Node.js", ["new URL(s)", "URL.canParse(s)", "every http://host/", "on the runtime"], GREEN)
for a, b in [(xs[0] + bw, xs[1]), (xs[1] + bw, xs[2])]:
    svg.line(a + 10, y + bh / 2, b - 12, y + bh / 2, stroke=GRAY, sw=4, arrow=True)

# measured on the runtime
y2 = 350
svg.text(40, y2, "Measured in Node.js, Xeon Gold 6548N, 100 000 URLs per corpus, best of 5:", size=22, fill=INK)
rows = [("IPv4 hosts", "+8%", "+13%"), ("IPv6, random", "+8%", "+20%"), ("IPv6, traffic-like", "+2%", "+9%")]
cx = [40, 400, 700]
svg.text(cx[1], y2 + 44, "new URL(s)", size=22, fill=GRAY, mono=True)
svg.text(cx[2], y2 + 44, "URL.canParse(s)", size=22, fill=GRAY, mono=True)
for i, (name, a, b) in enumerate(rows):
    yy = y2 + 90 + i * 40
    svg.text(cx[0], yy, name, size=22)
    svg.text(cx[1], yy, a, size=24, fill=GREEN, weight="bold")
    svg.text(cx[2], yy, b, size=24, fill=GREEN, weight="bold")
svg.text(1000, y2 + 90, "2 300–3 200 instructions", size=20, fill=GRAY)
svg.text(1000, y2 + 118, "per new URL; the address", size=20, fill=GRAY)
svg.text(1000, y2 + 146, "parser was a few hundred", size=20, fill=GRAY)
svg.text(1000, y2 + 174, "of them", size=20, fill=GRAY)
svg.save("../ada_node.svg")
