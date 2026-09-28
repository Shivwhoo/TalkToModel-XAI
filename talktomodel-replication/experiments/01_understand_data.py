import pandas as pd
import os

datasets = ["diabetes", "compas", "german"]

for dataset in datasets:
    path = f"data/{dataset}.csv"
    if not os.path.exists(path):
        # Fallback to external submodule for compas and german
        path = f"external/TalkToModel/data/{dataset}.csv"
        if not os.path.exists(path):
            print(f"Skipping {dataset}: not found.")
            continue

    print(f"\n======================================")
    print(f"      DATASET: {dataset.upper()}")
    print(f"======================================")
    
    df = pd.read_csv(path)

    print("\n===== FIRST 5 ROWS =====")
    print(df.head())

    print("\n===== SHAPE =====")
    print(df.shape)

    print("\n===== COLUMNS =====")
    print(df.columns.tolist())

    print("\n===== DATA TYPES =====")
    print(df.dtypes)

    if "y" in df.columns:
        print("\n===== TARGET DISTRIBUTION =====")
        print(df["y"].value_counts())
    
    print("\n===== BASIC STATISTICS =====")
    print(df.describe())