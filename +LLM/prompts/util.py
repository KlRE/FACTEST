import google.generativeai as genai

import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def get_example_prompt():
    return """"""


def test_gemini():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Give me python code to sort a list")
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


if __name__ == "__main__":
    test_groq()
