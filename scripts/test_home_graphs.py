"""Independently check homepage estimates against the Colab datasets.

Run: uv run python scripts/test_home_graphs.py
The builder uses pyfixest; these checks use statsmodels for an independent fit.
"""
import json
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]


class HomeGraphResults(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = json.loads((ROOT / 'assets/homepage/graph-sources.json').read_text())

    def test_rand_point_estimates_and_family_clustered_intervals(self):
        d = pd.read_csv(ROOT / 'data/ch1/rand_health_outcomes.csv')
        d = d[['health_index', 'plan_free', 'plan_deductible', 'plan_coinsurance', 'family_id']].dropna()
        fit = smf.ols('health_index ~ plan_free + plan_deductible + plan_coinsurance', d).fit(
            cov_type='cluster', cov_kwds={'groups': d.family_id}, use_t=True)
        self.assertEqual(self.sources['rct']['n'], len(d))
        for row, term in zip(self.sources['rct']['results'], ['plan_free', 'plan_deductible', 'plan_coinsurance']):
            self.assertAlmostEqual(row['estimate'], fit.params[term])
            np.testing.assert_allclose(row['ci95'], fit.conf_int().loc[term])

    def test_rd_uses_every_nonmissing_age_cell_and_actual_fitted_trends(self):
        d = pd.read_csv(ROOT / 'data/ch4/mlda_clean.csv')
        observed = d.dropna(subset=['agecell', 'age', 'all']).sort_values('agecell')
        self.assertEqual(self.sources['rd']['observations'], observed[['agecell', 'age', 'all']].to_dict(orient='records'))
        for key, subset in [('below', d[d.age < 0]), ('above', d[d.age >= 0])]:
            fit = smf.ols('all ~ age', subset).fit()
            for term in ['Intercept', 'age']:
                self.assertAlmostEqual(self.sources['rd']['fit_coefficients'][key][term], fit.params[term])

    def test_bank_series_match_csv_including_counterfactual(self):
        d = pd.read_csv(ROOT / 'data/ch5/banks_clean.csv')
        self.assertEqual(self.sources['did']['series'], d.to_dict(orient='records'))
        baseline = d.loc[d.year == 1930].iloc[0]
        post = d[d.year > 1930]
        np.testing.assert_array_equal(post.counterfactual, baseline.bib6 + post.bib8 - baseline.bib8)

    def test_reported_summaries_do_not_invent_a_precise_zero_or_missing_intervals(self):
        self.assertEqual(self.sources['regression']['results'], [
            ['No controls', '~14%'], ['Selectivity controls', '~7%'], ['Application controls', 'Near zero']])
        iv = self.sources['iv']['results']
        self.assertEqual(iv, {'first_stage': .741, 'reduced_form_sd': .355, 'late_sd': .48})
        self.assertEqual(round(iv['reduced_form_sd'] / iv['first_stage'], 2), iv['late_sd'])


if __name__ == '__main__':
    unittest.main()
