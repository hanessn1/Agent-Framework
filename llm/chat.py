from llm.client import LLMClient
from config import MODEL, REASONING_EFFORT
from agent.response import AgentResponse, ToolCall, FunctionCall
from agent.messages import MessageHistory
import logging

logger = logging.getLogger(__name__)


class ChatLLM:
	def __init__(self):
		self.client = LLMClient()
		self.model = MODEL

	def complete(self, messages, tools=None, stream=False):
		if isinstance(messages, MessageHistory):
			messages = messages.history

		if stream:
			return self.stream(messages, tools)

		return self._complete(messages, tools)

	def _complete(self, messages, tools):
		kwargs = {
			"model": self.model,
			"messages": messages,
			"stream": False,
			"reasoning_effort": REASONING_EFFORT
		}
		if tools:
			kwargs["tools"] = tools

		response = self.client.chat.create(**kwargs)
		logger.trace(f"Response from LLM: {response}")

		return self._parse(response)

	def stream(self, messages, tools=None):
		kwargs = {
			"model": self.model,
			"messages": messages,
			"stream": True,
			"reasoning_effort": REASONING_EFFORT
		}
		if tools:
			kwargs["tools"] = tools

		raw_stream = self.client.chat.create(**kwargs)
		logger.debug(f"Starting llm stream...")
		content_parts = []
		tool_calls_map = {}
		finish_reason = None

		for chunk in raw_stream:
			logger.trace(f"### Chunk: {chunk}")
			if not chunk.choices:
				continue

			delta = chunk.choices[0].delta
			logger.trace(f"Chunk delta: {delta}")

			delta_content = None
			if delta.content:
				delta_content = delta.content
				content_parts.append(delta_content)

			if delta.tool_calls:
				logger.trace(f"Chunk delta tool call: {delta.tool_calls}")
				for tc in delta.tool_calls:
					idx = tc.index
					if idx not in tool_calls_map:
						tool_calls_map[idx] = {
							"id": tc.id,
							"name": tc.function.name,
							"arguments": "",
						}
					if tc.id:
						tool_calls_map[idx]["id"] = tc.id
					if tc.function:
						if tc.function.name:
							tool_calls_map[idx]["name"] = tc.function.name
						if tc.function.arguments:
							tool_calls_map[idx]["arguments"] += tc.function.arguments

			if chunk.choices[0].finish_reason:
				finish_reason = chunk.choices[0].finish_reason

			logger.trace(f"Yielding delta content: {delta_content}")
			yield delta_content, None

		reconstructed_tool_calls = []
		logger.trace(f"Tool calls map: {tool_calls_map}")
		for idx in sorted(tool_calls_map.keys()):
			tc_data = tool_calls_map[idx]
			reconstructed_tool_calls.append(
				ToolCall(
					id=tc_data["id"],
					function=FunctionCall(
						name=tc_data["name"],
						arguments=tc_data["arguments"],
					),
				)
			)

		logger.trace(f"Stream completed. Full content: {''.join(content_parts)}")
		agent_response = AgentResponse(
			content="".join(content_parts),
			tool_calls=reconstructed_tool_calls,
			finish_reason=finish_reason,
			raw=raw_stream,
		)

		yield None, agent_response

	def _parse(self, response):
		message = response.choices[0].message
		logger.trace(f"Parsed message object: {message}")

		tool_calls = []
		if message.tool_calls:
			logger.trace(f"Found tool calls...")
			for tc in message.tool_calls:
				logger.trace(f"### Tool call ### ")
				logger.trace(tc)
				fn_name = tc.function.name
				fn_args = tc.function.arguments
				tool_calls.append(
					ToolCall(
						id=tc.id,
						function=FunctionCall(name=fn_name, arguments=fn_args),
					)
				)

		agent_response = AgentResponse(
			content=message.content,
			tool_calls=tool_calls,
			finish_reason=response.choices[0].finish_reason,
			raw=response,
		)
		logger.trace(f"Created agent response: {agent_response}")
		return agent_response
