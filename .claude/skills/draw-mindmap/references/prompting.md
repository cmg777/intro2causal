# Prompting and revisions

## Generation brief

Give the tool the accepted source-backed content, rather than asking it to invent a chapter summary. Specify:

1. Use, audience, language, aspect ratio and requested dimensions.
2. Palette, central node, radial hierarchy, typography and illustration medium.
3. Exact text grouped by branch, separated from instructions that must not appear on the image.
4. Each illustration's explanatory role and any quantitative geometry it must satisfy.
5. Scientific qualifications, forbidden invented numbers and layout constraints.

For a plot, specify the estimand, axes, units, variable support, which lines are observed/counterfactual, and what an arrow measures. A generic “draw a DD graph” is insufficient. Do not invent individual characters, numeric observations or study results simply to fill space. A schematic can use illustrative levels if it is explicitly a schematic and they are not presented as empirical estimates.

Ask for the chosen dimensions, but check the tool's actual output. The previous built-in generator returned 1672×941 images despite a larger requested size. Report the native dimensions; do not call them 4K. Do not stretch type or redraw content through an export helper.

## Local edit recipe

Name the edit target and the affected region. Describe the mathematical defect, the required replacement, exact text, and invariants. Use the tool's supported image-reference mechanism; do not assume its last-image context selects the intended file during a batch.

Example:

```text
Edit only the main DD mini plot. Erase its existing trend lines and effect markers.
Before the intervention: two horizontal lines at different levels.
After it: control stays horizontal; the treated counterfactual continues horizontally
from the treated intervention-date point; actual treatment rises.
Draw one vertical effect marker between actual and counterfactual at the SAME post time.
Keep every other label, illustration, equation and palette choice unchanged.
```

This permits a simplified but valid schematic. Horizontal parallel trends are a valid special case; nonzero identical slopes are equally valid. Do not require actual treated/control post-trends to remain parallel after a nonzero effect.

Persistent errors often require removing the entire offending mini diagram and drawing a simpler replacement. Our experience included edits that changed a label but left the old interval dot, a second floating effect arrow, or unequal slopes. Reinspect all resulting regions; the instruction to preserve them is not evidence they were preserved.

Useful constraints:

- A symmetric Wald CI has the estimate at the midpoint of its endpoints. A zero reference may coincide with the estimate; that is valid, not an error to “fix”.
- A probability axis must be within [0,1]. Forty percentage points is a 0.40 difference, not a 40% relative rise. Keep the effect marker on the two limit values.
- A binary treatment has support {0,1}. A plot of two fitted conditional means is often clearer than an invented scatter/residual plot.
- Both narrow and wide bandwidth windows should be centered on the same cutoff when the design is symmetric; explicitly label intentional asymmetric windows.
- A quantitative bar comparison must have a consistent scale and common baseline. Use labeled concept icons instead if exact bar geometry cannot be retained.
- Birth quarter and laws may be joint inputs; a visual arrow between them falsely claims one causes the other.

Store all exact prompts with their input/output identity and hashes. Do not copy discarded drafts into the accepted image folder. Tool-native edits are the route for content changes; helper scripts only measure, encode, verify, package and clean explicitly identified drafts.
