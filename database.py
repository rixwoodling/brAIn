#!/usr/bin/env python3

import sqlite3
from pathlib import Path


class Database:
    """SQLite database layer."""

    # Initialize the database.
    def __init__(self, path=None):
        if path is None:
            path = Path(__file__).resolve().parent / "memory.db"

        self.path = Path(path)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    # Create the database tables.
    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                created_at TEXT NOT NULL
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        self.conn.commit()

    # Close the database.
    def close(self):
        self.conn.close()


# Initialize the database.
def initialize():
    try:
        return Database()
    except sqlite3.Error as e:
        print(f"Database initialization failed: {e}")
        return None


# Run the database pipeline.
def run_pipeline(db):
    if db is None:
        return

    print(f"Database: {db.path}")
    print("SQLite: OK")


# Shut down the database.
def shutdown(db):
    if db is not None:
        db.close()


# Run the database pipeline.
def main():
    db = initialize()
    run_pipeline(db)
    shutdown(db)


if __name__ == "__main__":
    main()
