# Replicated Results Tables

The following tables are automatically generated from the raw JSON results produced by the evaluation scripts.

## 1. Parsing Accuracy (Exact Match)

| Dataset | Model Architecture | Paper Reported | Our Replication | Difference |
| :--- | :--- | :--- | :--- | :--- |
| Diabetes | T5-Small | 66.8% | 97.33% | +30.53% |
| Diabetes | T5-Base | 73.2% | N/A (Model missing) | - |


## 2. Explanation Quality (SHAP vs LIME)

- **Mean Top-3 Feature Overlap:** 58.33%
- **Mean Spearman Rank Correlation:** 0.364


## 3. End-to-End Latency

| Question | Mean Latency (s) | Std Dev (s) |
| :--- | :--- | :--- |
| explain the feature importance for the patient with id 51 | 0.44s | 0.15s |
| what is the model prediction for patient 10? | 0.39s | 0.08s |
| how does age affect the prediction for patient 20? | 0.38s | 0.06s |
| what would happen if we change glucose to 100 for patient 5? | 0.70s | 0.18s |
| what are the top 3 features? | 0.33s | 0.07s |


## 4. User Study Re-Analysis

| Metric | Paper Reported | Recalculated | Matches? |
| :--- | :--- | :--- | :--- |
| Easier To Use | 86.2% | 86.2% | ✅ Yes |
| Faster To Answer | 86.2% | 86.2% | ✅ Yes |
| Higher Confidence | 75.8% | 79.3% | ❌ No |
| Prefer For Future | 86.2% | 69.0% | ❌ No |
