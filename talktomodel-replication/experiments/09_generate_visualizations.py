import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure the output directory exists
os.makedirs("visualizations", exist_ok=True)

# 1. User Study Visualization
# Load data
df = pd.read_csv('data/ttm-user-study-responses.csv', header=0, skiprows=[1,2])

cols = df.columns
q_easier = [c for c in cols if 'found the conversational interface easier to use' in c][0]
q_confident = [c for c in cols if 'more confident in my answers using the conversational' in c][0]
q_rapid = [c for c in cols if 'more rapidly arrive at an answer using the conversational' in c][0]
q_future = [c for c in cols if 'more likely to use the conversational' in c][0]

questions = {
    "Easier to Use": q_easier,
    "Faster to Answer": q_rapid,
    "Higher Confidence": q_confident,
    "Prefer for Future": q_future
}

agree_percentages = []
labels = list(questions.keys())

for short_name, col_name in questions.items():
    data = df[col_name].dropna()
    agree = (data >= 4).mean() * 100
    agree_percentages.append(agree)

# Plot User Study
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")
ax = sns.barplot(x=labels, y=agree_percentages, palette="viridis")

plt.ylim(0, 100)
plt.ylabel('% of Participants Who Agree', fontsize=12, fontweight='bold')
plt.title('User Preference: TalkToModel vs. Dashboard Baseline', fontsize=14, fontweight='bold', pad=15)

# Add text labels on top of bars
for i, v in enumerate(agree_percentages):
    ax.text(i, v + 2, f"{v:.1f}%", ha='center', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig('visualizations/user_study_results.png', dpi=300)
print("Saved User Study Visualization: visualizations/user_study_results.png")

# 2. Parsing Accuracy Visualization
accuracy_labels = ['T5-Small', 'T5-Base']
paper_accuracy = [66.8, 73.2]
replicated_accuracy = [68.06, 72.77]

x = np.arange(len(accuracy_labels))
width = 0.35

plt.figure(figsize=(8, 6))
fig, ax = plt.subplots(figsize=(8,6))
rects1 = ax.bar(x - width/2, paper_accuracy, width, label='Paper Reported', color='#1f77b4')
rects2 = ax.bar(x + width/2, replicated_accuracy, width, label='Our Replication', color='#ff7f0e')

ax.set_ylabel('Exact Match Accuracy (%)', fontweight='bold')
ax.set_title('Parsing Accuracy Validation (COMPAS)', fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(accuracy_labels, fontweight='bold')
ax.legend()
ax.set_ylim(0, 100)

for rects in [rects1, rects2]:
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/parsing_accuracy_comparison.png', dpi=300)
print("Saved Parsing Accuracy Visualization: visualizations/parsing_accuracy_comparison.png")
