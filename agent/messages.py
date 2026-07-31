from typing import List, Dict, Any
from agent.response import ToolCall
import logging

logger=logging.getLogger(__name__)


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

    def add_assistant_tool_call(self, tool_calls: List[ToolCall], content: str):
        tool_call_json={
            "role": "assistant",
            "content": content,
            "tool_calls": [tc.to_dict() for tc in tool_calls],
        }
        logger.debug("Adding assistant tool call request...")
        logger.debug(tool_call_json)
        self.messages.append(tool_call_json)

    def add_tool_result(self, tool_call_id: str, content: str):
        tool_result_json={"role": "tool", "tool_call_id": tool_call_id, "content": content}
        logger.debug(f"Tool result json message: {tool_result_json}")
        self.messages.append(tool_result_json)

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)
