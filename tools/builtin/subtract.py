from tools.base import BaseTool


class SubtractTool(BaseTool):

    def __init__(self):
        super().__init__(
            name="subtract",
            description="Subtracts two numbers.",
            parameters={
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
                "required": ["a", "b"],
            },
        )

    def execute(self, a, b, **kwargs):
        return a - b

