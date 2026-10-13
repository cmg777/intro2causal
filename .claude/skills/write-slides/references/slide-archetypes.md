# Slide archetypes (Quarto markdown)

The 14 slide layouts a deck is built from, expressed as **Quarto markdown** (the deck is
authored as `slides.qmd` and rendered with `quarto render`). Each entry is a copy-paste
skeleton — substitute the ALL-CAPS placeholders. Read this in Phase 3 while writing the
`.qmd` body. The visual styling lives in `site-brand.scss`; the engine config lives in the
`.qmd` front matter (see `slides.qmd.tmpl`).

Conventions:

- `##` (h2) = a **content slide**; its heading is the **assertion title** (auto-underlined
  CausalBlue by the theme). `#` (h1) = a **section/divider slide**.
- `center: true` (front matter) vertically centers every slide — dividers land in the middle,
  content blocks use the white space.
- Speaker notes: `::: {.notes} … :::` (press **S**). Fill from the chapter's explanatory prose.
- Reveal one step at a time: `. . .` (a pause between blocks), `::: {.incremental}` (a list),
  or `{.fragment}` on a span/element.
- Figures use a local bundle path: `![caption](figures/<cache_file>)` — the images are copied into
  `slides/chNN/figures/` from `_figcache/` (see `slide-mapping.md § Figures`). Many chapters (e.g.
  ch01) have no matplotlib figures — their visuals are **tables** (archetype 6) and **mermaid
  diagrams** (archetype 13).
- **Math: write LaTeX, never literal Unicode** (`R² → $R^2$`, `α̂ → $\hat\alpha$`, `± → $\pm$`). The
  full rules — the Unicode→LaTeX table, **mixed numbers** (keep `[…]{.key}`/`[…]{.bignum}` as styled
  text), and **notes stay Unicode** — are the canonical `slide-mapping.md §Math symbols → LaTeX`.

---

## 1. Title — front matter only (no body slide)

The title slide is the **chapter visual summary, full-bleed, and nothing else** — no title,
subtitle, or byline text on it. The custom `title-slide.html` partial paints the visual summary as
the slide's **background image** (`data-background-image`, `size=contain`), so the *whole* summary
shows full width with no cropping. The 16:9 mind-map images fill the 1280×720 slide exactly; on a
non-16:9 screen the bars take `visual-summary-bg` (the image's edge colour). The image is the
chapter's mind map (`mindmaps/images/`, staged as `visual_summary.webp` by the exporter). Fill the
front matter:

```yaml
title: "1. Randomized Trials"                  # used for the browser tab / metadata, not shown on the title slide
subtitle: "Why comparing groups misleads — and how a coin flip fixes it"
deck-author: "Carlos Mendez"                   # retained for metadata (not rendered on the title slide)
deck-author-url: "https://carlos-mendez.org"
institute: "Nagoya University (GSID)"
date: today
date-format: long
visual-summary: "figures/visual_summary.webp"  # the chapter's mind-map image — the ENTIRE title slide (and the Recap)
visual-summary-bg: "#07172a"                    # its edge colour (manifest `visual_summary_bg`) — letterbox bars
```

**Use:** always. No `#`/`##` for it — it is the rendered title slide. (`deck-author` /
`deck-author-url` / `visual-summary` / `visual-summary-bg` are custom fields the partial reads.)

**Behaviour.** With `visual-summary:` set, the partial renders a single empty `<section>` whose
background *is* the image — no overlaid text. Clicking it opens the same **click-to-zoom** overlay as
the body figures (full-screen + zoom/pan controls, from `figure-zoom.html`). If a deck has **no**
`visual-summary`, the partial falls back to a text title slide (title + CausalBlue accent rule + subtitle + hyperlinked author +
institute + date); both paths live in `title-slide.html` / `site-brand.scss`.

---

## 2. Agenda (optional)

```markdown
## Where we're going

::: {.incremental}
- ROADMAP ITEM 1
- ROADMAP ITEM 2
- ROADMAP ITEM 3
:::
```

**Use:** always (decks are 30–45 slides). Build from the mind map's three act branches, phrased as
the chapter's **Learning Objectives**.

---

## 3. Section divider

```markdown
# ACT TITLE {.divider background-color="#3498db"}

[Act I]{.act}
```

**Use:** one before each act — the act names come from the mind map (`## Act I · The Question`,
etc.). Per-act colour (CLAUDE.md mermaid palette): **Act I → `#3498db`** (question blue), **Act II →
`#8e44ad`** (method purple), **Act III → `#2d8659`** (result green). The `.divider` class gives white
centred text; `center: true` puts it in the middle of the slide.

---

## 4. Narrative / Hook

```markdown
## ONE-SENTENCE PROVOCATION OR STAKE

A single concrete line — a named dataset, question, or tension.

. . .

The turn or the question that opens the investigation. *Italic for emphasis.*

::: {.notes}
The story you tell aloud; the slide only anchors it.
:::
```

**Use:** open Act I (and to re-engage mid-Act II). Minimal text, high pathos. For a chapter, the hook
is the motivating question (e.g. "Does health insurance make people healthier?").

---

## 5. Figure slide

```markdown
## WHAT THE FIGURE SHOWS, AS A CLAIM

![One-line reading aid — never "Figure 3".](figures/fig_03.png)

::: {.notes}
Walk the audience through what to look at first.
:::
```

**Use:** the deck's backbone — figure-first. Quarto's **`auto-stretch`** (on by default) bounds the
image to the slide and `fig-align: center` centres it — no overflow, no manual sizing. One figure,
one message. The alt/caption is the reading aid; the `##` is the finding. Figures come from the
`figures/` bundle (see `slide-mapping.md § Figures`). Every figure is **click-to-zoom** automatically
(full-screen overlay + zoom/pan controls, from `figure-zoom.html`) — no per-figure markup needed.

---

## 6. Table slide

```markdown
## WHAT THE TABLE PROVES

| Variable | Uninsured mean | Insured − uninsured |
|---|---:|---:|
| Health index (1–5) | [3.66]{.key} | 0.35 |
| Years of education | 11.67 | 2.70 |

[One-line takeaway under the table.]{.takeaway .fragment}
```

**Use:** where a summary-statistics or results table lands the point. Trim to the 2–3 load-bearing
columns; tag the headline cell `[…]{.key}` (renders caution orange). The theme styles it booktabs-ish
(no vertical rules, CausalBlue head rule). **Every number must match the rendered chapter** (read it
from `book/_book/notebooks_quarto/NN-*.html`, or re-run the chapter's regression) — never retype
from memory. Wide tables (4+ numeric columns): wrap in `::: {.small-table}` or keep the 2–3 columns
that carry the argument. Close with the takeaway card (component below).

---

## 7. Code slide

```markdown
## WHAT THESE LINES DO, IN ONE CLAIM

``` {.python code-line-numbers="1|3-4|6-8|10-11"}
!pip install -q pyfixest                     # install pyfixest in Colab (-q = quiet; not preinstalled)

import pandas as pd                           # pandas → load & handle tabular data
import pyfixest as pf                         # pyfixest → regressions with robust/clustered SEs

# all course datasets live in the repo's data/ folder on GitHub
GITHUB_DATA_URL = "https://raw.githubusercontent.com/cmg777/intro2causal/main/data/"
nhis = pd.read_csv(GITHUB_DATA_URL + "ch1/nhis_clean.csv")   # NHIS 2009 survey extract

m = pf.feols("health ~ insurance", data=nhis, weights="weight", vcov="hetero")  # regress on a dummy
m.summary()                                   # intercept = uninsured mean; slope = gap; robust SEs
```

[↗ Try it in Colab](https://colab.research.google.com/notebooks/empty.ipynb){.colab-link target="_blank" data-preview-link="false"}

::: {.notes}
Self-contained — paste it into the empty Colab notebook and it runs end to end.
:::
```

**Use:** when the deck teaches code. `{.python}` highlights **without executing** (the deck has no
kernel); `code-line-numbers="a|b|c"` reveals groups as fragments. **Make the block self-contained
and runnable** — lead with a quiet install of any package Colab lacks
(`!pip install -q pyfixest` — pyfixest isn't preinstalled; pandas/numpy/matplotlib are), then the
imports *and the data load* (the book's `GITHUB_DATA_URL + "chN/<file>.csv"` pattern with
`pd.read_csv`) so a reader can paste it into an empty Colab cell and reproduce the result — don't
assume a variable already exists. **Regressions always use `pf.feols()` with an explicit `vcov=`**
(`"hetero"` or `{"CRV1": "<cluster var>"}`), matching the chapter. Python only — no Stata on slides. Keep ≤ ~10 lines; if a full listing would overflow, show the load +
headline call here and push extra detail to the notes. **Comment every line pedagogically** — a
short trailing `#` note saying what that line does (what each import is *for*, what the data-load
reads, what the model call fits, what the output reports) so a learner can follow the block without
the chapter open. For a long line (e.g. a data URL), put its comment on the line *above* it to avoid
horizontal overflow.

**Always add the Colab link** on its own line right below the code fence — the branded `.colab-link`
pill to the empty-notebook URL, so a reader can open a scratch notebook and paste the block:

```markdown
[↗ Try it in Colab](https://colab.research.google.com/notebooks/empty.ipynb){.colab-link target="_blank" data-preview-link="false"}
```

`target="_blank"` opens it in a new tab; `data-preview-link="false"` stops reveal's inline
link-preview from intercepting the click.

---

## 8. Equation slide

```markdown
## WHAT THE EQUATION SAYS, IN WORDS

$$\hat{y} = b_1 + b_2 x$$

[The fitted line predicts $y$ from $x$: $b_1$ is the intercept, $b_2$ the slope — the predicted
change in $y$ per one-unit change in $x$.]{.comment}
```

**Use:** one equation per slide with a plain-language gloss (`.comment`, small/centred — it
*explains* the equation). If the closing line is instead the slide's **concluding takeaway** (not a
gloss of the math), use `[…]{.takeaway .fragment}` (component below). Plain LaTeX — Pandoc/MathJax
render it.

---

## 9. Two-column compare

```markdown
## A VS B — THE LOAD-BEARING CONTRAST

:::: {.columns}
::: {.column width="50%"}
### CORRELATION
- unit-free, in $[-1, 1]$
- symmetric in $x$ and $y$
:::
::: {.column width="50%"}
### COVARIANCE
- carries the units of $x \times y$
- sign only, scale not comparable
:::
::::
```

**Use:** the one place two ideas may share a slide — an *inseparable* contrast (correlation vs
covariance; association vs causation). Column `###` headers get a MethodPurple underline.

---

## 10. Devil's-Advocate

```markdown
## The tempting mistake — and the correction

[Objection.]{.objection} THE INSURED ARE HEALTHIER, SO INSURANCE MUST WORK.

. . .

[Response.]{.rebuttal} THE GAP BUNDLES THE CAUSAL EFFECT WITH SELECTION BIAS — PEOPLE WHO BUY
INSURANCE WERE ALREADY DIFFERENT.
```

**Use:** early Act III — one or two, taken from the mind map's "Devil's advocate" leaves (the
chapter's key causal-inference caveat: selection bias, untestable exclusion, LATE ≠ ATE, parallel
trends, significance ≠ importance…). Steelman the misconception (light red), then correct it
(CausalBlue).

---

## 11. Headline-result (optional for teaching chapters)

```markdown
## THE RESULT, AS A SENTENCE {background-color="#8e44ad"}

[+45%]{.bignum}

[more total health spending on the free plan than on the catastrophic plan]{.bignum-label}
```

**Use:** only when the chapter *does* have one memorable number worth a full-bleed slide. One giant
number + one line on a full-bleed method-purple slide that lifts off the dark canvas
(`has-dark-background` keeps text light; the theme makes `.bignum` bright amber there). Many teaching
chapters have no single headline number — skip this archetype then.

---

## 12. Closing

```markdown
# THE ONE SENTENCE YOU WANT THEM TO REMEMBER. {.divider background-color="#2d8659"}
```

**Use:** always, the final slide, right after the Recap (archetype 14). The mind map's **Thesis**
leaf, as a centred `#` section slide on a full-bleed brand colour (result green, or question blue to
bookend the Act-I divider). **Never** "Questions?", "Thank you", or a contact list.

---

## 13. Mermaid diagram slide

````markdown
## WHAT THE DIAGRAM SHOWS, AS A CLAIM

```{mermaid}
graph LR
    C["Confounders: education, income, jobs"] --> I["Insurance status"]
    C --> H["Health"]
    I -.->|"causal effect?"| H
    style C fill:#e67e22,color:#fff
    style I fill:#3498db,color:#fff
    style H fill:#2d8659,color:#fff
```

[One-line takeaway.]{.takeaway .fragment}
````

**Use:** for the chapter's causal diagrams (DAGs, decompositions, design flowcharts) — reuse the
chapter's own mermaid diagram, cleaned to the CLAUDE.md rules: `graph TD|LR` (never `flowchart`),
`["quoted"]` labels on **one line** (no `<br/>`, no `\n`, no numbered lists), every node styled from
the palette with `color:#fff`, ≤ 6–8 nodes so it fits 720p, and labels ≤ ~26 characters (longer
ones wrap onto two lines). No `%%| label`/`fig-cap` needed on a
slide (the `##` is the claim). Mermaid renders client-side — no kernel. Prefer `graph LR` for wide
slides. Mermaid `timeline` diagrams also work but are tall; keep them to ≤ 4 sections.

---

## 14. Recap (the visual summary again)

```markdown
## {.recap background-image="figures/visual_summary.webp" background-size="contain" background-color="#07172a"}

::: {.notes}
Walk the mind map one last time: Act I question → Act II investigation → Act III resolution.
:::
```

**Use:** always — the penultimate slide, just before the Closing. An **empty `##`** (no visible
title) whose background is the same image as the title slide, so the deck opens and closes on the
chapter's map. The `background-image` path **must equal the front-matter `visual-summary:`** and
`background-color` the `visual-summary-bg:` (`sync_mindmap_images.py` rewrites both). The smoke test checks for it (`.recap` +
≥ 2 visual-summary backgrounds).

---

## Takeaway card — the concluding line of a content slide

Not a full archetype — a **component** most content slides (Narrative, Figure, Table) should end
with: the slide's assertion restated as one memorable sentence, rendered as a prominent brand
**accent card** (soft result-green fill, bold EvidenceGreen left bar, semibold text) that **rises + fades
in** as the final fragment.

```markdown
[One-sentence takeaway — the point, stated so it sticks.]{.takeaway .fragment}
```

- **`.takeaway` vs `.comment`.** `.takeaway` is the prominent card — the slide's conclusion.
  `.comment` stays the small grey caption/gloss that *explains* a figure/table/equation. Don't swap
  them: a takeaway is a claim you want remembered; a gloss is a reading aid.
- **Always a `.fragment`** so it lands last, after the evidence above it. It counts as one fragment
  advance (keep the slide's total ≤ ~4).
- Sits on content slides (never on a `.divider`); the styling lives in `site-brand.scss`.
- This is the per-slide takeaway — distinct from the single **Closing** divider (archetype 12),
  which is the deck's one final thesis.

---

## Assembly notes

- Order follows the mind map: front-matter title → Act I divider → … → Recap → Closing. The
  auto title slide is first; the body starts at the Act I `#` divider.
- Prefer ending each substantive content slide with a `[…]{.takeaway .fragment}` — the assertion
  title states the claim; the takeaway card restates it as the memorable line.
- Prefer horizontal slides; use a vertical sub-stack only when one idea genuinely needs sub-steps
  (Quarto: nest with `##` under a `#`, or use `. . .`).
- Every content slide gets a `##` assertion; only the title, dividers, and closing use `#` or the
  front matter.
- Put `::: {.notes}` on any slide whose spoken content exceeds what's shown — most of them.
