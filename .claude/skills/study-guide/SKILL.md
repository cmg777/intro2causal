---
name: study-guide
description: Create a Quarto study guide for a chapter of Mastering 'Metrics. Reads the original chapter, existing Python scripts, and data files, then produces a pedagogical .qmd document with clean code and diagrams. Use this when the user asks to create a study guide for a specific chapter.
argument-hint: [chapter-number]
---

# Study Guide Generator for Mastering 'Metrics

Create a complete Quarto study guide for **Chapter $ARGUMENTS** of *Mastering 'Metrics* by Angrist & Pischke.

## Phase 1: Gather Materials

Read these files to understand the chapter content and available resources:

1. **Original chapter text**: Look in `original-book/` for the chapter markdown file (e.g., `01-randomized-trials.md`, `02-regression.md`, etc.)
2. **Existing Python scripts**: Look in `code/python/ch$ARGUMENTS/` for any `.py` files that replicate the chapter's tables and figures
3. **Existing clean data**: Check `data/ch$ARGUMENTS/` for any pre-processed `.csv` files
4. **Reference template**: Read `notebooks_quarto/01-randomized-trials.qmd` as the gold-standard template for structure, tone, and formatting

Identify:
- The chapter's main causal inference method (e.g., RCT, regression, IV, RD, DD)
- The motivating real-world question
- The key case studies and datasets
- The tables and figures to replicate
- The historical "Masters of 'Metrics" section
- The appendix topics

## Phase 2: Prepare Clean Data

If clean CSV files do not already exist in `data/ch$ARGUMENTS/`:

1. Create `code/python/ch$ARGUMENTS/prepare_data.py`
2. This script should:
   - Load raw `.dta` files from `data/ch$ARGUMENTS/`
   - Perform all messy transformations (Stata label conversion, filtering, merging, variable construction)
   - Save clean `.csv` files with intuitive English column names
   - Print a summary of what was saved
3. Run the script to verify it produces the clean files
4. The study guide will then load only the clean CSVs

## Phase 3: Write the Quarto Study Guide

Save the output to: `notebooks_quarto/NN-chapter-name.qmd`

Use the numbering from the book (e.g., `03-instrumental-variables.qmd` for Chapter 3).

### Document Structure

Follow this exact section order:

```
1. YAML front matter
2. Learning objectives (callout-tip)
3. Roadmap paragraph + mermaid flowchart
4. Motivating real-world question (with data)
5. Conceptual framework (theory that explains the data)
6. Case study sections (with Python code replicating key tables)
7. Historical perspective (Masters of 'Metrics)
8. Statistical/methodological toolkit
9. Key takeaways (numbered list + concept map mermaid)
10. Exercises (callout-caution, 3-4 problems)
```

### YAML Front Matter Template

```yaml
---
title: "Chapter N: Title"
subtitle: "A Study Guide for *Mastering 'Metrics* by Angrist & Pischke"
format:
  html:
    toc: true
    toc-depth: 3
    code-tools: true
    number-sections: true
    theme: cosmo
    self-contained: true
execute:
  warning: false
  message: false
---
```

### Pedagogical Flow Rules

- **ALWAYS start with the motivating question**, not the theory. Hook the student first.
- **Show data before theory.** Let students see the empirical puzzle, THEN introduce the framework that explains it.
- **Explain "regression on a dummy" early.** Remind students that regressing Y on D gives: intercept = control mean, coefficient = difference, SE = precision.
- **Every table must be followed by an interpretation** in a callout box or prose paragraph.
- **Add transition sentences** between every major section to maintain narrative flow.
- **Add a mini-summary** ("What did we learn?") after each case study.

### Code Block Rules

**Data loading blocks** (just `pd.read_csv`):
- Plain inline code, NO `code-fold`, NO `#| label:`, NO `#| tbl-cap:`
- Example:
```
  ```{python}
  # Load pre-cleaned data
  df = pd.read_csv("../data/chN/filename.csv")
  ```
```

**Analysis blocks** (regressions, tables):
- Always visible (no code-fold)
- MUST have `#| label: tbl-descriptive-name` for table numbering
- MUST have `#| tbl-cap: "Descriptive title"` (do NOT use book table numbers like "Table 3.1")
- Add `#` comments explaining each step
- Use `statsmodels.formula.api` as `smf` for regressions
- Use `linearmodels.iv.IV2SLS` for instrumental variables
- Avoid advanced Python: no f-string format specs like `:+.2f`, no complex comprehensions
- Keep each block under 25 lines

**When clustering standard errors**, add a brief explanatory note the first time clustering appears in the chapter (e.g., "We cluster by family because family members share the same treatment").

### Mermaid Diagram Rules

CRITICAL — follow these rules exactly to avoid rendering failures:

1. Use `graph TD` or `graph LR` — do NOT use `flowchart`
2. Use `["quoted text"]` for all node labels
3. **NEVER** put numbered lists inside nodes (e.g., `1.`, `2.`) — mermaid parses them as markdown lists and shows "Unsupported markdown: list"
4. **NEVER** use `\n` or `<br/>` for line breaks inside nodes — keep each node's text on a single line
5. Always include `%%| label: fig-*` and `%%| fig-cap: "Title"`
6. Style every node with explicit `fill:` and `color:` for readability
7. Maximum 8-10 nodes per diagram
8. When comparing two things side-by-side, prefer a **markdown table** over mermaid subgraphs (subgraph styling is unreliable)

**Good example:**
```
  ```{mermaid}
  %%| label: fig-example
  %%| fig-cap: "How the method works"

  graph TD
      A["Start with a causal question"] --> B["Identify the problem"]
      B --> C["Apply the method"]
      C --> D["Interpret results"]

      style A fill:#3498db,color:#fff
      style B fill:#e67e22,color:#fff
      style C fill:#8e44ad,color:#fff
      style D fill:#2d8659,color:#fff
  ```
```

**Bad example (will break):**
```
  graph TD
      A[1. First step\nDo something] --> B[2. Second step]
```

### Callout Box Usage

| Type | Use For |
|------|---------|
| `callout-tip` | Learning objectives, how-to-read guides |
| `callout-note` | Methodological explanations, definitions |
| `callout-important` | Key findings, surprising results |
| `callout-warning` | Pitfalls, red flags (like selection bias) |
| `callout-caution` | Exercises |

### Copyright and Originality Rules

- **All text must be original paraphrases.** Never copy sentences from the book.
- **Create new examples** instead of using the book's character names or specific stories.
- **Tables reproduced from public data** using our own code is standard academic practice.
- **Historical facts** (Daniel, Lind, Fisher, etc.) are general knowledge — paraphrase freely.
- **Reference the original authors** when summarizing published findings (e.g., "Finkelstein et al., 2012").

## Phase 4: Render and Verify

1. Run: `quarto render notebooks_quarto/NN-chapter-name.qmd`
2. Verify all Python code cells execute without error
3. Verify key numerical results match the book's published tables
4. Check that all mermaid diagrams render correctly (no "Unsupported markdown" errors)
5. Check that all tables have numbered captions

## Color Palette for Diagrams

Use these colors consistently across all chapters:

| Purpose | Color | Hex |
|---------|-------|-----|
| Question / Starting point | Blue | `#3498db` |
| Problem / Bias / Warning | Red | `#c0392b` |
| Confounders / Caution | Orange | `#e67e22` |
| Solution / Method | Purple | `#8e44ad` |
| Result / Outcome / Success | Green | `#2d8659` |
| Neutral / Context | Dark gray | `#2c3e50` |

Always use `color:#fff` (white text) with these fills.
