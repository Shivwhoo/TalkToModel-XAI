import pandas as pd
import torch

from transformers import T5Tokenizer, T5ForConditionalGeneration


# ==========================================
# 1. Configuration
# ==========================================

MODEL_NAME = "ucinlp/diabetes-t5-small"

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Device:", device)
print("Loading T5-small...")


# ==========================================
# 2. Load model
# ==========================================

tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)

model = T5ForConditionalGeneration.from_pretrained(
    MODEL_NAME
)

model = model.to(device)
model.eval()

print("Model loaded!")


# ==========================================
# 3. Load official diabetes dataset
# ==========================================

DATASET_PATH = "../TalkToModel/parsing/t5/datasets/diabetes_pandas.csv"

df = pd.read_csv(DATASET_PATH)

print("\n===== DATASET =====")
print("Total examples:", len(df))


# ==========================================
# 4. Prepare inputs
# ==========================================

instruction = "Convert the question into an SQL parse: "

questions = df["natural_language"].astype(str).tolist()
expected = df["parsed_utterance"].astype(str).str.lower().tolist()

inputs = [
    instruction + question
    for question in questions
]


# ==========================================
# 5. Generate predictions
# ==========================================

predictions = []

print("\n===== RUNNING T5 =====")

batch_size = 16

for start in range(0, len(inputs), batch_size):

    batch = inputs[start:start + batch_size]

    encoded = tokenizer(
        batch,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )

    input_ids = encoded["input_ids"].to(device)
    attention_mask = encoded["attention_mask"].to(device)

    with torch.no_grad():

        generated_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=150
        )

    batch_predictions = tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )

    predictions.extend(
        prediction.lower().strip()
        for prediction in batch_predictions
    )

    completed = min(
        start + batch_size,
        len(inputs)
    )

    print(
        f"Processed {completed}/{len(inputs)}"
    )


# ==========================================
# 6. Exact-match accuracy
# ==========================================

correct = sum(
    pred == true
    for pred, true in zip(predictions, expected)
)

total = len(expected)

accuracy = correct / total


# ==========================================
# 7. Results
# ==========================================

print("\n========================================")
print("T5-SMALL DIABETES PARSING RESULTS")
print("========================================")

print(f"Correct predictions : {correct}")
print(f"Total examples      : {total}")
print(f"Exact-match accuracy: {accuracy:.4f}")
print(f"Exact-match accuracy: {accuracy * 100:.2f}%")