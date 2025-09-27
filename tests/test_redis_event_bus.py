"""
tests/test_redis_event_bus.py
Unit test for RedisEventBus using fakeredis.
"""
import pytest
import fakeredis
import json
from infra.event_bus.redis_bus import RedisEventBus

class TestRedisEventBus(RedisEventBus):
    def __init__(self):
        # Use fakeredis for in-memory Redis
        self.redis = fakeredis.FakeRedis()
        self.pubsub = self.redis.pubsub()

@pytest.fixture
def event_bus():
    return TestRedisEventBus()

def test_publish_and_subscribe(event_bus):
    channel = "test_channel"
    message = {"foo": "bar"}
    received = []

    def callback(msg):
        received.append(msg)

    event_bus.subscribe(channel, callback)
    event_bus.publish(channel, message)

    # Give time for thread to process
    import time; time.sleep(0.1)
    assert received[0] == message
