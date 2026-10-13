# Chapter mind maps

One mind map per chapter of *Mastering Causal Metrics*, written as a **Markdown outline**. Each map
is the chapter's visual summary in text form and the **outline skeleton for the chapter's slide
deck** (`/write-slides chNN` reads it before writing `slides/chNN/slides.qmd`).

| File | Chapter |
|---|---|
| `ch01-randomized-trials.md` | 1. Randomized Trials |
| `ch02-regression.md` | 2. Regression |
| `ch03-instrumental-variables.md` | 3. Instrumental Variables |
| `ch04-regression-discontinuity.md` | 4. Regression Discontinuity Designs |
| `ch05-differences-in-differences.md` | 5. Differences-in-Differences |
| `ch06-wages-of-schooling.md` | 6. The Wages of Schooling |

## Format (keep every map in this shape)

```markdown
# <Chapter title>                       ← root node

## Act I · The Question                 ← branch 1: hook, motivating evidence, vocabulary
- <idea>
  - <detail>
    - <fine detail>

## Act II · The Investigation           ← branch 2: problem → method → evidence
- <block>                               ← becomes a group of slides
  - <leaf>                              ← roughly ONE slide each

## Act III · The Resolution             ← branch 3: caveats, takeaways, thesis
- Devil's advocate
- Takeaways
- Thesis: <one sentence>
```

Rules:

- Exactly three `##` branches, named as above, in the deck's 3-act order.
- At most three bullet levels under each act. Short noun phrases, not sentences (the Thesis leaf
  is the one exception).
- Inline math is allowed (`$Y_{1i}$`); keep it light — most mind-map apps show it as raw text.
- Numbers must come from the study guide's tables/text — never invented.
- Original wording only (no text copied from the book).
- No exercises, cheat sheets, or Stata blocks — those are not deck material.

## How the maps are used

- **Slides:** `/write-slides chNN` turns Act I/II/III into the deck's three divider-led acts, and
  each Act II second-level bullet into (roughly) one assertion-titled slide. Edit the map first if
  you want a deck to change shape.
- **Visual summaries:** the mind-map *images* are drawn in a dedicated app and saved, untouched, as
  `mindmaps/images/chNN-<slug>-vN.png` (16:9; bump `vN` for a new version — the highest wins). They
  are the title + recap slides of each deck and the image at the top of each book chapter. Publish
  them with `uv run python .claude/skills/write-slides/scripts/sync_mindmap_images.py` (WebP copies, old concept cards removed, decks + book re-rendered).
