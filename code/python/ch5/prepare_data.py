"""Data Preparation — Chapter 5: Differences-in-Differences"""
import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "ch5"

# --- Banks data ---
banks = pd.read_csv(DATA_DIR / "banks.csv")
annual = banks[(banks["month"] == 7) & (banks["day"] == 1)].copy()
gap_1930 = annual.loc[annual["year"] == 1930, "bib8"].values[0] - annual.loc[annual["year"] == 1930, "bib6"].values[0]
annual["counterfactual"] = np.where(
    annual["year"] <= 1929, annual["bib6"], annual["bib8"] - gap_1930
)
annual[["year", "bib6", "bib8", "counterfactual"]].to_csv(DATA_DIR / "banks_clean.csv", index=False)
print(f"Saved banks_clean.csv ({len(annual)} rows)")

# --- Deaths data ---
deaths = pd.read_stata(DATA_DIR / "deaths.dta")
d = deaths[(deaths["agegr"] == "18-20 yrs") & (deaths["year"] <= 1983)].copy()
d["state"] = d["state"].astype(str)
d["dtype"] = d["dtype"].astype(str)
d["year"] = d["year"].astype(int)
if "beertaxa" in d.columns and "beertax" not in d.columns:
    d = d.rename(columns={"beertaxa": "beertax"})
d[["year", "state", "dtype", "mrate", "legal", "pop", "beertax"]].to_csv(
    DATA_DIR / "deaths_clean.csv", index=False
)
print(f"Saved deaths_clean.csv ({len(d)} rows)")
