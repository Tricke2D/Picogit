"""
Status computation - compares working dir, index, and HEAD.
"""

from pathlib import Path

from minigit.core.hashing import compute_object_hash
from minigit.core.index import Index
from minigit.core.object_store import ObjectStore
from minigit.core.objects.commit import Commit
from minigit.core.objects.tree import Tree
from minigit.core.repository import Repository

IGNORED_ENTRIES = {".minigit", ".git", ".venv", "__pycache__"}


def _flatten_tree(tree: Tree, store: ObjectStore, prefix: str = "") -> dict[str, str]:
    """Flatten Tree recursively into dict of path -> blob hash."""
    flat: dict[str, str] = {}
    for entry in tree.entries:
        entry_path = f"{prefix}{entry.name}"
        if entry.obj_type == "blob":
            flat[entry_path] = entry.obj_hash
        else:
            subtree = Tree.load(store, entry.obj_hash)
            flat.update(_flatten_tree(subtree, store, prefix=f"{entry_path}/"))
    return flat


def compute_status(repo: Repository, store: ObjectStore) -> dict[str, list[str]]:
    """
    Returns dict with 3 categories:
    - "staged": files different between index and HEAD
    - "not_staged": files different between working dir and index
    - "untracked": files in working dir not in index
    """
    index = Index.load(repo.index_file)

    active_branch = repo.get_active_branch()
    head_commit_hash = repo.get_branch_commit_hash(active_branch)
    head_entries: dict[str, str] = {}
    if head_commit_hash:
        commit = Commit.load(store, head_commit_hash)
        head_tree = Tree.load(store, commit.tree_hash)
        head_entries = _flatten_tree(head_tree, store)

    working_files: dict[str, bytes] = {}
    for path in repo.working_dir.rglob("*"):
        if path.is_file() and not any(part in IGNORED_ENTRIES for part in path.parts):
            relative = str(path.relative_to(repo.working_dir))
            working_files[relative] = path.read_bytes()

    staged, not_staged, untracked = [], [], []

    for path, blob_hash in index.entries.items():
        if head_entries.get(path) != blob_hash:
            staged.append(path)

    for path, content in working_files.items():
        working_hash = compute_object_hash("blob", content)
        if path not in index.entries:
            untracked.append(path)
        elif index.entries[path] != working_hash:
            not_staged.append(path)

    return {"staged": staged, "not_staged": not_staged, "untracked": untracked}