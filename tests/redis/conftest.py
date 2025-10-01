import os
import pytest
import pytest_asyncio
from ai_architecture.infra.event_bus.redis_bus import RedisEventBus
import redis

# Specify docker-compose files for the test environment
# We could copy file from deploy and update port but for simplicity we keep a separate file here.
DOCKER_COMPOSE_FILES = [
    "tests/redis/docker-compose.yml",
]


# Test robustness settings
MESSAGE_TIMEOUT = int(os.getenv("REDIS_TEST_MESSAGE_TIMEOUT", 10))  # seconds
REDIS_READY_TIMEOUT = float(os.getenv("REDIS_READY_TIMEOUT", 10.0))  # seconds
REDIS_READY_PAUSE = float(os.getenv("REDIS_READY_PAUSE", 0.5))  # seconds


@pytest_asyncio.fixture
async def redis_event_bus(docker_services):
    # NOTE this will attend to start a docker container which may fail if redis is already running locally on this port
    def is_redis_responsive():
        try:
            client = redis.Redis(host="localhost", port=63379, socket_timeout=1)
            client.ping()
            return True
        except Exception:
            return False

    # Wait for Redis to be ready using ping
    docker_services.wait_until_responsive(
        timeout=REDIS_READY_TIMEOUT, pause=REDIS_READY_PAUSE, check=is_redis_responsive
    )

    bus = RedisEventBus(host="localhost", port=63379)
    yield bus
    await bus.close()


# Specify docker-compose files in configurable path
@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return [
        os.path.join(str(pytestconfig.rootdir), path) for path in DOCKER_COMPOSE_FILES
    ]


# Pin the project name to avoid creating multiple stacks
@pytest.fixture(scope="session")
def docker_compose_project_name() -> str:
    return "ai-architecture-tests"


# Stop the stack before starting a new one
@pytest.fixture(scope="session")
def docker_setup():
    return ["down -v", "up --build -d"]
