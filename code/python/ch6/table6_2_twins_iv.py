"""
Mastering 'Metrics — Chapter 6, Table 6.2
=========================================
Method: Twin Fixed Effects + Instrumental Variables (IV/2SLS)
Data: Twinsburg twins (Ashenfelter & Krueger 1994, Ashenfelter & Rouse 1998)

Key Takeaway:
    OLS returns to schooling (~0.11) may be biased upward by ability.
    Within-twins differencing (~0.06) and IV using twin's education (~0.08)
    suggest the true return is somewhat lower but still substantial.

Causal Inference Concept:
    The RETURNS TO SCHOOLING is one of the most studied causal questions in
    economics. The challenge: people with more education differ from those
    with less in many ways (ability, motivation, family background).

    Three strategies are compared here:

    1. OLS (biased): Regress wages on education + controls
       - Likely overstates the return due to ability bias

    2. TWIN FIXED EFFECTS: Compare wages WITHIN identical twin pairs
       - Twins share genes and family background
       - Differencing eliminates these shared confounders
       - Formula: Δwage = β·Δeducation (no intercept needed)

    3. IV using twin's education as instrument:
       - Key idea: one twin's education is correlated with the other's
         (shared family influences) but doesn't directly affect the
         other's wages (exclusion restriction)
       - IV2SLS: First stage regresses own education on twin's education
         + controls; second stage uses predicted education

    Combining twins + IV can further reduce bias from measurement error
    in self-reported education.
"""

# =============================================================================
# IMPORTS
# =============================================================================
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels.iv import IV2SLS

# =============================================================================
# DATA LOADING
# =============================================================================
print("=" * 70)
print("Mastering 'Metrics — Table 6.2")
print("Returns to schooling for Twinsburg twins")
print("=" * 70)

# NOTE: The pubtwins.dta file must be downloaded manually from Princeton:
#   https://dataspace.princeton.edu/handle/88435/dsp01rv042t084
# Save it to: code/stata/ch6/pubtwins.dta
import sys
import os

DATA_PATH = "../../../data/ch6/pubtwins.dta"
if not os.path.exists(DATA_PATH):
    print(f"\n  ERROR: {DATA_PATH} not found.")
    print("  Please download pubtwins.dta from:")
    print("    https://dataspace.princeton.edu/handle/88435/dsp01rv042t084")
    print("  and save it to code/stata/ch6/pubtwins.dta")
    sys.exit(1)

df = pd.read_stata(DATA_PATH)
print(f"\nDataset: {df.shape[0]} twin observations")
print(f"Variables: {list(df.columns)}")

# Replicate Stata: age2 is divided by 100
df["age2"] = df["age2"] / 100

# =============================================================================
# COLUMN 1: OLS RETURNS TO SCHOOLING
# =============================================================================
print("\n" + "─" * 60)
print("Column 1: OLS — Plain regression (potentially biased)")
print("─" * 60)
print("  Model: lwage = β₀ + β₁·educ + β₂·age + β₃·age² + β₄·female + β₅·white + ε")
print("  Problem: β₁ captures education effect + ability bias")

ols = smf.ols("lwage ~ educ + age + age2 + female + white", data=df).fit(cov_type="HC1")
print(f"\n  Return to schooling (OLS): {ols.params['educ']:.4f}")
print(f"  Robust SE:                  ({ols.bse['educ']:.4f})")
print(f"  N = {int(ols.nobs)}")

# =============================================================================
# COLUMN 2: WITHIN-TWINS DIFFERENCES
# =============================================================================
print("\n" + "─" * 60)
print("Column 2: Twin differences (fixed effects within pairs)")
print("─" * 60)
print("  Model: Δlwage = β₁·Δeduc + ε  (no intercept)")
print("  Logic: Differencing within twin pairs eliminates shared")
print("         genetics, family background, and upbringing")

# Use only first twin to avoid double-counting
first_twins = df[df["first"] == 1].copy()

twins_ols = smf.ols("dlwage ~ deduc - 1", data=first_twins).fit(cov_type="HC1")
print(f"\n  Return to schooling (twins Δ): {twins_ols.params['deduc']:.4f}")
print(f"  Robust SE:                      ({twins_ols.bse['deduc']:.4f})")
print(f"  N = {int(twins_ols.nobs)} twin pairs")

# =============================================================================
# COLUMN 3: IV USING TWIN'S EDUCATION (LEVELS)
# =============================================================================
print("\n" + "─" * 60)
print("Column 3: IV — Twin's education as instrument (levels)")
print("─" * 60)
print("  Endogenous: educ (own education)")
print("  Instrument: educt_t (twin's report of respondent's education)")
print("  Controls: age, age², female, white")
print("  Logic: Twin's report is correlated with true education")
print("         but may be less prone to measurement error")

iv_levels = IV2SLS.from_formula(
    "lwage ~ 1 + age + age2 + female + white + [educ ~ educt_t]",
    data=df,
).fit(cov_type="robust")

print(f"\n  Return to schooling (IV): {iv_levels.params['educ']:.4f}")
print(f"  Robust SE:                ({iv_levels.std_errors['educ']:.4f})")
print(f"  N = {int(iv_levels.nobs)}")

# =============================================================================
# COLUMN 4: IV USING TWIN'S EDUCATION (DIFFERENCES)
# =============================================================================
print("\n" + "─" * 60)
print("Column 4: IV — Twin differences + twin's report as instrument")
print("─" * 60)
print("  Endogenous: Δeduc (difference in own-reported education)")
print("  Instrument: Δeduct (difference in twin's report of education)")
print("  This combines twin FE with IV to address measurement error")

# For the differenced IV, we need first twins only
first_twins_iv = first_twins[["dlwage", "deduc", "deduct"]].dropna()

iv_diff = IV2SLS.from_formula(
    "dlwage ~ 0 + [deduc ~ deduct]",
    data=first_twins_iv,
).fit(cov_type="robust")

print(f"\n  Return to schooling (IV-Δ): {iv_diff.params['deduc']:.4f}")
print(f"  Robust SE:                   ({iv_diff.std_errors['deduc']:.4f})")
print(f"  N = {int(iv_diff.nobs)} twin pairs")

# =============================================================================
# SUMMARY TABLE
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: Table 6.2 — Returns to Schooling")
print("=" * 70)
print(f"{'Method':<35} {'Coefficient':>12} {'SE':>10}")
print("─" * 60)
print(f"{'(1) OLS':<35} {ols.params['educ']:>12.4f} ({ols.bse['educ']:.4f})")
print(f"{'(2) Twin differences':<35} {twins_ols.params['deduc']:>12.4f} ({twins_ols.bse['deduc']:.4f})")
print(f"{'(3) IV (levels)':<35} {iv_levels.params['educ']:>12.4f} ({iv_levels.std_errors['educ']:.4f})")
print(f"{'(4) IV (differences)':<35} {iv_diff.params['deduc']:>12.4f} ({iv_diff.std_errors['deduc']:.4f})")

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("""
Pattern of results:
  OLS (~0.11) > Twin FE (~0.06) ≤ IV (~0.08)

What this tells us:
  1. OLS likely OVERSTATES the return (ability bias pushes β₁ up)
  2. Within-twins estimate is LOWER — eliminating shared family factors
     reduces the estimated return, suggesting ability bias is real
  3. IV estimates are between OLS and twins — possibly because IV
     corrects measurement error that biases twin FE downward

The "true" return to schooling is probably 6-8% per year, compared to
the naïve OLS estimate of ~11%. This is still a large and economically
significant return — education pays off, just not quite as much as the
raw correlation suggests.
""")
