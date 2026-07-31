from typing import List
from tools.base import BaseTool


class ToolRegistry:
    def __init__(self, tools: List[BaseTool]):
        self.tools = {t.name: t for t in tools}

    def schemas(self):
        return [t.schema() for t in self.tools.values()]

    def execute(self, name, **kwargs):
        tool = self.tools[name]
        return tool.execute(**kwargs)
