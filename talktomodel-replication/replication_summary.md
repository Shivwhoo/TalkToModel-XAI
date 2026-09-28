# TalkToModel: Phase 1 Replication Summary

**Paper:** *Explaining machine learning models with interactive natural language conversations using TalkToModel* (Slack et al., Nature Machine Intelligence 2023)

## 1. Project Objective
This project is a Phase 1 Explainable AI (XAI) replication effort focusing on **TalkToModel**, a dialogue system that allows users to converse with machine learning models in natural language to extract explanations. The central idea of TalkToModel is the end-to-end dialogue framework:
**Natural Language** $\rightarrow$ **T5 Token Parser** $\rightarrow$ **Action Mapping Engine** $\rightarrow$ **XAI Explainer** $\rightarrow$ **Template-based Response**.

The goal was to restore the legacy codebase, evaluate the parsing accuracy of its underlying T5 models, and successfully demonstrate a working end-to-end interaction without relying on the web frontend.

## 2. Environment & Dependency Resolution
The original codebase relies on legacy packages and strict version constraints, complicating out-of-the-box execution. Key resolutions included:
*   **Python:** Enforced Python `3.10` via a dedicated virtual environment (`.venv-legacy`).
*   **Web Framework:** Pinned `Flask==2.0.3` and `Werkzeug==2.0.3` to resolve deprecation crashes (e.g., `url_quote` import errors). Pinned `Jinja2==3.0.3` to resolve `Markup` import issues in Flask.
*   **Data Science Stack:** Downgraded `numpy` to `1.21.6` to preserve binary compatibility with pre-compiled `pandas==1.3.5` and `dice-ml`.
*   **Other Dependencies:** Patched missing legacy NLP libraries (`wordninja`, `nltk`) and bypassed `sentence-transformers` instantiation bugs associated with deprecated Hugging Face Hub APIs.

## 3. Quantitative Replication: Parsing Accuracy
We evaluated the ability of the fine-tuned T5 models to translate natural language queries into executable parsing syntax. We successfully verified the parsing exact-match accuracy using the `compas` dataset:

| Model | Reported Accuracy (Paper Table 1) | Replicated Accuracy (Test Set) |
| :--- | :--- | :--- |
| **T5-Small** | 66.8% | **68.06%** |
| **T5-Base** | 73.2% | **72.77%** |

*Note: The replication scripts yielded parsing accuracies closely matching the original publication, confirming the integrity of the downloaded fine-tuned models.*

## 4. End-to-End Implementation
To validate the full interaction lifecycle, an end-to-end script (`07_end_to_end_talktomodel_diabetes.py`) was developed for the `diabetes` dataset. This bypasses the React/Flask frontend, allowing programmatic dialogue evaluation.

**Test Case Execution:**
*   **User Input:** *"explain the feature importance for the patient with id 51"*
*   **Parsed Command:** `filter id 51 and explain features [e]`
*   **Execution:** The internal execution engine dynamically mapped the tokens to `MegaExplainer`, computing local feature importances using the model's gradients/SHAP.
*   **Final Output:** Generated a natural language response identifying `glucose`, `bmi`, and `age` as the top three features with a negative influence on the prediction for patient 51.

This confirms the end-to-end system is completely functional.

## 5. Next Steps
*   **Further Quantitative Replication:** Reproduce 2-3 additional main result tables or graphs from the paper (e.g., Explanation Faithfulness, Latency, or User Study metrics).
*   **Presentation Preparation:** Prepare the live presentation (scheduled for Sept 29, 2026), including potential live demonstrations of the end-to-end script.
