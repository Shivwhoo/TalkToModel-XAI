"""
Dataset Documentation & Sources

The datasets in this repository are derived from the authors' original 
TalkToModel repository (Slack et al., Nature Machine Intelligence 2023).

1. Diabetes Dataset:
   - Origin: UCI Machine Learning Repository (Pima Indians Diabetes Database)
   - Source in this project: Pulled directly from the original TalkToModel GitHub 
     repository (under `external/TalkToModel/data/`).
   - Files: `diabetes.csv` (full), `diabetes_train.csv` (training split), 
     `diabetes_test.csv` (held-out test split).

2. TTM User Study Responses:
   - Origin: Slack et al. User Study
   - Source: `external/TalkToModel/data/ttm-user-study-responses.csv`

Note: All required datasets are committed to the git repository either directly 
in the `data/` directory (for smaller datasets) or accessed dynamically through 
the `external/TalkToModel` git submodule. Thus, no external downloading logic 
is needed in this script.
"""

def main():
    print("All datasets are included via the `external/TalkToModel` submodule or in the `data/` folder.")
    print("No additional downloads are required.")

if __name__ == "__main__":
    main()
