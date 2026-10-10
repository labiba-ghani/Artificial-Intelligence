
import json
from ollama import chat


# Tool 1: Get previous quiz scores
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

messages = [
    {
        "role": "system",
        "content": (
            "You are SmartStudy, an AI learning assistant. "
            "Student quiz scores are stored in the "
            "get_student_progress tool. "
            "When a user asks about scores, weak topics, "
            "or what to revise, call get_student_progress. "
            "Do not ask the student to provide scores. "
            "Do not invent scores."
        )
    },
    {
        "role": "user",
        "content": (
            "Check my saved quiz scores using the "
            "get_student_progress tool and tell me "
            "which topic I should revise first."
        )
    }
]


print("Asking AI to select a tool...")

response = chat(
    model="qwen2.5:3b",
    messages=messages,
    tools=[get_student_progress],
    options={"temperature": 0}
)

print("Model response:", response.message.content)
print("Tool calls:", response.message.tool_calls)

messages.append(response.message)


if response.message.tool_calls:

    for tool_call in response.message.tool_calls:

        tool_name = tool_call.function.name

        if tool_name == "get_student_progress":

            result = get_student_progress()

            print("\nTool executed:", tool_name)
            print("Returned scores:", result)

            messages.append({
                "role": "tool",
                "tool_name": tool_name,
                "content": json.dumps(result)
            })

    final_response = chat(
        model="qwen2.5:1.5b",
        messages=messages,
        options={"temperature": 0}
    )

    print("\nSmartStudy:", final_response.message.content)

else:
    print("\nThe model did not request a tool.")
    print("We may need a different model.")
