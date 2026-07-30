from client import LLMClient
from config import MODEL, REASONING_EFFORT
from agent.response import AgentResponse


class ChatLLM:
    def __init__(self):
        self.client = LLMClient()
        self.model = MODEL

    def complete(self, messages, tools=None, stream=False):
        if stream:
            return self._stream(messages, tools)

        return self._complete(messages, tools)

    def _complete(self, messages, tools):
        response = self.client.chat.create(
            model=self.model,
            messages=messages,
            tools=tools,
            reasoning_effort=REASONING_EFFORT,
            stream=False,
        )

        return self._parse(response)

    def _stream(self, messages, tools):
        stream = self.client.chat.create(
            model=self.model,
            messages=messages,
            tools=tools,
            reasoning_effort=REASONING_EFFORT,
            stream=True,
        )

        return self._parse_stream(stream)

    def _parse(self, response):
        message = response.choices[0].message

        return AgentResponse(
            content=message,
            tool_calls=message.tool_calls or [],
            finish_reason=response.choices[0].finish_reason,
            raw=response,
        )

    def _parse_stream(self, stream):
        """
        TODO
        Collect streamed content
        Reconstruct tool calls
        Return AgentResponse
        """
        raise NotImplementedError()
