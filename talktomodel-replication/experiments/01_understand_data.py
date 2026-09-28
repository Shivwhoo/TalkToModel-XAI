import pandas as pd

# Load the exact dataset used by TalkToModel
df = pd.read_csv("data/diabetes.csv")

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== SHAPE =====")
print(df.shape)

print("\n===== COLUMNS =====")
print(df.columns.tolist())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== TARGET DISTRIBUTION =====")
print(df["y"].value_counts())

print("\n===== BASIC STATISTICS =====")
print(df.describe())