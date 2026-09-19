"""Tiny SVG helper shared by the talk's hand-drawn diagrams (images/gen/*.py).

Palette matches the matplotlib charts in ../../plots so that every figure in the
deck reads as one system."""

BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7"
GRAY, INK, LIGHT, PALE = "#8a8985", "#0b0b0b", "#e6e6e3", "#f3f3f1"
MONO = "Menlo, Consolas, monospace"
SANS = "Helvetica, Arial, sans-serif"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{SANS}">',
                      '<defs><pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                      f'<rect width="7" height="7" fill="{LIGHT}"/><line x1="0" y1="0" x2="0" y2="7" stroke="{GRAY}" stroke-width="2"/></pattern>'
                      f'<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
                      f'<path d="M0,0 L10,5 L0,10 z" fill="{GRAY}"/></marker>'
                      '</defs>']

    def text(self, x, y, s, size=22, fill=INK, anchor="start", weight=None, mono=False, italic=False, extra="", raw=False):
        if not raw:
            s = esc(s).replace("&amp;amp;", "&amp;").replace("&amp;lt;", "&lt;").replace("&amp;gt;", "&gt;")
        attrs = f'x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"'
        if weight: attrs += f' font-weight="{weight}"'
        if mono: attrs += f' font-family="{MONO}"'
        if italic: attrs += ' font-style="italic"'
        self.parts.append(f'<text {attrs} {extra}>{s}</text>')

    def rect(self, x, y, w, h, fill, rx=6, stroke=None, sw=1.5, extra=""):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st} {extra}/>')

    def cell(self, x, y, w, h, label, fill, tcolor="white", size=22, mono=True, rx=6, weight="bold", stroke="white"):
        self.rect(x, y, w, h, fill, rx=rx, stroke=stroke)
        if label != "":
            self.text(x + w / 2, y + h / 2 + size * 0.36, esc(label), size=size, fill=tcolor, anchor="middle", weight=weight, mono=mono)

    def line(self, x1, y1, x2, y2, stroke=GRAY, sw=2, dash=None, arrow=False):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        a = ' marker-end="url(#arrow)"' if arrow else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}{a}/>')

    def path(self, d, stroke=GRAY, sw=2, fill="none", arrow=False, dash=None):
        a = ' marker-end="url(#arrow)"' if arrow else ''
        dd = f' stroke-dasharray="{dash}"' if dash else ''
        self.parts.append(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}"{a}{dd}/>')

    def bracket(self, x1, x2, y, label, color, size=20, up=True):
        s = -1 if up else 1
        self.path(f"M{x1},{y} v{-10*s} h{x2-x1} v{10*s}", stroke=color, sw=3)
        self.text((x1 + x2) / 2, y - 18 if up else y + 32, esc(label), size=size, fill=color, anchor="middle", weight="bold")

    def raw(self, s):
        self.parts.append(s)

    def save(self, path):
        self.parts.append('</svg>')
        open(path, "w").write("\n".join(self.parts))
        print("wrote", path)
