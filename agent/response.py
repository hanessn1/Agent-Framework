from typing import List, Any


class FunctionCall:
	def __init__(self, name: str = "", arguments: str = ""):
		self.name = name
		self.arguments = arguments

	def __str__(self):
		return f"FunctionCall(name={self.name!r}, arguments={self.arguments!r})"

	def __repr__(self):
		return self.__str__()


class ToolCall:
	def __init__(self, id: str = "", function: FunctionCall = None, type: str = "function"):
		self.id = id
		self.function = function
		self.type = type

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"type": self.type,
			"function": {
				"name": self.function.name,
				"arguments": self.function.arguments,
			},
		}

	def __str__(self):
		return f"ToolCall(id={self.id!r}, function={self.function}, type={self.type!r})"

	def __repr__(self):
		return self.__str__()


class AgentResponse:
	"""Normalized LLM response."""

	def __init__(
			self, content: str = "", tool_calls: List[ToolCall] = None, finish_reason: str = "", raw: Any = None
	):
		self.content = content
		self.tool_calls = tool_calls
		self.finish_reason = finish_reason
		self.raw = raw

	@property
	def has_tool_calls(self):
		return len(self.tool_calls) > 0

	def __str__(self):
		return (
			f"AgentResponse("
			f"content={self.content!r}, "
			f"tool_calls={self.tool_calls}, "
			f"finish_reason={self.finish_reason!r})"
		)

	def __repr__(self):
		return self.__str__()
