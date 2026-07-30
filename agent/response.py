from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class AgentResponse:
    """
    Normalized LLM repsonse.
    """

    content: str = ""
    tool_calls: List[Any] = field(default_factory=list)
    finish_reason: str = ""
    raw: Any = None

    @property
    def has_tool_calls(self):
        return len(self.tool_calls) > 0
