"""
Mastering 'Metrics — Chapter 1, Table 1.4 Panel A
==================================================
Method: Estimating causal effects from a Randomized Controlled Trial
Data: RAND Health Insurance Experiment (HIE) — person-year panel

Key Takeaway:
    More generous health insurance causes substantially higher health-care
    utilization. The free plan increased outpatient spending by ~68% and
    total expenses by ~45% relative to the catastrophic plan.

Causal Inference Concept:
    Because treatment (insurance plan) was RANDOMLY ASSIGNED, simple
    differences in means between plan groups have a CAUSAL interpretation.
    The regression of outcomes on plan dummies recovers average treatment
    effects — no need to control for confounders (randomization handled that).

    The regression coefficients represent:
        β_free = E[Y | Free plan] - E[Y | Catastrophic plan]
    which, under random assignment, equals the Average Treatment Effect (ATE).
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
print("Mastering 'Metrics — Table 1.4, Panel A (Health-care use)")
print("=" * 70)

# Load person-year data and annual spending data
person_years = pd.read_stata("../../../data/ch1/person_years.dta")
annual_spend = pd.read_stata("../../../data/ch1/annual_spend.dta")

# Merge on person and year (inner join — keep only matched observations)
df = person_years.merge(annual_spend, on=["person", "year"], how="inner")
print(f"\nMerged dataset: {df.shape[0]:,} person-year observations")

# =============================================================================
# PLAN TYPE CLASSIFICATION
# =============================================================================
# Group the 24 original plans into 4 categories:
#   1 = Free (plan 24)
#   2 = Individual Deductible (plans 1, 5)
#   3 = Coinsurance 25-50% (plans 9-23)
#   4 = Catastrophic 95-100% (plans 2-4, 6-8)

df["plantype"] = np.nan
df.loc[df["plan"] == 24, "plantype"] = 1  # Free
df.loc[df["plan"].isin([1, 5]), "plantype"] = 2  # Deductible
df.loc[(df["plan"] >= 2) & (df["plan"] <= 4), "plantype"] = 4  # Catastrophic
df.loc[(df["plan"] >= 6) & (df["plan"] <= 8), "plantype"] = 4  # Catastrophic
df.loc[(df["plan"] >= 9) & (df["plan"] <= 23), "plantype"] = 3  # Coinsurance

# Create plan dummies
df["plantype_1"] = (df["plantype"] == 1).astype(int)
df["plantype_2"] = (df["plantype"] == 2).astype(int)
df["plantype_3"] = (df["plantype"] == 3).astype(int)
df["plantype_4"] = (df["plantype"] == 4).astype(int)
df["any_ins"] = (df["plantype"].isin([1, 2, 3])).astype(int)

# =============================================================================
# INFLATION ADJUSTMENT
# =============================================================================
# Adjust spending to 1991 constant dollars using CPI multipliers
# (The Stata code adjusts to 1985 dollars; we replicate exactly)
df["expyear"] = df["indv_start_year"] + df["year"] - 1

cpi_multipliers = {
    1973: 3.07, 1974: 2.76, 1975: 2.53, 1976: 2.39, 1977: 2.24,
    1978: 2.09, 1979: 1.88, 1980: 1.65, 1981: 1.50, 1982: 1.41,
    1983: 1.37, 1984: 1.31, 1985: 1.27,
}

df["out_inf"] = df.apply(
    lambda row: row["outsum"] * cpi_multipliers.get(row["expyear"], np.nan), axis=1
)
df["inpdol_inf"] = df.apply(
    lambda row: row["inpdol"] * cpi_multipliers.get(row["expyear"], np.nan), axis=1
)
df["tot_inf"] = df["out_inf"] + df["inpdol_inf"]

# Create family ID for clustering
df["famid"] = df["fam_identifier"].str[2:].str.replace("A", "", regex=False)
df["famid"] = pd.to_numeric(df["famid"], errors="coerce")

# =============================================================================
# TABLE 1.4 PANEL A: HEALTH-CARE USE
# =============================================================================
variables = {
    "ftf": "Face-to-face visits",
    "out_inf": "Outpatient expenses",
    "totadm": "Hospital admissions",
    "inpdol_inf": "Inpatient expenses",
    "tot_inf": "Total expenses",
}

print(f"\n{'Variable':<25} {'Cata. mean':>12} {'[SD]':>10} {'Deduct':>10} {'Coins':>10} {'Free':>10} {'Any ins':>10}")
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

    print(f"{label:<25} {cat_mean:>10.0f}  [{cat_sd:>7.0f}]  {deduct_diff:>7.0f}   {coins_diff:>7.0f}   {free_diff:>7.0f}   {any_diff:>7.0f}")
    print(f"{'':>25} {'':>10}  {'':>9}  ({deduct_se:>5.0f})  ({coins_se:>5.0f})  ({free_se:>5.0f})  ({any_se:>5.0f})")

print("─" * 95)

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("""
Key findings from the RAND experiment (Panel A):
  1. The FREE PLAN increased outpatient spending by ~$169 (68% above catastrophic)
  2. Hospital admissions rose modestly (~0.03 more per year)
  3. Total expenses rose ~$285 (45% increase)
  4. Even the COINSURANCE plans (25-50% cost-sharing) raised utilization

Economic lesson: MORAL HAZARD is real.
  When insurance reduces the price of care to zero, people consume substantially
  more health care. This is the demand curve at work — lower prices mean higher
  quantity demanded. The policy question is whether this extra utilization
  actually improves health (see Panel B, Table 1.4b).
""")
