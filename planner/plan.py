from typing import Literal


class TaskStep:
    def __init__(
        self,
        id: int,
        description: str,
        status: Literal["pending", "running", "completed", "failed"] = "pending",
        result: str = "",
    ):
        self.id = id
        self.description = description
        self.status = status
        self.result = result

    def __str__(self) -> str:
        symbol = {
            "pending": "⏳",
            "running": "🔄",
            "completed": "✅",
            "failed": "❌",
        }.get(self.status, "❓")
        return f"{symbol} Step {self.id} [{self.status.upper()}]: {self.description}"

    def __repr__(self) -> str:
        return f"TaskStep(id={self.id}, status='{self.status}', description='{self.description[:30]}...')"


class Plan:
    def __init__(self, goal: str, steps: Literal[TaskStep]):
        self.goal = goal
        self.steps = steps

    def is_complete(self) -> bool:
        return all(s.status == "completed" for s in self.steps)

    def get_next_step(self) -> TaskStep | None:
        for s in self.steps:
            if s.status == "pending":
                return s
        return None

    def __str__(self) -> str:
        header = f"🎯 Plan Goal: '{self.goal}' ({len(self.steps)} steps)\n"
        steps_str = "\n".join(f"  {str(s)}" for s in self.steps)
        return header + steps_str

    def __repr__(self) -> str:
        return f"Plan(goal='{self.goal}', steps_count={len(self.steps)})"
