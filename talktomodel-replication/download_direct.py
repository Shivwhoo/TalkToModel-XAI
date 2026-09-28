import os
import urllib.request

models = ["ucinlp/german-t5-small", "ucinlp/compas-t5-small"]
files = ["config.json", "pytorch_model.bin", "special_tokens_map.json", "spiece.model", "tokenizer_config.json"]

for m in models:
    dir_name = f"models/{m.split('/')[-1]}"
    os.makedirs(dir_name, exist_ok=True)
    for f in files:
        url = f"https://huggingface.co/{m}/resolve/main/{f}"
        dest = os.path.join(dir_name, f)
        print(f"Downloading {url} to {dest}")
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            print(f"Failed to download {f} for {m}: {e}")

