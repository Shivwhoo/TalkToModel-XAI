import pickle
import pandas as pd
import matplotlib.pyplot as plt

from lime.lime_tabular import LimeTabularExplainer


# Load model
with open("models/diabetes_model.pkl", "rb") as f:
    model = pickle.load(f)


# Load training data
train_df = pd.read_csv("data/diabetes_train.csv")

feature_columns = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
]

X_train = train_df[feature_columns]


# LIME explainer
explainer = LimeTabularExplainer(
    X_train.values,
    feature_names=feature_columns,
    class_names=[
        "unlikely to have diabetes",
        "likely to have diabetes"
    ],
    mode="classification",
    random_state=3
)


# Select same person
person = X_train.iloc[0]


# Prediction function
def predict_fn(data):
    data = pd.DataFrame(data, columns=feature_columns)
    return model.predict_proba(data)


# Generate explanation
explanation = explainer.explain_instance(
    person.values,
    predict_fn,
    num_features=8
)


# Get feature names and weights
items = explanation.as_list()

features = [item[0] for item in items]
weights = [item[1] for item in items]


# Create figure
plt.figure(figsize=(10, 6))

plt.barh(features, weights)

plt.axvline(0, linewidth=1)

plt.xlabel("LIME Weight")
plt.ylabel("Feature condition")

plt.title(
    "LIME Explanation — Diabetes Prediction"
)

plt.tight_layout()


# Save figure
plt.savefig(
    "results/figures/lime_diabetes_explanation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nFigure saved to:")
print("results/figures/lime_diabetes_explanation.png")