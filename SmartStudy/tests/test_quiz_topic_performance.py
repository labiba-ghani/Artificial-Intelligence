
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from database import db_manager


def test_quiz_topic_performance():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_db = Path(temp_dir) / "test_learning.db"

        with patch.object(db_manager, "DATABASE_PATH", test_db):
            db_manager.initialize_database()

            # Insert sample quiz results.
            sample_records = [
                ("quiz", "Primary Keys", "Test quiz", 1),
                ("quiz", "primary keys", "Test quiz", 0),
                ("quiz", " PRIMARY KEYS ", "Test quiz", 1),
                ("quiz", "Foreign Keys", "Test quiz", 1),
                ("quiz", "Foreign Keys", "Test quiz", 1),
                ("general_question", "Primary Keys", "Test question", None),
            ]

            # Close the SQLite connection properly after inserting data.
            with closing(sqlite3.connect(test_db)) as connection:
                with connection:
                    connection.executemany(
                        """
                        INSERT INTO learning_history
                            (interaction_type, topic, content, score)
                        VALUES (?, ?, ?, ?)
                        """,
                        sample_records,
                    )

            # Retrieve quiz performance grouped by topic.
            results = db_manager.get_quiz_topic_performance()

            assert len(results) == 2

            performance = {
                record["topic"]: record
                for record in results
            }

            # Verify Primary Keys results.
            assert performance["primary keys"]["total_quizzes"] == 3
            assert performance["primary keys"]["correct_answers"] == 2

            # Verify Foreign Keys results.
            assert performance["foreign keys"]["total_quizzes"] == 2
            assert performance["foreign keys"]["correct_answers"] == 2

            print("PASS: Quiz results grouped by topic.")
            print("PASS: Topic names normalized correctly.")
            print("PASS: Correct answers counted accurately.")
            print("PASS: Non-quiz interactions excluded.")


if __name__ == "__main__":
    test_quiz_topic_performance()

    print("\nAll topic performance tests passed!")
