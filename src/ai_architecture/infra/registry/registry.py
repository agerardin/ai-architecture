from abc import ABC, abstractmethod
from pydantic import BaseModel


class Capability(BaseModel):
    capability: str
    description: str
    id: str


class Registry(ABC):
    @abstractmethod
    async def register_capabilities(self, capabilities: list[Capability]):
        pass

    @abstractmethod
    async def get_capability(self, capability: str) -> Capability | None:
        pass
