import pandas as pd
import torch

from transformers import T5Tokenizer, T5ForConditionalGeneration


# ==========================================
# 1. Model
# ==========================================

MODEL_NAME = "ucinlp/diabetes-t5-small"

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Device:", device)
print("Loading model...")


# ==========================================
# 2. Load tokenizer + model
# ==========================================

tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)

model = T5ForConditionalGeneration.from_pretrained(
    MODEL_NAME
)

model = model.to(device)
model.eval()

print("Model loaded!")


# ==========================================
# 3. Load official diabetes parsing dataset
# ==========================================

df = pd.read_csv(
    "../TalkToModel/parsing/t5/datasets/diabetes_pandas.csv"
)


# Take first example
question = df.loc[0, "natural_language"]
expected = df.loc[0, "parsed_utterance"]


# ==========================================
# 4. Use EXACT TalkToModel input format
# ==========================================

instruction = "Convert the question into an SQL parse: "

source_text = instruction + question


print("\n===== QUESTION =====")
print(question)

print("\n===== EXPECTED PARSE =====")
print(expected)

print("\n===== T5 INPUT =====")
print(source_text)


# ==========================================
# 5. Tokenize
# ==========================================

inputs = tokenizer(
    source_text,
    max_length=128,
    padding="max_length",
    truncation=True,
    return_tensors="pt"
)

input_ids = inputs["input_ids"].to(device)
attention_mask = inputs["attention_mask"].to(device)


# ==========================================
# 6. Generate prediction
# ==========================================

with torch.no_grad():

    generated_ids = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=150,
        early_stopping=True
    )


# ==========================================
# 7. Decode
# ==========================================

prediction = tokenizer.decode(
    generated_ids[0],
    skip_special_tokens=True,
    clean_up_tokenization_spaces=True
).lower()


# ==========================================
# 8. Compare
# ==========================================

print("\n===== T5 PREDICTION =====")
print(prediction)

print("\n===== EXACT MATCH =====")

if prediction == expected.lower():
    print("YES ✅")
    print("The prediction exactly matches the expected parse.")
else:
    print("NO ❌")
    print("Prediction and expected parse are different.")