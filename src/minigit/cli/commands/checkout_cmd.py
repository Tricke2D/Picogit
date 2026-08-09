"""
Checkout a branch - restore working directory to branch state.
"""

from pathlib import Path

from minigit.core.index import Index
from minigit.core.object_store import ObjectStore
from minigit.core.objects.commit import Commit
from minigit.core.objects.tree import Tree
from minigit.core.repository import Repository
from minigit.core.status import compute_status


def run_checkout(branch_name: str) -> None:
    """Checkout a branch with safety check."""
    repo = Repository(working_dir=Path.cwd())
    if not repo.is_initialized():
        raise RuntimeError("Not a Mini Git repository")

    store = ObjectStore(objects_dir=repo.objects_dir)

    # Safety check: working directory must be clean
    status = compute_status(repo, store)
    if status["staged"] or status["not_staged"]:
        raise RuntimeError(
            "Checkout aborted: there are uncommitted changes. "
            "Commit or discard changes first."
        )

    # Switch HEAD to target branch
    repo.switch_head_to_branch(branch_name)

    # Restore working directory from branch's latest commit
    commit_hash = repo.get_branch_commit_hash(branch_name)
    if commit_hash is not None:
        commit = Commit.load(store, commit_hash)
        tree = Tree.load(store, commit.tree_hash)
        tree.restore_to_directory(repo.working_dir, store)

        # Sync index with restored tree
        new_index = Index()
        _rebuild_index_from_tree(tree, store, new_index)
        new_index.save(repo.index_file)

    print(f"Switched to branch '{branch_name}'")


def _rebuild_index_from_tree(
    tree: Tree, store: ObjectStore, index: Index, prefix: str = ""
) -> None:
    """Recursively rebuild index from tree."""
    for entry in tree.entries:
        entry_path = f"{prefix}{entry.name}"
        if entry.obj_type == "blob":
            index.add(entry_path, entry.obj_hash)
        else:
            subtree = Tree.load(store, entry.obj_hash)
            _rebuild_index_from_tree(subtree, store, index, prefix=f"{entry_path}/")