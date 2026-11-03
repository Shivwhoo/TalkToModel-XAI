#!/bin/bash
set -e

echo "========================================================================"
echo "   TalkToModel: Complete Replication & Phase 2 Improvement Pipeline    "
echo "========================================================================"

export MPLCONFIGDIR="$(pwd)/.matplotlib"

# Auto-detect working Python executable
PYTHON_BIN="python"
if [ -f ".venv/bin/python" ] && .venv/bin/python --version >/dev/null 2>&1; then
    PYTHON_BIN=".venv/bin/python"
elif [ -f ".venv/Scripts/python.exe" ] && .venv/Scripts/python.exe --version >/dev/null 2>&1; then
    PYTHON_BIN=".venv/Scripts/python.exe"
fi

echo "Using Python executable: $PYTHON_BIN"

echo ""
echo "=== STEP 1: Phase 1 Parsing Accuracy Comparison ==="
$PYTHON_BIN experiments/10_compare_accuracy.py

echo ""
echo "=== STEP 2: Phase 1 User Study Re-Analysis ==="
$PYTHON_BIN experiments/08_user_study_analysis.py

echo ""
echo "=== STEP 3: Phase 1 Visualizations & Dashboard ==="
$PYTHON_BIN experiments/09_generate_visualizations.py
$PYTHON_BIN experiments/11_comprehensive_visualizations.py

echo ""
echo "=== STEP 4: Phase 2 Proposed Improvement Benchmark ==="
echo "Running Dual-Explainer Consensus & Faithfulness Evaluation across datasets..."
$PYTHON_BIN experiments/13_evaluate_consensus_improvement.py

echo ""
echo "=== STEP 5: Phase 2 Visualizations & Master Dashboard ==="
$PYTHON_BIN experiments/14_generate_phase2_visualizations.py

echo ""
echo "=== STEP 6: Auto-Generate Consolidated Results Tables ==="
$PYTHON_BIN experiments/12_generate_markdown_tables.py

echo ""
echo "========================================================================"
echo "   All Phase 1 and Phase 2 Pipeline Steps Completed Successfully!      "
echo "   Outputs generated in results/ and visualizations/ directories.       "
echo "========================================================================"
