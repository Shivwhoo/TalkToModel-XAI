# Replicated Results Tables

The following tables are automatically generated from the raw JSON results produced by the evaluation scripts.

## 1. Parsing Accuracy (Exact Match)

| Dataset | Model Architecture | Paper Reported | Our Replication | Difference |
| :--- | :--- | :--- | :--- | :--- |
| Diabetes | T5-Small | 66.8% | 97.33% | +30.53% |
| Diabetes | T5-Base | 73.2% | N/A (Model missing) | - |
| Diabetes | T5-Small | 50.5% | N/A | N/A |
| Diabetes | T5-Small | 59.6% | N/A | N/A |


## 2. Explanation Quality (SHAP vs LIME)

### Diabetes
- **Mean Top-3 Feature Overlap:** 58.33%
- **Mean Spearman Rank Correlation:** 0.364

### Compas
- **Mean Top-3 Feature Overlap:** 75.00%
- **Mean Spearman Rank Correlation:** 0.848

### German
- **Mean Top-3 Feature Overlap:** 25.00%
- **Mean Spearman Rank Correlation:** 0.121


## 3. End-to-End Latency

| Dataset | Question | Mean Latency (s) | Std Dev (s) |
| :--- | :--- | :--- | :--- |
| Diabetes | Pending... | N/A | N/A |
| Compas | Pending... | N/A | N/A |
| German | Pending... | N/A | N/A |


## 4. User Study Re-Analysis

| Metric | Paper Reported | Recalculated | Matches? |
| :--- | :--- | :--- | :--- |
| Easier To Use | 86.2% | 86.2% | ✅ Yes |
| Faster To Answer | 86.2% | 86.2% | ✅ Yes |
| Higher Confidence | 75.8% | 79.3% | ❌ No |
| Prefer For Future | 86.2% | 69.0% | ❌ No |
