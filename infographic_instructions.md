# The Furious Five: Causal Inference Methods — Infographic Instructions

## Section A: Full Image Prompt

Create a 1920 by 1080 pixel chalkboard-style infographic illustration titled "THE FURIOUS FIVE: Does Education Cause Higher Earnings?" rendered entirely as hand-drawn chalk on a dark slate chalkboard surface colored #1a1a2e. The title appears centered at the top in large warm white chalk lettering (#f0ece2) with a subtle chalk dust halo, and below it a guiding question in smaller italic chalk reads "Five methods, one question — and they all converge on the same answer." A faint decorative chalk line separates the title from the six content panels arranged in a 3 by 2 grid below, each panel enclosed in a steel blue (#4a90d9) chalk-drawn border with slightly uneven hand-drawn edges.

Panel 1, top-left, is titled "THE QUESTION" in warm orange chalk (#f5a623). A chalk-drawn icon of a graduation cap with a dollar sign sits in the upper-left corner. The body text in warm white chalk reads "Does education cause higher earnings? College graduates earn 2x more — but is it causation or selection?" Below this, a small chalk-drawn scatter plot shows a positive slope between "Years of Schooling" on the x-axis and "Log Earnings" on the y-axis, with a dashed line labeled "Correlation?" in muted red (#d94a4a). A callout box outlined in muted red chalk reads "Ability Bias: smarter people get more school AND earn more" with the formula "OLS bias = γ × π₁" sketched beneath it.

A chalk-drawn connector arrow flows rightward from Panel 1 to Panel 2 with the transition phrase "The gold standard" in muted gray chalk. Panel 2, top-center, is titled "RCT: RANDOM ASSIGNMENT" in teal chalk (#00d4c8). A chalk-drawn icon of a dice shows randomization. The body explains "Randomly assign scholarships (Z). The offer shifts schooling (S) but is independent of ability." The key equation "Wald = Reduced Form / First Stage" appears in warm white chalk, and below it a small two-column comparison shows "Scholarship: +2 yrs schooling → +0.16 earnings" with the result "Per-year return ≈ 0.08" highlighted in warm orange. A callout reads "Unbiased by construction — no confounders."

A connector arrow flows rightward to Panel 3 with "But we can't randomize education..." in muted gray. Panel 3, top-right, is titled "OLS: THE BIASED BASELINE" in warm orange chalk. A chalk-drawn icon of a regression line with a question mark sits in the corner. The equation "ln(W) = α + ρ·S + ε" appears prominently, with "ρ ≈ 0.07" in large warm orange numerals. Below, a chalk-drawn OVB diagram shows two arrows — one from "Ability" to "Schooling" and one from "Ability" to "Earnings" — converging on the estimate, labeled "Omitted Variable Bias." A callout in muted red reads "~7% raw return — but how much is causal?"

A connector arrow flows downward from Panel 3 to Panel 4 with "Use exogenous variation instead" in muted gray. Panel 4, bottom-left, is titled "IV: QUARTER OF BIRTH" in teal chalk. A chalk-drawn icon of a calendar with a baby footprint represents the instrument. The equation "Wald = Cov(Y,Z) / Cov(D,Z)" appears in warm white, and a small chalk diagram shows the causal chain "Z (birth quarter) → S (schooling) → W (earnings)" with a crossed-out direct arrow from Z to W labeled "Exclusion restriction." The estimate "LATE ≈ 0.07" appears in warm orange, with a note "Effect for compliers — students at the dropout margin." A callout reads "Quarter of birth shifts schooling but not ability."

A connector arrow flows rightward to Panel 5 with "Two more angles" in muted gray. Panel 5, bottom-center, is titled "RD & DD: LOCAL EVIDENCE" in steel blue chalk. This panel is split vertically. The left half shows a chalk-drawn RD plot — a scatter with a sharp cutoff line at x=0, a clear jump in "Diploma Receipt" but a flat line for "Earnings" — labeled "Sheepskin RD: credential effect ≈ $0." The right half shows a chalk-drawn parallel trends diagram with two lines diverging after a vertical dashed line labeled "Reform," with "Treated states" solid and "Control states" dashed, and the result "Wald-DiD ≈ 0.08" in warm orange. A callout reads "Learning matters — not the diploma."

A connector arrow flows rightward to Panel 6 with "The punchline" in muted gray. Panel 6, bottom-right, is titled "CONVERGENCE: 7–10%" in large warm orange chalk with a chalk glow effect. A chalk-drawn icon of five hands joining in a fist bump represents the five methods agreeing. A compact summary table lists "RCT ~8% | OLS ~7% | IV ~7% | RD ~$0 | DD ~8%" with all numbers in warm orange. Below the table, the conclusion reads "True causal return to schooling: 7–10% per year" in warm white, and "Education works through learning, not just credentials" in teal. A callout in teal reads "When five methods agree, the finding is real."

In the margins around the six panels, faint background formulas at 15 to 20 percent opacity are scattered: "E[Y₁-Y₀|D=1]", "β = (X'X)⁻¹X'Y", "Pr(D=1|Z)", and "δ_DD". A small chalk-drawn note in the bottom-right margin reads "Based on Mastering 'Metrics by Angrist & Pischke" with a chalk-drawn book icon. Subtle chalk dust particles, smudge marks, and eraser traces add atmospheric authenticity throughout the composition.

---

## Section B: Negative Prompt

Avoid photorealistic rendering, glossy or reflective surfaces, drop shadows, gradient color fills, emojis or Unicode symbols, 3D perspective effects, lens flare, bokeh, or photographic depth of field. Do not use perfectly straight lines or computer-generated typography — all text and lines must appear hand-drawn with natural chalk variation in thickness and opacity. Replace pure white (#ffffff) with warm white (#f0ece2) throughout. Avoid stock photo elements, clip art, or vector-perfect icons. Do not include any real photographs of people, classrooms, or universities. Avoid neon colors, metallic effects, or any surface that appears wet, glossy, or digitally polished.

---

## Section C: Condensed Prompt (~300 words)

Chalkboard infographic, 1920x1080, hand-drawn chalk on dark slate (#1a1a2e). Title: "THE FURIOUS FIVE: Does Education Cause Higher Earnings?" in warm white (#f0ece2) with chalk dust halo. Six panels in 3x2 grid, steel blue (#4a90d9) chalk borders.

Panel 1 top-left: "THE QUESTION" in orange (#f5a623). Graduation cap icon. Scatter plot showing schooling vs earnings correlation. Callout: "Ability Bias: OLS bias = γ × π₁" in red (#d94a4a).

Panel 2 top-center: "RCT: RANDOM ASSIGNMENT" in teal (#00d4c8). Dice icon. Equation: Wald = RF/FS. Result: "Per-year return ≈ 0.08" in orange. Callout: "Unbiased by construction."

Panel 3 top-right: "OLS: THE BIASED BASELINE" in orange. Regression line icon. Equation: ln(W) = α + ρS + ε, "ρ ≈ 0.07" large orange. OVB diagram with ability arrows. Callout: "~7% raw return — how much is causal?"

Panel 4 bottom-left: "IV: QUARTER OF BIRTH" in teal. Calendar icon. Equation: Wald = Cov(Y,Z)/Cov(D,Z). Causal chain Z→S→W. "LATE ≈ 0.07" in orange. Callout: "Birth quarter shifts schooling, not ability."

Panel 5 bottom-center: "RD & DD: LOCAL EVIDENCE" in blue. Split panel — left: RD plot with flat earnings at cutoff, "credential ≈ $0"; right: parallel trends diverging, "Wald-DiD ≈ 0.08" orange. Callout: "Learning matters — not the diploma."

Panel 6 bottom-right: "CONVERGENCE: 7–10%" in large orange with glow. Fist bump icon. Summary: RCT~8%, OLS~7%, IV~7%, RD~$0, DD~8%. Conclusion: "True return: 7–10%/year" white, "Learning, not credentials" teal.

Margins: faint formulas at 15-20% opacity. Bottom-right: "Based on Mastering 'Metrics." Chalk dust, smudge marks, eraser traces throughout. No glossy surfaces, no emojis, no straight computer lines.

---

## Section D: Structured Panel Reference

### Panel 1 — THE QUESTION
- **Icon**: Graduation cap with dollar sign
- **Headline**: Does education cause higher earnings?
- **Key number**: College grads earn 2× more
- **Visualization**: Scatter plot (schooling vs log earnings, positive slope)
- **Callout**: "Ability Bias: OLS bias = γ × π₁"
- **Color accent**: Muted red (#d94a4a) for bias warning

### Panel 2 — RCT: RANDOM ASSIGNMENT
- **Icon**: Dice (randomization)
- **Headline**: The gold standard — random assignment breaks selection
- **Key number**: Per-year return ≈ 0.08
- **Visualization**: Two-column comparison (scholarship vs no scholarship)
- **Callout**: "Unbiased by construction — no confounders"
- **Color accent**: Teal (#00d4c8)

### Panel 3 — OLS: THE BIASED BASELINE
- **Icon**: Regression line with question mark
- **Headline**: Simple regression captures correlation, not causation
- **Key number**: ρ ≈ 0.07
- **Visualization**: OVB diagram (Ability → Schooling, Ability → Earnings)
- **Callout**: "~7% raw return — but how much is causal?"
- **Color accent**: Warm orange (#f5a623)

### Panel 4 — IV: QUARTER OF BIRTH
- **Icon**: Calendar with baby footprint
- **Headline**: Exogenous variation isolates the causal effect
- **Key number**: LATE ≈ 0.07
- **Visualization**: Causal chain diagram (Z → S → W, crossed-out Z → W)
- **Callout**: "Quarter of birth shifts schooling but not ability"
- **Color accent**: Teal (#00d4c8)

### Panel 5 — RD & DD: LOCAL EVIDENCE
- **Icon**: Split — cutoff line (RD) and parallel lines (DD)
- **Headline**: Diploma has no value; policy reforms confirm returns
- **Key numbers**: Credential effect ≈ $0; Wald-DiD ≈ 0.08
- **Visualization**: Left: RD plot (jump in diploma, flat earnings). Right: Parallel trends diverging after reform
- **Callout**: "Learning matters — not the diploma"
- **Color accent**: Steel blue (#4a90d9)

### Panel 6 — CONVERGENCE: 7–10%
- **Icon**: Five hands in a fist bump
- **Headline**: Five methods, one answer
- **Key numbers**: RCT ~8%, OLS ~7%, IV ~7%, RD ~$0, DD ~8%
- **Visualization**: Compact summary table with all estimates
- **Callout**: "When five methods agree, the finding is real"
- **Color accent**: Warm orange (#f5a623) with teal conclusion

### Connector Arrows (between panels)
- Panel 1 → 2: "The gold standard"
- Panel 2 → 3: "But we can't randomize education..."
- Panel 3 → 4: "Use exogenous variation instead"
- Panel 4 → 5: "Two more angles"
- Panel 5 → 6: "The punchline"

### Color Palette Reference
| Element | Hex | Usage |
|---------|-----|-------|
| Chalkboard background | #1a1a2e | Dark slate surface |
| Body text | #f0ece2 | Warm white chalk |
| Key numbers | #f5a623 | Warm orange emphasis |
| Method highlights | #00d4c8 | Teal for causal methods |
| Panel borders | #4a90d9 | Steel blue frames |
| Bias warnings | #d94a4a | Muted red alerts |
| Transitions | #888888 | Muted gray connector text |
| Background formulas | #f0ece2 at 15-20% | Atmospheric math |
