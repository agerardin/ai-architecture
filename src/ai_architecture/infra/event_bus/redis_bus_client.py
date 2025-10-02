"""
Redis-based implementation of the event bus facade.
"""

import asyncio
import json
import logging
from redis.asyncio import Redis
from typing import Any, Awaitable, Dict, Callable, Union

from redis.typing import ResponseT
from .event_bus_client import EventBusClientFacade


class RedisClientFacade(EventBusClientFacade):
    """Redis-based implementation of the event bus facade.

    This implementation manages per-channel subscriptions and listener tasks.
    """

    def __init__(self, host="localhost", port=6379, db=0, redis_client=None):
        if redis_client is not None:
            self.redis_client = redis_client
        else:
            self.redis_client = Redis(host=host, port=port, db=db)
        self._channel_callbacks = {}  # channel -> set of callbacks
        self._channel_tasks = {}  # channel -> listener task

    async def publish(self, channel: str, message: Dict[str, Any]) -> ResponseT:
        return await self.redis_client.publish(channel, json.dumps(message))

    async def subscribe(
        self,
        channel: str,
        callback: Callable[[Dict[str, Any]], Union[Any, Awaitable[Any]]],
    ) -> None:
        """Subscribes a new callback to a given channel and creates a listener task if needed."""

        # Register the callback
        if channel not in self._channel_callbacks:
            self._channel_callbacks[channel] = set()
        self._channel_callbacks[channel].add(callback)

        # If this is the first callback for the channel, start the listener
        if channel not in self._channel_tasks:

            async def _listen():
                pubsub = self.redis_client.pubsub()
                await pubsub.subscribe(channel)
                async for item in pubsub.listen():
                    # we only care about messages
                    if item["type"] == "message":
                        data = json.loads(item["data"])
                        for cb in list(self._channel_callbacks.get(channel, [])):
                            result = cb(data)
                            if asyncio.iscoroutine(result):
                                await result

            task = asyncio.create_task(_listen())
            self._channel_tasks[channel] = task

    async def unsubscribe(
        self, channel: str, callback: Callable[[Dict[str, Any]], Any]
    ) -> None:
        """Unsubscribes a callback from a given channel and cancels the listener task if no callbacks remain."""

        callbacks = self._channel_callbacks.get(channel)
        if callbacks and callback in callbacks:
            callbacks.remove(callback)
            # If no more callbacks for this channel, cancel the listener
            if not callbacks:
                self._channel_callbacks.pop(channel, None)
                task = self._channel_tasks.pop(channel, None)
                # cancel tasks and log outcome
                if task:
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        logging.info(
                            f"Listener task for channel '{channel}' was cancelled."
                        )
                    if not task.cancelled() and not task.done():
                        logging.warning(
                            f"Listener task for channel '{channel}' was not cancelled as expected."
                        )

    async def close(self):
        """Closes the Redis client and cancels all listener tasks."""

        # Cancel all listener tasks
        tasks = list(self._channel_tasks.values())
        for task in tasks:
            task.cancel()

        # Await cancellation
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, (task_obj, result) in enumerate(zip(tasks, results)):
                if isinstance(result, asyncio.CancelledError):
                    logging.info(f"Listener task {i} was cancelled during close().")
                if not task_obj.cancelled() and not task_obj.done():
                    logging.warning(
                        f"Listener task {i} was not cancelled as expected during close()."
                    )

        # Clear internal state
        self._channel_tasks.clear()
        self._channel_callbacks.clear()

        # Close the Redis client
        await self.redis_client.aclose()
