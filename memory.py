#!/usr/bin/env python3

import sys


class Memory:
    """Public interface to the memory system."""

    # Initialize the memory system.
    def __init__(self):
        try:
            from .database import Database
            from .conversations import Conversations
            from .memories import Memories
            from .processor import Processor

            self.db = Database()
            self.conversations = Conversations(self.db)
            self.memories = Memories(self.db)
            self.processor = Processor()

        except ImportError as e:
            print(f"Memory initialization failed: {e}", file=sys.stderr)
            self.db = None
            self.conversations = None
            self.memories = None
            self.processor = None

    # Create a conversation.
    def create_conversation(self, title=None):
        if self.conversations is None:
            return None

        return self.conversations.create(title)

    # Get a conversation.
    def get_conversation(self, conversation_id):
        if self.conversations is None:
            return None

        return self.conversations.get(conversation_id)

    # Get all conversations.
    def get_conversations(self):
        if self.conversations is None:
            return []

        return self.conversations.get_all()

    # Determine whether a prompt may contain a durable memory.
    def is_candidate(self, prompt):
        text = prompt.strip().lower()

        patterns = (
            "my name is ",
            "people call me ",
            "i prefer ",
            "i like ",
            "i don't like ",
            "i work with ",
            "i work on ",
            "i'm working on ",
            "i am working on ",
            "remember that ",
        )

        return text.startswith(patterns)

    # Process a prompt for potential memories.
    def process(self, prompt):
        if self.memories is None or self.processor is None:
            return

        if not self.is_candidate(prompt):
            return

        memory = self.processor.process(prompt)

        if memory is None:
            return

        key, value = memory
        self.memories.remember(key, value)

    # Recall memories relevant to the prompt.
    def recall(self, prompt):
        if self.memories is None:
            return ""

        text = prompt.lower()

        if "what is my name" in text or "what's my name" in text:
            name = self.memories.recall("name")

            if name:
                return f"User's name is {name}.\n\n"

        if "what do i like" in text:
            likes = self.memories.recall("likes")

            if likes:
                return f"User likes {likes}.\n\n"

        return ""

    # Forget a memory.
    def forget(self, key):
        if self.memories is None:
            return

        self.memories.forget(key)

    # Get all memories.
    def get_memories(self):
        if self.memories is None:
            return []

        return self.memories.get_all()

    # Close the memory system.
    def close(self):
        if self.db is not None:
            self.db.close()


# Initialize the memory system.
def initialize():
    return Memory()


# Run the memory pipeline.
def run_pipeline(memory):
    conversation_id = memory.create_conversation("Test Conversation")

    if conversation_id is not None:
        print(f"Conversation: {conversation_id}")


# Shut down the memory system.
def shutdown(memory):
    memory.close()


# Run the memory chatbot pipeline.
def main():
    memory = initialize()
    run_pipeline(memory)
    shutdown(memory)


if __name__ == "__main__":
    main()
