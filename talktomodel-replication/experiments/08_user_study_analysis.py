import pandas as pd
import json
import os

def main():
    talktomodel_dir = os.environ.get("TALKTOMODEL_DIR", "external/TalkToModel")
    file_path = os.path.join(talktomodel_dir, 'data', 'ttm-user-study-responses.csv')
    
    if not os.path.exists(file_path):
        print(f"User study data not found at {file_path}. Skipping.")
        return
        
    df = pd.read_csv(file_path, header=0, skiprows=[1,2])
    
    cols = df.columns
    q_easier = [c for c in cols if 'found the conversational interface easier to use' in c][0]
    q_confident = [c for c in cols if 'more confident in my answers using the conversational' in c][0]
    q_rapid = [c for c in cols if 'more rapidly arrive at an answer using the conversational' in c][0]
    q_future = [c for c in cols if 'more likely to use the conversational' in c][0]

    questions = {
        "easier_to_use": q_easier,
        "faster_to_answer": q_rapid,
        "higher_confidence": q_confident,
        "prefer_for_future": q_future
    }

    results = {}
    for key, col_name in questions.items():
        data = df[col_name].dropna()
        agree_percentage = (data >= 4).mean() * 100
        results[key] = agree_percentage

    # Compare with paper's reported numbers
    paper_reported = {
        "easier_to_use": 86.2, # Approximated from charts/text
        "faster_to_answer": 86.2,
        "higher_confidence": 75.8,
        "prefer_for_future": 86.2
    }
    
    analysis = {
        "note": "This is a re-analysis of the authors' original user study data, not a new experiment.",
        "recalculated": results,
        "paper_reported": paper_reported,
        "matches_paper": all(abs(results[k] - paper_reported[k]) < 2.0 for k in results)
    }
    
    os.makedirs("results", exist_ok=True)
    with open("results/user_study_analysis.json", "w") as f:
        json.dump(analysis, f, indent=4)
    print("User study re-analysis saved to results/user_study_analysis.json")

if __name__ == "__main__":
    main()
