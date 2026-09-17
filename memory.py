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

            conversation = self.conversations.get_latest()

            if conversation is None:
                self.conversation_id = (
                    self.conversations.create()
                )
            else:
                self.conversation_id = conversation["id"]

        except ImportError as e:
            print(
                f"Memory initialization failed: {e}",
                file=sys.stderr
            )

            self.db = None
            self.conversations = None
            self.memories = None
            self.processor = None
            self.conversation_id = None

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

    # Get recent messages from a conversation.
    def get_messages(self, conversation_id=None, limit=10):
        if self.conversations is None:
            return []

        if conversation_id is None:
            conversation_id = self.conversation_id

        messages = self.conversations.get_messages(
            conversation_id
        )

        return messages[-limit:]

    # Process a prompt for potential memories.
    def process(self, prompt):
        if self.memories is None or self.processor is None:
            return

        memory = self.processor.process(prompt)

        if memory is None:
            return

        key, value = memory
        self.memories.remember(key, value)

    # Recall relevant memories and recent conversation history.
    def recall(self, prompt):
        if self.memories is None:
            return ""

        context = []

        memories = self.memories.search(prompt)

        if memories:
            context.append("Relevant user information:")

            for memory in memories:
                context.append(
                    f"{memory['key']}: {memory['value']}"
                )

        messages = self.get_messages()

        if messages:
            context.append("\nRecent conversation:")

            for message in messages:
                context.append(
                    f"{message['role']}: {message['content']}"
                )

        if not context:
            return ""

        return "\n".join(context) + "\n\n"

    # Store a user message.
    def store_user_message(self, content):
        if self.conversation_id is None:
            return None

        return self.add_message(
            self.conversation_id,
            "user",
            content
        )

    # Store an assistant message.
    def store_assistant_message(self, content):
        if self.conversation_id is None:
            return None

        return self.add_message(
            self.conversation_id,
            "assistant",
            content
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
    conversation_id = memory.conversation_id

    if conversation_id is None:
        return

    memory.store_user_message(
        "My name is Rix."
    )

    memory.store_assistant_message(
        "Nice to meet you, Rix!"
    )

    context = memory.recall(
        "What is my name?"
    )

    print(context)


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
