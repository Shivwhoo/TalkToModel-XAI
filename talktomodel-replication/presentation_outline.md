# TalkToModel: Phase 2 Presentation & Live Demo Outline
**Paper:** *Explaining machine learning models with interactive natural language conversations using TalkToModel* (Slack et al., Nature Machine Intelligence 2023)  
**Authors / Presenters:** Sachin Kumar, Shiv Kishore, Udit Dadhich, Sudhanshu Baberwal  
**Comprehensive Script:** See [`VIDEO_SCRIPT.md`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/VIDEO_SCRIPT.md) for the verbatim 10-minute recording script and slide-by-slide cues.

---

## 1. Presentation Structure (10-Minute Target)

| Section | Duration | Key Focus | Screen Action |
| :--- | :---: | :--- | :--- |
| **1. Introduction** | 1:00 min | Paper title, authors, motivation, dialogue architecture | Title slide + TalkToModel schematic |
| **2. Research Gap** | 2:00 min | The Disagreement Problem (Krishna et al. 2022); single-explainer vulnerability | Mathematical divergence + German Credit 25% overlap plot |
| **3. Proposed Improvement** | 2:00 min | DECF-Engine: Dual SHAP+LIME consensus, Borda fusion, perturbation ablation | Literature slide + DECF architecture flowchart |
| **4. Implementation** | 2:00 min | Code walkthrough of `xai/consensus_engine.py` + Live CLI demo | Code editor + Terminal execution of `15_interactive_consensus_demo.py` |
| **5. Experimental Results** | 2:00 min | Faithfulness gain (+11.1%), disagreement detection (100% on German), CPU latency | Phase 2 Master Dashboard + comparison tables |
| **6. Conclusion** | 1:00 min | Contributions, honest reporting of failure cases & edge cases | Summary slide + limitations + GitHub repo link |

---

## 2. Live Demo Cheat Sheet (For Section 4)

Open terminal and execute:
```bash
python experiments/15_interactive_consensus_demo.py
```
When prompted with `USER QUERY >`, type:
```text
demo
```

### Scenario 1: High Consensus (COMPAS Recidivism Prediction)
* **Query:** *"explain why patient 323 is predicted to recidivate"*
* **Behavior:** Both SHAP and LIME independently identify `number_of_prior_crimes` and `age` (Overlap: 66.7%, $\rho = 0.90$).
* **System Response:** 🟢 **High Confidence Dialogue** with verified prediction probability drop ($\Delta P = 0.528$).

### Scenario 2: Severe Disagreement Alert (German Credit Risk Prediction)
* **Query:** *"why was loan applicant 95 denied credit?"*
* **Behavior:** SHAP attributes denial to `LoanAmount` and `LoanDuration`, whereas LIME attributes to `NoCurrentLoan` and `loanpurposeUsedCar` (Overlap: 33.3%, $\rho = 0.116$).
* **System Response:** 🔴 **Critical Disagreement Alert** triggered. Exposes the divergent feature sets, warns user of epistemic uncertainty, and runs perturbation arbitration.

---

## 3. Key Visual Assets to Display
* **Master Phase 2 Dashboard:** [`visualizations/Phase_2_Master_Dashboard.png`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/visualizations/Phase_2_Master_Dashboard.png)
* **Faithfulness Ablation Comparison:** [`visualizations/phase2_faithfulness_comparison.png`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/visualizations/phase2_faithfulness_comparison.png)
* **Explainer Disagreement Distribution:** [`visualizations/phase2_disagreement_distribution.png`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/visualizations/phase2_disagreement_distribution.png)
* **Master Phase 1 Dashboard:** [`visualizations/Phase_1_Dashboard.png`](file:///c:/Users/Sachin/Desktop/talktomodel-replication/visualizations/Phase_1_Dashboard.png)
