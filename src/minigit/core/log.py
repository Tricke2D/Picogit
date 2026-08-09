"""
Commit log traversal.
"""

from minigit.core.object_store import ObjectStore
from minigit.core.objects.commit import Commit


def walk_commit_log(store: ObjectStore, start_commit_hash: str) -> list[tuple[str, Commit]]:
    """Walk commit history from start commit, without duplicates."""
    visited: set[str] = set()
    result: list[tuple[str, Commit]] = []
    queue: list[str] = [start_commit_hash]

    while queue:
        current_hash = queue.pop(0)
        if current_hash in visited:
            continue
        visited.add(current_hash)

        commit = Commit.load(store, current_hash)
        result.append((current_hash, commit))
        queue.extend(commit.parent_hashes)

    return result