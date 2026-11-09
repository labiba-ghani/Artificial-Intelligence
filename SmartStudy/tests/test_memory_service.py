
from unittest.mock import patch

from services.memory_service import (
    record_learning_activity,
    retrieve_learning_history,
)


def test_valid_learning_activity():
    with patch(
        "services.memory_service.save_learning_interaction"
    ) as mock_save:

        mock_save.return_value = 10

        result = record_learning_activity(
            interaction_type="quiz",
            topic=" Primary Keys ",
            content=" Correct answer ",
            score=1,
        )

        assert result == 10

        mock_save.assert_called_once_with(
            interaction_type="quiz",
            topic="Primary Keys",
            content="Correct answer",
            score=1,
        )

    print("PASS: Valid learning activity saved correctly.")


def test_invalid_interaction_type():
    with patch(
        "services.memory_service.save_learning_interaction"
    ) as mock_save:

        try:
            record_learning_activity(
                interaction_type="invalid_type",
                topic="Python",
                content="Test content",
            )
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Invalid interaction type was accepted."
            )

        mock_save.assert_not_called()

    print("PASS: Invalid interaction type rejected.")


def test_invalid_score():
    with patch(
        "services.memory_service.save_learning_interaction"
    ) as mock_save:

        try:
            record_learning_activity(
                interaction_type="quiz",
                topic="Databases",
                content="Test question",
                score=5,
            )
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Invalid quiz score was accepted."
            )

        mock_save.assert_not_called()

    print("PASS: Invalid quiz score rejected.")


def test_retrieve_history():
    expected_history = [
        {
            "id": 1,
            "interaction_type": "quiz",
            "topic": "Databases",
            "content": "Primary key question",
            "score": 1,
        }
    ]

    with patch(
        "services.memory_service.get_learning_history"
    ) as mock_history:

        mock_history.return_value = expected_history

        result = retrieve_learning_history(limit=5)

        assert result == expected_history

        mock_history.assert_called_once_with(limit=5)

    print("PASS: Learning history retrieved correctly.")


def test_invalid_history_limit():
    with patch(
        "services.memory_service.get_learning_history"
    ) as mock_history:

        try:
            retrieve_learning_history(limit=0)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Invalid history limit was accepted."
            )

        mock_history.assert_not_called()

    print("PASS: Invalid history limit rejected.")


if __name__ == "__main__":
    test_valid_learning_activity()
    test_invalid_interaction_type()
    test_invalid_score()
    test_retrieve_history()
    test_invalid_history_limit()

    print("\nAll memory service tests passed!")
