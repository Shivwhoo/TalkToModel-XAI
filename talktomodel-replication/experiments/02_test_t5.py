from transformers import T5Tokenizer, T5ForConditionalGeneration


MODEL_NAME = "ucinlp/diabetes-t5-small"


print("Loading tokenizer...")

tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)

print("Loading T5 model...")

model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

print("Model loaded successfully!")
print("Model:", MODEL_NAME)