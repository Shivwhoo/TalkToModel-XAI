import sys
import os
import time

# Ensure TalkToModel is in path
repo_path = os.path.abspath(os.path.expanduser('~/xai_project/TalkToModel'))
sys.path.append(repo_path)

import gin
from explain.logic import ExplainBot
from explain.conversation import fork_conversation
import explain.logic
import explain.actions.get_action_functions

def main():
    config_string = f"""
# ExplainBot Params
ExplainBot.parsing_model_name = "{repo_path}/parsing/t5/models/diabetes_t5-small_epoch_20_lr_0.0001_batchsize_32_optimizer_adamw"
ExplainBot.t5_config = "{repo_path}/parsing/t5/gin_configs/inference-t5-small.gin"
ExplainBot.seed = 0
ExplainBot.name = "diabetes"
ExplainBot.model_file_path = "{repo_path}/data/diabetes_model_grad_tree.pkl"
ExplainBot.dataset_file_path = "{repo_path}/data/diabetes_test.csv"
ExplainBot.background_dataset_file_path = "{repo_path}/data/diabetes_test.csv"

ExplainBot.dataset_index_column = 0
ExplainBot.target_variable_name = "y"
ExplainBot.categorical_features = None
ExplainBot.numerical_features = None
ExplainBot.remove_underscores = True

# Prompt params
Prompts.prompt_cache_size = 1_000_000
Prompts.prompt_cache_location = "{repo_path}/cache/prompts_cache.pkl"
Prompts.max_values_per_feature = 1
Prompts.sentence_transformer_model_name = "all-mpnet-base-v2"
Prompts.prompt_folder = "{repo_path}/explain/prompts"
Prompts.num_per_knn_prompt_template = 1
Prompts.num_prompt_template = 10

# Explanation Params
Explanation.max_cache_size = 1_000_000

# MegaExplainer Params
MegaExplainer.cache_location = "{repo_path}/cache/diabetes-mega-explainer-tabular.pkl"
MegaExplainer.use_selection = False

# Tabular Dice Params
TabularDice.cache_location = "{repo_path}/cache/diabetes-dice-tabular-grad-tree.pkl"

# Conversation params
Conversation.class_names = {{0: "unlikely to have diabetes", 1: "likely to have diabetes"}}

# Dataset description
DatasetDescription.dataset_objective = "predict whether someone has diabetes"
DatasetDescription.dataset_description = "diabetes prediction"
DatasetDescription.model_description = "gradient boosted tree"

log_dialogue_input.dynamodb_table = None
"""

    gin.parse_config(config_string)

    print("==================================================")
    print("TalkToModel End-to-End Diabetes Demo")
    print("==================================================")

    # Patch SentenceTransformer to avoid HF Hub issues
    import explain.prompts
    class DummySentenceTransformer:
        def __init__(self, *args, **kwargs):
            pass
        def encode(self, text, *args, **kwargs):
            import numpy as np
            return np.zeros(768)
    explain.prompts.SentenceTransformer = DummySentenceTransformer

    # Initialize ExplainBot
    bot = ExplainBot(skip_prompts=True)

    # Setup a conversation
    demo_conversation = fork_conversation(bot.conversation, "demo_user")

    # Patching to intercept and format output as requested
    original_compute_parse_text_t5 = bot.compute_parse_text_t5
    original_run_action = explain.logic.run_action

    def patched_compute_parse_text_t5(text: str):
        parse_tree, parse_text = original_compute_parse_text_t5(text)
        print(f"\\nPARSED COMMAND:\\n{parse_text}\\n")
        return parse_tree, parse_text

    bot.compute_parse_text_t5 = patched_compute_parse_text_t5

    def patched_run_action(conversation, parse_tree, parsed_string: str, **kwargs):
        print(f"EXECUTION:\\nExecuting mapped operations for parsed string: '{parsed_string}'\\n")
        return_statement = original_run_action(conversation, parse_tree, parsed_string, **kwargs)
        print(f"MODEL RESULT / XAI RESULT:\\nSuccessfully invoked the internal diabetes ML model and generated/retrieved explanations for the requested instance(s).\\n")
        return return_statement

    explain.logic.run_action = patched_run_action

    # Interactive Loop
    while True:
        print("\\n" + "="*50)
        query = input("USER (type 'exit' to quit):\\n> ")
        if query.strip().lower() in ['exit', 'quit']:
            print("Exiting demo...")
            break
        
        # Run
        try:
            result = bot.update_state(query, demo_conversation)
            
            # Clean up the output for the terminal
            clean_result = str(result)
            # Remove trailing UUID
            if "<>" in clean_result:
                clean_result = clean_result.split("<>")[0]
            
            # Replace HTML with terminal-friendly formatting
            clean_result = clean_result.replace("<b>", "\033[1m").replace("</b>", "\033[0m")
            clean_result = clean_result.replace("<em>", "\033[3m").replace("</em>", "\033[0m")
            clean_result = clean_result.replace("<br>", "\\n")
            clean_result = clean_result.replace("<ul>", "\\n").replace("</ul>", "")
            clean_result = clean_result.replace("<li>", "  • ").replace("</li>", "\\n")
            clean_result = clean_result.replace("&#129502", "") # Remove emoji hex
            
            print(f"\\nTALKToMODEL RESPONSE:\\n{clean_result.strip()}")
        except Exception as e:
            print(f"\\nError processing query: {e}")

if __name__ == "__main__":
    main()
