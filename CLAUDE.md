# CLAUDE.md — Project Guide for Claude Code

## Project Overview

This is a **pedagogical causal inference project** built around *Mastering 'Metrics* by Angrist & Pischke. It provides Quarto study guides with embedded Python code that replicate the book's key empirical results. The target audience is first-year students encountering econometrics for the first time.

## Key Directories

| Path | Purpose |
|------|---------|
| `notebooks_quarto/*.qmd` | **Study guides** — the main deliverable. Quarto documents with prose, code, and mermaid diagrams. |
| `data/chN/*.csv` | **Clean datasets** — ready for analysis. Loaded by the study guides. |
| `data/chN/*.dta` | Raw Stata files (not in git — too large). Downloaded from masteringmetrics.com. |
| `code/python/chN/prepare_data.py` | Data prep scripts: raw `.dta` → clean `.csv`. |
| `code/python/chN/*.py` | Standalone Python replication scripts (one per table/figure). |
| `code/stata/chN/*.do` | Original Stata do files from the book's website. |
| `original-book/*.md` | Chapter text in markdown (reference material). |
| `.claude/skills/study-guide/` | Custom `/study-guide` skill for generating new chapters. |

## Tech Stack

- **Python 3.12+** with `uv` for package management
- **Quarto** for rendering `.qmd` → `.html`
- **statsmodels** (`smf.ols`, `smf.wls`) for OLS, WLS, clustered SEs
- **linearmodels** (`IV2SLS.from_formula`) for instrumental variables / 2SLS
- **matplotlib** + **seaborn** for plots
- **pandas** for data manipulation

## Commands

```bash
# Install dependencies
uv sync

# Run a data preparation script
uv run python code/python/ch1/prepare_data.py

# Render a study guide
uv run quarto render notebooks_quarto/01-randomized-trials.qmd

# Render all study guides
for f in notebooks_quarto/*.qmd; do uv run quarto render "$f"; done
```

## Coding Conventions

### Study Guides (.qmd files)

- **Structure**: Learning objectives → roadmap mermaid → motivating question → data → theory → case studies with code → historical perspective → key takeaways with concept map → exercises
- **Data loading**: Plain inline `pd.read_csv(...)` followed by `df.head(3)`. No `code-fold`, no `#| label:`, no `#| tbl-cap:` on load blocks.
- **Analysis code**: Always visible (never folded). Must have `#| label: tbl-*` or `fig-*` and `#| tbl-cap:` or `fig-cap:`. Must include `#` comments explaining each step.
- **Equations**: Use standard math notation ($Y$, $D$, $\rho$) with an explicit bridge to the code variable names in surrounding text (e.g., "where $Y_{st}$ is the death rate (`mrate`)").
- **Regression**: Use `smf.ols()` / `smf.wls()` for OLS. Use `IV2SLS.from_formula()` for IV. Always specify `cov_type` for robust or clustered SEs.
- **Copyright**: All text must be original paraphrases — never copy from the book. Create new examples instead of using the book's character names.

### Mermaid Diagrams (critical rules)

- Use `graph TD` or `graph LR` — **never** `flowchart`
- Use `["quoted text"]` for all node labels
- **NEVER** put numbered lists (`1.`, `2.`) inside nodes — mermaid parses them as markdown lists and shows "Unsupported markdown: list"
- **NEVER** use `\n` or `<br/>` inside nodes — keep text on one line
- Always include `%%| label: fig-*` and `%%| fig-cap: "Title"`
- Style every node: `style A fill:#3498db,color:#fff`
- Max 8–10 nodes per diagram
- When comparing two things side-by-side, prefer a markdown table over mermaid subgraphs

### Color Palette (for mermaid diagrams)

| Purpose | Hex | Usage |
|---------|-----|-------|
| Question / Starting point | `#3498db` | Blue |
| Problem / Bias / Warning | `#c0392b` | Red |
| Confounders / Caution | `#e67e22` | Orange |
| Solution / Method | `#8e44ad` | Purple |
| Result / Outcome | `#2d8659` | Green |
| Neutral / Context | `#2c3e50` | Dark gray |

Always use `color:#fff` (white text) with these fills.

### Callout Box Types

| Type | Use For |
|------|---------|
| `callout-tip` | Learning objectives, how-to-read guides |
| `callout-note` | Methodological explanations, definitions, syntax guides |
| `callout-important` | Key findings, surprising results |
| `callout-warning` | Pitfalls, selection bias red flags |
| `callout-caution` | Exercises |

## Custom Skills

### `/study-guide [chapter-number]`

Generates a complete Quarto study guide for a chapter. Reads the original chapter text, existing Python scripts, and data files. Follows all the conventions above. See `.claude/skills/study-guide/SKILL.md` for the full specification.

## Data Flow

```
Raw .dta files (not in git)
    ↓ code/python/chN/prepare_data.py
Clean .csv files (in git, in data/chN/)
    ↓ loaded by notebooks_quarto/NN-chapter.qmd
Rendered .html (not in git, in notebooks_quarto/)
```

Students only need the clean CSVs (already in the repo). The `.dta` files are only needed if rebuilding from scratch.

## What Not To Do

- Do not add `.dta` files to git (they are too large; listed in `.gitignore`)
- Do not add rendered `.html` files to git (regenerated from `.qmd`)
- Do not use book table numbers in study guide captions (e.g., say "Causal effects of insurance on health" not "Table 1.4b")
- Do not use `flowchart` in mermaid — always use `graph`
- Do not put complex data wrangling in the `.qmd` files — keep it in `prepare_data.py` and load clean CSVs
