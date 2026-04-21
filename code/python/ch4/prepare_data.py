"""Data Preparation — Chapter 4: Regression Discontinuity"""
import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "ch4"

df = pd.read_stata(DATA_DIR / "AEJfigs.dta")
out = pd.DataFrame({
    "agecell": df["agecell"],
    "age": df["agecell"] - 21,
    "over21": (df["agecell"] >= 21).astype(int),
    "all": df["all"], "mva": df["mva"], "suicide": df["suicide"],
    "homicide": df["homicide"], "internal": df["internal"],
    "alcohol": df["alcohol"],
    "ext_oth": df["external"] - df["homicide"] - df["suicide"] - df["mva"],
})
out["age2"] = out["age"] ** 2
out["over_age"] = out["over21"] * out["age"]
out["over_age2"] = out["over21"] * out["age2"]
out.to_csv(DATA_DIR / "mlda_clean.csv", index=False)
print(f"Saved mlda_clean.csv ({len(out)} rows)")
