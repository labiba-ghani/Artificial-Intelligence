
from unittest.mock import patch

from services.weak_topic_service import get_learning_topic_assessment


def test_weak_topic_integration():
    """
    Verify that quiz performance from the database
    is correctly passed to the weak-topic detector.
    """

    mock_performance = [
        {
            "topic": "SQL Joins",
            "correct_answers": 1,
            "total_quizzes": 5,
        },
        {
            "topic": "Normalization",
            "correct_answers": 3,
            "total_quizzes": 5,
        },
        {
            "topic": "Primary Keys",
            "correct_answers": 4,
            "total_quizzes": 5,
        },
        {
            "topic": "Foreign Keys",
            "correct_answers": 0,
            "total_quizzes": 1,
        },
    ]

    # Replace the real database function with controlled test data.
    with patch(
        "services.weak_topic_service.get_quiz_topic_performance",
        return_value=mock_performance,
    ) as mock_database:

        results = get_learning_topic_assessment()

        mock_database.assert_called_once_with()

    classifications = {
        record["topic"]: record["classification"]
        for record in results
    }

    assert classifications["SQL Joins"] == "Weak"
    assert classifications["Normalization"] == "Developing"
    assert classifications["Primary Keys"] == "Strong"
    assert classifications["Foreign Keys"] == "Insufficient Data"

    assert len(results) == 4

    print("PASS: Quiz performance retrieved through database integration.")
    print("PASS: Weak, developing, and strong classifications verified.")
    print("PASS: Insufficient quiz attempts handled correctly.")


def test_custom_minimum_attempts():
    """
    Verify that the integration forwards custom
    minimum-attempt requirements.
    """

    mock_performance = [
        {
            "topic": "Database Indexing",
            "correct_answers": 1,
            "total_quizzes": 2,
        },
    ]

    with patch(
        "services.weak_topic_service.get_quiz_topic_performance",
        return_value=mock_performance,
    ):
        results = get_learning_topic_assessment(min_attempts=2)

    assert results[0]["classification"] == "Developing"
    assert results[0]["accuracy"] == 50.0

    print("PASS: Custom minimum-attempt threshold applied.")


if __name__ == "__main__":
    test_weak_topic_integration()
    test_custom_minimum_attempts()

    print("\nAll weak topic integration tests passed!")
