"""
Mastering 'Metrics — Chapter 6, Table 6.3
=========================================
Method: Instrumental Variables (IV/2SLS) with multiple instruments
Data: Angrist-Acemoglu child labor law data

Key Takeaway:
    Compulsory schooling laws (child labor laws) provide valid instruments
    for education. IV estimates of the return to schooling are ~0.07-0.10,
    broadly consistent with the twins-based estimates.

Causal Inference Concept:
    IV ESTIMATION uses an instrument Z that:
    1. RELEVANCE: Z is correlated with the endogenous variable X (education)
       → Tested via the first-stage F-statistic (rule of thumb: F > 10)
    2. EXCLUSION: Z affects Y (wages) ONLY through X (education)
       → Cannot be tested directly — requires economic reasoning

    Here, compulsory schooling laws (cl7, cl8, cl9) are instruments:
    - cl7: required to enter school by age 7
    - cl8: required to enter school by age 8
    - cl9: required to enter school by age 9

    These laws affect how much schooling people get (relevance) but
    shouldn't directly affect wages except through education (exclusion).

    The IV recipe:
    - First stage:  education = π₀ + π₁·cl7 + π₂·cl8 + π₃·cl9 + controls + ε
    - Reduced form:  wages = γ₀ + γ₁·cl7 + γ₂·cl8 + γ₃·cl9 + controls + ν
    - Second stage: wages = β₀ + β₁·education_hat + controls + u
"""

# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels.iv import IV2SLS

# =============================================================================
# DATA LOADING
# =============================================================================
print("=" * 70)
print("Mastering 'Metrics — Table 6.3")
print("Returns to schooling using child labor law instruments")
print("=" * 70)

df = pd.read_stata("../../../data/ch6/AA_small.dta")
print(f"\nDataset: {df.shape[0]:,} observations")

# =============================================================================
# FIRST STAGE: Do compulsory schooling laws predict education?
# =============================================================================
print("\n" + "─" * 70)
print("FIRST STAGE: Effect of compulsory schooling laws on education")
print("─" * 70)
print("  Model: education = π₀ + π·CL + year FE + YOB FE + SOB FE + ε")
print("  Key question: Do the instruments predict education? (Need F > 10)")

# Specification 1: Basic fixed effects
fs1 = smf.wls(
    "indEduc ~ C(year) + C(yob) + C(sob) + cl7 + cl8 + cl9",
    data=df,
    weights=df["weight"],
).fit(cov_type="cluster", cov_kwds={"groups": df["sob"]})

# F-test on instruments
f_test1 = fs1.f_test("cl7 = 0, cl8 = 0, cl9 = 0")
f_stat1 = float(np.atleast_1d(f_test1.fvalue).flat[0])

print(f"\n  Spec 1 (year + YOB + SOB FE):")
print(f"    cl7:  {fs1.params['cl7']:>8.4f}  ({fs1.bse['cl7']:.4f})")
print(f"    cl8:  {fs1.params['cl8']:>8.4f}  ({fs1.bse['cl8']:.4f})")
print(f"    cl9:  {fs1.params['cl9']:>8.4f}  ({fs1.bse['cl9']:.4f})")
print(f"    F-stat on instruments: {f_stat1:.2f}")

# Specification 2: Add state-of-birth × year-of-birth interactions
# This is more demanding — it absorbs state-cohort trends
fs2 = smf.wls(
    "indEduc ~ C(year) + C(yob) + C(sob) + C(sob):yob + cl7 + cl8 + cl9",
    data=df,
    weights=df["weight"],
).fit(cov_type="cluster", cov_kwds={"groups": df["sob"]})

f_test2 = fs2.f_test("cl7 = 0, cl8 = 0, cl9 = 0")
f_stat2 = float(np.atleast_1d(f_test2.fvalue).flat[0])

print(f"\n  Spec 2 (+ SOB × YOB interactions):")
print(f"    cl7:  {fs2.params['cl7']:>8.4f}  ({fs2.bse['cl7']:.4f})")
print(f"    cl8:  {fs2.params['cl8']:>8.4f}  ({fs2.bse['cl8']:.4f})")
print(f"    cl9:  {fs2.params['cl9']:>8.4f}  ({fs2.bse['cl9']:.4f})")
print(f"    F-stat on instruments: {f_stat2:.2f}")

# =============================================================================
# REDUCED FORM: Effect of laws directly on wages
# =============================================================================
print("\n" + "─" * 70)
print("REDUCED FORM: Effect of compulsory schooling laws on wages")
print("─" * 70)
print("  If laws affect wages ONLY through education, reduced form / first")
print("  stage should equal the IV estimate of the return to schooling.")

rf1 = smf.wls(
    "lnwkwage ~ C(year) + C(yob) + C(sob) + cl7 + cl8 + cl9",
    data=df,
    weights=df["weight"],
).fit(cov_type="cluster", cov_kwds={"groups": df["sob"]})

print(f"\n  Spec 1:")
print(f"    cl7:  {rf1.params['cl7']:>8.4f}  ({rf1.bse['cl7']:.4f})")
print(f"    cl8:  {rf1.params['cl8']:>8.4f}  ({rf1.bse['cl8']:.4f})")
print(f"    cl9:  {rf1.params['cl9']:>8.4f}  ({rf1.bse['cl9']:.4f})")

rf2 = smf.wls(
    "lnwkwage ~ C(year) + C(yob) + C(sob) + C(sob):yob + cl7 + cl8 + cl9",
    data=df,
    weights=df["weight"],
).fit(cov_type="cluster", cov_kwds={"groups": df["sob"]})

print(f"\n  Spec 2 (+ SOB × YOB):")
print(f"    cl7:  {rf2.params['cl7']:>8.4f}  ({rf2.bse['cl7']:.4f})")
print(f"    cl8:  {rf2.params['cl8']:>8.4f}  ({rf2.bse['cl8']:.4f})")
print(f"    cl9:  {rf2.params['cl9']:>8.4f}  ({rf2.bse['cl9']:.4f})")

# =============================================================================
# OLS AND IV (2SLS) ESTIMATES
# =============================================================================
print("\n" + "─" * 70)
print("OLS AND IV (2SLS) ESTIMATES OF RETURNS TO SCHOOLING")
print("─" * 70)

# OLS Spec 1
ols1 = smf.wls(
    "lnwkwage ~ indEduc + C(year) + C(yob) + C(sob)",
    data=df,
    weights=df["weight"],
).fit(cov_type="cluster", cov_kwds={"groups": df["sob"]})

print(f"\n  OLS Spec 1:     {ols1.params['indEduc']:.4f}  ({ols1.bse['indEduc']:.4f})")

# OLS Spec 2 (with SOB × YOB)
ols2 = smf.wls(
    "lnwkwage ~ indEduc + C(year) + C(yob) + C(sob) + C(sob):yob",
    data=df,
    weights=df["weight"],
).fit(cov_type="cluster", cov_kwds={"groups": df["sob"]})

print(f"  OLS Spec 2:     {ols2.params['indEduc']:.4f}  ({ols2.bse['indEduc']:.4f})")

# IV Spec 1: Using linearmodels IV2SLS
# For large FE models, we residualize (partial out) the fixed effects first,
# then run IV on the residuals. This is the Frisch-Waugh-Lovell approach.
print("\n  Running IV/2SLS estimation...")
print("  (Using residualization to handle many fixed effects)")

from linearmodels.iv import IV2SLS

# Create FE dummies for residualization
iv_df = df[["lnwkwage", "indEduc", "cl7", "cl8", "cl9", "weight", "sob", "year", "yob"]].dropna().copy()

# Residualize: partial out year, yob, sob fixed effects from all variables
def residualize(data, y_col, fe_cols):
    """Partial out fixed effects using OLS (Frisch-Waugh-Lovell)."""
    formula = f"{y_col} ~ " + " + ".join([f"C({c})" for c in fe_cols])
    res = smf.wls(formula, data=data, weights=data["weight"]).fit()
    return res.resid

fe_vars = ["year", "yob", "sob"]
for var in ["lnwkwage", "indEduc", "cl7", "cl8", "cl9"]:
    iv_df[f"{var}_r"] = residualize(iv_df, var, fe_vars)

iv1 = IV2SLS.from_formula(
    "lnwkwage_r ~ 0 + [indEduc_r ~ cl7_r + cl8_r + cl9_r]",
    data=iv_df,
    weights=iv_df["weight"],
).fit(cov_type="clustered", clusters=iv_df["sob"])

print(f"  IV Spec 1:      {iv1.params['indEduc_r']:.4f}  ({iv1.std_errors['indEduc_r']:.4f})")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: Table 6.3 — Returns to Schooling")
print("=" * 70)
print(f"{'Method':<25} {'Coefficient':>12} {'SE':>10}")
print("─" * 50)
print(f"{'OLS (Spec 1)':<25} {ols1.params['indEduc']:>12.4f} ({ols1.bse['indEduc']:.4f})")
print(f"{'OLS (Spec 2)':<25} {ols2.params['indEduc']:>12.4f} ({ols2.bse['indEduc']:.4f})")
print(f"{'IV/2SLS (Spec 1)':<25} {iv1.params['indEduc_r']:>12.4f} ({iv1.std_errors['indEduc_r']:.4f})")
print(f"{'First-stage F':<25} {f_stat1:>12.2f}")

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("""
The IV estimates using compulsory schooling laws suggest:
  • OLS return: ~7% per year of schooling
  • IV return: ~7-10% per year of schooling

The IV estimate is close to (or slightly higher than) OLS, which differs
from the twins results where OLS was higher than the causal estimate.

Possible explanations:
  1. The LATE (Local Average Treatment Effect) from compulsory laws applies
     to people whose schooling was changed BY the laws — these "compliers"
     may have higher returns than average
  2. Measurement error in education biases OLS downward, partially offsetting
     ability bias that pushes it upward

The first-stage F-statistic is crucial:
  • F > 10 suggests instruments are "strong" (rule of thumb: Staiger & Stock)
  • Weak instruments can cause severe bias in IV estimates
""")
