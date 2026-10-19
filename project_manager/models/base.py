"""Abstract base for all persisted entities."""
from abc import ABC, abstractmethod
from datetime import datetime, timezone
import uuid


class BaseEntity(ABC):
    """Common identity + timestamp behavior for User, Project, Task."""

    def __init__(self, name: str):
        self._id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.now(timezone.utc).isoformat()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize this object to a plain dict."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """Rebuild this object from a plain dict."""
        ...