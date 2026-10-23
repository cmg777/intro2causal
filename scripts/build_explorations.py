"""Build standalone beginner notebooks and compact page previews from curated cases.

Run after build_data_dictionary.py. No remote data or services required to build.
Notebooks themselves load the published raw GitHub CSVs.
"""
import hashlib
import html
import json
from pprint import pformat
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
from exploration_content import CASES, DEFINITIONS, LABELS, PREP, WEIGHTS

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raw.githubusercontent.com/cmg777/intro2causal/main/data/'
SITE = 'https://cmg777.github.io/intro2causal/'
COLAB = 'https://colab.research.google.com/github/cmg777/intro2causal/blob/main/notebooks_colab/'
COLORS = ['#2563eb', '#7c3aed', '#059669', '#64748b']
px.defaults.template = 'plotly_white'
px.defaults.color_continuous_scale = 'Blues'
px.defaults.color_discrete_sequence = COLORS
SETUP = '''import pandas as pd
import plotly.express as px
from IPython.display import display

# One consistent chart style; no plotting experience needed.
px.defaults.template = "plotly_white"
px.defaults.color_continuous_scale = "Blues"
px.defaults.color_discrete_sequence = ["#2563eb", "#7c3aed", "#059669", "#64748b"]'''

def markdown(text):
    return {'cell_type':'markdown','metadata':{},'source':text.strip().splitlines(True)}

def code(text):
    return {'cell_type':'code','execution_count':None,'metadata':{},'outputs':[], 'source':text.strip().splitlines(True)}

def notebook(cells, name):
    for i,c in enumerate(cells):
        c['id']=hashlib.sha256((name+str(i)).encode()).hexdigest()[:10]
    n={'cells':cells,'metadata':{'colab':{'name':name,'toc_visible':True},'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
    (ROOT/'notebooks_colab'/name).write_text(json.dumps(n,ensure_ascii=False,indent=1)+'\n')

def reveal(title,text):
    return f'<details>\n<summary>{title}</summary>\n\n{text}\n\n</details>'

def solution_block(text):
    # HTML pre avoids inconsistent fenced-code rendering inside Colab details.
    return '<pre><code>'+html.escape(text)+'</code></pre>'

def first_run():
    return markdown('''## Your first few minutes in Colab · 3 minutes

You do not need prior Python experience. A **cell** is one block of text or code. Read the text, then press the **▶** beside the next code cell (or Shift+Enter). Its output appears underneath. Run cells in order: later cells use tables created earlier.

Choose **File → Save a copy in Drive** if you want to keep your changes. If a name is “not defined,” run the earlier setup cells again. **Runtime → Restart session and run all** gives you a fresh start. An error does not mean you have damaged the data: this notebook only reads it.

Keep a short learning log in a text cell. Before each chart, make a prediction. Afterward, write one observation with a number and one question that the chart cannot answer.

**Chart controls:** hover for values, click legend labels to hide/show a group, drag to zoom, and double-click to reset. A chart’s menu also offers a reset/autoscale control.

The setup installs Plotly Express if needed. `import` makes a library available; `pd` and `px` are short names for pandas (tables) and Plotly Express (charts).''')

def key_table(c):
    return '| Column | What it records |\n|---|---|\n'+'\n'.join(f'| `{k}` | {DEFINITIONS[k]} |' for k in c['keys'])

def exercise(c):
    p=c['practice']
    return [markdown(f'''## Make it yours · 8 minutes

### 1. Modify an example

{p['modify']}

Copy that chart cell before editing, so you can compare the original and modified outputs. Say what changed in your question as well as in your code.

### 2. Try a small investigation

{p['task']}

Write a prediction first. The optional starter cell below is safe to leave unchanged; later cells do not depend on your answer.'''),
    code('# Your investigation goes here.\n# Describe your expected pattern before writing code.'),
    markdown(reveal('Hint 1 · choose the right evidence',p['hints'][0])+'\n\n'+reveal('Hint 2 · a Python starting point',p['hints'][1])+'\n\n'+reveal('Optional worked solution · open after trying',solution_block(p['solution'])+'\n\n'+p['interpretation']+'\n\nCopy the code into the starter cell to run it.'))]

def weighted(key):
    if key not in WEIGHTS:return []
    value,group,weight,explanation=WEIGHTS[key]
    source='df[df["dtype"] == "all"]' if key=='deaths_clean' else 'df'
    text=f'''## Optional extension · do weights change the picture?

{explanation}

A **weighted mean** multiplies each value by its weight, adds those products, and divides by the sum of weights. The code below drops rows missing any required value and keeps positive weights. Each group gets its own denominator. This is a descriptive calculation, not an uncertainty estimate or a causal adjustment.

Predict whether weighting will change the comparison. Then compare the two summaries and explain which units receive more influence.'''
    calc=f'''weighted_data = {source}.dropna(subset=["{value}", "{group}", "{weight}"]).copy()
weighted_data = weighted_data[weighted_data["{weight}"] > 0]
weighted_data["product"] = weighted_data["{value}"] * weighted_data["{weight}"]
totals = weighted_data.groupby("{group}")[["product", "{weight}"]].sum()
weighted_mean = totals["product"] / totals["{weight}"]
unweighted_mean = weighted_data.groupby("{group}")["{value}"].mean()
comparison = pd.DataFrame({{"Equal row weights": unweighted_mean, "Source weights": weighted_mean}})
display(comparison.round(3))'''
    return [markdown(text),code(calc)]

def build_case(d):
    key=Path(d['file']).stem;c=CASES[key];name=f'explore-{key}.ipynb'
    c['chapter']=d['chapter'];c['id']=d['id'];c['file']=d['file'];c['notebook']=name
    c['rows']=d['rows'];c['columns']=d['columns'];c['unit']=d['unit'];c['kind']=d['kind'];c['chapterTitle']=d['chapterTitle']
    c['guide']=d['notebook'].replace('.qmd','.html')
    c['definitions']={f['name']:f['meaning'] for f in d['fields']}
    intro=f'''# {c['title']}

**A guided investigation · Chapter {d['chapter']} · 30–45 minutes · No Python experience needed**

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name})

> **The question**  
> {c['question']}

{c['story']}

### By the end, you will be able to…

- {c['takeaway']}
- Read and modify three interactive charts using short Python examples.
- Explain one reason a descriptive pattern alone cannot settle this case’s causal question.

### Before you see the evidence

{c['prediction']}

Write two sentences now. You will return to them at the end.

**Your route:** meet the data → inspect three views → modify and try → ask the causal question.'''
    cells=[markdown(intro),first_run(),code('%pip install -q "plotly>=6,<7"'),code(SETUP),
      markdown(f'''## Meet the data · 5 minutes

**One row:** {d['unit']}  
**Stored size:** {d['rows']:,} rows × {d['columns']} columns.

{key_table(c)}

{c['caution']}

`read_csv` downloads a table. We call it `df`. `head(5)` shows just five rows, not a separate sample used for the analysis. Square brackets select columns by their names.'''),
      code(f'DATA_URL = "{BASE}{d["file"]}"\ndf = pd.read_csv(DATA_URL)\nprint(f"Loaded {{len(df):,}} rows and {{len(df.columns)}} columns")\ndisplay(df[{c["keys"]!r}].head(5))'),
      markdown('''### Pause: what do the rows mean?

Choose one displayed row. Translate it into a sentence using the variable guide. Which values are categories or identifiers? Which are quantities? A numeric storage type does not necessarily make a code a meaningful measurement.

The next table checks types, missing values, and the number of distinct values for the key columns. `isna()` marks missing cells; `sum()` counts them. Missing is not zero. Ask which comparison would lose a row if one of its required values were missing.'''),
      code(f'''key_columns = {c['keys']!r}
checks = pd.DataFrame({{"storage_type": df[key_columns].dtypes.astype(str),
                       "missing_rows": df[key_columns].isna().sum(),
                       "distinct_values": df[key_columns].nunique()}})
display(checks)
print("The charts below omit missing values required for each plotted quantity.")'''),
      markdown('''### A small summary before plotting

`describe()` summarizes numeric columns: `count` counts available values, `mean` is the average, and `50%` is the median. The median splits ordered values into two halves. Averages of identifiers or arbitrary category codes are not useful descriptions, even if Python calculates them.

For category-like key variables, the second table counts values, including missing entries. Check these labels before interpreting a chart.'''),
      code(f'''numeric_keys = df[key_columns].select_dtypes(include="number").columns
if len(numeric_keys):
    display(df[numeric_keys].describe().round(2))
for column in key_columns:
    if df[column].nunique() <= 8:
        display(df[column].value_counts(dropna=False).rename("Rows").to_frame())'''),
      markdown('''## Read the chart code · 2 minutes

`px.bar`, `px.scatter`, `px.line`, and `px.box` choose a chart type. `x` and `y` name columns for the axes; `color` distinguishes groups or values. `labels` translates column names for readers. `fig.show()` displays the result.

A table transformation and a plot answer different questions: first decide what each plotted row represents, then choose how to display it. Before running each chart, predict what you expect to see.'''),
      code('# Display labels: run once; you do not need to memorize this mapping.\nlabels = '+pformat({k:v for k,v in LABELS.items() if k in {f['name'] for f in d['fields']} | {'plan','offer','group','state_name','ability_group','census'}}, width=90))]
    if key in PREP:
        cells += [markdown('''### Keep known plan assignments

We exclude unknown plan types from plan comparisons and translate codes into readable labels. `notna()` identifies nonmissing assignments; `map` replaces a code with a label. The earlier missing-value check still includes the full stored file.'''),code(PREP[key])]
    for i,s in enumerate(c['steps'],1):
        cells.extend([markdown(f'''## Visual investigation {i} · {s['title']}

**Predict:** {s['question']}

{s['explain']}'''),code(s['code']+'\nfig.show()'),
          markdown(f'''**Explore the chart:** {s['interact']}

**Write before reading on:** Describe one pattern with its unit and comparison group. Then give one possible explanation.

{reveal('Interpretation checkpoint',s['interpret'])}''')])
    cells+=exercise(c)+weighted(key)
    source=f'[{c["source"]}]({c["sourceUrl"]})' if c['sourceUrl'] else c['source']+' (citation only; no verified destination included)'
    cells += [markdown(f'''## What can you now say? · 4 minutes

Return to your initial prediction. Write a four-sentence evidence note:

1. **I expected…** State your prediction.
2. **I observed…** Use a chart, a comparison, and the correct units.
3. **This does not establish…** Name a causal claim the evidence cannot settle.
4. **To learn more, I would need…** Propose an additional measurement or a more credible comparison.

### Carry this question into the chapter

**{c['bridge']}**

[Continue with Chapter {d['chapter']}: {d['chapterTitle']}]({SITE}{c['guide']}) · [Return to the case collection]({SITE}data-dictionary.html#{d['id']})

### Source and preparation notes

{source}

{d['provenance']}

These exploratory charts are based on the committed CSV. They are not a complete replication of the original study. Keep the source study, this prepared extract, and your descriptive results distinct.''')]
    notebook(cells,name)
    # Execute explicit lesson transformations locally to generate a compact preview.
    env={'df':pd.read_csv(ROOT/'data'/d['file']),'pd':pd,'np':np,'px':px,'labels':LABELS}
    if key in PREP:exec(PREP[key],env)
    # Preview chooses an informative aggregate with modest payload size.
    preview_idx={'nhis_clean':0,'rand_balance':1,'rand_health_outcomes':1,'rand_utilization':1,
      'mdve_clean':1,'mlda_clean':0,'banks_clean':0,'deaths_clean':0,'qob_clean':1,
      'twins_clean':1,'childlabor_clean':0,'sheepskin_clean':0,'synthetic_ovb':1,'synthetic_rct':1,'synthetic_did':0}[key]
    for i,s in enumerate(c['steps']):
        exec(s['code'],env)
        if i==preview_idx:
            fig=env['fig'];fig.update_layout(template=None,height=340,title=None,margin=dict(l=55,r=20,t=20,b=65),font=dict(family='Inter, system-ui',size=12),legend=dict(orientation='h',y=-0.25,x=0,title=None),colorway=COLORS)
            figure=json.loads(pio.to_json(fig,engine='json'))
            path=ROOT/'assets'/'exploration-previews'/f'{key}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(figure,separators=(',',':'))+'\n')
            c['preview']={'file':f'assets/exploration-previews/{key}.json','question':s['question'],'caption':s['interpret']}
            # Keyboard-readable evidence from the same trace data, without requiring hover.
            table=[]
            for trace in fig.data:
                x=list(trace.x) if getattr(trace,'x',None) is not None else []
                y=list(trace.y) if getattr(trace,'y',None) is not None else []
                z=getattr(trace,'z',None)
                if z is not None:
                    for row_index,yval in enumerate(y):
                        for col_index,xval in enumerate(x):table.append([str(yval)+' / '+str(xval),float(z[row_index][col_index])])
                elif trace.type in ('box','histogram'):
                    values=pd.Series(y if y else x)
                    if pd.api.types.is_numeric_dtype(values):table.append([trace.name or 'Values',float(values.median())])
                else:
                    for xv,yv in zip(x,y):
                        if pd.notna(yv):table.append([f'{trace.name+": " if trace.name else ""}{xv}',float(yv)])
            c['preview']['table']=table[:12]
            if any(t.type == 'heatmap' for t in fig.data):
                value_label = fig.layout.coloraxis.colorbar.title.text or 'Value'
            elif any(t.type == 'histogram' for t in fig.data):
                value_label = 'Median ' + (fig.layout.xaxis.title.text or 'value')
            elif any(t.type == 'box' for t in fig.data):
                value_label = 'Median ' + (fig.layout.yaxis.title.text or 'value')
            else:
                value_label = fig.layout.yaxis.title.text or 'Value'
            c['preview']['valueLabel'] = value_label
            c['preview']['tableNote']='First 12 plotted values; open the notebook for the full data.' if len(table)>12 else ('Median per group (distribution preview).' if any(t.type in ('box','histogram') for t in fig.data) else 'Values represented in the preview.')
    return c


def simulation_cells():
    """Exact Chapter 2 DGPs, with separate seed resets and source draw order."""
    specs=[
      ('Baseline selection','Higher ability raises the chance of private attendance; the true school effect is $5,000.',5000,5,False,False,False),
      ('No treatment effect','Keep ability-based selection but remove the school effect. A raw gap can remain even when the true effect is zero.',0,5,False,False,False),
      ('Stronger selection','Divide ability by 2 instead of 5 in the assignment equation, making selection steeper. The effect remains $5,000.',5000,2,False,False,False),
      ('Add family income','Income now influences both attendance and earnings. The effect remains $5,000.',5000,5,True,False,False),
      ('Reverse selection','Higher ability now makes private attendance less likely. The effect remains $5,000, but the direction of confounding reverses.',5000,5,False,False,True),
      ('Three confounders','Ability, income, and motivation each influence attendance and earnings. The effect remains $5,000.',5000,5,True,True,False)]
    cells=[]
    for i,(name,note,effect,scale,income,motivation,reverse) in enumerate(specs,1):
        s='np.random.seed(42)\nn = 1000\nability = np.random.normal(50, 10, n)\n'
        if income:s+='income = np.random.normal(60000, 20000, n)\n'
        if motivation:s+='motivation = np.random.normal(5, 2, n)\n'
        term=f'(ability - 50) / {scale}'
        if income:term+=' + (income - 60000) / 20000'
        if motivation:term+=' + (motivation - 5) / 2'
        s+=f'prob_private = 1 / (1 + np.exp({"" if reverse else "-"}({term})))\nprivate = np.random.binomial(1, prob_private)\n'
        s+=f'earnings = {10000 if income else 30000} + {effect} * private + 800 * ability'
        if income:s+=' + 0.3 * income'
        if motivation:s+=' + 2000 * motivation'
        s+=' + np.random.normal(0, 5000, n)\n'
        cols='"ability": ability, "private": private, "earnings": earnings'
        if income:cols+=', "income": income'
        if motivation:cols+=', "motivation": motivation'
        s+=f'scenarios["{i}. {name}"] = pd.DataFrame({{{cols}}})\ntrue_effects["{i}. {name}"] = {effect}'
        cells.extend([markdown(f'### Scenario {i} · {name}\n\n{note}\n\nPredict how the observed earnings gap will change. Run this short construction cell; you do not need to memorize the equations.'),code(s)])
    return cells


def build_simulations():
    name='explore-chapter-2-simulations.ipynb'
    cells=[markdown(f'''# One earnings gap. Six different stories.

**Chapter 2 · Guided simulation lab · 30–45 minutes · Complete beginners welcome**

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name})

> **Can a school appear to raise earnings even when its true effect is zero?**

Imagine comparing earnings of people who attended private and other schools. Attendance may reflect ability, family resources, and motivation, all of which could also affect earnings. In real observational data, we do not know the true school effect. In this lab, we construct six worlds and choose that effect ourselves. Each world contains 1,000 simulated students, and each changes a specific feature of selection or confounding. These are the six scenarios in the Chapter 2 Python exercises, reproduced with the same equations and seed resets. None is a real student dataset, and none uses randomized school attendance. That distinction matters: changing the treatment effect is different from making treatment random.

**You will learn to:** distinguish a raw gap from a known effect; visualize selection on ability; explain why reversing selection can reverse bias.

**Predict before running:** Could privately educated students earn more even if private education had no causal effect? Write one explanation.

**Route:** construct six worlds → inspect one → compare gaps → change one view → explain the causal lesson.'''),first_run(),code('%pip install -q "plotly>=6,<7"'),code(SETUP+'\nimport numpy as np\nscenarios = {}\ntrue_effects = {}'),
    markdown('''## Build six small worlds · 8 minutes

`np.random.seed(42)` restarts a reproducible sequence of random draws. Each scenario restarts it, as the chapter does. Ability is normally distributed around 50. The assignment equation converts characteristics to a probability between 0 and 1; `binomial(1, probability)` draws private attendance as 0 or 1. Earnings combine a school effect, other influences, and random noise.

Notice **which variables enter both assignment and earnings**. That is the central reasoning task. The six short cells expose the construction; running them is enough to continue.''')]
    sim=simulation_cells();cells+=sim
    cells += [markdown('''## Meet one world · 4 minutes

Each row is a simulated student. `private` is an attendance indicator (1 private, 0 other); `ability` is a constructed score; `earnings` is annual earnings in simulated dollars. Here earnings are **not logs**, unlike some Chapter 6 CSVs.

`head` shows rows; the next table checks types and missingness. `describe` summarizes numeric variables. The attendance counts describe a category, even though its storage type is numeric.'''),
    code('''baseline = scenarios["1. Baseline selection"]
display(baseline.head())
display(pd.DataFrame({"type": baseline.dtypes.astype(str), "missing": baseline.isna().sum()}))
display(baseline.describe())
display(baseline["private"].value_counts().rename("Students"))'''),
    markdown('''## Visual investigation 1 · who attends which school?

**Predict:** will ability be similarly distributed in the two attendance groups?

`map` turns 0 and 1 into readable labels. A box shows the middle half of the ability distribution, with its median inside.'''),
    code('''baseline = baseline.assign(school=baseline["private"].map({0: "Other school", 1: "Private school"}))
fig = px.box(baseline, x="school", y="ability", color="school", points=False, labels={"school": "Attendance", "ability": "Simulated ability"}, title="Selection is visible before comparing earnings")
fig.show()'''),
    markdown('''**Explore:** hover over the boxes. Explain why their difference matters if ability also affects earnings.

**Checkpoint:** higher ability makes private attendance more likely in this world. A raw earnings comparison therefore bundles the school effect with an ability difference.'''),
    markdown('''## Visual investigation 2 · compare what we see with what we know

For each world, subtract mean earnings among other-school students from mean earnings among private-school students. The `for` loop repeats the same calculation for each named table. A list collects the results; `DataFrame` makes that list into a table.

**Predict:** in which world should the observed gap be most misleading?'''),
    code('''rows = []
for name, students in scenarios.items():
    means = students.groupby("private")["earnings"].mean()
    rows.append({"scenario": name, "Observed gap": means.loc[1] - means.loc[0], "Known school effect": true_effects[name]})
comparison = pd.DataFrame(rows)
long = comparison.melt(id_vars="scenario", var_name="quantity", value_name="dollars")
fig = px.scatter(long, x="dollars", y="scenario", color="quantity", symbol="quantity", labels={"dollars": "Annual earnings difference (simulated dollars)", "scenario": "World", "quantity": "Quantity"}, title="A raw gap is not the school effect")
fig.add_vline(x=0, line_dash="dot")
fig.show()'''),
    markdown('''**Explore:** hover over both points for the zero-effect world and the reversed-selection world. State the observed gap and known effect separately.

**Checkpoint:** the zero-effect world can display a positive earnings gap because of selection. Reversing selection can push the observed gap below the positive school effect. Random noise also contributes to finite-sample differences.'''),
    markdown('''## Visual investigation 3 · connect the discrepancy to selection

**Predict:** which world puts lower-ability students into private education?

We now repeat the difference-in-means calculation for ability, which exists in every world. This is evidence about one confounder, not a complete explanation of the multi-confounder worlds.'''),
    code('''ability_rows = []
for name, students in scenarios.items():
    means = students.groupby("private")["ability"].mean()
    ability_rows.append({"scenario": name, "ability_gap": means.loc[1] - means.loc[0]})
ability_gaps = pd.DataFrame(ability_rows)
fig = px.bar(ability_gaps, x="ability_gap", y="scenario", orientation="h", labels={"ability_gap": "Private minus other: mean ability", "scenario": "World"}, title="The direction of selection can change")
fig.add_vline(x=0, line_dash="dot")
fig.show()'''),
    markdown('''**Explore:** compare the sign of the ability gap with the observed-minus-known earnings discrepancy. Why is ability alone insufficient in worlds 4 and 6?

**Checkpoint:** the direction of selection changes the interpretation of the raw comparison. Knowing the true effect is a privilege of a simulation, not a feature of real observational data.''')]
    exercise_case={'practice':dict(modify='Change the ability box plot to use scenario 5. Predict how the group ordering will change.',task='Plot earnings against ability in the zero-effect world, colored by school attendance.',hints=['Choose scenarios["2. No treatment effect"].','Map private to readable school labels, then use px.scatter with x="ability" and y="earnings".'],solution='''zero = scenarios["2. No treatment effect"].copy()
zero["school"] = zero["private"].map({0: "Other school", 1: "Private school"})
fig = px.scatter(zero, x="ability", y="earnings", color="school", opacity=0.5, labels={"ability": "Simulated ability", "earnings": "Annual earnings (simulated dollars)", "school": "Attendance"})
fig.show()''',interpretation='School attendance sorts students along ability even when its direct earnings effect is zero. The color pattern does not imply that the school caused their earnings.')}
    cells+=exercise(exercise_case)
    cells += [markdown(f'''## Return to your prediction · 4 minutes

Write an evidence note: one observed gap, its known effect, one source of their difference, and one assumption you would need in real data. Explain why a zero effect does not imply a zero observed gap.

**Next question:** When can regression adjustment separate a treatment effect from selection—and what happens when a confounder remains unobserved?

[Continue with Chapter 2: Regression]({SITE}book/_book/notebooks_quarto/02-regression.html) · [Return to the case collection]({SITE}data-dictionary.html#chapter-2-simulations)

**Construction:** exact six Python simulation variants in the chapter, seed 42 restarted for each, 1,000 students per world, normal earnings noise with SD $5,000. The known effect is $0 in scenario 2 and $5,000 in scenarios 1 and 3–6. No survey weights apply. The scenarios change equations, not just random samples.''')]
    notebook(cells,name)
    # Return the exact DGP source for validation and website preview generation.
    return sim


def main():
    from plotly.offline import get_plotlyjs
    vendor = ROOT/'assets/vendor/plotly.min.js'
    vendor.parent.mkdir(exist_ok=True)
    vendor.write_text(get_plotlyjs())
    summary=json.loads((ROOT/'data/dictionary-summary.json').read_text())
    cases=[build_case(d) for d in summary['datasets']]
    sim=build_simulations()
    env={'np':np,'pd':pd,'scenarios':{},'true_effects':{}}
    for c in sim:
        if c['cell_type']=='code':exec(''.join(c['source']),env)
    rows=[]
    for name,df in env['scenarios'].items():
        means=df.groupby('private')['earnings'].mean()
        rows.append({'scenario':name,'Observed gap':float(means[1]-means[0]),'Known effect':env['true_effects'][name]})
    public=[]
    for c in cases:
        public.append({k:v for k,v in c.items() if k not in ('steps','practice')})
    (ROOT/'data/exploration-cases.json').write_text(json.dumps({'cases':public,'simulations':rows},ensure_ascii=False,separators=(',',':'))+'\n')
    print(f'Built {len(cases)} case notebooks, the simulation lab, and {len(cases)} interactive previews.')

if __name__=='__main__':main()
