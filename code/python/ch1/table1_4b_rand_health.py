"""
Mastering 'Metrics — Chapter 1, Table 1.4 Panel B
==================================================
Method: RCT treatment effects on health outcomes
Data: RAND Health Insurance Experiment (HIE) — exit health measures

Key Takeaway:
    Despite dramatically higher health-care utilization under generous
    insurance (Panel A), health outcomes are remarkably SIMILAR across plan
    groups. More insurance → more spending, but NOT measurably better health.

Causal Inference Concept:
    This is a MECHANISM TEST. Panel A showed insurance increases utilization.
    Panel B asks: does that extra utilization translate into better health?
    The answer is "mostly no" — a striking finding that shapes health policy
    debates to this day.

    The null results here are substantively important. The differences are
    small AND precisely estimated (small SEs), so we can rule out large
    positive health effects of generous insurance.
"""

# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# =============================================================================
# DATA LOADING & PREPARATION
# =============================================================================
print("=" * 70)
print("Mastering 'Metrics — Table 1.4, Panel B (Health outcomes)")
print("=" * 70)

df = pd.read_stata("../../../data/ch1/rand_initial_sample_2.dta")
print(f"\nDataset: {df.shape[0]:,} observations")

# Create treatment indicators
df["any_ins"] = ((df["plantype"] == 1) | (df["plantype"] == 2) | (df["plantype"] == 3)).astype(int)

# Create family ID for clustering
df["famid"] = df["fam_identifier"].str[2:].str.replace("A", "", regex=False)
df["famid"] = pd.to_numeric(df["famid"], errors="coerce")

# Set plantype_1 to NaN where plantype is missing
df.loc[df["plantype"].isna(), "plantype_1"] = np.nan

# =============================================================================
# TABLE 1.4 PANEL B: HEALTH OUTCOMES
# =============================================================================
# These are EXIT health measures (measured 3-5 years after random assignment)
# The 'x' suffix denotes exit measures (vs baseline measures in Table 1.3)
variables = {
    "ghindxx": "General health index",
    "cholestx": "Cholesterol (mg/dl)",
    "systolx": "Systolic blood pressure (mm Hg)",
    "mhix": "Mental health index",
}

print(f"\n{'Variable':<35} {'Cata.':>8} {'[SD]':>8} {'Deduct':>9} {'Coins':>9} {'Free':>9} {'Any ins':>9}")
print("─" * 95)

catastrophic = df[df["plantype"] == 4]

for var, label in variables.items():
    # Column 1: Mean and SD for catastrophic group
    cat_data = catastrophic[var].dropna()
    cat_mean = cat_data.mean()
    cat_sd = cat_data.std()

    # Columns 2-4: Regression on plan dummies with clustered SEs
    reg_data = df[[var, "plantype_1", "plantype_2", "plantype_3", "famid"]].dropna()
    model = smf.ols(f"{var} ~ plantype_1 + plantype_2 + plantype_3", data=reg_data)
    res = model.fit(cov_type="cluster", cov_kwds={"groups": reg_data["famid"]})

    deduct_diff = res.params["plantype_2"]
    deduct_se = res.bse["plantype_2"]
    coins_diff = res.params["plantype_3"]
    coins_se = res.bse["plantype_3"]
    free_diff = res.params["plantype_1"]
    free_se = res.bse["plantype_1"]

    # Column 5: Any insurance vs catastrophic
    reg_data2 = df[[var, "any_ins", "famid"]].dropna()
    model2 = smf.ols(f"{var} ~ any_ins", data=reg_data2)
    res2 = model2.fit(cov_type="cluster", cov_kwds={"groups": reg_data2["famid"]})
    any_diff = res2.params["any_ins"]
    any_se = res2.bse["any_ins"]

    print(f"{label:<35} {cat_mean:>6.1f} [{cat_sd:>5.1f}]  {deduct_diff:>7.2f}  {coins_diff:>7.2f}  {free_diff:>7.2f}  {any_diff:>7.2f}")
    print(f"{'':>35} {'':>6} {'':>7}  ({deduct_se:.2f})  ({coins_se:.2f})  ({free_se:.2f})  ({any_se:.2f})")

# Sample sizes
print("─" * 95)
for ptype, name in [(4, "Catastrophic"), (2, "Deductible"), (3, "Coinsurance"), (1, "Free")]:
    n = (df["plantype"] == ptype).sum()
    print(f"  N ({name}): {n}")

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("""
Key findings from the RAND experiment (Panel B):
  • General health index: virtually identical across all groups
  • Cholesterol: no significant differences
  • Blood pressure: no significant differences
  • Mental health: no significant differences

The punchline:
  Free health insurance caused people to USE 45% more health care (Panel A),
  but this extra care produced NO MEASURABLE IMPROVEMENT in health (Panel B).

Policy implications:
  1. Cost-sharing (deductibles, copays) reduces utilization without harming health
  2. The "moral hazard" of generous insurance is real and costly
  3. Simply providing more care ≠ better health outcomes

Statistical note:
  "No significant effect" ≠ "no effect." But the standard errors here are
  small enough to rule out large health benefits. These are precisely estimated
  null effects, not imprecise estimates that could go either way.
""")
