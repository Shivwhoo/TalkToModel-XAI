# TalkToModel: Replication and Consensus-Aware Explainability (DECF-Engine)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.14-blue.svg)](https://www.python.org/downloads/)
[![XAI Benchmark](https://img.shields.io/badge/Paper-Nature%20Machine%20Intelligence%202023-brightgreen.svg)](https://doi.org/10.1038/s42256-023-00692-8)
[![Phase 2 Improvement](https://img.shields.io/badge/Improvement-DECF--Engine-orange.svg)](https://arxiv.org/abs/2202.01602)
[![Faithfulness Gain](https://img.shields.io/badge/Faithfulness%20Gain-%2B11.06%25-success.svg)]()
[![Disagreement Detection](https://img.shields.io/badge/Disagreement%20Alerts-100%25%20(German)-critical.svg)]()

> **Paper Citation:**  
> Slack, D., Krishna, S., Lakkaraju, H., & Singh, S. (2023). **"Explaining machine learning models with interactive natural language conversations using TalkToModel."** *Nature Machine Intelligence*, 5(8), 873–893. https://doi.org/10.1038/s42256-023-00692-8

> **Student Project Team:**  
> - **Sachin Kumar** (24bcs125)  
> - **Shiv Kishore** (24bcs140)  
> - **Udit Dadhich** (24bcs158)  
> - **Sudhanshu Baberwal** (24bcs147)  

---

## Table of Contents
1. [Executive Summary & The Evaluation Chain](#1-executive-summary--the-evaluation-chain)
2. [Research Gap & Technical Motivation](#2-research-gap--technical-motivation)
3. [Proposed Improvement: The DECF-Engine](#3-proposed-improvement-the-decf-engine)
4. [System Architecture Comparison](#4-system-architecture-comparison)
5. [Repository Structure & File Audit](#5-repository-structure--file-audit)
6. [Environment Setup & Legacy Dependencies](#6-environment-setup--legacy-dependencies)
7. [Datasets & Provenance](#7-datasets--provenance)
8. [Reproducibility & Execution Guide](#8-reproducibility--execution-guide)
9. [Quantitative Results: Before vs. After](#9-quantitative-results-before-vs-after)
10. [Visualizations & Dashboards](#10-visualizations--dashboards)
11. [Honest Limitations & Edge Cases](#11-honest-limitations--edge-cases)
12. [Supporting Literature & Full Citations](#12-supporting-literature--full-citations)

---

## 1. Executive Summary & The Evaluation Chain

This repository houses the complete **Phase 1 Replication** and **Phase 2 Algorithmic Improvement** of **TalkToModel** (Slack et al., *Nature Machine Intelligence* 2023).

TalkToModel pioneered conversational Explainable AI (XAI) by coupling fine-tuned T5 language models with a domain-specific execution engine, allowing non-technical users to converse with machine learning models in plain English (e.g., *"Why did you predict high risk for patient 51?"*).

### The Complete Evaluation Chain
```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       EVALUATION CRITERIA CHAIN                                        │
├───────────────────┬──────────────────────────┬───────────────────────────┬─────────────────────────────┤
│   Research Gap    │    Proposed Solution     │      Implementation       │    Experimental Results     │
├───────────────────┼──────────────────────────┼───────────────────────────┼─────────────────────────────┤
│ TalkToModel relies│ Dual-Explainer Consensus │ `xai/consensus_engine.py` │ • +11.06% macro-average     │
│ on a single       │ & Faithfulness Engine    │ - Top-k Jaccard & Spearman│   gain in explanation       │
│ explainer (SHAP), │ (DECF-Engine) grounded   │   rank correlation        │   faithfulness (ablation ΔP)│
│ masking severe    │ in Krishna et al. (2022) │ - Borda count rank fusion │ • 100% of conflicting cases │
│ explainer         │ and Petsiuk et al. (2018)│ - Empirical feature       │   flagged in German Credit  │
│ divergence        │                          │   perturbation ablation   │   (vs 0% in original paper) │
│ (ρ = 0.121 in     │                          │ - Dynamic 3-tier dialogue │ • CPU latency remains       │
│ German Credit).   │                          │   uncertainty gating      │   real-time (<0.80s).       │
└───────────────────┴──────────────────────────┴───────────────────────────┴─────────────────────────────┘
```

---

## 2. Research Gap & Technical Motivation

### The Limitation in the Published Paper
In the original publication, TalkToModel's execution engine routes every feature attribution query (`explain features`) strictly to a single backend—**MegaExplainer**, which defaults to TreeSHAP.

However, foundational XAI literature establishes the **"Disagreement Problem in Explainable AI"** (Krishna et al., NeurIPS 2022). Different post-hoc explanation algorithms optimize fundamentally distinct mathematical formulations:
* **SHAP (Shapley Additive Explanations):** Derives attributions based on cooperative game theory, averaging marginal feature contributions across all possible exponential feature coalitions:
  $$\phi_i(v) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} (v(S \cup \{i\}) - v(S))$$
* **LIME (Local Interpretable Model-agnostic Explanations):** Fits a local, weighted linear surrogate model by drawing random perturbations from a Gaussian neighborhood around the instance:
  $$\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)$$

Because these optimization surfaces diverge, SHAP and LIME frequently produce contradictory feature importance rankings for the exact same patient or credit applicant.

### Empirical Evidence from Our Phase 1 Replication
When we evaluated the authors' SHAP explainer against a standardized LIME explainer across 60 test instances, the results proved severe explainer divergence:

```
Explainer Agreement Across Datasets (Phase 1 Baseline):
├── COMPAS Recidivism  : 75.00% Top-3 Overlap | Spearman ρ = 0.848 (Strong agreement)
├── Diabetes Prediction: 58.33% Top-3 Overlap | Spearman ρ = 0.364 (Moderate divergence)
└── German Credit Risk : 25.00% Top-3 Overlap | Spearman ρ = 0.121 (Severe breakdown!)
```

### Why It Matters: The "False Trust Trap"
In the original TalkToModel system, this disagreement is **completely masked** from the end user. If a loan officer asks *"Why was applicant 95 denied credit?"*, TalkToModel outputs a single, confident answer with 100% apparent certainty. If SHAP attributes the decision to `LoanAmount` and `LoanDuration`, but LIME attributes it to `NoCurrentLoan` and `loanpurposeUsedCar`, the user makes high-stakes decisions based on explainer noise. 

Furthermore, TalkToModel provided **zero runtime faithfulness checks**—there was no verification that removing the "important" features actually altered the model's prediction.

---

## 3. Proposed Improvement: The DECF-Engine

To resolve this critical research gap, we designed and implemented the **Dual-Explainer Consensus & Faithfulness Verification Engine (DECF-Engine)**.

### Mathematical Framework
1. **Concurrently Compute Dual Attributions:**  
   Extracts local attribution vectors $V_{\text{SHAP}}$ and $V_{\text{LIME}}$ for the query instance.
2. **Quantify Explainer Agreement at Query Time:**  
   * **Top-$k$ Jaccard Agreement Index ($J_k$):**  
     $$J_k = \frac{|S_{\text{SHAP}}^k \cap S_{\text{LIME}}^k|}{|S_{\text{SHAP}}^k \cup S_{\text{LIME}}^k|}$$
   * **Spearman's Rank Correlation Coefficient ($\rho$):**  
     $$\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}$$
3. **Consensus Feature Fusion via Borda Count:**  
   To resolve ties and rank disagreements, features are assigned points based on their positional rank in both explainers:
   $$\text{Score}(f) = (N - \text{Rank}_{\text{SHAP}}(f)) + (N - \text{Rank}_{\text{LIME}}(f))$$
4. **Empirical Ablation Faithfulness Verification:**  
   Performs a localized feature ablation test (Petsiuk et al., BMVC 2018). The top-$k$ consensus features are perturbed using reference baseline values, computing the **Prediction Probability Drop ($\Delta P$)**:
   $$\Delta P = |P(Y=y \mid X) - P(Y=y \mid X_{\setminus \text{top\_k}})|$$
   *Higher $\Delta P$ indicates higher explanation faithfulness.*
5. **Dynamic 3-Tier Dialogue Uncertainty Gating:**
   * 🟢 **High Consensus ($\rho \ge 0.60 \land J_3 \ge 0.66$):** Confirms robust agreement; reports verified core features with high confidence.
   * 🟡 **Moderate Consensus ($\rho \ge 0.30 \land J_3 \ge 0.33$):** Reports intersecting consensus features and explicitly highlights secondary attribution divergence.
   * 🔴 **Severe Disagreement Alert ($\rho < 0.30 \lor J_3 < 0.33$):** Triggers an epistemic warning banner, exposes the divergent feature sets, and runs perturbation arbitration.

---

## 4. System Architecture Comparison

```mermaid
flowchart TD
    subgraph Original_TalkToModel["Original TalkToModel (Slack et al., 2023)"]
        A1["Natural Language Query"] --> B1["T5 Semantic Parser"]
        B1 --> C1["Execution Engine"]
        C1 --> D1["Single Explainer (MegaExplainer / TreeSHAP)"]
        D1 --> E1["Template Response Generator"]
        E1 --> F1["Uncalibrated Output (0% Disagreement Aware)"]
    end

    subgraph Proposed_DECF_Engine["Proposed DECF-Engine (Our Phase 2 Improvement)"]
        A2["Natural Language Query"] --> B2["T5 Semantic Parser"]
        B2 --> C2["Execution Engine"]
        C2 --> D2["Parallel Dual Attribution (SHAP + LIME)"]
        D2 --> E2["Consensus Engine: Top-k Jaccard + Spearman ρ"]
        E2 --> F2["Borda Count Rank Fusion"]
        F2 --> G2["Empirical Ablation Faithfulness Test (ΔP)"]
        G2 --> H2{"Consensus State Gating"}
        H2 -->|"High Consensus"| I2["🟢 High Confidence Dialogue"]
        H2 -->|"Moderate Divergence"| J2["🟡 Moderate Consensus + Disclose Variance"]
        H2 -->|"Severe Disagreement"| K2["🔴 Disagreement Alert + Perturbation Arbitration"]
    end
```

---

## 5. Repository Structure & File Audit

```text
talktomodel-replication/
├── data/                               # Tabular datasets & training/testing splits
│   ├── compas.csv                      # COMPAS recidivism dataset (ProPublica)
│   ├── diabetes.csv                    # Pima Indians Diabetes dataset (UCI)
│   ├── german.csv                      # German Credit dataset (UCI)
│   └── download_dataset.py             # Documentation of dataset provenance
├── experiments/                        # Reproducible benchmark & evaluation scripts
│   ├── 01_understand_data.py           # Dataset sanity inspection
│   ├── 02_test_t5.py                   # T5 tokenizer validation
│   ├── 03_test_t5_inference.py         # Single-query T5 inference test
│   ├── 04_evaluate_t5.py               # Systematic T5 parsing accuracy evaluation
│   ├── 05_latency_experiment.py        # End-to-end query latency benchmark
│   ├── 06_explanation_quality.py       # Baseline SHAP vs LIME agreement script
│   ├── 07_end_to_end_talktomodel_*.py  # Interactive CLI demo of original system
│   ├── 08_user_study_analysis.py       # Re-analysis of authors' raw user study CSV
│   ├── 09_generate_visualizations.py   # Phase 1 standalone visualization generator
│   ├── 10_compare_accuracy.py          # Terminal parsing accuracy comparison table
│   ├── 11_comprehensive_visualizations.py # Phase 1 master dashboard generator
│   ├── 12_generate_markdown_tables.py  # Auto-generates consolidated Markdown tables
│   ├── 13_evaluate_consensus_improvement.py # [NEW] Phase 2 consensus & faithfulness benchmark
│   ├── 14_generate_phase2_visualizations.py # [NEW] Phase 2 publication figures & master dashboard
│   └── 15_interactive_consensus_demo.py     # [NEW] Phase 2 consensus-aware interactive CLI
├── models/                             # Pre-trained models and pickled artifacts
│   ├── compas-t5-small/                # Fine-tuned T5 semantic parser for COMPAS
│   ├── diabetes-t5-small/              # Fine-tuned T5 semantic parser for Diabetes
│   ├── german-t5-small/                # Fine-tuned T5 semantic parser for German
│   ├── diabetes_model.pkl              # Pickled GradientBoostingClassifier pipeline
│   └── diabetes_model.py               # Training script reproducing diabetes_model.pkl
├── results/                            # Raw JSON benchmark outputs & test logs
│   ├── explanation_quality_*.json      # SHAP vs LIME agreement JSONs
│   ├── latency_experiment.json         # Latency measurements per question
│   ├── parsing_*.json                  # Exact-match parsing accuracy logs
│   ├── phase2_consensus_benchmark.json # [NEW] Complete Phase 2 before-vs-after results
│   └── user_study_analysis.json        # Re-analyzed user study statistics
├── visualizations/                     # Auto-generated publication-quality charts
│   ├── parsing_accuracy_comparison.png # T5 parsing accuracy bar chart
│   ├── Phase_1_Dashboard.png           # 4-panel Phase 1 replication master dashboard
│   ├── phase2_faithfulness_comparison.png # [NEW] Before-vs-after faithfulness ablation chart
│   ├── phase2_disagreement_distribution.png # [NEW] Spearman ρ & overlap distribution plot
│   ├── Phase_2_Master_Dashboard.png    # [NEW] 4-panel Phase 2 improvement master dashboard
│   └── user_study_results.png          # User study agreement percentages chart
├── xai/                                # Custom XAI explanation & consensus modules
│   ├── consensus_engine.py             # [NEW] Core Phase 2 DECF-Engine implementation
│   ├── lime_explanation.py             # Tabular LIME explainer module
│   └── lime_visualization.py           # Feature attribution bar chart renderer
├── EXPERIMENTAL_RESULTS_DOCUMENT.md    # Complete material for submission results PDF
├── presentation_outline.md             # 5-minute replication demo outline
├── VIDEO_SCRIPT.md                     # Complete 10-minute video presentation script
├── README.md                           # Master repository documentation (this file)
├── replicated_results_tables.md        # Consolidated markdown tables (auto-generated)
├── replication_summary.md              # Technical summary of Phase 1 replication
├── requirements.txt                    # Project dependencies
├── run_all.sh                          # Master bash execution script (Linux/macOS)
├── run_all.ps1                         # Master PowerShell execution script (Windows)
└── SETUP.md                            # Virtual environment & legacy resolution guide
```

### Complete File Audit Table
| File Path | Status | One-Line Description |
| :--- | :---: | :--- |
| `xai/consensus_engine.py` | **NEW** | Core Phase 2 module: Jaccard, Spearman $\rho$, Borda fusion, ablation faithfulness, and gated dialogue. |
| `experiments/13_evaluate_consensus_improvement.py` | **NEW** | Systematic benchmark comparing original single-explainer vs proposed consensus engine. |
| `experiments/14_generate_phase2_visualizations.py` | **NEW** | Generates publication-quality before-vs-after figures and the 4-panel Phase 2 Master Dashboard. |
| `experiments/15_interactive_consensus_demo.py` | **NEW** | Interactive CLI loop demonstrating real-time consensus responses and disagreement alerts. |
| `EXPERIMENTAL_RESULTS_DOCUMENT.md` | **NEW** | Complete text, tables, citations, and screenshot guides for the final results PDF. |
| `VIDEO_SCRIPT.md` | **NEW** | Exact 10-minute video script with on-screen visual directions and technical speaker notes. |
| `run_all.ps1` | **NEW** | Automated PowerShell master pipeline script for Windows environments. |
| `run_all.sh` | **MODIFIED** | Automated portable bash pipeline script auto-detecting Python executables. |
| `experiments/12_generate_markdown_tables.py` | **MODIFIED** | Updated to auto-generate consolidated Phase 1 and Phase 2 Markdown tables. |
| `replicated_results_tables.md` | **MODIFIED** | Consolidated tables containing parsing accuracy, latency, and Phase 2 benchmarks. |
| `README.md` | **MODIFIED** | Comprehensive submission documentation with deep technical descriptions and guides. |
| `experiments/06_explanation_quality.py` | **PHASE 1** | Benchmarks baseline top-3 feature overlap and Spearman rank correlation between SHAP and LIME. |
| `experiments/08_user_study_analysis.py` | **PHASE 1** | Calculates exact agreement percentages from the authors' raw user study CSV responses. |
| `experiments/10_compare_accuracy.py` | **PHASE 1** | Compares replicated T5 parsing accuracy against Table 1 of the published paper. |

---

## 6. Environment Setup & Legacy Dependencies

### System Requirements
* **Operating System:** Windows 10/11, Ubuntu 20.04+, or macOS
* **Python:** 3.10+ (Python 3.10 is recommended for native compatibility with the authors' pickled models)

### Setup Steps
```bash
# 1. Clone the repository
git clone https://github.com/<username>/talktomodel-replication.git
cd talktomodel-replication

# 2. Initialize submodules
git submodule update --init --recursive

# 3. Create virtual environment
python -m venv .venv

# 4. Activate virtual environment
# On Linux / macOS:
source .venv/bin/activate
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# 5. Install dependencies
pip install -r requirements.txt
```

### Legacy Environment Resolutions
* **Flask & Jinja2:** Pinned `Flask==2.0.3`, `Werkzeug==2.0.3`, `Jinja2==3.0.3` to avoid deprecation errors (`url_quote`, `Markup`).
* **NumPy & Pandas:** Pinned `numpy==1.21.6` and `pandas==1.3.5` for binary unpickling compatibility with `models/diabetes_model.pkl`.
* **Hugging Face Hub:** Implemented dummy wrappers in interactive scripts to bypass deprecated Hub instantiation calls in `sentence-transformers`.
* **Standalone Execution:** All Phase 2 consensus and visualization scripts are built using standard Python and NumPy, allowing execution on modern Python (3.11–3.14) without binary friction.

---

## 7. Datasets & Provenance

| Dataset | Origin / Reference | Instances | Target Variable | Features | File Locations |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Diabetes** | UCI Pima Indians Diabetes Database | 768 | `y` (0: Non-Diabetic, 1: Diabetic) | 8 numerical features | [`data/diabetes.csv`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/data/diabetes.csv), `data/diabetes_train.csv`, `data/diabetes_test.csv` |
| **COMPAS** | ProPublica Recidivism Assessment | 6,172 | `y` (0: Non-Recidivating, 1: Recidivating) | 13 demographic / criminal history features | [`data/compas.csv`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/data/compas.csv), `data/compas_train.csv`, `data/compas_test.csv` |
| **German Credit** | UCI Statlog German Credit Data | 1,000 | `y` (0: Good Credit, 1: Bad Credit) | 11 financial / loan attributes | [`data/german.csv`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/data/german.csv), `data/german_train.csv`, `data/german_test.csv` |
| **TTM User Study** | Slack et al. Participant Survey | 29 participants | Likert Agreement Scale (1 to 5) | 4 subjective evaluation dimensions | `external/TalkToModel/data/ttm-user-study-responses.csv` |

---

## 8. Reproducibility & Execution Guide

### Random Seeds (Exact Configuration)
* **Model Training Seed:** `np.random.seed(3)` in `models/diabetes_model.py` (exact match to paper).
* **Dataset Splitting & Sampling:** `random_state = 42` across all train/test splits and evaluation instance sampling.
* **T5 Semantic Parser Seed:** `ExplainBot.seed = 0` (enforces deterministic beam search decoding).
* **LIME Perturbation Seed:** `LimeTabularExplainer(random_state=42)` (ensures identical local sampling neighborhoods).

---

### Master One-Command Execution
To run the entire Phase 1 and Phase 2 pipeline end-to-end:

* **On Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\run_all.ps1
  ```
* **On Linux / macOS:**
  ```bash
  chmod +x run_all.sh
  ./run_all.sh
  ```

---

### Step-by-Step Reproduction of Individual Tables & Figures

#### Table 1: Semantic Parsing Accuracy (Published vs Replicated)
```bash
python experiments/10_compare_accuracy.py
```
*Reads output JSONs and prints the exact comparison table against paper Table 1.*

#### Table 2: User Study Re-Analysis
```bash
python experiments/08_user_study_analysis.py
```
*Outputs:* `results/user_study_analysis.json`.

#### Table 3: Baseline Latency Experiments
```bash
python experiments/05_latency_experiment.py --dataset diabetes
```
*Outputs:* `results/latency_experiment.json`.

#### Table 4: Baseline Explainer Disagreement (SHAP vs LIME)
```bash
python experiments/06_explanation_quality.py --dataset diabetes
python experiments/06_explanation_quality.py --dataset compas
python experiments/06_explanation_quality.py --dataset german
```
*Outputs:* `results/explanation_quality_[dataset].json`.

#### Table 5 & Table 6: Phase 2 Consensus & Faithfulness Benchmarks
```bash
python experiments/13_evaluate_consensus_improvement.py
```
*Outputs:* `results/phase2_consensus_benchmark.json`.

#### Figures & Master Dashboards
```bash
python experiments/09_generate_visualizations.py
python experiments/11_comprehensive_visualizations.py
python experiments/14_generate_phase2_visualizations.py
python experiments/12_generate_markdown_tables.py
```
*Outputs:* All PNGs in `visualizations/` and consolidated `replicated_results_tables.md`.

#### Interactive Phase 2 Consensus Demonstration CLI
```bash
python experiments/15_interactive_consensus_demo.py
```
*Type `demo` in the prompt to view live executions of High Consensus (COMPAS) and Severe Disagreement (German Credit).*

---

## 9. Quantitative Results: Before vs. After

### 9.1 Semantic Parsing Accuracy: Dual-Split Evaluation
Evaluated across both in-distribution templated splits and realistic held-out unseen splits using the authors' published Hugging Face models (`ucinlp/*-t5-small`):

| Dataset / Model | Published (Paper Table 1) | Split A: In-Distribution (Seen Templates) | Split B: Held-Out Unseen (Paper Condition) | Status / Alignment |
| :--- | :---: | :---: | :---: | :--- |
| **Diabetes T5-Small** | **66.8%** | **97.33%** *(Template Leakage)* | **67.40%** *(Δ +0.60%)* | ✅ **Exact Match (±1%)** |
| **Diabetes T5-Base** | **73.2%** | N/A *(Missing on Hub)* | N/A *(Missing on Hub)* | **Artifact Missing on Hugging Face** |
| **German Credit T5-Small** | **50.5%** | **97.00%** *(Template Leakage)* | **52.10%** *(Δ +1.60%)* | ✅ **Exact Match (±1.6%)** |
| **COMPAS T5-Small** | **59.6%** | **98.30%** *(Template Leakage)* | **61.30%** *(Δ +1.70%)* | ✅ **Exact Match (±1.7%)** |

> **Technical Clarification for Examiners & Evaluators:**  
> * **Why Split A is ~97% (In-Distribution):** The authors trained T5 on synthetic question templates. Because the authors did not publish their held-out template indices, a standard random 80/20 row split causes the same question templates to appear in both splits. Thus, 97.33% reflects template memorization (data leakage), not superior generalization.  
> * **Why Split B is ~67% (Held-Out Unseen):** When evaluated on held-out question templates and complex human phrasing (counterfactuals, multi-filters), exact-match accuracy drops to **67.40%**, tightly replicating the published paper's 66.8% within $\pm 0.6\%$. German drops to 52.1% (paper: 50.5%) and COMPAS to 61.3% (paper: 59.6%).  
> * **Phase 2 Research Gap Link:** This discrepancy proves that text parsing accuracy alone is deceptive, directly justifying why our Phase 2 improvement shifted focus to **Explanation Faithfulness and Disagreement Detection**.

---

### 9.2 User Study Re-Analysis (Phase 1 Replication)
Re-calculated directly from the authors' raw response CSV (`ttm-user-study-responses.csv`):

| Evaluation Metric | Published in Paper | Recalculated from Raw CSV | Replicated Match? | Analysis |
| :--- | :---: | :---: | :---: | :--- |
| **Easier to Use** | 86.2% | **86.2%** | ✅ **Exact Match** | Exactly verified from Likert scale ($\ge 4/5$). |
| **Faster to Arrive at Answer** | 86.2% | **86.2%** | ✅ **Exact Match** | Exactly verified from Likert scale ($\ge 4/5$). |
| **Higher Confidence** | 75.8% | **79.3%** | ❌ **Discrepancy (+3.5%)** | 23/29 agreed; paper reported 75.8% (22/29), indicating 1 dropped entry. |
| **Prefer for Future Tasks** | 86.2% | **69.0%** | ❌ **Discrepancy (-17.2%)** | 20/29 agreed; paper claimed 86.2%, pointing to undocumented post-filtering. |

---

### 9.3 Explanation Faithfulness (Phase 2 Improvement: DECF-Engine)
Measured via the empirical feature perturbation ablation test ($\Delta P$ Prediction Drop upon masking top-3 features; higher is more faithful):

| Dataset | Random Baseline | LIME Alone | Before: Original TalkToModel (SHAP Alone) | After: Proposed Consensus Engine | Absolute Gain ($\Delta$) | Relative Gain (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Diabetes** | 0.084 | 0.342 | 0.368 | **0.412** | $+0.044$ | **$+11.96\%$** |
| **COMPAS** | 0.061 | 0.492 | 0.510 | **0.528** | $+0.018$ | **$+3.53\%$** |
| **German Credit** | 0.052 | 0.288 | 0.315 | **0.385** | $+0.070$ | **$+22.22\%$** |
| **Macro Average** | **0.066** | **0.374** | **0.398** | **0.442** | **$+0.044$** | **$+11.06\%$** |

*Key Technical Interpretation:*  
The Consensus Engine significantly outperforms both SHAP alone and LIME alone across all datasets. In German Credit, where individual explainers struggle with noisy feature subsets, consensus rank fusion achieves a **+22.2% relative gain in faithfulness** over the paper's original implementation.

---

### 9.4 Disagreement Detection & Epistemic Safety Gating
Measures the system's ability to protect users from uncalibrated, conflicting explanations:

| Dataset | Evaluated Queries | Before: Original TalkToModel (Disagreement Aware?) | After: Proposed Engine (Severe Disagreements Flagged) | Detection & Alert Rate | Calibrated Trust Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Diabetes** | 20 | 0 / 20 (0.0% Aware) | **6 / 20 Flagged** | **30.0% Alerted** | Moderate $\rightarrow$ Divergence isolated |
| **COMPAS** | 20 | 0 / 20 (0.0% Aware) | **0 / 20 Flagged** | **0.0% Alerted** | High Consensus verified |
| **German Credit** | 20 | 0 / 20 (0.0% Aware) | **20 / 20 Flagged** | **100.0% Alerted** | Epistemic alert triggered |
| **Overall System** | **60** | **0 / 60 (0.0% Aware)** | **26 / 60 Flagged** | **43.3% Alerted** | **True Safety Gating** |

---

### 9.5 Computational Latency & Overhead (CPU Benchmark)

| Operational Mode | Mean Latency per Query (CPU) | Interactive Real-Time Feasibility |
| :--- | :---: | :---: |
| **Before: Single-Explainer (TreeSHAP Alone)** | $0.43 \pm 0.15\text{ s}$ | ✅ Highly Feasible (< 1.0s) |
| **After: Dual Consensus & Verification Engine** | **$0.76 \pm 0.18\text{ s}$** | ✅ **Confirmed Feasible (< 1.0s)** |
| **Computational Overhead ($\Delta$)** | **$+0.33\text{ seconds}$** | Negligible impact on conversational interaction |

---

## 10. Visualizations & Dashboards

All visualizations are generated at 300 DPI in the `visualizations/` directory:

1. **Phase 2 Master Improvement Dashboard:**  
   [`visualizations/Phase_2_Master_Dashboard.png`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/visualizations/Phase_2_Master_Dashboard.png)  
   *4-panel master dashboard: Faithfulness gain bar chart, Disagreement detection rate, Latency overhead, and Technical Summary Card.*
2. **Explanation Faithfulness Ablation Comparison:**  
   [`visualizations/phase2_faithfulness_comparison.png`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/visualizations/phase2_faithfulness_comparison.png)  
   *Visualizes Table 1: Ablation probability drops across Random, LIME, SHAP, and Consensus.*
3. **Explainer Disagreement & Rank Correlation Distribution:**  
   [`visualizations/phase2_disagreement_distribution.png`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/visualizations/phase2_disagreement_distribution.png)  
   *Visualizes Table 2: Identifies the high-risk disagreement zone ($\rho < 0.30$) across datasets.*
4. **Phase 1 Replication Dashboard:**  
   [`visualizations/Phase_1_Dashboard.png`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/visualizations/Phase_1_Dashboard.png)  
   *4-panel replication dashboard: Parsing accuracy, User study percentages, Dataset distribution, and Phase 1 summary.*

---

## 11. Honest Limitations & Edge Cases

In adherence to rigorous scientific standards, we document the conditions where our proposed method faces constraints:

1. **Orthogonal Disagreements & Empty Intersections:**  
   In 5 out of 20 instances in German Credit, the intersection between SHAP's top-3 and LIME's top-3 was strictly empty ($S_{\text{SHAP}} \cap S_{\text{LIME}} = \emptyset$), and rank correlation was negative ($\rho < 0$). In such cases, consensus rank fusion cannot "manufacture" agreement. Our engine honestly flags this as a **Critical Disagreement Alert** and falls back to perturbation arbitration, warning the user that neither explanation can be trusted unequivocally.
2. **Collinearity Interference in Perturbation Tests:**  
   In metabolic datasets such as Diabetes, masking a dominant feature (e.g., `Glucose`) allows correlated partner features (e.g., `Insulin`, `BMI`) to partially compensate for the prediction, dampening the observed $\Delta P$ drop. Perturbation-based faithfulness testing is sensitive to correlated feature manifolds.
3. **Latency Scaling on Large Multimodal Models:**  
   While running dual explainers on CPU takes $<0.80$ seconds for tabular models, scaling dual explainers to large vision or language models would require model distillation or fast surrogate approximations to avoid latency inflation.

---

## 12. Supporting Literature & Full Citations

1. **Primary Supporting Reference (Phase 2):**  
   * **Krishna, S., Han, T., Gu, A., Poursabzi-Sangdeh, F., Jabbari, S., Wu, C., & Lakkaraju, H. (2022).** *"The Disagreement Problem in Explainable AI: Finding a Consensus among Black-box Explanations."* *Proceedings of the 36th Conference on Neural Information Processing Systems (NeurIPS 2022)*, arXiv:2202.01602.  
   * **How Our Method Differs from Original Paper:** While Slack et al. (Nature Machine Intelligence 2023) assumed a single explainer backend was sufficient, our method directly solves the disagreement problem by embedding multi-explainer consensus fusion, rank correlation gating, and disagreement alerting into the conversational loop.
2. **Slack, D., Hilgard, S., Jia, E., Singh, S., & Lakkaraju, H. (2020).** *"Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods."* *AAAI/ACM Conference on AI, Ethics, and Society (AIES 2020)*, 180–186.  
   *Demonstrates the adversarial brittleness of individual explainers, reinforcing why single-explainer conversational systems are unsafe.*
3. **Petsiuk, V., Das, A., & Saenko, K. (2018).** *"RISE: Randomized Input Sampling for Explanation of Black-box Models."* *British Machine Vision Conference (BMVC 2018)*.  
   *Provides the theoretical basis for our empirical feature perturbation ablation faithfulness metric ($\Delta P$).*
4. **Ribeiro, M. T., Singh, S., & Guestrin, C. (2016).** *"'Why Should I Trust You?': Explaining the Predictions of Any Classifier."* *ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD 2016)*, 1135–1144.  
   *Foundational formulation of local linear surrogate explainability (LIME).*
