import base64
import json

import PIL.Image
import google.generativeai as genai

import os

from groq import Groq
from dotenv import load_dotenv
from rich.progress import TimeElapsedColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, \
    SpinnerColumn
from rich.table import Column
from supabase import create_client, Client
from supafunc.errors import FunctionsHttpError, FunctionsRelayError


def get_example_prompt():
    return """"""


def test_gemini_supabase():
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    with open("/home/erik/FACTEST/+LLM/envs/plots/2D Box Environment.png", mode='rb') as file:
        img = file.read()

    response = supabase.functions.invoke(
        "prompt",
        invoke_options={
            "headers": {
                "Content-Type": "application/json",
                "x-region": "us-west-1",
            },
            "body": {
                "secret": "ButtrFly",
                "prompt": "Hello, world! What do you see",
                "model": "gemini-1.5-flash",
                # "img": base64.b64encode(img).decode('utf-8')

            }
        }
    )
    print(json.loads(response))
    print(json.loads(response)["text"])
    # print(json.loads(response)["candidates"][0]["content"]["parts"][0]["text"])
    # print(response["candidates"][0]["content"]["parts"][0]["text"])


def test_groq():
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="llama-3.1-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)


def random_test():
    from rich.progress import Progress
    from time import sleep
    # Initial lists
    successfuls = [True, False, True, False, True]
    num_iterations_needed = [10, -1, 5, -1, 15]

    # Original filtering operation
    successfuls_filtered = [successfuls[i] for i in range(len(successfuls)) if num_iterations_needed[i] != -1]
    num_iterations_needed_filtered = [num_iterations_needed[i] for i in range(len(num_iterations_needed)) if
                                      num_iterations_needed[i] != -1]

    print("Original filtering approach:")
    print("Filtered successfuls:", successfuls_filtered)
    print("Filtered num_iterations_needed:", num_iterations_needed_filtered)

    # Optimized approach using zip
    paired_lists = list(zip(successfuls, num_iterations_needed))
    filtered_pairs = [(success, iterations) for success, iterations in paired_lists if iterations != -1]

    successfuls_optimized, num_iterations_needed_optimized = zip(*filtered_pairs)
    successfuls_optimized = list(successfuls_optimized)
    num_iterations_needed_optimized = list(num_iterations_needed_optimized)

    print("\nOptimized filtering approach:")
    print("Filtered successfuls:", successfuls_optimized)
    print("Filtered num_iterations_needed:", num_iterations_needed_optimized)

    # Verify that both approaches give the same result
    print("\nVerification:")
    print("Both approaches produce the same result:",
          successfuls_filtered == successfuls_optimized and num_iterations_needed_filtered == num_iterations_needed_optimized)

    with Progress(SpinnerColumn(spinner_name="simpleDots"),
                  TextColumn("[progress.description]{task.description}", table_column=Column(ratio=1)),
                  BarColumn(table_column=Column(ratio=1)),
                  TaskProgressColumn(table_column=Column(ratio=1)),
                  TimeRemainingColumn(table_column=Column(ratio=1)), TimeElapsedColumn(table_column=Column(ratio=1)),
                  refresh_per_second=3,
                  speed_estimate_period=600) as pb:
        t1 = pb.add_task('inner', total=10)
        t2 = pb.add_task('outer', total=100)

        for i in range(100):
            for j in range(10):
                print(f"Verbose info! {i, j}")
                sleep(10)
                pb.update(task_id=t1, completed=j + 1, refresh=True)
            pb.update(task_id=t2, completed=i + 1, refresh=True)


if __name__ == "__main__":
    # random_test()
    test_gemini_supabase()
# test_groq()
