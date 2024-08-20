import base64
import json
from time import strftime, gmtime

import PIL.Image
import polytope as pc
import numpy as np
import vertexai
from matplotlib import pyplot as plt
from scipy.spatial import ConvexHull
from vertexai.generative_models import GenerativeModel

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
    # url: str = os.environ.get("SUPABASE_URL")
    # key: str = os.environ.get("SUPABASE_KEY")
    # supabase: Client = create_client(url, key)
    #
    # with open("/home/erik/FACTEST/+LLM/envs/plots/2D Box Environment.png", mode='rb') as file:
    #     img = file.read()
    #
    # response = supabase.functions.invoke(
    #     "prompt",
    #     invoke_options={
    #         "headers": {
    #             "Content-Type": "application/json",
    #             "x-region": "us-west-1",
    #         },
    #         "body": {
    #             "secret": "ButtrFly",
    #             "prompt": "Hello, world! What do you see",
    #             "model": "gemini-1.5-flash",
    #             # "img": base64.b64encode(img).decode('utf-8')
    #
    #         }
    #     }
    # )
    # print(json.loads(response))
    # print(json.loads(response)["text"])
    # print(json.loads(response)["candidates"][0]["content"]["parts"][0]["text"])
    # print(response["candidates"][0]["content"]["parts"][0]["text"])
    # project_id = "PROJECT_ID

    vertexai.init(project="gentle-keyword-432706-b3", location="europe-west3")

    model = GenerativeModel("gemini-1.5-flash-001")

    response = model.generate_content(
        "What's a good name for a flower shop that specializes in selling bouquets of dried flowers?"
    )

    print(response.text)


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


def test_chatgpt():
    from openai import OpenAI
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Hello Chat."
            }
        ]
    )

    print(completion.choices[0].message.content)


def test_claude():
    from anthropic import Anthropic
    load_dotenv()
    client = Anthropic(
        # This is the default and can be omitted
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-3-haiku-20240307",
    )
    print(message.content[0].text)


def random_test():
    from rich.progress import Progress
    from time import sleep

    with Progress(SpinnerColumn(spinner_name="simpleDots"),
                  TextColumn("[progress.description]{task.description}", table_column=Column(ratio=1)),
                  BarColumn(table_column=Column(ratio=1)),
                  TaskProgressColumn(table_column=Column(ratio=1)),
                  TimeRemainingColumn(table_column=Column(ratio=1)), TimeElapsedColumn(table_column=Column(ratio=1)),
                  refresh_per_second=3,
                  speed_estimate_period=600) as pb:
        t1 = pb.add_task('inner', total=10)
        t2 = pb.add_task('outer', total=10)

        # random Polytope with random rotation
        A = np.random.rand(4, 2)
        b_init = np.random.rand(4)
        Theta = pc.Polytope(A, b_init)
        print(Theta)
        print(Theta.vertices)

        for i in range(10):
            for j in range(10):
                print(f"Verbose info! {i, j}")
                sleep(0.01)
                pb.update(task_id=t1, completed=j + 1, refresh=True)
            pb.update(task_id=t2, completed=i + 1, refresh=True)
        elapsed = pb.tasks[1].elapsed
        s_time = strftime("%Hh:%Mm:%Ss", gmtime(elapsed))
        print(s_time)


def generate_convex_hull_vertices(n=4, lower_bound=-10, upper_bound=10):
    while True:
        # Generate random points
        points = np.random.uniform(lower_bound, upper_bound, (n, 2))

        # Compute the convex hull
        hull = ConvexHull(points)

        # Check if the convex hull has 4 vertices
        if len(hull.vertices) == n:
            poly = pc.qhull(points)
            return points[hull.vertices], poly


def plot_polytope(vertices):
    plt.figure(figsize=(6, 6))
    vertices = np.vstack([vertices, vertices[0]])  # Close the polytope
    plt.plot(vertices[:, 0], vertices[:, 1], 'o-', markersize=10)
    plt.fill(vertices[:, 0], vertices[:, 1], alpha=0.3)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    test_chatgpt()
    # test_claude()
    # Generate random quadrilateral
    # A, b, vertices = generate_random_2d_polygon()
    #
    # print("Matrix A (coefficients of inequalities):")
    # print(A)
    # print("Vector b (constants of inequalities):")
    # print(b)
    # print("Vertices of the polygon:")
    # Theta = pc.Polytope(A, b)
    # print(Theta)
    # print(pc.extreme(Theta))
    # print(vertices)
    # random_test()
    # test_gemini_supabase()
# test_groq()
