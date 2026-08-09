"""
Commit graph traversal - find common ancestor for merge.
"""

from minigit.core.object_store import ObjectStore
from minigit.core.objects.commit import Commit


def _collect_ancestors(store: ObjectStore, commit_hash: str) -> set[str]:
    """Collect ALL ancestor commit hashes (including itself) via BFS."""
    visited: set[str] = set()
    queue: list[str] = [commit_hash]

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        commit = Commit.load(store, current)
        queue.extend(commit.parent_hashes)

    return visited


def find_common_ancestor(store: ObjectStore, hash_a: str, hash_b: str) -> str | None:
    """
    Find closest common ancestor between two commits using BFS.
    """
    ancestors_of_a = _collect_ancestors(store, hash_a)

    visited: set[str] = set()
    queue: list[str] = [hash_b]

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        if current in ancestors_of_a:
            return current

        commit = Commit.load(store, current)
        queue.extend(commit.parent_hashes)

    return None