
from unittest.mock import patch

from services.recommendation_service import (
    get_personalized_recommendations,
)


def test_personalized_recommendations():
    # Simulate aggregated data returned from SQLite.
    sample_performance = [
        {
            "topic": "primary keys",
            "correct_answers": 1,
            "total_quizzes": 4,
        },
        {
            "topic": "foreign keys",
            "correct_answers": 3,
            "total_quizzes": 5,
        },
        {
            "topic": "normalization",
            "correct_answers": 5,
            "total_quizzes": 5,
        },
    ]

    # Replace the database call with controlled test data.
    with patch(
        "services.recommendation_service.get_quiz_topic_performance",
        return_value=sample_performance,
    ) as mock_database:
        recommendations = get_personalized_recommendations()

    # Verify that the database function was called.
    mock_database.assert_called_once_with()

    # Verify the number and order of recommendations.
    assert len(recommendations) == 3

    assert recommendations[0]["topic"] == "primary keys"
    assert recommendations[0]["accuracy"] == 25.0
    assert recommendations[0]["priority"] == "High"

    assert recommendations[1]["topic"] == "foreign keys"
    assert recommendations[1]["accuracy"] == 60.0
    assert recommendations[1]["priority"] == "Medium"

    assert recommendations[2]["topic"] == "normalization"
    assert recommendations[2]["accuracy"] == 100.0
    assert recommendations[2]["priority"] == "Low"

    print("PASS: Database integration called correctly.")
    print("PASS: Recommendations generated successfully.")
    print("PASS: Accuracy calculated correctly.")
    print("PASS: Recommendations sorted by priority.")


if __name__ == "__main__":
    test_personalized_recommendations()

    print("\nAll recommendation integration tests passed!")
