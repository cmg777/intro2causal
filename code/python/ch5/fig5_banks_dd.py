"""
Mastering 'Metrics — Chapter 5, Figures 5.1, 5.2, 5.3
=====================================================
Method: Difference-in-Differences (visual/intuition)
Data: Bank failures in the 6th and 8th Federal Reserve Districts

Key Takeaway:
    The 6th Federal Reserve District (Atlanta Fed) intervened to support banks
    during the Great Depression, while the 8th District (St. Louis Fed) did not.
    The divergence in bank failures between these districts reveals the causal
    effect of the Fed's intervention.

Causal Inference Concept:
    DIFFERENCE-IN-DIFFERENCES (DD) compares changes over time in a treatment
    group vs. a control group. The key assumption is PARALLEL TRENDS: absent
    treatment, both groups would have followed the same trajectory.

    Here:
    - Treatment group: 6th District (received Fed support)
    - Control group: 8th District (no support)
    - Before: Pre-crisis (1929)
    - After: Crisis period (1930-1933)

    The COUNTERFACTUAL shows what would have happened to the 6th District's
    banks had the Fed NOT intervened. It is constructed by assuming the
    gap between districts would have remained constant (parallel trends).
"""

# =============================================================================
# IMPORTS
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# =============================================================================
# DATA LOADING
# =============================================================================
print("=" * 70)
print("Mastering 'Metrics — Figures 5.1, 5.2, 5.3")
print("Bank Failures: Difference-in-Differences")
print("=" * 70)

df = pd.read_csv("../../../data/ch5/banks.csv")
print(f"\nDataset: {df.shape[0]} observations")
print(f"Columns: {list(df.columns)}")

# Create proper date column
df["date"] = pd.to_datetime(df[["year", "month", "day"]])

# Create log-transformed variables (for percentage change interpretation)
df["lbib6"] = np.log(df["bib6"])
df["lbib8"] = np.log(df["bib8"])

# =============================================================================
# JULY 1 DATA FOR ANNUAL COMPARISON
# =============================================================================
# The Stata code filters to July 1 observations for the counterfactual
annual = df[(df["month"] == 7) & (df["day"] == 1)].copy().reset_index(drop=True)
print(f"\nJuly 1 observations: {len(annual)} years")
print(annual[["year", "bib6", "bib8"]].to_string(index=False))

# =============================================================================
# COUNTERFACTUAL CONSTRUCTION
# =============================================================================
# The DD counterfactual assumes the gap between districts stays constant
# at its 1930 level. This is the PARALLEL TRENDS assumption in action.

annual["diff"] = annual["bib8"] - annual["bib6"]

# The counterfactual for the 6th district = 8th district banks minus
# the gap that existed in 1930 (the second observation, index 1)
gap_1930 = annual.loc[annual["year"] == 1930, "diff"].values[0]
annual["bibc"] = np.where(
    annual["year"] == 1929,
    annual["bib6"],  # In 1929, counterfactual = actual
    annual["bib8"] - gap_1930,  # After 1929, apply 1930 gap
)

print(f"\nGap in 1930 (8th - 6th district): {gap_1930:.0f} banks")
print("\nCounterfactual comparison:")
print(annual[["year", "bib8", "bib6", "bibc"]].to_string(index=False))

# =============================================================================
# FIGURE 5.1: BANKS IN BUSINESS (1930-1931, SHORT WINDOW)
# =============================================================================
fig1_data = annual[(annual["year"] > 1929) & (annual["year"] < 1932)]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(fig1_data["year"], fig1_data["bib8"], "ko-", markersize=10, linewidth=2, label="8th District")
ax.plot(fig1_data["year"], fig1_data["bib6"], "ks-", markersize=10, linewidth=2, label="6th District")
ax.plot(fig1_data["year"], fig1_data["bibc"], "k^--", markersize=10, linewidth=1.5, label="6th Counterfactual")
ax.set_ylabel("Number of Banks in Business")
ax.set_title("Figure 5.1: Bank failures around the crisis (1930-1931)")
ax.legend()
ax.set_ylim(95, 170)
plt.tight_layout()
plt.savefig("fig5_1_banks.png", dpi=150)
plt.close()
print("\nSaved: fig5_1_banks.png")

# =============================================================================
# FIGURE 5.2: TRENDS (1929-1934)
# =============================================================================
fig2_data = annual[(annual["year"] > 1928) & (annual["year"] < 1935)]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(fig2_data["year"], fig2_data["bib8"], "ko-", markersize=10, linewidth=2, label="8th District")
ax.plot(fig2_data["year"], fig2_data["bib6"], "ks-", markersize=10, linewidth=2, label="6th District")
ax.set_ylabel("Number of Banks in Business")
ax.set_title("Figure 5.2: Trends in bank failures (1929-1934)")
ax.legend()
ax.set_ylim(70, 180)
plt.tight_layout()
plt.savefig("fig5_2_banks_trends.png", dpi=150)
plt.close()
print("Saved: fig5_2_banks_trends.png")

# =============================================================================
# FIGURE 5.3: TRENDS + COUNTERFACTUAL
# =============================================================================
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(fig2_data["year"], fig2_data["bib8"], "ko-", markersize=10, linewidth=2, label="8th District")
ax.plot(fig2_data["year"], fig2_data["bib6"], "ks-", markersize=10, linewidth=2, label="6th District")
ax.plot(fig2_data["year"], fig2_data["bibc"], "k^--", markersize=10, linewidth=1.5, label="6th Counterfactual")
ax.set_ylabel("Number of Banks in Business")
ax.set_title("Figure 5.3: DD counterfactual for the 6th District")
ax.legend()
ax.set_ylim(70, 180)

# Annotate the DD effect
for yr in [1931, 1932, 1933]:
    row = fig2_data[fig2_data["year"] == yr].iloc[0]
    dd_effect = row["bib6"] - row["bibc"]
    ax.annotate(
        f"DD={dd_effect:.0f}",
        xy=(yr, (row["bib6"] + row["bibc"]) / 2),
        fontsize=8,
        ha="left",
        color="red",
    )

plt.tight_layout()
plt.savefig("fig5_3_banks_counterfactual.png", dpi=150)
plt.close()
print("Saved: fig5_3_banks_counterfactual.png")

# =============================================================================
# DD CALCULATION
# =============================================================================
print("\n" + "─" * 70)
print("DIFFERENCE-IN-DIFFERENCES CALCULATION")
print("─" * 70)

# DD = (Change in 6th) - (Change in 8th)
# This is the "treatment effect" of Fed intervention
for yr in [1931, 1932, 1933]:
    pre_6 = annual.loc[annual["year"] == 1930, "bib6"].values[0]
    post_6 = annual.loc[annual["year"] == yr, "bib6"].values[0]
    pre_8 = annual.loc[annual["year"] == 1930, "bib8"].values[0]
    post_8 = annual.loc[annual["year"] == yr, "bib8"].values[0]

    change_6 = post_6 - pre_6
    change_8 = post_8 - pre_8
    dd = change_6 - change_8

    print(f"\n  Year {yr} vs. 1930:")
    print(f"    6th District change: {change_6:+.0f} banks")
    print(f"    8th District change: {change_8:+.0f} banks")
    print(f"    DD estimate: {dd:+.0f} banks (effect of Fed intervention)")

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("""
The DD analysis reveals that Fed intervention SAVED banks:
  • The 6th District (with Fed support) lost fewer banks than the 8th
  • The counterfactual shows what would have happened without intervention
  • The gap between actual and counterfactual = causal effect of the Fed

The parallel trends assumption is key:
  Before the crisis, both districts had similar trends in bank numbers.
  This makes it plausible that without intervention, the 6th District
  would have followed the same trajectory as the 8th.

This is the essence of DD: compare CHANGES (not levels) to eliminate
time-invariant differences between groups. The regression version of DD
(Table 5.2) formalizes this with state and time fixed effects.
""")
