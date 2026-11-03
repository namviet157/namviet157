"""Self-contained, font-embedded SVG primitives for GitHub's image sandbox."""
import base64
from collections import defaultdict
from functools import lru_cache
from html import escape
from io import BytesIO
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent
THEMES = {
    "light": dict(paper="#F7F5EE", surface="#FFFFFF", ink="#161616", muted="rgba(22,22,22,0.62)",
                  subtle="rgba(22,22,22,0.45)", accent="#FACC00", accent_ink="#161616", bar="#FDF7C4",
                  grid="rgba(22,22,22,0.07)", glow="#FFFFFF", band="#E3E1DB", signal="#E4572E"),
    "dark": dict(paper="#1A1B26", surface="#16161E", ink="#C0CAF5", muted="#A9B1D6",
                 subtle="#949EC8", accent="#E0AF68", accent_ink="#1A1B26", bar="#24283B",
                 grid="rgba(192,202,245,0.07)", glow="#C0CAF5", band="#292B39", signal="#E0AF68"),
}


@lru_cache(maxsize=None)
def font_data(mono, weight):
    path = ROOT / "fonts" / ("SpaceMono-Regular.ttf" if mono else "SpaceGrotesk.ttf")
    font = TTFont(path)
    if not mono:
        font = instantiateVariableFont(font, {"wght": weight})
    stream = BytesIO()
    font.save(stream)
    return stream.getvalue()


@lru_cache(maxsize=None)
def metrics(mono, weight):
    font = TTFont(BytesIO(font_data(mono, weight)))
    return font.getBestCmap(), font["hmtx"].metrics, font["head"].unitsPerEm


def width(text, size=14, weight=400, mono=False):
    cmap, advances, upm = metrics(mono, weight)
    return sum(advances[cmap.get(ord(ch), ".notdef")][0] for ch in text) * size / upm


def embedded_face(mono, weight, chars):
    font = TTFont(BytesIO(font_data(mono, weight)))
    options = subset.Options()
    options.name_IDs = []
    cutter = subset.Subsetter(options)
    cutter.populate(text="".join(sorted(chars)))
    cutter.subset(font)
    font.flavor = "woff"
    stream = BytesIO()
    font.save(stream)
    encoded = base64.b64encode(stream.getvalue()).decode()
    return f"@font-face{{font-family:{'Mono' if mono else 'Grotesk'};font-weight:{weight};src:url(data:font/woff;base64,{encoded}) format('woff')}}"


class Svg:
    def __init__(self, theme, height, title, w=840):
        self.theme, self.t, self.h, self.w, self.title = theme, THEMES[theme], height, w, title
        self.parts, self.css, self.defs, self.used = [], [], [], defaultdict(set)

    def add(self, value):
        self.parts.append(value)

    def group(self, content, attrs=""):
        self.add(f"<g {attrs}>{content}</g>")

    def text(self, x, y, value, size=14, weight=400, color="ink", mono=False, attrs=""):
        self.used[(mono, weight)] |= set(value)
        return f'<text x="{x}" y="{y}" font-family="{"Mono" if mono else "Grotesk"}" font-size="{size}" font-weight="{weight}" fill="{self.t.get(color, color)}" xml:space="preserve" {attrs}>{escape(value)}</text>'

    def rect(self, x, y, w, h, fill="surface", r=14, shadow=False):
        ink = self.t["ink"]
        base = f'<rect x="{x+6}" y="{y+6}" width="{w}" height="{h}" rx="{r}" fill="{ink}"/>' if shadow else ""
        return base + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{self.t.get(fill, fill)}" stroke="{ink}" stroke-width="2"/>'

    def line(self, x1, y1, x2, y2, color="subtle", stroke=1, attrs=""):
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{self.t[color]}" stroke-width="{stroke}" {attrs}/>'

    def paper(self):
        self.add(self.rect(2, 2, self.w-10, self.h-10, "paper", shadow=True))
        self.defs.append(f'<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0V40H0" fill="none" stroke="{self.t["grid"]}"/></pattern><radialGradient id="glow" cx=".5" cy="0" r=".9"><stop stop-color="{self.t["glow"]}" stop-opacity="{0.8 if self.theme == "light" else 0.05}"/><stop offset="1" stop-color="{self.t["glow"]}" stop-opacity="0"/></radialGradient>')
        for fill in ("grid", "glow"):
            self.add(f'<rect x="3" y="3" width="{self.w-12}" height="{self.h-12}" rx="13" fill="url(#{fill})"/>')

    def window(self, x, y, w, h, title):
        self.add(self.rect(x, y, w, h, shadow=True))
        self.add(f'<path d="M{x} {y+32}V{y+14}q0-14 14-14h{w-28}q14 0 14 14v18z" fill="{self.t["bar"]}" stroke="{self.t["ink"]}" stroke-width="2"/>')
        for i in range(3):
            self.add(f'<circle cx="{x+18+i*15}" cy="{y+16}" r="4" fill="none" stroke="{self.t["ink"]}" stroke-width="1.5"/>')
        self.add(self.text(x+70, y+21, title, 12, 500, "muted"))

    def type_line(self, x, y, value, size=12, delay=0, color="ink"):
        # Clip the complete line in monospace steps, preserving all text without motion.
        idx = len(self.css)
        total = width(value, size, mono=True) + 2
        self.defs.append(f'<clipPath id="typing{idx}"><rect class="typed{idx}" x="{x}" y="{y-size-2}" width="{total}" height="{size+8}"/></clipPath>')
        self.css.append(f'@keyframes type{idx}{{from{{width:0}}to{{width:{total}px}}}} .typed{idx}{{animation:type{idx} {len(value)/24:.3f}s steps({len(value)},end) {delay}s both}}')
        self.add(self.text(x, y, value, size, mono=True, color=color, attrs=f'clip-path="url(#typing{idx})"'))

    def icon(self, x, y, filename, size=18):
        path = ROOT / "logos" / filename
        mime = "image/png" if path.suffix == ".png" else "image/svg+xml"
        uri = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()
        recolor = ""
        if self.theme == "dark" and filename in {"openai.png", "onnx-runtime.png", "amazonwebservices-original-wordmark.svg"}:
            if not any('id="icon-ink"' in item for item in self.defs):
                self.defs.append('<filter id="icon-ink"><feColorMatrix type="matrix" values="0 0 0 0 .753 0 0 0 0 .792 0 0 0 0 .961 0 0 0 1 0"/></filter>')
            recolor = ' filter="url(#icon-ink)"'
        self.add(f'<image x="{x}" y="{y}" width="{size}" height="{size}" href="{uri}"{recolor}/>')

    def render(self):
        fonts = "".join(embedded_face(mono, weight, chars) for (mono, weight), chars in self.used.items())
        # Every animation has a visible, complete reduced-motion state.
        reduced = '@media(prefers-reduced-motion:reduce){*{animation:none!important}.hidden-motion{display:none!important}.still{display:inline!important}}'
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="title"><title id="title">{escape(self.title)}</title><defs>{"".join(self.defs)}</defs><style>{fonts}{"".join(self.css)}{reduced}</style>{"".join(self.parts)}</svg>\n'
