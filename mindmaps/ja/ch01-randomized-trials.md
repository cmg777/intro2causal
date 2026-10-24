# 第1章：無作為化比較試験 — Randomized Trials

Source: `book/images/ch01_visual_summary.webp` (the full English visual map).
This is a full visual translation, not an expansion of the Markdown outline or the compact Spotify cover.
The exact Japanese copy and its placement are recorded in `prompts/ch01-randomized-trials-v1.txt`; the active typography revision is recorded in `prompts/ch01-randomized-trials-v2-readable-type.txt`.

## Translation choices

- 潜在的な結果 / Potential outcomes: matches the existing Japanese glossary.
- 無作為割り当て / Random assignment: conditions balance on average, not necessarily exactly in a realized sample.
- 処置群 / Treatment; 対照群 / Control: preserve group labels.
- ATT: 処置を受けた人への平均効果; retain the distinction from ITT.
- ITT: compare lottery winners and losers, not actual insurance recipients and nonrecipients.
- Catastrophic coverage: 高額医療費のみを保障する保険; the compact illustration label is 高額医療費の保障. This is insurance, not a group without insurance.
- RAND: approximately 45% greater spending, little average health change, some poor/sick patients benefit. Retain every qualification.
- Oregon: more care, improved mental health, less medical debt; no statistically significant measured physical-health improvement at two years.
- Reading evidence: retain intercept/no-controls condition for the binary-treatment coefficient; large-sample qualifier, 95%, 1.96 × SE, and non-significance ≠ no effect.

## Reference checks

- `notebooks_quarto/01-randomized-trials.qmd`: spending calculation and catastrophic reference coverage; Oregon findings; sickest/poorest subgroup caveat.
- `notebooks_colab/01-randomized-trials.ipynb`: corresponding empirical replication and teaching discussion.
- `mindmaps-podcast/ja/glossary.json`: established technical terminology.

## Status

Chapter 1 version 2 was approved by the user: “Great, I like it. Proceed.”
Chapters 2–6 now apply the same readable typography and contrast.

Current sample: `images/ch01-randomized-trials-v2.png`, with larger Gothic-style
lettering and stronger white-on-navy contrast. The first version is retained
for comparison.
