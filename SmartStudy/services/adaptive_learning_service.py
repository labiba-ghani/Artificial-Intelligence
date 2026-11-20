
# ---------------------------------------------------------
# SmartStudy - Adaptive Learning Service
# Phase 10: Adaptive Quiz Difficulty
# ---------------------------------------------------------

from services.weak_topic_service import get_learning_topic_assessment
from services.recommendation_service import get_display_recommendations

def determine_quiz_difficulty(classification):
    """
    Determine the appropriate quiz difficulty based
    on the student's learning classification.

    Parameters:
        classification: Learning classification
            - Weak
            - Developing
            - Strong
            - Insufficient Data

    Returns:
        Quiz difficulty as a string:
            - easy
            - medium
            - hard
    """

    difficulty_mapping = {
        "Weak": "easy",
        "Developing": "medium",
        "Strong": "hard",
        "Insufficient Data": "easy",
    }

    if classification not in difficulty_mapping:
        raise ValueError(
            f"Unknown learning classification: {classification}"
        )

    return difficulty_mapping[classification]


def generate_adaptive_quiz_plan(topic_assessments):
    """
    Generate adaptive quiz plans from topic assessments.

    Parameters:
        topic_assessments: List of dictionaries
        produced by the weak-topic detection service.

    Returns:
        A list of dictionaries containing:
            - topic
            - classification
            - accuracy
            - difficulty
    """

    adaptive_plans = []

    for assessment in topic_assessments:
        topic = assessment["topic"]
        classification = assessment["classification"]
        accuracy = assessment["accuracy"]

        difficulty = determine_quiz_difficulty(
            classification
        )

        adaptive_plans.append({
            "topic": topic,
            "classification": classification,
            "accuracy": accuracy,
            "difficulty": difficulty,
        })

    return adaptive_plans


def get_adaptive_quiz_plans(min_attempts=3):
    """
    Generate adaptive quiz plans using the student's
    actual quiz performance stored in SQLite.

    Parameters:
        min_attempts: Minimum completed quizzes required
                      for performance classification.

    Returns:
        A list of adaptive quiz plans.
    """

    # Retrieve topic assessments from learning history.
    topic_assessments = get_learning_topic_assessment(
        min_attempts=min_attempts
    )

    # Convert classifications into quiz difficulty plans.
    adaptive_plans = generate_adaptive_quiz_plan(
        topic_assessments
    )

    return adaptive_plans
