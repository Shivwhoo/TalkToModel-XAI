# TalkToModel: Phase 1 Replication Presentation
**Date:** September 29, 2026

---

## 1. Introduction (2 mins)
* **The Paper:** "Explaining machine learning models with interactive natural language conversations using TalkToModel" (Slack et al., Nature Machine Intelligence 2023).
* **The Core Concept:** Unlike static dashboards, TalkToModel translates natural language questions into executable code to generate XAI explanations (SHAP, DiCE) on the fly.
* **Our Objective:** Conduct a strict Phase 1 replication to restore the legacy codebase, validate the authors' quantitative claims, and prove the end-to-end inference pipeline still functions.

## 2. Engineering Challenges & Environment Restoration (3 mins)
*Highlight this to show the technical effort required before any data could be generated.*
* **Dependency Decay:** The original code relied on deprecated versions of `Flask` (<2.3.0) and `Werkzeug`, which fundamentally broke the application due to removed URL quoting libraries. 
* **Binary Incompatibilities:** Newer ML installations auto-upgraded `numpy` to >2.0, causing binary incompatibilities with the pre-compiled `pandas 1.3.5` dependency required by the system.
* **API Breakages:** The original `sentence-transformers` instantiation crashed on initialization due to deprecated Hugging Face Hub APIs. 
* **The Fix:** We meticulously reconstructed a strict legacy environment (`.venv-legacy`), enforced dependency downgrades, and dynamically patched API crashes without modifying the integrity of the authors' core logic.

## 3. Quantitative Replication (3 mins)
*Show them the `replicated_results_tables.md` file.*
* **System Accuracy:** We successfully reran the T5 inference evaluation on the COMPAS dataset. We achieved **68.06%** for T5-Small (vs paper's 66.8%) and **72.77%** for T5-Base (vs paper's 73.2%), confirming the fine-tuned weights are authentic and reproducible.
* **User Study Validation:** We went straight to the raw survey data (`ttm-user-study-responses.csv`) and wrote a custom script to extract their subjective metrics. We confirmed the paper's core claim: **86.2% of participants agreed the conversational interface was easier and faster** than the traditional dashboard.

## 4. Live Demonstration (4 mins)
*Run the `07_end_to_end_talktomodel_diabetes.py` script live.*
* **Explain the Flow:** 
    1. **Input:** *"explain the feature importance for the patient with id 51"*
    2. **Parser:** The local T5 model translates this to `filter id 51 and explain features [e]`.
    3. **Execution Engine:** The internal `ExplainBot` orchestrates the extraction of patient 51, runs it through the actual Diabetes ML model, and computes local feature importances using the `MegaExplainer` class.
    4. **Output:** It returns a dynamic template response indicating that Glucose, BMI, and Age were the primary negative drivers.
* **Key Takeaway:** We aren't just hitting an OpenAI API; this is a fully localized, deterministic, intent-driven XAI pipeline.

## 5. Next Steps / Phase 2 Discussion (2 mins)
* **What's Next:** Ask your professor where they want to take Phase 2. 
    * Do they want to upgrade the frontend and deploy it?
    * Do they want to swap the legacy T5 parser for a modern LLM (like Llama 3 or Gemini)?
    * Do they want to test it on a completely novel dataset?
