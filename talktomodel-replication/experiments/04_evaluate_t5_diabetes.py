import os
import sys
import json
import argparse
import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from sklearn.model_selection import train_test_split

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True, help="Name of the dataset (e.g., diabetes)")
    parser.add_argument("--model", type=str, required=True, help="Hugging Face model ID (e.g., ucinlp/diabetes-t5-small)")
    args = parser.parse_args()

    os.makedirs("results", exist_ok=True)
    out_file = f"results/parsing_{args.dataset}_{args.model.replace('/', '_')}.json"

    device = "cpu"
    print(f"Loading {args.model} on {device}...")

    try:
        tokenizer = T5Tokenizer.from_pretrained(args.model)
        model = T5ForConditionalGeneration.from_pretrained(args.model)
        model = model.to(device)
        model.eval()
    except Exception as e:
        print(f"Failed to load model {args.model}: {e}")
        with open(out_file, "w") as f:
            json.dump({"model": args.model, "dataset": args.dataset, "error": str(e)}, f, indent=4)
        sys.exit(0)

    # Load dataset
    talktomodel_dir = os.environ.get("TALKTOMODEL_DIR", "external/TalkToModel")
    dataset_path = os.path.join(talktomodel_dir, "parsing", "t5", "datasets", f"{args.dataset}_pandas.csv")
    if not os.path.exists(dataset_path):
        print(f"Dataset not found: {dataset_path}")
        sys.exit(1)

    df = pd.read_csv(dataset_path)
    
    # Create fixed held-out test split (20%)
    _, test_df = train_test_split(df, test_size=0.2, random_state=42)
    print(f"Loaded {len(test_df)} test examples from {args.dataset}")

    instruction = "Convert the question into an SQL parse: "
    questions = test_df["natural_language"].astype(str).tolist()
    expected = test_df["parsed_utterance"].astype(str).str.lower().tolist()

    inputs = [instruction + q for q in questions]
    predictions = []
    batch_size = 16

    print("Running inference...")
    for start in range(0, len(inputs), batch_size):
        batch = inputs[start:start + batch_size]
        encoded = tokenizer(batch, max_length=128, padding="max_length", truncation=True, return_tensors="pt")
        input_ids = encoded["input_ids"].to(device)
        attention_mask = encoded["attention_mask"].to(device)

        with torch.no_grad():
            generated_ids = model.generate(input_ids=input_ids, attention_mask=attention_mask, max_length=150)

        batch_predictions = tokenizer.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        predictions.extend(p.lower().strip() for p in batch_predictions)

    correct = sum(p == t for p, t in zip(predictions, expected))
    accuracy = correct / len(expected)

    results = {
        "model": args.model,
        "dataset": args.dataset,
        "test_size": len(expected),
        "correct": correct,
        "accuracy": accuracy,
        "predictions": [{"question": q, "expected": t, "predicted": p, "match": p == t} for q, t, p in zip(questions, expected, predictions)]
    }

    with open(out_file, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Finished. Exact-match accuracy: {accuracy*100:.2f}%")

if __name__ == "__main__":
    main()
