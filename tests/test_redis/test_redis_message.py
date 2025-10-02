"""
Tests for Redis message publishing and subscribing.
"""

from tests.redis.conftest import MESSAGE_TIMEOUT
import pytest
import asyncio
from ai_architecture.infra.context.context import SessionContext


@pytest.mark.asyncio
async def test_redis_pubsub(redis_event_bus):
    """
    Subscribe to a Redis channel, publish a message, and verify receipt of a session message.
    """
    bus = redis_event_bus
    channel = "test_channel"
    context = SessionContext.create(action="say_hello")
    sub_active = asyncio.Event()
    sub_ready = asyncio.Event()
    messages = asyncio.Queue()

    async def sub_callback(msg):
        await messages.put(msg)
        sub_ready.set()

    async def subscribe_and_signal():
        await bus.subscribe(channel, sub_callback)
        sub_active.set()  # Signal that subscription is active

    # Start subscription and wait for readiness
    asyncio.create_task(subscribe_and_signal())
    await sub_active.wait()

    # Publish a message and wait for delivery
    await bus.publish(channel, context.model_dump())
    await asyncio.wait_for(sub_ready.wait(), timeout=MESSAGE_TIMEOUT)

    # Retrieve a message
    msg = await messages.get()

    # Validate the message content
    assert msg["session_id"] == context.session_id
    assert msg["action"] == "say_hello"
