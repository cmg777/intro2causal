"""Data Preparation — Chapter 3: Instrumental Variables"""
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "ch3"

df = pd.read_stata(DATA_DIR / "mdve.dta")
assign_map = {1: "Arrest", 2: "Advise", 3: "Separate"}
deliver_map = {1: "Arrest", 2: "Advise", 3: "Separate", 4: "Other"}
df["assigned"] = df["T_RANDOM"].map(assign_map)
df["delivered"] = df["T_FINAL"].map(deliver_map)
df = df[df["delivered"] != "Other"].copy()
df[["assigned", "delivered"]].to_csv(DATA_DIR / "mdve_clean.csv", index=False)
print(f"Saved mdve_clean.csv ({len(df)} rows)")
