"""
event_bus/redis_bus.py
Redis implementation of the EventBus interface.
"""
import redis
import threading
import json
from typing import Any, Dict, Callable
from .base import EventBus

class RedisEventBus(EventBus):
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.pubsub = self.redis.pubsub()

    def publish(self, channel: str, message: Dict[str, Any]) -> None:
        self.redis.publish(channel, json.dumps(message))

    def subscribe(self, channel: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        def listen():
            self.pubsub.subscribe(channel)
            for item in self.pubsub.listen():
                if item['type'] == 'message':
                    data = json.loads(item['data'])
                    callback(data)
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
