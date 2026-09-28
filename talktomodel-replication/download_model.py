from transformers import T5Tokenizer, T5ForConditionalGeneration
import os

def main():
    model_name = "ucinlp/diabetes-t5-small"
    save_dir = os.path.abspath("models/diabetes-t5-small")
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"Downloading {model_name} to {save_dir}...")
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    tokenizer.save_pretrained(save_dir)
    model.save_pretrained(save_dir)
    print("Download complete!")

if __name__ == "__main__":
    main()
