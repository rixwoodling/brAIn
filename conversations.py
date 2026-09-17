#!/usr/bin/env python3

from datetime import datetime


class Conversations:
    """Conversation management."""

    # Initialize conversations.
    def __init__(self, db):
        self.db = db

    # Create a conversation.
    def create(self, title=None):
        now = datetime.now().isoformat(timespec="seconds")

        cursor = self.db.conn.execute(
            """
            INSERT INTO conversations (title, created_at)
            VALUES (?, ?)
            """,
            (title, now)
        )

        self.db.conn.commit()
        return cursor.lastrowid

    # Get a conversation.
    def get(self, conversation_id):
        return self.db.conn.execute(
            """
            SELECT id, title, created_at
            FROM conversations
            WHERE id = ?
            """,
            (conversation_id,)
        ).fetchone()

    # Get all conversations.
    def get_all(self):
        return self.db.conn.execute(
            """
            SELECT id, title, created_at
            FROM conversations
            ORDER BY id DESC
            """
        ).fetchall()


# Initialize the conversation system.
def initialize():
    try:
        from .database import Database
        return Conversations(Database())
    except ImportError as e:
        print(f"Conversation initialization failed: {e}")
        return None


# Run the conversation pipeline.
def run_pipeline(conversations):
    if conversations is None:
        return

    conversation_id = conversations.create("Test Conversation")
    conversation = conversations.get(conversation_id)

    print(f"Conversation: {conversation['id']}")
    print(f"Title: {conversation['title']}")


# Shut down the conversation system.
def shutdown(conversations):
    if conversations is not None:
        conversations.db.close()


# Run the conversation pipeline.
def main():
    conversations = initialize()
    run_pipeline(conversations)
    shutdown(conversations)


if __name__ == "__main__":
    main()
