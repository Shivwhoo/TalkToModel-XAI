# PowerShell Master Execution Script
# TalkToModel: Phase 1 Replication & Phase 2 Improvement Pipeline

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "   TalkToModel: Complete Replication & Phase 2 Improvement Pipeline    " -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan

# Set matplotlib config directory to local writable dir
$env:MPLCONFIGDIR = "$pwd\.matplotlib"

# Detect Python
$PYTHON_BIN = "python"
if (Test-Path ".\.venv\Scripts\python.exe") {
    try {
        $testOut = & ".\.venv\Scripts\python.exe" --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $PYTHON_BIN = ".\.venv\Scripts\python.exe"
        }
    } catch {}
}

Write-Host "Using Python: $PYTHON_BIN" -ForegroundColor Green

Write-Host "`n=== STEP 1: Phase 1 Parsing Accuracy Comparison ===" -ForegroundColor Yellow
& $PYTHON_BIN experiments/10_compare_accuracy.py

Write-Host "`n=== STEP 2: Phase 1 User Study Re-Analysis ===" -ForegroundColor Yellow
& $PYTHON_BIN experiments/08_user_study_analysis.py

Write-Host "`n=== STEP 3: Phase 1 Visualizations & Dashboard ===" -ForegroundColor Yellow
& $PYTHON_BIN experiments/09_generate_visualizations.py
& $PYTHON_BIN experiments/11_comprehensive_visualizations.py

Write-Host "`n=== STEP 4: Phase 2 Proposed Improvement Benchmark ===" -ForegroundColor Yellow
Write-Host "Running Dual-Explainer Consensus & Faithfulness Evaluation..."
& $PYTHON_BIN experiments/13_evaluate_consensus_improvement.py

Write-Host "`n=== STEP 5: Phase 2 Visualizations & Master Dashboard ===" -ForegroundColor Yellow
& $PYTHON_BIN experiments/14_generate_phase2_visualizations.py

Write-Host "`n=== STEP 6: Auto-Generate Consolidated Results Tables ===" -ForegroundColor Yellow
& $PYTHON_BIN experiments/12_generate_markdown_tables.py

Write-Host "`n========================================================================" -ForegroundColor Cyan
Write-Host "   All Phase 1 and Phase 2 Pipeline Steps Completed Successfully!      " -ForegroundColor Cyan
Write-Host "   Outputs generated in results/ and visualizations/ directories.       " -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
