
from services.recommendation_service import (
    generate_topic_recommendations,
)


def test_topic_recommendations():
    sample_performance = [
        {
            "topic": "Foreign Keys",
            "correct_answers": 4,
            "total_quizzes": 5,
        },
        {
            "topic": "Primary Keys",
            "correct_answers": 1,
            "total_quizzes": 3,
        },
        {
            "topic": "Normalization",
            "correct_answers": 3,
            "total_quizzes": 5,
        },
    ]

    recommendations = generate_topic_recommendations(
        sample_performance
    )

    assert len(recommendations) == 3

    assert recommendations[0]["topic"] == "Primary Keys"
    assert recommendations[0]["priority"] == "High"
    assert recommendations[0]["accuracy"] == 33.33

    assert recommendations[1]["topic"] == "Normalization"
    assert recommendations[1]["priority"] == "Medium"
    assert recommendations[1]["accuracy"] == 60.0

    assert recommendations[2]["topic"] == "Foreign Keys"
    assert recommendations[2]["priority"] == "Low"
    assert recommendations[2]["accuracy"] == 80.0

    print("PASS: Topic recommendations generated correctly.")
    print("PASS: Topics sorted by revision priority.")


if __name__ == "__main__":
    test_topic_recommendations()

    print("\nAll recommendation service tests passed!")
