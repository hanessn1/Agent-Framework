from typing import List, Dict, Any
from .base import BasePersistence
import json
import os


class JSONPersistence(BasePersistence):
    """Saves and loads message history to/from a JSON file."""

    def __init__(self, filepath: str = "storage/agent_history.json"):
        self.filepath = filepath
        self._ensure_dir_exists()

    def _ensure_dir_exists(self):
        """Ensures the 'data' directory exists."""
        directory = os.path.dirname(self.filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def save(self, messages: List[Dict[str, Any]]):
        with open(self.filepath, "w", encoding="UTF-8") as f:
            json.dump(messages, f, indent=2)

    def load(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="UTF-8") as f:
                    return json.load(f)
            except Exception as e:
                return []
        return []
