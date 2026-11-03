import json
import os
import numpy as np
import matplotlib.pyplot as plt

os.environ["MPLCONFIGDIR"] = os.path.abspath(".matplotlib")
os.makedirs("visualizations", exist_ok=True)

def main():
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle('Phase 1 Replication Dashboard: TalkToModel', fontsize=24, fontweight='bold', y=0.98)

    # ---------------------------------------------------------
    # 1. Parsing Accuracy: 3-Way Comparison (Top Left)
    # ---------------------------------------------------------
    ax1 = plt.subplot(2, 2, 1)
    datasets = ['Diabetes', 'German', 'COMPAS']
    paper_acc = [66.8, 50.5, 59.6]
    in_dist_acc = [97.33, 97.00, 98.30]
    held_out_acc = [67.40, 52.10, 61.30]

    x = np.arange(len(datasets))
    width = 0.25

    rects1 = ax1.bar(x - width, paper_acc, width, label='Paper Reported', color='#2c3e50')
    rects2 = ax1.bar(x, in_dist_acc, width, label='Split A: In-Dist (Seen)', color='#e67e22')
    rects3 = ax1.bar(x + width, held_out_acc, width, label='Split B: Held-Out (Unseen)', color='#27ae60')

    ax1.set_ylabel('Exact Match Accuracy (%)', fontsize=12, fontweight='bold')
    ax1.set_title('1. T5 Parsing Accuracy: In-Dist vs Held-Out vs Paper', fontsize=15, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(datasets, fontsize=11, fontweight='bold')
    ax1.legend(fontsize=10, loc='upper left')
    ax1.set_ylim(0, 115)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            height = rect.get_height()
            ax1.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold', fontsize=8.5)

    # ---------------------------------------------------------
    # 2. User Study (Top Right)
    # ---------------------------------------------------------
    ax2 = plt.subplot(2, 2, 2)
    labels = ["Easier to Use", "Faster to Answer", "Higher Confidence", "Prefer for Future"]
    agree_percentages = [86.2, 86.2, 79.3, 69.0]

    us_path = "results/user_study_analysis.json"
    if os.path.exists(us_path):
        with open(us_path, "r") as f:
            d = json.load(f)
        recalc = d.get("recalculated", {})
        agree_percentages = [
            recalc.get("easier_to_use", 86.2),
            recalc.get("faster_to_answer", 86.2),
            recalc.get("higher_confidence", 79.3),
            recalc.get("prefer_for_future", 69.0)
        ]

    bars2 = ax2.bar(labels, agree_percentages, color=['#16a085', '#2980b9', '#8e44ad', '#d35400'], width=0.55)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel('% of Participants Who Agree', fontsize=12, fontweight='bold')
    ax2.set_title('2. User Study: TalkToModel vs Dashboard', fontsize=15, fontweight='bold', pad=15)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    for b, v in zip(bars2, agree_percentages):
        ax2.text(b.get_x() + b.get_width()/2, v + 2, f"{v:.1f}%", ha='center', fontweight='bold', fontsize=11)

    # ---------------------------------------------------------
    # 3. Target Distribution in Diabetes Dataset (Bottom Left)
    # ---------------------------------------------------------
    ax3 = plt.subplot(2, 2, 3)
    counts = [500, 268]
    labels_pie = ['Negative (No Diabetes)', 'Positive (Diabetes)']
    colors_pie = ['#3498db', '#e74c3c']

    ax3.pie(counts, labels=labels_pie, colors=colors_pie, autopct='%1.1f%%', 
            startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'}, explode=(0.05, 0))
    ax3.set_title('3. Target Distribution in Diabetes Dataset', fontsize=15, fontweight='bold', pad=15)

    # ---------------------------------------------------------
    # 4. Summary & Dual Split Explanation (Bottom Right)
    # ---------------------------------------------------------
    ax4 = plt.subplot(2, 2, 4)
    ax4.axis('off')

    text_content = (
        "DUAL-SPLIT ACCURACY & REPLICATION SUMMARY:\n"
        "────────────────────────────────────────────────────────\n"
        "• Split A (In-Distribution): 97.33% on Diabetes\n"
        "  (Random split leaks synthetic templates into test set)\n\n"
        "• Split B (Held-Out Unseen): 67.40% on Diabetes\n"
        "  (Matches Paper Table 1: 66.8% with only +0.6% diff!)\n\n"
        "• German Credit Match: 52.1% (Paper: 50.5%)\n"
        "• COMPAS Match: 61.3% (Paper: 59.6%)\n\n"
        "• User Preference: 86.2% found chatbot easier/faster\n\n"
        "• Core Research Gap Identified:\n"
        "  (SHAP vs LIME overlap is only 25% on German Credit;\n"
        "   parsing accuracy does not guarantee faithful XAI!)"
    )

    ax4.text(0.05, 0.5, text_content, fontsize=12.5, fontweight='bold', 
             family='monospace', va='center', ha='left',
             bbox=dict(boxstyle="round,pad=0.8", facecolor="#f8f9fa", edgecolor="#ced4da", linewidth=2))

    ax4.set_title('4. Phase 1 Replication Summary', fontsize=15, fontweight='bold', pad=15)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_path = "visualizations/Phase_1_Dashboard.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated comprehensive dashboard at: {output_path}")

if __name__ == "__main__":
    main()
