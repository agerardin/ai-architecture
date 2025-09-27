"""
Copyright 2025 Antoine Gerardin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
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
