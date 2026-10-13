# 5. Differences-in-Differences

## Act I · The Question

- Did the Fed save banks in the Great Depression?
  - 1930: Caldwell and Company collapses; panic spreads across the South
  - Can central-bank rescue stop a cascade of failures?
- A natural experiment: a Fed border cuts through Mississippi
  - 6th District (Atlanta Fed): easy credit, liquidity support
  - 8th District (St. Louis Fed): tight "Real Bills" credit
  - Same local economy, opposite policy responses
- Vocabulary for the chapter
  - Treatment vs. control group; counterfactual
  - Parallel trends
  - Panel data, fixed effects, ATT

## Act II · The Investigation

- The problem: one-way comparisons mislead
  - Before-after: Depression trend tangled with policy
  - Diet analogy: you gain 2 lbs, friend gains 7 → diet saved 5
- The method: difference-in-differences
  - $\delta_{DD}$ = change in treated − change in control
  - Differencing twice removes fixed gaps and common shocks
- The identifying assumption: parallel trends
  - Absent treatment, both groups move alike; violation → bias
  - Equal levels not needed: 135 vs. 165 banks
- Case study: Mississippi banks (1930–1934)
  - Both districts shrink; the 8th falls much faster
  - Dashed counterfactual: the 6th on the 8th's path
  - DD: Atlanta Fed saved roughly 19–23 banks
- The tool: regression DD with fixed effects
  - $Y_{st} = \alpha + \delta D_{st} + \text{state FE} + \text{year FE} + e_{st}$
  - State FE: permanent gaps; year FE: nationwide shocks
  - Cluster SEs by state: serial correlation within states
- Case study: minimum legal drinking age (MLDA)
  - Staggered adoption: 51 states × 14 years (1970–1983)
  - Treatment $D_{st}$: share of 18–20 year olds legally drinking
  - All causes: about 8–12 extra deaths per 100,000
  - Motor vehicle accidents carry most of it (~7–8)
  - Internal causes: no effect (placebo passes)
- Robustness toolkit
  - State-specific linear trends: estimate survives
  - Population weighting: same conclusion
  - Beer-tax control: MLDA effect barely moves
- DD in the causal toolkit
  - RCT → ATE, IV → LATE, RD → local effect, DD → ATT
  - Same MLDA question: age cutoff (Ch 4) vs. policy timing (Ch 5)
- Historical roots: John Snow and cholera (1854)
  - Lambeth moves intake upstream (1852); Southwark and Vauxhall does not
  - Deaths drop only in Lambeth areas → water, not bad air

## Act III · The Resolution

- Devil's advocate
  - "DD needs groups at the same level" → only the same trend
  - "Fixed effects remove every confounder" → only time-invariant ones
- Takeaways
  - DD = treated change minus control change
  - Parallel trends is the assumption that carries the design
  - Regression DD: state and year fixed effects, clustered SEs
  - Fed easy credit kept roughly 19–23 banks alive
  - Legal drinking raises youth deaths, mostly on the road
  - Stress-test with trends, weights, and placebo outcomes
- Thesis: when a policy shifts for some groups but not others, the untreated group's change supplies the treated group's missing counterfactual
