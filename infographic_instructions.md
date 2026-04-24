# The Furious Five: Infographic Instructions for Gemini

> **Purpose:** Hero image for the Mastering Causal Metrics website. Must match the site's dark-mode palette.

---

## Prompt for Gemini (copy and paste this)

Create a wide 1920×1080 infographic with a dark navy background (#0f172a).

**Title at the top center:** "THE FURIOUS FIVE" in large bold sky blue (#38bdf8) text with a subtle glow. Below it, a smaller subtitle in gray (#94a3b8): "Five Methods to Separate Cause from Correlation."

**Layout:** Five cards arranged in a single horizontal row across the middle of the image. Each card is a dark rounded rectangle (#1e293b) with a colored top border stripe and generous spacing between cards. Each card contains: a number, a method name, a small signature graph, the key equation, and one sentence about the key assumption.

**Card 1 — RCT (sky blue #38bdf8 top stripe):**
- Large "1" and title "RCT" in sky blue
- Small graph: two groups (Treatment and Control) shown as two simple bar charts side by side, same height baseline, treatment bar slightly taller
- Equation in white text: "ATE = E[Y₁] − E[Y₀]"
- Assumption in small gray text: "Random assignment eliminates selection bias"

**Card 2 — REGRESSION (soft purple #a78bfa top stripe):**
- Large "2" and title "OLS" in purple
- Small graph: a scatter plot with a fitted regression line through the dots, showing a positive slope
- Equation in white text: "Y = α + βX + ε"
- Assumption in small gray text: "All confounders are observed and controlled"

**Card 3 — IV (emerald green #34d399 top stripe):**
- Large "3" and title "IV" in green
- Small graph: a flow diagram with three nodes — Z (instrument) with an arrow to D (treatment) with an arrow to Y (outcome), and a crossed-out dashed arrow from Z directly to Y
- Equation in white text: "β_IV = Cov(Y,Z) / Cov(D,Z)"
- Assumption in small gray text: "Instrument affects Y only through D"

**Card 4 — RD (warm orange #f5a623 top stripe):**
- Large "4" and title "RD" in orange
- Small graph: a scatter plot with a vertical dashed line at a cutoff point, and a clear discontinuous jump in the outcome at the cutoff — dots on the left side are lower, dots on the right side jump up
- Equation in white text: "τ = lim Y⁺ − lim Y⁻"
- Assumption in small gray text: "No manipulation of the running variable"

**Card 5 — DD (red #f87171 top stripe):**
- Large "5" and title "DD" in red
- Small graph: two lines over time — a solid line (treated group) and a dashed line (control group) that run parallel before a vertical dashed line marking the treatment, then the solid line diverges upward after treatment
- Equation in white text: "δ = (Y_T,post − Y_T,pre) − (Y_C,post − Y_C,pre)"
- Assumption in small gray text: "Parallel trends in the absence of treatment"

**Bottom center:** A single line in white text: "When all five methods agree, the finding is real." Below it in smaller gray: "Mastering Causal Metrics — An AI-Powered Study Guide"

**Style notes:** Clean, modern, minimal. Thin line-art style for all graphs (no filled areas, no 3D). White (#e2e8f0) lines and text on the dark background. Each mini-graph should be simple and iconic — just enough to recognize the method at a glance. No photographs, no emojis, no chalkboard textures. The overall feel should be like a polished dark-mode tech dashboard.

---

## Alternative: Condensed One-Paragraph Prompt

Create a wide 1920x1080 dark navy (#0f172a) infographic titled "THE FURIOUS FIVE" in glowing sky blue (#38bdf8). Five dark cards (#1e293b) in a horizontal row, each with a colored top stripe and a signature mini-graph in thin white lines. Card 1 (blue stripe): "RCT" with two comparison bars, equation "ATE = E[Y₁] − E[Y₀]". Card 2 (purple #a78bfa stripe): "OLS" with scatter plot and regression line, equation "Y = α + βX + ε". Card 3 (green #34d399 stripe): "IV" with Z→D→Y flow diagram, equation "β = Cov(Y,Z)/Cov(D,Z)". Card 4 (orange #f5a623 stripe): "RD" with discontinuity jump at a cutoff, equation "τ = lim Y⁺ − lim Y⁻". Card 5 (red #f87171 stripe): "DD" with parallel trends diverging after treatment, equation "δ = ΔY_T − ΔY_C". Bottom text: "When all five methods agree, the finding is real." Clean minimal style, thin line art, no photos, no 3D, dark-mode tech dashboard aesthetic.

---

## Visual Reference: What Each Mini-Graph Shows

| Method | Signature Graph | What to Draw |
|--------|----------------|--------------|
| **RCT** | Two-group comparison | Two vertical bars side by side: "Control" and "Treatment." Treatment bar is taller. Simple difference. |
| **OLS** | Scatter + regression line | Cloud of dots with a straight line fitted through them, positive slope. |
| **IV** | Causal flow diagram | Three circles labeled Z, D, Y connected by arrows: Z→D→Y. A dashed arrow from Z to Y is crossed out (X). |
| **RD** | Discontinuity at cutoff | Dots following a smooth curve, then a sharp vertical jump at a dashed cutoff line. Left side lower, right side higher. |
| **DD** | Parallel trends | Two lines over time. Both parallel before a dashed vertical "treatment" line. After treatment, one line (solid) diverges upward while the other (dashed) continues flat. |

---

## Color Palette

| Element | Hex | Usage |
|---------|-----|-------|
| Background | #0f172a | Deep navy canvas |
| Cards | #1e293b | Dark card surface |
| Text | #e2e8f0 | Light gray body text |
| Muted text | #94a3b8 | Subtitles, assumptions |
| RCT accent | #38bdf8 | Sky blue |
| OLS accent | #a78bfa | Soft purple |
| IV accent | #34d399 | Emerald green |
| RD accent | #f5a623 | Warm orange |
| DD accent | #f87171 | Soft red |
