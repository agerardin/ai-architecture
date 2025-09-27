"""
Redis implementation of the EventBus interface.
"""
import asyncio
import json
from redis.asyncio import Redis
from typing import Any, Dict, Callable
from .event_bus import EventBus

class RedisEventBus(EventBus):
    """
    Async Redis-based EventBus implementation.
    
    Each worker/process should instantiate its own RedisEventBus for isolation.
    Subscriptions are tracked per instance to prevent duplicate (channel, callback) listeners.
    Multiple workers can subscribe to the same channel for parallel processing and load balancing.

    NOTE Currently event bus expect messages to be JSON serializable.
    """

    def __init__(self, host='localhost', port=6379, db=0, redis_client=None):
        # Create a Redis connection (or use provided client)
        if redis_client is not None:
            self.redis = redis_client
        else:
            self.redis = Redis(host=host, port=port, db=db)
        # Track active subscriptions: {(channel, id(callback)): task}
        # This is per instance, ensuring isolation between workers/processes.
        self._subscriptions = {}

    async def publish(self, channel: str, message: Dict[str, Any]) -> None:
        """
        Publish a message to a channel. Message is serialized as JSON.
        """
        await self.redis.publish(channel, json.dumps(message))

    async def subscribe(self, channel: str, callback: Callable[[Dict[str, Any]], Any]) -> None:
        """
        Subscribe to a channel with a callback.
        Prevents duplicate subscriptions for the same channel/callback in this instance.
        The callback is called for each message received on the channel.
        """
        key = (channel, id(callback))
        if key in self._subscriptions:
            # Already subscribed with this callback for this channel
            return

        async def listen():
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(channel)
            async for item in pubsub.listen():
                # Only process actual messages
                if item['type'] == 'message':
                    data = json.loads(item['data'])
                    result = callback(data)
                    if asyncio.iscoroutine(result):
                        await result

        # Start the listener task and track it
        task = asyncio.create_task(listen())
        self._subscriptions[key] = task


    async def unsubscribe(self, channel: str, callback: Callable[[Dict[str, Any]], Any]) -> None:
        """
        Unsubscribe the callback from the channel and cancel the associated task.
        """
        key = (channel, id(callback))
        task = self._subscriptions.pop(key, None)
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def close(self):
        """
        Gracefully cancel all active subscription tasks in parallel and close Redis connection.
        """
        # Cancel all subscription tasks in parallel
        tasks = list(self._subscriptions.values())
        for task in tasks:
            task.cancel()
        if tasks:
            # NOTE gather expect arguments, not a list
            await asyncio.gather(*tasks, return_exceptions=True)
        self._subscriptions.clear()
        # Close Redis connection if possible
        if hasattr(self.redis, 'aclose'):
            await self.redis.aclose()
        elif hasattr(self.redis, 'close'):
            await self.redis.close()