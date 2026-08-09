"""
Merge command - 3-way merge between branches.
"""

from pathlib import Path

from minigit.core.commit_graph import find_common_ancestor
from minigit.core.merge import merge_file
from minigit.core.object_store import ObjectStore
from minigit.core.objects.blob import Blob
from minigit.core.objects.commit import Commit
from minigit.core.objects.tree import Tree
from minigit.core.repository import Repository
from minigit.core.status import _flatten_tree


def _tree_of_commit(store: ObjectStore, commit_hash: str | None) -> dict[str, str]:
    """Helper: flat dict path->blob_hash from a commit."""
    if commit_hash is None:
        return {}
    commit = Commit.load(store, commit_hash)
    tree = Tree.load(store, commit.tree_hash)
    return _flatten_tree(tree, store)


def _blob_lines(store: ObjectStore, blob_hash: str | None) -> list[str]:
    """Helper: read blob content as list of lines with encoding fallback."""
    if blob_hash is None:
        return []
    content = Blob.load(store, blob_hash).content
    # Try to decode as UTF-8, fallback to replacement for binary files
    try:
        return content.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        # Binary file - return empty list and treat as conflict later
        return []


def run_merge(branch_name: str, author: str = "unknown") -> str:
    """Merge branch into current branch."""
    repo = Repository(working_dir=Path.cwd())
    if not repo.is_initialized():
        raise RuntimeError("Not a Mini Git repository")

    store = ObjectStore(objects_dir=repo.objects_dir)

    active_branch = repo.get_active_branch()
    head_hash = repo.get_branch_commit_hash(active_branch)
    incoming_hash = repo.get_branch_commit_hash(branch_name)

    if head_hash is None or incoming_hash is None:
        raise ValueError("Both branches must have at least one commit.")

    base_hash = find_common_ancestor(store, head_hash, incoming_hash)

    base_files = _tree_of_commit(store, base_hash)
    head_files = _tree_of_commit(store, head_hash)
    incoming_files = _tree_of_commit(store, incoming_hash)

    all_paths = sorted(set(base_files) | set(head_files) | set(incoming_files))
    conflicted_paths: list[str] = []

    for path in all_paths:
        merged_lines, has_conflict = merge_file(
            _blob_lines(store, base_files.get(path)),
            _blob_lines(store, head_files.get(path)),
            _blob_lines(store, incoming_files.get(path)),
        )

        target_path = repo.working_dir / path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text("\n".join(merged_lines) + "\n")

        if has_conflict:
            conflicted_paths.append(path)

    if conflicted_paths:
        raise RuntimeError(
            "Merge stopped due to conflicts in: " + ", ".join(conflicted_paths) +
            ". Resolve conflicts manually, then `minigit add` and `minigit commit`."
        )

    merged_tree = Tree.build_from_directory(repo.working_dir, store)
    tree_hash = merged_tree.save(store)

    merge_commit = Commit.create(
        tree_hash=tree_hash,
        parent_hashes=[head_hash, incoming_hash],
        author=author,
        message=f"Merge branch '{branch_name}' into '{active_branch}'",
    )
    commit_hash = merge_commit.save(store)
    repo.update_branch_ref(active_branch, commit_hash)
    return commit_hash