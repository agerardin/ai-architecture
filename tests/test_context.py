"""
tests/test_context.py
Unit tests for Context and SessionContext models.
"""
from ai_architecture.infra.context.context import Context, SessionContext

def test_context_instantiation():
    ctx = Context(agent_id="agent-123", action="say_hello", filters={"priority": "high"})
    assert ctx.agent_id == "agent-123"
    assert ctx.action == "say_hello"
    assert ctx.filters is not None
    assert ctx.filters["priority"] == "high"

def test_session_context_creation():
    sctx = SessionContext.create(agent_id="agent-456", action="process", filters={"type": "test"})
    assert sctx.session_id is not None
    assert sctx.agent_id == "agent-456"
    assert sctx.action == "process"
    assert sctx.filters is not None
    assert sctx.filters["type"] == "test"
