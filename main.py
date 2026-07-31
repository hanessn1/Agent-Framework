from agent.messages import MessageHistory
from agent.agent import Agent
from llm.chat import ChatLLM
from tools.registry import ToolRegistry
from tools.builtin.add import AddTool
from tools.builtin.multiply import MultiplyTool
from tools.builtin.subtract import SubtractTool
from tools.builtin.time import TimeTool
from logger import setup_logging


registry = ToolRegistry([
    AddTool(),
    MultiplyTool(),
    SubtractTool(),
    TimeTool(),
])

history = MessageHistory("You are a helpful assistant. You use tools when appropriate.")

agent = Agent(
    llm=ChatLLM(),
    history=history,
    tools=registry,
    stream=True,
)

if __name__ == "__main__":
    setup_logging()
    agent.run("What is the current time? and what is 238*7234?")
