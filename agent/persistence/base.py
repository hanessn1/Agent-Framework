from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BasePersistence(ABC):
	@abstractmethod
	def save(self, messages: List[Dict[str, Any]]):
		"""Persist message to storage"""
		pass

	@abstractmethod
	def load(self) -> List[Dict[str, Any]]:
		"""Loads messages from storage"""
		pass
