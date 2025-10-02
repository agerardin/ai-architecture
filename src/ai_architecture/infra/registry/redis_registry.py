import asyncio
from redis.asyncio import Redis
from typing import Awaitable, List, cast, Optional, Dict, Any
from .registry import Registry, Capability


class RedisRegistry(Registry):
    def __init__(self, redis: Redis, key: str = "capability_registry"):
        self.r: Redis = redis
        self.key = key

    async def register_capabilities(self, capabilities: list[Capability]):
        await asyncio.gather(
            *[
                cast(
                    Awaitable[int],
                    self.r.hset(
                        self.key, capability.capability, capability.model_dump_json()
                    ),
                )
                for capability in capabilities
            ]
        )

    async def get_capability(self, capability: str) -> Capability | None:
        entry = await cast(Awaitable[Optional[str]], self.r.hget(self.key, capability))
        if entry:
            return Capability.model_validate_json(entry)
        return None

    async def list_capabilities(self) -> List[str]:
        entries = await cast(Awaitable[Dict[Any, Any]], self.r.hgetall(self.key))
        return [k.decode("utf-8") for k in entries.keys()]

    async def remove_capability(self, capability: str):
        await cast(Awaitable[int], self.r.hdel(self.key, capability))
