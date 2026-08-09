"""
List tree contents.
"""

from pathlib import Path

from minigit.core.object_store import ObjectStore
from minigit.core.objects.tree import Tree
from minigit.core.repository import Repository


def run_ls_tree(tree_hash: str, recursive: bool = False) -> None:
    repo = Repository(working_dir=Path.cwd())
    if not repo.is_initialized():
        raise RuntimeError("Not a Mini Git repository")

    store = ObjectStore(objects_dir=repo.objects_dir)

    if recursive:
        _ls_tree_recursive(store, tree_hash, "")
    else:
        _ls_tree_flat(store, tree_hash)


def _ls_tree_flat(store: ObjectStore, tree_hash: str) -> None:
    tree = Tree.load(store, tree_hash)
    for entry in sorted(tree.entries, key=lambda e: e.name):
        print(f"{entry.mode} {entry.obj_type} {entry.obj_hash[:8]} {entry.name}")


def _ls_tree_recursive(store: ObjectStore, tree_hash: str, prefix: str) -> None:
    tree = Tree.load(store, tree_hash)
    for entry in sorted(tree.entries, key=lambda e: e.name):
        full_path = f"{prefix}{entry.name}" if prefix else entry.name
        print(f"{entry.mode} {entry.obj_type} {entry.obj_hash[:8]} {full_path}")
        if entry.obj_type == "tree":
            _ls_tree_recursive(store, entry.obj_hash, f"{full_path}/")