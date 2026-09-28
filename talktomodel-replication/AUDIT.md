# AUDIT.md

## 1. What is Reused (From Authors)
- **TalkToModel Logic:** The core natural language parsing, dialogue state management (`ExplainBot`), and XAI orchestration (`MegaExplainer`, `TabularDice`) are reused directly from the authors' repository (`dylan-slack/TalkToModel`).
- **Pretrained T5 Parsers:** `ucinlp/diabetes-t5-small` and `ucinlp/diabetes-t5-base` are the authors' fine-tuned Hugging Face models used to parse text to logic.
- **Datasets:** `data/diabetes.csv` and `data/ttm-user-study-responses.csv` are the exact tabular datasets and user study responses provided by the authors.

## 2. What I Implemented (My Own Code)
- **Environment Restoration:** I isolated and restored the legacy dependency graph (`numpy==1.21.6`, `pandas==1.3.5`, `Flask==2.0.3`, `Werkzeug==2.0.3`) required to successfully execute the authors' pickled models without binary incompatibility errors.
- **Evaluation Scripts:** `experiments/04_evaluate_t5_diabetes.py` to test the T5 parsing accuracy.
- **End-to-End Demo:** `experiments/07_end_to_end_talktomodel_diabetes.py` which provides an interactive CLI loop wrapping the authors' pipeline.
- **Visualization Scripts:** `experiments/09_generate_visualizations.py` and `experiments/11_comprehensive_visualizations.py` using `matplotlib`/`seaborn` to render result charts.
- **My LIME Module:** `xai/lime_explanation.py` implementation.

## 3. What is Broken or Inconsistent
- **Hardcoded Results:** `10_compare_accuracy.py`, `09_generate_visualizations.py`, and `11_comprehensive_visualizations.py` contain hardcoded values (e.g. 68.06, 72.77) instead of reading from actual generated output JSON files.
- **Missing T5-Base Eval:** There is no script that actually evaluated T5-Base to produce the 72.77% number; `04_evaluate_t5_diabetes.py` only evaluates T5-Small.
- **Inconsistent Dataset Labelling:** Earlier versions of charts and tables mistakenly referenced the `COMPAS` dataset when the code actually evaluated `DIABETES`.
- **Hardcoded Paths:** Multiple scripts use absolute paths (e.g. `/home/shivwhoo/...` or `../TalkToModel/...`) instead of dynamic/relative submodules.
- **Missing Test Split Logic:** The evaluation script currently tests the entire `diabetes_pandas.csv` file rather than a proper held-out test split, meaning the accuracy reported isn't a true representation of the authors' held-out test set accuracy.
- **Script Numbering Gaps:** The `experiments/` directory skips numbers (01, 02, 03, 04, 07, 09, 10, 11).
- **Missing Reproducibility Orchestrator:** No `Makefile` or `run_all.sh` exists to run the full pipeline end-to-end.
