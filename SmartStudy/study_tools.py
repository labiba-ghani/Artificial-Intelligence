
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
