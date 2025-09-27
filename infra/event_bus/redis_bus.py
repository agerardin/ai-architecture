"""
infra/event_bus/async_redis_bus.py
Async Redis implementation of the EventBus interface.
"""
import asyncio
import json
from redis.asyncio import Redis
from typing import Any, Dict, Callable
from .base import EventBus

class RedisEventBus(EventBus):
    def __init__(self, host='localhost', port=6379, db=0, redis_client=None):
        if redis_client is not None:
            self.redis = redis_client
        else:
            self.redis = Redis(host=host, port=port, db=db)

    async def publish(self, channel: str, message: Dict[str, Any]) -> None:
        await self.redis.publish(channel, json.dumps(message))

    async def subscribe(self, channel: str, callback: Callable[[Dict[str, Any]], Any]) -> None:
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        async for item in pubsub.listen():
            if item['type'] == 'message':
                data = json.loads(item['data'])
                result = callback(data)
                if asyncio.iscoroutine(result):
                    await result
