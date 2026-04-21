"""
Data Preparation Script — Chapter 1: Randomized Trials
======================================================
This script transforms the raw Stata (.dta) files into clean CSV files
with intuitive column names. Run this once before using the study guide.

Usage:
    python code/python/ch1/prepare_data.py

Output files (saved to data/ch1/):
    - nhis_clean.csv          — NHIS 2009 health and insurance data
    - rand_balance.csv        — RAND HIE baseline characteristics
    - rand_utilization.csv    — RAND HIE health-care use (person-year panel)
    - rand_health_outcomes.csv — RAND HIE exit health measures
"""

import numpy as np
import pandas as pd
from pathlib import Path

# Paths
RAW_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "ch1"
OUT_DIR = RAW_DIR  # save clean files in the same directory

print("=" * 60)
print("Preparing clean datasets for Chapter 1")
print("=" * 60)

# =====================================================================
# 1. NHIS 2009 — Health and insurance comparison
# =====================================================================
print("\n[1/4] NHIS 2009 data...")

df = pd.read_stata(RAW_DIR / "NHIS2009_clean.dta")

# Convert categorical columns (Stata labels like "4 people") to numeric
for col in df.select_dtypes(include="category").columns:
    df[col] = df[col].astype(str).str.extract(r"(\d+)").astype(float)

# Apply sample selection: married adults, ages 26-59, employed household
df = df[(df["marradult"] == 1) & (df["perweight"] != 0)].copy()
df["hi_hsb"] = df.groupby("serial")["hi_hsb1"].transform("mean")
df = df[df["hi_hsb"].notna() & df["hi"].notna()].copy()
df["numfem"] = df.groupby("serial")["fml"].transform("sum")
df = df[df["numfem"] == 1].copy()
df = df[(df["age"] >= 26) & (df["age"] <= 59) & (df["adltempl"] >= 1)].copy()
df["hh_size"] = df.groupby("serial")["serial"].transform("count")
df = df[df["hh_size"] > 1].copy()

# Create clean output with intuitive names
nhis = pd.DataFrame({
    "health": df["hlth"],
    "insurance": df["hi"].astype(int),
    "nonwhite": df["nwhite"],
    "age": df["age"],
    "education": df["yedu"],
    "family_size": df["famsize"],
    "employed": df["empl"],
    "family_income": df["inc"],
    "gender": np.where(df["fml"] == 0, "husband", "wife"),
    "weight": df["perweight"],
})

nhis.to_csv(OUT_DIR / "nhis_clean.csv", index=False)
print(f"  Saved nhis_clean.csv ({len(nhis):,} rows)")

# =====================================================================
# 2. RAND HIE — Baseline characteristics (for balance check)
# =====================================================================
print("\n[2/4] RAND HIE baseline data...")

rand = pd.read_stata(RAW_DIR / "rand_initial_sample_2.dta")

# Create family ID (strip prefix, remove "A")
famid = pd.to_numeric(
    rand["fam_identifier"].str[2:].str.replace("A", "", regex=False),
    errors="coerce",
)

rand_balance = pd.DataFrame({
    "female": rand["female"],
    "nonwhite": rand["blackhisp"],
    "age": rand["age"],
    "education": rand["educper"],
    "family_income": rand["income1cpi"],
    "health_index": rand["ghindx"],
    "cholesterol": rand["cholest"],
    "blood_pressure": rand["systol"],
    "mental_health": rand["mhi"],
    "plan_type": rand["plantype"],
    "plan_free": rand["plantype_1"],
    "plan_deductible": rand["plantype_2"],
    "plan_coinsurance": rand["plantype_3"],
    "any_insurance": rand["plantype"].isin([1, 2, 3]).astype(int),
    "family_id": famid,
})

# Set plan dummies to NaN where plan_type is missing
rand_balance.loc[rand_balance["plan_type"].isna(), "plan_free"] = np.nan

rand_balance.to_csv(OUT_DIR / "rand_balance.csv", index=False)
print(f"  Saved rand_balance.csv ({len(rand_balance):,} rows)")

# =====================================================================
# 3. RAND HIE — Health-care utilization (person-year panel)
# =====================================================================
print("\n[3/4] RAND HIE utilization data...")

py = pd.read_stata(RAW_DIR / "person_years.dta")
spend = pd.read_stata(RAW_DIR / "annual_spend.dta")
hie = py.merge(spend, on=["person", "year"], how="inner")

# Classify 24 original plans into 4 types
hie["plantype"] = np.nan
hie.loc[hie["plan"] == 24, "plantype"] = 1   # Free
hie.loc[hie["plan"].isin([1, 5]), "plantype"] = 2  # Deductible
hie.loc[(hie["plan"] >= 2) & (hie["plan"] <= 4), "plantype"] = 4  # Catastrophic
hie.loc[(hie["plan"] >= 6) & (hie["plan"] <= 8), "plantype"] = 4
hie.loc[(hie["plan"] >= 9) & (hie["plan"] <= 23), "plantype"] = 3  # Coinsurance

# CPI adjustment to constant (1991) dollars
hie["expyear"] = hie["indv_start_year"] + hie["year"] - 1
cpi = {
    1973: 3.07, 1974: 2.76, 1975: 2.53, 1976: 2.39, 1977: 2.24,
    1978: 2.09, 1979: 1.88, 1980: 1.65, 1981: 1.50, 1982: 1.41,
    1983: 1.37, 1984: 1.31, 1985: 1.27,
}
hie["out_inf"] = hie.apply(lambda r: r["outsum"] * cpi.get(r["expyear"], np.nan), axis=1)
hie["inpdol_inf"] = hie.apply(lambda r: r["inpdol"] * cpi.get(r["expyear"], np.nan), axis=1)

famid_hie = pd.to_numeric(
    hie["fam_identifier"].str[2:].str.replace("A", "", regex=False), errors="coerce"
)

rand_util = pd.DataFrame({
    "visits": hie["ftf"],
    "outpatient_expenses": hie["out_inf"],
    "admissions": hie["totadm"],
    "inpatient_expenses": hie["inpdol_inf"],
    "total_expenses": hie["out_inf"] + hie["inpdol_inf"],
    "plan_type": hie["plantype"],
    "plan_free": (hie["plantype"] == 1).astype(int),
    "plan_deductible": (hie["plantype"] == 2).astype(int),
    "plan_coinsurance": (hie["plantype"] == 3).astype(int),
    "any_insurance": hie["plantype"].isin([1, 2, 3]).astype(int),
    "family_id": famid_hie,
})

rand_util.to_csv(OUT_DIR / "rand_utilization.csv", index=False)
print(f"  Saved rand_utilization.csv ({len(rand_util):,} rows)")

# =====================================================================
# 4. RAND HIE — Exit health outcomes
# =====================================================================
print("\n[4/4] RAND HIE health outcomes data...")

rand_health = pd.DataFrame({
    "health_index": rand["ghindxx"],
    "cholesterol": rand["cholestx"],
    "blood_pressure": rand["systolx"],
    "mental_health": rand["mhix"],
    "plan_type": rand["plantype"],
    "plan_free": rand["plantype_1"],
    "plan_deductible": rand["plantype_2"],
    "plan_coinsurance": rand["plantype_3"],
    "any_insurance": rand["plantype"].isin([1, 2, 3]).astype(int),
    "family_id": famid,
})

rand_health.loc[rand_health["plan_type"].isna(), "plan_free"] = np.nan

rand_health.to_csv(OUT_DIR / "rand_health_outcomes.csv", index=False)
print(f"  Saved rand_health_outcomes.csv ({len(rand_health):,} rows)")

print("\n" + "=" * 60)
print("Done! All clean datasets saved to data/ch1/")
print("=" * 60)
