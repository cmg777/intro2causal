"""
Mastering 'Metrics — Chapter 1, Table 1.1
=========================================
Method: Observational comparison (illustrating selection bias)
Data: National Health Interview Survey (NHIS), 2009

Key Takeaway:
    Insured people are healthier than uninsured people, but this comparison
    is NOT causal. The insured are also richer, more educated, and more likely
    to be employed — classic selection bias.

Causal Inference Concept:
    Before we can claim that health insurance *causes* better health, we need
    to address the fact that people who choose insurance differ systematically
    from those who don't. This table documents those differences, motivating
    the need for randomized experiments (covered next in Tables 1.3–1.4).
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
# Path to the NHIS 2009 data (Stata format)
DATA_PATH = "../../../data/ch1/NHIS2009_clean.dta"

print("=" * 70)
print("Mastering 'Metrics — Table 1.1")
print("Health and demographic characteristics of insured and uninsured")
print("couples in the NHIS (2009)")
print("=" * 70)

df = pd.read_stata(DATA_PATH)
print(f"\nRaw dataset: {df.shape[0]:,} observations, {df.shape[1]} variables")

# Convert categorical columns to numeric (Stata value labels → numbers)
# Some categorical columns have labels like "4 people" — extract the number
for col in df.select_dtypes(include="category").columns:
    df[col] = df[col].astype(str).str.extract(r"(\d+)").astype(float)

# =============================================================================
# SAMPLE SELECTION
# =============================================================================
# The Stata code applies several filters to get married couples aged 26-59
# with at least one spouse working.

# Keep married adults with non-zero survey weights
df = df[(df["marradult"] == 1) & (df["perweight"] != 0)].copy()

# Keep households where health insurance variable is not missing
# Create household-level insurance variable (mean of hi_hsb1 within household)
df["hi_hsb"] = df.groupby("serial")["hi_hsb1"].transform("mean")
df = df[df["hi_hsb"].notna() & df["hi"].notna()].copy()

# Keep households with exactly one female
df["numfem"] = df.groupby("serial")["fml"].transform("sum")
df = df[df["numfem"] == 1].copy()

# Apply age restriction and employment requirement (Angrist's criteria)
df = df[(df["age"] >= 26) & (df["age"] <= 59) & (df["adltempl"] >= 1)].copy()

# Drop single-person households
df["hh_size"] = df.groupby("serial")["serial"].transform("count")
df = df[df["hh_size"] > 1].copy()

print(f"Analysis sample: {df.shape[0]:,} observations")

# Split into husbands and wives
husbands = df[df["fml"] == 0].copy()
wives = df[df["fml"] == 1].copy()
print(f"  Husbands: {len(husbands):,}")
print(f"  Wives:    {len(wives):,}")

# =============================================================================
# TABLE 1.1: COMPARISON BY INSURANCE STATUS
# =============================================================================
# Variables to compare:
#   hlth    = health index (1=poor to 5=excellent)
#   nwhite  = nonwhite indicator
#   age     = age in years
#   yedu    = years of education
#   famsize = family size
#   empl    = employed indicator
#   inc     = family income

variables = {
    "hlth": "Health index",
    "nwhite": "Nonwhite",
    "age": "Age",
    "yedu": "Education",
    "famsize": "Family size",
    "empl": "Employed",
    "inc": "Family income",
}


def make_comparison_table(data, label):
    """
    For each variable, compute:
      - Weighted mean for insured (hi=1) and uninsured (hi=0)
      - Difference via OLS regression of variable on hi, with robust SEs
        (This is equivalent to a weighted difference in means)

    Why regression for a simple difference?
        In Stata, regressing Y on a dummy D gives:
          - Intercept = mean of Y when D=0
          - Coefficient on D = difference in means (D=1 minus D=0)
          - Robust SE on D = standard error of the difference
        This is a convenient way to get the difference AND its SE in one step.
    """
    print(f"\n{'─' * 70}")
    print(f"  {label}")
    print(f"{'─' * 70}")
    print(f"{'Variable':<20} {'Insured':>12} {'Uninsured':>12} {'Difference':>12} {'SE':>10}")
    print(f"{'─' * 70}")

    insured = data[data["hi"] == 1]
    uninsured = data[data["hi"] == 0]

    for var, var_label in variables.items():
        # Weighted means
        mean_ins = np.average(insured[var].dropna(), weights=insured.loc[insured[var].notna(), "perweight"])
        mean_unins = np.average(uninsured[var].dropna(), weights=uninsured.loc[uninsured[var].notna(), "perweight"])

        # Regression for difference with robust standard errors
        # Using analytic weights (aweights in Stata) = WLS with normalized weights
        model = smf.wls(f"{var} ~ hi", data=data, weights=data["perweight"])
        result = model.fit(cov_type="HC1")  # HC1 = Stata's "robust"

        diff = result.params["hi"]
        se = result.bse["hi"]

        # For health index, also show standard deviations
        if var == "hlth":
            sd_ins = insured[var].std()
            sd_unins = uninsured[var].std()
            print(f"{var_label:<20} {mean_ins:>9.2f}    {mean_unins:>9.2f}    {diff:>9.2f}   ({se:.2f})")
            print(f"{'  [std dev]':<20} [{sd_ins:>7.2f}]   [{sd_unins:>7.2f}]")
        else:
            print(f"{var_label:<20} {mean_ins:>9.2f}    {mean_unins:>9.2f}    {diff:>9.2f}   ({se:.2f})")

    # Sample sizes
    n_ins = len(insured)
    n_unins = len(uninsured)
    print(f"{'─' * 70}")
    print(f"{'Sample size':<20} {n_ins:>12,} {n_unins:>12,}")

    return n_ins, n_unins


# Generate tables for husbands and wives
make_comparison_table(husbands, "HUSBANDS")
make_comparison_table(wives, "WIVES")

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("""
The insured are healthier (higher health index), but they are also:
  • More educated (~3 more years of schooling)
  • Much richer (~$60,000 more family income)
  • More likely to be employed
  • Older and from smaller families

This is SELECTION BIAS: people who choose insurance differ from those who
don't in many ways that independently affect health. The raw difference in
health outcomes conflates the causal effect of insurance with pre-existing
differences between the groups.

Key equation from the chapter:
    Observed difference = Causal effect (κ) + Selection bias

To isolate the causal effect, we need a research design that eliminates
selection bias. Chapter 1 proceeds to show how RANDOMIZED EXPERIMENTS
(the RAND HIE and Oregon Health Plan) accomplish exactly this.
""")
