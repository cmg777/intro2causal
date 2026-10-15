# Selectable preset: book-dark

Read this only when the user selects the Mastering Causal Metrics book style. It reproduces the approved series while allowing different topics and source-based branch structures.

| Element | Preset |
|---|---|
| Intended use | Opening slide; also a concise chapter overview |
| Audience | First-year students new to econometrics |
| Language | English |
| Density | Main ideas and major concepts; a few equations and verified numbers |
| Canvas | 16:9 landscape; deep navy `#0f172a` |
| Primary accents | Cyan `#38bdf8`, lavender `#a78bfa`, emerald `#34d399` |
| Text | Near-white `#f1f5f9`; secondary slate `#94a3b8` |
| Typography | Clear, professionally typeset Inter-like sans serif; formulas correctly rendered |
| Illustration | Hand-drawn ink contours, restrained hatching and colored fills |
| Topology | Dominant compact center; curved branches radiating in all directions |
| Central content | Chapter number/title, motivating question, small explanatory illustration |
| Branch craft | Short connected labels and relevant mini illustrations; generous space and safe margins |

The selected preset supplies these preferences; verify any remaining run-specific requirements in the interview. No rigid six-branch rule, tiny text to retain every point, panel grid, glow, watermark or invented numerical decoration. Do not confuse the dark accent palette with the darker Mermaid solid-fill palette.

Repository sources: `book/custom.css`, `slides/chNN/site-brand.scss`, `mindmaps/chNN-*.md`, and `book/notebooks_quarto/NN-*.qmd`. Reference examples are the latest accepted `mindmaps/images/chNN-*-vN.png`, inspected before use. Never select by lexicographic version order. Resolve one slug per chapter, rather than choosing an arbitrary file if several match.

Chapter output stem: `chNN-<source-slug>`, matching the existing highest-version image consumers. Other topics use a descriptive lowercase hyphenated stem at the agreed destination. Existing image files outside the accepted folder can be failed drafts; do not use them as style references without checking their status.

Useful explanatory motifs, chosen only when relevant:

- Potential outcomes: alternative paths for the same person, with one unobserved.
- Randomization: a coin/lottery assigning groups, balanced in expectation.
- Confounding: a pre-treatment trait pointing toward both treatment and outcome.
- IV: instrument → treatment → outcome; no alternative outcome channel.
- RD: one threshold, separate fitted limits, a same-cutoff gap and nested bandwidths.
- DD: parallel untreated trends and a treated counterfactual anchored at the intervention date.
- Schooling: books, twins, entry rules, and a diploma effect distinguished from years-of-schooling returns.

The earlier audit at `mindmaps/audit/econometric-audit.txt` is a source of demonstrated pitfalls, not a substitute for auditing a new image or source. Its empirical figures are chapter-specific.
