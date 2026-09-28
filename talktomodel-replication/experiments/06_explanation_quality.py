import sys
import os
import json
import pickle
import pandas as pd
import numpy as np
import shap
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
from lime.lime_tabular import LimeTabularExplainer

def main():
    print("Running Explanation Quality Comparison (SHAP vs LIME)...")
    
    # 1. Load model and data
    with open("models/diabetes_model.pkl", "rb") as f:
        model = pickle.load(f)
        
    train_df = pd.read_csv("data/diabetes_train.csv")
    test_df = pd.read_csv("data/diabetes_test.csv")
    
    feature_columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
    X_train = train_df[feature_columns]
    X_test = test_df[feature_columns]
    
    # 2. Setup Explainers
    # SHAP Explainer
    # TreeExplainer is used for GradientBoostedTrees (which this model is)
    model_step = model.steps[-1][1] if hasattr(model, 'steps') else model
    shap_explainer = shap.TreeExplainer(model_step)
    
    # LIME Explainer (reusing user's logic)
    lime_explainer = LimeTabularExplainer(
        training_data=X_train.values,
        feature_names=feature_columns,
        class_names=["unlikely to have diabetes", "likely to have diabetes"],
        mode="classification",
        random_state=42
    )
    
    def predict_fn(data):
        df_in = pd.DataFrame(data, columns=feature_columns)
        return model.predict_proba(df_in)

    N = min(20, len(X_test))
    np.random.seed(42)
    sample_indices = np.random.choice(X_test.index, N, replace=False)
    
    results = []
    top_3_overlaps = []
    correlations = []
    
    for idx in sample_indices:
        instance = X_test.loc[idx]
        
        # SHAP explanation
        shap_vals = shap_explainer.shap_values(instance)
        if isinstance(shap_vals, list):
            shap_vals = shap_vals[1] # For binary classification
            
        shap_importance = np.abs(shap_vals)
        shap_ranks = np.argsort(-shap_importance)
        shap_top_3 = set(shap_ranks[:3])
        
        # LIME explanation
        lime_exp = lime_explainer.explain_instance(instance.values, predict_fn, num_features=8)
        lime_vals = np.zeros(8)
        for feat_idx, weight in lime_exp.local_exp[1]:
            lime_vals[feat_idx] = weight
            
        lime_importance = np.abs(lime_vals)
        lime_ranks = np.argsort(-lime_importance)
        lime_top_3 = set(lime_ranks[:3])
        
        # Metrics
        overlap = len(shap_top_3.intersection(lime_top_3)) / 3.0
        top_3_overlaps.append(overlap)
        
        corr, _ = spearmanr(shap_importance, lime_importance)
        correlations.append(corr)
        
        results.append({
            "patient_id": int(idx),
            "shap_top_3": [feature_columns[i] for i in shap_ranks[:3]],
            "lime_top_3": [feature_columns[i] for i in lime_ranks[:3]],
            "overlap_ratio": overlap,
            "spearman_corr": corr
        })
        
    mean_overlap = np.mean(top_3_overlaps)
    mean_corr = np.mean(correlations)
    
    print(f"Evaluated {N} patients.")
    print(f"Mean Top-3 Feature Overlap: {mean_overlap:.2%}")
    print(f"Mean Spearman Rank Correlation: {mean_corr:.3f}")
    
    os.makedirs("results/figures", exist_ok=True)
    with open("results/explanation_quality.json", "w") as f:
        json.dump({
            "mean_top3_overlap": mean_overlap,
            "mean_spearman_corr": mean_corr,
            "details": results
        }, f, indent=4)
        
    # Plotting
    plt.figure(figsize=(8, 5))
    sns.histplot(correlations, bins=10, kde=True, color="purple")
    plt.axvline(mean_corr, color="red", linestyle="--", label=f"Mean: {mean_corr:.2f}")
    plt.title("Distribution of Rank Correlation (SHAP vs LIME)")
    plt.xlabel("Spearman Rank Correlation")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/figures/explanation_quality_hist.png", dpi=300)
    print("Saved results to results/explanation_quality.json and results/figures/explanation_quality_hist.png")

if __name__ == "__main__":
    main()
