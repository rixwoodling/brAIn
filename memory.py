#!/usr/bin/env python3

import sys


class Memory:
    """Public interface to the memory system."""

    # Initialize the memory system.
    def __init__(self, llm):
        try:
            from .database import Database
            from .conversations import Conversations
            from .memories import Memories
            from .processor import Processor

            self.db = Database()
            self.conversations = Conversations(self.db)
            self.memories = Memories(self.db)
            self.processor = Processor(llm)

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

    # Add a message to a conversation.
    def add_message(self, conversation_id, role, content):
        if self.conversations is None:
            return None

        return self.conversations.add_message(
            conversation_id,
            role,
            content
        )

    # Get messages from a conversation.
    def get_messages(self, conversation_id):
        if self.conversations is None:
            return []

        return self.conversations.get_messages(
            conversation_id
        )

    # Process a prompt for potential memories.
    def process(self, prompt):
        if self.memories is None or self.processor is None:
            return

        memory = self.processor.process(prompt)

        if memory is None:
            return

        key, value = memory
        self.memories.remember(key, value)

    # Recall stored memories.
    def recall(self, prompt):
        if self.memories is None:
            return ""

        memories = self.memories.get_all()

        if not memories:
            return ""

        context = []

        for memory in memories:
            context.append(
                f"{memory['key']}: {memory['value']}"
            )

        return (
            "Known user information:\n"
            + "\n".join(context)
            + "\n\n"
        )

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
def initialize(llm):
    return Memory(llm)


# Run the memory pipeline.
def run_pipeline(memory):
    conversation_id = memory.create_conversation(
        "Test Conversation"
    )

    if conversation_id is None:
        return

    memory.add_message(
        conversation_id,
        "user",
        "My name is Rix."
    )

    memory.add_message(
        conversation_id,
        "assistant",
        "Nice to meet you, Rix!"
    )

    messages = memory.get_messages(
        conversation_id
    )

    for message in messages:
        print(
            f"{message['role']}: "
            f"{message['content']}"
        )


# Shut down the memory system.
def shutdown(memory):
    memory.close()


# Run the memory pipeline.
def main():
    memory = initialize(None)
    run_pipeline(memory)
    shutdown(memory)


if __name__ == "__main__":
    main()
