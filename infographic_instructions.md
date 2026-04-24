# The Furious Five: Causal Inference Methods — Infographic Instructions

> **Purpose:** This infographic will serve as the hero image of the Mastering Causal Metrics website. The color palette and visual style must match the site's dark-mode identity: deep navy background (#0f172a), sky blue (#38bdf8) for primary accents, soft purple (#a78bfa) for secondary accents, emerald green (#34d399) for success states, and warm orange (#f5a623) for key numbers.

## Section A: Full Image Prompt

Create a 1920 by 1080 pixel premium dark-mode infographic illustration titled "THE FURIOUS FIVE" with subtitle "Does Education Cause Higher Earnings?" The background is a rich deep navy (#0f172a) with a very subtle noise texture and faint geometric grid lines at 5 percent opacity to create depth. The title "THE FURIOUS FIVE" appears centered at the top in bold sky blue (#38bdf8) lettering with a soft luminous glow effect, and the subtitle below in lighter muted slate (#94a3b8) italic reads "Five methods, one question — and they all converge on the same answer." A thin horizontal gradient line in soft purple (#a78bfa) fading to transparent separates the title from the six content panels arranged in a 3 by 2 grid below. Each panel sits inside a dark card (#1e293b) with rounded corners and a thin border, with a color-coded top accent stripe indicating its method.

Panel 1, top-left, has a sky blue (#38bdf8) top stripe and is titled "THE QUESTION" in sky blue. A minimalist icon of a graduation cap with a question mark rendered in thin sky blue lines sits beside the title. The body text in light gray (#e2e8f0) reads "Does education cause higher earnings? College graduates earn 2× more — but is it causation or selection?" Below, a small stylized scatter plot rendered in thin glowing dots shows a positive slope between "Years of Schooling" on the x-axis and "Log Earnings" on the y-axis, with a dashed trend line. A highlighted callout card with a subtle red-tinted background (#c0392b at 15 percent opacity) and a thin red left border reads "Ability Bias: smarter people get more school AND earn more" with the formula "OLS bias = γ × π₁" in warm orange (#f5a623).

A subtle connector line with a small arrow flows rightward from Panel 1 to Panel 2, with the transition phrase "The gold standard" in muted slate text. Panel 2, top-center, has an emerald green (#34d399) top stripe and is titled "RCT: RANDOM ASSIGNMENT" in emerald green. A minimalist dice icon in thin green lines represents randomization. The body explains "Randomly assign scholarships (Z). The offer shifts schooling (S) but is independent of ability." The key equation "Wald = Reduced Form / First Stage" appears in light gray, and a compact result card shows "Per-year return ≈ 0.08" in large warm orange (#f5a623) numerals. A callout with a green-tinted background reads "Unbiased by construction — no confounders."

A connector flows rightward to Panel 3 with "But we can't randomize education..." in muted slate. Panel 3, top-right, has a soft purple (#a78bfa) top stripe and is titled "OLS: THE BIASED BASELINE" in soft purple. A minimalist chart icon with a trend line sits beside the title. The equation "ln(W) = α + ρ·S + ε" appears prominently in light gray, with "ρ ≈ 0.07" in large warm orange below it. A small causal diagram shows arrows from "Ability" to both "Schooling" and "Earnings," illustrating the omitted variable bias path, rendered in thin purple and red lines. A callout with a red-tinted background reads "~7% raw return — but how much is causal?"

A connector flows downward from Panel 3 to Panel 4 with "Use exogenous variation instead" in muted slate. Panel 4, bottom-left, has an emerald green top stripe and is titled "IV: QUARTER OF BIRTH" in emerald green. A minimalist calendar icon with a small footprint represents the instrument. The equation "Wald = Cov(Y,Z) / Cov(D,Z)" appears in light gray, and a clean causal chain diagram shows "Z (birth quarter) → S (schooling) → W (earnings)" with a crossed-out direct arrow from Z to W labeled "Exclusion." The result "LATE ≈ 0.07" appears in warm orange. A callout reads "Effect for compliers — students at the dropout margin."

A connector flows rightward to Panel 5 with "Two more angles" in muted slate. Panel 5, bottom-center, has a sky blue top stripe and is titled "RD & DD: LOCAL EVIDENCE" in sky blue. This panel is visually split. The left half shows a clean RD plot — scattered dots with a vertical cutoff line at x equals zero, a clear jump in "Diploma Receipt" but a flat line for "Earnings" — with the label "Credential effect ≈ $0" in warm orange. The right half shows a parallel trends diagram with two lines (solid for treated states, dashed for control) diverging after a vertical dashed line labeled "Reform," with "Wald-DiD ≈ 0.08" in warm orange. A callout reads "Learning matters — not the diploma."

A connector flows rightward to Panel 6 with "The punchline" in muted slate. Panel 6, bottom-right, has a gradient top stripe blending from sky blue through purple to green, representing all five methods. It is titled "CONVERGENCE: 7–10%" in large warm orange with a subtle outer glow. A minimalist icon of five converging arrows forming a single point represents agreement. A compact horizontal bar chart shows five bars labeled "RCT," "OLS," "IV," "RD," "DD" — the first four clustering around 7 to 8 percent in emerald green, and the RD bar near zero in muted slate with a note "credential only." Below the chart, the conclusion reads "True causal return to schooling: 7–10% per year" in bold light gray, and "Education works through learning, not just credentials" in emerald green. A callout with a green glow reads "When five methods agree, the finding is real."

In the margins and empty spaces around the panels, faint mathematical formulas float at 8 to 12 percent opacity in muted slate: "E[Y₁−Y₀|D=1]," "β = (X'X)⁻¹X'Y," "Pr(D=1|Z)," and "δ_DD." A small attribution line in the bottom-right corner reads "Mastering Causal Metrics — An AI-Powered Study Guide" in muted slate at small size with a subtle book icon. The overall aesthetic is clean, modern, and premium — like a polished dark-mode dashboard, not a literal chalkboard.

---

## Section B: Negative Prompt

Avoid chalkboard textures, literal chalk rendering, chalk dust particles, or any rustic educational aesthetic. Do not use photorealistic rendering, glossy or reflective surfaces, drop shadows with hard edges, emojis or Unicode symbols, 3D perspective effects, lens flare, bokeh, or photographic depth of field. Avoid neon colors that are too bright or saturated — all colors should feel refined and muted against the dark background. Do not use stock photo elements, clip art, or vector-perfect icons with thick outlines. Avoid pure white (#ffffff) text — use warm light gray (#e2e8f0) instead. Do not include real photographs of people, classrooms, or universities. Avoid busy or cluttered compositions — maintain generous whitespace between elements. Do not use gradients that create a shiny or metallic appearance.

---

## Section C: Condensed Prompt (~300 words)

Premium dark-mode infographic, 1920x1080, deep navy background (#0f172a) with subtle noise texture. Title "THE FURIOUS FIVE" in sky blue (#38bdf8) with glow, subtitle "Does Education Cause Higher Earnings?" in muted slate (#94a3b8). Six dark card panels (#1e293b) in 3x2 grid, rounded corners, each with a color-coded top accent stripe.

Panel 1 top-left: blue stripe. "THE QUESTION" in sky blue. Graduation cap icon. Scatter plot with positive slope. Callout: "Ability Bias: OLS bias = γ × π₁" in red-tinted box. Key stat in orange (#f5a623).

Panel 2 top-center: green stripe (#34d399). "RCT: RANDOM ASSIGNMENT." Dice icon. Equation: Wald = RF/FS. Result: "≈ 0.08" in orange. Callout: "Unbiased by construction."

Panel 3 top-right: purple stripe (#a78bfa). "OLS: THE BIASED BASELINE." Chart icon. Equation: ln(W) = α + ρS + ε. "ρ ≈ 0.07" large orange. OVB causal diagram. Callout: "~7% — how much is causal?"

Panel 4 bottom-left: green stripe. "IV: QUARTER OF BIRTH." Calendar icon. Equation: Wald = Cov(Y,Z)/Cov(D,Z). Causal chain Z→S→W. "LATE ≈ 0.07" orange.

Panel 5 bottom-center: blue stripe. "RD & DD: LOCAL EVIDENCE." Split panel — left: RD plot, flat earnings at cutoff, "≈ $0"; right: parallel trends diverging, "Wald-DiD ≈ 0.08" orange. Callout: "Learning, not diploma."

Panel 6 bottom-right: gradient stripe (blue→purple→green). "CONVERGENCE: 7–10%" in large orange with glow. Five converging arrows icon. Horizontal bar chart: RCT~8%, OLS~7%, IV~7%, RD~$0, DD~8%. Conclusion: "True return: 7–10%/year."

Margins: faint formulas at 10% opacity. Bottom-right: "Mastering Causal Metrics." Clean, modern, dark-mode dashboard aesthetic. No chalkboard, no chalk dust, no emojis, no glossy surfaces.

---

## Section D: Structured Panel Reference

### Panel 1 — THE QUESTION
- **Top stripe**: Sky blue (#38bdf8)
- **Icon**: Graduation cap with question mark (thin line art)
- **Headline**: Does education cause higher earnings?
- **Key number**: College grads earn 2× more
- **Visualization**: Scatter plot (schooling vs log earnings, glowing dots, positive slope)
- **Callout**: "Ability Bias: OLS bias = γ × π₁" (red-tinted background)
- **Transition to next**: "The gold standard" →

### Panel 2 — RCT: RANDOM ASSIGNMENT
- **Top stripe**: Emerald green (#34d399)
- **Icon**: Dice (thin line art)
- **Headline**: Random assignment breaks selection bias
- **Key number**: Per-year return ≈ 0.08
- **Visualization**: Two-column comparison (scholarship effect)
- **Callout**: "Unbiased by construction — no confounders"
- **Transition to next**: "But we can't randomize education..." →

### Panel 3 — OLS: THE BIASED BASELINE
- **Top stripe**: Soft purple (#a78bfa)
- **Icon**: Chart with trend line (thin line art)
- **Headline**: Correlation is not causation
- **Key number**: ρ ≈ 0.07
- **Visualization**: OVB causal diagram (Ability → Schooling, Ability → Earnings)
- **Callout**: "~7% raw return — but how much is causal?"
- **Transition to next**: "Use exogenous variation instead" ↓

### Panel 4 — IV: QUARTER OF BIRTH
- **Top stripe**: Emerald green (#34d399)
- **Icon**: Calendar with footprint (thin line art)
- **Headline**: Exogenous variation isolates the causal effect
- **Key number**: LATE ≈ 0.07
- **Visualization**: Causal chain (Z → S → W, crossed-out Z → W)
- **Callout**: "Effect for compliers — students at the dropout margin"
- **Transition to next**: "Two more angles" →

### Panel 5 — RD & DD: LOCAL EVIDENCE
- **Top stripe**: Sky blue (#38bdf8)
- **Icon**: Cutoff line + parallel trends (split)
- **Headline**: Diploma has no value; policy reforms confirm returns
- **Key numbers**: Credential ≈ $0 (RD); Wald-DiD ≈ 0.08 (DD)
- **Visualization**: Left: RD plot (jump in diploma, flat earnings). Right: Parallel trends diverging
- **Callout**: "Learning matters — not the diploma"
- **Transition to next**: "The punchline" →

### Panel 6 — CONVERGENCE: 7–10%
- **Top stripe**: Gradient (blue → purple → green)
- **Icon**: Five converging arrows into one point
- **Headline**: Five methods, one answer
- **Key numbers**: RCT ~8%, OLS ~7%, IV ~7%, RD ~$0, DD ~8%
- **Visualization**: Horizontal bar chart (five bars, green for clustering estimates, slate for RD)
- **Callout**: "When five methods agree, the finding is real" (green glow)

### Connector Arrows
- Panel 1 → 2: "The gold standard"
- Panel 2 → 3: "But we can't randomize education..."
- Panel 3 → 4: "Use exogenous variation instead"
- Panel 4 → 5: "Two more angles"
- Panel 5 → 6: "The punchline"

### Color Palette (Website-Aligned)
| Element | Hex | CSS Variable |
|---------|-----|-------------|
| Background | #0f172a | --bg |
| Card surface | #1e293b | --bg-card |
| Body text | #e2e8f0 | --text |
| Muted text | #94a3b8 | --text-muted |
| Primary accent (blue) | #38bdf8 | --blue |
| Secondary accent (purple) | #a78bfa | --purple |
| Success/method (green) | #34d399 | --green |
| Key numbers (orange) | #f5a623 | — |
| Warning/bias (red) | #c0392b | — |
| Borders | rgba(255,255,255,0.1) | --border |
