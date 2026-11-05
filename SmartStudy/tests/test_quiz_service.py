
import json

from services.quiz_service import validate_quiz_response


def test_valid_quiz():
    """Test that a correctly formatted quiz is accepted."""

    sample = {
        "question": "What is a primary key?",
        "options": [
            "Unique identifier",
            "Password",
            "Backup",
            "Query"
        ],
        "correct_answer": 0,
        "explanation": "It uniquely identifies rows."
    }

    response = json.dumps(sample)

    result = validate_quiz_response(response)

    assert result["question"] == sample["question"]
    assert result["correct_answer"] == 0
    assert len(result["options"]) == 4

    print("PASS: Valid quiz accepted.")


def test_invalid_quiz():
    """Test that an incorrectly formatted quiz is rejected."""

    invalid_sample = {
        "question": "What is a primary key?",
        "options": [
            "Unique identifier",
            "Password"
        ],
        "correct_answer": 5,
        "explanation": "It uniquely identifies rows."
    }

    response = json.dumps(invalid_sample)

    try:
        validate_quiz_response(response)
    except ValueError as error:
        print(f"PASS: Invalid quiz rejected: {error}")
    else:
        raise AssertionError(
            "Invalid quiz was incorrectly accepted."
        )


if __name__ == "__main__":
    test_valid_quiz()
    test_invalid_quiz()

    print("All quiz validation tests passed.")
