
from database.db_manager import (
    get_all_quiz_records,
    get_learning_activity_counts,
)


def calculate_quiz_statistics(history):
    """
    Calculate quiz performance statistics
    from learning history records.
    """

    quiz_records = [
        record
        for record in history
        if record["interaction_type"] == "quiz"
        and record["score"] in (0, 1)
    ]

    total_quizzes = len(quiz_records)

    correct_answers = sum(
        record["score"]
        for record in quiz_records
    )

    incorrect_answers = total_quizzes - correct_answers

    accuracy = (
        (correct_answers / total_quizzes) * 100
        if total_quizzes > 0
        else 0.0
    )

    return {
        "total_quizzes": total_quizzes,
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "accuracy": round(accuracy, 2),
    }


def get_quiz_performance_summary():
    """
    Retrieve all saved quiz records and
    calculate overall quiz performance.
    """

    history = get_all_quiz_records()

    return calculate_quiz_statistics(history)


def get_learning_activity_summary():
    """
    Retrieve learning activity counts and
    calculate total learning interactions.
    """

    activity_counts = get_learning_activity_counts()

    general_questions = activity_counts["general_question"]
    document_questions = activity_counts["document_question"]
    quizzes = activity_counts["quiz"]

    total_interactions = (
        general_questions
        + document_questions
        + quizzes
    )

    return {
        "general_questions": general_questions,
        "document_questions": document_questions,
        "quizzes": quizzes,
        "total_interactions": total_interactions,
    }
