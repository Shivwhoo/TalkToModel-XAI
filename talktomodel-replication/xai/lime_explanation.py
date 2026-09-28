import pickle
import pandas as pd

from lime.lime_tabular import LimeTabularExplainer


# ==========================================
# 1. Load trained model
# ==========================================

with open("models/diabetes_model.pkl", "rb") as f:
    model = pickle.load(f)


# ==========================================
# 2. Load training data
# ==========================================

train_df = pd.read_csv("data/diabetes_train.csv")


# EXACT 8 features used by the model
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


# ==========================================
# 3. Create LIME explainer
# ==========================================

explainer = LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=feature_columns,
    class_names=[
        "unlikely to have diabetes",
        "likely to have diabetes"
    ],
    mode="classification",
    random_state=3
)


# ==========================================
# 4. Select one person
# ==========================================

person = X_train.iloc[0]


print("\n===== PERSON =====")
print(person)


# ==========================================
# 5. Prediction function
# ==========================================

def predict_fn(data):
    """
    LIME gives us a NumPy array.
    Convert it back into a DataFrame so that
    the model receives the same feature names
    it saw during training.
    """

    data = pd.DataFrame(
        data,
        columns=feature_columns
    )

    return model.predict_proba(data)


# ==========================================
# 6. Get model prediction
# ==========================================

prediction = model.predict(person.to_frame().T)[0]

probabilities = model.predict_proba(
    person.to_frame().T
)[0]


print("\n===== MODEL PREDICTION =====")

if prediction == 0:
    print("Prediction: unlikely to have diabetes")
else:
    print("Prediction: likely to have diabetes")


print("\n===== PREDICTION PROBABILITIES =====")

print(f"Class 0: {probabilities[0]:.4f}")
print(f"Class 1: {probabilities[1]:.4f}")


# ==========================================
# 7. Generate LIME explanation
# ==========================================

explanation = explainer.explain_instance(
    person.values,
    predict_fn,
    num_features=8
)


# ==========================================
# 8. Print explanation
# ==========================================

print("\n===== LIME EXPLANATION =====")

for feature, weight in explanation.as_list():
    print(f"{feature:40s} {weight:+.4f}")