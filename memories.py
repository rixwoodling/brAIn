#!/usr/bin/env python3

from datetime import datetime


class Memories:
    """Persistent memory management."""

    # Initialize memories.
    def __init__(self, db):
        self.db = db

    # Store or update a memory.
    def remember(self, key, value):
        now = datetime.now().isoformat(timespec="seconds")

        self.db.conn.execute(
            """
            INSERT INTO memories (
                key, value, created_at, updated_at
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
            """,
            (key, value, now, now)
        )

        self.db.conn.commit()

    # Recall a memory.
    def recall(self, key):
        row = self.db.conn.execute(
            """
            SELECT value
            FROM memories
            WHERE key = ?
            """,
            (key,)
        ).fetchone()

        if row is None:
            return None

        return row["value"]

    # Forget a memory.
    def forget(self, key):
        self.db.conn.execute(
            """
            DELETE FROM memories
            WHERE key = ?
            """,
            (key,)
        )

        self.db.conn.commit()

    # Get all memories.
    def get_all(self):
        return self.db.conn.execute(
            """
            SELECT id, key, value, created_at, updated_at
            FROM memories
            ORDER BY updated_at DESC
            """
        ).fetchall()


# Initialize the memory system.
def initialize():
    try:
        from .database import Database
        return Memories(Database())
    except ImportError as e:
        print(f"Memory initialization failed: {e}")
        return None


# Run the memory pipeline.
def run_pipeline(memories):
    if memories is None:
        return

    memories.remember("name", "Rix")
    print("Name:", memories.recall("name"))


# Shut down the memory system.
def shutdown(memories):
    if memories is not None:
        memories.db.close()


# Run the memory pipeline.
def main():
    memories = initialize()
    run_pipeline(memories)
    shutdown(memories)


if __name__ == "__main__":
    main()
