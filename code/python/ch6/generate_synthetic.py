"""
Generate Synthetic Datasets — Chapter 6: The Wages of Schooling
================================================================
Creates three pre-made CSV files used in the study guide to illustrate
causal inference concepts where real data is unavailable.

Students load these CSVs just like any other dataset. They do NOT need
to run this script — the CSVs are already committed to the repo.
"""
import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "ch6"
np.random.seed(2024)

# =====================================================================
# 1. synthetic_ovb.csv — Omitted Variables Bias demonstration
# =====================================================================
# DGP: ability → schooling + earnings; occupation caused by schooling
# True return to schooling = 0.08 per year
# OLS without ability ≈ 0.11 (upward bias)
# OLS with ability ≈ 0.08 (correct)
# OLS with occupation (bad control) ≈ biased downward

n_ovb = 1000

ability = np.random.normal(0, 1, n_ovb)
schooling = 12 + 2 * ability + np.random.normal(0, 1.5, n_ovb)
schooling = np.clip(schooling, 6, 20).round(0)

# True causal return = 0.08 per year; ability also directly affects earnings
earnings = 8.0 + 0.08 * schooling + 0.15 * ability + np.random.normal(0, 0.3, n_ovb)

# Occupation is caused by schooling (post-treatment / bad control)
# Higher schooling → higher-status occupation (1-5 scale)
occupation = np.clip(1 + 0.25 * (schooling - 10) + np.random.normal(0, 0.8, n_ovb), 1, 5).round(0)

ovb_df = pd.DataFrame({
    "earnings": earnings.round(4),
    "schooling": schooling.astype(int),
    "ability": ability.round(4),
    "occupation": occupation.astype(int),
})
ovb_df.to_csv(DATA_DIR / "synthetic_ovb.csv", index=False)
print(f"Saved synthetic_ovb.csv ({len(ovb_df)} rows)")


# =====================================================================
# 2. synthetic_rct.csv — Hypothetical scholarship RCT
# =====================================================================
# DGP: scholarship randomly assigned (independent of ability)
# Scholarship increases schooling by ~2 years on average
# True return = 0.08 per year → scholarship effect on earnings ≈ 0.16

n_rct = 2000

ability_rct = np.random.normal(0, 1, n_rct)
scholarship = np.random.binomial(1, 0.5, n_rct)  # random assignment

# Schooling: depends on ability (as usual) + scholarship adds ~2 years
schooling_rct = 12 + 1.5 * ability_rct + 2.0 * scholarship + np.random.normal(0, 1.2, n_rct)
schooling_rct = np.clip(schooling_rct, 6, 20).round(0)

# Earnings: true return 0.08, ability effect 0.12
earnings_rct = 8.0 + 0.08 * schooling_rct + 0.12 * ability_rct + np.random.normal(0, 0.2, n_rct)

rct_df = pd.DataFrame({
    "earnings": earnings_rct.round(4),
    "schooling": schooling_rct.astype(int),
    "ability": ability_rct.round(4),
    "scholarship": scholarship,
})
rct_df.to_csv(DATA_DIR / "synthetic_rct.csv", index=False)
print(f"Saved synthetic_rct.csv ({len(rct_df)} rows)")


# =====================================================================
# 3. synthetic_did.csv — Compulsory schooling reform DiD
# =====================================================================
# DGP: 20 states × 20 years; 10 states adopt reform raising compulsory
# schooling age in year 2005 (year 11 of 1995-2014).
# Reform increases avg schooling by ~0.5 years → earnings by ~4%.
# Parallel pre-trends in both schooling and earnings.

n_states = 20
years = np.arange(1995, 2015)
n_years = len(years)

rows = []
for s in range(1, n_states + 1):
    treated = int(s <= 10)  # states 1-10 are treated
    # State-level baseline (treated states start slightly lower)
    base_school = 11.5 - 0.3 * treated + np.random.normal(0, 0.2)
    base_earn = 9.5 - 0.1 * treated + np.random.normal(0, 0.1)

    for y in years:
        post = int(y >= 2005)
        # Common time trend for both groups (parallel trends)
        time_trend_school = 0.03 * (y - 1995)
        time_trend_earn = 0.02 * (y - 1995)

        # Treatment effect: reform raises schooling and earnings
        treat_effect_school = 0.5 * treated * post
        treat_effect_earn = 0.04 * treated * post

        avg_schooling = base_school + time_trend_school + treat_effect_school + np.random.normal(0, 0.08)
        avg_earnings = base_earn + time_trend_earn + treat_effect_earn + np.random.normal(0, 0.03)

        rows.append({
            "state": s,
            "year": y,
            "treated": treated,
            "post": post,
            "avg_schooling": round(avg_schooling, 4),
            "avg_earnings": round(avg_earnings, 4),
        })

did_df = pd.DataFrame(rows)
did_df.to_csv(DATA_DIR / "synthetic_did.csv", index=False)
print(f"Saved synthetic_did.csv ({len(did_df)} rows)")
