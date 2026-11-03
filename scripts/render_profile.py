"""Render README artwork: pip install -r scripts/requirements.txt; python scripts/render_profile.py.

Palette, font choices, and ASCII-cat motif reference aahil-khan/aahil-khan.
Personalized artwork and animation for Bui Nam Viet; no runtime network requests.
"""
from pathlib import Path
from svg_tools import Svg, width

OUT = Path(__file__).resolve().parents[1] / 'assets'


def cat(c, x, y, walking=False):
    c.css += ['@keyframes blink{0%,31%,35%,73%,77%,100%{opacity:1}32%,34%,74%,76%{opacity:0}}',
              '@keyframes shut{0%,31%,35%,73%,77%,100%{opacity:0}32%,34%,74%,76%{opacity:1}}',
              '@keyframes tail{from{transform:rotate(-8deg)}to{transform:rotate(8deg)}}']
    parts = c.text(x, y, r' /\_/\ ', 15, mono=True)
    parts += c.text(x, y+17, '( o.o )', 15, mono=True, attrs='style="animation:blink 8s step-end infinite"')
    parts += c.text(x, y+17, '( -.- )', 15, mono=True, attrs='class="hidden-motion" style="opacity:0;animation:shut 8s step-end infinite"')
    parts += c.text(x, y+34, ' > ^ <', 15, mono=True)
    parts += c.text(x, y+51, '(\")_(\")', 15, mono=True)
    parts += f'<g style="transform-origin:{x+77}px {y+48}px;animation:tail 2.4s ease-in-out infinite alternate">'+c.text(x+73, y+51, '_/', 15, mono=True)+'</g>'
    if walking:
        c.css += ['@keyframes stroll{0%{transform:translateX(840px)}40%,53%{transform:translateX(360px)}94%,100%{transform:translateX(-110px)}}',
                  '@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}}',
                  '@media(prefers-reduced-motion:reduce){.walking-cat{transform:translateX(600px)}}']
        c.group('<g style="animation:bob .4s ease-in-out infinite">'+parts+'</g>', 'class="walking-cat" style="animation:stroll 20s linear infinite"')
    else:
        c.add(parts)


def hero(theme):
    c = Svg(theme, 414, 'Bui Nam Viet, Ho Chi Minh City, Vietnam. AI Engineer building RAG, retrieval, and efficient ML systems. A cat blinks above the now.txt window.')
    c.paper()
    c.add(c.text(40, 54, 'HO CHI MINH CITY, VIETNAM', 11, 500, 'muted', attrs='letter-spacing="1.5"'))
    c.add(c.line(248, 50, 460, 50))
    c.css += ['@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}',
              '@keyframes highlight{from{transform:scaleX(0)}to{transform:scaleX(1)}}']
    for i, (word, y) in enumerate([('BUI NAM', 150), ('VIET', 236)]):
        c.group(c.text(35, y, word, 88, 700, attrs='letter-spacing="-2.5"'), f'style="animation:rise .7s cubic-bezier(.16,1,.3,1) {i*.15}s both"')
    c.add(c.text(40, 293, 'AI Engineer building', 22))
    c.group(c.text(40, 324, 'RAG, retrieval, and efficient ML', 22, 700), 'style="animation:rise .6s ease-out .3s both"')
    c.add(f'<rect x="40" y="331" width="{width("RAG, retrieval, and efficient ML", 22, 700)}" height="5" rx="2" fill="{c.t["accent"]}" style="transform-box:fill-box;transform-origin:left;animation:highlight .65s ease-out 1s both"/>')
    c.add(c.text(40, 357, 'from data to useful systems.', 22))
    c.window(496, 133, 278, 240, 'now.txt')
    rows = [('focus', 185, ['NLP & Generative AI']), ('build', 212, ['RAG & vector search']),
            ('past', 239, ['AI intern @ TMA']), ('study', 266, ['VNU-HCM University', 'of Science']),
            ('GPA', 315, ['3.73 / 4.0']), ('grad', 342, ['July 2027'])]
    for i, (label, y, lines) in enumerate(rows):
        c.add(c.text(512, y, label, 12, 700, '#9A6700' if theme == 'light' else '#E0AF68'))
        for j, value in enumerate(lines):
            c.type_line(558, y+j*17, value, 11.5, .4+i*.12+j*.08)
    cat(c, 674, 72)
    return c


def buttons(theme):
    for name, label, primary in [('site', 'Portfolio', True), ('resume', 'Résumé PDF ↓', False), ('linkedin', 'LinkedIn ↗', False), ('email', 'Email ↗', False)]:
        text_w = width(label, 15, 500)
        w = round(text_w+50+(35 if primary else 0))
        c = Svg(theme, 56, label, w=w)
        c.add(c.rect(2, 4, w-12, 43, r=22, shadow=True))
        c.add(c.text(22, 31, label, 15, 500))
        if primary:
            x = w-35
            c.add(f'<circle cx="{x}" cy="25.5" r="14" fill="{c.t["accent"]}" stroke="{c.t["ink"]}" stroke-width="1.5"/>')
            c.css.append('@keyframes nudge{0%,65%,100%{transform:translateX(0)}80%{transform:translateX(3px)}}')
            c.group(c.text(x-7, 31, '→', 18, 700, 'accent_ink'), 'style="animation:nudge 2.5s ease-in-out infinite"')
        save(c, 'btn-'+name, theme)


def experience(theme):
    c = Svg(theme, 222, 'AI Engineer Intern, TMA Solutions — SignTalk. March–September 2026. 520 classes, 111,220 labeled samples; median CPU inference 0.42 ms/sample.')
    c.paper()
    c.add(c.text(32, 36, 'EXPERIENCE', 10.5, 500, 'muted', attrs='letter-spacing="1.5"'))
    c.add(c.text(32, 73, 'TMA Solutions — SignTalk', 28, 700))
    c.add(c.text(32, 99, 'AI Engineer Intern · March–September 2026', 13, color='muted'))
    c.add(c.text(32, 139, '520 classes · 111,220 labeled samples · PyTorch → ONNX', 16, 500))
    c.add(c.text(32, 168, '98.67% Top-1 on an independent English test set; 97.83% on Vietnamese samples.', 13, color='muted'))
    c.add(c.text(32, 195, 'Median CPU inference: 0.42 ms/sample, approximately 2.1× faster with ONNX Runtime.', 13, color='muted'))
    c.css.append('@keyframes status{0%,100%{opacity:1}50%{opacity:.35}}')
    c.add(f'<circle cx="792" cy="45" r="5" fill="{c.t["accent"]}" style="animation:status 3s ease-in-out infinite"/>')
    return c


PROJECTS = [
    ('scholarhub', 'ScholarHub', 'Research assistance over 15K+ arXiv papers', ['FASTAPI', 'BGE', 'PGVECTOR', 'OPENAI']),
    ('tourism', 'Tourism Together', 'Multilingual semantic travel search', ['FASTAPI', 'SENTENCE TRANSFORMERS', 'PGVECTOR']),
    ('hypernetworks', 'HyperNetworks', 'Weight generation and controlled benchmarks', ['TENSORFLOW', 'PYTORCH', 'KERAS']),
    ('music', 'Music Recommender', 'Lyric-based discovery across 57,650 songs', ['SBERT', 'FAISS', 'STREAMLIT']),
]


def project_rows(theme):
    c = Svg(theme, 94, 'Selected work: four AI systems and experiments worth opening.')
    c.add(c.text(4, 25, 'SELECTED WORK', 11, 500, 'muted', attrs='letter-spacing="1.5"'))
    c.add(c.text(4, 65, 'Four things worth opening', 30, 700))
    c.add(c.line(4, 91, 836, 91, 'ink', 2))
    save(c, 'work-head', theme)
    for i, (slug, name, tagline, tools) in enumerate(PROJECTS):
        c = Svg(theme, 136, f'{name}: {tagline}. Animated illustration of the project workflow.')
        c.add(c.text(4, 77, f'{i+1:02}', 54, 700, 'none', attrs=f'stroke="{c.t["ink"]}" stroke-width="1.3"'))
        c.add(c.text(103, 43, name, 27, 700))
        c.add(c.text(103, 72, tagline, 13.5, color='muted'))
        c.add(c.text(103, 102, '  ·  '.join(tools), 9.5, 500, 'subtle'))
        c.add(c.line(4, 132, 836, 132))
        c.css.append('@keyframes arrow{0%,70%,100%{transform:translate(0,0)}85%{transform:translate(3px,-3px)}}')
        c.group(c.text(814, 42, '↗', 23, 500), 'style="animation:arrow 3s ease-in-out infinite"')
        if slug == 'scholarhub':
            c.type_line(548, 37, '$ ask scholarhub', 11.5)
            c.type_line(548, 62, '15K+ papers -> [context]', 11.5, .7, 'muted')
            c.type_line(548, 87, 'answer + sources', 11.5, 1.6, 'signal')
            progress(c, 548, 106, 210)
        elif slug == 'tourism':
            c.type_line(548, 37, '? multilingual query', 11.5)
            c.type_line(548, 62, 'intent -> vector -> top-k', 11.5, .8, 'muted')
            c.type_line(548, 87, '2.8 s -> ~87 ms', 11.5, 1.6, 'signal')
            progress(c, 548, 106, 210)
        elif slug == 'hypernetworks':
            c.type_line(548, 37, '[hypernet] -> weights', 11.5)
            c.type_line(548, 62, '[target]   -> evaluate', 11.5, .9, 'muted')
            for j, h in enumerate([12, 18, 26, 20, 33, 39, 35, 45, 41, 47, 44, 50]):
                c.css.append(f'@keyframes bar{j}{{0%,100%{{transform:scaleY(.45)}}50%{{transform:scaleY(1)}}}}')
                c.add(f'<rect x="{552+j*16}" y="{121-h}" width="9" height="{h}" rx="2" fill="{c.t["accent"]}" style="transform-box:fill-box;transform-origin:bottom;animation:bar{j} {2+j*.08}s ease-in-out {j*.1}s infinite"/>')
        else:
            c.type_line(548, 35, '? find similar lyrics', 11.5)
            c.type_line(548, 59, '57,650 songs / 4 models', 11.5, .8, 'muted')
            for j in range(19):
                h = [14, 24, 36, 20, 29, 42, 18][j%7]
                c.css.append(f'@keyframes eq{j}{{0%,100%{{transform:scaleY(.25)}}50%{{transform:scaleY(1)}}}}')
                c.add(f'<rect x="{550+j*11}" y="{116-h}" width="5" height="{h}" rx="2" fill="{c.t["accent"]}" style="transform-box:fill-box;transform-origin:bottom;animation:eq{j} {1+j%4*.2}s ease-in-out {j*.09}s infinite"/>')
        save(c, 'work-'+slug, theme)


def progress(c, x, y, w):
    c.add(f'<rect x="{x}" y="{y}" width="{w}" height="5" rx="2" fill="{c.t["grid"]}"/>')
    c.css.append('@keyframes scan{0%{transform:translateX(0);opacity:0}15%,80%{opacity:1}100%{transform:translateX(155px);opacity:0}}')
    c.add(f'<rect x="{x}" y="{y}" width="50" height="5" rx="2" fill="{c.t["accent"]}" style="animation:scan 3s ease-in-out infinite"/>')


STACK = [
    ('Languages', [('Python','python-original.svg'),('C++','cplusplus-original.svg'),('TypeScript','Typescript.svg')]),
    ('Deep learning', [('PyTorch','PyTorch_logo_icon.svg'),('TensorFlow','TensorFlow_logo.svg'),('Keras','Keras_logo.svg'),('MediaPipe','mediapipe.svg')]),
    ('LLM & retrieval', [('OpenAI','openai.png'),('RAG',None),('BGE',None),('LangGraph',None),('Embeddings',None)]),
    ('Vector search', [('pgvector','postgresql-original.svg'),('FAISS',None),('Qdrant','qdrant.png')]),
    ('Backend & data', [('FastAPI','FastAPI.svg'),('PostgreSQL','postgresql-original.svg'),('MongoDB','MongoDB.svg'),('Polars',None)]),
    ('Delivery', [('ONNX','onnx-runtime.png'),('Docker','docker-original.svg'),('AWS','amazonwebservices-original-wordmark.svg'),('Actions','githubactions-original.svg')]),
]


def stack(theme):
    c = Svg(theme, 460, 'What I build with: Python, C++, TypeScript, PyTorch, TensorFlow, Keras, MediaPipe, LLMs, retrieval, vector search, backend, and deployment tools. A sleeping cat breathes beneath the tool badges.')
    c.paper()
    c.add(c.text(40, 44, 'TOOLBOX', 11, 500, 'muted', attrs='letter-spacing="1.5"'))
    c.add(c.text(40, 81, 'What I build with', 28, 700))
    c.css.append('@keyframes pop{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}')
    for row, (label, tools) in enumerate(STACK):
        y = 110+row*45
        c.add(c.text(40, y+20, label, 11, 500, 'muted'))
        x = 186
        for j, (name, logo) in enumerate(tools):
            w = width(name, 12.5, 500)+(47 if logo else 26)
            start = len(c.parts)
            c.add(c.rect(x, y, w, 30, r=8, shadow=True))
            if logo:
                c.icon(x+10, y+7, logo, 16)
            c.add(c.text(x+(34 if logo else 13), y+20, name, 12.5, 500))
            body = ''.join(c.parts[start:]); del c.parts[start:]
            c.group(body, f'style="animation:pop .5s ease-out {(row*4+j)*.035}s both"')
            x += w+12
        assert x < 818, (label, x)
    c.css.append('@keyframes breathe{0%,100%{transform:translateY(0)}50%{transform:translateY(-1.5px)}}')
    nap = [r'     |\      _,,,---,,_', r"     /,`.-'`'    -.  ;-;;,_", r"    |,4-  ) )-,_. ,\ (  `'-'", r"   '---''(_/--'  `-'\_)"]
    c.group(''.join(c.text(541, 383+i*14, line, 12, color='muted', mono=True) for i,line in enumerate(nap)), 'style="animation:breathe 3.6s ease-in-out infinite"')
    c.css.append('@keyframes zzz{0%{opacity:0;transform:translate(0,0)}30%{opacity:1}100%{opacity:0;transform:translate(10px,-22px)}}')
    for j in range(3):
        c.group(c.text(557+j*10, 380, 'z', 10+j*2, color='subtle', mono=True), f'class="hidden-motion" style="animation:zzz 3.6s linear {j*1.2}s infinite"')
    return c


def footer(theme):
    c = Svg(theme, 222, "Let's build something useful. Contact Bui Nam Viet: bnviet05@gmail.com. An ASCII cat trots across the footer.")
    c.add(c.rect(2, 2, 830, 212, 'band', shadow=True))
    c.add(c.text(40, 43, 'CONTACT', 11, 500, 'muted', attrs='letter-spacing="1.5"'))
    c.add(c.text(40, 88, "Let's build something useful.", 33, 700))
    c.add(c.text(40, 118, 'NLP, RAG, or an interesting ML problem — email is the fastest way to reach me.', 14, color='muted'))
    c.add(c.text(40, 146, 'bnviet05@gmail.com', 12, mono=True))
    c.add(c.line(40, 200, 792, 200, attrs='stroke-dasharray="2 7" stroke-linecap="round"'))
    c.defs.append('<clipPath id="cat-floor"><rect x="4" y="149" width="824" height="57"/></clipPath>')
    start = len(c.parts); cat(c, 0, 150, walking=True)
    body = ''.join(c.parts[start:]); del c.parts[start:]
    c.group('<g transform="translate(0,40) scale(1,.8)">'+body+'</g>', 'clip-path="url(#cat-floor)"')
    return c


def recognition(theme):
    c = Svg(theme, 94, 'Background & recognition: education, competition awards, scholarships, and certifications.')
    c.add(c.text(4, 25, 'BACKGROUND & RECOGNITION', 11, 500, 'muted', attrs='letter-spacing="1.5"'))
    c.add(c.text(4, 65, 'Learning, building, and competing', 30, 700))
    c.add(c.line(4, 91, 836, 91, 'ink', 2))
    save(c, 'recognition-head', theme)

    c = Svg(theme, 180, 'VNU-HCM University of Science. Bachelor of Information Technology, major in Data Science. GPA 3.73/4.0. Expected graduation July 2027.')
    c.paper()
    c.add(c.text(32, 36, 'EDUCATION', 10.5, 500, 'muted', attrs='letter-spacing="1.5"'))
    c.add(c.text(32, 74, 'VNU-HCM University of Science', 28, 700))
    c.add(c.text(32, 105, 'Bachelor of Information Technology · Major in Data Science', 15, color='muted'))
    for x, label in [(32, 'GPA 3.73 / 4.0'), (221, 'Graduating July 2027'), (468, 'Final-year student')]:
        w = width(label, 13, 700)+28
        c.add(c.rect(x, 125, w, 30, 'accent' if x == 32 else 'surface', r=8, shadow=True))
        c.add(c.text(x+14, 145, label, 13, 700, 'accent_ink' if x == 32 else 'ink'))
    save(c, 'education', theme)

    awards = [
        ('aib', 'Runner-up', 'AI in Business 3 · 2026', 'ZERO-STOP E-BORDER', 'LLMs · RAG · OCR · Computer vision'),
        ('attacker', 'Runner-up', 'ATTACKER 2026', 'BelieveLedger', 'Financial data for small merchants'),
        ('hackathon', 'Consolation Prize', 'HCMUTE Hackathon 2025', 'UniHub', 'Academic resources & AI study tools'),
        ('scholarship', '3 consecutive years', 'Academic Encouragement', 'Scholarship · 2023–2025', 'VNU-HCM University of Science'),
    ]
    for slug, badge, event, project, detail in awards:
        c = Svg(theme, 166, f'{badge}: {event}. {project}. {detail}.', w=410)
        c.add(c.rect(2, 2, 398, 154, shadow=True))
        badge_w = width(badge, 12, 700)+26
        c.add(c.rect(20, 17, badge_w, 27, 'accent', r=8))
        c.add(c.text(33, 36, badge, 12, 700, 'accent_ink'))
        # Draw a medal directly as vector art so no remote icon is required.
        c.add(f'<path d="M358 17l7 23 7-11 7 11 7-23" fill="{c.t["accent"]}" stroke="{c.t["ink"]}" stroke-width="1.5"/>')
        c.add(f'<circle cx="372" cy="43" r="10" fill="{c.t["accent"]}" stroke="{c.t["ink"]}" stroke-width="1.5"/>')
        c.add(c.text(20, 77, event, 20, 700))
        c.add(c.text(20, 105, project, 16, 500))
        c.add(c.text(20, 133, detail, 12, color='muted'))
        save(c, 'award-'+slug, theme)

    certificates = [
        ('ml', 'Machine Learning', 'Stanford University & DeepLearning.AI', '2026'),
        ('google', 'Google Data Analytics', 'Professional Certificate · Coursera', '2025'),
        ('sql', 'SQL (Advanced)', 'HackerRank Certified', '2025'),
        ('toeic', 'TOEIC 785', 'English communication proficiency', '2025'),
    ]
    for slug, name, issuer, year in certificates:
        c = Svg(theme, 106, f'{name}. {issuer}. {year}.', w=410)
        c.add(c.rect(2, 2, 398, 94, shadow=True))
        c.add(c.rect(19, 21, 27, 27, 'accent', r=8))
        c.add(f'<path d="M25 34l5 5 10-12" fill="none" stroke="{c.t["accent_ink"]}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
        c.add(c.text(59, 39, name, 19, 700))
        c.add(c.text(20, 75, issuer, 12, color='muted'))
        c.add(c.text(356, 75, year, 11, color='muted'))
        save(c, 'cert-'+slug, theme)


def typography(theme):
    c = Svg(theme, 88, 'I build AI systems from data preparation and model training to retrieval APIs and optimized inference. My focus is NLP, Generative AI, and efficient ML systems.')
    c.add(c.text(4, 21, 'I build AI systems from data preparation and model training', 16))
    c.add(c.text(4, 46, 'to retrieval APIs and optimized inference.', 16))
    c.add(c.text(4, 75, 'Focused on NLP, Generative AI, and efficient ML systems.', 16, 700))
    save(c, 'intro', theme)

    c = Svg(theme, 52, 'GitHub activity — expand or collapse the contribution graph.', w=220)
    c.add(c.rect(2, 2, 208, 40, r=14, shadow=True))
    c.add(c.text(18, 29, 'GitHub activity', 18, 700))
    c.add(f'<path d="M175 30v-6m8 6V18m8 12V13" fill="none" stroke="{c.t["accent"]}" stroke-width="3" stroke-linecap="round"/>')
    save(c, 'activity-label', theme)


def save(c, name, theme):
    svg = c.render()
    (OUT/f'{name}-{theme}.svg').write_text(svg, encoding='utf-8')
    # Browsers do not reliably forward reduced-motion preferences into SVG img
    # documents. Select explicit still variants from the outer picture element.
    still = svg.replace('</svg>', '<style>*{animation:none!important}.hidden-motion{display:none!important}.walking-cat{transform:translateX(600px)}</style></svg>')
    (OUT/f'{name}-{theme}-still.svg').write_text(still, encoding='utf-8')


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for theme in ('light', 'dark'):
        for name, fn in [('hero',hero),('experience',experience),('stack',stack),('footer',footer)]:
            save(fn(theme), name, theme)
        buttons(theme)
        project_rows(theme)
        recognition(theme)
        typography(theme)
    print(f'Rendered {len(list(OUT.glob("*.svg")))} theme and reduced-motion SVG assets.')
