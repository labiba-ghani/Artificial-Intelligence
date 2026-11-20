
# ---------------------------------------------------------
# SmartStudy - Weak Topic Detection Service
# Phase 10: Adaptive Learning
# ---------------------------------------------------------
from database.db_manager import get_quiz_topic_performance

def detect_weak_topics(topic_performance, min_attempts=3):
    """
    Analyse quiz performance and classify learning topics.

    Parameters:
        topic_performance: List of dictionaries containing:
            - topic
            - correct_answers
            - total_quizzes

        min_attempts: Minimum quizzes required before
                      classifying a topic's performance.

    Returns:
        A list of topic performance classifications.
    """

    if not isinstance(min_attempts, int) or isinstance(min_attempts, bool):
        raise ValueError("min_attempts must be a positive integer.")

    if min_attempts < 1:
        raise ValueError("min_attempts must be at least 1.")

    results = []

    for record in topic_performance:
        topic = record["topic"]
        correct_answers = record["correct_answers"]
        total_quizzes = record["total_quizzes"]

        # Skip topics with no completed quizzes.
        if total_quizzes <= 0:
            continue

        # Calculate topic accuracy.
        accuracy = round(
            (correct_answers / total_quizzes) * 100,
            2
        )

        # Require sufficient evidence before classification.
        if total_quizzes < min_attempts:
            classification = "Insufficient Data"

        elif accuracy < 50:
            classification = "Weak"

        elif accuracy < 80:
            classification = "Developing"

        else:
            classification = "Strong"

        results.append({
            "topic": topic,
            "correct_answers": correct_answers,
            "total_quizzes": total_quizzes,
            "accuracy": accuracy,
            "classification": classification,
        })

    # Show topics requiring attention first.
    classification_order = {
        "Weak": 0,
        "Developing": 1,
        "Strong": 2,
        "Insufficient Data": 3,
    }

    results.sort(
        key=lambda item: (
            classification_order[item["classification"]],
            item["accuracy"],
            item["topic"],
        )
    )

    return results


def get_learning_topic_assessment(min_attempts=3):
    """
    Retrieve quiz performance from SQLite and classify
    each topic based on accuracy and completed attempts.

    Returns:
        A list of topic assessments ordered by priority.
    """

    # Retrieve aggregated quiz performance from SQLite.
    topic_performance = get_quiz_topic_performance()

    # Apply the weak-topic detection rules.
    assessments = detect_weak_topics(
        topic_performance,
        min_attempts=min_attempts,
    )

    return assessments

