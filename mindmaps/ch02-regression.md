# 2. Regression

## Act I · The Question

- Is an elite private college worth the extra tuition?
  - Roughly $20,000 more per year than a public university
  - Graduates of top private schools earn substantially more
- Naive evidence: a raw earnings gap
  - Private-school students differ: smarter, more motivated, better connected
  - No coin flip at the admissions office → no experiment
- Vocabulary for the chapter
  - Control variable, ceteris paribus
  - Short vs. long regression
  - Omitted variables bias (OVB)
  - Conditional independence assumption (CIA)

## Act II · The Investigation

- The problem: selection without randomization
  - Same selection bias as Chapter 1, but no lottery to fix it
  - Regression as automated matching: similar on paper, different choice
- The tool: regression with controls
  - Model: $Y_i = \alpha + \beta P_i + \gamma X_i + e_i$
  - OLS: minimize the sum of squared residuals
  - From a Chapter 1 dummy to an "other things equal" comparison
  - Identifying assumption: CIA, treatment as good as random given controls
- Simulation lab: OVB with a known truth
  - Design: 1,000 simulated students, ability drives private choice, true effect $5,000
  - Short regression (no ability): estimate well above $5,000
  - Long regression (with ability): back to about $5,000
- The OVB formula
  - $\text{OVB} = \beta^s - \beta^l = \pi_1 \times \gamma$; zero if either factor is zero
  - Auxiliary regression: omitted variable on treatment gives $\pi_1$
  - Simulation check: formula reproduces short minus long exactly
  - Sign table: predict the direction of bias without seeing the confounder
- Case study: Dale and Krueger, the private college premium
  - Data: College and Beyond, 14,000+ students (not public)
  - Self-revelation design: same admission set, different enrollment choice
  - No controls: private premium about 14%
  - Barron's selectivity controls: about 7%
  - Application-set controls: close to zero
- Sensitivity analysis
  - Adding SAT, parental income, demographics barely moves the estimate
  - Why: given application behavior, $\pi_1 \approx 0$ for these traits
- The danger: bad controls
  - Post-treatment variables (occupation) block the causal channel
  - Rule: control only for pre-treatment traits; revisited in Chapter 6
- Regression across the book
  - Building block for RCTs, IV, RD, DD, and returns to schooling
  - Roots: Galton 1886 (regression to the mean), Yule 1899 (pauperism controls)

## Act III · The Resolution

- Devil's advocate
  - "Elite graduates earn more, so elite college pays" → mostly selection
  - "Just add more controls" → only pre-treatment confounders help; bad controls add bias
- Takeaways
  - Regression compares treated and untreated with the same controls
  - OVB = $\pi_1 \times \gamma$; signs predict the direction
  - Stable estimates across specifications build confidence
  - Never control for outcomes of the treatment
  - Private college premium largely vanishes with the right controls
- Thesis: regression delivers causal effects only when the right pre-treatment controls make treatment as good as random
