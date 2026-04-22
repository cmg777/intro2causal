# Chapter 5: Differences-in-Differences

**Mastering Causal Metrics: An AI-Powered Study Guide**

*A companion to Mastering 'Metrics by Angrist & Pischke*

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/intro2causal/blob/main/notebooks_colab/05-differences-in-differences.ipynb)

---

> 💡 **Learning Objectives**
>

By the end of this chapter, you will be able to:

- Explain the **difference-in-differences (DD)** strategy for causal inference
- Construct a **counterfactual** using a control group's trajectory
- State and assess the **parallel trends assumption**
- Estimate DD effects using **regression with fixed effects**
- Understand why **state-specific trends**, **weighting**, and **clustered standard errors** matter
- Interpret DD results from two case studies: banking crises and drinking age policy


This chapter introduces a method for settings where treatment is not randomly assigned but varies across groups and over time. By comparing *changes* rather than levels, DD removes time-invariant confounders.

> 📊 **Roadmap for Chapter 5** *(diagram — view in the [online book](https://github.com/cmg777/intro2causal))*


## A Mississippi Experiment

### The Great Depression and the Fed

In 1930, the collapse of Caldwell and Company, a Nashville banking giant, triggered a cascade of bank failures across the American South. Within weeks, dozens of banks closed. The question for policymakers: **could aggressive central bank intervention have prevented the collapse?**

A natural experiment emerged from the structure of the Federal Reserve System. The border between two Fed districts runs through Mississippi, splitting the state between:

- **6th District (Atlanta Fed)**: favored easy credit and liquidity support for struggling banks
- **8th District (St. Louis Fed)**: followed a restrictive "Real Bills" doctrine, tightening credit during the crisis

Banks on either side of this border faced the same economic conditions but received very different policy responses.

```python
# Load clean bank failure data (July 1 each year, both districts)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
sns.set_style("whitegrid")

# --- Data source ---
DATA = "https://raw.githubusercontent.com/cmg777/intro2causal/main/data/"

# bib6 = banks in business (6th district), bib8 = banks in business (8th district)
# counterfactual = what 6th district would look like under parallel trends
banks = pd.read_csv(DATA + "ch5/banks_clean.csv")
banks
```


### Visualizing the DD

```python

fig, ax = plt.subplots(figsize=(9, 5))

# Plot actual data for both districts
ax.plot(banks["year"], banks["bib8"], "ko-", markersize=8, label="8th District (no intervention)")
ax.plot(banks["year"], banks["bib6"], "ks-", markersize=8, label="6th District (Fed intervention)")
ax.plot(banks["year"], banks["counterfactual"], "k^--", markersize=8, alpha=0.6,
        label="6th District counterfactual")

ax.set_xlabel("Year")
ax.set_ylabel("Number of Banks in Business")
ax.set_title("Fed intervention and bank survival during the Great Depression")
ax.legend()
ax.set_ylim(60, 180)
plt.tight_layout()
plt.show()
```


### Computing the DD

The DD calculation compares **changes** across groups, which removes any fixed differences between the districts:

```python

# Compute DD for each post-crisis year
# Get the 1930 baseline values for each district
pre_6 = banks.loc[banks["year"] == 1930, "bib6"].values[0]
pre_8 = banks.loc[banks["year"] == 1930, "bib8"].values[0]

# Loop over each year after 1930
rows = []
post_years = banks[banks["year"] > 1930]
for _, row in post_years.iterrows():
    # Change in each district relative to 1930
    change_6 = row["bib6"] - pre_6
    change_8 = row["bib8"] - pre_8
    # DD = treated change minus control change
    dd = change_6 - change_8

    rows.append({
        "Year": int(row["year"]),
        "Change in 6th (treated)": int(change_6),
        "Change in 8th (control)": int(change_8),
        "DD estimate (banks saved)": int(dd),
    })

pd.DataFrame(rows)
```


> ⭐ **Key finding**
>

The Atlanta Fed's easy money policy saved approximately **19--23 banks** relative to the restrictive St. Louis Fed approach. The DD works by subtracting the control group's change from the treated group's change, removing any common trends.


> 📝 **Intuition Builder: The Diet Analogy**
>

Suppose you and a friend both plan to eat well over the holidays. You go on a new diet; your friend doesn't. After the holidays, you gained 2 lbs and your friend gained 7 lbs. Did the diet work?

- **Naive comparison**: You weigh more than before (gained 2 lbs) --- diet "failed"?
- **DD comparison**: You gained 2, your friend gained 7. The diet saved you 5 lbs (7 − 2 = 5).

The key assumption: without the diet, you would have gained the same 7 lbs as your friend (parallel trends). DD uses the control group to estimate this counterfactual.


## The DD Framework

### The Core Logic

DD compares changes over time in a treatment group with changes in a control group:

$$\delta_{DD} = \underbrace{(\bar{Y}_{treat,after} - \bar{Y}_{treat,before})}_{\text{Change in treated}} - \underbrace{(\bar{Y}_{control,after} - \bar{Y}_{control,before})}_{\text{Change in control}}$$

> 📊 **The DD method: subtract the control group's change from the treated group's change to isolate the causal effect.** *(diagram — view in the [online book](https://github.com/cmg777/intro2causal))*


### The Parallel Trends Assumption

> ⚠️ **The key assumption**
>

DD requires that, **absent treatment**, the treated and control groups would have followed **parallel trends**. The treatment and control groups can start at different levels --- but their *changes over time* must be similar.

If this assumption fails (e.g., the treated group was already on a different trajectory), the DD estimate will be biased.


> ⚠️ **Common Misconception: DD does NOT require equal levels**
>

Students often think DD requires the treatment and control groups to have the same *level* of the outcome. This is wrong. The 6th District had 135 banks and the 8th had 165 --- very different levels. What matters is that they would have *changed at the same rate* without the intervention. Groups can start miles apart; DD only needs them to travel in the same direction at the same speed.


## Case Study: MLDA and Death Rates

### The Policy Variation

After Prohibition ended in 1933, states set their own drinking ages. In 1984, federal legislation pushed all states to adopt a minimum legal drinking age of 21, but states complied at different times. This staggered adoption creates variation for a DD analysis.

```python
# Load clean MLDA death rate data (state-year panel, 18-20 year olds, 1970-1983)
# mrate = death rate per 100,000; legal = fraction of 18-20 yr olds who can legally drink
# dtype = cause of death (all, MVA, suicide, internal); pop = state population of 18-20 yr olds
deaths = pd.read_csv(DATA + "ch5/deaths_clean.csv")
deaths.head(3)
```


### The Regression DD Model

With many states and years, DD is implemented as a regression with **fixed effects**:

$$Y_{st} = \alpha + \delta \, D_{st} + \sum_s \beta_s \, \text{STATE}_s + \sum_t \gamma_t \, \text{YEAR}_t + e_{st}$$

where $Y_{st}$ is the death rate (`mrate`) in state $s$ at time $t$, and $D_{st}$ is the fraction of 18--20 year olds who can legally drink (`legal`).

- **State fixed effects** ($\beta_s$) absorb permanent differences between states (culture, geography, road conditions)
- **Year fixed effects** ($\gamma_t$) absorb nationwide trends (vehicle safety improvements, national campaigns)
- **$\delta$** is the DD estimate: the causal effect of legal drinking access on the death rate

> 📝 **Why cluster standard errors by state?**
>

The treatment variable (`legal`) changes at the state level, and death rates within a state are correlated over time. **Clustering** standard errors at the state level accounts for this serial correlation, preventing us from overstating precision.


Let's start with a single regression for all-cause mortality:

```python

# Filter to all-cause deaths
allcause = deaths[deaths["dtype"] == "all"]

# DD regression with state and year fixed effects
model = smf.ols("mrate ~ legal + C(state) + C(year)", data=allcause)

# Cluster standard errors by state because treatment (legal) varies at the state level
result = model.fit(cov_type="cluster", cov_kwds={"groups": allcause["state"]})

# Show just the key coefficient
coef_table = pd.DataFrame({
    "Variable": ["legal"],
    "Coefficient": [round(result.params["legal"], 2)],
    "Std. Error": [round(result.bse["legal"], 2)],
    "t-stat": [round(result.tvalues["legal"], 2)],
})
coef_table
```


Now let's check across multiple causes of death and specifications:

```python

# Compare three specifications for each cause of death:
#   Spec 1 — Unweighted OLS with state + year fixed effects
#   Spec 2 — Add state-specific linear trends (each state gets its own slope over time)
#   Spec 3 — Population-weighted WLS (larger states count more)

dtype_labels = {"all": "All causes", "MVA": "Motor vehicle", "suicide": "Suicide", "internal": "Internal"}

rows = []
for dtype_val, label in dtype_labels.items():
    s = deaths[deaths["dtype"] == dtype_val].copy()

    # Spec 1: State + Year FE, unweighted
    model1 = smf.ols("mrate ~ legal + C(state) + C(year)", data=s)
    r1 = model1.fit(cov_type="cluster", cov_kwds={"groups": s["state"]})

    # Spec 2: Add state-specific linear trends
    # C(state):year = interaction of state dummies with year, giving each state its own slope
    model2 = smf.ols("mrate ~ legal + C(state) + C(year) + C(state):year", data=s)
    r2 = model2.fit(cov_type="cluster", cov_kwds={"groups": s["state"]})

    # Spec 3: Population-weighted (WLS)
    # Weight by state population so larger states count more (more reliable death rates)
    model3 = smf.wls("mrate ~ legal + C(state) + C(year)", data=s, weights=s["pop"])
    r3 = model3.fit(cov_type="cluster", cov_kwds={"groups": s["state"]})

    # Format each result as "coefficient (standard error)"
    coef1 = str(round(r1.params["legal"], 2)) + " (" + str(round(r1.bse["legal"], 2)) + ")"
    coef2 = str(round(r2.params["legal"], 2)) + " (" + str(round(r2.bse["legal"], 2)) + ")"
    coef3 = str(round(r3.params["legal"], 2)) + " (" + str(round(r3.bse["legal"], 2)) + ")"

    rows.append({
        "Cause": label,
        "Unweighted": coef1,
        "With state trends": coef2,
        "Pop. weighted": coef3,
    })

pd.DataFrame(rows)
```


> ⭐ **Interpreting the DD results**
>

- **Legal drinking access increases the death rate** by approximately **7--10 per 100,000** among 18--20 year olds
- **Motor vehicle accidents** account for most of the effect (~5--7 deaths)
- **Internal causes** (disease) show no significant effect --- a **placebo test** confirming the design
- Results are **robust** to adding state-specific trends and population weighting


## Robustness Checks

### State-Specific Trends

Adding state-specific linear time trends is a more demanding test. It allows each state to have its own background trajectory and asks whether the MLDA effect is a **deviation from this trend** rather than a continuation of pre-existing patterns. The results hold up.

### Beer Tax Control

Some states may have changed beer taxes at the same time as their MLDA. Controlling for beer taxes tests whether the MLDA effect is confounded by other alcohol-control policies:

```python

# Check if MLDA effects hold after controlling for beer taxes
rows = []
for dtype_val, label in [("all", "All causes"), ("MVA", "Motor vehicle")]:
    s = deaths[deaths["dtype"] == dtype_val].dropna(subset=["beertax"]).copy()

    model = smf.ols("mrate ~ legal + beertax + C(state) + C(year)", data=s)
    # Cluster standard errors by state
    r = model.fit(cov_type="cluster", cov_kwds={"groups": s["state"]})

    # Format results as "coefficient (standard error)"
    legal_str = str(round(r.params["legal"], 2)) + " (" + str(round(r.bse["legal"], 2)) + ")"
    tax_str = str(round(r.params["beertax"], 2)) + " (" + str(round(r.bse["beertax"], 2)) + ")"

    rows.append({
        "Cause": label,
        "Legal effect": legal_str,
        "Beer tax effect": tax_str,
    })

pd.DataFrame(rows)
```


The MLDA coefficients are largely unchanged after controlling for beer taxes, reinforcing the causal interpretation.


## Historical Perspective: John Snow

Long before modern econometrics, **John Snow** (1813--1858) used DD reasoning to solve one of the great public health mysteries: the cause of cholera.

In 1854 London, Snow noticed that cholera deaths were concentrated in neighborhoods served by the **Southwark and Vauxhall** water company, which drew from a contaminated stretch of the Thames. A competing company, **Lambeth**, had moved its intake upstream to cleaner water in 1852.

Snow compared the *change* in cholera death rates before and after Lambeth's move, relative to Southwark and Vauxhall's unchanged source. The dramatic decline in Lambeth-served neighborhoods --- with no corresponding decline in Southwark areas --- provided compelling evidence that contaminated water caused cholera, overturning the prevailing "miasma" (bad air) theory.

This was a DD analysis avant la lettre: two groups (water companies), a treatment that changed for one but not the other, and a comparison of changes in outcomes.


### How DD Compares to Other Methods

| Feature | RCT (Ch 1) | IV (Ch 3) | RD (Ch 4) | **DD (This Chapter)** |
|:---|:---|:---|:---|:---|
| **Key requirement** | Random assignment | Valid instrument | Sharp cutoff | Parallel trends |
| **Handles unobservables?** | Yes (by randomization) | Yes (via instrument) | Yes (at the cutoff) | Only time-invariant ones |
| **Estimates** | ATE | LATE (compliers) | Local effect (at cutoff) | ATT (treated group) |
| **Data structure** | Cross-section | Cross-section or panel | Running variable | Panel (group × time) |

: Comparing the four causal inference methods covered so far {.striped}

> 📝 **Connection to Chapters 1 and 4**
>

DD complements the other methods:

- **vs. RCTs (Chapter 1)**: DD works when randomization is impossible but policy varies across groups and time. It sacrifices the randomization guarantee for broader applicability.
- **vs. RD (Chapter 4)**: Both exploit policy rules, but RD uses a cutoff in a running variable while DD uses changes over time. The MLDA question appears in *both* chapters: Chapter 4 uses the age-21 cutoff (RD); this chapter uses state-level policy changes over time (DD). Same question, different identification strategies.


## Key Takeaways

> 📊 **How the key concepts of Chapter 5 connect** *(diagram — view in the [online book](https://github.com/cmg777/intro2causal))*


1. **DD compares changes over time** between treatment and control groups, removing time-invariant confounders.

2. **The parallel trends assumption** is key: absent treatment, both groups must have been on the same trajectory.

3. **Regression DD with fixed effects** is the standard implementation for multi-group, multi-period settings.

4. **State fixed effects** remove permanent state differences; **year fixed effects** remove common time trends.

5. **Cluster standard errors** at the level of treatment assignment (e.g., state) to account for serial correlation.

6. **Robustness checks** include state-specific trends, population weighting, and placebo tests on unaffected outcomes.


## Learn by Coding

Copy this code into a Python notebook to reproduce the key results from this chapter.

```python
# ============================================================
# Chapter 5: Differences-in-Differences — Code Cheatsheet
# ============================================================
import pandas as pd
import statsmodels.formula.api as smf

DATA = "https://raw.githubusercontent.com/cmg777/intro2causal/main/data/"

# --- Step 1: Manual DD with the Great Depression banking data ---
banks = pd.read_csv(DATA + "ch5/banks_clean.csv")
print("Banks in business by district and year:")
print(banks)

pre_6 = banks.loc[banks["year"] == 1930, "bib6"].values[0]
pre_8 = banks.loc[banks["year"] == 1930, "bib8"].values[0]
post_6 = banks.loc[banks["year"] == 1931, "bib6"].values[0]
post_8 = banks.loc[banks["year"] == 1931, "bib8"].values[0]
dd = (post_6 - pre_6) - (post_8 - pre_8)
print(f"\nDD estimate (1931 vs 1930): {dd} banks saved by Atlanta Fed intervention")

# --- Step 2: Load MLDA death rate panel data ---
deaths = pd.read_csv(DATA + "ch5/deaths_clean.csv")
allcause = deaths[deaths["dtype"] == "all"]
print(f"\nDeath rate panel: {allcause.shape[0]} state-year observations")

# --- Step 3: Regression DD with state and year fixed effects ---
model = smf.ols("mrate ~ legal + C(state) + C(year)", data=allcause)
result = model.fit(cov_type="cluster", cov_kwds={"groups": allcause["state"]})
print(f"\nDD estimate (all-cause deaths): {round(result.params['legal'], 2)}")
print(f"  Standard error: {round(result.bse['legal'], 2)}")

# --- Step 4: Population-weighted DD ---
model = smf.wls("mrate ~ legal + C(state) + C(year)", data=allcause, weights=allcause["pop"])
result = model.fit(cov_type="cluster", cov_kwds={"groups": allcause["state"]})
print(f"\nWeighted DD estimate: {round(result.params['legal'], 2)}")

# --- Step 5: Placebo test (suicide should NOT respond to drinking age) ---
suicide = deaths[deaths["dtype"] == "suicide"]
model = smf.ols("mrate ~ legal + C(state) + C(year)", data=suicide)
result = model.fit(cov_type="cluster", cov_kwds={"groups": suicide["state"]})
print(f"\nPlacebo (suicide): {round(result.params['legal'], 2)}")
print("  (Expect: small and insignificant)")
```

> 💡 **Try it yourself!**
>
Copy the code above and paste it into [this Google Colab scratchpad](https://colab.research.google.com/notebooks/empty.ipynb) to run it interactively. Modify the variables, change the specifications, and see how results change!


## Exercises

### Conceptual Questions

> ✏️ **Conceptual Questions**
>

1. **Parallel trends**: A city implements a minimum wage increase in 2020. You plan to compare employment changes in that city with a neighboring city that didn't raise the minimum wage. What would it mean if the two cities already had diverging employment trends before 2020? How would this affect your DD estimate?

2. **Computing DD**: Before a policy change, the treatment group's outcome average is 50 and the control group's is 40. After the change, they are 55 and 48. (a) Compute the DD estimate. (b) What assumption is needed for this to be causal?

3. **Fixed effects**: Explain in your own words why we need *both* state and year fixed effects in the MLDA regression. What would happen if we omitted state effects? Year effects?

4. **State-specific trends**: Explain what adding `C(state):year` to the DD regression does. Under what circumstances might the DD estimate change substantially when you add state-specific trends, and what would that imply about the parallel trends assumption?

5. **Placebo test design**: You are studying whether a new air pollution regulation reduced asthma hospitalizations. Propose a placebo outcome that should NOT be affected by the regulation. Why would finding a significant effect on your placebo outcome be concerning?


### Research Tasks

> ✏️ **Research Tasks**
>

1. **DD for suicide deaths**: Using `deaths_clean.csv`, run the DD regression for suicide deaths (`dtype == "suicide"`) with state and year fixed effects and state-clustered SEs. Is the effect of legal drinking significant for suicides? How does the coefficient compare to the all-cause result?

2. **DD over time for banks**: Using `banks_clean.csv`, compute the DD estimate for each post-crisis year (1931, 1932, 1933, 1934) relative to the 1930 baseline. Does the effect grow or shrink over time? What does this trend suggest about the lasting impact of the Fed's intervention?

3. **Population-weighted DD**: Using `deaths_clean.csv`, run the all-cause DD regression with population weights (`smf.wls` with `weights=pop`). Compare the coefficient with the unweighted result. Why might weighting by population change the estimate?


## Solutions

### Conceptual Questions

**Q1.** If the two cities already had diverging employment trends before the minimum wage increase, the parallel trends assumption is violated. The DD estimate would capture both the causal effect of the policy *and* the pre-existing trend difference. For example, if the treatment city's employment was already declining faster, the DD estimate would overstate the negative effect of the minimum wage. You could test for this by plotting pre-treatment trends and checking whether they are parallel.

**Q2.** (a) DD = (55 − 50) − (48 − 40) = 5 − 8 = −3. The treatment group's outcome fell by 3 units relative to the control group. (b) The parallel trends assumption must hold: absent the policy change, both groups would have experienced the same change over time. Here, the control group rose by 8, so we assume the treatment group would have also risen by 8 without the policy --- making the treatment effect −3.

**Q3.** State fixed effects control for permanent differences between states (e.g., some states have higher death rates due to geography, culture, or road conditions). Without them, we might confuse these permanent differences for the effect of MLDA policy. Year fixed effects control for nationwide changes over time (e.g., improvements in vehicle safety or changes in drinking culture). Without them, we might attribute a nationwide trend in mortality to MLDA changes. Both are needed to isolate the within-state, within-year variation in MLDA policy.

**Q4.** Adding `C(state):year` allows each state to have its own linear time trend. This is more demanding than standard DD because it asks: did the MLDA effect cause a *deviation* from the state's own trend, not just from the national average trend? The DD estimate might change substantially if some states were on different trajectories for reasons unrelated to MLDA (e.g., southern states experiencing rapid economic changes). A large change would suggest the standard parallel trends assumption is questionable and that state-specific trends are needed to get a reliable estimate.

### Research Tasks

**R1.**

```python

import pandas as pd
import statsmodels.formula.api as smf

deaths = pd.read_csv(DATA + "ch5/deaths_clean.csv")

# Compare all-cause and suicide DD regressions
rows = []
for dtype_val, label in [("all", "All causes"), ("suicide", "Suicide")]:
    s = deaths[deaths["dtype"] == dtype_val].copy()
    model = smf.ols("mrate ~ legal + C(state) + C(year)", data=s)
    # Cluster standard errors by state
    r = model.fit(cov_type="cluster", cov_kwds={"groups": s["state"]})
    rows.append({
        "Cause": label,
        "Legal effect": round(r.params["legal"], 2),
        "SE": round(r.bse["legal"], 2),
        "t-stat": round(r.tvalues["legal"], 2),
    })

pd.DataFrame(rows)
```


The suicide effect is much smaller than the all-cause effect and is not statistically significant (t-stat well below 2). While alcohol can contribute to suicide through impaired judgment, the DD analysis does not find strong evidence that MLDA changes substantially affected suicide rates. The all-cause result is driven primarily by motor vehicle accidents.

**R2.**

```python

banks = pd.read_csv(DATA + "ch5/banks_clean.csv")

# Get the 1930 baseline values for each district
pre_6 = banks.loc[banks["year"] == 1930, "bib6"].values[0]
pre_8 = banks.loc[banks["year"] == 1930, "bib8"].values[0]

# Compute DD for each year relative to 1930 baseline
rows = []
for _, row in banks[banks["year"] > 1930].iterrows():
    change_6 = row["bib6"] - pre_6   # change in treated (6th district)
    change_8 = row["bib8"] - pre_8   # change in control (8th district)
    dd = change_6 - change_8         # DD = treated change - control change

    rows.append({
        "Year": int(row["year"]),
        "Change in 6th (treated)": int(change_6),
        "Change in 8th (control)": int(change_8),
        "DD (banks saved)": int(dd),
    })

pd.DataFrame(rows)
```


The DD effect grows from 19 banks in 1931 to 23 in 1932, then stabilizes around 21 in 1933--1934. This suggests the Fed's intervention had a lasting protective effect: the banks it saved in the early crisis years remained in business through the worst of the Depression. The gap between districts didn't close as the crisis deepened, indicating the initial intervention had durable benefits.

**Q5.** A good placebo outcome would be hospitalizations for broken bones or appendicitis --- conditions unrelated to air quality. If the air pollution regulation appears to significantly reduce broken-bone hospitalizations, something is wrong: either the regulation coincided with another change (confounding), or the parallel trends assumption fails. A significant placebo effect undermines confidence in the main result because it suggests the DD is picking up spurious trends rather than the causal effect of the regulation.

**R3.**

```python

import pandas as pd
import statsmodels.formula.api as smf

deaths = pd.read_csv(DATA + "ch5/deaths_clean.csv")
allcause = deaths[deaths["dtype"] == "all"]

# Unweighted OLS
model_uw = smf.ols("mrate ~ legal + C(state) + C(year)", data=allcause)
r_uw = model_uw.fit(cov_type="cluster", cov_kwds={"groups": allcause["state"]})

# Population-weighted WLS (larger states count more)
model_wt = smf.wls("mrate ~ legal + C(state) + C(year)", data=allcause, weights=allcause["pop"])
r_wt = model_wt.fit(cov_type="cluster", cov_kwds={"groups": allcause["state"]})

pd.DataFrame({
    "Specification": ["Unweighted OLS", "Population-weighted WLS"],
    "Legal effect": [round(r_uw.params["legal"], 2), round(r_wt.params["legal"], 2)],
    "SE": [round(r_uw.bse["legal"], 2), round(r_wt.bse["legal"], 2)],
})
```


Population weighting gives more influence to large states (California, Texas) where death rates are measured more precisely. The weighted estimate is often slightly different because MLDA effects may vary by state size. If the estimates are similar, it suggests the effect is consistent across large and small states.
