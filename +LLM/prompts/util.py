import base64
from time import strftime, gmtime

import polytope as pc
import numpy as np
import vertexai
from anthropic import AnthropicVertex
from matplotlib import pyplot as plt
from scipy.spatial import ConvexHull
from vertexai.generative_models import GenerativeModel, Image

import os

from groq import Groq
from dotenv import load_dotenv
from rich.progress import TimeElapsedColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, \
    SpinnerColumn
from rich.table import Column
from supabase import create_client, Client
from supafunc.errors import FunctionsHttpError, FunctionsRelayError

with open("/home/erik/FACTEST/+LLM/envs/plots/manual/Box.png", mode='rb') as file:
    img = file.read()


def get_example_prompt():
    return """"""


def test_gemini_supabase():
    load_dotenv()
    # url: str = os.environ.get("SUPABASE_URL")
    # key: str = os.environ.get("SUPABASE_KEY")
    # supabase: Client = create_client(url, key)
    #
    #
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
    image = Image.load_from_file("/home/erik/FACTEST/+LLM/envs/plots/manual/Box.png")
    response = model.generate_content(
        ["What do you see", image]
    )
    print(response.text)
    vertexai.init(project="gentle-keyword-432706-b3", location="us-central1")

    image = Image.load_from_file("/home/erik/FACTEST/+LLM/envs/plots/manual/Box.png")
    response = model.generate_content(
        ["What do you see", image]
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
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What do you see"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64.b64encode(img).decode('utf-8')}"
                        }
                    }
                ]
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
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64.b64encode(img).decode('utf-8'),
                        },
                    },
                    {
                        "type": "text",
                        "text": "Describe this image."
                    }]
            }
        ],
        model="claude-3-5-sonnet-20240620",
    )
    print(message.content[0].text)


def test_claude_vertex():
    client = AnthropicVertex(region="europe-west1", project_id="gentle-keyword-432706-b3")
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64.b64encode(img).decode('utf-8'),
                        },
                    },
                    {
                        "type": "text",
                        "text": "Describe this image."
                    }]
            }
        ],
        model="claude-3-5-sonnet@20240620",
    )

    print(message.content[0].text)


def test_gemini():
    import google.generativeai as genai
    load_dotenv()
    # genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    model = genai.GenerativeModel('tunedModels/factest-pathonly-v1-gpt')
    response = model.generate_content("Write a story about an AI and magic")
    print(response.text)


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


def test_reges():
    import re
    response = "new_path = [[1.0, 1.0], [13.31, 16.25], [19.0, 19.0]]"
    path_section = re.search(r'new_path\s*=\s*\[(.*)]', response, re.DOTALL).group(1)
    print(path_section)
    coordinate_pattern = re.compile(r'[(\[][+-]?(?:\d*\.)?\d+, [+-]?(?:\d*\.)?\d+[])]')
    coordinates = coordinate_pattern.findall(path_section)
    print(coordinates)
    # Convert the found coordinate pairs to a list of tuples
    path = [tuple(map(float, coord.strip('()[]').split(', '))) for coord in coordinates]
    print(path)


if __name__ == "__main__":
    # test_gemini()
    # ätest_reges()
    # test_chatgpt()
    test_claude_vertex()
    # test_claude()
    # test_gemini()
    # random_test()
    # test_gemini_supabase()
# test_groq()
