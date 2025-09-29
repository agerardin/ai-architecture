"""
OrchestratorAgent: Coordinates workflows and agent actions via the event bus.
"""

from typing import Any, Dict
from ai_architecture.infra.event_bus.factory import create_event_bus


class OrchestratorAgent:
    def __init__(
        self, agent_id: str = "orchestrator", event_bus_provider: str = "redis"
    ):
        self.agent_id = agent_id
        self.event_bus = create_event_bus(provider=event_bus_provider)
        self._running = False

    async def handle_event(self, event: Dict[str, Any]) -> None:
        """Process an incoming event."""
        print(f"[{self.agent_id}] Received event: {event}")
        # TODO: Add workflow coordination logic here

    async def start(self, channel: str = "workflow_events") -> None:
        """Start the agent and subscribe to the event bus channel."""
        self._running = True

        async def callback(msg: Dict[str, Any]) -> None:
            await self.handle_event(msg)

        await self.event_bus.subscribe(channel, callback)
        print(f"[{self.agent_id}] Subscribed to channel: {channel}")
        # The event loop will schedule callbacks as events arrive; no need to block or sleep here.

    async def stop(self) -> None:
        """Stop the agent."""
        self._running = False
        # TODO: Unsubscribe logic if needed
        print(f"[{self.agent_id}] Stopped.")
