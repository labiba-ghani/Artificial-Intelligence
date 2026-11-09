
import tempfile
from pathlib import Path
from unittest.mock import patch

from database import db_manager


def test_database_persistence():
    with tempfile.TemporaryDirectory() as temp_dir:

        test_database = Path(temp_dir) / "test_memory.db"

        with patch.object(
            db_manager,
            "DATABASE_PATH",
            test_database,
        ):

            # Save a quiz interaction.
            record_id = db_manager.save_learning_interaction(
                interaction_type="quiz",
                topic="Python Functions",
                content="What does a function return?",
                score=1,
            )

            assert record_id == 1

            # Retrieve the saved interaction.
            history = db_manager.get_learning_history(limit=10)

            assert len(history) == 1
            assert history[0]["interaction_type"] == "quiz"
            assert history[0]["topic"] == "Python Functions"
            assert history[0]["score"] == 1

            # Verify that the SQLite file exists.
            assert test_database.exists()

            print("PASS: Learning interaction saved to SQLite.")
            print("PASS: Learning history retrieved correctly.")
            print("PASS: SQLite database file created.")

            # Simulate reopening the database by reading it
            # through a new database connection.
            reopened_history = db_manager.get_learning_history(
                limit=10
            )

            assert reopened_history == history

            print("PASS: Data persists across connections.")


def test_history_order_and_limit():
    with tempfile.TemporaryDirectory() as temp_dir:

        test_database = Path(temp_dir) / "test_memory.db"

        with patch.object(
            db_manager,
            "DATABASE_PATH",
            test_database,
        ):

            for number in range(3):
                db_manager.save_learning_interaction(
                    interaction_type="general_question",
                    topic=f"Topic {number}",
                    content=f"Answer {number}",
                )

            history = db_manager.get_learning_history(limit=2)

            assert len(history) == 2
            assert history[0]["topic"] == "Topic 2"
            assert history[1]["topic"] == "Topic 1"

            print("PASS: History ordering and limits work.")


def test_database_error_handling():
    with tempfile.TemporaryDirectory() as temp_dir:

        # A directory cannot be opened as a SQLite database file.
        invalid_database_path = Path(temp_dir)

        with patch.object(
            db_manager,
            "DATABASE_PATH",
            invalid_database_path,
        ):

            try:
                db_manager.get_learning_history(limit=10)

            except db_manager.sqlite3.Error:
                print("PASS: Database errors propagate correctly.")

            else:
                raise AssertionError(
                    "Expected a SQLite error for an invalid database path."
                )


if __name__ == "__main__":
    test_database_persistence()
    test_history_order_and_limit()
    test_database_error_handling()

    print("\nAll SQLite database tests passed!")
