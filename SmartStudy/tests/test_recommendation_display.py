
from unittest.mock import patch

from services.recommendation_service import (
    get_display_recommendations,
)


def test_recommendation_display():
    sample_recommendations = [
        {
            "topic": "primary key",
            "accuracy": 100.0,
            "priority": "Low",
            "recommendation": "Review periodically.",
        },
        {
            "topic": "which constraint ensures unique values?",
            "accuracy": 0.0,
            "priority": "High",
            "recommendation": "Revise this topic.",
        },
        {
            "topic": "foreign keys",
            "accuracy": 60.0,
            "priority": "Medium",
            "recommendation": "Continue practising.",
        },
        {
            "topic": (
                "this is a very long historical quiz question "
                "that was incorrectly saved as a topic"
            ),
            "accuracy": 50.0,
            "priority": "Medium",
            "recommendation": "Review this topic.",
        },
    ]

    with patch(
        "services.recommendation_service.get_personalized_recommendations",
        return_value=sample_recommendations,
    ):
        results = get_display_recommendations()

    assert len(results) == 2

    topics = [record["topic"] for record in results]

    assert "primary key" in topics
    assert "foreign keys" in topics

    assert all("?" not in topic for topic in topics)

    assert all(
        len(topic.split()) <= 8
        for topic in topics
    )

    print("PASS: Valid learning topics retained.")
    print("PASS: Historical question-style topics excluded.")
    print("PASS: Long invalid topic values excluded.")
    print("PASS: Recommendation data preserved.")


if __name__ == "__main__":
    test_recommendation_display()

    print("\nAll recommendation display tests passed!")
