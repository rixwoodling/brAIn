#!/usr/bin/env python3

import json
from anthropic import Anthropic


class Processor:
    """Process prompts into persistent memories using an LLM."""

    # Initialize the processor.
    def __init__(self):
        self.client = Anthropic()
        self.model = "claude-haiku-4-5-20251001"

    # Process a prompt into a memory.
    def process(self, prompt):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=256,
            system="""
Determine whether the user's message contains information worth
remembering long-term.

If it does, return exactly one JSON object:

{
  "remember": true,
  "key": "short_key",
  "value": "short_value"
}

If it does not, return:

{
  "remember": false
}

Remember information such as names, preferences, persistent interests,
work, skills, or other facts about the user that are likely to remain
useful in future conversations.

Do not remember temporary activities, questions, requests, or casual
conversation.

Return JSON only.
""",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        return self._parse_response(response)

    # Parse the LLM response.
    def _parse_response(self, response):
        try:
            data = json.loads(response.content[0].text)
        except (json.JSONDecodeError, IndexError, AttributeError):
            return None

        if not data.get("remember"):
            return None

        key = data.get("key")
        value = data.get("value")

        if not key or not value:
            return None

        return key, value
