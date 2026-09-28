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
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="diabetes", help="Dataset name")
    args = parser.parse_args()
    
    dataset_name = args.dataset
    print(f"Running Explanation Quality Comparison (SHAP vs LIME) for {dataset_name}...")
    
    # 1. Load model and data
    repo_path = os.environ.get("TALKTOMODEL_DIR", "external/TalkToModel")
    if dataset_name == "compas":
        model_file = f"{repo_path}/data/{dataset_name}_model_grad_boosted_tree.pkl"
    else:
        model_file = f"{repo_path}/data/{dataset_name}_model_grad_tree.pkl"
        
    with open(model_file, "rb") as f:
        model = pickle.load(f)
        
    train_df = pd.read_csv(f"{repo_path}/data/{dataset_name}_train.csv")
    test_df = pd.read_csv(f"{repo_path}/data/{dataset_name}_test.csv")
    
    feature_columns = [c for c in train_df.columns if c not in ["y", "id", "Unnamed: 0"]]
    
    X_train = train_df[feature_columns]
    X_test = test_df[feature_columns]
    
    # 2. Setup Explainers
    # SHAP Explainer
    # TreeExplainer is used for GradientBoostedTrees (which this model is)
    model_step = model.steps[-1][1] if hasattr(model, 'steps') else model
    shap_explainer = shap.TreeExplainer(model_step)
    
    class_names = ["unlikely", "likely"]
    if dataset_name == "diabetes":
        class_names = ["unlikely to have diabetes", "likely to have diabetes"]
    elif dataset_name == "compas":
        class_names = ["likely to recidivate", "unlikely to recidivate"]
    elif dataset_name == "german":
        class_names = ["good credit", "bad credit"]
        
    # LIME Explainer (reusing user's logic)
    lime_explainer = LimeTabularExplainer(
        training_data=X_train.values,
        feature_names=feature_columns,
        class_names=class_names,
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
        num_features = min(8, len(feature_columns))
        lime_exp = lime_explainer.explain_instance(instance.values, predict_fn, num_features=num_features)
        lime_vals = np.zeros(len(feature_columns))
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
    
    print(f"Evaluated {N} instances.")
    print(f"Mean Top-3 Feature Overlap: {mean_overlap:.2%}")
    print(f"Mean Spearman Rank Correlation: {mean_corr:.3f}")
    
    os.makedirs("results/figures", exist_ok=True)
    with open(f"results/explanation_quality_{dataset_name}.json", "w") as f:
        json.dump({
            "mean_top3_overlap": mean_overlap,
            "mean_spearman_corr": mean_corr,
            "details": results
        }, f, indent=4)
        
    # Plotting
    plt.figure(figsize=(8, 5))
    sns.histplot(correlations, bins=10, kde=True, color="purple")
    plt.axvline(mean_corr, color="red", linestyle="--", label=f"Mean: {mean_corr:.2f}")
    plt.title(f"Distribution of Rank Correlation (SHAP vs LIME) - {dataset_name}")
    plt.xlabel("Spearman Rank Correlation")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"results/figures/explanation_quality_hist_{dataset_name}.png", dpi=300)
    print(f"Saved results to results/explanation_quality_{dataset_name}.json and results/figures/explanation_quality_hist_{dataset_name}.png")

if __name__ == "__main__":
    main()
