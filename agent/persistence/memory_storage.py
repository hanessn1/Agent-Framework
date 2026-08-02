from typing import Dict, List, Any
from .base import BasePersistence


class MemoryPersistence(BasePersistence):
    """Default: Pure in-memory (No-op storage)."""

    def save(self, messages: List[Dict[str, Any]]):
        pass

    def load(self):
        return []
