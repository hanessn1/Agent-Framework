from tools.base import BaseTool
import os


class PwdTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="get_cwd",
            description="Returns the current working directory path of the agent process.",
            parameters={"type": "object", "properties": {}, "required": []},
        )

    def execute(self, **kwargs):
        try:
            return os.getcwd()
        except Exception as e:
            return f"Error getting current working directory: {str(e)}"
