import pytest
import redis
from ai_architecture.infra.registry.redis_registry import RedisRegistry, Capability


@pytest.fixture(scope="module")
def registry():
    client = redis.Redis(host="localhost", port=63379, socket_timeout=1)
    if not client.ping():
        raise ConnectionError("Could not connect to Redis server at localhost:633379")
    reg = RedisRegistry(redis=client, key="capability_registry")
    reg.r.delete(reg.key)
    yield reg
    reg.r.delete(reg.key)


def test_register_and_get_capability(registry):
    cap = Capability(
        capability="test_capability",
        description="A test capability",
        id="test_id",
    )
    registry.register_capabilities([cap])
    result = registry.get_capability("test_capability")
    assert result is not None
    assert result.capability == "test_capability"
    assert result.description == "A test capability"


def test_list_capabilities(registry):
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
    registry.register_capabilities([cap1, cap2])
    all_caps = registry.list_capabilities()
    assert "cap1" in all_caps and "cap2" in all_caps


def test_remove_capability(registry):
    cap1 = Capability(
        capability="cap1",
        description="First capability",
        id="id1",
    )
    registry.register_capabilities([cap1])
    result = registry.get_capability("cap1")
    assert result is not None
    registry.remove_capability("cap1")
    result = registry.get_capability("cap1")
    assert result is None
