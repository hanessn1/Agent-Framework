import json
from agent.response import AgentResponse
from messages import MessageHistory


class Agent:

    def __init__(self, llm, history: MessageHistory, tools, stream=False):
        self.llm = llm
        self.history = history
        self.tools = tools
        self.stream = stream

    def run(self, query):
        """Public API"""

        self.history.add_user(query)

        while True:
            response = self.chat()

            if response.tool_calls:
                self.handle_tool_calls(response)
                continue

            self.history.add_assistant(response.content)
            return response.content

    def chat(self):
        """LLM"""

        raw = self.llm.chat(
            messages=self.history.messages, tools=self.tools.schemas, stream=self.stream
        )
        return self.parse_response(raw)

    def handle_tool_calls(self, response: AgentResponse):
        self.history.add_assistant_tool_call(response.tool_calls)

        for tool_call in response.tool_calls:
            result = self.call_tool(tool_call)
            self.history.add_tool_result(tool_call.id, result)

    def call_tool(self, tool_call):
        args = json.loads(tool_call.function.arguments)
        return self.tools.execute(tool_call.function.name, args)
