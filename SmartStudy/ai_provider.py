
import os

from dotenv import load_dotenv
from groq import Groq
from ollama import chat as ollama_chat


load_dotenv()


def ask_ai(question: str, provider: str = "groq") -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are SmartStudy, a helpful AI "
                "learning assistant. Explain concepts "
                "clearly to students."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing.")

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages
        )

        return response.choices[0].message.content or ""

    elif provider == "ollama":
        response = ollama_chat(
            model="qwen2.5:3b",
            messages=messages
        )

        return response.message.content or ""

    else:
        raise ValueError(
            "Invalid provider. Choose 'groq' or 'ollama'."
        )
