"""
Base class for all Git objects.
"""

from abc import ABC, abstractmethod


class GitObject(ABC):
    """Abstract base class for all Git objects."""

    @abstractmethod
    def serialize(self) -> bytes:
        """Convert object to bytes for storage."""
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, data: bytes) -> "GitObject":
        """Create object from bytes."""
        pass