# 4. Regression Discontinuity Designs

## Act I · The Question

- Does legal access to alcohol raise death rates?
  - US minimum legal drinking age (MLDA) set at 21
  - Other bright lines: voting at 18, Medicare at 65
- The puzzle: rigid rules as a source of experiments
  - Bureaucratic cutoffs seem to remove randomness
  - Yet people just either side of a line are near twins
  - Monthly death rates: a visible step at the 21st birthday
- Vocabulary for the chapter
  - Running variable, cutoff, treatment indicator $D_a$
  - Sharp vs. fuzzy RD
  - Continuity assumption, bandwidth, placebo test

## Act II · The Investigation

- The problem: no overlap at the threshold
  - No age where treated and untreated people coexist
  - Not "controlling for" age: RD extrapolates each side's trend
- The design: sharp RD
  - Ingredients: age as running variable, 21 as cutoff, $D_a$ as switch
  - Deterministic switch: legal access goes from 0% to 100%
  - Continuity: without treatment, outcomes glide smoothly through 21
- The tool: RD regression
  - Plot the data before any regression
  - $M_a = \alpha + \rho D_a + \gamma a + e_a$: $\rho$ = jump, $\gamma$ = age trend
  - Separate fitted lines per side; vertical gap at 21 = effect
- Case study: MLDA and youth mortality
  - Data: monthly age cells, deaths per 100,000, ages 19–22
  - Linear estimate: about 7.7 extra deaths per 100,000
  - Main channel: motor vehicle accidents, 4–6 extra deaths
  - Placebo: internal causes (cancer, heart disease) show no jump
- Robustness toolkit
  - Polynomial order: linear vs. interacted quadratic trends
  - Bandwidth: wide window (19–22) vs. narrow (20–22), comparability vs. precision
  - Verdict: all-cause jump of 7–10 across every specification
- Extension: fuzzy RD
  - Crossing the cutoff raises the probability of treatment, not to certainty
  - Cutoff dummy as instrument; 2SLS = reduced form ÷ first stage
  - Sharp vs. fuzzy: OLS effect vs. LATE for compliers at the cutoff
- Case study: Boston exam schools
  - Admission by test-score cutoff; some decline, some enter by other routes
  - Peer quality jumps 0.8 SD at the cutoff; achievement does not
  - Selective schools' raw advantage looks like selection, not causation
- Interpretation and roots
  - Local effect: valid near the cutoff, not for ages far from it
  - Origins: Thistlethwaite and Campbell (1960), National Merit recognition

## Act III · The Resolution

- Devil's advocate
  - "RD just controls for the running variable" → no overlap exists; it extrapolates, so functional form matters
  - "A jump at 21 proves alcohol kills" → only if other factors stay smooth and placebo outcomes stay flat
- Takeaways
  - Cutoff rules create natural experiments
  - Causal effect = jump at the cutoff net of the smooth trend
  - Plot first, then vary polynomial and bandwidth
  - Placebo outcomes guard the design
  - Estimates are local to the threshold
  - Fuzzy RD = IV at a cutoff
- Thesis: when a rule flips treatment at a threshold, the jump in outcomes right at that line reveals the causal effect for people standing near it
