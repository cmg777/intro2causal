"""
Mastering 'Metrics — Chapter 5, Tables 5.2 and 5.3
===================================================
Method: Regression Difference-in-Differences with Fixed Effects
Data: MLDA-induced deaths among 18-20 year olds, 1970-1983

Key Takeaway:
    States that lowered their minimum legal drinking age (MLDA) experienced
    about 7-10 additional deaths per 100,000 among 18-20 year olds,
    concentrated in motor vehicle accidents.

Causal Inference Concept:
    REGRESSION DD uses fixed effects to implement difference-in-differences:
      mrate = β₀ + β₁·legal + αₛ + γₜ + εₛₜ

    Where:
    - αₛ = state fixed effects (absorb time-invariant state differences)
    - γₜ = year fixed effects (absorb nationwide trends)
    - β₁ = DD estimate (effect of legal drinking on death rate)

    The identifying variation comes from states that CHANGED their MLDA
    at different times — some lowered it in the 1970s, others didn't.

    Robustness checks:
    - State-specific linear time trends (more demanding parallel trends)
    - Population-weighted regressions (WLS)
    - Controlling for beer taxes (alternative policy confound)
    - Clustering SEs at the state level (correct for serial correlation)
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
print("=" * 70)
print("Mastering 'Metrics — Tables 5.2 and 5.3")
print("Regression DD: MLDA effects on death rates")
print("=" * 70)

df = pd.read_stata("../../../data/ch5/deaths.dta")
print(f"\nDataset: {df.shape[0]:,} observations")
print(f"Variables: {list(df.columns)}")

# =============================================================================
# SAMPLE SELECTION
# =============================================================================
# The data uses string labels for agegr and dtype
# agegr: '18-20 yrs' is the target age group
# dtype: 'all', 'MVA', 'suicide', 'internal', etc.
# The variable 'beertaxa' in the data corresponds to 'beertax' in the Stata code

# Rename for consistency with Stata code
if "beertaxa" in df.columns and "beertax" not in df.columns:
    df = df.rename(columns={"beertaxa": "beertax"})

sample = df[(df["year"] <= 1983) & (df["agegr"] == "18-20 yrs")].copy()
print(f"Analysis sample (18-20 yr olds, ≤1983): {len(sample):,} obs")

# Convert state and year to standard types for fixed effects
sample["state"] = sample["state"].astype(str)
sample["year_cat"] = sample["year"].astype(int)
sample["year"] = sample["year"].astype(int)

# =============================================================================
# TABLE 5.2: DD REGRESSION ESTIMATES
# =============================================================================
print("\n" + "─" * 90)
print("TABLE 5.2: Regression DD estimates of MLDA effects on death rates")
print("─" * 90)

dtype_labels = {"all": "All causes", "MVA": "MVA", "suicide": "Suicide", "internal": "Internal"}

print(f"\n{'Cause':<15} {'No tr, no w':>14} {'Trends, no w':>14} {'No tr, WLS':>14} {'Trends, WLS':>14}")
print("─" * 75)

for dtype_val, dtype_label in dtype_labels.items():
    s = sample[sample["dtype"] == dtype_val].copy()

    results = []

    # Specification 1: State + Year FE, no trends, no weights
    formula = "mrate ~ legal + C(state) + C(year_cat)"
    r1 = smf.ols(formula, data=s).fit(
        cov_type="cluster", cov_kwds={"groups": s["state"]}
    )
    results.append((r1.params["legal"], r1.bse["legal"]))

    # Specification 2: State + Year FE + state-specific trends, no weights
    # State-specific trends = interaction of state dummies with year
    formula_trend = "mrate ~ legal + C(state) + C(year_cat) + C(state):year"
    r2 = smf.ols(formula_trend, data=s).fit(
        cov_type="cluster", cov_kwds={"groups": s["state"]}
    )
    results.append((r2.params["legal"], r2.bse["legal"]))

    # Specification 3: State + Year FE, no trends, population weights
    r3 = smf.wls(
        "mrate ~ legal + C(state) + C(year_cat)",
        data=s,
        weights=s["pop"],
    ).fit(cov_type="cluster", cov_kwds={"groups": s["state"]})
    results.append((r3.params["legal"], r3.bse["legal"]))

    # Specification 4: State + Year FE + state trends, population weights
    r4 = smf.wls(
        "mrate ~ legal + C(state) + C(year_cat) + C(state):year",
        data=s,
        weights=s["pop"],
    ).fit(cov_type="cluster", cov_kwds={"groups": s["state"]})
    results.append((r4.params["legal"], r4.bse["legal"]))

    coefs = "  ".join([f"{r[0]:>12.2f}" for r in results])
    ses = "  ".join([f"  ({r[1]:>8.2f})" for r in results])
    print(f"{dtype_label:<15} {coefs}")
    print(f"{'':>15} {ses}")

print("─" * 75)
print("Notes: SEs clustered at state level. Columns vary by trends/weights.")

# =============================================================================
# TABLE 5.3: DD WITH BEER TAX CONTROL
# =============================================================================
print("\n" + "─" * 70)
print("TABLE 5.3: DD estimates controlling for beer taxes")
print("─" * 70)

print(f"\n{'Cause':<15} {'No trends':>24} {'With trends':>24}")
print(f"{'':>15} {'legal':>12} {'beertax':>12} {'legal':>12} {'beertax':>12}")
print("─" * 70)

for dtype_val, dtype_label in dtype_labels.items():
    s = sample[sample["dtype"] == dtype_val].dropna(subset=["mrate", "legal", "beertax"]).copy()

    # Without state trends
    r1 = smf.ols(
        "mrate ~ legal + beertax + C(state) + C(year_cat)", data=s
    ).fit(cov_type="cluster", cov_kwds={"groups": s["state"]})

    # With state trends
    r2 = smf.ols(
        "mrate ~ legal + beertax + C(state) + C(year_cat) + C(state):year", data=s
    ).fit(cov_type="cluster", cov_kwds={"groups": s["state"]})

    print(f"{dtype_label:<15} {r1.params['legal']:>10.2f}  {r1.params['beertax']:>10.2f}  {r2.params['legal']:>10.2f}  {r2.params['beertax']:>10.2f}")
    print(f"{'':>15} ({r1.bse['legal']:>8.2f}) ({r1.bse['beertax']:>8.2f}) ({r2.bse['legal']:>8.2f}) ({r2.bse['beertax']:>8.2f})")

print("─" * 70)

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("""
Key findings:
  1. Legal drinking access increases the death rate by ~7-10 per 100,000
  2. The effect is concentrated in MOTOR VEHICLE ACCIDENTS (~5-7 deaths)
  3. Internal causes (unrelated to drinking) show NO effect — a placebo
  4. Results are ROBUST to:
     - Adding state-specific trends
     - Population weighting
     - Controlling for beer taxes

Why fixed effects matter:
  • State FE remove permanent state differences (culture, geography, etc.)
  • Year FE remove nationwide shocks (recessions, federal policy changes)
  • What's left: within-state changes in MLDA policy, which vary across
    states and over time — the identifying variation for DD

Clustering:
  Standard errors are clustered at the state level because:
  1. Treatment (MLDA) varies at the state level
  2. Observations within a state are correlated over time
  Without clustering, we would overstate precision (too-small SEs).
""")
