# Content and geometry audit

Apply checks relevant to the actual map. An unrelated topic does not require econometric terminology, but still requires accurate claims, numbers, arrows, labels and quantitative geometry.

## Evidence and equations

Read exact symbols and subscripts from the generated image, not only the prompt. Check units, denominators, signs, approximations and the target population. Verify important numerical calculations with source data/specifications where feasible. When browsing is needed, prefer papers, author/institution documentation and primary study reports; cite specific support in the audit. Record what could not be re-estimated. Do not replace “no significant effect detected” with “zero effect”, or generalize a local/sample average to everyone.

For the book preset, resolve these common distinctions:

| Topic | Correctness checks |
|---|---|
| Potential outcomes | The same person's Y(1), Y(0); one observed; individual difference is not an observed group gap. |
| Selection decomposition | Population observed mean gap = ATT + E[Y(0)\|D=1]−E[Y(0)\|D=0]. ATT is not generally ATE. Sampling uncertainty still exists. |
| Randomization | Baseline balance in expectation; finite samples can differ; ITT is assignment, not receipt. |
| Mean regression | Binary treatment coefficient equals mean gap with an intercept and no other controls. |
| Regression identification | Conditional independence, overlap and suitable specification; fitted coefficients need not be causal merely because controls were added. |
| OVB | For one omitted regressor, βshort−βlong=π₁γ. Auxiliary regression includes shared controls. Multiple omissions require a sum/vector product. Regression association is not itself a causal arrow. |
| Bad controls | A mediator can block a total-effect channel; a collider can open bias. Not every pre-treatment variable is automatically helpful. |
| IV | Relevance, independence (possibly conditional), exclusion of all non-treatment channels, monotonicity for binary LATE, consistency/no interference. First stage is an uptake difference. |
| 2SLS | Include the same exogenous controls in both stages; use appropriate IV inference. The simple binary Wald ratio and continuous-treatment causal responses need distinct interpretations. |
| RD | Compare fitted limits at the same cutoff; potential outcomes smooth absent treatment; sharp versus fuzzy; local effect versus local complier effect; no simultaneous causal change. |
| DD | Parallel untreated trends, no anticipation and appropriate interference assumptions. Different baseline levels are fine. Two-way FE do not cure time-varying confounding; staggered timing/continuous dose can need additional methods/assumptions. |
| Schooling | Log-coefficient percentages are approximate: exact change is 100(exp(ρ)−1). A DD log-earnings/schooling ratio also needs exclusion and a nonzero schooling first stage. Twins do not eliminate nonshared differences; co-twin IV needs valid reporting-error/exogeneity assumptions. Diploma RD targets a credential, not an extra year. |

The audit should distinguish an error from a valid simplification: ±2SE is a familiar large-sample rule of thumb; a CI centered at zero is legitimate; flat parallel pre-trends are valid; a negative DD effect is possible. Nevertheless, a generic sketch placed beside a positive study finding should not inadvertently look like that study's negative estimate.

## Inspect and measure the actual diagram

- Arrows: confounder → treatment and confounder → outcome; distinguish association from causal paths and mediation. Read arrowheads carefully.
- Parallel trends: sample matching horizontal coordinates over the untreated interval. Compare slopes AND drift in vertical separation. Post-period treatment effects may change actual treated trends; the untreated treated counterfactual must follow the appropriate control change and start at its own baseline.
- Effect markers: both endpoints lie on the quantities compared at the same time/threshold; no second floating marker.
- Intervals: midpoint for a symmetric CI; endpoints, estimate and zero reference have distinct roles.
- Cutoff windows: check shared center and nested ranges, or an explicitly intended asymmetric design.
- Probability/percentage plots: calibrated bounds, difference versus relative change, step height and arrow endpoints.
- Binary/categorical axes: supported locations only, rather than fabricated continuous observations.
- Presentation: read all text at full size and intended slide scale; check formulas, collisions, clipping and displaced legends after every revision.

`scripts/check_geometry.py` supports raster sampling of colored parallel lines and constraints on manually measured landmarks. Prepare its checks JSON **after** viewing the image at native resolution. For landmarks, record how coordinates were measured. This helper cannot recognize semantics, infer a causal model, verify an estimate's interpretation or prove identification assumptions.

Example parallel check (replace these illustrative coordinates with actual observed regions):

```json
{"checks": [{
  "id": "pre-trends", "type": "parallel_lines",
  "xs": [100, 125, 150, 175],
  "line_a": {"y_range": [530, 560], "rgb": [56, 189, 248], "color_tolerance": 65},
  "line_b": {"y_range": [575, 600], "rgb": [167, 139, 250], "color_tolerance": 65},
  "max_separation_drift_px": 3, "max_slope_difference": 0.02
}]}
```

Run:

```text
python .claude/skills/draw-mindmap/scripts/check_geometry.py IMAGE --checks RUN/geometry-input.json --out RUN/geometry-results.json
```

Use tight image-specific sampling regions that exclude text/icons and the policy date. Color misses, poor coverage or ambiguous landmarks require another observation, not fabricated data or increased tolerance until a pass. State tolerances in pixel units, proportional to line thickness/resolution; they do not relax exact algebra. For manually supplied `symmetric_interval`, `centered_windows`, `jump_fraction` or `same_coordinate` checks, the helper evaluates the supplied measurements, so independently verify that they describe the pixels.

Manual check rows use `id`, `type`, `measurement_method` (how pixels were measured), and optional `tolerance_px` (default 3), plus these fields. Coordinates are native-image pixels, origin at the top-left, y increasing downward.

| Type | Fields |
|---|---|
| `symmetric_interval` | `left`, `right`, `estimate`: each `[x,y]`; checks a horizontal interval and its midpoint. |
| `centered_windows` | `cutoff_x`; `narrow` and `wide`: each `[left_x,right_x]`; checks centering and nesting. |
| `jump_fraction` | `zero`, `one`: `[x,y]` axis landmarks; `before`, `after`: `[x,y]` limit values at the same cutoff; `expected_fraction`, optional `fraction_tolerance` (default 0.03). Checks bounds and signed scale fraction. |
| `same_coordinate` | `points`: at least two `[x,y]` landmarks; `axis`: `x` or `y`. For effect arrows, also manually verify each endpoint lies on the appropriate line. |

Helpers can be revalidated offline with `python .claude/skills/draw-mindmap/scripts/test_helpers.py`. Its synthetic fixtures are tests, never substitutes for a generated mind map.

## Release decision

A pass requires readable image content, correct source-backed labels, correct relevant mathematics, coherent graphical semantics, and satisfactory measured geometry. `not_applicable` requires a reason; unavailable empirical data requires scoped source attribution, not a fabricated replication. An important unresolved assertion or inaccurate graph means `failed`/`incomplete` and no export as an accepted master.

Save enough evidence for a future reviewer: source locations, calculation specifications/results, native image size/hash, manual findings, measurement inputs/results, repaired issues and limitations. Keep failed attempt history distinct from the audit of the selected final image.
