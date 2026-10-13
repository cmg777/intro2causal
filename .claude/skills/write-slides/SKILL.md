---
name: write-slides
description: Generate a branded Quarto reveal.js lecture deck for a Mastering Causal Metrics (intro2causal) chapter. Reads the chapter's 3-act mind map (mindmaps/chNN-*.md) as the outline skeleton and its study guide (book/notebooks_quarto/NN-*.qmd) for content — key concepts, equations, mermaid causal diagrams, case-study results tables, Python (pyfixest) code, and key takeaways — then autonomously (no interview) builds an assertion-titled, one-idea-per-slide, 3-act lecture deck (~30–45 slides) with case studies as core content. Writes slides.qmd + the book-palette dark SCSS theme + a visual-summary title-slide partial into slides/chNN/, renders with `uv run quarto render`, verifies (render + static smoke test + browser math-check), adds a "View Slides" badge to the book chapter, and re-renders the book. The chapter visual summary (stand-in for the future mind-map image) is the title slide and the closing recap. English-only.
argument-hint: "<chNN> [--no-verify]"
disable-model-invocation: true
user-invocable: true
---

# Write Slide Deck: a branded Quarto reveal.js lecture for a Mastering Causal Metrics chapter

Produce a **Quarto reveal.js deck** for a chapter of the study guide. The deck follows the chapter's
**mind map** (`mindmaps/chNN-*.md`) act by act and presents the chapter as an **assertion-titled,
one-idea-per-slide lecture** — the chapter's own tables, mermaid diagrams, equations, and Python code,
restructured into a teaching talk with reveal.js's built-in **menu, chalkboard, speaker view,
preview-links, and overview**.

The deck is authored as a `slides.qmd` (`format: revealjs`) and rendered by the **Quarto CLI**
(`uv run quarto`) to a standalone **`slides/chNN/`** directory, published by GitHub Pages at
`https://cmg777.github.io/intro2causal/slides/chNN/`. It is branded to the book's **fixed** dark
palette and needs no CDN except MathJax and mermaid (reveal + plugins are bundled by Quarto).

The workflow is **autonomous**: given `chNN`, the skill reads the mind map (outline) and the study
guide (content), derives the full slide list, then builds, renders, verifies, and links the deck in
one pass. The user reviews the rendered deck afterward. The craft (3-act arc, assertion titles,
pedagogical movement, MB/MC pacing, Devil's-Advocate) lives in
[`references/rhetoric-of-decks.md`](references/rhetoric-of-decks.md); the mind-map → deck mapping is
in [`references/derivation-heuristics.md`](references/derivation-heuristics.md).

---

## What this skill does NOT do

- **Does not change chapter content.** The only edit outside `slides/` is the one-line "View Slides"
  badge in `book/notebooks_quarto/NN-*.qmd` (Phase 5) and the resulting `book/_book/` re-render.
- **Does not execute code in the deck.** Deck code blocks are illustrative (`{.python}`, not
  `{python}`), so `quarto render slides.qmd` is a pure Pandoc render — no kernel. (Code blocks *are*
  test-run locally once in Phase 3 so every slide's code works.)
- **Does not draw the mind-map image.** The visual summary image is made later in a separate app from
  `mindmaps/chNN-*.md`; until then the concept card `book/images/chNN_visual_summary.svg` stands in.
- **Does not design a theme per deck.** `site-brand.scss` is copied verbatim every run.
- **Does not produce a single self-contained file.** Chalkboard is incompatible with
  `embed-resources`, so the deck ships `index.html` + `slides_files/`.
- **Does not export a PDF.** It documents reveal.js's `?print-pdf` recipe (Phase 6).
- **Does not show Stata.** Code slides are Python (pyfixest) only.
- **Does not commit or push** unless the user asked for it in the conversation; Phase 6 prints a
  copy-pasteable commit snippet.

---

## Example invocations

```
# Standard run: read mind map + chapter, export figures, derive the outline, write slides.qmd +
# theme + partials, render → index.html + slides_files/, verify, add the book badge, re-render book.
/write-slides ch01
/write-slides ch03

# Skip verification (render + smoke test + math-check). A minimal file sanity check still runs.
/write-slides ch02 --no-verify
```

---

## Deliverables

| Path | Purpose |
|---|---|
| `mindmaps/chNN-<slug>.md` | The chapter's 3-act mind map (read; written first only if missing) |
| `slides/chNN/slides.qmd` | Deck source (`format: revealjs`) — the only per-chapter authored deck file |
| `slides/chNN/site-brand.scss` | revealjs theme (copied verbatim from `references/templates/`) |
| `slides/chNN/title-slide.html` | title-slide partial rendering the visual summary (copied verbatim) |
| `slides/chNN/figure-zoom.html` | click-to-zoom lightbox for figures + the visual summary (copied verbatim) |
| `slides/chNN/figures/` | `visual_summary.svg` (or `.png`) + any chosen chapter figures |
| `slides/chNN/index.html` | the rendered deck (`quarto render` output) |
| `slides/chNN/slides_files/` | reveal.js + plugins + libs (`quarto render` output, ~8 MB) |
| `book/notebooks_quarto/NN-<slug>.qmd` | + one "View Slides" badge line next to the Colab badge |

**Commit the whole `slides/chNN/` dir** — source **and** rendered output — plus the re-rendered
`book/_book/`. Only the staging cache and Quarto cache are ignored (`slides/*/_figcache/`,
`slides/*/.quarto/` — see `.gitignore`).

---

## Book-palette dark brand (fixed — every deck)

`site-brand.scss` carries these; do not vary them.

| Token | Hex | Use in the deck |
|---|---|---|
| DeepSlate canvas | `#0f172a` | The deck canvas (the book's dark-mode background and the visual summaries' fill) |
| Body / headings | `#e2e8f0` / `#f1f5f9` | Body copy / assertion titles |
| Muted | `#94a3b8` | Captions, glosses |
| **Question blue** | `#3498db` | **Act I divider** |
| **Method purple** | `#8e44ad` | **Act II divider**, optional headline-result background |
| **Result green** | `#2d8659` | **Act III divider**, Closing, `.takeaway` card fill |
| Bias red / light | `#c0392b` / `#f87171` | Mermaid "problem" nodes / Devil's-Advocate objection text |
| Caution orange | `#e67e22` | `.key` table cells, `.bignum`, mermaid confounder nodes |
| CausalBlue (dark) | `#38bdf8` | Title underline, links, `strong`, list markers, code rule, rebuttal |
| MethodPurple (dark) | `#a78bfa` | h3 column-header underline |
| EvidenceGreen (dark) | `#34d399` | `.takeaway` accent bar |
| Fonts | Inter / JetBrains Mono | Body + headings / code |

Fills are the CLAUDE.md mermaid palette (so slides match the chapter diagrams); inline accents are
the book's dark-mode tokens from `book/custom.css`.

---

## Phase 1: Pre-flight (read-only, except the figure cache)

### 1.1 Parse arguments
- **Chapter id** — first positional token, `ch01`…`ch06`. Mandatory.
- **`--no-verify`** — skip Phase 4 (a minimal file sanity check still runs).
Reject unknown flags.

### 1.2 Locate the inputs
- Chapter: glob `book/notebooks_quarto/<NN>-*.qmd` (e.g. `ch01` → `01-randomized-trials.qmd`).
  Hard-fail if absent.
- Mind map: `mindmaps/ch<NN>-*.md`. If absent, **write it first** following `mindmaps/README.md`
  (3 acts, ≤ 3 levels, numbers only from the study guide), then continue.
- Visual summary: `book/images/ch<NN>_visual_summary.*` (staged by the exporter).

### 1.3 Detect an existing deck
If `slides/<chNN>/slides.qmd` exists, ask: **(a)** overwrite [default], **(b)** cancel. (The one
allowed interactive prompt — a safety guard, not an interview.)

### 1.4 Read the mind map, then the chapter
Read the mind map: its three acts become the three dividers; each Act II leaf becomes ≈ one slide;
the Devil's-advocate, Takeaways, and Thesis leaves fill Act III.

Read the chapter `.qmd` in full and extract, per leaf: the interpretation prose (→ speaker notes and
takeaway cards), the relevant `$$…$$` equations, `{mermaid}` diagrams, Markdown tables, and the
`tbl-*` results tables. Note the Learning Objectives (→ Agenda) and Key Concepts (→ 1–2 concept
slides). **Identify the main tools** — the `pf.feols` patterns and pandas idioms the chapter
introduces (from its `{python}` cells and the "Learn by Coding" cheat sheet). Each needs a Code slide.

### 1.5 Collect the numbers
For every results table you will show, take the values from the rendered chapter
(`book/_book/notebooks_quarto/NN-*.html`) or re-run the chapter's own regression locally
(`uv run python` on the local `data/chN/*.csv`). Never type numbers from memory.

### 1.6 Export figures + the visual summary
```bash
uv run python .claude/skills/write-slides/scripts/export_chapter_figures.py <chNN>
```
Writes `slides/<chNN>/_figcache/` with `figures_manifest.json` (each figure → `{cache_file, src,
heading}`) + `visual_summary.svg|png`. A chapter with **zero figures** (ch01) is normal. Add
`--source render` if the chapter's plots changed since the last book render. **Cap on-slide figures
at 12**; log any dropped filenames.

---

## Phase 2: Derive the deck (autonomous — no interview)

Apply [`references/derivation-heuristics.md`](references/derivation-heuristics.md) +
[`references/slide-mapping.md`](references/slide-mapping.md):

- **Audience** = Teaching (fixed). **Length** = ~30–45 slides.
- **Outline** = the mind map: Act I (hook, naive evidence, agenda, key concepts) → Act II (one slide
  per leaf; **case studies are core** — design → validity check → results → interpretation) → Act III
  (Devil's-Advocate ×1–2, Key Takeaways, **Recap** with the visual summary, Closing = Thesis).
- **Code slides (required)** = one per main tool (typically 3–5), next to the leaf that introduces it.
- **Diagrams** = the chapter's mermaid diagrams, cleaned to the CLAUDE.md mermaid rules.

Print a short SCOPE note (one line per slide: `archetype · assertion title`), then proceed directly
to writing — no approval gate.

---

## Phase 3: Generate the deck

### 3.1 Create the folder
`slides/<chNN>/`.

### 3.2 Copy verbatim templates
Copy unchanged from `references/templates/`: **`site-brand.scss`**, **`title-slide.html`**,
**`figure-zoom.html`**.

### 3.3 Copy images
Copy `_figcache/visual_summary.*` and the chosen `_figcache/fig_*.png` into `slides/<chNN>/figures/`.

### 3.4 Author `slides.qmd`
Start from `references/templates/slides.qmd.tmpl`. Front matter:
- `title` (the chapter title, e.g. "1. Randomized Trials") and a one-line `subtitle`.
- `deck-author: "Carlos Mendez"`, `deck-author-url: "https://carlos-mendez.org"`,
  `institute: "Nagoya University (GSID)"`, `date: today`, `date-format: long`.
- `visual-summary: "figures/visual_summary.svg"` (or `.png`).

Write the body from the outline using
[`references/slide-archetypes.md`](references/slide-archetypes.md):
- `##` assertion titles; `# … {.divider background-color="…"}` act dividers (Act I `#3498db`,
  Act II `#8e44ad`, Act III `#2d8659`) named after the mind map's acts.
- Tables as Markdown with `[cell]{.key}`; `{mermaid}` diagrams (archetype 13); equations `$$…$$`;
  columns `::: {.columns}`; speaker notes `::: {.notes}` on nearly every slide.
- **Code** ` ``` {.python code-line-numbers="…"} ` (**illustrative, never `{python}`**), each block
  self-contained: `!pip install -q pyfixest`, imports, `GITHUB_DATA_URL =
  "https://raw.githubusercontent.com/cmg777/intro2causal/main/data/"`, `pd.read_csv(GITHUB_DATA_URL +
  "chN/<file>.csv")`, then `pf.feols(..., vcov=...)`; **comment every line**; the
  `↗ Try it in Colab` `.colab-link` pill on its own line below each fence. **Test every block**
  locally (drop the `!pip` line; `uv run python`) before rendering.
- **End each substantive content slide with its takeaway card** — `[…]{.takeaway .fragment}`;
  `.comment` only for small figure/equation glosses.
- **On-slide math is LaTeX `$...$`, never literal Unicode**; notes stay Unicode.
- **Recap** (archetype 14) right before the Closing, with `background-image` equal to
  `visual-summary:`.
- Original wording only (CLAUDE.md copyright rule); no book table numbers in titles.

Run the **MB/MC + one-idea-per-slide pass** before rendering.

### 3.5 Render
```bash
cd slides/<chNN> && uv run quarto render slides.qmd
```
→ `index.html` + `slides_files/`. On failure, apply the **render-and-fix loop (max 3 attempts)** from
[`references/render-and-fix.md`](references/render-and-fix.md). Confirm `index.html` exists (> 30 KB)
and no `{{…}}` marker remains.

---

## Phase 4: Verification (skip if `--no-verify`)

Run [`references/verification-checklist.md`](references/verification-checklist.md):
- **Layer 0** — the render above.
- **Layer A** — local files: `index.html` > 30 KB, `slides_files/`, every `figures/*` resolves.
- **Layer B** — `BASE="$PWD/slides/<chNN>" node .claude/skills/write-slides/references/templates/smoke-test.js`
  (title + recap visual summary, code ≥ 1, mermaid, dividers, slide band).
- **Layer C** — `node .claude/skills/write-slides/references/templates/math-check.cjs "$PWD/slides/<chNN>/index.html"`
  (Playwright; **mandatory when the deck has math**). If Playwright is unavailable, open the deck in
  Chrome and check every math slide and every mermaid slide by eye.
- **Overflow pass** — screenshot every slide at 1280×720 (fragments shown) and look at each; fix
  overflow, truncated mermaid labels, and diagrams too small to read (a table often beats a 6+-node
  diagram). Keep scratch files in a per-chapter folder (`<scratchpad>/chNN_work/`).
- **Content checks** — every Act II mind-map leaf has a slide (or is logged as folded); every table
  number matches Phase 1.5; every code block ran.

---

## Phase 5: Link the deck from the book

1. In `book/notebooks_quarto/NN-<slug>.qmd`, add this line directly after the "Open In Colab" badge
   (skip if already present):
   ```markdown
   [![View Slides](https://img.shields.io/badge/View-Lecture_Slides-8e44ad?logo=revealdotjs&logoColor=white)](https://cmg777.github.io/intro2causal/slides/chNN/)
   ```
2. Re-render the book (CLAUDE.md rule — the published book is `book/_book/`):
   ```bash
   uv run quarto render book/
   ```
3. Confirm the chapter page in `book/_book/notebooks_quarto/NN-<slug>.html` shows the badge.

---

## Phase 6: Report + follow-ups

Print the `[✓]/[✗]/[~]` report from the checklist, then offer copy-pasteable follow-ups (never
auto-run):
```
NEXT STEPS (copy + paste)
=========================
1. Preview (press M=menu, B=chalkboard, S=speaker view, O=overview):
   open slides/<chNN>/index.html
   # or, if a file:// asset is blocked:
   python3 -m http.server -d slides/<chNN> 8000  &&  open http://localhost:8000/

2. Export a PDF handout (the skill does not build one):
   a) in-browser: open the deck, append ?print-pdf, Print → Save as PDF (landscape, no margins,
      background graphics on)
   b) scriptable — one page per slide, fragments flattened:
      CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
      "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
        --run-all-compositor-stages-before-draw --virtual-time-budget=40000 \
        --print-to-pdf=slides/<chNN>/deck.pdf \
        "file://$PWD/slides/<chNN>/index.html?print-pdf&pdfSeparateFragments=false"

3. Re-render after editing slides.qmd:
   cd slides/<chNN> && uv run quarto render slides.qmd

4. Swap in the mind-map image when it exists:
   save it as book/images/<chNN>_visual_summary.png (or .svg), re-run the exporter, copy
   _figcache/visual_summary.* into slides/<chNN>/figures/, update `visual-summary:` and the Recap
   `background-image` in slides.qmd, re-render.

5. Commit (source + rendered deck + re-rendered book):
   git add slides/<chNN>/ book/notebooks_quarto/<NN>-*.qmd book/_book/
   git commit -m "<chNN>: add Quarto reveal.js lecture deck

   Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
If any `[✗]`: surface the failed assertion with its path; suggest the matching `render-and-fix.md`
entry; offer a re-run.

---

## Reference files

- [`references/derivation-heuristics.md`](references/derivation-heuristics.md) — mind map → deck
  mapping; content-source and numbers rules; no interview.
- [`references/slide-mapping.md`](references/slide-mapping.md) — chapter element → slide → act;
  lecture coverage; code coverage; tables/figures; title + recap visual summary; MB/MC pass.
- [`references/slide-archetypes.md`](references/slide-archetypes.md) — the 14 slide layouts as
  copy-paste Quarto markdown (incl. Mermaid and Recap).
- [`references/rhetoric-of-decks.md`](references/rhetoric-of-decks.md) — Three Laws, audience triad,
  3-act arc, assertion titles, MB/MC, Devil's-Advocate.
- [`references/quarto-revealjs-guide.md`](references/quarto-revealjs-guide.md) — how the
  `.qmd`+`.scss`+partials compose; render command; format options; why not embed-resources.
- [`references/verification-checklist.md`](references/verification-checklist.md) — Phase-4 checks +
  report template.
- [`references/render-and-fix.md`](references/render-and-fix.md) — failure-mode catalog.
- `scripts/export_chapter_figures.py` — stages a chapter's figures + visual summary into `_figcache/`.
- `references/templates/` — `slides.qmd.tmpl`, `site-brand.scss`, `title-slide.html`,
  `figure-zoom.html`, `smoke-test.js`, `math-check.cjs`.
- `mindmaps/README.md` (repo root) — the mind-map format.

---

## Acceptance tests (for the skill itself)

1. **Reference deck — `ch01`.** Expect `slides/ch01/{slides.qmd, site-brand.scss, title-slide.html,
   figure-zoom.html, figures/visual_summary.svg}`; `quarto render` → `index.html` + `slides_files/`;
   title and recap show the visual summary; smoke test 100% `[✓]`; math renders.
2. **Mind-map fidelity.** Three dividers named after the mind map's acts; every Act II leaf has a
   slide (or is logged as folded); the Closing is the Thesis leaf.
3. **Lecture length.** ~30–45 slides; case studies covered as design → check → results.
4. **Numbers.** Every table value equals the rendered chapter / local re-run.
5. **Code coverage.** ≥ 1 Code slide per main tool; each block self-contained, commented, runs
   locally, and carries the `↗ Try it in Colab` pill. Python only.
6. **Zero-figure chapter.** `export_chapter_figures.py ch01` writes an empty `figures` list and
   stages `visual_summary.svg` without error.
7. **Book link.** The chapter page has the "View Slides" badge → `…/slides/chNN/`; book re-rendered.
8. **No embed-resources.** The deck ships `index.html` + `slides_files/` (chalkboard works).
9. **Idempotent re-run.** A second run detects `slides/chNN/`, asks before overwriting, reproduces
   byte-identical `site-brand.scss`/`title-slide.html`/`figure-zoom.html`.
