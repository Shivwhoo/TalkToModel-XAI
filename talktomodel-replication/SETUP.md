# Environment Setup

This project uses modern tools for reproducibility, but it relies on an older ecosystem to maintain compatibility with the authors' pickled models and legacy code.

## Virtual Environment Requirements
The code must be run inside a virtual environment. We use `uv` for fast dependency resolution.

To setup the environment, run:
```bash
# We use Python 3.10 to ensure compatibility with pre-compiled legacy packages.
uv venv --python=3.10 .venv
source .venv/bin/activate

# Install the exact frozen versions used during this replication
uv pip install -r requirements.txt
```

## Legacy Environment Notes
The authors' code (from ~2023) required freezing specific versions to avoid runtime and binary incompatibility errors:
- **Python 3.10**: Enforced as newer Python versions break legacy pre-compiled wheels.
- **numpy==1.21.6 & pandas==1.3.5**: Pinned to maintain binary compatibility with `dice-ml` and the authors' pickled `diabetes_model.pkl`.
- **Flask==2.0.3, Werkzeug==2.0.3, Jinja2==3.0.3**: Pinned to resolve import errors like `url_quote` and `Markup` which were deprecated and removed in newer versions.
- **Sentence-Transformers**: A dummy wrapper is used inside our scripts to avoid `huggingface-hub` API issues when loading the outdated model architecture.

## Running the Code
Once the environment is activated, you can reproduce all results by running:
```bash
./run_all.sh
```
