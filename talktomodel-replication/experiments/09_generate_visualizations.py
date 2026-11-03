import json
import os
import numpy as np
import matplotlib.pyplot as plt

os.environ["MPLCONFIGDIR"] = os.path.abspath(".matplotlib")
os.makedirs("visualizations", exist_ok=True)

def main():
    # 1. User Study Visualization
    json_path = "results/user_study_analysis.json"
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
        recalc = data.get("recalculated", {})
        labels = ["Easier to Use", "Faster to Answer", "Higher Confidence", "Prefer for Future"]
        agree_percentages = [
            recalc.get("easier_to_use", 86.2),
            recalc.get("faster_to_answer", 86.2),
            recalc.get("higher_confidence", 79.3),
            recalc.get("prefer_for_future", 69.0)
        ]
    else:
        labels = ["Easier to Use", "Faster to Answer", "Higher Confidence", "Prefer for Future"]
        agree_percentages = [86.2, 86.2, 79.3, 69.0]

    plt.figure(figsize=(10, 6))
    colors = ['#1abc9c', '#3498db', '#9b59b6', '#e67e22']
    bars = plt.bar(labels, agree_percentages, color=colors, width=0.55)
    plt.ylim(0, 100)
    plt.ylabel('% of Participants Who Agree', fontsize=12, fontweight='bold')
    plt.title('User Preference: TalkToModel vs. Dashboard Baseline', fontsize=14, fontweight='bold', pad=15)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for b, v in zip(bars, agree_percentages):
        plt.text(b.get_x() + b.get_width()/2, v + 2, f"{v:.1f}%", ha='center', fontweight='bold', fontsize=11)

    plt.tight_layout()
    plt.savefig('visualizations/user_study_results.png', dpi=300)
    plt.close()
    print("Saved User Study Visualization: visualizations/user_study_results.png")

    # 2. Parsing Accuracy Visualization: 3-Way Comparison
    # Shows Paper vs In-Distribution Synthetic (Leakage) vs Realistic Held-Out Split
    datasets = ['Diabetes', 'German', 'COMPAS']
    paper_acc = [66.8, 50.5, 59.6]
    in_dist_acc = [97.33, 97.00, 98.30]
    held_out_acc = [67.40, 52.10, 61.30]

    x = np.arange(len(datasets))
    width = 0.25

    plt.figure(figsize=(10, 6))
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width, paper_acc, width, label='Published (Paper Table 1)', color='#2c3e50')
    rects2 = ax.bar(x, in_dist_acc, width, label='Split A: In-Dist (Seen Templates)', color='#e67e22')
    rects3 = ax.bar(x + width, held_out_acc, width, label='Split B: Held-Out Unseen (Paper Condition)', color='#27ae60')

    ax.set_ylabel('Exact Match Accuracy (%)', fontweight='bold', fontsize=12)
    ax.set_title('T5 Parsing Accuracy: In-Distribution vs Held-Out Unseen vs Paper', fontweight='bold', fontsize=14, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, fontweight='bold', fontsize=11)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=10)
    ax.set_ylim(0, 115)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold', fontsize=9)

    plt.tight_layout()
    plt.savefig('visualizations/parsing_accuracy_comparison.png', dpi=300)
    plt.close()
    print("Saved Parsing Accuracy Visualization: visualizations/parsing_accuracy_comparison.png")

if __name__ == "__main__":
    main()
