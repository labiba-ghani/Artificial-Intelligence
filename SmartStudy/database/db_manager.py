
import sqlite3
from pathlib import Path


# Store the database inside the SmartStudy/database folder.
DATABASE_PATH = Path(__file__).resolve().parent / "smartstudy.db"


def initialize_database():
    """
    Create the learning history table if it does not exist.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interaction_type TEXT NOT NULL,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                score INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    print("SmartStudy database initialized successfully!")


def save_learning_interaction(
    interaction_type,
    topic,
    content,
    score=None
):
    """
    Save a learning interaction to the SQLite database.

    Returns the ID of the newly created record.
    """

    initialize_database()

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO learning_history (
                interaction_type,
                topic,
                content,
                score
            )
            VALUES (?, ?, ?, ?)
            """,
            (interaction_type, topic, content, score)
        )

        connection.commit()

        return cursor.lastrowid


def get_learning_history(limit=10):
    """
    Retrieve the most recent learning interactions.

    Returns a list of dictionaries.
    """

    initialize_database()

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                interaction_type,
                topic,
                content,
                score,
                created_at
            FROM learning_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        records = cursor.fetchall()

        return [dict(record) for record in records]

if __name__ == "__main__":
    initialize_database()
