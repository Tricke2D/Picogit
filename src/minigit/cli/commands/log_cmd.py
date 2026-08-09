"""
Show commit history.
"""

from pathlib import Path

from minigit.core.log import walk_commit_log
from minigit.core.object_store import ObjectStore
from minigit.core.repository import Repository


def run_log() -> str:
    """Show commit history from HEAD."""
    repo = Repository(working_dir=Path.cwd())
    if not repo.is_initialized():
        raise RuntimeError("Not a Mini Git repository")

    store = ObjectStore(objects_dir=repo.objects_dir)

    active_branch = repo.get_active_branch()
    head_hash = repo.get_branch_commit_hash(active_branch)
    if head_hash is None:
        return "(no commits yet)"

    entries = walk_commit_log(store, head_hash)

    lines = []
    for commit_hash, commit in entries:
        marker = " (merge)" if commit.is_merge_commit else ""
        lines.append(f"commit {commit_hash}{marker}")
        lines.append(f"Author: {commit.author}")
        lines.append(f"    {commit.message}")
        lines.append("")

    return "\n".join(lines)