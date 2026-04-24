# Project Status

*Last updated: 2026-04-24*

## Study Guides: Complete

All six chapters have full Quarto study guides with Python code, mermaid diagrams, and exercises.

| Chapter | File | Status | Code | Data |
|:---|:---|:---:|:---:|:---:|
| 1. Randomized Trials | `notebooks_quarto/01-randomized-trials.qmd` | Complete | NHIS, RAND HIE regressions | `data/ch1/*.csv` |
| 2. Regression | `notebooks_quarto/02-regression.qmd` | Complete | Simulated OVB demo | Simulated (in-notebook) |
| 3. Instrumental Variables | `notebooks_quarto/03-instrumental-variables.qmd` | Complete | MDVE cross-tabulation, IV recipe | `data/ch3/*.csv` |
| 4. Regression Discontinuity | `notebooks_quarto/04-regression-discontinuity.qmd` | Complete | MLDA RD regressions + plots | `data/ch4/*.csv` |
| 5. Differences-in-Differences | `notebooks_quarto/05-differences-in-differences.qmd` | Complete | Banks DD, MLDA regression DD | `data/ch5/*.csv` |
| 6. Wages of Schooling | `notebooks_quarto/06-wages-of-schooling.qmd` | Complete | Twins IV, QOB IV, sheepskin RD | `data/ch6/*.csv` |

## Features per Chapter

Each study guide includes:

- Learning objectives (callout-tip)
- Visual roadmap (mermaid diagram)
- Motivating real-world question
- Case studies with: research question, challenge, data description, method, analysis, interpretation, lessons
- Pedagogical enrichment: intuition builders, common misconceptions, method comparisons, policy connections, cross-chapter links
- Historical perspective (Masters of 'Metrics)
- Statistical inference toolkit (Ch1) or method-specific toolkit
- Concept map (mermaid diagram)
- Exercises: multiple choice (Ch4-6), conceptual questions (5+), research tasks (3+)
- Full solutions with executable Python code

## Data Pipeline

```
Raw .dta files (not in git, from masteringmetrics.com)
    ↓ code/python/chN/prepare_data.py
Clean .csv files (in git, data/chN/)
    ↓ loaded by notebooks_quarto/NN-*.qmd
Rendered HTML (not in git)
```

## Python Scripts

| Script | Purpose |
|:---|:---|
| `code/python/ch1/prepare_data.py` | NHIS + RAND .dta → 4 clean CSVs |
| `code/python/ch3/prepare_data.py` | MDVE .dta → 1 clean CSV |
| `code/python/ch4/prepare_data.py` | AEJfigs .dta → 1 clean CSV |
| `code/python/ch5/prepare_data.py` | banks.csv + deaths.dta → 2 clean CSVs |
| `code/python/ch6/prepare_data.py` | twins + ak91 + sheepskin .dta → 3 clean CSVs |
| `code/python/ch*/table*.py` | Standalone replication scripts (12 total) |

## Quality Passes Completed

1. **Structure**: All chapters follow the study-guide skill template
2. **Code simplification**: Data wrangling separated from analysis; clean CSVs loaded directly
3. **Mermaid fixes**: All diagrams use `graph TD/LR`, `["quoted text"]`, styled nodes
4. **Equation audit**: Consistent math notation with code-variable bridges
5. **Case study enrichment**: Research question, challenge, data, method, lessons, limitations for all 12 case studies
6. **Pedagogical enrichment**: 28+ content blocks added (intuition builders, misconceptions, method comparisons, policy connections, cross-chapter links)
7. **Readability rewrite**: Short sentences, active voice, bold keywords, signpost phrases, bullet points, white space

## Custom Skill

`/study-guide [chapter-number]` — generates a new chapter following all conventions. See `.claude/skills/study-guide/SKILL.md`.

## AI Tutors

5 Google Gemini Gems with distinct pedagogical approaches. See `tutors.html` and `tutors/*.md`.

| Tutor | Style | Color | System Prompt |
|:---|:---|:---:|:---|
| Learning Coach | Step-by-step guidance | Blue | `tutors/learning-coach.md` |
| Socratic Challenger | Question-based critical thinking | Purple | `tutors/socratic-challenger.md` |
| Code-First Experimenter | Hands-on Python coding | Green | `tutors/code-first.md` |
| Exam Coach | Test preparation and drills | Yellow | `tutors/exam-coach.md` |
| Case-Study Explainer | Institutional context and policy analysis | Orange | `tutors/case-study-explainer.md` |

## Known Limitations

- **Chapter 2** uses simulated data (no replication data available from the book's website)
- **Chapter 3** has limited code (only MDVE cross-tab; KIPP and family size are narrative)
- **Chapter 6** child labor IV (AA_small.dta) is too large for in-notebook analysis; results described narratively
- Raw `.dta` files not in git (too large); must be downloaded separately
- `pubtwins.dta` requires manual download from Princeton DataSpace (captcha)
