
from unittest.mock import patch

from services.quiz_service import generate_quiz


def test_retry_after_invalid_json():
    """
    Verify that quiz generation retries once
    after receiving invalid JSON.
    """

    valid_response = """
    {
        "question": "What does a primary key do?",
        "options": [
            "Allows duplicate values",
            "Uniquely identifies each row",
            "Allows NULL values",
            "Deletes a table"
        ],
        "correct_answer": 1,
        "explanation": "A primary key identifies each row uniquely."
    }
    """

    # Simulate two consecutive AI responses:
    # 1. Invalid JSON
    # 2. Valid JSON
    with patch(
        "services.quiz_service.ask_ai",
        side_effect=[
            "This is not valid JSON.",
            valid_response
        ]
    ) as mock_ai:

        quiz = generate_quiz(
            context="A primary key uniquely identifies each row.",
            provider="ollama"
        )

        assert quiz["correct_answer"] == 1
        assert len(quiz["options"]) == 4

        # Confirm that the AI was called twice.
        assert mock_ai.call_count == 2

    print("PASS: Invalid JSON triggered a retry.")
    print("PASS: Second valid response was accepted.")
    print("PASS: AI was called exactly twice.")


def test_retry_stops_after_two_failures():
    """
    Verify that quiz generation stops after
    two invalid AI responses.
    """

    with patch(
        "services.quiz_service.ask_ai",
        side_effect=[
            "Invalid JSON response one.",
            "Invalid JSON response two."
        ]
    ) as mock_ai:

        try:
            generate_quiz(
                context="A primary key uniquely identifies each row.",
                provider="ollama"
            )

        except ValueError as error:

            assert (
                "after two attempts" in str(error)
            )

        else:

            raise AssertionError(
                "Expected ValueError was not raised."
            )

        assert mock_ai.call_count == 2

    print("PASS: Two invalid responses were rejected.")
    print("PASS: Retry stopped after exactly two attempts.")


if __name__ == "__main__":
    test_retry_after_invalid_json()
    test_retry_stops_after_two_failures()