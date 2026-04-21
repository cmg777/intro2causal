"""
Mastering 'Metrics — Chapter 6, Figures 6.3 and 6.4
====================================================
Method: Regression Discontinuity Design (RDD)
Data: Clark & Martorell (2014) — Texas last-chance exam and sheepskin effects

Key Takeaway:
    Barely passing the last-chance high school exit exam sharply increases
    diploma receipt (RD jump ~0.50), but has a modest effect on earnings
    (~$200-400/year). This suggests the "sheepskin" (diploma) effect is
    smaller than often claimed.

Causal Inference Concept:
    This is a SHARP RD at the exam passing cutoff:
    - Running variable: test score relative to the passing threshold
    - Treatment: receiving a high school diploma
    - Outcome 1: diploma receipt (first stage — should show a big jump)
    - Outcome 2: annual earnings (the quantity of interest)

    Methodology:
    - Fit separate polynomials on each side of the cutoff
    - The JUMP at the cutoff is the causal RD estimate
    - Weighted by cell sizes (cell-level data)

    This is a "fuzzy" RD in spirit (not everyone who passes gets a diploma,
    and some who fail get one via other routes), but the analysis uses the
    sharp RD approach on the probability of receiving a diploma.
"""

# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# =============================================================================
# DATA LOADING
# =============================================================================
print("=" * 70)
print("Mastering 'Metrics — Figures 6.3 and 6.4")
print("Sheepskin effects: RD at the last-chance exam cutoff")
print("=" * 70)

df = pd.read_stata("../../../data/ch6/clark_martorell_cellmeans.dta")
print(f"\nDataset: {df.shape[0]} score cells")
print(f"Score range: {df['minscore'].min():.0f} to {df['minscore'].max():.0f}")

# =============================================================================
# VARIABLE CONSTRUCTION
# =============================================================================
# minscore: test score relative to passing cutoff (0 = cutoff)
# receivehsd: fraction receiving high school diploma
# avgearnings: average annual earnings
# n: number of observations in each cell
# person_years: person-year weights for earnings

# Treatment: passed the exam (score >= 0)
df["pass_exam"] = (df["minscore"] >= 0).astype(int)

# Create polynomial terms on each side of the cutoff
# This allows different functional forms left and right of the cutoff
for i in range(1, 5):
    df[f"left_{i}"] = (df["minscore"] ** i) * (1 - df["pass_exam"])
    df[f"right_{i}"] = (df["minscore"] ** i) * df["pass_exam"]

# =============================================================================
# FIGURE 6.3: DIPLOMA RECEIPT (FIRST STAGE)
# =============================================================================
print("\n--- Figure 6.3: Diploma receipt around the cutoff ---")

# Fit 4th-order polynomial on the LEFT (fail) side
left_data = df[df["minscore"] < 0].copy()
left_model = smf.wls(
    "receivehsd ~ pass_exam + left_1 + left_2 + left_3 + left_4",
    data=left_data,
    weights=left_data["n"],
).fit()
# Predict fitted values for left side (including cutoff point)
left_pred_data = df[df["minscore"] <= 0].copy()
left_pred_data["fit"] = left_model.predict(left_pred_data)

# Fit 4th-order polynomial on the RIGHT (pass) side
right_data = df[df["minscore"] >= 0].copy()
right_model = smf.wls(
    "receivehsd ~ pass_exam + right_1 + right_2 + right_3 + right_4",
    data=right_data,
    weights=right_data["n"],
).fit()
right_pred_data = df[df["minscore"] >= 0].copy()
right_pred_data["fit"] = right_model.predict(right_pred_data)

# RD estimate at the cutoff
left_at_cutoff = left_model.predict(pd.DataFrame({
    "pass_exam": [0], "left_1": [0], "left_2": [0], "left_3": [0], "left_4": [0]
})).values[0]
right_at_cutoff = right_model.predict(pd.DataFrame({
    "pass_exam": [1], "right_1": [0], "right_2": [0], "right_3": [0], "right_4": [0]
})).values[0]
rd_diploma = right_at_cutoff - left_at_cutoff

print(f"  Left of cutoff (predicted):  {left_at_cutoff:.4f}")
print(f"  Right of cutoff (predicted): {right_at_cutoff:.4f}")
print(f"  RD jump in diploma receipt:  {rd_diploma:.4f}")

# Plot
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.scatter(df["minscore"], df["receivehsd"], color="black", s=15, alpha=0.6)
ax.plot(left_pred_data["minscore"], left_pred_data["fit"], "k-", linewidth=2)
ax.plot(right_pred_data["minscore"], right_pred_data["fit"], "k-", linewidth=2)
ax.axvline(x=0, color="black", linewidth=0.8)
ax.set_xlim(-30, 15)
ax.set_ylim(0, 1)
ax.set_xlabel("Test score relative to cutoff")
ax.set_ylabel("Fraction receiving diploma")
ax.set_title("Figure 6.3: Last-chance exam scores and Texas sheepskin")
plt.tight_layout()
plt.savefig("fig6_3_sheepskin_diploma.png", dpi=150)
plt.close()
print("  Saved: fig6_3_sheepskin_diploma.png")

# =============================================================================
# FIGURE 6.4: EARNINGS (THE SHEEPSKIN EFFECT)
# =============================================================================
print("\n--- Figure 6.4: Earnings around the cutoff ---")

# Fit polynomial on LEFT side (weighted by person-years)
earn_left = df[(df["minscore"] < 0) & (df["minscore"] >= -30)].copy()
earn_left_model = smf.wls(
    "avgearnings ~ pass_exam + left_1 + left_2 + left_3 + left_4",
    data=earn_left,
    weights=earn_left["person_years"],
).fit()
earn_left_pred = df[df["minscore"] <= 0].copy()
earn_left_pred["fit"] = earn_left_model.predict(earn_left_pred)

# Fit polynomial on RIGHT side
earn_right = df[df["minscore"] >= 0].copy()
earn_right_model = smf.wls(
    "avgearnings ~ pass_exam + right_1 + right_2 + right_3 + right_4",
    data=earn_right,
    weights=earn_right["person_years"],
).fit()
earn_right_pred = df[df["minscore"] >= 0].copy()
earn_right_pred["fit"] = earn_right_model.predict(earn_right_pred)

# RD estimate for earnings
earn_left_at_cutoff = earn_left_model.predict(pd.DataFrame({
    "pass_exam": [0], "left_1": [0], "left_2": [0], "left_3": [0], "left_4": [0]
})).values[0]
earn_right_at_cutoff = earn_right_model.predict(pd.DataFrame({
    "pass_exam": [1], "right_1": [0], "right_2": [0], "right_3": [0], "right_4": [0]
})).values[0]
rd_earnings = earn_right_at_cutoff - earn_left_at_cutoff

print(f"  Left of cutoff (predicted):  ${earn_left_at_cutoff:,.0f}")
print(f"  Right of cutoff (predicted): ${earn_right_at_cutoff:,.0f}")
print(f"  RD jump in earnings:         ${rd_earnings:,.0f}")

# Plot
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.scatter(df["minscore"], df["avgearnings"], color="black", s=15, alpha=0.6)
ax.plot(
    earn_left_pred.loc[earn_left_pred["minscore"] <= 0, "minscore"],
    earn_left_pred.loc[earn_left_pred["minscore"] <= 0, "fit"],
    "k-",
    linewidth=2,
)
ax.plot(
    earn_right_pred.loc[earn_right_pred["minscore"] >= 0, "minscore"],
    earn_right_pred.loc[earn_right_pred["minscore"] >= 0, "fit"],
    "k-",
    linewidth=2,
)
ax.axvline(x=0, color="black", linewidth=0.8)
ax.set_xlim(-30, 15)
ax.set_xlabel("Test score relative to cutoff")
ax.set_ylabel("Annual earnings ($)")
ax.set_title("Figure 6.4: Effect of last-chance exam scores on earnings")
plt.tight_layout()
plt.savefig("fig6_4_sheepskin_earnings.png", dpi=150)
plt.close()
print("  Saved: fig6_4_sheepskin_earnings.png")

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print(f"""
RD Results at the passing cutoff:
  • Diploma receipt jumps by ~{rd_diploma:.0%} (a large, sharp discontinuity)
  • Earnings jump by ~${rd_earnings:,.0f}/year (modest)

The "sheepskin" (credential) effect:
  People just above vs. just below the cutoff have nearly identical
  skills (they scored almost the same on the test). The only difference
  is whether they received a diploma. Therefore:

  Sheepskin effect ≈ ${rd_earnings:,.0f} / {rd_diploma:.2f} ≈ ${rd_earnings/rd_diploma:,.0f}/year

  This suggests the diploma CREDENTIAL itself has a modest effect on
  earnings, beyond what the underlying skills (proxied by test scores)
  already provide. Much of the "education premium" may reflect human
  capital (actual learning) rather than pure signaling (the diploma).
""")
