
from unittest.mock import patch

from services.adaptive_quiz_service import (
    get_topic_quiz_difficulty,
    generate_adaptive_quiz_from_pdf
)


def test_topic_difficulty():
    """
    Verify that topics receive the correct difficulty
    based on their learning classifications.
    """

    mock_plans = [
        {
            "topic": "primarykeys",
            "classification": "Weak",
            "accuracy": 30.0,
            "difficulty": "easy"
        },
        {
            "topic": "foreignkeys",
            "classification": "Developing",
            "accuracy": 65.0,
            "difficulty": "medium"
        },
        {
            "topic": "normalization",
            "classification": "Strong",
            "accuracy": 90.0,
            "difficulty": "hard"
        }
    ]

    with patch(
        "services.adaptive_quiz_service.get_adaptive_quiz_plans",
        return_value=mock_plans
    ) as mock_get_plans:

        # Weak topic -> Easy
        assert get_topic_quiz_difficulty("Primary Keys") == "easy"
        print("PASS: Weak topic receives EASY difficulty.")

        # Developing topic -> Medium
        assert get_topic_quiz_difficulty("Foreign Keys") == "medium"
        print("PASS: Developing topic receives MEDIUM difficulty.")

        # Strong topic -> Hard
        assert get_topic_quiz_difficulty("Normalization") == "hard"
        print("PASS: Strong topic receives HARD difficulty.")

        # Topic normalization should ignore spaces and punctuation.
        assert get_topic_quiz_difficulty("PRIMARY-KEYS") == "easy"
        print("PASS: Topic normalization works correctly.")

        # Unknown topics start with Easy difficulty.
        assert get_topic_quiz_difficulty("SQL Joins") == "easy"
        print("PASS: New topics receive EASY difficulty.")

        # Confirm the adaptive plans were requested.
        assert mock_get_plans.call_count == 5


def test_adaptive_pdf_quiz():
    """
    Verify that adaptive PDF quiz generation forwards
    the selected difficulty correctly.
    """

    chunks = [
        {
            "page_number": 1,
            "text": "Database normalization reduces redundancy."
        }
    ]

    mock_quiz = {
        "question": "Why is normalization important?",
        "options": [
            "Reduces redundancy",
            "Increases duplication",
            "Removes primary keys",
            "Disables relationships"
        ],
        "correct_answer": 0,
        "explanation": "Normalization reduces data redundancy."
    }

    with patch(
        "services.adaptive_quiz_service.get_topic_quiz_difficulty",
        return_value="hard"
    ) as mock_difficulty, patch(
        "services.adaptive_quiz_service.generate_quiz_from_pdf",
        return_value=mock_quiz
    ) as mock_generate:

        quiz = generate_adaptive_quiz_from_pdf(
            chunks=chunks,
            topic="Normalization",
            provider="groq",
            min_attempts=3
        )

        mock_difficulty.assert_called_once_with(
            topic="Normalization",
            min_attempts=3
        )

        mock_generate.assert_called_once_with(
            chunks=chunks,
            topic="Normalization",
            provider="groq",
            difficulty="hard"
        )

        assert quiz == mock_quiz

        print("PASS: Adaptive PDF quiz forwards HARD difficulty.")


def test_empty_topic():
    """
    Verify that an empty topic is rejected.
    """

    try:
        generate_adaptive_quiz_from_pdf(
            chunks=[],
            topic="   "
        )

    except ValueError as error:
        assert str(error) == (
            "Please provide a topic for adaptive quiz generation."
        )
        print("PASS: Empty topic is rejected correctly.")

    else:
        raise AssertionError("Empty topic should raise ValueError.")


if __name__ == "__main__":
    test_topic_difficulty()
    test_adaptive_pdf_quiz()
    test_empty_topic()

    print("\nAll adaptive quiz service tests passed!")
