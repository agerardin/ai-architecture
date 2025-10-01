from abc import ABC, abstractmethod
from pydantic import BaseModel


class Capability(BaseModel):
    capability: str
    description: str
    id: str


class Registry(ABC):
    @abstractmethod
    def register_capabilities(self, capabilities: list[Capability]):
        pass

    @abstractmethod
    def get_capability(self, capability: str) -> Capability | None:
        pass
