# TalkToModel: Phase 2 Video Presentation Script & Technical Speaker Notes
**Target Duration:** Exactly 10 Minutes (6 Sections)  
**Format:** Voice narration with synchronized screen recording (slides, live terminal CLI, code walkthrough, and dashboards)  
**Presenter:** Sachin Kumar (Team: Sachin Kumar, Shiv Kishore, Udit Dadhich, Sudhanshu Baberwal)  
**Paper:** *Explaining machine learning models with interactive natural language conversations using TalkToModel* (Slack et al., Nature Machine Intelligence 2023)

---

## Timing Overview
| Section | Topic | Allocated Time | Cumulative Time |
| :--- | :--- | :---: | :---: |
| **Section 1** | Introduction & Problem Overview | **1:00 min** | 0:00 – 1:00 |
| **Section 2** | The Research Gap: Single-Explainer Vulnerability & Disagreement | **2:00 min** | 1:00 – 3:00 |
| **Section 3** | Proposed Improvement: Consensus & Faithfulness Engine (DECF) | **2:00 min** | 3:00 – 5:00 |
| **Section 4** | Implementation Walkthrough (Code & Architecture Changes) | **2:00 min** | 5:00 – 7:00 |
| **Section 5** | Experimental Results: Before-vs-After Empirical Evaluation | **2:00 min** | 7:00 – 9:00 |
| **Section 6** | Conclusion, Contribution & Honest Limitations | **1:00 min** | 9:00 – 10:00 |

---

## Detailed Section-by-Section Script & Screen Directions

### Section 1: Introduction (1:00 min | 0:00 – 1:00)

#### What to Show on Screen:
* **[0:00 – 0:30] Slide 1 (Title Slide):**
  * Title: *TalkToModel: Replication and Consensus-Aware Explanations*
  * Subtitle: Resolving Explainer Disagreement in Conversational Explainable AI
  * Authors of Original Paper: Dylan Slack, Satyapriya Krishna, Himabindu Lakkaraju, Sameer Singh (*Nature Machine Intelligence*, 2023)
  * Presenter / Team: Sachin Kumar, Shiv Kishore, Udit Dadhich, Sudhanshu Baberwal
* **[0:30 – 1:00] Slide 2 (Architecture Schematic of TalkToModel):**
  * Flow diagram showing: Natural Language Query $\rightarrow$ Fine-tuned T5 Semantic Parser $\rightarrow$ Execution Engine $\rightarrow$ XAI Explainer (`MegaExplainer`) $\rightarrow$ Template-Based Dialogue Response.

#### Spoken Narration & Technical Speaker Notes:
> *"Hello everyone. Today I am presenting our work on replicating and advancing **TalkToModel**, a landmark conversational Explainable AI system published by Dylan Slack, Satyapriya Krishna, Himabindu Lakkaraju, and Sameer Singh in Nature Machine Intelligence 2023.*
>
> *Traditional Explainable AI—like SHAP or LIME—relies on static, monolithic dashboards. If a doctor, credit officer, or policy maker wants to interrogate a prediction, they are restricted to fixed visualizations without the ability to ask iterative follow-up questions. TalkToModel solved this interaction bottleneck by providing a natural language dialogue framework. Users type plain English queries—such as 'Why was patient 51 classified as high risk?' or 'What happens if we reduce glucose to 100?'—and the system uses a fine-tuned T5 language model to translate the text into a domain-specific execution language. A deterministic backend executes the requested operations on tabular models, generating natural language explanations in real time.*
>
> *In Phase 1, our team restored the legacy environment, replicated T5 parsing accuracy across Diabetes, COMPAS, and German Credit, and reproduced the paper's claimed latency of under one second. However, during replication, we identified a critical vulnerability in TalkToModel's underlying explanation mechanism. That brings us to our research gap."*

---

### Section 2: Research Gap (2:00 min | 1:00 – 3:00)

#### What to Show on Screen:
* **[1:00 – 1:40] Slide 3 (The Research Gap: The Disagreement Problem):**
  * Diagram contrasting SHAP (Shapley coalitional cooperative game theory) versus LIME (local linear surrogate fitting on perturbed Gaussian samples).
  * Key Question: *What happens when two state-of-the-art explainers give contradictory answers to the same user query?*
* **[1:40 – 2:20] Slide 4 (Phase 1 Empirical Findings - Baseline Explainer Divergence):**
  * Show the baseline correlation table and histogram ([`results/figures/explanation_quality_hist_german.png`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/results/figures/explanation_quality_hist_german.png)):
    * COMPAS: 75% Top-3 Overlap, Spearman $\rho = 0.848$
    * Diabetes: 58.3% Top-3 Overlap, Spearman $\rho = 0.364$
    * German Credit: **25.0% Top-3 Overlap, Spearman $\rho = 0.121$**!
* **[2:20 – 3:00] Slide 5 (The Consequence: The False Trust Trap):**
  * Mockup of a clinician or loan officer receiving a confident, single-explainer answer that is completely uncalibrated.

#### Spoken Narration & Technical Speaker Notes:
> *"Here is the fundamental limitation: TalkToModel was designed around a **single-explainer paradigm**. When a user requests feature importance, the system routes the query exclusively to a single backend—TreeSHAP inside MegaExplainer.*
>
> *Why is this a fatal flaw? In machine learning theory, post-hoc explainers optimize fundamentally different mathematical objectives. SHAP computes marginal feature contributions over all possible coalitional feature subsets based on Shapley values. In contrast, LIME fits a local, weighted linear surrogate model over a perturbed Gaussian neighborhood around the instance. Because these formulations differ, explainers frequently disagree on feature rankings and top attributes.*
>
> *In our Phase 1 replication, we rigorously benchmarked the authors' SHAP explainer against LIME across 60 instances. The results were startling. While COMPAS showed strong alignment with 75% overlap, the Diabetes dataset dropped to 58.3% overlap and a Spearman rank correlation of only 0.364. Most alarmingly, on the German Credit dataset, top-3 feature overlap plummeted to **25%**, and the mean rank correlation was just **0.121**—meaning the explainers were virtually orthogonal!*
>
> *In the published TalkToModel paper, this disagreement is completely hidden from the user. When an applicant is denied a loan or a patient is flagged for disease, the chatbot outputs a single, confident answer with 100% apparent certainty. If TreeSHAP attributes the denial to Loan Amount, but LIME attributes it to Lack of Prior Credit, the user makes high-stakes decisions based on an artifact of the explainer algorithm rather than true model mechanics. Furthermore, TalkToModel offered zero runtime faithfulness verification—meaning there was no check to prove that perturbing the 'explained' features actually altered the model's decision."*

---

### Section 3: Proposed Improvement (2:00 min | 3:00 – 5:00)

#### What to Show on Screen:
* **[3:00 – 3:45] Slide 6 (Supporting Literature & Theoretical Foundation):**
  * Paper citation: Krishna et al. (NeurIPS 2022), *"The Disagreement Problem in Explainable AI: Finding a Consensus among Black-box Explanations"*.
  * Secondary references: Slack et al. (AIES 2020) on Explainer Adversarial Brittleness; Petsiuk et al. (BMVC 2018) on Perturbation Deletion Metrics.
  * Bullet comparison: *Original TalkToModel (Single Explainer, Blind Execution) vs. Our Method (Consensus Fusion, Faithfulness Arbitration, Gated Dialogue).*
* **[3:45 – 5:00] Slide 7 (The DECF-Engine Architecture):**
  * Flowchart of our **Dual-Explainer Consensus & Faithfulness Verification Engine**:
    1. Parallel SHAP + LIME Attribution
    2. Agreement Metric: Top-$k$ Jaccard Index & Spearman Rank Correlation ($\rho$)
    3. Consensus Rank Fusion via Borda Count
    4. Empirical Ablation Faithfulness Test ($\Delta P$ drop)
    5. Calibrated Conversational Generator (Green / Yellow / Red Alert States).

#### Spoken Narration & Technical Speaker Notes:
> *"To bridge this critical research gap, we grounded our solution in the theoretical work of **Krishna et al. (NeurIPS 2022)** on the Disagreement Problem in Explainable AI, as well as perturbation faithfulness metrics by **Petsiuk et al. (BMVC 2018)**.*
>
> *How does our method differ from the original paper? While Slack et al. treated feature attribution as a static, single-backend pipeline, we re-architected TalkToModel's execution core into a **Consensus-Aware Dual-Explainer & Faithfulness Verification Engine (DECF-Engine)**.*
>
> *Our improvement operates through four key mathematical stages:*
> *First, when an explanation is requested, our engine concurrently generates attributions from both SHAP and LIME.*
> *Second, we quantify real-time agreement using two complementary metrics: **Top-$k$ Jaccard Overlap**, which measures set intersection of the dominant features, and **Spearman's Rank Correlation Coefficient ($\rho$)**, which evaluates monotonic alignment across the entire feature ranking.*
> *Third, we synthesize a robust feature ranking using **Borda Count Rank Fusion**, giving preference to features that appear in the consensus intersection.*
> *Fourth, we execute an empirical **Faithfulness Ablation Test**. We perturb the identified top features with baseline reference values and compute the Prediction Probability Drop: $\Delta P = |P(Y|X) - P(Y|X_{\setminus \text{top\_k}})|$. A faithful explanation must induce a sharp decrease in the target class probability.*
>
> *Finally, our response generator dynamically gates the conversation: High Consensus queries are reported with verified confidence; Moderate cases highlight the core intersection while disclosing secondary variance; and Severe Disagreement cases trigger an epistemic warning, alerting the user and using faithfulness arbitration rather than presenting false certainty."*

---

### Section 4: Implementation (2:00 min | 5:00 – 7:00)

#### What to Show on Screen:
* **[5:00 – 5:45] Screen Recording: VS Code / IDE Code Walkthrough:**
  * Open [`xai/consensus_engine.py`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/xai/consensus_engine.py).
  * Highlight functions:
    * `compute_spearman_rank_correlation()` and `compute_top_k_jaccard()`
    * `compute_borda_consensus_ranking()`
    * `evaluate_consensus()` (High / Moderate / Severe Disagreement logic)
    * `generate_conversational_response()`
* **[5:45 – 7:00] Screen Recording: Live Terminal Demonstration:**
  * Open terminal and run: `python experiments/15_interactive_consensus_demo.py`.
  * Type `demo` and let it execute.
  * Show Scenario 1 (COMPAS High Consensus, Green banner, verified features).
  * Show Scenario 2 (German Credit Severe Disagreement Alert, Red banner, SHAP vs LIME discrepancy exposed).

#### Spoken Narration & Technical Speaker Notes:
> *"Now let's examine the concrete code changes implemented in our repository.*
>
> *In `xai/consensus_engine.py`, we created the modular DECF-Engine. Notice lines 18 through 40: we implemented the Spearman rank correlation and Top-$k$ Jaccard calculations directly without brittle external dependencies. Lines 42 to 62 implement Borda rank aggregation, weighting features across both attribution distributions. Lines 75 through 105 define our three-tier consensus state machine based on rigorous empirical thresholds: High Consensus requires both $\rho \ge 0.60$ and overlap $\ge 66.7\%$; Moderate requires $\rho \ge 0.30$ and overlap $\ge 33.3\%$; otherwise, the system drops into Severe Disagreement.*
>
> *Now, let's watch this live in the terminal using our interactive demo script, `15_interactive_consensus_demo.py`.*
> *(Trigger demo in terminal)*
> *In Scenario 1, we query COMPAS patient 323: 'Explain why patient 323 is predicted to recidivate'. Notice the output: both explainers agree with 66.7% overlap and a Spearman $\rho$ of 0.90. The system issues a Green High Confidence response, highlighting 'number_of_prior_crimes' and 'age' with a verified prediction drop of $\Delta P = 0.528$.*
>
> *In Scenario 2, we query German Credit applicant 95: 'Why was applicant 95 denied credit?'. In the original TalkToModel, the chatbot gave an uncalibrated list of SHAP features. But look at our engine's output: it immediately catches a critical disagreement! Spearman correlation is only 0.116. It triggers a Red Warning Banner, explicitly telling the user: 'Warning: Severe Disagreement Detected. SHAP attributes to Loan Amount, whereas LIME attributes to No Current Loan.' It runs a faithfulness ablation check and warns the user of epistemic uncertainty. The system now actively defends against false trust."*

---

### Section 5: Experimental Results (2:00 min | 7:00 – 9:00)

#### What to Show on Screen:
* **[7:00 – 7:45] Slide 8 (Master Phase 2 Dashboard):**
  * Display [`visualizations/Phase_2_Master_Dashboard.png`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/visualizations/Phase_2_Master_Dashboard.png).
  * Point cursor to Panel 1 (Faithfulness Gain) and Panel 2 (Disagreement Detection Rate).
* **[7:45 – 8:30] Slide 9 (Before-vs-After Comparison Tables):**
  * Table 1: Faithfulness Ablation Comparison ($\Delta P$ drop across Random, LIME, SHAP, and Consensus).
  * Table 2: Disagreement Detection Rates across Datasets (0% Before vs 100% on German Credit After).
* **[8:30 – 9:00] Slide 10 (Latency Overhead & Trade-off):**
  * Point cursor to Panel 3: Latency comparison (0.43s Before vs 0.76s After).

#### Spoken Narration & Technical Speaker Notes:
> *"Let us examine the quantitative before-and-after experimental results under strictly comparable experimental conditions across all 60 benchmark instances.*
>
> *Looking at Panel 1 and Table 1: we measured explanation faithfulness via systematic feature ablation. When we mask the top-3 consensus features, the mean prediction probability drop across all datasets increases from 0.398 for SHAP alone and 0.374 for LIME alone, to **0.442 for our Consensus Engine**—representing an overall **+11.1% gain in explanation faithfulness** over the published implementation. Most notably, on German Credit, where individual explainers struggle with noisy feature subsets, our consensus fusion achieved a **+22.2% gain** in faithfulness ($\Delta P$ increased from 0.315 to 0.385).*
>
> *Looking at Panel 2 and Table 2: consider the safety and reliability metric—Disagreement Detection. The published TalkToModel flagged exactly **zero** disagreements—a 0% detection rate. Our proposed engine successfully caught and alerted **100% of the severe disagreement instances in German Credit (20/20)** and **30% in Diabetes (6/20)**, establishing true safety gating.*
>
> *Looking at Panel 3 and Table 3: what is the computational cost? In the original paper, feature explanation queries on CPU averaged 0.43 seconds. In our dual-explainer consensus engine with runtime ablation testing, mean CPU latency is **0.76 seconds**—an overhead of 330 milliseconds. This remains well under the 1.0-second interactive threshold, confirming that our reliability gains do not compromise real-time conversational usability."*

---

### Section 6: Conclusion & Honest Limitations (1:00 min | 9:00 – 10:00)

#### What to Show on Screen:
* **[9:00 – 9:40] Slide 11 (Summary of Findings & Core Contributions):**
  * Clear bullet chain: Research Gap $\rightarrow$ DECF-Engine $\rightarrow$ +11.1% Faithfulness & 100% Conflict Gating.
  * Published vs. Replicated vs. Improved metrics clearly summarized.
* **[9:40 – 10:00] Slide 12 (Honest Limitations & Future Work / Q&A Slide):**
  * Limitation 1: Negative rank correlation cases ($S_{\text{SHAP}} \cap S_{\text{LIME}} = \emptyset$) require fallback arbitration.
  * Limitation 2: Multicollinearity in metabolic datasets (Diabetes).
  * GitHub Repository link, Final Checklist, and Thank You message.

#### Spoken Narration & Technical Speaker Notes:
> *"In conclusion, our Phase 2 investigation establishes a complete, rigorous research chain:*
> *We identified that TalkToModel's single-explainer architecture created dangerous vulnerability to explainer disagreement.*
> *We proposed and implemented the Consensus-Aware Dual-Explainer & Faithfulness Verification Engine, grounded in Krishna et al. (NeurIPS 2022).*
> *Our empirical results prove that our consensus engine improves explanation faithfulness by +11.1% while successfully catching 100% of severe attribution conflicts.*
>
> *In the spirit of honest scientific reporting, we highlight key limitations:*
> *First, in cases of extreme negative rank correlation where the intersection of SHAP and LIME is empty, consensus fusion cannot manufacture agreement. Our engine honestly flags this as a critical alert and triggers perturbation arbitration.*
> *Second, in datasets with high multicollinearity, such as Glucose and Insulin in Diabetes, masking one feature allows correlated features to absorb attribution, dampening ablation drops.*
> *Third, scaling dual explainers to large language models will require faster distillation surrogates to avoid latency inflation.*
>
> *All code, datasets, evaluation scripts, and replication artifacts are fully documented in our GitHub repository. Thank you for your time, and I welcome any questions."*

