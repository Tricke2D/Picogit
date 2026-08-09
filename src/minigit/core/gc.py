"""
Garbage collection - remove unreachable objects.
"""

from minigit.core.object_store import ObjectStore
from minigit.core.objects.commit import Commit
from minigit.core.objects.tree import Tree
from minigit.core.repository import Repository


def _walk_tree(tree_hash: str, store: ObjectStore, reachable: set[str]) -> None:
    """Mark tree and all its contents as reachable."""
    if tree_hash in reachable:
        return
    reachable.add(tree_hash)

    tree = Tree.load(store, tree_hash)
    for entry in tree.entries:
        if entry.obj_type == "blob":
            reachable.add(entry.obj_hash)
        else:
            _walk_tree(entry.obj_hash, store, reachable)


def _walk_commit(commit_hash: str | None, store: ObjectStore, reachable: set[str]) -> None:
    """Mark commit, its tree, and ancestors as reachable."""
    if commit_hash is None or commit_hash in reachable:
        return
    reachable.add(commit_hash)

    commit = Commit.load(store, commit_hash)
    _walk_tree(commit.tree_hash, store, reachable)
    for parent_hash in commit.parent_hashes:
        _walk_commit(parent_hash, store, reachable)


def run_garbage_collection(repo: Repository, store: ObjectStore) -> int:
    """Delete all unreachable objects. Returns number deleted."""
    reachable: set[str] = set()
    for branch_name in repo.list_branches():
        commit_hash = repo.get_branch_commit_hash(branch_name)
        _walk_commit(commit_hash, store, reachable)

    deleted_count = 0
    for object_file in repo.objects_dir.rglob("*"):
        if not object_file.is_file():
            continue
        object_hash = object_file.parent.name + object_file.name
        if object_hash not in reachable:
            object_file.unlink()
            deleted_count += 1

    return deleted_count