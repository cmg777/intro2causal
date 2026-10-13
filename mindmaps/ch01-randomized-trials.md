# 1. Randomized Trials

## Act I · The Question

- Does health insurance make people healthier?
  - Highest health spending in the rich world
  - Millions still uninsured
- Naive evidence: NHIS 2009 survey
  - Insured report better health (3.98 vs 3.66 on a 1–5 scale)
  - Insured are also older, more educated, richer, more often employed
- Vocabulary for the chapter
  - Potential outcomes $Y_{1i}$, $Y_{0i}$
  - Selection bias
  - Random assignment

## Act II · The Investigation

- The problem: selection bias
  - Potential outcomes: two roads, only one observed
  - Two-person example: naive gap has the wrong sign
  - Decomposition: observed gap = causal effect + selection bias
  - Confounders open a back-door path
  - Fundamental problem of causal inference
- The tool: regression on a dummy
  - Intercept = control mean; coefficient = difference in means
  - Standard error and the |t| > 2 rule
  - NHIS comparison table: large gaps on every trait
- The solution: random assignment
  - A coin flip breaks the link between treatment and traits
  - Law of large numbers balances observed and unobserved traits
  - Selection-bias term goes to zero
  - Roots: Lind 1747, Peirce and Jastrow 1885, Fisher 1925
- Case study: RAND Health Insurance Experiment (1974–1982)
  - Design: ~4,000 people, four plan types, catastrophic plan = control
  - Balance check passes (SEs clustered by family)
  - Free care raises use: +1.7 visits, +45% total spending
  - Health outcomes: a precisely estimated null
- Case study: Oregon Medicaid lottery (2008)
  - Low-income adults; lottery for Medicaid
  - Only ~25% of winners enrolled → intent-to-treat (preview of IV)
  - More care, no physical-health gain
  - Better mental health, less medical debt
- Inference toolkit
  - Standard error, t-statistic, 95% confidence interval
  - Significance measures precision, not importance

## Act III · The Resolution

- Devil's advocate
  - "The insured are healthier, so insurance works" → selection bias
  - "Not significant means no effect" → only if the estimate is precise
- Takeaways
  - Any comparison = causal effect + selection bias
  - Randomize, then check balance
  - Regression on a dummy = difference in means + standard error
  - RAND: more care, not more health
  - Oregon: financial protection and mental health
- Thesis: random assignment turns a comparison of groups into a causal effect
