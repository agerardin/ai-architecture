"""
event_bus/facade.py
Facade to select and use the appropriate EventBus implementation.
"""
from .base import EventBus
from .redis_bus import RedisEventBus

class EventBusFacade:
    def __init__(self, provider: str = 'redis', **kwargs):
        if provider == 'redis':
            self.bus = RedisEventBus(**kwargs)
        else:
            raise NotImplementedError(f"Provider {provider} not implemented.")

    def publish(self, channel: str, message):
        self.bus.publish(channel, message)

    def subscribe(self, channel: str, callback):
        self.bus.subscribe(channel, callback)
