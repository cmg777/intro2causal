# 6. The Wages of Schooling

## Act I · The Question

- Does more education cause higher earnings?
  - College graduates earn roughly twice what high school graduates earn
  - How much of that gap is caused by school, and how much by who goes?
- Naive evidence: 1980 Census regression
  - Each extra year of school goes with ~7% higher weekly earnings
  - Very precise, but the more able may both study longer and earn more
- One question, all five tools
  - A methods ladder: each rung fixes a weakness of the one before
- Vocabulary for the chapter
  - Return to schooling $\rho$ (log-wage gain per year)
  - Ability bias, measurement error, reliability ratio
  - Human capital vs. signaling (sheepskin effect)

## Act II · The Investigation

- The problem: ability bias
  - Bivariate model: $\ln W_i = \alpha + \rho S_i + e_i$, with ability in the error
  - OVB formula: $\gamma \times \pi_1 > 0$, so OLS runs high
    - Rare twist: star dropouts could push the bias down
  - Twinsburg twins with demographic controls: still ~11%
  - Synthetic demo: short regression ~0.12 vs. true ~0.09 (~40% too high)
  - Bad control: occupation is an outcome of schooling, so it soaks up a real channel
- The benchmark: why not an RCT?
  - Randomizing years of school: unethical and impractical
  - Synthetic scholarship lottery: ~2 extra years; Wald ratio recovers the true 0.08
- Strategy 1: twin comparisons (Twinsburg, 340 pairs)
  - Within-pair differences cancel shared genes and upbringing
  - Twin fixed effects: estimate falls to ~6%
  - Measurement error: differencing shrinks the signal, not the noise
    - Reliability ratio of 0.5 would halve the estimate
  - Fix: co-twin's report as instrument → ~12% (levels), ~11% (differences)
  - Caveats: festival-goers are self-selected; shared misreports weaken the fix
- Strategy 2: quarter-of-birth IV (Angrist and Krueger 1991)
  - Design: 1980 Census, 329,509 men born 1930–1939
  - Mechanism: entry-age cutoffs plus dropout at 16 keep Q4 births in school longer
  - First stage ~0.09 years; Wald ratio ~7%, matched by 2SLS
  - A LATE for compliers at the dropout margin
- Strategy 3: child labor law IV (Acemoglu and Angrist)
  - Instruments: required school entry by age 7, 8, or 9; state, cohort, census-year effects
  - OLS ~7% vs. IV ~13%
  - First-stage F below 10: weak instruments, wide uncertainty
- Strategy 4: sheepskin RD (Clark and Martorell 2014)
  - Texas last-chance exit exam: 46 score bins around the passing line
  - Diploma receipt jumps ~40 points at the cutoff (a fuzzy RD)
  - Earnings barely move: the credential alone adds little
- Strategy 5: differences-in-differences (synthetic)
  - Reform in 10 of 20 states in 2005; parallel pre-trends in schooling and earnings
  - DD on earnings ÷ DD on schooling = implied return; same policy variation as Strategy 3
- Synthesis: the Furious Five side by side
  - Twin FE sits low, OLS runs high, the IV estimates cluster at 7–10%

## Act III · The Resolution

- Devil's advocate
  - "Twin FE is lowest, so it must be closest to the truth" → noise drags it down
  - "No diploma jump means school does not pay" → it pays through skills, not the paper
- Takeaways
  - Raw OLS (~7%) blends the causal return with ability bias
  - Twins remove shared ability but magnify reporting errors
  - Instruments correct the errors and point to 7–10%
  - The diploma itself is worth little; learning drives the premium
  - Trust convergence across methods with different weak spots
- Thesis: when five imperfect designs agree, a year of school raises earnings by roughly 7–10%
