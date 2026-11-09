
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


if __name__ == "__main__":
    initialize_database()

