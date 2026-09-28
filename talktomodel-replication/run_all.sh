#!/bin/bash
set -e

echo "========================================================="
echo "   TalkToModel Replication - Complete Run Script         "
echo "========================================================="

export TALKTOMODEL_DIR="external/TalkToModel"
PYTHON_BIN="../TalkToModel/.venv-legacy/bin/python"

if [ ! -d "$TALKTOMODEL_DIR" ]; then
    echo "ERROR: Submodule external/TalkToModel not found."
    echo "Please run: git submodule update --init"
    exit 1
fi

if [ ! -f "$PYTHON_BIN" ]; then
    echo "ERROR: Virtual environment not found at ../TalkToModel/.venv-legacy"
    echo "Please create it and install requirements."
    exit 1
fi

# echo "1. Understand Data..."
# $PYTHON_BIN experiments/01_understand_data.py || echo "Warning: 01_understand_data.py failed."

# echo "2. Run test t5 (legacy)..."
# $PYTHON_BIN experiments/02_test_t5.py || echo "Warning: 02_test_t5.py failed."

# echo "3. Run test inference..."
# $PYTHON_BIN experiments/03_test_t5_inference.py || echo "Warning: 03_test_t5_inference.py failed."

# echo "4. Evaluate Parsing - Diabetes - T5 Small"
# .venv/bin/python experiments/04_evaluate_t5_diabetes.py --dataset diabetes --model /home/shivwhoo/xai_project/talktomodel-replication/models/diabetes-t5-small

# echo "4. Evaluate Parsing - Diabetes - T5 Base"
# T5-Base is not available on HuggingFace under ucinlp. Skip or run if we somehow find it.
# $PYTHON_BIN experiments/04_evaluate_t5_diabetes.py --dataset diabetes --model ucinlp/diabetes-t5-base

# echo "5. Latency Experiment (New)"
# $PYTHON_BIN experiments/05_latency_experiment.py

echo "6. Explanation Quality Comparison (New)"
$PYTHON_BIN experiments/06_explanation_quality.py

echo "7. End-to-End Test (Sample input automatically provided for verification, if modified to take it, otherwise skip or run automatically)"
# For automated runs, we skip 07 as it's interactive.
# echo "exit" | $PYTHON_BIN experiments/07_end_to_end_talktomodel_diabetes.py

echo "8. User Study Re-Analysis (New)"
$PYTHON_BIN experiments/08_user_study_analysis.py

echo "9. Generate Visualizations"
$PYTHON_BIN experiments/09_generate_visualizations.py

echo "10. Compare Accuracy"
$PYTHON_BIN experiments/10_compare_accuracy.py

echo "11. Comprehensive Visualizations"
$PYTHON_BIN experiments/11_comprehensive_visualizations.py

echo "========================================================="
echo "   All automated scripts completed successfully!         "
echo "========================================================="
echo '12. Generate Markdown Tables'
$PYTHON_BIN experiments/12_generate_markdown_tables.py
