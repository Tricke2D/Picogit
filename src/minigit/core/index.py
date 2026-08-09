"""
Staging area (index) - tracks files ready for commit.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Index:
    """Staging area: mapping of file path -> blob hash."""

    entries: dict[str, str] = field(default_factory=dict)

    def add(self, relative_path: str, blob_hash: str) -> None:
        """Add or update a staged file."""
        self.entries[relative_path] = blob_hash

    def remove(self, relative_path: str) -> None:
        """Remove a file from staging area."""
        self.entries.pop(relative_path, None)

    def save(self, index_path: Path) -> None:
        """Write index to disk."""
        lines = [
            f"{blob_hash}\t{path}"
            for path, blob_hash in sorted(self.entries.items())
        ]
        index_path.write_text("\n".join(lines) + ("\n" if lines else ""))

    @classmethod
    def load(cls, index_path: Path) -> "Index":
        """Read index from disk."""
        if not index_path.exists():
            return cls()

        entries: dict[str, str] = {}
        for line in index_path.read_text().splitlines():
            if not line:
                continue
            blob_hash, path = line.split("\t")
            entries[path] = blob_hash
        return cls(entries=entries)