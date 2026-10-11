
import os

from dotenv import load_dotenv
from groq import Groq


# Step 1: Load environment variables from .env
load_dotenv()

# Step 2: Read our Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. Check your .env file."
    )

# Step 3: Create the Groq client
client = Groq(api_key=api_key)

# Step 4: Send a question to the AI model
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": (
                "You are SmartStudy, a helpful AI "
                "learning assistant."
            )
        },
        {
            "role": "user",
            "content": (
                "Explain what an AI agent is "
                "in two simple sentences."
            )
        }
    ],
    temperature=0
)

# Step 5: Display the AI response
print("\nSmartStudy (Groq):")
print(response.choices[0].message.content)
