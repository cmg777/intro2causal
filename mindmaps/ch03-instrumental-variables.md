# 3. Instrumental Variables

## Act I · The Question

- What if people ignore their assigned treatment?
  - Experiments rarely go to plan
  - Officers, patients, lottery winners all deviate
- Naive evidence: compare by treatment received
  - Choosing to comply is tied to the outcome
  - Selection bias sneaks back in
- Vocabulary for the chapter
  - Instrument $Z$, treatment $D$, outcome $Y$
  - First stage, reduced form, LATE
  - Compliers, always-takers, never-takers, defiers

## Act II · The Investigation

- The problem: non-compliance
  - Assigned treatment vs received treatment
  - Minneapolis Domestic Violence Experiment: arrest, advise, or separate
  - Lopsided compliance: 99% for arrest vs 78% advise, 73% separate
- The tool: IV as a chain reaction
  - Domino picture: $Z \to D \to Y$
  - First stage $\phi$ ($Z$ on $D$) and reduced form $\rho$ ($Z$ on $Y$)
  - Wald ratio: LATE $= \rho / \phi$
  - Roots: Philip Wright 1928, separating supply from demand
- Identifying assumptions
  - Relevance: the instrument moves treatment
  - Independence: as good as randomly assigned
  - Exclusion: one channel only, cannot be tested
- Who LATE speaks for
  - Four subject types; monotonicity rules out defiers
  - Effect for compliers only, silent on the rest
- Case study: MDVE, arrest vs coddle
  - Binary recode: coddle (advise or separate) vs arrest
  - First stage: about 79 pp more coddling when assigned to coddle
  - Coddling raises repeat violence 14.5 pp for compliers (naive gap 8.7 pp)
- Case study: KIPP Lynn charter lottery
  - Oversubscribed after 2005; balance check passes
  - First stage 0.741; reduced form +0.355 SD in math
  - LATE: +0.48 SD in one year, for lottery compliers
- Case study: family size and children's schooling
  - Quantity-quality story; OLS: −0.15 years per extra sibling
  - Twin second birth: +0.32 children
  - Same-sex first two children: +0.08 children
  - Reduced forms near zero; 2SLS +0.24 (SE 0.13) → selection bias
- Inference toolkit: 2SLS and weak instruments
  - Stage 1 predicts $D$; stage 2 regresses $Y$ on $\hat{D}$
  - Hand-rolled 2SLS gives wrong SEs; use `pf.feols`
  - Weak instruments: first-stage F below 10
  - Choosing a design: RCT (ATE), OLS (observed confounders), IV (LATE)

## Act III · The Resolution

- Devil's advocate
  - "IV recovers the effect for everyone" → only for compliers
  - "A huge sample cures a weak instrument" → bias persists; find a stronger one
- Takeaways
  - Comparing by received treatment revives selection bias
  - LATE = reduced form ÷ first stage
  - Valid instrument: relevant, as good as random, single channel
  - Run 2SLS with IV software; check the first-stage F
  - KIPP: big math gains; family size: no harm to schooling
- Thesis: a random nudge, scaled by how far it moves treatment, reveals the causal effect for those it moves
