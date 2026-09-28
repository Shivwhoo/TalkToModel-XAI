import os
from huggingface_hub import snapshot_download

models = ['ucinlp/german-t5-small', 'ucinlp/compas-t5-small']
for m in models:
    save_dir = os.path.abspath(f"models/{m.split('/')[-1]}")
    snapshot_download(repo_id=m, local_dir=save_dir)
