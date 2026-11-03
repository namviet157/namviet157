"""Generate the profile's self-contained SVG panels: python scripts/render_profile.py.

Design inspiration: https://github.com/aahil-khan/aahil-khan
Original implementation and personalized content for namviet157.
"""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
THEMES = {
    "light": {"paper": "#f7f5ee", "surface": "#ffffff", "ink": "#20232c", "muted": "#535a66", "accent": "#f5cf48", "grid": "#e7e4dc"},
    "dark": {"paper": "#1a1b26", "surface": "#24283b", "ink": "#c0caf5", "muted": "#a9b1d6", "accent": "#e0af68", "grid": "#2b3044"},
}


class Panel:
    def __init__(self, theme, height, title):
        self.t = THEMES[theme]
        self.height, self.title, self.parts = height, title, []

    def rect(self, x, y, w, h, fill="surface", radius=12, shadow=False):
        if shadow:
            self.parts.append(f'<rect x="{x+5}" y="{y+5}" width="{w}" height="{h}" rx="{radius}" fill="{self.t["ink"]}"/>')
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{self.t.get(fill, fill)}" stroke="{self.t["ink"]}" stroke-width="1.5"/>')

    def text(self, x, y, value, size=16, weight=400, color="ink", mono=False):
        family = "Consolas,Menlo,monospace" if mono else "Verdana,DejaVu Sans,sans-serif"
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{self.t.get(color, color)}" xml:space="preserve">{escape(value)}</text>')

    def paper(self):
        self.rect(2, 2, 828, self.height-12, "paper", shadow=True)
        self.parts.append(f'<rect x="3" y="3" width="826" height="{self.height-14}" rx="12" fill="url(#grid)"/>')

    def cat(self, x, y):
        for i, row in enumerate([r" /\_/\ ", "( o.o )", " > ^ <"]):
            self.text(x, y+i*17, row, 16, mono=True)

    def save(self, name, theme):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="{self.height}" viewBox="0 0 840 {self.height}" role="img" aria-labelledby="title">
<title id="title">{escape(self.title)}</title>
<defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{self.t['grid']}" stroke-width="0.8"/></pattern></defs>
{''.join(self.parts)}</svg>'''
        (OUT / f"{name}-{theme}.svg").write_text(svg, encoding="utf-8")


def hero(theme):
    p = Panel(theme, 390, "Bui Nam Viet — AI Engineer, NLP & Generative AI. Ho Chi Minh City, Vietnam.")
    p.paper()
    p.text(36, 44, "Ho Chi Minh City, Vietnam", 13, color="muted")
    p.text(31, 121, "BUI NAM", 62, 700)
    p.text(31, 192, "VIET", 62, 700)
    p.rect(36, 218, 157, 30, "accent", 4)
    p.text(47, 239, "AI Engineer", 18, 700, "#20232c")
    p.text(36, 284, "NLP & Generative AI", 24, 700)
    p.text(36, 318, "From data and models", 19)
    p.text(36, 346, "to useful AI systems.", 19)
    p.cat(699, 70)
    p.rect(472, 125, 317, 220, shadow=True)
    p.text(491, 153, "o  o  o     now.txt", 13, color="muted", mono=True)
    for i, (label, value) in enumerate([
        ("focus", "RAG & semantic search"), ("build", "Efficient ML systems"),
        ("past", "AI intern @ TMA"), ("study", "Data Science @ HCMUS"),
        ("GPA", "3.73 / 4.0"), ("grad", "July 2027 (expected)")]):
        p.text(490, 185+i*26, f"{label:<6} {value}", 13, mono=True)
    p.save("hero", theme)


PROJECTS = [
    ("scholarhub", "ScholarHub", "Research assistance grounded in 15K+ arXiv papers.", "Parse, chunk, embed, retrieve — then answer with context.", "FastAPI / BGE / pgvector / OpenAI", "15K+", "research papers"),
    ("tourism", "Tourism Together", "Multilingual semantic search for travel discovery.", "Moved vector ranking into PostgreSQL with Supabase RPCs.", "Sentence Transformers / FastAPI / pgvector", "~87 ms", "retrieval latency"),
    ("hypernetworks", "HyperNetworks", "Static weight generation and controlled ML experiments.", "HyperConv2D, HyperLSTM-style sequences, and ablations.", "TensorFlow / Keras / PyTorch", "12 runs", "controlled benchmarks"),
    ("music", "Music Recommender", "Find similar lyrics across a catalog of 57,650 songs.", "Compare TF-IDF, FastText, Word2Vec, and SBERT retrieval.", "Sentence Transformers / FAISS / Streamlit", "57,650", "songs indexed"),
]


def projects(theme):
    p = Panel(theme, 90, "Selected work — RAG, retrieval, and model experiments")
    p.text(4, 29, "Selected work", 26, 700)
    p.text(4, 61, "RAG, retrieval, and model experiments", 15, color="muted")
    p.save("work-head", theme)
    for slug, name, line1, line2, stack, metric, label in PROJECTS:
        p = Panel(theme, 154, f"{name}. {line1} {line2} {metric} {label}.")
        p.rect(2, 2, 828, 140, shadow=True)
        p.rect(19, 20, 5, 108, "accent", 2)
        p.text(40, 37, name, 23, 700)
        p.text(40, 66, line1, 13, color="muted")
        p.text(40, 89, line2, 13, color="muted")
        p.text(40, 120, stack, 11, color="muted", mono=True)
        p.text(635, 66, metric, 26, 700)
        p.text(635, 91, label, 11, color="muted")
        p.save(f"work-{slug}", theme)


def experience(theme):
    p = Panel(theme, 228, "TMA Solutions — SignTalk. AI Engineer Intern, March–September 2026. 520 classes, 111,220 labeled samples, 0.42 ms median CPU inference.")
    p.paper()
    p.text(32, 40, "Experience / TMA Solutions — SignTalk", 23, 700)
    p.text(32, 70, "AI Engineer Intern · March–September 2026", 14, color="muted")
    p.text(32, 110, "Video → MediaPipe keypoints → PyTorch → ONNX Runtime", 16, 700)
    p.text(32, 143, "520 gesture classes across English and Vietnamese · 111,220 labeled samples", 14)
    p.text(32, 172, "98.67% Top-1 on an independent English test set; 97.83% on Vietnamese samples", 13)
    p.text(32, 199, "0.42 ms median CPU inference per sample · ~2.1× faster with ONNX Runtime", 13)
    p.save("experience", theme)


def stack(theme):
    p = Panel(theme, 316, "Toolbox: Python, C++, TypeScript, PyTorch, TensorFlow, RAG, vector search, FastAPI, ONNX Runtime, and Docker.")
    p.paper()
    p.text(32, 46, "What I build with", 27, 700)
    rows = [
        ("Languages", "Python · C++ · TypeScript"),
        ("Deep learning", "PyTorch · TensorFlow · Keras · MediaPipe"),
        ("LLMs & retrieval", "RAG · OpenAI · Sentence Transformers · BGE"),
        ("Vector search", "pgvector · FAISS · Qdrant · LangGraph"),
        ("Backend & data", "FastAPI · PostgreSQL · MongoDB · Polars"),
        ("Delivery", "ONNX Runtime · Docker · AWS · GitHub Actions"),
    ]
    for i, (label, values) in enumerate(rows):
        p.text(32, 91+i*36, label, 13, 700, "muted")
        p.text(204, 91+i*36, values, 14)
    p.save("stack", theme)


def footer(theme):
    p = Panel(theme, 138, "Have an AI problem to solve? Contact Bui Nam Viet at bnviet05@gmail.com.")
    p.paper()
    p.text(32, 47, "Have an AI problem to solve?", 27, 700)
    p.text(32, 82, "Let's build something useful together.", 15, color="muted")
    p.text(32, 109, "bnviet05@gmail.com", 14, mono=True)
    p.cat(727, 54)
    p.save("footer", theme)


def buttons(theme):
    for slug, label in [("site", "Portfolio"), ("resume", "Résumé PDF"), ("linkedin", "LinkedIn"), ("email", "Email")]:
        p = Panel(theme, 54, label)
        p.rect(2, 2, 143, 42, "accent" if slug == "site" else "surface", 18, True)
        p.text(18, 29, label, 15, 700, "#20232c" if slug == "site" else "ink")
        # Keep the button viewBox as wide as the visible pill.
        p.save(f"btn-{slug}", theme)
        path = OUT / f"btn-{slug}-{theme}.svg"
        path.write_text(path.read_text(encoding="utf-8").replace('width="840"', 'width="154"').replace('viewBox="0 0 840', 'viewBox="0 0 154'), encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for theme in THEMES:
        for render in (hero, buttons, experience, projects, stack, footer):
            render(theme)
    print(f"Generated {len(list(OUT.glob('*.svg')))} SVG assets.")
