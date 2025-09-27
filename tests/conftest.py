import os
import pytest_asyncio
from infra.event_bus.redis_bus import RedisEventBus

# Test robustness settings
MESSAGE_TIMEOUT = int(os.getenv("REDIS_TEST_MESSAGE_TIMEOUT", 2))  # needed to account for message delivery delays
REDIS_READY_TIMEOUT = float(os.getenv("REDIS_READY_TIMEOUT", 4.0))  # seconds
REDIS_READY_PAUSE = float(os.getenv("REDIS_READY_PAUSE", 0.2))  # seconds

@pytest_asyncio.fixture
async def redis_event_bus(docker_services):
    def is_redis_responsive():
        import socket
        try:
            s = socket.create_connection(("localhost", 6379), timeout=1)
            s.close()
            return True
        except Exception:
            return False

    # Wait for Redis to be ready using the correct argument order
    docker_services.wait_until_responsive(
        timeout=REDIS_READY_TIMEOUT,
        pause=REDIS_READY_PAUSE,
        check=is_redis_responsive
    )

    bus = RedisEventBus()
    yield bus
    await bus.close()
