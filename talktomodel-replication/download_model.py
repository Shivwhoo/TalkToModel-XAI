from transformers import T5Tokenizer, T5ForConditionalGeneration
import os

def main():
    models = [
        "ucinlp/diabetes-t5-small",
        "ucinlp/german-t5-small",
        "ucinlp/compas-t5-small"
    ]
    for model_name in models:
        save_dir = os.path.abspath(f"models/{model_name.split('/')[-1]}")
        os.makedirs(save_dir, exist_ok=True)
        
        print(f"Downloading {model_name} to {save_dir}...")
        try:
            tokenizer = T5Tokenizer.from_pretrained(model_name)
            model = T5ForConditionalGeneration.from_pretrained(model_name)
            
            tokenizer.save_pretrained(save_dir)
            model.save_pretrained(save_dir)
            print(f"Download complete for {model_name}!")
        except Exception as e:
            print(f"Failed to download {model_name}: {e}")

if __name__ == "__main__":
    main()
