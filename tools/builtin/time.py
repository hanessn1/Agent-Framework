from datetime import datetime
from tools.base import BaseTool


class TimeTool(BaseTool):

    def __init__(self):
        super().__init__(
            name="get_time",
            description="Returns the current local date and time.",
            parameters={},
        )

    def execute(self, **kwargs):
        return str(datetime.now())