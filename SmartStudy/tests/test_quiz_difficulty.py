
import json
from unittest.mock import patch

from services.quiz_service import generate_quiz


def test_quiz_difficulty():
    """
    Verify that the quiz generator includes the correct
    difficulty instructions in the AI prompt.
    """

    mock_quiz = {
        "question": "What is a primary key?",
        "options": [
            "A unique identifier",
            "A duplicate identifier",
            "A table name",
            "A database password"
        ],
        "correct_answer": 0,
        "explanation": "A primary key uniquely identifies a record."
    }

    for difficulty in ["easy", "medium", "hard"]:

        with patch(
            "services.quiz_service.ask_ai",
            return_value=json.dumps(mock_quiz)
        ) as mock_ai:

            quiz = generate_quiz(
                context="A primary key uniquely identifies a record.",
                provider="groq",
                difficulty=difficulty
            )

            # Confirm that the AI provider was called once.
            mock_ai.assert_called_once()

            # Extract the prompt passed to the AI.
            args, kwargs = mock_ai.call_args
            prompt = args[0]

            # Verify that the selected difficulty appears.
            assert f"QUIZ DIFFICULTY: {difficulty.upper()}" in prompt

            # Verify that the appropriate instruction appears.
            expected_instructions = {
                "easy": "beginner-level",
                "medium": "intermediate-level",
                "hard": "advanced-level"
            }

            assert expected_instructions[difficulty] in prompt

            # Confirm that the quiz was validated and returned.
            assert quiz["correct_answer"] == 0
            assert len(quiz["options"]) == 4
            assert kwargs["provider"] == "groq"

            print(
                f"PASS: {difficulty.upper()} difficulty "
                "instructions included correctly."
            )


def test_default_difficulty():
    """
    Confirm that existing calls use medium difficulty.
    """

    mock_quiz = {
        "question": "What is a primary key?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": 0,
        "explanation": "A primary key identifies a record."
    }

    with patch(
        "services.quiz_service.ask_ai",
        return_value=json.dumps(mock_quiz)
    ) as mock_ai:

        generate_quiz(
            context="A primary key uniquely identifies a record."
        )

        prompt = mock_ai.call_args.args[0]

        assert "QUIZ DIFFICULTY: MEDIUM" in prompt

        print("PASS: Default difficulty is MEDIUM.")


if __name__ == "__main__":
    test_quiz_difficulty()
    test_default_difficulty()

    print("\nAll quiz difficulty tests passed!")
