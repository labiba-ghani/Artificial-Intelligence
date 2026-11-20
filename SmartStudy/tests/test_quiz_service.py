
import json
import unittest

from services.quiz_service import validate_quiz_response


class TestQuizService(unittest.TestCase):
    """Automated tests for quiz response validation."""

    def test_valid_quiz(self):
        """Verify that a correctly formatted quiz is accepted."""

        sample = {
            "question": "What is a primary key?",
            "options": [
                "Unique identifier",
                "Password",
                "Backup",
                "Query",
            ],
            "correct_answer": 0,
            "explanation": "It uniquely identifies rows.",
        }

        response = json.dumps(sample)

        result = validate_quiz_response(response)

        self.assertEqual(
            result["question"],
            sample["question"],
        )

        self.assertEqual(
            result["correct_answer"],
            0,
        )

        self.assertEqual(
            len(result["options"]),
            4,
        )

    def test_invalid_quiz(self):
        """Verify that an incorrectly formatted quiz is rejected."""

        invalid_sample = {
            "question": "What is a primary key?",
            "options": [
                "Unique identifier",
                "Password",
            ],
            "correct_answer": 5,
            "explanation": "It uniquely identifies rows.",
        }

        response = json.dumps(invalid_sample)

        with self.assertRaises(ValueError):
            validate_quiz_response(response)


if __name__ == "__main__":
    unittest.main()
