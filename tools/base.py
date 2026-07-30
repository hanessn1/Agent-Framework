from abc import ABC, abstractmethod


class BaseTool(ABC):
    def __init__(self, name: str, description: str, parameters: dict):
        self.name = name
        self.desciption = description
        self.parameters = parameters

    def schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.desciption,
                "parameters": self.parameters,
            },
        }

    @abstractmethod
    def execute(self, **kwargs):
        pass
