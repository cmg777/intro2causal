"""Build compact, unweighted profiles for CSVs loaded by the six study guides."""
import csv, json, math, re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "dictionary-summary.json"
CHAPTERS = {1:"Randomized Trials",2:"Regression",3:"Instrumental Variables",4:"Regression Discontinuity",5:"Differences-in-Differences",6:"The Wages of Schooling"}
META = {
"ch1/nhis_clean.csv":("NHIS 2009: insurance and health", "Empirical · survey", "Do insured and uninsured people differ in observed health and socioeconomic characteristics?", "Person in the 2009 NHIS sample of married, employed adults ages 26–59.", "`code/python/ch1/prepare_data.py` selects married adults, positive person weight, nonmissing own/spouse insurance, one woman per household, ages 26–59, employed household, and households with more than one sampled person. It recodes Stata categories, creates household size/spouse insurance, and writes 10 teaching columns. Survey weight is retained as `weight`; displayed profiles remain unweighted.","notebooks_quarto/01-randomized-trials.qmd", "CDC NHIS", "https://www.cdc.gov/nchs/nhis/2009nhis.htm"),
"ch1/rand_balance.csv":("RAND HIE: baseline balance", "Empirical · randomized experiment", "Were participants assigned to different insurance plans comparable at baseline?", "RAND Health Insurance Experiment participant.", "`code/python/ch1/prepare_data.py` maps demographics, baseline outcomes, plan indicators and a numeric family identifier from `rand_initial_sample_2.dta`. It sets the free-plan indicator missing when plan type is missing; otherwise retains source rows. Profiles are unweighted.","notebooks_quarto/01-randomized-trials.qmd", "RAND HIE documentation", "https://doi.org/10.3886/ICPSR06439.v1"),
"ch1/rand_utilization.csv":("RAND HIE: utilization and spending", "Empirical · randomized experiment", "How did insurance generosity affect healthcare use and spending?", "Participant-year after inner joining claims and annual spending.", "The preparation script inner-joins source files on person and year, maps 24 plans into four types, applies a year-specific CPI multiplier to expenses (constant 1991 dollars), sums total expense, and creates indicators/family ID. Profiles are unweighted.","notebooks_quarto/01-randomized-trials.qmd", "RAND HIE documentation", "https://doi.org/10.3886/ICPSR06439.v1"),
"ch1/rand_health_outcomes.csv":("RAND HIE: health outcomes", "Empirical · randomized experiment", "Did free care improve measured health outcomes?", "RAND HIE participant with exit health measures.", "The preparation script maps exit health measures, plan indicators and numeric family ID from the RAND source. Free-plan indicator is set missing when plan type is missing. Profiles are unweighted.","notebooks_quarto/01-randomized-trials.qmd", "RAND HIE documentation", "https://doi.org/10.3886/ICPSR06439.v1"),
"ch3/mdve_clean.csv":("Minneapolis Domestic Violence Experiment", "Empirical · randomized experiment", "What is the effect of arrest on repeat domestic violence?", "Police response to an eligible misdemeanor domestic assault call (330 cases in source study).", "The 1981–82 field experiment randomly assigned arrest, advice/mediation, or separation (suspect ordered away for eight hours). The notebook CSV retains only assigned treatment (`assigned`) and delivered treatment (`delivered`), written by code/python/ch3/prepare_data.py; it omits the study's recidivism outcomes.", "notebooks_quarto/03-instrumental-variables.qmd", "Sherman & Berk (1984)", "https://doi.org/10.2307/2094475"),
"ch4/mlda_clean.csv":("Minimum legal drinking age and mortality", "Empirical · aggregated", "Does legal access to alcohol at age 21 change mortality?", "Monthly age cell.", "The preparation script creates centered age, the age-21 indicator, cause-specific rates, external-other mortality by subtraction, and polynomial/interacted terms. Rates are source age-cell aggregates; no individual records are supplied. Mortality rates are deaths per 100,000 person-years.","notebooks_quarto/04-regression-discontinuity.qmd", "Carpenter & Dobkin (2009)", "https://doi.org/10.1257/app.1.1.164"),
"ch5/banks_clean.csv":("Mississippi bank failures", "Empirical · annual extract", "Did emergency Federal Reserve lending reduce bank failures?", "Annual July 1 snapshot of banks in business in each Federal Reserve district.", "Correction: despite the daily `banks.csv` source, this six-row file is produced by selecting July 1 rows, then holding the 1930 district gap constant to construct `counterfactual`. It is not a daily panel or a full annual aggregation.","notebooks_quarto/05-differences-in-differences.qmd", "Richardson & Troost (2009)", "https://doi.org/10.1086/605129"),
"ch5/deaths_clean.csv":("Minimum drinking age and death rates", "Empirical · state panel", "Did changes in legal drinking ages affect death rates among young people?", "State × year × death cause × age group.", "Prepared state panel derived from published MLDA research data. `pop` is an analysis weight, not used for the unweighted descriptive profiles here; the exact upstream transformation cannot be independently established from files in this repository.","notebooks_quarto/05-differences-in-differences.qmd#mlda-and-mortality", "Du Mouchel, Williams & Zador (1987)", "https://doi.org/10.2307/724056"),
"ch6/childlabor_clean.csv":("Child labor laws and schooling", "Empirical · aggregated cells", "Did compulsory schooling and child labor laws raise schooling and earnings?", "Birth-state × birth-year × census-year cell.", "Cell-level analysis file used by the notebook; this CSV is already aggregated and its upstream creation is not included in the repository. `weight`/cell sizes are distinct from the unweighted summaries shown.","notebooks_quarto/06-wages-of-schooling.qmd#child-labor-laws", "Acemoglu & Angrist (2000)", "https://doi.org/10.1257/aer.90.2.9"),
"ch6/qob_clean.csv":("Quarter of birth and schooling returns", "Empirical · census microdata extract", "Does compulsory schooling raise earnings?", "Man in U.S. Census sample.", "Prepared extract from Angrist and Krueger's 1980 Census data. Notebook analysis restricts birth cohorts as described there; the full source construction is not reproduced in this repository.","notebooks_quarto/06-wages-of-schooling.qmd#quarter-of-birth", "Angrist & Krueger (1991)", "https://doi.org/10.2307/2937954"),
"ch6/twins_clean.csv":("Twins and returns to schooling", "Empirical · twin pairs", "What is the return to schooling after controlling for shared family background?", "Individual twin within a twin pair.", "Prepared analysis extract from the Twinsburg study; notebook subsets/constructs twin-pair variables. Source preparation details beyond the notebook are not available here.","notebooks_quarto/06-wages-of-schooling.qmd#twins", "Ashenfelter & Krueger (1994)", "https://doi.org/10.1257/aer.84.5.1157"),
"ch6/sheepskin_clean.csv":("Texas exit exam and diploma returns", "Empirical · aggregated score cells", "Does receiving a diploma itself raise earnings near an exam cutoff?", "Exit-exam score bin.", "Forty-six score-bin means, not individual records. `n` and `person_years` are denominators/weights for different outcomes; profiles here treat each bin equally.","notebooks_quarto/06-wages-of-schooling.qmd#sheepskin-effects", "Clark & Martorell (2014)", "https://doi.org/10.1086/675238"),
"ch6/synthetic_ovb.csv":("Omitted-variable-bias demonstration", "Simulated · teaching data", "How does omitted ability bias an OLS schooling coefficient?", "Simulated individual.", "Generated by code/python/ch6/generate_synthetic.py (seed 2024, legacy NumPy global RNG). See generation details in source. The generator draws ability, schooling noise, occupation noise, then earnings noise; schooling and occupation are clipped and rounded.","notebooks_quarto/06-wages-of-schooling.qmd#omitted-variable-bias", "Generation code", "code/python/ch6/generate_synthetic.py"),
"ch6/synthetic_rct.csv":("Scholarship randomized trial", "Simulated · teaching data", "Can randomized scholarship assignment instrument for schooling?", "Simulated individual.", "Generated by code/python/ch6/generate_synthetic.py using the continuing seed-2024 RNG stream after synthetic_ovb. Assignment is Bernoulli(0.5); schooling is clipped to 6–20 and rounded. Earnings and continuous ability are rounded to four decimals.","notebooks_quarto/06-wages-of-schooling.qmd#scholarship-instrument", "Generation code", "code/python/ch6/generate_synthetic.py"),
"ch6/synthetic_did.csv":("Compulsory-schooling reform", "Simulated · teaching data", "How does two-way fixed-effects DiD recover a known reform effect?", "Simulated state-year.", "Generated by code/python/ch6/generate_synthetic.py after the OVB and RCT draws without resetting the seed. States 1–10 are treated; treatment starts in 2005. State baselines are drawn once per state, followed by schooling and earnings noise for each year.","notebooks_quarto/06-wages-of-schooling.qmd#difference-in-differences", "Generation code", "code/python/ch6/generate_synthetic.py"),
}

def clean(v):
    if v is None or not v.strip(): return None
    try:
        x=float(v)
        return x if math.isfinite(x) else None
    except ValueError: return v.strip()

def build_file(path):
    rel=path.relative_to(ROOT).as_posix(); key=rel.removeprefix("data/")
    with path.open(newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f); rows=list(reader); cols=reader.fieldnames or []
    title,kind,question,unit,provenance,notebook,source,source_url=META[key]
    fields=[]
    for name in cols:
        vals=[clean(r.get(name)) for r in rows]; present=[x for x in vals if x is not None]; nums=[x for x in present if isinstance(x,(int,float))]
        numeric=len(nums)==len(present) and bool(nums)
        freq=Counter(str(x) for x in present)
        identifier=bool(re.search(r"(^id$|_id$|^state$|^year$|^date$|^serial$|^pernum$)",name,re.I))
        categorical=(not numeric) or len(freq)<=12 or identifier
        record={"name":name,"type":"identifier" if identifier else ("categorical" if categorical else "numeric"),"n":len(present),"missingPct":round(100*(len(rows)-len(present))/len(rows),2) if rows else 0,
                "meaning":f"{name.replace('_',' ').capitalize()}; see notebook for its analytical use. The CSV does not supply a variable label.","role":"Identifier / grouping field" if identifier else ("Category or coded indicator" if categorical else "Measured quantity or outcome; units follow the source data.")}
        if numeric and nums:
            s=sorted(float(x) for x in nums); mean=sum(s)/len(s); sd=math.sqrt(sum((x-mean)**2 for x in s)/(len(s)-1)) if len(s)>1 else 0
            record["stats"]={"mean":mean,"sd":sd,"median":(s[(len(s)-1)//2]+s[len(s)//2])/2,"min":s[0],"max":s[-1]}
            if s[0] < s[-1]:
                bins=[0]*12
                for x in s: bins[min(11,int((x-s[0])/(s[-1]-s[0])*12))]+=1
                record["bins"]=bins
        if categorical:
            record["categories"]=[{"value":v,"count":c,"share":c/len(present) if present else 0} for v,c in freq.most_common()]
            record["distinct"]=len(freq)
        fields.append(record)
    anchor=re.sub(r"[^a-z0-9]+","-",key.lower()).strip("-")
    return {"id":anchor,"chapter":int(key[2]),"chapterTitle":CHAPTERS[int(key[2])],"file":key,"title":title,"kind":kind,"question":question,"unit":unit,"rows":len(rows),"columns":len(cols),"provenance":provenance,"notebook":notebook,"source":source,"sourceUrl":source_url,"fields":fields}

def main():
    files=[]
    # Coverage is defined by the data files referenced through pandas read_csv in notebooks_quarto.
    for qmd in sorted((ROOT/"notebooks_quarto").glob("*.qmd")):
        text=qmd.read_text()
        for rel in re.findall(r"(?:DATA|GITHUB_DATA_URL)\s*\+\s*[\"'](ch\d+/[^\"']+\.csv)[\"']",text):
            p=ROOT/"data"/rel
            if p.exists() and p not in files: files.append(p)
    payload={"generatedFrom":"notebooks_quarto/*.qmd and data/**/*.csv","profiles":"Unweighted; numeric SD uses sample denominator (n-1).","datasets":[build_file(p) for p in files]}
    OUT.write_text(json.dumps(payload,separators=(",",":"),ensure_ascii=False)+"\n")
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(files)} datasets, {sum(len(d['fields']) for d in payload['datasets'])} variables")
if __name__=="__main__": main()
