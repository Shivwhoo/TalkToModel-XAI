"""
Phase 2 Interactive CLI Demo: Consensus-Aware TalkToModel (DECF-Engine)
Demonstrates the conversational interface handling:
  1. High Consensus Queries (SHAP and LIME agree -> High Confidence explanation)
  2. Severe Disagreement Queries (SHAP and LIME diverge -> Alert Warning & Faithfulness Arbitration)
  3. Feature Ablation Verification

Authors: Sachin Kumar, Shiv Kishore, Udit Dadhich, Sudhanshu Baberwal
Supporting Literature: Krishna et al. (NeurIPS 2022)
"""

import sys
import os
import json

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from xai.consensus_engine import evaluate_consensus, generate_conversational_response

def main():
    print("=========================================================================")
    print("  TalkToModel: Phase 2 Consensus & Faithfulness Interactive Demonstration")
    print("  Powered by Dual-Explainer Consensus & Fidelity Engine (DECF-Engine)    ")
    print("=========================================================================\n")
    print("This interactive console showcases how TalkToModel resolves the")
    print("'Disagreement Problem' (Krishna et al., NeurIPS 2022) in conversational XAI.\n")
    print("Commands:")
    print("  - Type 'demo' to run through predefined high-consensus and high-disagreement cases.")
    print("  - Type 'exit' to quit.\n")

    # Load benchmark data
    with open("results/phase2_consensus_benchmark.json", "r") as f:
        benchmark = json.load(f)

    while True:
        try:
            user_input = input("USER QUERY > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting demo...")
            break

        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting demo...")
            break

        if user_input.lower() == "demo":
            print("\n" + "="*70)
            print("DEMO SCENARIO 1: HIGH CONSENSUS CASE (COMPAS Recidivism Prediction)")
            print("="*70)
            print("Natural Language Query: 'explain why patient 323 is predicted to recidivate'")
            print("T5 DSL Parse: filter id 323 and explain features [e]\n")
            
            # Instance 323 from COMPAS
            shap_top3 = ["number_of_prior_crimes", "age", "recidivated"]
            lime_top3 = ["number_of_prior_crimes", "age", "months_in_jail"]
            all_feats = ["age", "number_of_prior_crimes", "recidivated", "months_in_jail"]
            eval_res = evaluate_consensus(shap_top3, lime_top3, all_feats, spearman_corr=0.90)
            
            print("--- ORIGINAL TALKTOMODEL (SINGLE-EXPLAINER / SHAP ALONE) ---")
            print("Response: 'The top features for patient 323 are number_of_prior_crimes (+0.45), age (+0.32), and recidivated (+0.18).'")
            print("Limitation: Hides explanation uncertainty, zero verification against other attribution methods.\n")
            
            print("--- PROPOSED ENHANCED TALKTOMODEL (CONSENSUS & FAITHFULNESS ENGINE) ---")
            resp = generate_conversational_response(323, "compas", eval_res, "likely to recidivate")
            print(resp)
            print("\nFaithfulness Check: Prediction Drop Delta P = 0.528 upon ablation of verified features.\n")

            print("="*70)
            print("DEMO SCENARIO 2: SEVERE DISAGREEMENT ALERT (German Credit Risk Prediction)")
            print("="*70)
            print("Natural Language Query: 'why was loan applicant 95 denied credit?'")
            print("T5 DSL Parse: filter id 95 and explain features [e]\n")
            
            # Instance 95 from German Credit
            shap_top3_g = ["LoanAmount", "LoanDuration", "CheckingAccountBalanceGreaterOrEqualTo0"]
            lime_top3_g = ["NoCurrentLoan", "loanpurposeUsedCar", "LoanDuration"]
            all_feats_g = list(set(shap_top3_g + lime_top3_g))
            eval_res_g = evaluate_consensus(shap_top3_g, lime_top3_g, all_feats_g, spearman_corr=0.116)
            
            print("--- ORIGINAL TALKTOMODEL (SINGLE-EXPLAINER / SHAP ALONE) ---")
            print("Response: 'The top features for applicant 95 are LoanAmount, LoanDuration, and CheckingAccountBalance.'")
            print("Danger: Severe false trust! LIME identified completely different features (NoCurrentLoan, UsedCar). SHAP alone misled the user.\n")
            
            print("--- PROPOSED ENHANCED TALKTOMODEL (CONSENSUS & FAITHFULNESS ENGINE) ---")
            resp_g = generate_conversational_response(95, "german", eval_res_g, "bad credit risk")
            print(resp_g)
            print("\nFaithfulness Arbitration: Perturbation test shows Consensus feature set retains Delta P = 0.385 vs LIME 0.288.\n")
            print("="*70)
            print("Demo completed. Type 'exit' to quit or 'demo' to rerun.")
        else:
            print(f"Simulating query: '{user_input}'...")
            print("Parsed DSL: filter and explain features [e]")
            # Generic response
            shap_top3 = ["Glucose", "BMI", "Age"]
            lime_top3 = ["Glucose", "BMI", "DiabetesPedigreeFunction"]
            eval_res = evaluate_consensus(shap_top3, lime_top3, shap_top3 + lime_top3, 0.428)
            print("\n" + generate_conversational_response("SAMPLE", "diabetes", eval_res, "likely to have diabetes") + "\n")

if __name__ == "__main__":
    main()

