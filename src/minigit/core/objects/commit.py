"""
Commit object - snapshot with metadata and parent link(s).
Now supports multiple parents (merge commits).
"""

import time
from dataclasses import dataclass

from minigit.core.object_store import ObjectStore


@dataclass
class Commit:
    """Objek Commit: metadata + pointer ke Tree dan parent Commit(s)."""

    tree_hash: str
    parent_hashes: list[str]
    author: str
    message: str
    timestamp: int

    def serialize(self) -> bytes:
        """Convert commit to bytes for storage."""
        lines = [f"tree {self.tree_hash}"]
        for parent_hash in self.parent_hashes:
            lines.append(f"parent {parent_hash}")
        lines.append(f"author {self.author} {self.timestamp}")
        lines.append("")
        lines.append(self.message)
        return "\n".join(lines).encode("utf-8")

    def save(self, store: ObjectStore) -> str:
        """Save commit to object store."""
        return store.write_object("commit", self.serialize())

    @classmethod
    def create(
        cls, tree_hash: str, parent_hashes: list[str],
        author: str, message: str,
    ) -> "Commit":
        """Factory method with current timestamp."""
        return cls(
            tree_hash=tree_hash, parent_hashes=parent_hashes,
            author=author, message=message,
            timestamp=int(time.time()),
        )

    @classmethod
    def load(cls, store: ObjectStore, object_hash: str) -> "Commit":
        """Load commit from object store."""
        object_type, content = store.read_object(object_hash)
        if object_type != "commit":
            raise ValueError(f"Expected commit, got {object_type}")

        text = content.decode("utf-8")
        header_part, message = text.split("\n\n", 1)

        tree_hash = ""
        parent_hashes: list[str] = []
        author = ""
        timestamp = 0

        for line in header_part.splitlines():
            if line.startswith("tree "):
                tree_hash = line.removeprefix("tree ")
            elif line.startswith("parent "):
                parent_hashes.append(line.removeprefix("parent "))
            elif line.startswith("author "):
                _, author, ts = line.rsplit(" ", 2)
                timestamp = int(ts)

        return cls(
            tree_hash=tree_hash, parent_hashes=parent_hashes,
            author=author, message=message, timestamp=timestamp,
        )

    @property
    def is_merge_commit(self) -> bool:
        """True if this commit has more than one parent."""
        return len(self.parent_hashes) > 1