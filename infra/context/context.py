"""
context.py
Defines Context and SessionContext models for agent communication using Pydantic.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid

class Context(BaseModel):
    agent_id: Optional[str] = Field(None, description="Target agent ID, if specified.")
    action: Optional[str] = Field(None, description="Requested action for the agent.")
    filters: Optional[Dict[str, Any]] = Field(None, description="Additional filters for routing or processing.")

class SessionContext(Context):
    session_id: str = Field(..., description="Session identifier for tracking requests.")

    @classmethod
    def create(cls, agent_id: Optional[str] = None, action: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> "SessionContext":
        return cls(
            session_id=str(uuid.uuid4()),
            agent_id=agent_id,
            action=action,
            filters=filters
        )
