
from services.quiz_service import generate_quiz_from_pdf


def test_pdf_quiz():
    """
    Test quiz generation using sample PDF chunks.
    """

    chunks = [
        {
            "chunk_id": 1,
            "page_number": 1,
            "text": (
                "A primary key uniquely identifies each row "
                "in a database table. A primary key cannot "
                "contain NULL values."
            )
        },
        {
            "chunk_id": 2,
            "page_number": 2,
            "text": (
                "A foreign key creates a relationship "
                "between two database tables. It references "
                "a primary key in another table."
            )
        },
        {
            "chunk_id": 3,
            "page_number": 3,
            "text": (
                "Database normalization organizes data "
                "to reduce redundancy and improve "
                "data integrity."
            )
        }
    ]

    quiz = generate_quiz_from_pdf(
        chunks=chunks,
        topic="primary key",
        provider="ollama"
    )

    print("\nGenerated Question:")
    print(quiz["question"])

    print("\nAnswer Options:")
    for index, option in enumerate(quiz["options"]):
        print(f"{index}. {option}")

    print("\nCorrect Answer Index:")
    print(quiz["correct_answer"])

    print("\nExplanation:")
    print(quiz["explanation"])

    assert len(quiz["options"]) == 4
    assert quiz["correct_answer"] in range(4)

    print("\nPASS: RAG-based PDF quiz generated successfully.")


if __name__ == "__main__":
    test_pdf_quiz()
