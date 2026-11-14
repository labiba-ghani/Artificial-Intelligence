
from unittest.mock import patch

from services.analytics_service import (
    calculate_quiz_statistics,
    get_quiz_performance_summary,
)


def test_quiz_statistics():
    sample_history = [
        {"interaction_type": "quiz", "score": 1},
        {"interaction_type": "quiz", "score": 0},
        {"interaction_type": "quiz", "score": 1},
        {"interaction_type": "general_question", "score": None},
    ]

    result = calculate_quiz_statistics(sample_history)

    assert result["total_quizzes"] == 3
    assert result["correct_answers"] == 2
    assert result["incorrect_answers"] == 1
    assert result["accuracy"] == 66.67

    print("PASS: Quiz statistics calculated correctly.")


def test_quiz_performance_summary():
    sample_records = [
        {"interaction_type": "quiz", "score": 1},
        {"interaction_type": "quiz", "score": 0},
        {"interaction_type": "quiz", "score": 1},
    ]

    with patch(
        "services.analytics_service.get_all_quiz_records",
        return_value=sample_records,
    ) as mock_retrieve:

        result = get_quiz_performance_summary()

        mock_retrieve.assert_called_once_with()

        assert result["total_quizzes"] == 3
        assert result["correct_answers"] == 2
        assert result["incorrect_answers"] == 1
        assert result["accuracy"] == 66.67

    print("PASS: Database-to-analytics integration works.")


def test_empty_quiz_history():
    result = calculate_quiz_statistics([])

    assert result["total_quizzes"] == 0
    assert result["correct_answers"] == 0
    assert result["incorrect_answers"] == 0
    assert result["accuracy"] == 0.0

    print("PASS: Empty quiz history handled correctly.")


if __name__ == "__main__":
    test_quiz_statistics()
    test_quiz_performance_summary()
    test_empty_quiz_history()

    print("\nAll analytics service tests passed!")
