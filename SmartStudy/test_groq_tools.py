
import os
import json

from dotenv import load_dotenv
from groq import Groq


# ----------------------------------
# 1. Our Python tools
# ----------------------------------

def get_student_progress():
    scores = {
        "BFS": 40,
        "DFS": 85,
        "A* Search": 60
    }

    weakest_topic = min(scores, key=scores.get)

    return {
        "scores": scores,
        "weakest_topic": weakest_topic,
        "weakest_score": scores[weakest_topic]
    }


def get_study_tips(topic: str):
    tips = {
        "BFS": [
            "Understand how a queue works.",
            "Practice graph traversal level by level.",
            "Trace BFS manually on a graph."
        ],
        "DFS": [
            "Understand recursion and stacks.",
            "Practice depth-first traversal.",
            "Compare DFS with BFS."
        ],
        "A* Search": [
            "Understand heuristic functions.",
            "Learn f(n) = g(n) + h(n).",
            "Practice finding paths using A*."
        ]
    }

    return {
        "topic": topic,
        "tips": tips.get(
            topic,
            ["Review the fundamentals and practice questions."]
        )
    }


# ----------------------------------
# 2. Connect to Groq
# ----------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing.")

client = Groq(api_key=api_key)


# ----------------------------------
# 3. Describe tools to the AI
# ----------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_student_progress",
            "description": (
                "Get a student's topic scores "
                "and identify their weakest topic."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_study_tips",
            "description": "Get study tips for a specific topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": (
                            "The topic name, such as BFS, "
                            "DFS or A* Search."
                        )
                    }
                },
                "required": ["topic"]
            }
        }
    }
]


# ----------------------------------
# 4. Ask the AI
# ----------------------------------

messages = [
    {
        "role": "system",
        "content": (
            "You are SmartStudy, an AI learning assistant. "
            "Use the available tools when needed. "
            "Trust the weakest_topic calculated by the "
            "student progress tool."
        )
    },
    {
        
    "role": "user",
    "content": "Can you give me some study tips for DFS?"

    }
]

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

assistant_message = response.choices[0].message

print("\nAI selected tools:")

if assistant_message.tool_calls:
    messages.append(assistant_message.model_dump(exclude_none=True))

    for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print(function_name)

        if function_name == "get_student_progress":
            result = get_student_progress()

        elif function_name == "get_study_tips":
            result = get_study_tips(**arguments)

        else:
            raise ValueError(f"Unknown tool: {function_name}")

        print("Tool result:", result)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

    final_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )

    print("\nSmartStudy:")
    print(final_response.choices[0].message.content)

else:
    print("No tool selected.")
    print(assistant_message.content)
