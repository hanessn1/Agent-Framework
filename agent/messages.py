from typing import List, Dict, Any


class MessageHistory:
    """
    Maintains conversation history.
    Responsible only for storing and manipulating messages.
    """

    def __init__(self, system_prompt: str = ""):
        self.messages: List[Dict[str, Any]] = []

        if system_prompt:
            self.add_system(system_prompt)

    @property
    def history(self):
        return self.messages

    def clear(self):
        self.messages.clear()

    def add_system(self, content: str):
        self.messages.append({"role": "system", "content": content})

    def add_user(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def add_assistant(self, content: str):
        self.messages.append({"role": "assistant", "content": content})

    def add_assistant_tool_call(self, tool_call):
        self.messages.append({"role": "assistant", "tool_calls": tool_call})

    def add_tool_result(self, tool_call_id: str, content: str):
        self.messages.append(
            {"role": "tool", "tool_call_id": tool_call_id, "content": content}
        )

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)
