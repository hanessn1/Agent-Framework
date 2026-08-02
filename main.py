from agent.messages import MessageHistory
from agent.agent import Agent
from llm.chat import ChatLLM
from tools.registry import ToolRegistry
from tools.builtin.add import AddTool
from tools.builtin.multiply import MultiplyTool
from tools.builtin.subtract import SubtractTool
from tools.builtin.time import TimeTool
from tools.builtin.list_files import ListFilesTool
from tools.builtin.read_file import ReadFileTool
from tools.builtin.get_pwd import PwdTool
from agent.persistence import MemoryPersistence
from planner.planner import Planner
from planner.executor import Executor
from logger import setup_logging

setup_logging()

registry = ToolRegistry([
	AddTool(),
	MultiplyTool(),
	SubtractTool(),
	TimeTool(),
	PwdTool(),
	ListFilesTool(),
	ReadFileTool()
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
