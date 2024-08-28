import os

import google.generativeai as genai
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
from rich.progress import track
import time
from finetuning.load_dataset import read_ds_file


def fine_tune_gemini(train_data_path):
    # for model_info in genai.list_tuned_models():
    #     print(model_info.name)

    base_model = "models/gemini-1.5-flash-001-tuning"
    raw_training_data = read_ds_file(train_data_path)
    training_data = [{"text_input": conv["input"], "output": conv["output"]} for conv in
                     track(raw_training_data, description="Processing data")]

    operation = genai.create_tuned_model(
        # You can use a tuned model here too. Set `source_model="tunedModels/..."`
        id="factest-reasoning-v1",
        display_name="factest-reasoning-v1-",
        source_model=base_model,
        epoch_count=1,
        batch_size=3,
        learning_rate=0.001,
        training_data=training_data,
    )

    for status in operation.wait_bar():
        time.sleep(5)

    result = operation.result()
    print(result)
    # # You can plot the loss curve with:
    snapshots = pd.DataFrame(result.tuning_task.snapshots)
    sns.lineplot(data=snapshots, x='epoch', y='mean_loss')

    model = genai.GenerativeModel(model_name=result.name)
    result = model.generate_content("III")
    print(result.text)  # IV


if __name__ == '__main__':
    fine_tune_gemini("datasets/mixed_ds_400.json")
