# Mastering Causal Metrics

**An AI-Powered Study Guide** for *Mastering 'Metrics: The Path from Cause to Effect* by Joshua D. Angrist and Jorn-Steffen Pischke (Princeton University Press, 2015).

This project provides an interactive Quarto book with Python notebooks that walk students through the core methods of causal inference using real data. Each chapter pairs conceptual explanations with hands-on replication of the book's key empirical tables and figures, enhanced with AI-powered learning tools.

**[Read Online](https://cmg777.github.io/intro2causal/book/_book/)** | **[AI Tutors](https://cmg777.github.io/intro2causal/tutors.html)** | **[GitHub](https://github.com/cmg777/intro2causal)**

## Study Guides

| Chapter | Method | Case Studies |
|:--------|:-------|:-------------|
| [Ch 1: Randomized Trials](notebooks_quarto/01-randomized-trials.qmd) | RCTs, potential outcomes, selection bias | NHIS, RAND HIE, Oregon Health Plan |
| [Ch 3: Instrumental Variables](notebooks_quarto/03-instrumental-variables.qmd) | IV/2SLS, LATE, complier types | MDVE, KIPP lotteries, family size |
| [Ch 4: Regression Discontinuity](notebooks_quarto/04-regression-discontinuity.qmd) | Sharp and fuzzy RD | MLDA and mortality, Boston exam schools |
| [Ch 5: Differences-in-Differences](notebooks_quarto/05-differences-in-differences.qmd) | DD with fixed effects, parallel trends | Great Depression banking, MLDA deaths |
| [Ch 6: The Wages of Schooling](notebooks_quarto/06-wages-of-schooling.qmd) | OLS, twin FE, IV, RD (synthesis) | Twins, quarter of birth, sheepskin effects |

Each guide includes:

- Learning objectives and a visual roadmap
- Conceptual explanations with mermaid diagrams
- Python code replicating the book's key results
- Interpretation callouts connecting numbers to intuition
- Historical perspective on the method's origins
- Practice exercises

## Project Structure

```
intro2causal/
├── book/                      # Quarto book project
│   ├── _quarto.yml            # Book configuration (parts, chapters, theme)
│   ├── custom.css             # Branded CSS (dark/light mode)
│   ├── index.qmd              # Preface / landing page
│   ├── notebooks_quarto/      # Study guides (book versions)
│   │   ├── 01-randomized-trials.qmd
│   │   ├── 02-regression.qmd       # (under development)
│   │   ├── 03-instrumental-variables.qmd
│   │   ├── 04-regression-discontinuity.qmd
│   │   ├── 05-differences-in-differences.qmd
│   │   └── 06-wages-of-schooling.qmd
│   └── images/                # Visual summaries, cover, badges (SVG)
├── notebooks_quarto/          # Study guides (standalone versions)
├── data/                      # Clean CSV datasets (ready to use)
│   ├── ch1/                   # NHIS, RAND HIE
│   ├── ch3/                   # MDVE
│   ├── ch4/                   # MLDA mortality
│   ├── ch5/                   # Bank failures, MLDA deaths
│   └── ch6/                   # Twins, QOB, sheepskin
├── code/
│   ├── python/                # Python scripts by chapter
│   └── stata/                 # Original Stata do files
├── original-book/             # Chapter text (markdown reference)
├── tutors/                    # AI tutor system prompts
├── index.html                 # Project website (GitHub Pages)
├── tutors.html                # AI tutors page
├── favicon.svg                # Site favicon
├── pyproject.toml             # Python dependencies
└── uv.lock                   # Dependency lock file
```

## Getting Started

### Prerequisites

- [Python 3.12+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Quarto](https://quarto.org/) (for rendering the study guides)

### Installation

```bash
# Clone the repository
git clone https://github.com/cmg777/intro2causal.git
cd intro2causal

# Create virtual environment and install dependencies
uv sync
```

### Download the Raw Data

The raw Stata data files (`.dta`) are not included in the repository due to their size. You can either:

**Option A: Use the pre-processed clean CSVs** (already included in `data/`). The study guides load these directly --- no extra download needed.

**Option B: Download raw data and rebuild** from [masteringmetrics.com/resources](https://www.masteringmetrics.com/resources/):

1. Download "All Data Files" from the resources page
2. Extract the `.dta` files into `data/ch1/`, `data/ch3/`, etc.
3. Run the preparation scripts:

```bash
uv run python code/python/ch1/prepare_data.py
uv run python code/python/ch3/prepare_data.py
uv run python code/python/ch4/prepare_data.py
uv run python code/python/ch5/prepare_data.py
uv run python code/python/ch6/prepare_data.py
```

> **Note:** The twins data for Chapter 6 (`pubtwins.dta`) must be downloaded separately from [Princeton DataSpace](https://dataspace.princeton.edu/handle/88435/dsp01rv042t084).

### Render the Book

```bash
# Render the full book (recommended)
uv run quarto render book/

# Render a single standalone chapter
uv run quarto render notebooks_quarto/01-randomized-trials.qmd
```

The book output appears in `book/_book/`. Open `book/_book/index.html` to view it locally.

## Python Libraries

| Library | Purpose |
|:--------|:--------|
| `pandas` | Data loading and manipulation |
| `numpy` | Numerical operations |
| `statsmodels` | OLS, WLS, robust and clustered standard errors |
| `linearmodels` | IV/2SLS estimation (`IV2SLS`) |
| `matplotlib` | Scatter plots and RD visualizations |
| `seaborn` | Plot styling |

The library choices follow [Causal Inference for The Brave and True](https://matheusfacure.github.io/python-causality-handbook/) by Matheus Facure.

## Data Sources

All datasets are from publicly available sources distributed with the book:

- **NHIS 2009**: National Health Interview Survey ([IHIS](https://www.ihis.us/ihis/))
- **RAND HIE**: RAND Health Insurance Experiment ([ICPSR](https://doi.org/10.3886/ICPSR06439.v1))
- **MDVE**: Minneapolis Domestic Violence Experiment (Sherman & Berk, 1984)
- **MLDA Mortality**: Carpenter & Dobkin (2009), *American Economic Journal: Applied Economics*
- **Bank Failures**: Richardson & Troost (2009), *Journal of Political Economy*
- **MLDA Death Rates**: State-level panel from Du Mouchel, Williams & Zador (1987)
- **Twinsburg Twins**: Ashenfelter & Krueger (1994); Ashenfelter & Rouse (1998)
- **Quarter of Birth**: Angrist & Krueger (1991), *Quarterly Journal of Economics*
- **Texas Sheepskin**: Clark & Martorell (2014), *Journal of Political Economy*

## Acknowledgments

- **Joshua D. Angrist and Jorn-Steffen Pischke** for writing *Mastering 'Metrics* and making the replication data publicly available
- **Princeton University Press** for publishing the book and hosting the data at [masteringmetrics.com](https://www.masteringmetrics.com/)
- **Matheus Facure** for [Causal Inference for The Brave and True](https://matheusfacure.github.io/python-causality-handbook/), which informed the Python library choices

## License

The study guide text and Python code in this repository are original work. The datasets are distributed under the terms set by their respective authors and publishers. See the individual `ReadMe` files in `code/stata/` for dataset-specific terms.
