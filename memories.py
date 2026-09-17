#!/usr/bin/env python3

import re
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

    # Recall a memory by key.
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

    # Extract useful search terms from a query.
    def _get_search_terms(self, query):
        if not query:
            return []

        words = re.findall(r"[a-zA-Z0-9_]+", query.lower())

        stop_words = {
            "a",
            "an",
            "and",
            "are",
            "be",
            "can",
            "did",
            "do",
            "does",
            "for",
            "from",
            "how",
            "i",
            "is",
            "it",
            "my",
            "of",
            "on",
            "or",
            "the",
            "this",
            "to",
            "was",
            "what",
            "when",
            "where",
            "who",
            "why",
            "with",
            "you",
        }

        return [
            word
            for word in words
            if word not in stop_words and len(word) > 1
        ]

    # Search memories by relevant terms.
    def search(self, query, limit=10):
        terms = self._get_search_terms(query)

        if not terms:
            return []

        conditions = []
        parameters = []

        for term in terms:
            pattern = f"%{term}%"

            conditions.append(
                """
                (
                    LOWER(key) LIKE ?
                    OR LOWER(value) LIKE ?
                )
                """
            )

            parameters.extend([pattern, pattern])

        sql = f"""
            SELECT
                id,
                key,
                value,
                created_at,
                updated_at
            FROM memories
            WHERE {" OR ".join(conditions)}
            ORDER BY updated_at DESC
            LIMIT ?
        """

        parameters.append(limit)

        return self.db.conn.execute(
            sql,
            parameters
        ).fetchall()

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
    memories.remember("job", "Linux Engineer")
    memories.remember("favorite_color", "Red")

    results = memories.search(
        "What is my favorite color?"
    )

    for memory in results:
        print(
            f"{memory['key']}: {memory['value']}"
        )


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
