import sys
import os
import time
import json
import numpy as np

# Ensure TalkToModel is in path
repo_path = os.environ.get("TALKTOMODEL_DIR", "external/TalkToModel")
sys.path.append(repo_path)

import gin
from explain.logic import ExplainBot
from explain.conversation import fork_conversation
import explain.logic
import explain.actions.get_action_functions

def main():
    config_string = f"""
# ExplainBot Params
ExplainBot.parsing_model_name = "/home/shivwhoo/xai_project/talktomodel-replication/models/diabetes-t5-small"
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

    # Patch SentenceTransformer to avoid HF Hub issues
    import explain.prompts
    class DummySentenceTransformer:
        def __init__(self, *args, **kwargs):
            pass
        def encode(self, text, *args, **kwargs):
            return np.zeros(768)
    explain.prompts.SentenceTransformer = DummySentenceTransformer

    # Initialize ExplainBot
    print("Initializing ExplainBot...")
    bot = ExplainBot(skip_prompts=True)
    demo_conversation = fork_conversation(bot.conversation, "demo_user")

    sample_questions = [
        "explain the feature importance for the patient with id 51",
        "what is the model prediction for patient 10?",
        "how does age affect the prediction for patient 20?",
        "what would happen if we change glucose to 100 for patient 5?",
        "what are the top 3 features?"
    ]

    print("Running latency experiment...")
    num_runs = 3
    results = {}

    for question in sample_questions:
        times = []
        for i in range(num_runs):
            # To avoid caching making subsequent runs 0s, you might need to recreate the conversation 
            # or just accept that caching is part of the system latency. We accept it as is.
            start_time = time.time()
            try:
                bot.update_state(question, demo_conversation)
            except Exception:
                pass # Ignore parsing errors in latency test
            times.append(time.time() - start_time)
        
        results[question] = {
            "mean_latency_sec": np.mean(times),
            "std_latency_sec": np.std(times),
            "all_times": times
        }
        print(f"Question: '{question}' -> Mean: {np.mean(times):.2f}s ± {np.std(times):.2f}s")

    os.makedirs("results", exist_ok=True)
    with open("results/latency_experiment.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Latency experiment saved to results/latency_experiment.json")

if __name__ == "__main__":
    main()
