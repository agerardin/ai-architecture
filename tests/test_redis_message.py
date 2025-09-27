"""
tests/test_redis_message.py
Async integration test: send and receive a message with session_id and say_hello action using RedisEventBus and SessionContext.
"""


import pytest
import asyncio

import pytest_asyncio
from infra.event_bus.redis_bus import RedisEventBus
from infra.context.context import SessionContext

@pytest_asyncio.fixture
async def redis_event_bus():
    bus = RedisEventBus()
    yield bus
    await bus.close()


@pytest.mark.asyncio
async def test_redis_pubsub(docker_services, redis_event_bus):
    bus = redis_event_bus
    channel = "test_channel"
    context = SessionContext.create(action="say_hello")
    received = asyncio.Queue()
    ready = asyncio.Event()

    async def callback(msg):
        print("Callback received message:", msg)
        await received.put(msg)
        ready.set()

    def is_redis_responsive():
        import socket
        try:
            s = socket.create_connection(("localhost", 6379), timeout=1)
            print("Redis is ready.")
            s.close()
            return True
        except Exception:
            print("Redis is not ready. Timing out.")
            return False

    print("Waiting for Redis to be responsive...")
    docker_services.wait_until_responsive(
        timeout=10.0,
        pause=0.5,
        check=is_redis_responsive
    )

    # register subscription callback
    await bus.subscribe(channel, callback)

    # Ensure subscription is active
    await asyncio.sleep(0.1)
    # Publish a message
    await bus.publish(channel, context.model_dump())
    # Signal that event is ready
    await asyncio.wait_for(ready.wait(), timeout=2)
    # Retrieve the message
    msg = await received.get()

    # Validate the message content
    assert msg["session_id"] == context.session_id
    assert msg["action"] == "say_hello"
