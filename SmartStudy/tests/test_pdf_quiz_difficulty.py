
from unittest.mock import patch

from services.quiz_service import generate_quiz_from_pdf


def test_pdf_quiz_difficulty():
    """
    Verify that PDF quiz generation forwards the selected
    difficulty to the main quiz generator.
    """

    # Simulated PDF text chunks.
    chunks = [
        {
            "page_number": 1,
            "text": "A primary key uniquely identifies a database record."
        }
    ]

    # Simulated relevant content returned by the retriever.
    relevant_chunks = [
        {
            "page_number": 1,
            "text": "A primary key uniquely identifies a database record."
        }
    ]

    # Simulated validated quiz.
    mock_quiz = {
        "question": "What is a primary key?",
        "options": [
            "A unique identifier",
            "A table name",
            "A column type",
            "A database connection"
        ],
        "correct_answer": 0,
        "explanation": "A primary key uniquely identifies a record."
    }

    for difficulty in ["easy", "medium", "hard"]:

        with patch(
            "services.quiz_service.DocumentRetriever"
        ) as mock_retriever_class, patch(
            "services.quiz_service.generate_quiz",
            return_value=mock_quiz
        ) as mock_generate_quiz:

            # Simulate finding relevant PDF passages.
            mock_retriever = mock_retriever_class.return_value
            mock_retriever.search.return_value = relevant_chunks

            # Generate a quiz at the selected difficulty.
            quiz = generate_quiz_from_pdf(
                chunks=chunks,
                topic="Primary Keys",
                provider="groq",
                difficulty=difficulty
            )

            # Verify the retriever received the PDF chunks.
            mock_retriever_class.assert_called_once_with(chunks)

            # Verify the retriever searched the correct topic.
            mock_retriever.search.assert_called_once_with(
                question="Primary Keys",
                top_k=3
            )

            # Verify difficulty was forwarded correctly.
            mock_generate_quiz.assert_called_once_with(
                context=(
                    "Page 1:\n"
                    "A primary key uniquely identifies a database record."
                ),
                provider="groq",
                difficulty=difficulty
            )

            # Verify the quiz result was returned.
            assert quiz == mock_quiz

            print(
                f"PASS: PDF quiz forwards "
                f"{difficulty.upper()} difficulty."
            )


def test_pdf_quiz_default_difficulty():
    """
    Verify that PDF quizzes default to medium difficulty.
    """

    chunks = [
        {
            "page_number": 1,
            "text": "A primary key identifies a record."
        }
    ]

    with patch(
        "services.quiz_service.DocumentRetriever"
    ) as mock_retriever_class, patch(
        "services.quiz_service.generate_quiz",
        return_value={"question": "Test question"}
    ) as mock_generate_quiz:

        mock_retriever_class.return_value.search.return_value = chunks

        generate_quiz_from_pdf(
            chunks=chunks,
            topic="Primary Keys"
        )

        assert (
            mock_generate_quiz.call_args.kwargs["difficulty"]
            == "medium"
        )

        print("PASS: PDF quiz defaults to MEDIUM difficulty.")


if __name__ == "__main__":
    test_pdf_quiz_difficulty()
    test_pdf_quiz_default_difficulty()

    print("\nAll PDF quiz difficulty tests passed!")
