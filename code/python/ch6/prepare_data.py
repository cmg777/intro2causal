"""Data Preparation — Chapter 6: The Wages of Schooling"""
import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "ch6"

# --- Twins data ---
tw = pd.read_stata(DATA_DIR / "pubtwins.dta")
pd.DataFrame({
    "lwage": tw["lwage"], "educ": tw["educ"], "educt_t": tw["educt_t"],
    "age": tw["age"], "age2": tw["age2"] / 100,
    "female": tw["female"], "white": tw["white"], "first": tw["first"],
    "dlwage": tw["dlwage"], "deduc": tw["deduc"], "deduct": tw["deduct"],
}).to_csv(DATA_DIR / "twins_clean.csv", index=False)
print(f"Saved twins_clean.csv ({len(tw)} rows)")

# --- Quarter of birth data ---
ak = pd.read_stata(DATA_DIR / "ak91.dta")
ak["q1"] = (ak["qob"] == 1).astype(int)
ak["q2"] = (ak["qob"] == 2).astype(int)
ak["q3"] = (ak["qob"] == 3).astype(int)
ak["q4"] = (ak["qob"] == 4).astype(int)
ak["age"] = ((79 - ak["yob"]) * 4 + 5 - ak["qob"]) / 4
pd.DataFrame({
    "lnw": ak["lnw"], "s": ak["s"], "qob": ak["qob"].astype(int),
    "yob": ak["yob"].astype(int),
    "q1": ak["q1"], "q2": ak["q2"], "q3": ak["q3"], "q4": ak["q4"],
    "age": ak["age"],
}).to_csv(DATA_DIR / "qob_clean.csv", index=False)
print(f"Saved qob_clean.csv ({len(ak)} rows)")

# --- Sheepskin RD data ---
cm = pd.read_stata(DATA_DIR / "clark_martorell_cellmeans.dta")
out = pd.DataFrame({
    "minscore": cm["minscore"],
    "pass_exam": (cm["minscore"] >= 0).astype(int),
    "receivehsd": cm["receivehsd"],
    "avgearnings": cm["avgearnings"],
    "n": cm["n"], "person_years": cm["person_years"],
})
for i in range(1, 5):
    out[f"left_{i}"] = (cm["minscore"] ** i) * (cm["minscore"] < 0).astype(int)
    out[f"right_{i}"] = (cm["minscore"] ** i) * (cm["minscore"] >= 0).astype(int)
out.to_csv(DATA_DIR / "sheepskin_clean.csv", index=False)
print(f"Saved sheepskin_clean.csv ({len(out)} rows)")

# --- Child labor law data (collapsed to cell means) ---
aa = pd.read_stata(DATA_DIR / "AA_small.dta")
# Instruments (cl7, cl8, cl9) vary at state-of-birth × year-of-birth level,
# so collapsing to (sob, yob, year) cell means preserves all instrument variation.
# WLS on cell means with analytical weights ≈ individual-level WLS.
collapsed = aa.groupby(["sob", "yob", "year"]).agg(
    lnwkwage=("lnwkwage", lambda x: np.average(x, weights=aa.loc[x.index, "weight"])),
    indEduc=("indEduc", lambda x: np.average(x, weights=aa.loc[x.index, "weight"])),
    cl7=("cl7", "first"),
    cl8=("cl8", "first"),
    cl9=("cl9", "first"),
    weight=("weight", "sum"),
    n=("lnwkwage", "count"),
).reset_index()
collapsed.to_csv(DATA_DIR / "childlabor_clean.csv", index=False)
print(f"Saved childlabor_clean.csv ({len(collapsed)} rows)")
