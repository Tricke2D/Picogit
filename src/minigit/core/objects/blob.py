"""
Blob object - stores file content (no metadata).
"""

from dataclasses import dataclass

from minigit.core.object_store import ObjectStore


@dataclass
class Blob:
    """Objek Blob: pembungkus tipis untuk isi mentah satu file."""

    content: bytes

    def save(self, store: ObjectStore) -> str:
        """Menyimpan blob ini ke object store."""
        return store.write_object("blob", self.content)

    @classmethod
    def load(cls, store: ObjectStore, object_hash: str) -> "Blob":
        """Memuat Blob dari object store."""
        object_type, content = store.read_object(object_hash)
        if object_type != "blob":
            raise ValueError(f"Expected blob, got {object_type}")
        return cls(content=content)