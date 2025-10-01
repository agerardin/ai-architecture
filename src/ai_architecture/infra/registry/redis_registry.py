import redis
from typing import List
from .registry import Registry, Capability


class RedisRegistry(Registry):
    def __init__(self, redis: redis.Redis, key: str = "capability_registry"):
        self.r = redis
        self.key = key

    def register_capabilities(self, capabilities: list[Capability]):
        for capability in capabilities:
            self.r.hset(self.key, capability.capability, capability.model_dump_json())

    def get_capability(self, capability: str) -> Capability | None:
        entry = self.r.hget(self.key, capability)
        if entry:
            return Capability.model_validate_json(entry)
        return None

    def list_capabilities(self) -> List[str]:
        entries = self.r.hgetall(self.key)
        return [k.decode("utf-8") for k in entries.keys()]

    def remove_capability(self, capability: str):
        self.r.hdel(self.key, capability)
