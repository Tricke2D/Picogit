"""
Object store - read/write objects to .minigit/objects/.
"""

from pathlib import Path

from minigit.core.compression import compress_bytes, decompress_bytes
from minigit.core.hashing import build_storable_content, compute_object_hash


class ObjectStore:
    """Mengelola penyimpanan dan pembacaan Git object."""

    def __init__(self, objects_dir: Path) -> None:
        self.objects_dir = objects_dir

    def write_object(self, object_type: str, content: bytes) -> str:
        """
        Menyimpan sebuah objek baru (blob/tree/commit).
        """
        object_hash = compute_object_hash(object_type, content)
        object_path = self._hash_to_path(object_hash)

        if not object_path.exists():
            object_path.parent.mkdir(parents=True, exist_ok=True)
            storable = build_storable_content(object_type, content)
            object_path.write_bytes(compress_bytes(storable))

        return object_hash

    def read_object(self, object_hash: str) -> tuple[str, bytes]:
        """
        Membaca objek berdasarkan hash-nya.
        Returns: (object_type, content)
        """
        object_path = self._hash_to_path(object_hash)
        if not object_path.exists():
            raise FileNotFoundError(f"Object not found: {object_hash}")

        raw = decompress_bytes(object_path.read_bytes())
        header_end = raw.index(b"\0")
        header = raw[:header_end].decode("utf-8")
        object_type, _size = header.split(" ")
        content = raw[header_end + 1:]

        return object_type, content

    def _hash_to_path(self, object_hash: str) -> Path:
        """Mengubah hash 40-karakter jadi path 2/38."""
        return self.objects_dir / object_hash[:2] / object_hash[2:]