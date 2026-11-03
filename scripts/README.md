# Profile artwork

The palette, Space Grotesk / Space Mono pairing, paper grid, hard shadows, and
ASCII-cat motif reference [Aahil Khan's profile](https://github.com/aahil-khan/aahil-khan).
The artwork and project animations are personalized for Bui Nam Viet.

```sh
python -m pip install -r scripts/requirements.txt
python scripts/render_profile.py
```

Commit the generated `assets/*.svg` alongside renderer changes. GitHub selects
the light or dark variants through the README's `<picture>` elements.

Each SVG embeds its font subsets and technology logos as data URIs: rendering
requires no remote font or icon requests. CSS handles the title entrance,
typewriter text, workflow illustrations, equalizer, and cats. Every animation
stops under `prefers-reduced-motion`, with the content still visible. Explicit
`*-still.svg` variants are selected by the README's outer `<picture>` element
because browsers do not consistently forward motion preferences into SVG images.

Fonts are bundled under their SIL Open Font License; see `fonts/*-OFL.txt`.
Technology logos are brand identifiers sourced from the portfolio's logo assets
and [Devicon](https://github.com/devicons/devicon). Their respective brand owners
retain their trademarks.
