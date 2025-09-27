"""
event_bus/factory.py
Factory to select and instantiate the appropriate EventBus implementation.
"""
from .redis_bus import RedisEventBus

class EventBusFactory:
    def __init__(self, provider: str = 'redis', **kwargs):
        if provider == 'redis':
            self.bus = RedisEventBus(**kwargs)
        else:
            raise NotImplementedError(f"Provider {provider} not implemented.")

    async def publish(self, channel: str, message):
        await self.bus.publish(channel, message)

    async def subscribe(self, channel: str, callback):
        await self.bus.subscribe(channel, callback)
