"""Execute every standalone lesson and its optional solution; validate study coverage.

Writes review evidence only under .work/exploration-qa/. Run with uv run --with pip python.
"""
import concurrent.futures
import html
import json
import os
import re
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
import numpy as np
import pandas as pd
from exploration_content import CASES
from build_explorations import simulation_cells

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.work/exploration-qa'
OUT.mkdir(parents=True,exist_ok=True)
kernels=OUT/'jupyter/kernels/exploration-qa'
kernels.mkdir(parents=True,exist_ok=True)
(kernels/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Exploration QA','language':'python'}))
os.environ['JUPYTER_PATH']=str(OUT/'jupyter')
os.environ['PLOTLY_RENDERER']='notebook_connected'

# Independent inventory from chapter sources, not the generated page.
expected=set()
for path in (ROOT/'notebooks_quarto').glob('*.qmd'):
    expected.update(re.findall(r'(?:DATA|GITHUB_DATA_URL)\s*\+\s*["\'](ch\d+/[^"\']+\.csv)["\']',path.read_text()))
assert len(expected)==15
assert {Path(x).stem for x in expected}==set(CASES)
notebooks=sorted((ROOT/'notebooks_colab').glob('explore-*.ipynb'))
assert len(notebooks)==16

# Compare all six reconstructed simulation dataframes against the actual chapter draws.
source=(ROOT/'notebooks_quarto/02-regression.qmd').read_text()
actual={'np':np,'pd':pd}; generated={'np':np,'pd':pd,'scenarios':{},'true_effects':{}}
starts=['ability =','ability2 =','ability3 =','ability4 =','ability_r =','ability_s =']
ends=['students = pd.DataFrame','students2 = pd.DataFrame','students3 = pd.DataFrame','students4 = pd.DataFrame','df_r = pd.DataFrame','df_s = pd.DataFrame']
# Build expressions from the first seeded block for each unique variant, stopping before regression.
blocks=re.findall(r'```\{python\}\n(.*?)```',source,re.S)
variant_frames=[]
for marker in starts:
    block=next(b for b in blocks if marker in b and 'np.random.seed(42)' in b)
    start=block.index('np.random.seed(42)')
    lines=block[start:].splitlines()
    kept=[]; in_frame=False; balance=0
    for line in lines:
        if 'pd.DataFrame({' in line:in_frame=True
        kept.append(line)
        if in_frame:
            balance+=line.count('(')-line.count(')')
            if balance==0:break
    # n is defined in the baseline and reused in source exercises.
    actual['n']=1000
    exec('\n'.join(kept),actual)
    frame_name=next(re.match(r'(\w+)\s*=',line).group(1) for line in kept if 'pd.DataFrame({' in line)
    variant_frames.append(actual[frame_name].copy())
for c in simulation_cells():
    if c['cell_type']=='code':exec(''.join(c['source']),generated)
for expected_frame,result in zip(variant_frames,generated['scenarios'].values()):
    expected_frame=expected_frame.rename(columns={'family_income':'income'})
    for column in expected_frame.columns:
        np.testing.assert_array_equal(expected_frame[column].to_numpy(),result[column].to_numpy())
print('PASS: 15-CSV coverage and exact six-scenario source equivalence',flush=True)


def run(path):
    nb=nbformat.read(path,as_version=4)
    nbformat.validate(nb)
    # Append the actual concealed solution, rather than a separate reimplementation.
    solutions=[]
    for cell in nb.cells:
        if cell.cell_type=='markdown':
            text=cell.source
            solutions += [html.unescape(s) for s in re.findall(r'<pre><code>(.*?)</code></pre>',text,re.S)]
    for solution in solutions:nb.cells.append(nbformat.v4.new_code_cell(solution))
    NotebookClient(nb,timeout=180,kernel_name='exploration-qa',allow_errors=False,resources={'metadata':{'path':str(ROOT)}}).execute()
    errors=[o for c in nb.cells if c.cell_type=='code' for o in c.outputs if o.output_type=='error']
    assert not errors
    for c in nb.cells:
        if c.cell_type=='code':
            assert c.execution_count is not None
    nbformat.write(nb,OUT/path.name)
    # Review HTML shows the lesson only; appended solution checks stay in QA output.
    preview = nbformat.from_dict(dict(nb))
    preview.cells = nb.cells[:-len(solutions)] if solutions else nb.cells
    exported,_=HTMLExporter().from_notebook_node(preview)
    (OUT/(path.stem+'.html')).write_text(exported)
    return {'notebook':path.name,'status':'passed','code_cells':sum(c.cell_type=='code' for c in nb.cells),'solutions_executed':len(solutions)}

results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures={pool.submit(run,p):p for p in notebooks}
    for f in concurrent.futures.as_completed(futures):
        p=futures[f]
        try:
            result=f.result();results.append(result);print('PASS',p.name,flush=True)
        except Exception as e:
            results.append({'notebook':p.name,'status':'failed','error':str(e)})
            print('FAIL',p.name,str(e)[-1500:],flush=True)
(OUT/'notebook-execution.json').write_text(json.dumps(results,indent=2))
assert len(results)==16 and all(r['status']=='passed' for r in results)
print('PASS: all 16 notebooks and concealed solutions executed from clean kernels',flush=True)
