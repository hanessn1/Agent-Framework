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
from logger import setup_logging


registry = ToolRegistry([
    AddTool(),
    MultiplyTool(),
    SubtractTool(),
    TimeTool(),
    ListFilesTool(),
    ReadFileTool()
])

SYSTEM_PROMPT="""You are a helpful, versatile AI assistant equipped with tools.
- When asked a question, always inspect and verify facts using your available tools before answering.
- If a tool call fails or returns an error, analyze the error message in your history, self-correct your parameters, and try again.
- Provide clear and accurate responses based on observed tool results.
"""

history = MessageHistory(SYSTEM_PROMPT)

agent = Agent(
    llm=ChatLLM(),
    history=history,
    tools=registry,
    stream=False,
)

if __name__ == "__main__":
    setup_logging()
    agent.run("Which files mentions kubernetes in the current directory?")
