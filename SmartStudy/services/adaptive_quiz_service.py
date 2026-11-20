
from services.adaptive_learning_service import get_adaptive_quiz_plans
from services.quiz_service import generate_quiz_from_pdf


def get_topic_quiz_difficulty(
    topic: str,
    min_attempts: int = 3
) -> str:
    """
    Determine quiz difficulty for a topic using
    the student's previous quiz performance.
    """

    # Retrieve adaptive learning plans from quiz history.
    adaptive_plans = get_adaptive_quiz_plans(
        min_attempts=min_attempts
    )

    # Normalize the requested topic for comparison.
    normalized_topic = "".join(
        character.lower()
        for character in topic
        if character.isalnum()
    )

    # Find the matching topic in learning history.
    for plan in adaptive_plans:

        stored_topic = "".join(
            character.lower()
            for character in plan["topic"]
            if character.isalnum()
        )

        if stored_topic == normalized_topic:
            return plan["difficulty"]

    # New topics begin with easy difficulty.
    return "easy"


def generate_adaptive_quiz_from_pdf(
    chunks: list[dict],
    topic: str,
    provider: str = "groq",
    min_attempts: int = 3
) -> dict:
    """
    Generate a PDF-based quiz using difficulty
    selected from the student's learning history.
    """

    if not topic.strip():
        raise ValueError(
            "Please provide a topic for adaptive quiz generation."
        )

    # Determine difficulty using previous performance.
    difficulty = get_topic_quiz_difficulty(
        topic=topic,
        min_attempts=min_attempts
    )

    # Generate a quiz at the selected difficulty.
    quiz = generate_quiz_from_pdf(
        chunks=chunks,
        topic=topic,
        provider=provider,
        difficulty=difficulty
    )

    return quiz
