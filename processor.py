#!/usr/bin/env python3

class Processor:
    """Process candidate prompts into memories."""

    # Process a prompt into a memory.
    def process(self, prompt):
        text = prompt.strip()

        if text.lower().startswith("my name is "):
            value = text[11:].strip().rstrip(".")

            if value:
                return "name", value

        if text.lower().startswith("i like "):
            value = text[7:].strip().rstrip(".")

            if value:
                return "likes", value

        return None
