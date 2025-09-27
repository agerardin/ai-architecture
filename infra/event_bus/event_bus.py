"""
Defines the abstract EventBus interface for agent communication.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict

class EventBus(ABC):
    @abstractmethod
    async def publish(self, channel: str, message: Dict[str, Any]) -> None:
        """Publish a message to a channel (async)."""
        pass

    @abstractmethod
    async def subscribe(self, channel: str, callback) -> None:
        """Subscribe to a channel with a callback (async)."""
        pass

    @abstractmethod
    async def unsubscribe(self, channel: str, callback) -> None:
        """Unsubscribe the callback from the channel (async)."""
        pass
