"""Build the homepage's inline SVGs from Colab inputs and reported results.

Run with the project environment: uv run python scripts/build_home_graphs.py
Use --check to verify committed markup and provenance without writing changes.
No synthetic observations, arbitrary fitted lines, or unreported estimates are added.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re

import pandas as pd
import pyfixest as pf

ROOT = Path(__file__).resolve().parents[1]
COLAB = 'https://colab.research.google.com/github/cmg777/intro2causal/blob/main/notebooks_colab/'


def notebook(name, cell):
    path = ROOT / 'notebooks_colab' / (name + '.ipynb')
    return ''.join(json.loads(path.read_text())['cells'][cell]['source'])


def text(x, y, content, cls='plot-text', anchor='start'):
    return f'<text class="{cls}" x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}">{html.escape(str(content))}</text>'


def line(x1, y1, x2, y2, cls='plot-axis'):
    return f'<path class="{cls}" d="M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}"/>'


def polyline(points, cls):
    return '<path class="' + cls + '" d="' + ' '.join(('M' if i == 0 else 'L') + f'{x:.2f} {y:.2f}' for i, (x, y) in enumerate(points)) + '"/>'


def svg(key, title, description, body):
    return (f'<svg class="assignment-diagram method-plot" viewBox="0 0 480 246" role="img" aria-labelledby="{key}-graph-title {key}-graph-desc">'
            f'<title id="{key}-graph-title">{html.escape(title)}</title><desc id="{key}-graph-desc">{html.escape(description)}</desc>{body}</svg>')


def build():
    provenance = {}
    graphs = {}
    chapters = {'rct': '01-randomized-trials', 'regression': '02-regression', 'iv': '03-instrumental-variables', 'rd': '04-regression-discontinuity', 'did': '05-differences-in-differences'}
    # Same outcome, sample, plan indicators, and family-clustered covariance as Ch. 1, cell 19.
    assert 'vcov={"CRV1": "family_id"}' in notebook(chapters['rct'], 19)
    assert 'f"{var} ~ plan_free + plan_deductible + plan_coinsurance"' in notebook(chapters['rct'], 19)
    health = pd.read_csv(ROOT / 'data/ch1/rand_health_outcomes.csv')
    d = health[['health_index', 'plan_free', 'plan_deductible', 'plan_coinsurance', 'family_id']].dropna()
    model = pf.feols('health_index ~ plan_free + plan_deductible + plan_coinsurance', data=d, vcov={'CRV1': 'family_id'})
    intervals = model.confint()
    rows = []
    x = lambda value: 170 + (value + 3) / 6 * 270
    body = text(24, 22, 'General health · effect vs. catastrophic plan', 'plot-text graph-subtitle')
    body += line(x(0), 40, x(0), 187, 'policy-marker')
    for i, (term, label) in enumerate([('plan_free', 'Free care'), ('plan_deductible', 'Deductible'), ('plan_coinsurance', 'Coinsurance')]):
        estimate = float(model.coef()[term]); low, high = map(float, intervals.loc[term])
        rows.append({'plan': label, 'estimate': estimate, 'ci95': [low, high]})
        yy = 66 + i * 53
        cls = 'line-blue' if i == 0 else 'line-purple'
        body += text(24, yy + 5, label)
        body += f'<g><title>{label}: {estimate:.2f}; 95% interval {low:.2f} to {high:.2f}</title>'
        body += line(x(low), yy, x(high), yy, 'plot-line ' + cls)
        body += line(x(low), yy - 5, x(low), yy + 5, 'plot-line ' + cls) + line(x(high), yy - 5, x(high), yy + 5, 'plot-line ' + cls)
        body += f'<circle class="{"plot-dot" if i == 0 else "dot-purple"}" cx="{x(estimate):.2f}" cy="{yy}" r="5"/></g>'
    body += line(170, 198, 440, 198)
    for value in [-3, 0, 3]:
        body += text(x(value), 219, f'{value:+d}' if value else '0', anchor='middle')
    body += text(305, 242, 'Health-index points · 95% intervals', 'plot-text graph-subtitle', 'middle')
    graphs['rct'] = svg('rct', 'RAND: general-health effects relative to the catastrophic plan', 'Recomputed using the Chapter 1 model and dataset. Points are plan effects in general-health-index units; lines are 95% confidence intervals clustered by family. All three intervals include zero.', body)
    provenance['rct'] = {'kind': 'recomputed', 'cells_zero_based': [18, 19], 'data': 'data/ch1/rand_health_outcomes.csv', 'model': 'health_index ~ plan_free + plan_deductible + plan_coinsurance', 'covariance': 'CRV1 clustered by family_id', 'n': len(d), 'results': rows}

    # Ch. 2 explicitly says the C&B microdata are unavailable. Preserve its approximation
    # and its qualitative "close to zero" statement; do not turn that into an invented 0%.
    source = notebook(chapters['regression'], 10)
    raw = re.search(r'Without controls.*?\*\*(\d+)% more\*\*', source).group(1)
    controlled = re.search(r"Barron's selectivity.*?\*\*(\d+)%\*\*", source).group(1)
    assert '**close to zero**' in source and 'not publicly available' in source
    summaries = [('No controls', '~' + raw + '%'), ('Selectivity controls', '~' + controlled + '%'), ('Application controls', 'Near zero')]
    body = text(24, 22, 'Private-college earnings premium', 'plot-text graph-subtitle')
    for i, (label, value) in enumerate(summaries):
        yy = 65 + i * 55
        body += line(24, yy + 19, 456, yy + 19, 'plot-grid') + text(24, yy, label)
        body += text(448, yy, value, ['plot-text label-blue result-value', 'plot-text label-purple result-value', 'plot-text label-green result-value'][i], 'end')
    body += text(240, 230, 'Approximate findings reported in Chapter 2', 'plot-text graph-subtitle', 'middle')
    graphs['regression'] = svg('regression', 'Private-college premium: the notebook’s literature summary', 'Chapter 2 reports about 14% without controls, about 7% with selectivity controls, and close to zero with application controls. These are approximate literature summaries, not estimates replicated from student microdata. No exact value is supplied for near zero.', body)
    provenance['regression'] = {'kind': 'notebook literature summary, not a microdata replication', 'cells_zero_based': [10], 'results': summaries, 'qualification': 'Approximate percentages; no numerical value assigned to close to zero.'}

    # Ch. 3 reports KIPP estimates but does not provide the KIPP microdata.
    source = notebook(chapters['iv'], 9)
    fs = float(re.search(r'First stage \(lottery → attendance\) \| ([\d.]+)', source).group(1))
    rf = float(re.search(r'Reduced form \(lottery → math scores\) \| \+([\d.]+)', source).group(1))
    late = float(re.search(r'\*\*LATE\*\*.*?\*\*\+([\d.]+)', source).group(1))
    assert round(rf / fs, 2) == late
    body = text(240, 25, f'Offer → attendance: +{fs * 100:.1f} percentage points', 'plot-text graph-subtitle', 'middle')
    body += '<defs><marker id="iv-arrow" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1L6 4L1 7" fill="none" stroke="#74ceff" stroke-width="1.5"/></marker></defs>'
    for xx, box, labels, color in [(8, 'treatment-group', ['Lottery', 'offer'], 'label-blue'), (173, 'comparison-group', ['KIPP', 'attendance'], 'label-purple'), (338, 'outcome-group', ['Math', 'scores'], 'label-green')]:
        body += f'<rect class="graph-group {box}" x="{xx}" y="65" width="134" height="82" rx="12"/>'
        for yy, label in zip([99, 123], labels):
            body += text(xx + 67, yy, label, 'plot-text ' + color, 'middle')
    body += '<path class="plot-line line-blue" d="M146 106H166" marker-end="url(#iv-arrow)"/><path class="plot-line line-blue" d="M311 106H331" marker-end="url(#iv-arrow)"/>'
    body += text(240, 187, f'Offer → math scores: +{rf:.3f} SD', 'plot-text', 'middle')
    body += text(240, 220, f'Attendance effect: +{late:.2f} SD for compliers', 'plot-text label-green', 'middle')
    graphs['iv'] = svg('iv', 'KIPP: the estimates reported in Chapter 3', 'The notebook reports a first stage of 0.741, a reduced-form effect on math scores of 0.355 standard deviations, and an IV attendance effect of 0.48 standard deviations for compliers. These are notebook-reported estimates, not a new replication. SD means standard deviations.', body)
    provenance['iv'] = {'kind': 'notebook-reported estimates, not a microdata replication', 'cells_zero_based': [9], 'results': {'first_stage': fs, 'reduced_form_sd': rf, 'late_sd': late}, 'qualification': 'First stage is an attendance-probability difference, not simply a winner attendance rate. No confidence intervals are reported here.'}

    # Ch. 4, cell 11: ALL plotted age cells, with separate OLS fits below and above 21.
    source = notebook(chapters['rd'], 11)
    assert 'pf.feols("all ~ age", data=below)' in source and 'pf.feols("all ~ age", data=above)' in source
    data = pd.read_csv(ROOT / 'data/ch4/mlda_clean.csv')
    d = data.dropna(subset=['agecell', 'age', 'all']).sort_values('agecell')
    x = lambda value: 60 + (value - 19) / 4 * 385
    y = lambda value: 205 - (value - 85) / 25 * 160
    body = text(60, 22, 'All-cause deaths per 100,000', 'plot-text graph-subtitle')
    for value in [90, 100, 110]:
        body += line(60, y(value), 445, y(value), 'plot-grid') + text(50, y(value) + 5, value, anchor='end')
    body += line(60, 45, 60, 205) + line(60, 205, 445, 205) + line(x(21), 35, x(21), 205, 'policy-marker')
    for age in [19, 20, 21, 22, 23]:
        body += text(x(age), 225, age, 'plot-text label-green' if age == 21 else 'plot-text', 'middle')
    body += text(252, 245, 'Age (years)', 'plot-text graph-subtitle', 'middle')
    for row in d.itertuples(index=False):
        body += f'<circle class="{"plot-dot" if row.age < 0 else "plot-dot dot-purple"}" cx="{x(row.agecell):.2f}" cy="{y(row.all):.2f}" r="3"><title>Age {row.agecell:.3f}: {row.all:.3f} deaths per 100,000</title></circle>'
    fits = {}
    for key, subset, color in [('below', d[d.age < 0], 'line-blue'), ('above', d[d.age >= 0], 'line-purple')]:
        fit = pf.feols('all ~ age', data=subset)
        predictions = fit.predict(newdata=subset)
        body += polyline([(x(age), y(value)) for age, value in zip(subset.agecell, predictions)], 'plot-line ' + color)
        fits[key] = {k: float(v) for k, v in fit.coef().items()}
    graphs['rd'] = svg('rd', 'All-cause mortality around age 21: reproduced from Chapter 4', f'All {len(d)} nonmissing age-cell observations are plotted from mlda_clean.csv, with separate linear regressions on each side as in notebook cell 11. Mortality jumps upward at 21; the fitted trend above the cutoff slopes downward. Units are deaths per 100,000.', body)
    provenance['rd'] = {'kind': 'recomputed notebook scatter and fitted lines', 'cells_zero_based': [3, 11], 'data': 'data/ch4/mlda_clean.csv', 'n_plotted': len(d), 'raw_rows': len(data), 'model': 'all ~ age separately for age < 0 and age >= 0', 'fit_coefficients': fits, 'observations': d[['agecell', 'age', 'all']].to_dict(orient='records')}

    # Ch. 5 cells 3 and 5: use all six years and the supplied counterfactual column.
    banks = pd.read_csv(ROOT / 'data/ch5/banks_clean.csv')
    assert 'banks["counterfactual"]' in notebook(chapters['did'], 5)
    baseline = banks.loc[banks.year == 1930].iloc[0]
    post = banks[banks.year > 1930]
    assert (post.counterfactual == baseline.bib6 + post.bib8 - baseline.bib8).all()
    x = lambda value: 60 + (value - 1929) / 5 * 385
    y = lambda value: 197 - (value - 60) / 120 * 151
    body = text(60, 20, 'Banks in business · July 1 counts', 'plot-text graph-subtitle')
    for value in [60, 120, 180]:
        body += line(60, y(value), 445, y(value), 'plot-grid') + text(50, y(value) + 5, value, anchor='end')
    body += line(60, 46, 60, 197) + line(60, 197, 445, 197) + line(x(1930), 46, x(1930), 197, 'policy-marker')
    body += text(x(1930), 39, 'Baseline', 'plot-text graph-subtitle', 'middle')
    for year in banks.year:
        body += text(x(year), 218, int(year), 'plot-text graph-subtitle', 'middle')
    for column, cls in [('counterfactual', 'line-green counterfactual'), ('bib6', 'line-blue'), ('bib8', 'line-purple')]:
        body += polyline([(x(year), y(value)) for year, value in zip(banks.year, banks[column])], 'plot-line ' + cls)
        if column != 'counterfactual':
            for year, value in zip(banks.year, banks[column]):
                body += f'<circle class="{"plot-dot" if column == "bib6" else "dot-purple"}" cx="{x(year):.2f}" cy="{y(value):.2f}" r="3"><title>{"6th" if column == "bib6" else "8th"} district, {int(year)}: {value} banks</title></circle>'
    body += text(62, 243, '6th (policy)', 'plot-text label-blue graph-subtitle')
    body += text(195, 243, '8th', 'plot-text label-purple graph-subtitle')
    body += line(253, 237, 281, 237, 'plot-line line-green counterfactual') + text(288, 243, '6th counterfactual', 'plot-text label-green graph-subtitle')
    graphs['did'] = svg('did', 'Bank counts and the counterfactual reproduced from Chapter 5', 'Annual July 1 bank counts, 1929–1934, for the 6th and 8th Federal Reserve districts. Both districts lose banks. The dashed 6th-district counterfactual is copied from banks_clean.csv, using 1930 as the baseline for subsequent comparison-group changes. In 1934, the 6th district has 102 banks versus a counterfactual of 79.', body)
    provenance['did'] = {'kind': 'exact notebook series', 'cells_zero_based': [3, 5, 19], 'data': 'data/ch5/banks_clean.csv', 'baseline_year': 1930, 'series': banks.to_dict(orient='records')}

    copy = {
        'rct': ('No clear general-health improvement.', 'In RAND, the free-care, deductible, and coinsurance effects on general health all have 95% intervals spanning zero. These comparisons are against catastrophic coverage, not no insurance.', 'Recomputed RAND results · family-clustered intervals'),
        'regression': ('The premium shrinks with controls.', 'Chapter 2 summarizes the private-college premium as about 14%, then 7%, then close to zero as controls improve. The study data are unavailable here; this is the notebook’s literature summary.', 'Notebook literature summary · approximate findings'),
        'iv': ('A positive effect for lottery compliers.', 'Chapter 3 reports a +0.48 standard-deviation math effect of KIPP attendance for lottery compliers. The causal reading requires the lottery to affect scores only through attendance.', 'Notebook-reported KIPP estimates · SD = standard deviations'),
        'rd': ('An upward jump at age 21.', 'These age-cell mortality rates and separate linear fits reproduce Chapter 4. Mortality rises at the cutoff; a causal reading requires other determinants to change smoothly there.', 'Observed age cells and fitted lines · Chapter 4'),
        'did': ('Fewer losses, not a recovery.', 'Bank counts fall in both districts. In 1934, the 6th has 102 banks versus a counterfactual of 79. The 23-bank difference relies on the parallel-trends assumption.', 'Notebook bank series · dashed line is counterfactual'),
    }
    document = (ROOT / 'index.html').read_text()
    for key, graph in graphs.items():
        pattern = rf'(<figure class="method-scene[^"\n]*" id="scene-{key}".*?</figure>)'
        match = re.search(pattern, document, re.S)
        if not match:
            raise ValueError(f'Missing scene: {key}')
        scene = match.group(1)
        scene = re.sub(r'(<div class="scene-graph">).*?(</div>)', lambda m: m[1] + graph + m[2], scene, flags=re.S)
        takeaway, explanation, note = copy[key]
        for cls, value in [('scene-takeaway', takeaway), ('scene-explanation', explanation)]:
            scene = re.sub(rf'(<p class="{cls}">).*?(</p>)', lambda m: m[1] + html.escape(value) + m[2], scene, flags=re.S)
        note_markup = f'{html.escape(note)}.<br><a href="{COLAB}{chapters[key]}.ipynb" target="_blank" rel="noopener">Colab source ↗</a> · Artwork is illustrative.'
        scene = re.sub(r'(<p class="scene-note">).*?(</p>)', lambda m: m[1] + note_markup + m[2], scene, flags=re.S)
        document = document[:match.start()] + scene + document[match.end():]
        provenance[key]['notebook'] = 'notebooks_colab/' + chapters[key] + '.ipynb'
        files = [provenance[key]['notebook']]
        if 'data' in provenance[key]:
            files.append(provenance[key]['data'])
        provenance[key]['input_sha256'] = {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in files}
    return document, json.dumps(provenance, indent=2, ensure_ascii=False) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    document, provenance = build()
    outputs = {ROOT / 'index.html': document, ROOT / 'assets/homepage/graph-sources.json': provenance}
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit(f'Out of date: {path.relative_to(ROOT)}')
        else:
            path.write_text(content)
    print('Verified notebook-derived graphs and provenance.' if args.check else 'Built five notebook-grounded graphics and provenance.')
