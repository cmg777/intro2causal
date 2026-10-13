# Quarto reveal.js guide

How a deck is built and what every knob does. The deck is authored as a `.qmd` and rendered by the
**Quarto CLI** (`uv run quarto`, 1.8+) to a **standalone** reveal.js HTML deck
in `slides/chNN/`. Nothing serves or re-renders it downstream — the rendered `index.html` +
`slides_files/` are committed as-is. Read this in Phase 3.

---

## The files and the render

| File | Role | Per-run |
|---|---|---|
| `slides.qmd` | The deck source (`format: revealjs`). Front matter = engine config; body = the slides. | **Composed per chapter** from `slides.qmd.tmpl` + the archetypes. |
| `site-brand.scss` | The revealjs theme (book palette/fonts/archetype styling). **Dark mode:** the deck canvas is DeepSlate (`$body-bg: $canvas` / `#0f172a`, the book's dark background) with light text (`#e2e8f0`); fills use the CLAUDE.md mermaid palette (blue/purple/green/red/orange) and inline accents the book's dark-mode tokens (CausalBlue `#38bdf8`, MethodPurple `#a78bfa`, EvidenceGreen `#34d399`). | **Copied verbatim** from `templates/site-brand.scss`. |
| `title-slide.html` | A Quarto title-slide **partial** that paints the chapter's visual-summary image as the full-bleed title slide (no overlaid text). | **Copied verbatim** from `templates/title-slide.html`. |
| `figure-zoom.html` | A click-to-zoom lightbox (CSS + JS) injected via `include-after-body` — every figure **and the title visual summary** opens full-screen with zoom/pan controls. | **Copied verbatim** from `templates/figure-zoom.html`. |
| `figures/` | The chosen chapter figures + `visual_summary.webp` (the mind-map image), copied from `_figcache/`. | **Selected per chapter** from the export manifest. |

Render (from the `slides/chNN/` dir):

```bash
uv run quarto render slides.qmd
```

→ `index.html` + `slides_files/` (reveal.js + plugins + libs, ~8 MB). Figures are referenced locally
as `figures/<cache_file>.png`. The deck is a pure Pandoc render — **no kernel**, because code blocks
are illustrative (`{.python}`, not `{python}`), figures are pre-exported images, and `{mermaid}`
diagrams are rendered client-side by mermaid.js.

---

## Why NOT embed-resources (single file)

`embed-resources: true` would inline everything into one `index.html`, BUT **RevealChalkboard is
incompatible with self-contained output** (`quarto render` errors out). Because chalkboard is a core
feature, the deck ships **`index.html` + `slides_files/`** instead. (If a deck ever drops chalkboard,
`embed-resources: true` becomes available again.)

---

## Front-matter config (in `slides.qmd`)

The validated block lives in `templates/slides.qmd.tmpl`. Key options:

- `output-file: index.html` — render to `index.html` (not `slides.html`).
- `theme: [default, site-brand.scss]` — reveal base + the book's brand layer.
- `template-partials: [title-slide.html]` — the custom title slide (visual-summary image).
- `visual-summary:` (front-matter field) — path to the title slide's key visual, `figures/visual_summary.webp` (plus `visual-summary-bg:`, its edge colour)
  (the Recap slide repeats the same path as its `background-image`).
- `mermaid: theme: dark` — light edges/labels on the dark canvas for `{mermaid}` slides.
- `center: true` — **vertical-centers every slide** → centred dividers + strategic white space.
- `slide-number: c/t`, `progress: true`, `transition: fade`, `width: 1280`, `height: 720`.
- `fig-align: center` + `auto-stretch: true` — centre + bound figures (no overflow).
- `highlight-style: github` — code highlighting.

---

## Features (all on by default) and their keys

| Feature | Front matter | Key |
|---|---|---|
| reveal.js-menu plugin | `menu: true` | **M** |
| Chalkboard (draw on slides) | `chalkboard: true` | **B** (board), **C** (chalk) |
| Speaker view (notes window) | (notes plugin always on) | **S** |
| Overview (slide grid) | `overview: true` | **O** / **Esc** |
| Slide number | `slide-number: c/t` | — |
| Preview-links (open external links inline) | `preview-links: auto` | — |
| Fullscreen | (built in) | **F** |
| Help (all shortcuts) | (built in) | **?** |

---

## Authoring mechanics

- **Slides:** `##` = a content slide (its heading is the assertion title); `#` = a section divider.
  See `slide-archetypes.md`.
- **Math:** write **LaTeX, never literal Unicode** (`$R^2$` not `R²`, `$\hat\beta$` not `β̂`). Rendered
  by **MathJax** (Quarto revealjs's default — no `html-math-method`; reveal.js is local but math needs
  a network; why not KaTeX → `render-and-fix.md §7`). The chapter `.qmd` is already Pandoc, so copy
  equations straight across. The Unicode→LaTeX table + mixed-numbers + notes-stay-Unicode rules are
  the canonical `slide-mapping.md §Math symbols → LaTeX`.
- **Code:** ` ``` {.python code-line-numbers="2-3|5"} ` highlights (without executing) and reveals
  line-groups as fragments. Use `.python` (or `.r` / `.stata`). **Illustrative only — never `{python}`.**
- **Figures:** `![caption](figures/<cache_file>.png)` — `auto-stretch` bounds, `fig-align` centres.
  Every figure is **click-to-zoom**: clicking it opens a full-screen overlay with zoom in/out/reset,
  a fullscreen toggle, scroll-to-zoom, drag-to-pan, and Esc-to-close (from `figure-zoom.html`,
  injected via `include-after-body` — no markup per figure, works automatically).
- **Columns:** `:::: {.columns} ::: {.column width="50%"} … ::: ::::`.
- **Speaker notes:** `::: {.notes} … :::`.
- **Reveals:** `. . .` (pause), `::: {.incremental}` (list), `{.fragment}` (element).
- **Title slide:** the chapter **visual summary, full-bleed** — the partial paints `visual-summary:`
  as the slide `data-background-image` (`size=contain`, whole image, no crop) with no overlaid text.
  (With no `visual-summary:`, it falls back to a text title slide: title + subtitle + author +
  institute + date.)
- **Dividers / emphasis slides:** `{.divider background-color="#…"}` (white centred text). Use a
  **brand colour** for full-bleed emphasis so it stands out from the dark canvas — Act I question blue
  `#3498db`, Act II method purple `#8e44ad`, Act III result green `#2d8659`. Avoid near-black, which blends
  into the canvas. Dark brand fills still get `has-dark-background`; the theme keeps text light.

---

## The 4 layout requirements → how they're met

| Requirement | Mechanism |
|---|---|
| Title slide has a key visual | `title-slide.html` partial + `visual-summary:` → the chapter visual-summary image |
| Figures respect slide margins | Quarto **`auto-stretch`** (default) + `fig-align: center` + a `max-width:100%` SCSS guard — **no viewport units** |
| Section dividers centred (middle of slide) | `center: true` + `.divider` class on the `#` heading |
| Strategic white space; centred figures/tables/captions | `center: true` (block centred) + SCSS centres `figcaption` and makes `.comment` a centred **`display:block`**; lists stay left |
| A slide's concluding takeaway made prominent | `[…]{.takeaway .fragment}` → the result-green **accent card** (SCSS `.takeaway`), rising/fading in last — the prominent sibling to the small grey `.comment` gloss |

---

## PDF export (manual, not built)

The skill does not generate a PDF. reveal.js exports one in the browser: open the deck, append
**`?print-pdf`** to the URL, then Print → Save as PDF. Chalkboard/menu don't interfere with print mode.

Chrome headless makes the same export scriptable:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --no-pdf-header-footer --run-all-compositor-stages-before-draw --virtual-time-budget=40000 \
  --print-to-pdf=deck.pdf "<deck-url>?print-pdf&pdfSeparateFragments=false"
```

`pdfSeparateFragments=false` collapses each slide's fragments into **one page per slide**. Verify
with `pdfinfo deck.pdf` against `Reveal.getTotalSlides()`.

---

## Viewing the deck

The deck is standalone — open it straight from disk:

```bash
open slides/chNN/index.html
```

reveal.js runs from `file://`. If a `file://` quirk blocks an asset (rare), serve the folder
locally: `python3 -m http.server -d slides/chNN 8000` → `open http://localhost:8000/`. Figures
resolve via `figures/<name>` (local to the bundle); `slides_files/` carries reveal + plugins.
