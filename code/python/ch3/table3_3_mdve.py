"""
Mastering 'Metrics — Chapter 3, Table 3.3
=========================================
Method: Intent-to-Treat (ITT) and Non-Compliance Analysis
Data: Minneapolis Domestic Violence Experiment (MDVE)

Key Takeaway:
    In many experiments, the treatment ASSIGNED differs from the treatment
    DELIVERED. This table cross-tabulates assignment vs. actual police action,
    revealing the extent of non-compliance in the MDVE.

Causal Inference Concept:
    NON-COMPLIANCE occurs when subjects don't receive their assigned treatment.
    In the MDVE, police were randomly told to arrest, advise, or separate
    domestic violence suspects — but they didn't always follow orders.

    This matters because:
    1. The INTENT-TO-TREAT (ITT) effect measures the effect of ASSIGNMENT
       (what police were told to do), not the effect of actual treatment.
    2. To estimate the effect of ACTUAL TREATMENT on compliers, we need
       INSTRUMENTAL VARIABLES (Chapter 3's main topic).

    The cross-tabulation here shows:
    - Diagonal entries = compliance (police followed assignment)
    - Off-diagonal = non-compliance (police deviated from assignment)
"""

# =============================================================================
# IMPORTS
# =============================================================================
import pandas as pd
import numpy as np

# =============================================================================
# DATA LOADING
# =============================================================================
print("=" * 70)
print("Mastering 'Metrics — Table 3.3")
print("Assigned and delivered treatments in the MDVE")
print("=" * 70)

df = pd.read_stata("../../../data/ch3/mdve.dta")
print(f"\nRaw dataset: {df.shape[0]} cases")

# =============================================================================
# DATA PREPARATION
# =============================================================================
# T_RANDOM: randomly assigned police response
#   1 = Arrest, 2 = Advise, 3 = Separate
# T_FINAL: actual police action taken
#   1 = Arrest, 2 = Advise, 3 = Separate, 4 = Other

# Create readable labels
assignment_map = {1: "Arrest", 2: "Advise", 3: "Separate"}
outcome_map = {1: "Arrest", 2: "Advise", 3: "Separate", 4: "Other"}

df["assigned"] = df["T_RANDOM"].map(assignment_map)
df["delivered"] = df["T_FINAL"].map(outcome_map)

# Drop cases where actual outcome was "Other" (following the Stata code)
df = df[df["T_FINAL"] != 4].copy()
print(f"After dropping 'Other' outcomes: {df.shape[0]} cases")

# =============================================================================
# TABLE 3.3: CROSS-TABULATION OF ASSIGNMENT vs. DELIVERY
# =============================================================================
print("\n" + "─" * 70)
print("CROSS-TABULATION: Assigned Treatment × Delivered Treatment")
print("─" * 70)

# Create the cross-tabulation (counts)
ct = pd.crosstab(
    df["assigned"],
    df["delivered"],
    margins=True,
    margins_name="Total",
)

# Reorder rows and columns to match book
row_order = ["Arrest", "Advise", "Separate", "Total"]
col_order = ["Arrest", "Advise", "Separate", "Total"]
ct = ct.reindex(index=row_order, columns=col_order)

print("\nCounts:")
print(ct.to_string())

# Row and column percentages
print(f"\n{'Assigned':<12} {'Arrest':>10} {'Advise':>10} {'Separate':>10} {'Total (col %)':>15}")
print("─" * 60)

total_n = ct.loc["Total", "Total"]

for row in ["Arrest", "Advise", "Separate"]:
    row_total = ct.loc[row, "Total"]
    arrest_pct = 100 * ct.loc[row, "Arrest"] / row_total
    advise_pct = 100 * ct.loc[row, "Advise"] / row_total
    separate_pct = 100 * ct.loc[row, "Separate"] / row_total
    col_pct = 100 * row_total / total_n

    print(f"{row:<12} {arrest_pct:>7.0f}%    {advise_pct:>7.0f}%    {separate_pct:>7.0f}%    {col_pct:>10.0f}%")
    print(f"{'':>12} ({ct.loc[row, 'Arrest']:>4})     ({ct.loc[row, 'Advise']:>4})     ({ct.loc[row, 'Separate']:>4})     ({row_total:>4})")

# Total row
print("─" * 60)
print(f"{'Total':<12} {100*ct.loc['Total','Arrest']/total_n:>7.0f}%    {100*ct.loc['Total','Advise']/total_n:>7.0f}%    {100*ct.loc['Total','Separate']/total_n:>7.0f}%    {'100%':>10}")
print(f"{'':>12} ({ct.loc['Total', 'Arrest']:>4})     ({ct.loc['Total', 'Advise']:>4})     ({ct.loc['Total', 'Separate']:>4})     ({total_n:>4})")

# =============================================================================
# COMPLIANCE ANALYSIS
# =============================================================================
print("\n" + "─" * 70)
print("COMPLIANCE ANALYSIS")
print("─" * 70)

# Compliance rate: fraction who received their assigned treatment
compliers = ((df["assigned"] == df["delivered"])).sum()
compliance_rate = compliers / len(df)
print(f"\nOverall compliance rate: {compliance_rate:.1%}")
print(f"  ({compliers} out of {len(df)} cases followed their assignment)")

# By assignment group
for group in ["Arrest", "Advise", "Separate"]:
    group_data = df[df["assigned"] == group]
    group_comply = (group_data["delivered"] == group).sum()
    print(f"  Compliance for '{group}' assignment: {group_comply}/{len(group_data)} = {group_comply/len(group_data):.1%}")

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("""
Key observations:
  1. Compliance is imperfect — police often deviate from their random assignment
  2. Those assigned to ARREST have the highest compliance (~91%)
  3. Those assigned to ADVISE or SEPARATE show more crossing over

Why this matters for causal inference:
  • If we compare outcomes by ASSIGNED treatment (ITT), we get a diluted
    estimate of the true treatment effect (because some people didn't get
    their assigned treatment)
  • To recover the causal effect of ACTUAL TREATMENT on compliers, we can
    use the assignment as an INSTRUMENT for actual treatment — this is the
    IV/Wald estimator:

        LATE = ITT effect / Compliance rate

    This is exactly what Chapter 3 teaches: using random assignment as an
    instrument to handle non-compliance via 2SLS.
""")
