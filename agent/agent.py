import json
from agent.response import AgentResponse
from agent.messages import MessageHistory
from llm.chat import ChatLLM
from typing import List
from config import MAX_STEPS
import logging

logger=logging.getLogger(__name__)


class Agent:

    def __init__(self, llm: ChatLLM, history: MessageHistory, tools:List=None, stream:bool=False):
        self.llm = llm
        self.history = history
        self.tools = tools
        self.stream = stream

    def run(self, query: str):
        """Public API"""
        if self.stream:
            return self._run_stream(query)
        else:
            return self._run_sync(query)

    def _run_sync(self, query: str):
        self.history.add_user(query)

        steps=0
        while steps<MAX_STEPS:
            steps+=1
            response = self.chat()

            if response.tool_calls:
                logger.debug("Tool call found in agent response...")
                self.handle_tool_calls(response)
                continue

            self.history.add_assistant(response.content)
            print(response.content)
            return response.content

    def _run_stream(self, query: str):
        self.history.add_user(query)
        final_response = None
        steps=0

        while steps<MAX_STEPS:
            steps+=1
            schemas = self.tools.schemas()
            final_response = None

            for delta_text, response in self.llm.stream(messages=self.history.messages, tools=schemas):
                if delta_text:
                    print(delta_text, end="", flush=True)
                if response is not None:
                    final_response = response

            if final_response and final_response.tool_calls:
                self.handle_tool_calls(final_response)
                continue

            if final_response:
                self.history.add_assistant(final_response.content)
            break

        return final_response

    def chat(self):
        """LLM"""
        schemas = self.tools.schemas()
        # logger.debug(f"Tool calls schema list: {schemas}",)
        return self.llm.complete(messages=self.history.messages, tools=schemas, stream=False)

    def handle_tool_calls(self, response: AgentResponse):
        self.history.add_assistant_tool_call(response.tool_calls, content=response.content)

        for tool_call in response.tool_calls:
            result = self.call_tool(tool_call)
            self.history.add_tool_result(tool_call.id, str(result))

    def call_tool(self, tool_call):
        args = (
            json.loads(tool_call.function.arguments)
            if tool_call.function.arguments
            else {}
        )
        result=self.tools.execute(tool_call.function.name, **args)
        logger.debug(f"Tool called: {tool_call}")
        logger.debug(f"Tool call result: {result}")
        return result
