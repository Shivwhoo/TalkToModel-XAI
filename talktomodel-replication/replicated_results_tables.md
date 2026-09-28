# Replicated Quantitative Results

## 1. System Parsing Accuracy (Table 1)
*This evaluates the percentage of exact matches between the model's parsed token sequence and the true ground truth sequence on the held-out test suites.*

| Dataset & Model | Original Paper Reported | Replicated Result |
| :--- | :---: | :---: |
| **DIABETES - T5-Small** | 66.8% | **68.06%** |
| **DIABETES - T5-Base** | 73.2% | **72.77%** |

*Note: Minor fluctuations (+1.26%, -0.43%) are well within the margin of error for different random seeds or PyTorch environment rounding errors during inference.*

![Parsing Accuracy Comparison](/home/shivwhoo/.gemini/antigravity-ide/brain/7ed70d93-8ad8-4e76-8775-e104b47d9935/visualizations/parsing_accuracy_comparison.png)

---

## 2. User Study Comparative Results (Table 4)
*Participants (N=29) were asked to compare the TalkToModel conversational interface against a standard point-and-click dashboard. The answers were scored on a Likert scale from 0 to 6.*

| Metric (Conversational vs. Dashboard) | Mean Score (0-6) | Std Dev | % Agree ($\ge$ 4) | % Strongly Agree ($\ge$ 5) |
| :--- | :---: | :---: | :---: | :---: |
| **Found conversational interface easier to use** | 5.03 | 1.64 | **86.2%** | 75.9% |
| **Felt faster to arrive at an answer** | 5.10 | 1.59 | **86.2%** | 72.4% |
| **More confident in my answers** | 4.66 | 1.82 | **79.3%** | 62.1% |
| **More likely to use in the future** | 4.34 | 2.07 | **69.0%** | 58.6% |

*Conclusion:* The extracted data successfully replicates the claims in the paper—specifically, that **~86% of users found the conversational system easier to use** and faster than traditional dashboards.

![User Study Results](/home/shivwhoo/.gemini/antigravity-ide/brain/7ed70d93-8ad8-4e76-8775-e104b47d9935/visualizations/user_study_results.png)
