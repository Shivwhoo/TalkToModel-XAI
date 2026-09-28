import json
import os

def main():
    md_content = """# Replicated Results Tables

The following tables are automatically generated from the raw JSON results produced by the evaluation scripts.

## 1. Parsing Accuracy (Exact Match)

| Dataset | Model Architecture | Paper Reported | Our Replication | Difference |
| :--- | :--- | :--- | :--- | :--- |
"""

    models = [
        ("ucinlp/diabetes-t5-small", 66.8, "T5-Small", "Diabetes"),
        ("ucinlp/diabetes-t5-base", 73.2, "T5-Base", "Diabetes"),
        ("ucinlp/german-t5-small", 50.5, "T5-Small", "German"),
        ("ucinlp/compas-t5-small", 59.6, "T5-Small", "COMPAS")
    ]

    for model_id, paper_acc, name, dataset in models:
        json_path = f"results/parsing_{dataset.lower()}_{model_id.replace('/', '_')}.json"
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
                if "error" in data:
                    md_content += f"| {dataset} | {name} | {paper_acc:.1f}% | N/A (Model missing) | - |\n"
                else:
                    acc = data.get("accuracy", 0) * 100
                    diff_str = f"{acc - paper_acc:+.2f}%" if paper_acc > 0 else "N/A"
                    paper_str = f"{paper_acc:.1f}%" if paper_acc > 0 else "Unknown"
                    md_content += f"| {dataset} | {name} | {paper_str} | {acc:.2f}% | {diff_str} |\n"
        else:
            md_content += f"| Diabetes | {name} | {paper_acc:.1f}% | N/A | N/A |\n"

    md_content += """

## 2. Explanation Quality (SHAP vs LIME)

"""
    for dataset in ["diabetes", "compas", "german"]:
        eq_path = f"results/explanation_quality_{dataset}.json"
        if os.path.exists(eq_path):
            with open(eq_path, 'r') as f:
                data = json.load(f)
                md_content += f"### {dataset.capitalize()}\n"
                md_content += f"- **Mean Top-3 Feature Overlap:** {data.get('mean_top3_overlap', 0):.2%}\n"
                md_content += f"- **Mean Spearman Rank Correlation:** {data.get('mean_spearman_corr', 0):.3f}\n\n"
        else:
            md_content += f"### {dataset.capitalize()}\nResults pending.\n\n"

    md_content += """
## 3. End-to-End Latency

| Dataset | Question | Mean Latency (s) | Std Dev (s) |
| :--- | :--- | :--- | :--- |
"""
    for dataset in ["diabetes", "compas", "german"]:
        lat_path = f"results/latency_experiment_{dataset}.json"
        if os.path.exists(lat_path):
            with open(lat_path, 'r') as f:
                data = json.load(f)
                for q, metrics in data.items():
                    mean_l = metrics.get('mean_latency_sec', 0)
                    std_l = metrics.get('std_latency_sec', 0)
                    md_content += f"| {dataset.capitalize()} | {q} | {mean_l:.2f}s | {std_l:.2f}s |\n"
        else:
            md_content += f"| {dataset.capitalize()} | Pending... | N/A | N/A |\n"


    md_content += """

## 4. User Study Re-Analysis

| Metric | Paper Reported | Recalculated | Matches? |
| :--- | :--- | :--- | :--- |
"""
    us_path = "results/user_study_analysis.json"
    if os.path.exists(us_path):
        with open(us_path, 'r') as f:
            data = json.load(f)
            recalc = data.get("recalculated", {})
            paper = data.get("paper_reported", {})
            for key in recalc:
                r_val = recalc[key]
                p_val = paper.get(key, 0)
                match = "✅ Yes" if abs(r_val - p_val) < 2.0 else "❌ No"
                md_content += f"| {key.replace('_', ' ').title()} | {p_val:.1f}% | {r_val:.1f}% | {match} |\n"
    else:
        md_content += "| Pending... | N/A | N/A | N/A |\n"

    with open("replicated_results_tables.md", "w") as f:
        f.write(md_content)
    
    print("Regenerated replicated_results_tables.md")

if __name__ == "__main__":
    main()
