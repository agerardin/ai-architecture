"""
Factory to instantiate the appropriate EventBus implementation.
"""

from .event_bus import EventBus
from .redis_bus import RedisEventBus

def create_event_bus(provider: str = 'redis', **kwargs) -> EventBus:
    if provider == 'redis':
        return RedisEventBus(**kwargs)
    else:
        raise NotImplementedError(f"Provider {provider} not implemented.")
