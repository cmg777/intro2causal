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
import pyfixest as pf

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

# Specification 1: Basic fixed effects (absorbed via | syntax)
fs1 = pf.feols(
    "indEduc ~ cl7 + cl8 + cl9 | sob + yob + year",
    data=df, weights="weight", vcov={"CRV1": "sob"},
)

# Joint F-test on instruments using Wald test
coefs1 = np.array([fs1.coef()['cl7'], fs1.coef()['cl8'], fs1.coef()['cl9']])
idx1 = [list(fs1.coef().index).index(v) for v in ['cl7', 'cl8', 'cl9']]
V1 = fs1._vcov[np.ix_(idx1, idx1)]
f_stat1 = float(coefs1 @ np.linalg.inv(V1) @ coefs1 / 3)

print(f"\n  Spec 1 (year + YOB + SOB FE):")
print(f"    cl7:  {fs1.coef()['cl7']:>8.4f}  ({fs1.se()['cl7']:.4f})")
print(f"    cl8:  {fs1.coef()['cl8']:>8.4f}  ({fs1.se()['cl8']:.4f})")
print(f"    cl9:  {fs1.coef()['cl9']:>8.4f}  ({fs1.se()['cl9']:.4f})")
print(f"    F-stat on instruments: {f_stat1:.2f}")

# Specification 2: Add state-of-birth × year-of-birth interactions
# This is more demanding — it absorbs state-cohort trends
fs2 = pf.feols(
    "indEduc ~ cl7 + cl8 + cl9 + i(sob, yob) | sob + yob + year",
    data=df, weights="weight", vcov={"CRV1": "sob"},
)

coefs2 = np.array([fs2.coef()['cl7'], fs2.coef()['cl8'], fs2.coef()['cl9']])
idx2 = [list(fs2.coef().index).index(v) for v in ['cl7', 'cl8', 'cl9']]
V2 = fs2._vcov[np.ix_(idx2, idx2)]
f_stat2 = float(coefs2 @ np.linalg.inv(V2) @ coefs2 / 3)

print(f"\n  Spec 2 (+ SOB × YOB interactions):")
print(f"    cl7:  {fs2.coef()['cl7']:>8.4f}  ({fs2.se()['cl7']:.4f})")
print(f"    cl8:  {fs2.coef()['cl8']:>8.4f}  ({fs2.se()['cl8']:.4f})")
print(f"    cl9:  {fs2.coef()['cl9']:>8.4f}  ({fs2.se()['cl9']:.4f})")
print(f"    F-stat on instruments: {f_stat2:.2f}")

# =============================================================================
# REDUCED FORM: Effect of laws directly on wages
# =============================================================================
print("\n" + "─" * 70)
print("REDUCED FORM: Effect of compulsory schooling laws on wages")
print("─" * 70)
print("  If laws affect wages ONLY through education, reduced form / first")
print("  stage should equal the IV estimate of the return to schooling.")

rf1 = pf.feols(
    "lnwkwage ~ cl7 + cl8 + cl9 | sob + yob + year",
    data=df, weights="weight", vcov={"CRV1": "sob"},
)

print(f"\n  Spec 1:")
print(f"    cl7:  {rf1.coef()['cl7']:>8.4f}  ({rf1.se()['cl7']:.4f})")
print(f"    cl8:  {rf1.coef()['cl8']:>8.4f}  ({rf1.se()['cl8']:.4f})")
print(f"    cl9:  {rf1.coef()['cl9']:>8.4f}  ({rf1.se()['cl9']:.4f})")

rf2 = pf.feols(
    "lnwkwage ~ cl7 + cl8 + cl9 + i(sob, yob) | sob + yob + year",
    data=df, weights="weight", vcov={"CRV1": "sob"},
)

print(f"\n  Spec 2 (+ SOB × YOB):")
print(f"    cl7:  {rf2.coef()['cl7']:>8.4f}  ({rf2.se()['cl7']:.4f})")
print(f"    cl8:  {rf2.coef()['cl8']:>8.4f}  ({rf2.se()['cl8']:.4f})")
print(f"    cl9:  {rf2.coef()['cl9']:>8.4f}  ({rf2.se()['cl9']:.4f})")

# =============================================================================
# OLS AND IV (2SLS) ESTIMATES
# =============================================================================
print("\n" + "─" * 70)
print("OLS AND IV (2SLS) ESTIMATES OF RETURNS TO SCHOOLING")
print("─" * 70)

# OLS Spec 1
ols1 = pf.feols(
    "lnwkwage ~ indEduc | sob + yob + year",
    data=df, weights="weight", vcov={"CRV1": "sob"},
)

print(f"\n  OLS Spec 1:     {ols1.coef()['indEduc']:.4f}  ({ols1.se()['indEduc']:.4f})")

# OLS Spec 2 (with SOB × YOB)
ols2 = pf.feols(
    "lnwkwage ~ indEduc + i(sob, yob) | sob + yob + year",
    data=df, weights="weight", vcov={"CRV1": "sob"},
)

print(f"  OLS Spec 2:     {ols2.coef()['indEduc']:.4f}  ({ols2.se()['indEduc']:.4f})")

# IV Spec 1: pyfixest handles IV with absorbed FE natively
# Formula: outcome ~ controls | FE | endogenous ~ instruments
print("\n  Running IV/2SLS estimation...")

iv1 = pf.feols(
    "lnwkwage ~ 1 | sob + yob + year | indEduc ~ cl7 + cl8 + cl9",
    data=df, weights="weight", vcov={"CRV1": "sob"},
)

print(f"  IV Spec 1:      {iv1.coef()['indEduc']:.4f}  ({iv1.se()['indEduc']:.4f})")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: Table 6.3 — Returns to Schooling")
print("=" * 70)
print(f"{'Method':<25} {'Coefficient':>12} {'SE':>10}")
print("─" * 50)
print(f"{'OLS (Spec 1)':<25} {ols1.coef()['indEduc']:>12.4f} ({ols1.se()['indEduc']:.4f})")
print(f"{'OLS (Spec 2)':<25} {ols2.coef()['indEduc']:>12.4f} ({ols2.se()['indEduc']:.4f})")
print(f"{'IV/2SLS (Spec 1)':<25} {iv1.coef()['indEduc']:>12.4f} ({iv1.se()['indEduc']:.4f})")
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
