
from unittest.mock import patch

from services.weak_topic_service import get_learning_topic_assessment


def test_historical_question_filtering():
    """
    Verify that historical question-style topics are
    excluded from learning assessments.
    """

    mock_performance = [
        {
            "topic": "primarykeys",
            "correct_answers": 2,
            "total_quizzes": 3,
        },
        {
            "topic": "foreignkey",
            "correct_answers": 1,
            "total_quizzes": 4,
        },
        {
            "topic": "Which constraint ensures that a column cannot contain null values?",
            "correct_answers": 1,
            "total_quizzes": 1,
        },
        {
            "topic": "which database constraint is used to identify each individual record within a database table",
            "correct_answers": 1,
            "total_quizzes": 1,
        },
    ]

    with patch(
        "services.weak_topic_service.get_quiz_topic_performance",
        return_value=mock_performance,
    ) as mock_database:
        assessments = get_learning_topic_assessment()

        mock_database.assert_called_once_with()

    topics = [assessment["topic"] for assessment in assessments]

    assert len(assessments) == 2
    assert "primarykeys" in topics
    assert "foreignkey" in topics

    assert all("?" not in topic for topic in topics)
    assert all(len(topic.split()) <= 8 for topic in topics)

    print("PASS: Historical question-style topics filtered.")
    print("PASS: Valid learning topics preserved.")


def test_empty_filtered_results():
    """
    Verify that the service returns an empty list
    when all historical records are filtered.
    """

    mock_performance = [
        {
            "topic": "What is a primary key?",
            "correct_answers": 1,
            "total_quizzes": 1,
        },
    ]

    with patch(
        "services.weak_topic_service.get_quiz_topic_performance",
        return_value=mock_performance,
    ):
        assessments = get_learning_topic_assessment()

    assert assessments == []

    print("PASS: Empty results handled after filtering.")


if __name__ == "__main__":
    test_historical_question_filtering()
    test_empty_filtered_results()

    print("\nAll weak topic filtering tests passed!")
