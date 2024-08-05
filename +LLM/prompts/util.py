import json

import google.generativeai as genai

import os

from groq import Groq
from dotenv import load_dotenv
from supabase import create_client, Client
from supafunc.errors import FunctionsHttpError, FunctionsRelayError


def get_example_prompt():
    return """"""


def test_gemini_supabase():
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    response = supabase.functions.invoke(
        "prompt",
        invoke_options={
            "headers": {
                "Content-Type": "application/json",
                "x-region": "us-west-1",
            },
            "body": {"secret": "ButtrFly", "prompt": "Hello, world!"}}
    )
    print(json.loads(response)["candidates"][0]["content"]["parts"][0]["text"])
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


if __name__ == "__main__":
    test_gemini_supabase()
    # test_groq()
