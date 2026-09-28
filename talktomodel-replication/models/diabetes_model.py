import numpy as np
import pandas as pd
import pickle

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# Same seed used in the original TalkToModel code
np.random.seed(3)


# =========================
# 1. Load dataset
# =========================

X_values = pd.read_csv("data/diabetes.csv")

y_values = X_values.pop("y")


# =========================
# 2. Train / Test split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X_values,
    y_values,
    test_size=0.40
)


# =========================
# 3. Create model
# =========================

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", GradientBoostingClassifier())
])


# =========================
# 4. Train model
# =========================

model.fit(X_train, y_train)


# =========================
# 5. Evaluate model
# =========================

train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print("\n===== MODEL RESULTS =====")

print(f"Training accuracy: {train_score:.4f}")
print(f"Testing accuracy:  {test_score:.4f}")

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")


# =========================
# 6. Save model
# =========================

with open("models/diabetes_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nModel saved to:")
print("models/diabetes_model.pkl")