
from services.weak_topic_service import detect_weak_topics


def test_weak_topic_detection():
    """
    Verify topic classification, accuracy calculations,
    minimum attempt requirements, and sorting.
    """

    sample_performance = [
        {
            "topic": "Primary Keys",
            "correct_answers": 1,
            "total_quizzes": 5,
        },
        {
            "topic": "Foreign Keys",
            "correct_answers": 2,
            "total_quizzes": 5,
        },
        {
            "topic": "Normalization",
            "correct_answers": 3,
            "total_quizzes": 5,
        },
        {
            "topic": "SQL Joins",
            "correct_answers": 5,
            "total_quizzes": 5,
        },
        {
            "topic": "Indexing",
            "correct_answers": 0,
            "total_quizzes": 1,
        },
    ]

    results = detect_weak_topics(sample_performance)

    assert len(results) == 5

    classifications = {
        record["topic"]: record
        for record in results
    }

    # Verify weak topic detection.
    assert classifications["Primary Keys"]["accuracy"] == 20.0
    assert classifications["Primary Keys"]["classification"] == "Weak"

    assert classifications["Foreign Keys"]["accuracy"] == 40.0
    assert classifications["Foreign Keys"]["classification"] == "Weak"

    # Verify developing and strong topics.
    assert classifications["Normalization"]["classification"] == "Developing"
    assert classifications["SQL Joins"]["classification"] == "Strong"

    # One attempt is insufficient for classification.
    assert classifications["Indexing"]["classification"] == "Insufficient Data"

    # Verify priority ordering.
    assert [record["topic"] for record in results] == [
        "Primary Keys",
        "Foreign Keys",
        "Normalization",
        "SQL Joins",
        "Indexing",
    ]

    print("PASS: Weak topics detected correctly.")
    print("PASS: Developing and strong topics classified correctly.")
    print("PASS: Minimum quiz attempt requirement enforced.")
    print("PASS: Topics sorted by learning priority.")


def test_accuracy_boundaries():
    """
    Verify classification at the 50% and 80% boundaries.
    """

    sample_performance = [
        {
            "topic": "Boundary 50",
            "correct_answers": 2,
            "total_quizzes": 4,
        },
        {
            "topic": "Boundary 80",
            "correct_answers": 4,
            "total_quizzes": 5,
        },
    ]

    results = detect_weak_topics(sample_performance)

    classifications = {
        record["topic"]: record["classification"]
        for record in results
    }

    assert classifications["Boundary 50"] == "Developing"
    assert classifications["Boundary 80"] == "Strong"

    print("PASS: Accuracy classification boundaries verified.")


def test_edge_cases():
    """
    Verify empty input, zero attempts,
    and invalid minimum attempt settings.
    """

    assert detect_weak_topics([]) == []

    assert detect_weak_topics([
        {
            "topic": "Empty Topic",
            "correct_answers": 0,
            "total_quizzes": 0,
        }
    ]) == []

    for invalid_value in [0, -1, 1.5, True]:
        try:
            detect_weak_topics([], min_attempts=invalid_value)
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"Expected ValueError for min_attempts={invalid_value}"
            )

    print("PASS: Empty and zero-attempt data handled correctly.")
    print("PASS: Invalid minimum attempt settings rejected.")


if __name__ == "__main__":
    test_weak_topic_detection()
    test_accuracy_boundaries()
    test_edge_cases()

    print("\nAll weak topic detection tests passed!")
