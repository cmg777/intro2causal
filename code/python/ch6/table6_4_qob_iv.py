"""
Mastering 'Metrics — Chapter 6, Tables 6.4 & 6.5; Figures 6.1 & 6.2
====================================================================
Method: Instrumental Variables using Quarter of Birth (Angrist & Krueger 1991)
Data: 1980 U.S. Census — men born 1930-1939

Key Takeaway:
    Quarter of birth affects school entry age, which affects total schooling
    (via compulsory schooling laws). Using QOB as an instrument, the IV
    estimate of returns to schooling is ~0.08-0.10 per year.

Causal Inference Concept:
    THE IV RECIPE (Wald Estimator):
    When you have a single binary instrument Z:

        IV estimate = Reduced Form / First Stage
                    = (Effect of Z on Y) / (Effect of Z on X)
                    = Cov(Y,Z)/Var(Z) ÷ Cov(X,Z)/Var(Z)

    Here:
    - Y = log weekly earnings
    - X = years of schooling (endogenous)
    - Z = born in Q4 dummy (instrument)

    Why QOB works as an instrument:
    1. RELEVANCE: Children born in Q4 start school younger (due to cutoff
       dates) → they reach the compulsory schooling age with MORE years of
       school → slightly MORE education on average
    2. EXCLUSION: Season of birth shouldn't directly affect earnings
       (debatable — see discussion of weak instruments)

    Table 6.4 shows the Wald recipe step by step.
    Table 6.5 compares OLS and IV across specifications.
    Figures 6.1-6.2 visualize the first stage and reduced form.
"""

# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
import pandas as pd
import pyfixest as pf
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# =============================================================================
# DATA LOADING
# =============================================================================
print("=" * 70)
print("Mastering 'Metrics — Tables 6.4, 6.5 & Figures 6.1, 6.2")
print("Quarter of Birth IV estimates of returns to schooling")
print("=" * 70)

df = pd.read_stata("../../../data/ch6/ak91.dta")
print(f"\nDataset: {df.shape[0]:,} men born 1930-1939")

# Create quarter of birth dummies
df["q1"] = (df["qob"] == 1).astype(int)
df["q2"] = (df["qob"] == 2).astype(int)
df["q3"] = (df["qob"] == 3).astype(int)
df["q4"] = (df["qob"] == 4).astype(int)

# Create age variable (for collapsing later)
df["age"] = ((79 - df["yob"]) * 4 + 5 - df["qob"]) / 4
df["age2"] = df["age"] ** 2

# =============================================================================
# TABLE 6.4: THE IV RECIPE (WALD ESTIMATOR)
# =============================================================================
print("\n" + "─" * 70)
print("TABLE 6.4: IV Recipe — Step by Step")
print("─" * 70)

# REDUCED FORM: Effect of Q4 birth on earnings (Y on Z)
rf = pf.feols("lnw ~ q4", data=df, vcov="hetero")
rf_coef = rf.coef()["q4"]
rf_se = rf.se()["q4"]
rf_q1_mean = rf.coef()["Intercept"]  # Mean for Q1-Q3
rf_q4_mean = rf.coef()["Intercept"] + rf.coef()["q4"]  # Mean for Q4

print(f"\n  STEP 1: Reduced Form (earnings on Q4 dummy)")
print(f"    Mean log earnings (Q1-Q3): {rf_q1_mean:.4f}")
print(f"    Mean log earnings (Q4):    {rf_q4_mean:.4f}")
print(f"    Difference (Q4 - rest):    {rf_coef:.4f}  ({rf_se:.4f})")

# FIRST STAGE: Effect of Q4 birth on schooling (X on Z)
fs = pf.feols("s ~ q4", data=df, vcov="hetero")
fs_coef = fs.coef()["q4"]
fs_se = fs.se()["q4"]
fs_q1_mean = fs.coef()["Intercept"]
fs_q4_mean = fs.coef()["Intercept"] + fs.coef()["q4"]

print(f"\n  STEP 2: First Stage (schooling on Q4 dummy)")
print(f"    Mean schooling (Q1-Q3): {fs_q1_mean:.4f}")
print(f"    Mean schooling (Q4):    {fs_q4_mean:.4f}")
print(f"    Difference (Q4 - rest): {fs_coef:.4f}  ({fs_se:.4f})")

# WALD ESTIMATE: Reduced form / First stage
wald = rf_coef / fs_coef
print(f"\n  STEP 3: Wald Estimate = Reduced Form / First Stage")
print(f"    IV estimate = {rf_coef:.4f} / {fs_coef:.4f} = {wald:.4f}")

# Verify with 2SLS
iv_check = pf.feols("lnw ~ 1 | s ~ q4", data=df, vcov="hetero")
print(f"    2SLS check:  {iv_check.coef()['s']:.4f}  ({iv_check.se()['s']:.4f})")

# =============================================================================
# TABLE 6.5: REGRESSION ESTIMATES ACROSS SPECIFICATIONS
# =============================================================================
print("\n" + "─" * 70)
print("TABLE 6.5: Returns to schooling — OLS vs IV specifications")
print("─" * 70)

# Column 1: OLS, no controls
ols1 = pf.feols("lnw ~ s", data=df, vcov="hetero")
print(f"\n  (1) OLS, no controls:           {ols1.coef()['s']:.4f}  ({ols1.se()['s']:.4f})")

# Column 2: IV with Q4 only, no controls
# First stage F-stat (single instrument: t² = F)
fs2 = pf.feols("s ~ q4", data=df, vcov="hetero")
f_stat2 = fs2.tstat()["q4"] ** 2
iv2 = pf.feols("lnw ~ 1 | s ~ q4", data=df, vcov="hetero")
print(f"  (2) IV (Q4), no controls:       {iv2.coef()['s']:.4f}  ({iv2.se()['s']:.4f})  F={f_stat2:.1f}")

# Column 3: OLS with year-of-birth FE (absorbed)
ols3 = pf.feols("lnw ~ s | yob", data=df, vcov="hetero")
print(f"  (3) OLS + YOB FE:               {ols3.coef()['s']:.4f}  ({ols3.se()['s']:.4f})")

# Column 4: IV (Q4) with year-of-birth FE (absorbed)
fs4 = pf.feols("s ~ q4 | yob", data=df, vcov="hetero")
f_stat4 = fs4.tstat()["q4"] ** 2
iv4 = pf.feols("lnw ~ 1 | yob | s ~ q4", data=df, vcov="hetero")
print(f"  (4) IV (Q4) + YOB FE:           {iv4.coef()['s']:.4f}  ({iv4.se()['s']:.4f})  F={f_stat4:.1f}")

# Column 5: IV with all quarter dummies + YOB FE (multiple instruments)
fs5 = pf.feols("s ~ q2 + q3 + q4 | yob", data=df, vcov="hetero")
# Joint F-test on 3 instruments using Wald test
coefs5 = np.array([fs5.coef()['q2'], fs5.coef()['q3'], fs5.coef()['q4']])
idx5 = [list(fs5.coef().index).index(v) for v in ['q2', 'q3', 'q4']]
V5 = fs5._vcov[np.ix_(idx5, idx5)]
f_stat5 = float(coefs5 @ np.linalg.inv(V5) @ coefs5 / 3)
iv5 = pf.feols("lnw ~ 1 | yob | s ~ q2 + q3 + q4", data=df, vcov="hetero")
print(f"  (5) IV (all QOB) + YOB FE:      {iv5.coef()['s']:.4f}  ({iv5.se()['s']:.4f})  F={f_stat5:.1f}")

# =============================================================================
# FIGURES 6.1 AND 6.2: FIRST STAGE AND REDUCED FORM
# =============================================================================
print("\n--- Generating Figures 6.1 and 6.2 ---")

# Collapse to cell means by age (= birth cohort)
cell = df.groupby("age").agg(
    s=("s", "mean"),
    lnw=("lnw", "mean"),
    q1=("q1", "mean"),
    q4=("q4", "mean"),
).reset_index()

# Reconstruct year of birth from age
cell["yob"] = 80 - cell["age"]

# Identify Q1 and Q4 cohorts (those where most people were born in that quarter)
# A cohort is "Q4" if the average q4 indicator is highest, etc.
cell["is_q4"] = cell["q4"] > 0.5
cell["is_q1"] = cell["q1"] > 0.5

# Figure 6.1: First Stage — Education by Year of Birth
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(cell["yob"], cell["s"], "k-", linewidth=1, alpha=0.5)
q4_pts = cell[cell["is_q4"]]
q1_pts = cell[cell["is_q1"]]
other = cell[~cell["is_q4"] & ~cell["is_q1"]]
ax.scatter(q4_pts["yob"], q4_pts["s"], color="black", s=60, zorder=5, label="Quarter 4")
ax.scatter(q1_pts["yob"], q1_pts["s"], facecolors="none", edgecolors="black", s=60, zorder=5, label="Quarter 1")
ax.set_xlabel("Year of Birth")
ax.set_ylabel("Years of Education")
ax.set_title("Figure 6.1: First Stage — Education by Year of Birth")
ax.legend()
plt.tight_layout()
plt.savefig("fig6_1_first_stage.png", dpi=150)
plt.close()
print("  Saved: fig6_1_first_stage.png")

# Figure 6.2: Reduced Form — Earnings by Year of Birth
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(cell["yob"], cell["lnw"], "k-", linewidth=1, alpha=0.5)
ax.scatter(q4_pts["yob"], q4_pts["lnw"], color="black", s=60, zorder=5, label="Quarter 4")
ax.scatter(q1_pts["yob"], q1_pts["lnw"], facecolors="none", edgecolors="black", s=60, zorder=5, label="Quarter 1")
ax.set_xlabel("Year of Birth")
ax.set_ylabel("Log Weekly Earnings")
ax.set_title("Figure 6.2: Reduced Form — Earnings by Year of Birth")
ax.legend()
plt.tight_layout()
plt.savefig("fig6_2_reduced_form.png", dpi=150)
plt.close()
print("  Saved: fig6_2_reduced_form.png")

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("""
The Angrist-Krueger (1991) quarter of birth strategy:
  • Q4 births → start school at younger age → more schooling by the time
    they can legally drop out → slightly higher education on average
  • The first-stage effect is small (~0.1 years) but significant
  • The IV estimate (~0.08-0.10) is close to OLS

Figures show the patterns visually:
  • Fig 6.1: Q1 cohorts (open circles) have slightly LESS education
  • Fig 6.2: Q1 cohorts also have slightly LOWER earnings
  • The ratio of these two patterns = the IV estimate

Important caveats:
  1. The first-stage F-statistic may be marginal — weak instruments can
     cause biased and unreliable IV estimates
  2. Adding more instruments (all quarters) improves the first stage but
     raises concerns about over-identification
  3. Later work questioned whether QOB truly satisfies the exclusion
     restriction (birth timing correlates with family characteristics)
""")
