"""
event_bus/base.py
Defines the abstract EventBus interface for agent communication.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict

class EventBus(ABC):
    @abstractmethod
    def publish(self, channel: str, message: Dict[str, Any]) -> None:
        """Publish a message to a channel."""
        pass

    @abstractmethod
    def subscribe(self, channel: str, callback) -> None:
        """Subscribe to a channel with a callback."""
        pass
