# Chapter 4: Regression Discontinuity

**Mastering Causal Metrics: An AI-Powered Study Guide**

*A companion to Mastering 'Metrics by Angrist & Pischke*

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/intro2causal/blob/main/notebooks_colab/04-regression-discontinuity.ipynb)

---

> 💡 **Learning Objectives**
>

By the end of this chapter, you will be able to:

- Explain how **rigid rules and cutoffs** create natural experiments
- Define the **running variable**, **cutoff**, and **treatment indicator** in an RD design
- Distinguish between **sharp** and **fuzzy** RD designs
- Estimate causal effects using **polynomial regression** at a discontinuity
- Assess robustness through **bandwidth choice** and **specification checks**
- Interpret the RD estimate as a **local causal effect** at the cutoff

This chapter shows how bureaucratic rules --- the very things that seem to reduce randomness --- can actually *create* valuable natural experiments for causal inference.

```mermaid

graph TD
    A["THE QUESTION: Does legal drinking access increase mortality?"]
    B["THE INSIGHT: The age-21 cutoff creates a natural experiment"]
    C["THE METHOD: Compare outcomes just above vs. just below the cutoff"]
    D["THE EVIDENCE: Sharp mortality jump at age 21, driven by car accidents"]
    E["THE EXTENSION: Fuzzy RD when treatment probability jumps at a cutoff"]

    A --> B --> C --> D --> E

    style A fill:#3498db,color:#fff
    style B fill:#e67e22,color:#fff
    style C fill:#8e44ad,color:#fff
    style D fill:#2d8659,color:#fff
    style E fill:#2c3e50,color:#fff
    linkStyle default stroke:#fff,stroke-width:2px
```


## Rules Create Experiments

Many policies have sharp eligibility rules. You can vote at 18 but not at 17. You qualify for Medicare at 65 but not at 64. You can legally drink at 21 but not at 20. These cutoffs create a powerful opportunity: people just above and just below the threshold are nearly identical in every way --- except that one group receives the treatment and the other doesn't.

This is the logic of **Regression Discontinuity (RD)** designs. The causal effect is identified by the **jump** in outcomes at the cutoff.

> 📝 **Intuition Builder: The Speed Limit Analogy**
>

Think of a speed limit sign on a highway. The road is the same on both sides of the sign --- same surface, same weather, same cars. But drivers caught going 66 mph vs. 64 mph face very different consequences if the limit is 65. The sign creates a sharp rule that affects behavior, even though the drivers on both sides are virtually identical. RD exploits exactly this kind of rule: people just above and just below a threshold are nearly interchangeable, but the rule treats them differently.

### The MLDA Question

The **minimum legal drinking age (MLDA)** is 21 in the United States. Does reaching this threshold actually affect health? Specifically, does turning 21 --- and gaining legal access to alcohol --- increase mortality?

```python
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

# Load clean MLDA mortality data
# Each row is one monthly age cell with death rates per 100,000
# Key variables:
#   agecell  = age in years (e.g., 19.08, 20.17, 21.00, ...)
#   age      = centered at 21 (so age=0 is the cutoff; negative = under 21)
#   over21   = treatment dummy (1 if age >= 21, 0 otherwise)
#   age2, over_age, over_age2 = polynomial/interaction terms for flexible RD models
#   all, mva, suicide, homicide, internal, alcohol = death rates by cause

# --- Data source ---
DATA = "https://raw.githubusercontent.com/cmg777/intro2causal/main/data/"

mlda = pd.read_csv(DATA + "ch4/mlda_clean.csv")
mlda.head(3)
```


**Output:**

```
   agecell    age        over21  all        mva        suicide    homicide   internal   alcohol   ext_oth    age2      over_age  over_age2
-  ---------  ---------  ------  ---------  ---------  ---------  ---------  ---------  --------  ---------  --------  --------  ---------
0  19.068493  -1.931507  0       92.825400  35.829327  11.203714  16.316818  16.617590  0.639138  12.857960  3.730720  -0.0      0.0
1  19.150684  -1.849316  0       95.100740  35.639256  12.193368  16.859964  18.327684  0.677409  12.080471  3.419968  -0.0      0.0
2  19.232876  -1.767124  0       92.144295  34.205650  11.715812  15.219254  18.911053  0.866443  12.092522  3.122728  -0.0      0.0
```


### Visualizing the Discontinuity

The first step in any RD analysis is to **plot the data**. If the causal effect is real, we should see a visible jump in mortality at age 21.

::: {#cell-fig-scatter .cell execution_count=2}
```python
# Scatter plot: mortality rate vs. age in months
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(mlda["agecell"], mlda["all"], color="gray", alpha=0.7, s=40)  # one dot per age cell
ax.axvline(x=21, color="red", linestyle="--", alpha=0.5, label="MLDA cutoff")  # mark the cutoff
ax.set_xlabel("Age (years)")
ax.set_ylabel("Deaths per 100,000")
ax.set_title("All-cause mortality around the 21st birthday")
ax.legend()
plt.tight_layout()
plt.show()
```


**Output:**

![All-cause mortality rate by age. Each dot is one monthly age cell. The vertical dashed line marks the 21st birthday (MLDA cutoff).](04-regression-discontinuity_files/figure-html/fig-scatter-output-1.png){#fig-scatter width=854 height=470}


There is a visible jump right at age 21. Let's now estimate its size formally.

> ⚠️ **Common Misconception: RD is not just "controlling for" the running variable**
>

In standard regression (Chapter 2), we control for confounders to make treated and untreated groups comparable. RD is fundamentally different: there is **no value of the running variable where we observe both treated and untreated individuals**. Everyone over 21 is treated; everyone under 21 is untreated. Instead, RD *extrapolates* the trend from one side of the cutoff to estimate what would have happened without the jump. This is why the functional form (linear vs. quadratic) matters --- it determines how we extrapolate.


## The Sharp RD Regression

### What Is a Running Variable?

In an RD design, the **running variable** is the variable that determines treatment. Here, age is the running variable and 21 is the **cutoff**. The treatment --- legal access to alcohol --- switches on deterministically at the cutoff:

$$D_a = \begin{cases} 1 & \text{if } a \geq 21 \\ 0 & \text{if } a < 21 \end{cases}$$

where $a$ is age (the running variable) and $D_a$ is the treatment indicator. In our data, these correspond to the columns `agecell` and `over21`.

This is a **sharp RD**: treatment switches completely on at the cutoff, with no exceptions.

> 📝 **How RD regression works**
>

We regress the outcome $M_a$ (mortality rate at age $a$) on the treatment dummy $D_a$ and a smooth function of the running variable:

$$M_a = \alpha + \rho \, D_a + \gamma \, a + e_a$$

- **Intercept** ($\alpha$) = predicted mortality just below the cutoff
- **$\rho$** = the **jump at the cutoff** --- this is the causal effect we want
- **$\gamma$** = the background age trend (mortality naturally changes with age)

In Python, this is: `smf.ols("all ~ over21 + age", data=mlda)` --- where `all` is $M_a$, `over21` is $D_a$, and `age` is $a$.

The key insight: because age varies smoothly, any **sudden jump** at the cutoff must be caused by the treatment.

::: {#tbl-rd-simple .cell tbl-cap='Sharp RD estimate of the MLDA effect on all-cause mortality. The over21 coefficient is the causal jump at the cutoff.' execution_count=3}
```python
# Simple linear RD regression
model = smf.ols("all ~ over21 + age", data=mlda)
result = model.fit(cov_type="HC1")

# Extract key regression results into a clear table
pd.DataFrame({
    "Variable": result.params.index,
    "Coefficient": result.params.round(4).values,
    "Std. Error": result.bse.round(4).values,
    "t-statistic": result.tvalues.round(2).values,
    "p-value": result.pvalues.round(3).values,
})
```


**Output:**

```
           coef     std err  z        P>|z|  [0.025  0.975]
---------  -------  -------  -------  -----  ------  ------
Intercept  91.8414  0.709    129.529  0.000  90.452  93.231
over21     7.6627   1.514    5.060    0.000  4.695   10.631
age        -0.9747  0.664    -1.468   0.142  -2.276  0.326
```


The coefficient on `over21` is approximately **7.7 deaths per 100,000** --- a substantial increase caused by gaining legal access to alcohol.


## Robustness: Does the Specification Matter?

A critical question in RD is whether the estimated jump depends on how we model the age trend. We test robustness in two ways:

1. **Polynomial order**: linear vs. quadratic trends
2. **Bandwidth**: full sample (ages 19--22) vs. narrow window (ages 20--22)

::: {#tbl-rd-robust .cell tbl-cap='RD estimates across specifications and bandwidths for multiple causes of death. Robust standard errors in parentheses.' execution_count=4}
```python
# Define narrow bandwidth subsample (ages 20-22 only)
narrow = mlda[(mlda["agecell"] >= 20) & (mlda["agecell"] <= 22)]

# Outcomes to test: each cause of death
outcomes = {"all": "All causes", "mva": "Motor vehicle", "suicide": "Suicide",
            "internal": "Internal causes", "alcohol": "Alcohol-related"}

# For each cause of death, run 4 RD specifications:
#   1. Linear trend, full sample (ages 19-22)
#   2. Quadratic trend, full sample
#   3. Linear trend, narrow bandwidth (ages 20-22)
#   4. Quadratic trend, narrow bandwidth
# This tests whether the RD estimate is robust to model choice and sample window.
rows = []
for var, label in outcomes.items():
    specs = []

    # Spec 1: Linear, full sample
    model1 = smf.ols(f"{var} ~ over21 + age", data=mlda)
    r1 = model1.fit(cov_type="HC1")
    coef1 = round(r1.params["over21"], 2)
    se1 = round(r1.bse["over21"], 2)
    specs.append(str(coef1) + " (" + str(se1) + ")")

    # Spec 2: Quadratic, full sample
    model2 = smf.ols(f"{var} ~ over21 + age + age2 + over_age + over_age2",
                      data=mlda)
    r2 = model2.fit(cov_type="HC1")
    coef2 = round(r2.params["over21"], 2)
    se2 = round(r2.bse["over21"], 2)
    specs.append(str(coef2) + " (" + str(se2) + ")")

    # Spec 3: Linear, narrow bandwidth
    model3 = smf.ols(f"{var} ~ over21 + age", data=narrow)
    r3 = model3.fit(cov_type="HC1")
    coef3 = round(r3.params["over21"], 2)
    se3 = round(r3.bse["over21"], 2)
    specs.append(str(coef3) + " (" + str(se3) + ")")

    # Spec 4: Quadratic, narrow bandwidth
    model4 = smf.ols(f"{var} ~ over21 + age + age2 + over_age + over_age2",
                      data=narrow)
    r4 = model4.fit(cov_type="HC1")
    coef4 = round(r4.params["over21"], 2)
    se4 = round(r4.bse["over21"], 2)
    specs.append(str(coef4) + " (" + str(se4) + ")")

    rows.append({"Cause of death": label, "Linear (full)": specs[0],
                 "Quadratic (full)": specs[1], "Linear (narrow)": specs[2],
                 "Quadratic (narrow)": specs[3]})

pd.DataFrame(rows)
```


**Output:**

```
   Cause of death   Linear (full)  Quadratic (full)  Linear (narrow)  Quadratic (narrow)
-  ---------------  -------------  ----------------  ---------------  ------------------
0  All causes       7.66 (1.51)    9.55 (1.83)       9.75 (2.06)      9.61 (2.29)
1  Motor vehicle    4.53 (0.72)    4.66 (1.09)       4.76 (1.08)      5.89 (1.33)
2  Suicide          1.79 (0.5)     1.81 (0.78)       1.72 (0.73)      1.3 (1.14)
3  Internal causes  0.39 (0.54)    1.07 (0.8)        1.69 (0.74)      1.25 (1.01)
4  Alcohol-related  0.44 (0.21)    0.8 (0.32)        0.74 (0.33)      1.03 (0.41)
```


> ⭐ **Key findings**
>

- **All-cause mortality**: jumps by 7--10 deaths per 100,000 across all specifications
- **Motor vehicle accidents**: the primary driver (4--6 extra deaths) --- drunk driving is the main mechanism
- **Internal causes**: no significant jump --- this is a **placebo test**. Diseases shouldn't respond to the drinking age, and they don't. This validates the RD design.
- **Results are robust**: similar across linear/quadratic models and bandwidth choices

Why is the **internal causes** placebo so powerful? Diseases like cancer, heart disease, and diabetes take years or decades to develop. There is no biological reason why crossing the age-21 threshold would suddenly cause internal organ failure. So if we found a jump in internal-cause deaths, something else must be changing at 21 (perhaps data reporting practices or insurance eligibility), and we couldn't trust the MVA result either. Finding no jump in this placebo outcome gives us confidence that the design is working as intended.


## Visualizing the RD with Fitted Lines

::: {#cell-fig-rd-fitted .cell execution_count=5}
```python
# Split data at the cutoff
below = mlda[mlda["age"] < 0]   # under 21
above = mlda[mlda["age"] >= 0]  # 21 and over

# Fit separate linear regressions on each side
fit_below = smf.ols("all ~ age", data=below).fit()
fit_above = smf.ols("all ~ age", data=above).fit()

# Plot scatter + fitted lines
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(mlda["agecell"], mlda["all"], color="gray", alpha=0.6, s=35)
ax.plot(below["agecell"], fit_below.predict(below), "k-", linewidth=2)   # left line
ax.plot(above["agecell"], fit_above.predict(above), "k-", linewidth=2)   # right line
ax.axvline(x=21, color="red", linestyle="--", alpha=0.5)
ax.set_xlabel("Age (years)")
ax.set_ylabel("Deaths per 100,000")
ax.set_title("Sharp RD: All-cause mortality around the MLDA cutoff")
plt.tight_layout()
plt.show()
```


**Output:**

![RD estimate with fitted regression lines on each side of the cutoff. The gap between the lines at age 21 is the causal effect.](04-regression-discontinuity_files/figure-html/fig-rd-fitted-output-1.png){#fig-rd-fitted width=854 height=470}


::: {#cell-fig-rd-causes .cell execution_count=6}
```python
# Plot two causes on the same figure: MVA (should jump) vs internal (should not)
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(mlda["agecell"], mlda["mva"], color="steelblue", alpha=0.6, s=30, label="Motor vehicle")
ax.scatter(mlda["agecell"], mlda["internal"], color="darkorange", alpha=0.6, s=30, label="Internal causes")

# Fit separate regression lines on each side of the cutoff, for each cause of death.
# The outer loop picks the death cause; the inner loop picks below-21 vs. above-21.
for var, color in [("mva", "steelblue"), ("internal", "darkorange")]:
    for subset in [below, above]:
        model = smf.ols(f"{var} ~ age", data=subset)
        fit = model.fit()
        ax.plot(subset["agecell"], fit.predict(subset), color=color, linewidth=2)

ax.axvline(x=21, color="red", linestyle="--", alpha=0.5)  # cutoff line
ax.set_xlabel("Age (years)")
ax.set_ylabel("Deaths per 100,000")
ax.set_title("RD by cause: Motor vehicle accidents vs. internal causes")
ax.legend()
plt.tight_layout()
plt.show()
```


**Output:**

![RD by cause of death. Motor vehicle accidents show a clear jump; internal causes (a placebo) show none.](04-regression-discontinuity_files/figure-html/fig-rd-causes-output-1.png){#fig-rd-causes width=854 height=470}


## Sharp vs. Fuzzy RD

The MLDA example is a **sharp RD**: everyone over 21 can legally drink, no exceptions. But many policy cutoffs are less precise.

**Boston exam schools** illustrate a **fuzzy RD**. Students are admitted based on a test score cutoff, but not everyone above the cutoff enrolls, and some below it get in through other channels. In a fuzzy RD, the *probability* of treatment jumps at the cutoff, but doesn't go from 0 to 1.

Fuzzy RD is analyzed using **IV/2SLS**, with the cutoff dummy as the instrument for actual treatment. The first stage captures the jump in treatment probability; the second stage estimates the causal effect on compliers.

| Feature | Sharp RD | Fuzzy RD |
|:---|:---|:---|
| Treatment at cutoff | Switches completely on/off | Probability jumps |
| Estimation | OLS with running variable control | IV/2SLS with cutoff as instrument |
| Interpretation | Effect of treatment | LATE for compliers at the cutoff |

: Sharp vs. fuzzy regression discontinuity designs {.striped}

> 📝 **Connection to Chapter 3: Fuzzy RD is IV at a Cutoff**
>

Fuzzy RD is a special case of instrumental variables. The cutoff dummy serves as the instrument, the treatment probability jumps at the cutoff (first stage), and the outcome may jump too (reduced form). The ratio --- reduced form / first stage --- gives the LATE for compliers at the cutoff. If you understand IV from Chapter 3, you already understand fuzzy RD.

Research on Boston exam schools found that peer quality jumped by 0.8 standard deviations at the admissions cutoff, but student achievement showed **no corresponding jump**. This challenges the widely held belief that attending a more selective school --- with higher-ability peers --- causally improves outcomes. The policy implication is that reallocating students across schools of different selectivity may not improve achievement, even though the raw correlation between school quality and student outcomes is strong (selection bias at work again).


## Historical Perspective: Donald Campbell

The RD design was invented by **Donald Thistlethwaite and Donald Campbell** in 1960. They studied whether receiving National Merit Scholarship recognition affected students' career plans. Their RD analysis at the recognition cutoff found minimal effects --- one of the first applications of this now-ubiquitous method.

Campbell went on to pioneer quasi-experimental methods more broadly, co-authoring influential textbooks on research design that shaped how social scientists think about causal inference outside of true experiments.


## Key Takeaways

```mermaid

graph TD
    Q["Rigid rules create sharp cutoffs"]
    RV["Running variable determines treatment"]
    RD["RD: compare just above vs. just below"]
    SPEC["Test robustness: polynomial order and bandwidth"]
    PLAC["Placebo test: outcomes that should not jump"]
    LOCAL["RD estimates are local: valid at the cutoff"]
    FUZZY["Fuzzy RD: when treatment probability jumps, use IV"]

    Q --> RV --> RD
    RD --> SPEC
    RD --> PLAC
    RD --> LOCAL
    RD --> FUZZY

    style Q fill:#3498db,color:#fff
    style RD fill:#8e44ad,color:#fff
    style SPEC fill:#e67e22,color:#fff
    style PLAC fill:#2d8659,color:#fff
    style LOCAL fill:#2c3e50,color:#fff
    linkStyle default stroke:#fff,stroke-width:2px
```


1. **RD exploits cutoff rules** where treatment switches on at a threshold of a running variable.

2. **The causal effect** is the jump in outcomes at the cutoff, after controlling for the smooth relationship between the running variable and the outcome.

3. **Always plot the data first.** Visual inspection is the most important step in RD.

4. **Test robustness** by varying polynomial order (linear vs. quadratic) and bandwidth (wide vs. narrow).

5. **Placebo tests** on outcomes unaffected by treatment (e.g., internal causes of death) validate the design.

6. **RD estimates are local** --- they apply to people near the cutoff and may not generalize to people far from it.

7. **Fuzzy RD** handles cases where treatment probability (not treatment itself) jumps, using IV at the cutoff.


## Learn by Coding

Copy this code into a Python notebook to reproduce the key results from this chapter.

```python
# ============================================================
# Chapter 4: Regression Discontinuity — Code Cheatsheet
# ============================================================
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

DATA = "https://raw.githubusercontent.com/cmg777/intro2causal/main/data/"

# --- Step 1: Load MLDA mortality data ---
mlda = pd.read_csv(DATA + "ch4/mlda_clean.csv")
print("MLDA data:", mlda.shape[0], "age cells")
print(mlda[["agecell", "over21", "all", "mva", "internal"]].head())

# --- Step 2: Plot the discontinuity ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(mlda["agecell"], mlda["all"], color="gray", alpha=0.7, s=40)
ax.axvline(x=21, color="red", linestyle="--", label="MLDA cutoff (age 21)")
ax.set_xlabel("Age")
ax.set_ylabel("Deaths per 100,000")
ax.set_title("All-cause mortality around the MLDA cutoff")
ax.legend()
plt.show()

# --- Step 3: Sharp RD regression (linear) ---
model = smf.ols("all ~ over21 + age", data=mlda)
result = model.fit(cov_type="HC1")
print("\nSharp RD — linear specification:")
print(pd.DataFrame({
    "Variable": result.params.index,
    "Coefficient": result.params.round(4).values,
    "Std. Error": result.bse.round(4).values,
    "t-statistic": result.tvalues.round(2).values,
    "p-value": result.pvalues.round(3).values,
}))
print(f"  Jump at cutoff: {round(result.params['over21'], 2)} deaths per 100k")

# --- Step 4: Quadratic RD for robustness ---
model = smf.ols("all ~ over21 + age + age2 + over_age + over_age2", data=mlda)
result = model.fit(cov_type="HC1")
print("\nSharp RD — quadratic specification:")
print(f"  Jump at cutoff: {round(result.params['over21'], 2)} deaths per 100k")

# --- Step 5: Placebo test (internal causes should NOT jump) ---
model = smf.ols("internal ~ over21 + age", data=mlda)
result = model.fit(cov_type="HC1")
print(f"\nPlacebo test (internal causes): {round(result.params['over21'], 2)}")
print("  (Expect: small and insignificant — diseases don't respond to MLDA)")
```

> 💡 **Try it yourself!**
>
Copy the code above and paste it into [this Google Colab scratchpad](https://colab.research.google.com/notebooks/empty.ipynb) to run it interactively. Modify the variables, change the specifications, and see how results change!


## Exercises

### Conceptual Questions

> ✏️ **Conceptual Questions**
>

1. **Identifying RD opportunities**: A scholarship program awards funding to students who score above 80 on an entrance exam. (a) What is the running variable? (b) What is the cutoff? (c) Is this a sharp or fuzzy RD? (d) What assumption must hold for the RD estimate to be causal?

2. **The placebo test**: In our MLDA analysis, internal causes of death showed no jump at age 21. Why is this important for the credibility of the RD design? What would it mean if internal causes *did* show a significant jump?

3. **Bandwidth tradeoff**: Explain the tradeoff between using a narrow bandwidth (ages 20--22) and a wide bandwidth (ages 19--23) in an RD analysis. What does each gain and lose?

4. **Manipulation of the running variable**: Why is manipulation of the running variable a threat to RD validity? Can people manipulate their age? What about an exam score? Give an example where manipulation would be a serious concern.

5. **Local vs. global effects**: The RD estimate tells us about the effect of legal drinking for people *at* the age-21 cutoff. Why might this effect differ from the effect at age 18 or age 25? What does "local" mean in this context?

### Research Tasks

> ✏️ **Research Tasks**
>

1. **Alcohol-related deaths**: Using `mlda_clean.csv`, run the linear RD regression for `alcohol`-related deaths (instead of all-cause). Is the jump at age 21 statistically significant? How does the effect size compare to the `mva` result?

2. **Visualizing the suicide RD**: Using `mlda_clean.csv`, create an RD scatter plot for `suicide` deaths with separate fitted lines on each side of the cutoff. Does the visual pattern match what the regression coefficient suggests?

3. **Quadratic vs. linear specification**: Using `mlda_clean.csv`, run the quadratic RD model for all-cause mortality (including `age2`, `over_age`, `over_age2`). Compare the coefficient on `over21` with the linear model. Is the estimate sensitive to the polynomial order?


## Solutions

### Conceptual Questions

**Q1.** (a) The running variable is the entrance exam score. (b) The cutoff is 80. (c) If all students above 80 receive funding and none below do, it is a sharp RD. If some above 80 decline and some below 80 receive funding through appeals, it is fuzzy. (d) The key assumption is that all other factors affecting the outcome vary *smoothly* at the cutoff --- students scoring 79 and 81 must be comparable in every way except scholarship receipt.

**Q2.** Internal causes of death (diseases, cancer, etc.) should not be affected by legal drinking access at age 21 --- these conditions take years to develop. Finding no jump in internal causes confirms that the RD design is picking up the causal effect of alcohol access, not some other factor that changes at 21. If internal causes *did* show a significant jump, it would suggest that something other than drinking is changing at the cutoff (e.g., a change in health insurance eligibility or data reporting), casting doubt on the entire RD design.

**Q3.** A narrow bandwidth (e.g., ages 20--22) reduces bias because people very close to the cutoff are nearly identical, and nonlinear trends in the running variable have less room to confuse the estimate. However, it increases variance because fewer observations are used. A wide bandwidth (ages 19--23) uses more data, giving more precise estimates, but risks bias from nonlinear trends that could be mistaken for a discontinuity. The optimal choice balances this bias-variance tradeoff.

**Q4.** If people can manipulate the running variable to land on their preferred side of the cutoff, the groups just above and just below are no longer comparable --- those who manipulated are systematically different. Age cannot be manipulated (you cannot choose your birthday), which is why the MLDA design is strong. Exam scores, however, can be manipulated: students might retake exams, cheat, or receive score adjustments. A concerning example would be a tax threshold where accountants manipulate reported income to fall just below the cutoff for a higher tax rate.

### Research Tasks

**R1.**

::: {#tbl-sol-alcohol .cell tbl-cap='RD estimates: alcohol-related vs. motor vehicle deaths' execution_count=7}
```python
import pandas as pd
import statsmodels.formula.api as smf

mlda = pd.read_csv(DATA + "ch4/mlda_clean.csv")

# Compare RD estimates for alcohol and MVA deaths
# Loop through two causes of death and run the same RD regression for each
rows = []
for var, label in [("alcohol", "Alcohol-related"), ("mva", "Motor vehicle")]:
    model = smf.ols(f"{var} ~ over21 + age", data=mlda)
    r = model.fit(cov_type="HC1")
    rows.append({
        "Cause": label,
        "RD estimate (over21)": round(r.params["over21"], 2),
        "SE": round(r.bse["over21"], 2),
        "t-stat": round(r.tvalues["over21"], 2),
    })

pd.DataFrame(rows)
```


**Output:**

```
   Cause            RD estimate (over21)  SE    t-stat
-  ---------------  --------------------  ----  ------
0  Alcohol-related  0.44                  0.21  2.15
1  Motor vehicle    4.53                  0.72  6.32
```


The alcohol-related death jump is much smaller than the MVA jump (roughly one-fifth the size), but it is statistically significant. This makes sense: relatively few young people die directly from alcohol poisoning, but many die in alcohol-related car accidents. The dominant mechanism through which legal drinking kills is drunk driving, not direct alcohol toxicity.

**R2.**

::: {#cell-fig-sol-suicide .cell execution_count=8}
```python
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

# Split data at the cutoff
below = mlda[mlda["age"] < 0]
above = mlda[mlda["age"] >= 0]

# Fit separate lines
fit_below = smf.ols("suicide ~ age", data=below).fit()
fit_above = smf.ols("suicide ~ age", data=above).fit()

# Plot
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(mlda["agecell"], mlda["suicide"], color="gray", alpha=0.6, s=35)
ax.plot(below["agecell"], fit_below.predict(below), "k-", linewidth=2)
ax.plot(above["agecell"], fit_above.predict(above), "k-", linewidth=2)
ax.axvline(x=21, color="red", linestyle="--", alpha=0.5)
ax.set_xlabel("Age (years)")
ax.set_ylabel("Deaths per 100,000")
ax.set_title("Suicide deaths around the MLDA cutoff")
plt.tight_layout()
plt.show()
```


**Output:**

![RD plot for suicide deaths around the MLDA cutoff](04-regression-discontinuity_files/figure-html/fig-sol-suicide-output-1.png){#fig-sol-suicide width=854 height=470}


The visual shows a modest upward jump at age 21, consistent with the regression estimate of about 1.8 deaths per 100,000. The effect is smaller and noisier than for motor vehicle accidents. Alcohol can contribute to suicide through impulsivity and impaired judgment, but the link is less direct than for drunk driving.

**Q5.** "Local" means the RD estimate applies specifically to people at the cutoff --- those just turning 21. At age 18, people may have less driving experience, so the mortality effect of alcohol access could be different. At age 25, people may drink more responsibly. The RD cannot tell us about these other ages without extrapolation, which requires stronger assumptions about how the treatment effect varies with age.

**R3.**

::: {#tbl-sol-quadratic .cell tbl-cap='Linear vs. quadratic RD specification for all-cause mortality' execution_count=9}
```python
import pandas as pd
import statsmodels.formula.api as smf

mlda = pd.read_csv(DATA + "ch4/mlda_clean.csv")

# Linear specification
model_lin = smf.ols("all ~ over21 + age", data=mlda)
r_lin = model_lin.fit(cov_type="HC1")

# Quadratic specification with interactions
model_quad = smf.ols("all ~ over21 + age + age2 + over_age + over_age2", data=mlda)
r_quad = model_quad.fit(cov_type="HC1")

pd.DataFrame({
    "Specification": ["Linear", "Quadratic (interacted)"],
    "RD estimate (over21)": [round(r_lin.params["over21"], 2), round(r_quad.params["over21"], 2)],
    "SE": [round(r_lin.bse["over21"], 2), round(r_quad.bse["over21"], 2)],
})
```


**Output:**

```
   Specification           RD estimate (over21)  SE
-  ----------------------  --------------------  ----
0  Linear                  7.66                  1.51
1  Quadratic (interacted)  9.55                  1.83
```


The quadratic estimate is somewhat larger (~9.5 vs. ~7.7) because it allows the trend to curve differently on each side of the cutoff. Both estimates are statistically significant and in the same ballpark. The fact that the estimate is robust to polynomial order strengthens confidence in the RD design.
