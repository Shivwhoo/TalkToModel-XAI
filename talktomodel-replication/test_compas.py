import sys
import os

repo_path = os.path.abspath(os.path.expanduser('~/xai_project/TalkToModel'))
sys.path.append(repo_path)

import gin
from explain.logic import ExplainBot
from explain.conversation import fork_conversation

def main():
    dataset_name = "compas"
    model_file = f"{repo_path}/data/{dataset_name}_model_grad_boosted_tree.pkl"

    class_names = '{0: "likely to recidivate", 1: "unlikely to recidivate"}'
    
    config_string = f"""
# ExplainBot Params
ExplainBot.parsing_model_name = "/home/shivwhoo/xai_project/talktomodel-replication/models/{dataset_name}-t5-small"
ExplainBot.t5_config = "{repo_path}/parsing/t5/gin_configs/inference-t5-small.gin"
ExplainBot.seed = 0
ExplainBot.name = "{dataset_name}"
ExplainBot.model_file_path = "{model_file}"
ExplainBot.dataset_file_path = "{repo_path}/data/{dataset_name}_test.csv"
ExplainBot.background_dataset_file_path = "{repo_path}/data/{dataset_name}_test.csv"

ExplainBot.dataset_index_column = 0
ExplainBot.target_variable_name = "y"
ExplainBot.categorical_features = None
ExplainBot.numerical_features = None
ExplainBot.remove_underscores = True

# Conversation params
Conversation.class_names = {class_names}
"""
    gin.parse_config(config_string)

    import explain.prompts
    class DummySentenceTransformer:
        def __init__(self, *args, **kwargs): pass
        def encode(self, text, *args, **kwargs):
            import numpy as np
            return np.zeros(768)
    explain.prompts.SentenceTransformer = DummySentenceTransformer

    bot = ExplainBot(skip_prompts=True)
    demo_conversation = fork_conversation(bot.conversation, "demo_user")

    query = "filter id 5 and mistake sample [e]"
    try:
        result = bot.update_state(query, demo_conversation)
        print("Result:", result)
    except Exception as e:
        print("Error:", type(e), e)

if __name__ == "__main__":
    main()
