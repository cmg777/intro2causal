# Slide mapping (chapter → deck)

Heuristics that turn a Mastering Causal Metrics chapter — its **mind map**
(`mindmaps/chNN-*.md`, the outline skeleton) + its **study guide** (`book/notebooks_quarto/NN-*.qmd`,
the content) + any exported figures — into an assertion-titled, one-idea-per-slide, 3-act **lecture**
deck (~30–45 slides). Read this in Phase 1 (to draft the outline) and Phase 3 (to assemble slides).
It applies the principles in `rhetoric-of-decks.md` using the Quarto markdown in `slide-archetypes.md`.

The audience is always **Teaching** (first-year students). The goal is a full lecture that follows the
mind map: the question, the investigation (including the case studies), and the resolution.

---

## Chapter element → slide → act

| Chapter element | Slide archetype | Act |
|---|---|---|
| Mind-map root + the chapter's framing | Title (1) — **visual summary** is the key visual | — |
| Act I: the motivating question | Narrative/Hook (4) | I |
| Act I: the naive evidence (first comparison) | Table (6) / Narrative (4) | I |
| Learning Objectives / the three acts | Agenda (2) | I |
| Key Concepts (bold terms + definitions) | Narrative (4) / Two-column (9), 1–2 slides | I |
| Each Act II mind-map **leaf** | Figure (5) / Table (6) / Equation (8) / Mermaid (13) / Narrative (4) — ≈ one each | II |
| A display equation `$$…$$` (decomposition, Wald ratio, …) | Equation (8) — one each | II |
| A `{mermaid}` causal diagram (DAG, design flow) | Mermaid (13), cleaned to CLAUDE.md rules | II |
| A `{python}` cell that introduces a tool | Code (7) — illustrative `{.python}` | II |
| A case study's results table (`tbl-*`) | Table (6), key cell highlighted; values from the rendered chapter | II |
| A headline number (e.g. +45% spending) | Headline-result (11) — optional | II → III |
| Mind map "Devil's advocate" leaves | Devil's-Advocate (10), 1–2 slides | III |
| Mind map "Takeaways" | Narrative (4) as assertions | III |
| — | Recap (14) — the visual summary again | III |
| Mind map "Thesis" | Closing (12), single sentence | III |
| Each slide's concluding line | Takeaway card `[…]{.takeaway .fragment}` (component) | any |

Each act is preceded by a Divider (3). The **per-slide** takeaway card (the green accent card
each content slide ends on) is distinct from the single **Closing** divider — the card restates
that one slide's assertion; the Closing is the deck's final thesis.

---

## Principles applied

- **Mind map first.** Every Act II leaf gets a slide (or is explicitly folded into a neighbour's
  notes — log it). The deck never introduces a block the mind map lacks; edit the map instead.
- **Figure-first, code-first.** A figure, table, diagram or code block is its *own* slide titled with its finding
  — never buried under bullets.
- **One idea per slide.** Split any source paragraph that carries two assertions into two slides;
  merge adjacent thin slides.
- **Assertion titles.** Every content slide's `##` is a sentence stating the finding (see
  `rhetoric-of-decks.md` examples). Pull the claim from the chapter's interpretation prose for
  that figure/table/section.
- **Speaker notes carry the prose.** The chapter's explanatory text goes into `::: {.notes}`, not
  onto the slide.

---

## Lecture coverage — target ~30–45 slides

The study guides have a Key Concepts glossary, 4–6 main sections, 1–3 case studies, a history
section, an inference toolkit, takeaways, a cheat sheet and exercises. The deck follows the mind map:

- **One slide per Act II leaf** (~18–26 leaves) + dividers, hook, agenda, concepts, code slides,
  Devil's-Advocate, takeaways, recap, closing ≈ 30–45 slides.
- **Case studies are core.** Give each its arc: design → validity check (balance / first stage /
  pre-trends …) → main results table → interpretation.
- Keep the Key Concepts glossary to 1–2 slides (the 4–6 terms the deck actually uses); the rest of
  the glossary goes in notes.
- **Skip** Exercises, the "Learn by Coding" cheat sheet (mine it for code slides instead), Stata
  blocks, and badges/boilerplate. The history section is at most one slide (a short `timeline` or
  narrative), and only if the mind map has it.

If the mapping would exceed ~45 slides, merge thin leaves and push detail to notes. If it falls under
~30, do not pad — a shorter chapter makes a shorter deck.

---

## Code coverage (REQUIRED — one code slide per main tool)

The Python code is the point of these chapters. **Every deck MUST include at least one Code slide
(archetype 7), and in general one per *main tool* the chapter introduces** — the new packages,
functions, or methods a student is meant to walk away able to use. Identify them in Phase 1 from the
chapter's `{python}` cells and its "Learn by Coding" cheat sheet; the smoke test fails a deck with
zero code blocks.

Rule of thumb for the essentials deck:

- **One code slide per distinct tool/method**, placed next to the leaf that introduces it — e.g.
  for ch01: `groupby().mean()` (naive comparison) · `pf.feols("y ~ d", vcov="hetero")` (regression on
  a dummy) · `pf.feols(..., vcov={"CRV1": "family_id"})` (balance check with clustered SEs) · the same
  call on an outcome (causal effect). IV chapters add `pf.feols("y ~ 1 | d ~ z")`; panel chapters add
  `| fe` absorbed fixed effects. Typically 3–5 code slides.
- Each block is **self-contained and runnable** (`!pip install -q pyfixest` + imports +
  `GITHUB_DATA_URL = "https://raw.githubusercontent.com/cmg777/intro2causal/main/data/"` +
  `pd.read_csv(GITHUB_DATA_URL + "chN/<file>.csv")` + the tool call), **every line commented**, with
  the `↗ Try it in Colab` pill — see `slide-archetypes.md` archetype 7. **Test each block** locally
  before rendering (`uv run python` with the `!pip` line removed) — a code slide that errors is a bug.
- **Python only** (pyfixest `pf.feols` for every regression, with explicit `vcov=`); no Stata.
- If two tools are tiny and naturally paired, one slide may show both; never cram more than one
  *concept* onto a code slide, and keep each block ≤ ~10 lines (push extra to the notes).
- A theory-only chapter with no new tool is the rare exception — still include the one code slide that
  reproduces its core computation.

## The MB/MC pacing pass (run before rendering)

Walk every slide and every fragment; apply `rhetoric-of-decks.md` § MB/MC:

- Cut/merge **underloaded** slides (a word that wants a sentence; a point the audience already inferred).
- Split/simplify **overloaded** slides (> 5 bullets, two data series, a wall of prose). Push overflow
  to `::: {.notes}`.
- No slide should need > 4 fragment advances.
- Allow one or two deliberate dense "jump scare" slides for effect — on purpose.

---

## Figures: export, selection, capping

- **Export** the chapter's figures in Phase 1 with
  `uv run python .claude/skills/write-slides/scripts/export_chapter_figures.py chNN`. This reuses the
  book-rendered PNGs (or renders fresh) and writes `slides/chNN/_figcache/figures_manifest.json` —
  each entry `{cache_file, src, heading}` — plus `visual_summary.svg` (or `.png`). **A chapter may
  have zero figures** (ch01: tables + mermaid only) — then the manifest's `figures` list is empty and
  the deck leans on Table (6) and Mermaid (13) slides. The book renders plots on a light page; if a
  PNG looks harsh on the dark canvas, keep it anyway (never re-style chapter plots from the skill).
- **Select** the load-bearing figure per mind-map leaf from the manifest (match on `heading`). Copy the chosen `_figcache/*.png` into `slides/chNN/figures/` and
  reference each as `![caption](figures/<cache_file>)`.
- **Cap at 12 on-slide figures.** If more are load-bearing, keep one per distinct finding and **log
  the dropped filenames** in the Phase-5 report — never silently drop.
- Pass `--source render` to the exporter after editing a chapter's plots, so the figures are current.

---

## Tables: Markdown → Quarto markdown

Reuse the chapter's table almost verbatim (archetype 6). Keep the 2–3 columns that carry the
argument; the rest → notes. Tag the headline cell `[…]{.key}` (renders caution orange). The theme
styles it booktabs-ish and right-aligns numbers (`tabular-nums`). **Values come from the rendered
chapter** (`book/_book/notebooks_quarto/NN-*.html`) or a local re-run of the chapter's regression —
show coefficient (SE) pairs exactly as the chapter rounds them. Use plain variable labels
("Family income") instead of code names (`family_income`), and mention the code name in notes.

## Title + Recap slides: the visual summary, full-bleed

The title slide is **only** the chapter's visual-summary image, filling the whole slide — no title,
subtitle, or byline text. Set the front-matter `visual-summary:` field to `figures/visual_summary.svg`
(copied from `_figcache/` by the skill); the `title-slide.html` partial paints it as the slide
**background** (`data-background-image`, `size=contain` → the entire summary, no crop). The **Recap**
slide (archetype 14), just before the Closing, repeats the **same** image path.

The visual summary is meant to be the chapter's **mind-map image** (to be drawn in a separate app from
`mindmaps/chNN-*.md`). Until it exists, the stand-in is the concept card
`book/images/chNN_visual_summary.svg`. When the mind-map image lands (e.g. as
`book/images/chNN_visual_summary.png`, which the exporter prefers when newer), re-run the exporter,
point `visual-summary:` and the Recap `background-image` at the new file, and re-render.

---

## Writing equations (plain LaTeX — the .qmd is Pandoc)

Chapter `.qmd` files are already Pandoc + MathJax, so copy a display equation straight across — no
Goldmark escaping to strip. Inline math `$…$`, display `$$…$$`. Verify visually in the browser
(MathJax errors render visibly but the static smoke test can't catch them — see `render-and-fix.md`
§7 for unsupported macros, §12 for the katex-not-mathjax guard).

## Math symbols → LaTeX (never literal Unicode)

`R²`, `α̂`, and other Unicode math render inconsistently. Convert **all on-slide** math symbols to
LaTeX `$...$`:

| Unicode | LaTeX | · | Unicode | LaTeX |
|---|---|---|---|---|
| `R²` | `$R^2$` | · | `±` | `$\pm$` |
| `α̂` `β̂` | `$\hat\alpha$` `$\hat\beta$` | · | `≈` | `$\approx$` |
| `α` `β` `λ` `σ` | `$\alpha$` `$\beta$` `$\lambda$` `$\sigma$` | · | `∑` `∈` `×̄` | `$\sum$` `$\in$` `$\bar x$` |

- **Mixed numbers:** in captions/bullets/comments/labels write the full expression (`slope $b_2 =
  0.35$`); but keep the orange `[…]{.key}` table cells and the giant `[…]{.bignum}` as **styled
  text** (math drops their colour/size). Plain standalone numbers (284, 0.79) stay text.
- **Notes stay Unicode.** The reveal speaker-notes window doesn't run the math renderer, so LaTeX
  source would show raw there — keep `R²`, `α̂` etc. inside `::: {.notes}`.
- Engine: **MathJax** — Quarto revealjs's default, from a CDN (reveal.js is bundled locally; math
  needs a network). Do NOT set `html-math-method: katex` — it is broken in revealjs (why, and the
  static/browser guards that catch it → `render-and-fix.md §12`).

---

## Edge cases (full handling in `render-and-fix.md`)

- **No exported figures (e.g. ch01):** lean on Table + Mermaid + Equation + Two-column; the visual
  summary still anchors the title and recap slides. Use the chapter's own mermaid diagrams — do not
  invent new diagram types.
- **No single headline number:** that is normal for teaching chapters — skip the optional
  Headline-result slide and let the assertion titles + takeaway cards carry the argument.
- **Very long code:** skeleton on-slide (`{.python}`, illustrative) + full workflow in notes; if
  still overflowing, split into a vertical sub-slide stack.
- **A chapter edited after the last book render:** pass `--source render` to the exporter so the
  figures reflect the current plots.
