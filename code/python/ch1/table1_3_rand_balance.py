"""
Mastering 'Metrics — Chapter 1, Table 1.3
=========================================
Method: Balance check in a Randomized Controlled Trial (RCT)
Data: RAND Health Insurance Experiment (HIE)

Key Takeaway:
    When treatment is randomly assigned, treatment and control groups should
    look similar on all baseline characteristics. This table verifies that
    randomization "worked" — differences across insurance plan groups are
    small and rarely statistically significant.

Causal Inference Concept:
    CHECKING FOR BALANCE is the first step in analyzing any RCT. If baseline
    characteristics are balanced across treatment arms, we can be confident
    that any post-treatment differences in outcomes reflect causal effects
    of the treatment, not pre-existing differences between groups.

    Why cluster standard errors?
    Family members in the HIE were assigned to the same plan. Observations
    within a family are correlated, so we cluster SEs at the family level
    to avoid overstating statistical precision.
"""

# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# =============================================================================
# DATA LOADING
# =============================================================================
DATA_PATH = "../../../data/ch1/rand_initial_sample_2.dta"

print("=" * 70)
print("Mastering 'Metrics — Table 1.3")
print("Demographic characteristics and baseline health in the RAND HIE")
print("=" * 70)

df = pd.read_stata(DATA_PATH)
print(f"\nDataset: {df.shape[0]:,} observations, {df.shape[1]} variables")

# =============================================================================
# DATA PREPARATION
# =============================================================================
# Plan types in the RAND HIE:
#   1 = Free plan (most generous — zero cost-sharing)
#   2 = Deductible plan (pay 95% of outpatient, capped)
#   3 = Coinsurance plan (pay 25-50% of costs, capped)
#   4 = Catastrophic plan (pay 95% of all costs — approximates NO insurance)
#
# The catastrophic plan is our CONTROL GROUP (baseline).

# Create "any insurance" indicator (any plan more generous than catastrophic)
df["any_ins"] = ((df["plantype"] == 1) | (df["plantype"] == 2) | (df["plantype"] == 3)).astype(int)

# Create family ID for clustering
# The fam_identifier has a prefix we need to strip
df["famid"] = df["fam_identifier"].str[2:].str.replace("A", "", regex=False)
df["famid"] = pd.to_numeric(df["famid"], errors="coerce")

# Ensure plan type dummies are missing when plantype is missing
df.loc[df["plantype"].isna(), "plantype_1"] = np.nan

# =============================================================================
# TABLE 1.3: BALANCE CHECK
# =============================================================================
# Variables to check for balance:
variables = {
    "female": "Female",
    "blackhisp": "Nonwhite",
    "age": "Age",
    "educper": "Education",
    "income1cpi": "Family income",
    "ghindx": "General health index",
    "cholest": "Cholesterol (mg/dl)",
    "systol": "Systolic blood pressure (mm Hg)",
    "mhi": "Mental health index",
}

# Column 1: Means and SDs for catastrophic plan group
catastrophic = df[df["plantype"] == 4]

print(f"\n{'Variable':<30} {'Cata. mean':>12} {'[SD]':>10} {'Deduct':>10} {'Coins':>10} {'Free':>10} {'Any ins':>10}")
print("─" * 100)

results = []

for var, label in variables.items():
    # Column 1: Mean and SD for catastrophic group
    cat_data = catastrophic[var].dropna()
    cat_mean = cat_data.mean()
    cat_sd = cat_data.std()

    # Columns 2-4: Regress variable on plan dummies (catastrophic = omitted baseline)
    # This gives us the DIFFERENCE between each plan and catastrophic
    reg_data = df[[var, "plantype_1", "plantype_2", "plantype_3", "famid"]].dropna()
    model = smf.ols(f"{var} ~ plantype_1 + plantype_2 + plantype_3", data=reg_data)
    res = model.fit(cov_type="cluster", cov_kwds={"groups": reg_data["famid"]})

    # Extract coefficients (differences from catastrophic) and SEs
    deduct_diff = res.params["plantype_2"]
    deduct_se = res.bse["plantype_2"]
    coins_diff = res.params["plantype_3"]
    coins_se = res.bse["plantype_3"]
    free_diff = res.params["plantype_1"]
    free_se = res.bse["plantype_1"]

    # Column 5: Regress on "any insurance" dummy
    reg_data2 = df[[var, "any_ins", "famid"]].dropna()
    model2 = smf.ols(f"{var} ~ any_ins", data=reg_data2)
    res2 = model2.fit(cov_type="cluster", cov_kwds={"groups": reg_data2["famid"]})
    any_diff = res2.params["any_ins"]
    any_se = res2.bse["any_ins"]

    # Print row
    print(f"{label:<30} {cat_mean:>10.1f}  [{cat_sd:>7.1f}]  {deduct_diff:>7.2f}   {coins_diff:>7.2f}   {free_diff:>7.2f}   {any_diff:>7.2f}")
    print(f"{'':>30} {'':>10}  {'':>9}  ({deduct_se:.2f})  ({coins_se:.2f})  ({free_se:.2f})  ({any_se:.2f})")

    results.append({
        "variable": label,
        "cat_mean": cat_mean,
        "cat_sd": cat_sd,
        "deduct_diff": deduct_diff,
        "deduct_se": deduct_se,
        "coins_diff": coins_diff,
        "coins_se": coins_se,
        "free_diff": free_diff,
        "free_se": free_se,
        "any_diff": any_diff,
        "any_se": any_se,
    })

# Sample sizes per plan type
print("─" * 100)
for ptype, name in [(4, "Catastrophic"), (2, "Deductible"), (3, "Coinsurance"), (1, "Free")]:
    n = (df["plantype"] == ptype).sum()
    print(f"  N ({name}): {n}")
n_any = df["any_ins"].sum()
print(f"  N (Any insurance): {n_any}")

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("""
How to read this table:
  - Column 1 shows means for the CATASTROPHIC (control) group
  - Columns 2-5 show DIFFERENCES between each treatment group and control
  - Standard errors (in parentheses) are clustered at the family level

Rule of thumb for balance:
  - A difference is "statistically significant" if |diff/SE| > 2
  - In a well-randomized experiment, we expect few significant differences
  - Any significant differences should be small and inconsistent in direction

Key finding:
  Most differences are small relative to their SEs. The few that approach
  significance (e.g., proportion female) don't show a consistent pattern.
  This confirms that randomization successfully created comparable groups,
  unlike the NHIS comparison in Table 1.1 where the groups differed
  dramatically on every dimension.
""")
