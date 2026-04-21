"""
Mastering 'Metrics — Chapter 4, Table 4.1 & Figures 4.2, 4.4, 4.5
==================================================================
Method: Regression Discontinuity Design (RDD)
Data: Minimum Legal Drinking Age (MLDA) and mortality (Carpenter & Dobkin 2009)

Key Takeaway:
    Turning 21 causes a sharp ~8 deaths per 100,000 increase in mortality,
    driven primarily by motor vehicle accidents. This is a causal effect
    identified by the sharp discontinuity in legal drinking status at age 21.

Causal Inference Concept:
    REGRESSION DISCONTINUITY exploits situations where treatment is determined
    by whether a "running variable" (here: age) crosses a known threshold
    (here: 21st birthday). Just below 21, you can't legally drink; just above,
    you can. People barely below and barely above the cutoff are essentially
    identical — except one group can legally drink. Any jump in outcomes at the
    cutoff is therefore CAUSAL.

    Key assumptions:
    1. No manipulation of the running variable (people can't choose their birthday)
    2. All other factors vary smoothly at the cutoff
    3. The functional form is correctly specified near the cutoff

    We test robustness by:
    - Varying the polynomial order (linear vs. quadratic)
    - Varying the bandwidth (full sample vs. ages 20-22)
    - Allowing different slopes on each side of the cutoff
"""

# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

# Set plot style
sns.set_style("whitegrid")

# =============================================================================
# DATA LOADING
# =============================================================================
print("=" * 70)
print("Mastering 'Metrics — Table 4.1 & Figures 4.2, 4.4, 4.5")
print("Regression Discontinuity: MLDA and Mortality")
print("=" * 70)

df = pd.read_stata("../../../data/ch4/AEJfigs.dta")
print(f"\nDataset: {df.shape[0]} age cells")
print(f"Age range: {df['agecell'].min():.2f} to {df['agecell'].max():.2f}")

# =============================================================================
# VARIABLE CONSTRUCTION
# =============================================================================
# Center age at the cutoff (21) — this makes the intercept interpretable
# as the predicted value AT the cutoff
df["age"] = df["agecell"] - 21

# Treatment indicator: legally allowed to drink
df["over21"] = (df["agecell"] >= 21).astype(int)

# Polynomial terms for flexible functional form
df["age2"] = df["age"] ** 2

# Interaction terms: allow different slopes on each side of the cutoff
df["over_age"] = df["over21"] * df["age"]
df["over_age2"] = df["over21"] * df["age2"]

# Other causes of death (not in the original categories)
df["ext_oth"] = df["external"] - df["homicide"] - df["suicide"] - df["mva"]

# =============================================================================
# FIGURE 4.2: SHARP RD — ALL-CAUSE MORTALITY
# =============================================================================
print("\n--- Figure 4.2: Linear RD for all-cause mortality ---")

# Fit linear model (same slope both sides)
model_lin = smf.ols("all ~ age + over21", data=df).fit()
df["allfitlin"] = model_lin.predict(df)

# Fit linear model (different slopes each side)
model_lini = smf.ols("all ~ age + over21 + over_age", data=df).fit()
df["allfitlini"] = model_lini.predict(df)

print(f"  Linear (common slope):   over21 coef = {model_lin.params['over21']:.2f}")
print(f"  Linear (different slopes): over21 coef = {model_lini.params['over21']:.2f}")

# Plot Figure 4.2
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df["agecell"], df["all"], color="gray", alpha=0.6, s=30, label="Data")
below = df[df["age"] < 0]
above = df[df["age"] >= 0]
ax.plot(below["agecell"], below["allfitlin"], "k-", linewidth=2)
ax.plot(above["agecell"], above["allfitlin"], "k-", linewidth=2)
ax.axvline(x=21, color="red", linestyle="--", alpha=0.5)
ax.set_xlabel("Age")
ax.set_ylabel("Mortality rate (per 100,000)")
ax.set_title("Figure 4.2: Sharp RD estimate of MLDA mortality effects")
ax.legend()
plt.tight_layout()
plt.savefig("fig4_2_rd_linear.png", dpi=150)
plt.close()
print("  Saved: fig4_2_rd_linear.png")

# =============================================================================
# FIGURE 4.4: LINEAR VS. QUADRATIC
# =============================================================================
print("\n--- Figure 4.4: Linear vs. Quadratic control ---")

# Quadratic with different curvature on each side
model_qi = smf.ols("all ~ age + age2 + over21 + over_age + over_age2", data=df).fit()
df["allfitqi"] = model_qi.predict(df)

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df["agecell"], df["all"], color="gray", alpha=0.6, s=30, label="Data")
below = df[df["age"] < 0]
above = df[df["age"] >= 0]
ax.plot(below["agecell"], below["allfitlin"], "r--", linewidth=2, label="Linear")
ax.plot(above["agecell"], above["allfitlin"], "r--", linewidth=2)
ax.plot(below["agecell"], below["allfitqi"], "k-", linewidth=2, label="Quadratic")
ax.plot(above["agecell"], above["allfitqi"], "k-", linewidth=2)
ax.axvline(x=21, color="red", linestyle="--", alpha=0.3)
ax.set_xlabel("Age")
ax.set_ylabel("Mortality rate (per 100,000)")
ax.set_title("Figure 4.4: Quadratic control in an RD design")
ax.legend()
plt.tight_layout()
plt.savefig("fig4_4_rd_quadratic.png", dpi=150)
plt.close()
print("  Saved: fig4_4_rd_quadratic.png")

# =============================================================================
# FIGURE 4.5: MVA vs. INTERNAL CAUSES
# =============================================================================
print("\n--- Figure 4.5: Motor Vehicle Fatalities vs. Internal Causes ---")

# MVA: quadratic on each side
model_mva = smf.ols("mva ~ age + age2 + over21 + over_age + over_age2", data=df).fit()
df["exfitqi"] = model_mva.predict(df)

# Internal causes: quadratic on each side
model_int = smf.ols("internal ~ age + age2 + over21 + over_age + over_age2", data=df).fit()
df["infitqi"] = model_int.predict(df)

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df["agecell"], df["mva"], color="blue", alpha=0.5, s=25, label="Motor Vehicle Accidents")
ax.scatter(df["agecell"], df["internal"], color="orange", alpha=0.5, s=25, label="Internal Causes")
below = df[df["agecell"] < 21]
above = df[df["agecell"] >= 21]
ax.plot(below["agecell"], below["exfitqi"], "b-", linewidth=2)
ax.plot(above["agecell"], above["exfitqi"], "b-", linewidth=2)
ax.plot(below["agecell"], below["infitqi"], color="orange", linewidth=2)
ax.plot(above["agecell"], above["infitqi"], color="orange", linewidth=2)
ax.axvline(x=21, color="red", linestyle="--", alpha=0.3)
ax.set_xlabel("Age")
ax.set_ylabel("Mortality rate (per 100,000)")
ax.set_title("Figure 4.5: RD estimates by cause of death")
ax.legend()
plt.tight_layout()
plt.savefig("fig4_5_rd_by_cause.png", dpi=150)
plt.close()
print("  Saved: fig4_5_rd_by_cause.png")

# =============================================================================
# TABLE 4.1: RD ESTIMATES WITH MULTIPLE SPECIFICATIONS
# =============================================================================
print("\n" + "─" * 90)
print("Table 4.1: Sharp RD estimates of MLDA effects on mortality")
print("─" * 90)
print(f"{'Outcome':<15} {'Linear':>10} {'Quad':>10} {'Lin(±1)':>10} {'Quad(±1)':>10}")
print("─" * 90)

outcomes = {
    "all": "All causes",
    "mva": "MVA",
    "suicide": "Suicide",
    "homicide": "Homicide",
    "ext_oth": "Ext. other",
    "internal": "Internal",
    "alcohol": "Alcohol",
}

# Narrow bandwidth: ages 20-22 (±1 year around cutoff)
df_narrow = df[(df["agecell"] >= 20) & (df["agecell"] <= 22)]

for var, label in outcomes.items():
    results = []

    # Spec 1: Linear, full sample
    r1 = smf.ols(f"{var} ~ age + over21", data=df).fit(cov_type="HC1")
    results.append((r1.params["over21"], r1.bse["over21"]))

    # Spec 2: Quadratic (interacted), full sample
    r2 = smf.ols(f"{var} ~ age + age2 + over21 + over_age + over_age2", data=df).fit(cov_type="HC1")
    results.append((r2.params["over21"], r2.bse["over21"]))

    # Spec 3: Linear, narrow bandwidth (ages 20-22)
    r3 = smf.ols(f"{var} ~ age + over21", data=df_narrow).fit(cov_type="HC1")
    results.append((r3.params["over21"], r3.bse["over21"]))

    # Spec 4: Quadratic (interacted), narrow bandwidth
    r4 = smf.ols(f"{var} ~ age + age2 + over21 + over_age + over_age2", data=df_narrow).fit(cov_type="HC1")
    results.append((r4.params["over21"], r4.bse["over21"]))

    coefs = "  ".join([f"{r[0]:>8.2f}" for r in results])
    ses = "  ".join([f"({r[1]:>6.2f})" for r in results])
    print(f"{label:<15} {coefs}")
    print(f"{'':>15} {ses}")

print("─" * 90)
print("Notes: Robust standard errors in parentheses.")
print("       Columns 1-2: full sample. Columns 3-4: ages 20-22 only.")

# =============================================================================
# INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("""
The RD design reveals that turning 21 causes:
  • ~7-9 additional deaths per 100,000 (all causes)
  • Most of the effect is driven by MOTOR VEHICLE ACCIDENTS (~4-5 deaths)
  • Internal causes show NO discontinuity (as expected — a placebo check)

Why this is credible:
  1. Age is NOT manipulable (you can't choose your birthday)
  2. The effect appears regardless of polynomial order or bandwidth
  3. Internal causes (unaffected by drinking) show no jump — a built-in placebo

The RD estimate is LOCAL: it tells us about the effect of legal drinking
access for people right at age 21. It may not generalize to other ages.
""")
