import sys

from agent.messages import MessageHistory
from agent.agent import Agent
from llm.chat import ChatLLM
from mcp_client.adapter import load_mcp_tools
from tools.registry import ToolRegistry
from agent.persistence import MemoryPersistence
from planner.planner import Planner
from planner.executor import Executor
from logger import setup_logging

setup_logging()

# Load tools from all domain MCP servers
math_tools = load_mcp_tools(sys.executable, ["mcp_servers/math_server.py"])
fs_tools = load_mcp_tools(sys.executable, ["mcp_servers/filesystem_server.py"])
system_tools = load_mcp_tools(sys.executable, ["mcp_servers/system_server.py"])

# External MCP tools
external_mcp_tools = load_mcp_tools(sys.executable, ["mcp_servers/test_mcp_server.py"])

registry = ToolRegistry([
	*math_tools,
	*fs_tools,
	*system_tools,
	*external_mcp_tools,
])

SYSTEM_PROMPT = """You are a helpful, versatile AI assistant equipped with tools.
- When asked a question, always inspect and verify facts using your available tools.
- If a tool call fails or returns an error, analyze the error message in your history, self-correct your parameters, and try again.
- Provide clear and accurate responses based on observed tool results.
"""

agent_persistence = MemoryPersistence()
planner_persistence = MemoryPersistence()

history = MessageHistory(
	system_prompt=SYSTEM_PROMPT,
	persistence=agent_persistence
)
llm = ChatLLM()

agent = Agent(
	llm=llm,
	history=history,
	tools=registry,
	stream=True,
)

planner = Planner(llm=llm, persistence=planner_persistence)
executor = Executor(agent=agent)


def run_with_planning(user_goal: str):
	plan = planner.create_plan(user_goal)
	return executor.execute_plan(plan)


if __name__ == "__main__":
	# Standard single query (no planning needed for simple questions)
	agent.run(
		"Do a search inside this directory. tell me what do you find. how many python files are there?"
	)

	# Complex goal using Planning & Execution!
	# run_with_planning("How many python files are here? consider any folders which might have python files too.")

	# test invoking MCP tool
	# agent.run("Use the uppercase_text tool to convert 'hello world from mcp_client' to uppercase.")
