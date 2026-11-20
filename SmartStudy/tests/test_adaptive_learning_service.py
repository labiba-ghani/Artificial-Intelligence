
from services.adaptive_learning_service import (
    determine_quiz_difficulty,
    generate_adaptive_quiz_plan,
)


def test_difficulty_mapping():
    """
    Verify that learning classifications are mapped
    to the correct quiz difficulty.
    """

    assert determine_quiz_difficulty("Weak") == "easy"
    assert determine_quiz_difficulty("Developing") == "medium"
    assert determine_quiz_difficulty("Strong") == "hard"
    assert determine_quiz_difficulty("Insufficient Data") == "easy"

    print("PASS: All learning classifications mapped correctly.")


def test_adaptive_quiz_plan():
    """
    Verify that adaptive quiz plans are generated
    correctly from topic assessments.
    """

    sample_assessments = [
        {
            "topic": "SQL Joins",
            "classification": "Weak",
            "accuracy": 20.0,
        },
        {
            "topic": "Normalization",
            "classification": "Developing",
            "accuracy": 60.0,
        },
        {
            "topic": "Primary Keys",
            "classification": "Strong",
            "accuracy": 100.0,
        },
        {
            "topic": "Foreign Keys",
            "classification": "Insufficient Data",
            "accuracy": 0.0,
        },
    ]

    plans = generate_adaptive_quiz_plan(sample_assessments)

    assert len(plans) == 4

    assert [plan["difficulty"] for plan in plans] == [
        "easy",
        "medium",
        "hard",
        "easy",
    ]

    assert plans[0]["topic"] == "SQL Joins"
    assert plans[0]["classification"] == "Weak"
    assert plans[0]["accuracy"] == 20.0

    print("PASS: Adaptive quiz plans generated correctly.")
    print("PASS: Topic details preserved in generated plans.")


def test_empty_assessments():
    """
    Verify that empty input produces an empty plan.
    """

    assert generate_adaptive_quiz_plan([]) == []

    print("PASS: Empty topic assessments handled correctly.")


def test_invalid_classification():
    """
    Verify that unknown classifications are rejected.
    """

    try:
        determine_quiz_difficulty("Unknown")
    except ValueError:
        print("PASS: Invalid classifications rejected.")
    else:
        raise AssertionError(
            "Expected ValueError for an unknown classification."
        )


def test_invalid_plan_classification():
    """
    Verify that invalid classifications within
    topic assessments are also rejected.
    """

    invalid_assessments = [
        {
            "topic": "SQL",
            "classification": "Unknown",
            "accuracy": 50.0,
        }
    ]

    try:
        generate_adaptive_quiz_plan(invalid_assessments)
    except ValueError:
        print("PASS: Invalid classifications in quiz plans rejected.")
    else:
        raise AssertionError(
            "Expected ValueError for an invalid quiz plan."
        )


if __name__ == "__main__":
    test_difficulty_mapping()
    test_adaptive_quiz_plan()
    test_empty_assessments()
    test_invalid_classification()
    test_invalid_plan_classification()

    print("\nAll adaptive learning service tests passed!")
