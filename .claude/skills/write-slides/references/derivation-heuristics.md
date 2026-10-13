# Autonomous derivation heuristics (Phase 2)

> **This skill is autonomous — there is no interview.** Given `chNN`, the skill derives the audience,
> takeaways, and outline from the chapter's **mind map** (`mindmaps/chNN-*.md`) and its **study
> guide** (`book/notebooks_quarto/NN-*.qmd`), then builds, renders, and verifies in one pass. The
> user reviews the rendered deck afterward. **Do not call `AskUserQuestion`** (the only prompt is
> the overwrite guard in Phase 1).

---

## Audience → always **Teaching**

Mastering Causal Metrics is a study guide for first-year students. This fixes the rhetorical balance
(clarity > compression, intuition before formalism, an Agenda slide), the slide count (**~30–45, a
full lecture including the case studies**), and the MB/MC threshold — see `rhetoric-of-decks.md` §
audience table (Teaching row).

---

## Outline → the mind map is the skeleton

The mind map **drives** the deck. Map it mechanically:

| Mind-map element | Deck element |
|---|---|
| `# <Chapter title>` | front-matter `title:` |
| `## Act I · The Question` | Act I divider (`#3498db`) — its bullets → Hook, motivating evidence, Agenda, Key-concepts slides |
| `## Act II · The Investigation` | Act II divider (`#8e44ad`) |
| each Act II top-level bullet (a *block*) | a run of slides; optionally a short block-intro slide if the block is long |
| each Act II second-level bullet (a *leaf*) | **≈ one slide** (figure / table / equation / mermaid / code / narrative) |
| `## Act III · The Resolution` | Act III divider (`#2d8659`) |
| `Devil's advocate` leaves | one Devil's-Advocate slide each (≤ 2) |
| `Takeaways` | one Key-Takeaways slide (assertions) |
| `Thesis: …` | the Closing divider (after the Recap slide) |

Add on top of the mapped slides: the **Agenda** (Act I), **3–5 Code slides** (next to the leaves
that introduce each tool — see `slide-mapping.md § Code coverage`), and the **Recap** (visual
summary again, just before the Closing).

If a leaf carries two assertions, split it; if two adjacent leaves are thin, merge them. If the deck
would exceed ~45 slides, merge thin leaves first, then move detail into speaker notes. **If the
mind map is missing**, write it first (format: `mindmaps/README.md`; derive it from the study guide's
Learning Objectives, Key Concepts, sections, case studies, Key Takeaways), then continue.

```
Title (visual summary)
Act I  · Divider              — the question
  Hook                        — the motivating question (pathos)
  Naive evidence              — the first comparison and why it is suspicious
  Agenda                      — the three acts as learning objectives
  Key concepts                — 1–2 slides of the chapter's vocabulary
Act II · Divider              — the investigation
  one slide per mind-map leaf — figure / table / equation / mermaid / code, assertion-titled
  case studies are CORE       — design → validity check → main results → interpretation
Act III· Divider              — the resolution
  Devil's-Advocate (1–2)      — the chapter's causal caveat(s)
  Headline-result (optional)  — only if one memorable number exists
  Key Takeaways               — restated as assertions
  Recap                       — the visual summary (mind map) again
  Closing                     — the Thesis leaf as one declarative sentence
```

---

## Content source → the study guide (never invent)

- **Assertions and prose** ← the study guide's interpretation text (callouts, "Interpretation",
  "What did we learn") → slide titles, takeaway cards, and `::: {.notes}`.
- **Numbers** ← the chapter's rendered tables (`book/_book/notebooks_quarto/NN-*.html`) or, when a
  value only exists as code output, a quick local re-run of the chapter's own regression
  (`uv run python …`). Never retype numbers from memory.
- **Diagrams** ← the chapter's `{mermaid}` blocks, cleaned to the CLAUDE.md rules.
- **Code** ← the chapter's `{python}` cells and the "Learn by Coding" cheatsheet (Python only).
- **Skip** Exercises, the cheat-sheet section itself, Stata blocks, and Colab/badge boilerplate.
- **Copyright:** paraphrase; never copy the book's sentences or character names.

---

## Takeaways → per-slide cards

The chapter's **Learning Objectives** and **Key Takeaways** (and the mind map's Takeaways leaves) seed
both the Act-III Key-Takeaways slide **and** the per-slide `.takeaway` cards (the green accent card
each content slide ends on; see `slide-archetypes.md`).

---

## Devil's-Advocate → from the mind map

Use the mind map's `Devil's advocate` leaves (each is "misconception → correction"). Typical caveats
in this book: *a raw comparison is causal* (selection bias), *not significant = no effect*
(precision), *IV estimates the effect for everyone* (LATE), *the exclusion restriction can be
tested*, *parallel trends are guaranteed*, *RD estimates apply far from the cutoff*.

---

## No confirmation gate

The skill writes, renders, and verifies without waiting for a `y`. Print the SCOPE note (one line per
slide: `archetype · assertion title`), build, and report — including any dropped figures, any mind-map
leaf folded into notes, and any `[~]` verification warnings.
