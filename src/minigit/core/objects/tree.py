"""
Tree object - represents folder structure.
"""

from dataclasses import dataclass, field
from pathlib import Path

from minigit.core.object_store import ObjectStore
from minigit.core.objects.blob import Blob

IGNORED_ENTRIES = {".minigit", ".git", ".venv", "__pycache__"}


@dataclass
class TreeEntry:
    """Satu entry di dalam Tree."""

    mode: str      # "100644" (file) atau "040000" (subfolder)
    obj_type: str  # "blob" atau "tree"
    obj_hash: str
    name: str


@dataclass
class Tree:
    """Objek Tree: daftar entry yang merepresentasikan isi satu folder."""

    entries: list[TreeEntry] = field(default_factory=list)

    def serialize(self) -> bytes:
        sorted_entries = sorted(self.entries, key=lambda e: e.name)
        lines = [
            f"{e.mode} {e.obj_type} {e.obj_hash}\t{e.name}"
            for e in sorted_entries
        ]
        return "\n".join(lines).encode("utf-8")

    def save(self, store: ObjectStore) -> str:
        return store.write_object("tree", self.serialize())

    @classmethod
    def build_from_directory(cls, dir_path: Path, store: ObjectStore) -> "Tree":
        """Build Tree recursively from a directory."""
        entries: list[TreeEntry] = []

        for path in sorted(dir_path.iterdir()):
            if path.name in IGNORED_ENTRIES:
                continue

            if path.is_file():
                blob = Blob(content=path.read_bytes())
                blob_hash = blob.save(store)
                entries.append(
                    TreeEntry(mode="100644", obj_type="blob",
                              obj_hash=blob_hash, name=path.name)
                )
            elif path.is_dir():
                subtree = cls.build_from_directory(path, store)
                subtree_hash = subtree.save(store)
                entries.append(
                    TreeEntry(mode="040000", obj_type="tree",
                              obj_hash=subtree_hash, name=path.name)
                )

        return cls(entries=entries)

    @classmethod
    def build_from_index(cls, index, store: ObjectStore) -> "Tree":
        """
        Build Tree from staging area (index), not from filesystem.

        Args:
            index: Index object containing staged files
            store: ObjectStore for saving sub-trees

        Returns:
            Tree object representing the staged files
        """
        # Build nested dictionary structure from flat index
        root: dict = {}
        for path, blob_hash in index.entries.items():
            parts = path.split("/")
            current = root
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = blob_hash

        def _build(node: dict) -> "Tree":
            """Recursively build Tree from nested dict."""
            entries = []
            for name, value in node.items():
                if isinstance(value, dict):
                    # This is a subdirectory - build subtree
                    subtree = _build(value)
                    subtree_hash = subtree.save(store)
                    entries.append(
                        TreeEntry(
                            mode="040000",
                            obj_type="tree",
                            obj_hash=subtree_hash,
                            name=name
                        )
                    )
                else:
                    # This is a file - blob
                    entries.append(
                        TreeEntry(
                            mode="100644",
                            obj_type="blob",
                            obj_hash=value,
                            name=name
                        )
                    )
            return cls(entries=entries)

        return _build(root)

    @classmethod
    def load(cls, store: ObjectStore, object_hash: str) -> "Tree":
        """Load Tree from object store."""
        object_type, content = store.read_object(object_hash)
        if object_type != "tree":
            raise ValueError(f"Expected tree, got {object_type}")

        entries = []
        for line in content.decode("utf-8").splitlines():
            meta, name = line.split("\t")
            mode, obj_type, obj_hash = meta.split(" ")
            entries.append(
                TreeEntry(
                    mode=mode,
                    obj_type=obj_type,
                    obj_hash=obj_hash,
                    name=name
                )
            )
        return cls(entries=entries)

    def restore_to_directory(self, target_dir: Path, store: ObjectStore) -> None:
        """Restore Tree to filesystem."""
        target_dir.mkdir(parents=True, exist_ok=True)

        for entry in self.entries:
            entry_path = target_dir / entry.name

            if entry.obj_type == "blob":
                blob = Blob.load(store, entry.obj_hash)
                entry_path.write_bytes(blob.content)
            elif entry.obj_type == "tree":
                subtree = Tree.load(store, entry.obj_hash)
                subtree.restore_to_directory(entry_path, store)