"""
Copyright 2025 Antoine Gerardin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import asyncio
import json
from redis.asyncio import Redis
from typing import Any, Dict, Callable

from redis.typing import ResponseT
from .event_bus import EventBus


class RedisEventBus(EventBus):
    def __init__(self, host="localhost", port=6379, db=0, redis_client=None):
        if redis_client is not None:
            self.redis = redis_client
        else:
            self.redis = Redis(host=host, port=port, db=db)
        self._subscriptions = {}

    async def publish(self, channel: str, message: Dict[str, Any]) -> ResponseT:
        return await self.redis.publish(channel, json.dumps(message))

    async def subscribe(
        self, channel: str, callback: Callable[[Dict[str, Any]], Any]
    ) -> None:
        key = (channel, id(callback))
        if key in self._subscriptions:
            return

        async def listen():
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(channel)
            async for item in pubsub.listen():
                if item["type"] == "message":
                    data = json.loads(item["data"])
                    result = callback(data)
                    if asyncio.iscoroutine(result):
                        await result

        task = asyncio.create_task(listen())
        self._subscriptions[key] = task

    async def unsubscribe(
        self, channel: str, callback: Callable[[Dict[str, Any]], Any]
    ) -> None:
        key = (channel, id(callback))
        task = self._subscriptions.pop(key, None)
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def close(self):
        tasks = list(self._subscriptions.values())
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        self._subscriptions.clear()
        await self.redis.aclose()
