"""
Show status of working directory vs index vs HEAD.
"""

from pathlib import Path

from minigit.core.object_store import ObjectStore
from minigit.core.repository import Repository
from minigit.core.status import compute_status


def run_status() -> None:
    """Show working tree status."""
    repo = Repository(working_dir=Path.cwd())
    if not repo.is_initialized():
        raise RuntimeError("Not a Mini Git repository")

    store = ObjectStore(objects_dir=repo.objects_dir)
    status = compute_status(repo, store)

    if status["staged"]:
        print("Staged changes:")
        for path in status["staged"]:
            print(f"  staged: {path}")
    else:
        print("No staged changes")

    if status["not_staged"]:
        print("\nNot staged changes:")
        for path in status["not_staged"]:
            print(f"  modified: {path}")

    if status["untracked"]:
        print("\nUntracked files:")
        for path in status["untracked"]:
            print(f"  untracked: {path}")