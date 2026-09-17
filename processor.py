#!/usr/bin/env python3

import json


class Processor:
    """Process prompts into persistent memories using an LLM."""

    # Initialize the processor.
    def __init__(self, llm):
        self.llm = llm

    # Process a prompt into a memory.
    def process(self, prompt):
        response = self.llm(
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
            prompt=prompt,
        )

        return self._parse_response(response)

    # Parse the LLM response.
    def _parse_response(self, response):
        if not response:
            return None

        response = response.strip()

        if response.startswith("```"):
            lines = response.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            response = "\n".join(lines).strip()

        try:
            data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            return None

        if "remember" in data:
            if not data.get("remember"):
                return None

            key = data.get("key")
            value = data.get("value")

            if not key or not value:
                return None

            return key, value

        if len(data) == 1:
            key, value = next(iter(data.items()))

            if key and value:
                return key, value

        return None
