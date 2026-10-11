
import json
import os

from dotenv import load_dotenv
from groq import Groq
from ollama import chat as ollama_chat

from study_tools import get_student_progress, get_study_tips


load_dotenv()


TOOL_FUNCTIONS = {
    "get_student_progress": get_student_progress,
    "get_study_tips": get_study_tips
}


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_student_progress",
            "description": (
                "Get the student's topic scores "
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
                        "description": "Topic name: BFS, DFS or A* Search."
                    }
                },
                "required": ["topic"]
            }
        }
    }
]


SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are SmartStudy, a personalized learning assistant. "
        "You have access to Python tools that provide student data. "

        "IMPORTANT TOOL RULES: "
        "If the student asks about their scores, progress, "
        "weakest topic, or what to revise first, "
        "you MUST call get_student_progress. "

        "If the student asks for study tips about a topic, "
        "you MUST call get_study_tips with that topic. "

        "Do not ask the student for information that "
        "the available tools can provide. "

        "After receiving tool results, use them to answer. "
        "Trust the weakest_topic calculated by the progress tool. "
        "Never invent student scores."
    )
}



def run_agent(question: str, provider: str = "groq") -> str:

    messages = [
        SYSTEM_MESSAGE,
        {"role": "user", "content": question}
    ]

    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing.")

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        if not assistant_message.tool_calls:
            return assistant_message.content or ""

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name
            arguments = json.loads(
                tool_call.function.arguments
            )

            if name not in TOOL_FUNCTIONS:
                raise ValueError(f"Unknown tool: {name}")

            result = TOOL_FUNCTIONS[name](**arguments)

            print(f"[Groq tool] {name}: {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        final_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages
        )

        return final_response.choices[0].message.content or ""

    elif provider == "ollama":
        response = ollama_chat(
            model="qwen2.5:3b",
            messages=messages,
            tools=[get_student_progress, get_study_tips]
        )

        assistant_message = response.message

        if not assistant_message.tool_calls:
            return assistant_message.content or ""

        messages.append(assistant_message.model_dump(exclude_none=True))

        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name
            arguments = tool_call.function.arguments or {}

            if name not in TOOL_FUNCTIONS:
                raise ValueError(f"Unknown tool: {name}")

            result = TOOL_FUNCTIONS[name](**arguments)

            print(f"[Ollama tool] {name}: {result}")

            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": json.dumps(result)
            })

        final_response = ollama_chat(
            model="qwen2.5:3b",
            messages=messages
        )

        return final_response.message.content or ""

    else:
        raise ValueError("Choose 'groq' or 'ollama'.")
