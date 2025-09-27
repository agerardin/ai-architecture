import os
import pytest_asyncio
from infra.event_bus.redis_bus import RedisEventBus

# Test robustness settings
MESSAGE_TIMEOUT = int(os.getenv("REDIS_TEST_MESSAGE_TIMEOUT", 1))  # seconds
SUBSCRIBE_DELAY = float(os.getenv("REDIS_TEST_SUBSCRIBE_DELAY", 0.5))  # seconds
MAX_RETRIES = int(os.getenv("REDIS_TEST_MAX_RETRIES", 3))
RETRY_DELAY = float(os.getenv("REDIS_TEST_RETRY_DELAY", 1.0))  # seconds
REDIS_READY_TIMEOUT = float(os.getenv("REDIS_READY_TIMEOUT", 10.0))  # seconds
REDIS_READY_PAUSE = float(os.getenv("REDIS_READY_PAUSE", 0.5))  # seconds

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

    # Retry logic for Redis readiness
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Checking Redis readiness (attempt {attempt})...")
        try:
            docker_services.wait_until_responsive(
                timeout=REDIS_READY_TIMEOUT,
                pause=REDIS_READY_PAUSE,
                check=is_redis_responsive
            )
            print("Redis is ready.")
            break
        except Exception as e:
            print(f"Redis not ready (attempt {attempt}): {e}")
            if attempt == MAX_RETRIES:
                raise
            import time
            time.sleep(RETRY_DELAY)

    bus = RedisEventBus()
    yield bus
    await bus.close()
