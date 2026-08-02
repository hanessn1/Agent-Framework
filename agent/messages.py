from typing import List
from agent.response import ToolCall
from agent.persistence.base import BasePersistence
from agent.persistence.memory_storage import MemoryPersistence
import logging

logger = logging.getLogger(__name__)


class MessageHistory:
	"""
	Maintains conversation history.
	Responsible only for storing and manipulating messages.
	"""

	def __init__(
			self,
			system_prompt: str = "",
			max_working_messages: int = 20,
			persistence: BasePersistence = None,
	):
		self.max_working_messages = max_working_messages
		self.persistence = persistence or MemoryPersistence()
		self.messages = self.persistence.load()
		if not self.messages and system_prompt:
			self.add_system(system_prompt)

	def get_messages_for_llm(self):
		"""Dynamically computes the sliding window before every LLM call."""
		if len(self.messages) <= self.max_working_messages + 1:
			return self.messages

		# Preserve system prompt and take last N messages
		logger.debug(f"History length: `{len(self.messages)}` exceeded capacity.")
		system_msg = self.messages[0]
		recent_msgs = self.messages[-self.max_working_messages:]
		return [system_msg] + recent_msgs

	@property
	def history(self):
		return self.messages

	def clear(self):
		self.messages.clear()

	def add_system(self, content: str):
		self.messages.append({"role": "system", "content": content})
		self._save()

	def add_user(self, content: str):
		self.messages.append({"role": "user", "content": content})
		self._save()

	def add_assistant(self, content: str):
		self.messages.append({"role": "assistant", "content": content})
		self._save()

	def add_assistant_tool_call(self, tool_calls: List[ToolCall], content: str):
		tool_call_json = {
			"role": "assistant",
			"content": content,
			"tool_calls": [tc.to_dict() for tc in tool_calls],
		}
		logger.trace("Adding assistant tool call request...")
		logger.trace(tool_call_json)
		self.messages.append(tool_call_json)
		self._save()

	def add_tool_result(self, tool_call_id: str, content: str):
		tool_result_json = {
			"role": "tool",
			"tool_call_id": tool_call_id,
			"content": content,
		}
		logger.trace(f"Tool result json message: {tool_result_json}")
		self.messages.append(tool_result_json)
		self._save()

	def _save(self):
		"""Internal helper to trigger auto-save after message mutations."""
		self.persistence.save(self.messages)

	def __iter__(self):
		return iter(self.messages)

	def __len__(self):
		return len(self.messages)
