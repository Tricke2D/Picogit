"""
Commit command - snapshot staging area.
"""

from pathlib import Path

from minigit.core.index import Index
from minigit.core.object_store import ObjectStore
from minigit.core.objects.commit import Commit
from minigit.core.objects.tree import Tree
from minigit.core.repository import Repository


def run_commit(message: str, author: str = "unknown") -> str:
    """Commit staged files to repository."""
    repo = Repository(working_dir=Path.cwd())
    if not repo.is_initialized():
        raise RuntimeError("Not a Mini Git repository")

    store = ObjectStore(objects_dir=repo.objects_dir)
    index = Index.load(repo.index_file)

    if not index.entries:
        raise ValueError("Nothing to commit — staging area is empty. Run `minigit add` first.")

    tree = Tree.build_from_index(index, store)
    tree_hash = tree.save(store)

    active_branch = repo.get_active_branch()
    parent_hash = repo.get_branch_commit_hash(active_branch)
    parent_hashes = [parent_hash] if parent_hash else []

    commit = Commit.create(
        tree_hash=tree_hash,
        parent_hashes=parent_hashes,
        author=author,
        message=message,
    )
    commit_hash = commit.save(store)

    repo.update_branch_ref(active_branch, commit_hash)
    return commit_hash