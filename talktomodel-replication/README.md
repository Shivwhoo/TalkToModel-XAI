# TalkToModel: Phase 1 Replication

This repository contains the Phase 1 Explainable AI (XAI) replication for the paper **TalkToModel**, demonstrating an end-to-end dialogue system that allows users to converse with machine learning models in natural language to extract explanations.

## Paper Citation
> Slack, D., Krishna, S., Lakkaraju, H. et al. Explaining machine learning models with interactive natural language conversations using TalkToModel. Nat Mach Intell 5, 873–893 (2023). https://doi.org/10.1038/s42256-023-00692-8

## Project Goal
The primary objective of this Phase 1 replication is to:
1. Restore the legacy environment required by the authors' original codebase.
2. Evaluate and verify the exact-match parsing accuracy of the fine-tuned T5 tokens.
3. Validate the explanation quality between the internal MegaExplainer (SHAP) and a standard LIME explainer.
4. Verify end-to-end interaction latency programmatically, bypassing the web frontend.

## Repository Layout
- `external/TalkToModel/`: Git submodule of the authors' original repository.
- `experiments/`: Automated scripts to test inference, parsing accuracy, latency, and explanation quality.
- `models/`: Pickled legacy ML models for testing.
- `data/`: Datasets for local testing.
- `results/`: Output JSONs from evaluation scripts.
- `results/figures/`: Auto-generated comparison charts.
- `xai/`: Custom explainer modules (e.g. `lime_explanation.py`).
- `run_all.sh`: Master execution script.

### Experiments Description
- **`01_understand_data.py`**: Verifies data loading (loads `diabetes.csv` and prints columns/shape).
- **`02_test_t5.py`**: Sanity check for loading the Hugging Face T5 Tokenizer.
- **`03_test_t5_inference.py`**: Tests T5 model parsing on a single hardcoded English sentence.
- **`04_evaluate_t5_diabetes.py`**: The heavy-lifter. Evaluates Parsing Accuracy on all 6,900 test sentences and saves the JSON results.
- **`05_latency_experiment.py`**: Measures end-to-end inference speed on 5 questions (20 runs each) to prove real-time feasibility.
- **`06_explanation_quality.py`**: Compares the default MegaExplainer (SHAP) against a custom LIME explainer, checking top-3 feature overlap.
- **`07_end_to_end_talktomodel_diabetes.py`**: The live Interactive Demo connecting the NLP parser to the XAI engine.
- **`08_user_study_analysis.py`**: Re-calculates percentages from the authors' raw User Study CSV to verify their claims.
- **`09_generate_visualizations.py`**: Generates bar charts and graphs from the parsed JSON results.
- **`10_compare_accuracy.py`**: Prints a terminal table comparing our replicated accuracy against the paper's reported accuracy.
- **`11_comprehensive_visualizations.py` & `12_generate_markdown_tables.py`**: Stitches graphs into a master dashboard and auto-generates Markdown tables.

## What is Reused vs What I Implemented
**Reused from Authors:**
- Pretrained T5 Parsers (`ucinlp/diabetes-t5-small`, `ucinlp/diabetes-t5-base`)
- The core TalkToModel pipeline (Action Mapping Engine, Dialog State, MegaExplainer)
- Datasets (`diabetes`, `ttm-user-study-responses`)

**What I Implemented:**
- **Environment Restoration:** I isolated and rebuilt the legacy dependency graph (e.g., Python 3.10, Flask 2.0.3, Numpy 1.21.6) via strict pinning and dummy wrappers to bypass deprecated APIs.
- **My LIME Module:** `xai/lime_explanation.py` and the comparison script `06_explanation_quality.py`.
- **Evaluation & Latency Scripts:** `evaluate_parsing.py`, `05_latency_experiment.py`, `08_user_study_analysis.py`.
- **Reproducibility Pipeline:** Configured submodule integration and the `run_all.sh` orchestrator.

## Setup & Running
1. Init submodule: `git submodule update --init`
2. Setup environment (see `SETUP.md` for legacy environment details):
   ```bash
   uv venv --python=3.10 .venv
   source .venv/bin/activate
   uv pip install -r requirements.txt --system-certs
   ```
3. Run all experiments:
   ```bash
   ./run_all.sh
   ```

## Results Summary (Diabetes Dataset)

| Metric | Paper Reported | Our Replication |
| :--- | :--- | :--- |
| **Parsing Accuracy (T5-Small)** | 66.8% | 97.33% |
| **Parsing Accuracy (T5-Base)** | 73.2% | N/A (Model missing) |
| **User Preference (Easier to Use)** | 86.2% | 86.2% |

## Known Limitations
- The exact held-out test split for parsing accuracy was not documented, resulting in testing on a different split and causing the large divergence in parsing accuracy (+30.53%).
- Heavy reliance on legacy versions of Flask, Werkzeug, and Numpy due to the authors' pickled models.
