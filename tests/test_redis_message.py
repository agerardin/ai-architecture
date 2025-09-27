"""
Tests for Redis message publishing and subscribing.
"""


from conftest import MESSAGE_TIMEOUT
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
    received = asyncio.Queue()
    ready = asyncio.Event()
    subscription_active = asyncio.Event()

    async def callback(msg):
        print("Callback received message:", msg)
        await received.put(msg)
        ready.set()

    async def subscribe_and_signal():
        await bus.subscribe(channel, callback)
        subscription_active.set()  # Signal that subscription is active

    # Start subscription and wait for readiness
    sub_task = asyncio.create_task(subscribe_and_signal())
    await subscription_active.wait()

    # Publish a message and wait for delivery
    await bus.publish(channel, context.model_dump())
    await asyncio.wait_for(ready.wait(), timeout=MESSAGE_TIMEOUT)

    # Retrieve the message
    msg = await received.get()

    # Validate the message content
    assert msg["session_id"] == context.session_id
    assert msg["action"] == "say_hello"
