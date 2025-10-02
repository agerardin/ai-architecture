import pytest
import pytest_asyncio
from redis.asyncio import Redis
from ai_architecture.infra.registry.redis_registry import RedisRegistry, Capability


@pytest_asyncio.fixture(scope="function")
async def registry(redis_event_bus):
    client = Redis(host="localhost", port=63379, socket_timeout=1)
    if not await client.ping():
        raise ConnectionError("Could not connect to Redis server at localhost:63379")
    reg = RedisRegistry(redis=client, key="capability_registry")
    await reg.r.delete(reg.key)
    yield reg
    await reg.r.delete(reg.key)


@pytest.mark.asyncio
async def test_register_and_get_capability(registry):
    cap = Capability(
        capability="test_capability",
        description="A test capability",
        id="test_id",
    )
    await registry.register_capabilities([cap])
    result = await registry.get_capability("test_capability")
    assert result is not None
    assert result.capability == "test_capability"
    assert result.description == "A test capability"


@pytest.mark.asyncio
async def test_list_capabilities(registry):
    cap1 = Capability(
        capability="cap1",
        description="First capability",
        id="id1",
    )
    cap2 = Capability(
        capability="cap2",
        description="Second capability",
        id="id2",
    )
    await registry.register_capabilities([cap1, cap2])
    all_caps = await registry.list_capabilities()
    assert "cap1" in all_caps and "cap2" in all_caps


@pytest.mark.asyncio
async def test_remove_capability(registry):
    cap1 = Capability(
        capability="cap1",
        description="First capability",
        id="id1",
    )
    await registry.register_capabilities([cap1])
    result = await registry.get_capability("cap1")
    assert result is not None
    await registry.remove_capability("cap1")
    result = await registry.get_capability("cap1")
    assert result is None
