from database.db_manager import get_quiz_topic_performance

def generate_topic_recommendations(topic_performance):
    """
    Generate personalized revision recommendations
    based on quiz performance for each topic.

    Each topic must contain:
    - topic: Name of the learning topic
    - correct_answers: Number of correct answers
    - total_quizzes: Number of completed quizzes
    """

    recommendations = []

    for record in topic_performance:
        topic = record["topic"]
        correct_answers = record["correct_answers"]
        total_quizzes = record["total_quizzes"]

        if total_quizzes <= 0:
            continue

        accuracy = round(
            (correct_answers / total_quizzes) * 100,
            2,
        )

        if accuracy < 50:
            priority = "High"
            message = (
                f"Revise {topic} as a priority. "
                "Review the core concepts and practise "
                "more questions."
            )

        elif accuracy < 80:
            priority = "Medium"
            message = (
                f"Continue practising {topic}. "
                "Focus on areas where you made mistakes."
            )

        else:
            priority = "Low"
            message = (
                f"You are performing well in {topic}. "
                "Review it periodically to retain your knowledge."
            )

        recommendations.append(
            {
                "topic": topic,
                "accuracy": accuracy,
                "priority": priority,
                "recommendation": message,
            }
        )

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2,
    }

    recommendations.sort(
        key=lambda item: (
            priority_order[item["priority"]],
            item["accuracy"],
            item["topic"],
        )
    )

    return recommendations


def get_personalized_recommendations():
    """
    Generate personalized learning recommendations
    using quiz performance stored in SQLite.

    Returns recommendations ordered by revision priority.
    """

    # Retrieve aggregated quiz performance from the database.
    topic_performance = get_quiz_topic_performance()

    # Reuse the existing recommendation algorithm.
    recommendations = generate_topic_recommendations(
        topic_performance
    )

    return recommendations


def get_display_recommendations():
    """
    Return personalized recommendations suitable for
    display in the Streamlit interface.

    Exclude historical quiz records that were saved
    using full questions instead of topic names.
    """

    recommendations = get_personalized_recommendations()

    display_recommendations = []

    for recommendation in recommendations:
        topic = recommendation["topic"].strip()

        # Older records sometimes contain full quiz questions.
        # Exclude obvious question-style topic values.
        if "?" in topic:
            continue

        # Exclude unusually long topic values.
        if len(topic.split()) > 8:
            continue

        display_recommendations.append(recommendation)

    return display_recommendations
